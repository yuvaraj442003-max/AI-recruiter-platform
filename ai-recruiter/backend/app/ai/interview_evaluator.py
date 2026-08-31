"""
interview_evaluator.py — evaluates a single candidate answer (via the
configured LLM) on technical knowledge, relevance, problem solving, and
communication clarity, and separately synthesizes a holistic
interview-level evaluation from all per-answer scores.

Falls back to a deterministic, keyword-overlap heuristic when no LLM is
configured or the call fails — clearly labeled as a low-fidelity
substitute, never presented as equivalent to an LLM's judgment.

Per the platform's fairness requirements: this module never evaluates
or infers personality, emotion, honesty, confidence, or any protected
characteristic. It scores only the content of the answer text against
the question's expected topics and the job's requirements.
"""
import json
import re

from app.ai import llm_service

ANSWER_SYSTEM_PROMPT = (
    "You evaluate a candidate's interview answer for a recruitment platform. "
    "Respond with ONLY a JSON object (no markdown, no commentary) matching this shape: "
    '{"technical_score": number, "relevance_score": number, "problem_solving_score": number, '
    '"communication_score": number, "overall_score": number, "strengths": string[], '
    '"improvements": string[]}. All scores are 0-100. Base the evaluation strictly on the '
    "content of the answer. Do not evaluate or infer the candidate's personality, emotional "
    "state, confidence, honesty, accent, or any protected characteristic — evaluate only what "
    "was said, not how it was said or who said it."
)

INTERVIEW_SYSTEM_PROMPT = (
    "You write a concise, professional interview summary for a recruiter, based on a "
    "candidate's per-question scores from earlier in the interview. Respond with ONLY a "
    "JSON object (no markdown, no commentary) matching this shape: "
    '{"strengths": string[], "weaknesses": string[], "recommendation": string}. '
    "The recommendation should be a short, factual note for the recruiter — never a final "
    "hiring decision; a human recruiter always makes that call. Do not comment on the "
    "candidate's personality, emotional state, or any protected characteristic."
)


def _build_answer_prompt(question: str, expected_topics: list[str], answer_text: str, job_context: str) -> str:
    topics = ", ".join(expected_topics) or "not specified"
    return (
        f"Job context: {job_context[:1000]}\n\n"
        f"Question: {question}\n"
        f"Expected topics: {topics}\n\n"
        f"Candidate's answer:\n{answer_text[:3000]}\n\n"
        "Evaluate this answer."
    )


def _try_parse_json_object(raw: str):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        return None
    return data if isinstance(data, dict) else None


def _template_answer_evaluation(expected_topics: list[str], answer_text: str) -> dict:
    """
    Deterministic fallback: scores relevance by keyword overlap between the
    answer and the question's expected topics, and uses answer length as a
    weak proxy for elaboration. This is intentionally low-fidelity — it's a
    safety net so the platform still functions without an LLM configured,
    not a substitute for real language understanding.
    """
    answer_lower = answer_text.lower()
    word_count = len(answer_text.split())

    if expected_topics:
        matched = sum(1 for topic in expected_topics if topic.lower() in answer_lower)
        relevance_score = round((matched / len(expected_topics)) * 100, 2)
    else:
        relevance_score = 50.0  # neutral — no topics to check against

    # Length-based proxy: longer, more elaborated answers score a bit higher,
    # capped so a wall of text can't game the score.
    length_score = min(100.0, round((word_count / 80) * 100, 2))

    overall = round((relevance_score * 0.6) + (length_score * 0.4), 2)

    strengths = []
    improvements = []
    if relevance_score >= 50:
        strengths.append("Answer addresses several of the expected topics.")
    else:
        improvements.append("Answer could more directly address the key topics for this question.")
    if word_count < 20:
        improvements.append("Consider elaborating further with specific examples.")

    return {
        "technical_score": relevance_score,
        "relevance_score": relevance_score,
        "problem_solving_score": length_score,
        "communication_score": length_score,
        "overall_score": overall,
        "strengths": strengths,
        "improvements": improvements,
    }


