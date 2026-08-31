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
    "You generate interview questions for a recruitment platform. Respond with ONLY "
    "a JSON array (no markdown, no commentary) of objects matching this shape: "
    '{"question": string, "type": "technical"|"behavioral"|"problem_solving", '
    '"difficulty": "easy"|"medium"|"hard", "expected_topics": string[]}. '
    "Base technical questions on the job's required skills. Do not ask about the "
    "candidate's age, background, appearance, or any other personal characteristic "
    "unrelated to job qualifications."
)


def _build_user_prompt(
    job_title: str, required_skills: list[str], experience_years, num_questions: int
) -> str:
    skills_line = ", ".join(required_skills) or "general software engineering"
    experience_line = f"{experience_years} years" if experience_years else "unspecified"
    return (
        f"Job title: {job_title}\n"
        f"Required skills: {skills_line}\n"
        f"Candidate experience: {experience_line}\n\n"
        f"Generate {num_questions} interview questions: a mix of technical questions on the "
        "required skills, one behavioral question, and one problem-solving/system-design "
        "question. Vary the difficulty (easy/medium/hard) appropriately for the experience level."
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

    for skill in required_skills:
        for item in TECHNICAL_QUESTIONS.get(skill, []):
            questions.append(
                {
                    "question": item["q"],
                    "type": "technical",
                    "difficulty": item["difficulty"],
                    "expected_topics": [skill],
                }
            )

    if not questions:
        for item in GENERIC_TECHNICAL_QUESTIONS:
            questions.append(
                {"question": item["q"], "type": "technical", "difficulty": item["difficulty"], "expected_topics": []}
            )

    random.shuffle(questions)
    questions = questions[: max(num_questions - 2, 1)]

    # Always include at least one behavioral and one problem-solving/system-design question.
    questions.append(
        {
            "question": random.choice(BEHAVIORAL_QUESTIONS),
            "type": "behavioral",
            "difficulty": "medium",
            "expected_topics": ["teamwork", "communication"],
        }
    )
    questions.append(
        {
            "question": GENERIC_TECHNICAL_QUESTIONS[0]["q"],
            "type": "problem_solving",
            "difficulty": "hard",
            "expected_topics": ["system design"],
        }
    )

    return questions[:num_questions]


def generate_interview_questions(
    job_title: str,
    required_skills: list[str],
    experience_years=None,
    num_questions: int = 6,
) -> dict:
    """Returns {"questions": [...], "source": "llm" | "template"}."""
    llm_output = llm_service.generate(
        SYSTEM_PROMPT,
        _build_user_prompt(job_title, required_skills, experience_years, num_questions),
        max_tokens=1000,
    )

    if llm_output:
        parsed = _try_parse_json_array(llm_output)
        if parsed:
            questions = [
                {
                    "question": q.get("question", "").strip(),
                    "type": q.get("type", "technical"),
                    "difficulty": q.get("difficulty", "medium"),
                    "expected_topics": q.get("expected_topics", []) or [],
                }
                for q in parsed
                if q.get("question")
            ]
            if questions:
                return {"questions": questions[:num_questions], "source": "llm"}

    return {"questions": _template_questions(required_skills, num_questions), "source": "template"}
