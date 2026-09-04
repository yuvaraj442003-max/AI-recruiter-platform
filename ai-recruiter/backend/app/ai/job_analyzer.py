"""
job_analyzer.py — turns a free-form job description into structured
data (title, required skills, preferred skills, experience range) via
the configured LLM, so a recruiter can paste a description and have
the "Post a Job" form pre-filled. Falls back to the Phase 2/3 NLP
skill extraction if no LLM is configured or the call fails/returns
unparseable output.
"""
import json
import re

from app.ai import llm_service
from app.nlp.skill_extractor import EXPERIENCE_RE, extract_skills

SYSTEM_PROMPT = (
    "You analyze job descriptions for a recruitment platform. Extract structured "
    "requirements. Respond with ONLY a JSON object (no markdown, no commentary) "
    "matching this exact shape: "
    '{"title": string, "required_skills": string[], "preferred_skills": string[], '
    '"non_technical_skills": string[], "relevant_work_experience": string, '
    '"company_experience_requirements": string, "experience": string, "responsibilities": string[]}. '
    "Only include skills, titles, and requirements actually stated or clearly implied "
    "by the text. Do not infer anything about the ideal candidate's personal "
    "characteristics."
)


def _build_user_prompt(description: str) -> str:
    return f"Job description:\n\n{description[:4000]}"


def _try_parse_json(raw: str) -> dict | None:
    # Models sometimes wrap JSON in ```json fences despite instructions; strip them.
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(data, dict):
        return None
    return data


def _template_analysis(description: str) -> dict:
    """Deterministic fallback: reuse the Phase 2/3 NLP skill extractor and a
    simple regex for years of experience."""
    skills = extract_skills(description)
    match = EXPERIENCE_RE.search(description)
    experience = f"{match.group(1)}+ years" if match else "Not specified"

    return {
        "title": None,
        "required_skills": skills,
        "preferred_skills": [],
        "non_technical_skills": ["Problem Solving", "Communication", "Team Collaboration"],
        "relevant_work_experience": f"Relevant hands-on role experience matching {skills[:3]} domains.",
        "company_experience_requirements": "Experience in product companies, high-growth startups, or enterprise tech environments.",
        "experience": experience,
        "responsibilities": [],
    }


def analyze_job_description(description: str) -> dict:
    """
    Returns {"title", "required_skills", "preferred_skills", "non_technical_skills",
    "relevant_work_experience", "company_experience_requirements", "experience",
    "responsibilities", "source": "llm" | "template"}.
    """
    llm_output = llm_service.generate(SYSTEM_PROMPT, _build_user_prompt(description), max_tokens=500)

    if llm_output:
        parsed = _try_parse_json(llm_output)
        if parsed:
            return {
                "title": parsed.get("title"),
                "required_skills": parsed.get("required_skills", []) or [],
                "preferred_skills": parsed.get("preferred_skills", []) or [],
                "non_technical_skills": parsed.get("non_technical_skills", []) or [],
                "relevant_work_experience": parsed.get("relevant_work_experience"),
                "company_experience_requirements": parsed.get("company_experience_requirements"),
                "experience": parsed.get("experience"),
                "responsibilities": parsed.get("responsibilities", []) or [],
                "source": "llm",
            }

    result = _template_analysis(description)
    result["source"] = "template"
    return result
