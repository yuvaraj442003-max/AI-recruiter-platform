"""
question_generator.py — generates interview questions for a job +
candidate pairing (technical, behavioral, problem-solving; easy/medium/
hard), via the configured LLM. Falls back to a small hand-written
question bank (question_bank.py) keyed by the job's required skills if
no LLM is configured or the call fails, so this is usable immediately
without any API key.

Persisting generated questions into an Interview record happens in
Phase 5, once the interview flow/tables exist — this module only
generates the questions.
"""
import json
import random
import re

from app.ai import llm_service
from app.ai.question_bank import BEHAVIORAL_QUESTIONS, GENERIC_TECHNICAL_QUESTIONS, TECHNICAL_QUESTIONS

SYSTEM_PROMPT = (
    "You generate structured interview questions for an AI recruitment platform. "
    "Respond with ONLY a JSON array of objects matching this exact schema: "
    '{"question": string, "category": "TECHNICAL"|"BEHAVIORAL"|"PROBLEM_SOLVING"|"SYSTEM_DESIGN"|"DOMAIN_KNOWLEDGE"|"COMMUNICATION", '
    '"difficulty": "EASY"|"MEDIUM"|"HARD", "skill": string, "expected_topics": string[], "time_limit_seconds": number}. '
    "CRITICAL RULE: Do NOT invent skills for candidate resume facts. Rely ONLY on evidenced candidate skills. "
    "Do not inflate unevidenced skills (e.g. if candidate resume lists only 'React.js', do not assume 'JavaScript'/'HTML'/'CSS' unless explicitly evidenced)."
)


def _build_user_prompt(
    job_title: str,
    required_skills: list[str],
    experience_years=None,
    num_questions: int = 6,
    candidate_resume_skills: list[str] = None,
    ats_weaknesses: list[str] = None,
    seniority_level: str = "Mid",
    previous_scores: list[float] = None,
) -> str:
    skills_line = ", ".join(required_skills) if required_skills else "general software engineering"
    cand_skills_line = ", ".join(candidate_resume_skills) if candidate_resume_skills else "as listed in resume"
    weaknesses_line = ", ".join(ats_weaknesses) if ats_weaknesses else "none identified"
    exp_line = f"{experience_years} years" if experience_years else "unspecified"

    adaptive_note = ""
    if previous_scores:
        avg_score = sum(previous_scores) / len(previous_scores) if previous_scores else 70.0
        if avg_score >= 80:
            adaptive_note = "Candidate scored high on previous questions. Increase difficulty to HARD."
        elif avg_score < 55:
            adaptive_note = "Candidate struggled on previous questions. Provide clearer, supportive clarification questions."

    return (
        f"Job Title: {job_title} (Seniority: {seniority_level})\n"
        f"Job Required Skills: {skills_line}\n"
        f"Evidenced Candidate Resume Skills: {cand_skills_line}\n"
        f"Candidate Experience: {exp_line}\n"
        f"Identified ATS Weaknesses/Gaps: {weaknesses_line}\n"
        f"{adaptive_note}\n\n"
        f"Generate {num_questions} questions covering TECHNICAL, BEHAVIORAL, PROBLEM_SOLVING, SYSTEM_DESIGN, DOMAIN_KNOWLEDGE, and COMMUNICATION categories."
    )


def _try_parse_json_array(raw: str):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        return None
    return data if isinstance(data, list) else None


def _template_questions(required_skills: list[str], num_questions: int) -> list[dict]:
    """Deterministic fallback built from the hand-written question bank."""
    questions: list[dict] = []

    for skill in (required_skills or ["Python"]):
        for item in TECHNICAL_QUESTIONS.get(skill, []):
            questions.append(
                {
                    "question": item["q"],
                    "category": "TECHNICAL",
                    "type": "technical",
                    "difficulty": item["difficulty"].upper(),
                    "skill": skill,
                    "expected_topics": [skill],
                    "time_limit_seconds": 120,
                }
            )

    if not questions:
        for item in GENERIC_TECHNICAL_QUESTIONS:
            questions.append(
                {
                    "question": item["q"],
                    "category": "TECHNICAL",
                    "type": "technical",
                    "difficulty": item["difficulty"].upper(),
                    "skill": "Software Engineering",
                    "expected_topics": [],
                    "time_limit_seconds": 120,
                }
            )

    random.shuffle(questions)
    questions = questions[: max(num_questions - 2, 1)]

    # Always include behavioral and system design / problem solving
    questions.append(
        {
            "question": random.choice(BEHAVIORAL_QUESTIONS),
            "category": "BEHAVIORAL",
            "type": "behavioral",
            "difficulty": "MEDIUM",
            "skill": "Teamwork",
            "expected_topics": ["teamwork", "communication"],
            "time_limit_seconds": 120,
        }
    )
    questions.append(
        {
            "question": GENERIC_TECHNICAL_QUESTIONS[0]["q"],
            "category": "SYSTEM_DESIGN",
            "type": "problem_solving",
            "difficulty": "HARD",
            "skill": "System Architecture",
            "expected_topics": ["system design", "scalability"],
            "time_limit_seconds": 180,
        }
    )

    return questions[:num_questions]


def generate_interview_questions(
    job_title: str,
    required_skills: list[str],
    experience_years=None,
    num_questions: int = 6,
    candidate_resume_skills: list[str] = None,
    ats_weaknesses: list[str] = None,
    seniority_level: str = "Mid",
    previous_scores: list[float] = None,
) -> dict:
    """Returns {"questions": [...], "source": "llm" | "template"}."""
    llm_output = llm_service.generate(
        SYSTEM_PROMPT,
        _build_user_prompt(
            job_title,
            required_skills,
            experience_years,
            num_questions,
            candidate_resume_skills=candidate_resume_skills,
            ats_weaknesses=ats_weaknesses,
            seniority_level=seniority_level,
            previous_scores=previous_scores,
        ),
        max_tokens=1200,
    )

    if llm_output:
        parsed = _try_parse_json_array(llm_output)
        if parsed:
            questions = [
                {
                    "question": q.get("question", "").strip(),
                    "category": str(q.get("category", "TECHNICAL")).upper(),
                    "type": str(q.get("category", "technical")).lower(),
                    "difficulty": str(q.get("difficulty", "MEDIUM")).upper(),
                    "skill": q.get("skill", (required_skills[0] if required_skills else "General")),
                    "expected_topics": q.get("expected_topics", []) or [],
                    "time_limit_seconds": int(q.get("time_limit_seconds", 120)),
                }
                for q in parsed
                if q.get("question")
            ]
            if questions:
                return {"questions": questions[:num_questions], "source": "llm"}

    return {"questions": _template_questions(required_skills, num_questions), "source": "template"}