def evaluate_answer(question: str, expected_topics: list[str], answer_text: str, job_context: str = "") -> dict:
    """Returns the evaluation dict plus a 'source': 'llm' | 'template' key."""
    llm_output = llm_service.generate(
        ANSWER_SYSTEM_PROMPT,
        _build_answer_prompt(question, expected_topics, answer_text, job_context),
        max_tokens=400,
    )

    if llm_output:
        parsed = _try_parse_json_object(llm_output)
        if parsed and "overall_score" in parsed:
            parsed.setdefault("strengths", [])
            parsed.setdefault("improvements", [])
            parsed["source"] = "llm"
            return parsed

    result = _template_answer_evaluation(expected_topics, answer_text)
    result["source"] = "template"
    return result


def _template_interview_summary(answer_evaluations: list[dict]) -> dict:
    if not answer_evaluations:
        return {"strengths": [], "weaknesses": [], "recommendation": "No answers were submitted."}

    avg_overall = sum(a["overall_score"] for a in answer_evaluations) / len(answer_evaluations)

    strengths = []
    weaknesses = []
    for evaluation in answer_evaluations:
        strengths.extend(evaluation.get("strengths", []))
        weaknesses.extend(evaluation.get("improvements", []))

    # De-duplicate while preserving order, cap length.
    strengths = list(dict.fromkeys(strengths))[:5]
    weaknesses = list(dict.fromkeys(weaknesses))[:5]

    if avg_overall >= 70:
        recommendation = "Candidate's answers were strong overall. Recommend proceeding to the next stage."
    elif avg_overall >= 45:
        recommendation = "Candidate showed mixed results. Recommend a closer review of individual answers."
    else:
        recommendation = "Candidate's answers showed significant gaps. Recommend caution before proceeding."

    return {"strengths": strengths, "weaknesses": weaknesses, "recommendation": recommendation}


def evaluate_interview(job_title: str, answer_evaluations: list[dict]) -> dict:
    """
    Synthesizes per-answer evaluations (each a dict from evaluate_answer)
    into a holistic interview-level summary. Numeric category scores are
    always computed as straightforward averages (never LLM-guessed), so
    they stay consistent with the per-answer scores shown to the
    recruiter; only the strengths/weaknesses/recommendation text is
    optionally LLM-generated.
    """
    if not answer_evaluations:
        return {
            "technical_score": None,
            "communication_score": None,
            "relevance_score": None,
            "problem_solving_score": None,
            "overall_score": None,
            "strengths": [],
            "weaknesses": [],
            "recommendation": "No answers were submitted.",
            "source": "template",
        }

    def avg(key: str) -> float:
        values = [a.get(key, 0) for a in answer_evaluations]
        return round(sum(values) / len(values), 2)

    scores = {
        "technical_score": avg("technical_score"),
        "communication_score": avg("communication_score"),
        "relevance_score": avg("relevance_score"),
        "problem_solving_score": avg("problem_solving_score"),
        "overall_score": avg("overall_score"),
    }

    summary_prompt = (
        f"Job: {job_title}\n\n"
        f"Average scores across {len(answer_evaluations)} answers: "
        f"technical={scores['technical_score']}, relevance={scores['relevance_score']}, "
        f"problem_solving={scores['problem_solving_score']}, communication={scores['communication_score']}\n\n"
        "Write a short strengths/weaknesses/recommendation summary based on these scores."
    )
    llm_output = llm_service.generate(INTERVIEW_SYSTEM_PROMPT, summary_prompt, max_tokens=300)

    if llm_output:
        parsed = _try_parse_json_object(llm_output)
        if parsed and "recommendation" in parsed:
            return {
                **scores,
                "strengths": parsed.get("strengths", []) or [],
                "weaknesses": parsed.get("weaknesses", []) or [],
                "recommendation": parsed.get("recommendation", ""),
                "source": "llm",
            }

    template_summary = _template_interview_summary(answer_evaluations)
    return {**scores, **template_summary, "source": "template"}
