"""
resume_summarizer.py — generates a professional summary, key skills
highlight, and technical-strengths blurb from a candidate's parsed
resume, via the configured LLM. Falls back to a deterministic template
built from the Phase 2 NLP extraction if no LLM is configured or the
call fails, so this endpoint always returns something useful.
"""
from app.ai import llm_service

SYSTEM_PROMPT = (
    "You are an assistant that writes concise, factual professional summaries for "
    "candidate resumes, for use by recruiters. Write in third person. Do not invent "
    "any skills, employers, or experience not present in the provided data. Do not "
    "comment on the candidate's name, age, gender, ethnicity, or any other personal "
    "characteristic. Keep the summary to 3-4 sentences."
)


def _build_user_prompt(fields: dict) -> str:
    skills = ", ".join(fields.get("skills", [])) or "not specified"
    experience = fields.get("experience_years")
    experience_line = f"{experience} years of experience" if experience else "experience not specified"
    education = fields.get("education") or "not specified"
    resume_excerpt = (fields.get("resume_text") or "")[:3000]

    return (
        f"Skills: {skills}\n"
        f"Experience: {experience_line}\n"
        f"Education: {education}\n\n"
        f"Resume excerpt:\n{resume_excerpt}\n\n"
        "Write a 3-4 sentence professional summary highlighting this candidate's "
        "key skills, experience level, and technical strengths."
    )


def _template_summary(fields: dict) -> str:
    """Deterministic fallback used when no LLM is configured or the call fails."""
    skills = fields.get("skills", [])
    experience = fields.get("experience_years")
    education = fields.get("education")

    parts = []
    if experience:
        parts.append(f"Candidate with {experience} years of relevant experience.")
    else:
        parts.append("Candidate profile built from an uploaded resume.")

    if skills:
        top_skills = ", ".join(skills[:6])
        parts.append(f"Key skills include {top_skills}.")

    if education:
        first_line = education.splitlines()[0]
        parts.append(f"Education: {first_line}.")

    return " ".join(parts)


def generate_resume_summary(fields: dict) -> dict:
    """
    fields: dict with keys skills (list[str]), experience_years (float|None),
    education (str|None), resume_text (str|None).

    Returns {"summary": str, "source": "llm" | "template"}.
    """
    llm_output = llm_service.generate(SYSTEM_PROMPT, _build_user_prompt(fields), max_tokens=300)
    if llm_output:
        return {"summary": llm_output, "source": "llm"}

    return {"summary": _template_summary(fields), "source": "template"}
