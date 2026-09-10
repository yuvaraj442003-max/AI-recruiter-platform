"""
screening_ai_service.py — AI Service for Screening Question Generation & Natural Language Extraction.
Leverages app/ai/llm_service.py with deterministic fallback rules when no LLM key is configured.
"""
import json
import logging
import re
from typing import Any, Dict, List, Optional

from app.ai import llm_service

logger = logging.getLogger("ai_recruiter.screening_ai")

# Intent keywords for opting out of automated messages
OPT_OUT_KEYWORDS = {"stop", "opt out", "opt-out", "unsubscribe", "cancel", "quit", "dont message me", "stop messaging"}


def check_is_opt_out(text: str) -> bool:
    """Checks if the candidate reply expresses a desire to stop receiving automated messages."""
    clean = text.strip().lower()
    return any(kw in clean for kw in OPT_OUT_KEYWORDS)


def generate_job_questions(job_data: Dict[str, Any], candidate_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Generates job-tailored screening questions.
    Uses LLM if available, otherwise builds structured fallback questions based on job properties.
    """
    job_title = job_data.get("title", "Position")
    req_exp = job_data.get("experience_required") or job_data.get("min_experience") or 0.0
    location = job_data.get("location") or "Remote / Office"
    salary = job_data.get("salary_range") or "Market competitive"
    skills = job_data.get("skills") or []
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]

    system_prompt = (
        "You are an expert AI Recruiting Coordinator. Generate a concise, natural pre-screening interview questionnaire "
        "for a job applicant. Return ONLY a valid JSON list of question objects with keys:\n"
        "- 'question': clear conversational question text\n"
        "- 'question_type': one of ('experience', 'technical', 'location', 'notice_period', 'salary', 'work_mode')\n"
        "- 'expected_answer': brief description of ideal answer criteria\n"
        "- 'weight': float weight between 0.5 and 1.5\n"
        "Ensure questions are polite, non-repetitive, and directly relevant to job requirements."
    )

    user_prompt = (
        f"Job Title: {job_title}\n"
        f"Required Experience: {req_exp} years\n"
        f"Location: {location}\n"
        f"Salary Range: {salary}\n"
        f"Key Required Skills: {', '.join(skills) if skills else 'Relevant skills'}\n"
        f"Generate 5 high-impact screening questions."
    )

    llm_output = llm_service.generate(system_prompt, user_prompt, max_tokens=700)
    if llm_output:
        try:
            # Strip markdown code blocks if returned
            clean_json = re.sub(r"^```json\s*", "", llm_output, flags=re.MULTILINE)
            clean_json = re.sub(r"```$", "", clean_json, flags=re.MULTILINE).strip()
            parsed = json.loads(clean_json)
            if isinstance(parsed, list) and len(parsed) >= 3:
                questions = []
                for idx, q in enumerate(parsed):
                    questions.append({
                        "question": q.get("question", f"Question {idx+1}"),
                        "question_type": q.get("question_type", "technical"),
                        "expected_answer": q.get("expected_answer", ""),
                        "weight": float(q.get("weight", 1.0)),
                        "sequence": idx + 1,
                    })
                return questions
        except Exception as err:
            logger.warning(f"Failed to parse LLM screening questions JSON: {err}. Using deterministic questions.")

    # --- Deterministic Fallback Question Generation ---
    questions = []
    seq = 1

    # 1. Experience Question
    questions.append({
        "question": f"How many years of professional experience do you have related to {job_title}?",
        "question_type": "experience",
        "expected_answer": f"At least {req_exp} years of relevant experience",
        "weight": 1.2,
        "sequence": seq,
    })
    seq += 1

    # 2. Key Skills Question
    if skills:
        top_skills = ", ".join(skills[:3])
        questions.append({
            "question": f"Which of these key skills do you have hands-on production experience with: {top_skills}?",
            "question_type": "technical",
            "expected_answer": f"Hands-on experience in {top_skills}",
            "weight": 1.3,
            "sequence": seq,
        })
        seq += 1

    # 3. Location / Work Mode Question
    questions.append({
        "question": f"Are you comfortable working in or relocating to {location}?",
        "question_type": "location",
        "expected_answer": f"Willing to work at / relocate to {location}",
        "weight": 1.0,
        "sequence": seq,
    })
    seq += 1

    # 4. Notice Period / Availability Question
    questions.append({
        "question": "What is your current notice period or earliest available start date?",
        "question_type": "notice_period",
        "expected_answer": "30 days or immediate availability preferred",
        "weight": 1.0,
        "sequence": seq,
    })
    seq += 1

    # 5. Expected Salary Question
    questions.append({
        "question": f"What is your expected annual salary for this role (Current range: {salary})?",
        "question_type": "salary",
        "expected_answer": f"Within budget range ({salary})",
        "weight": 0.8,
        "sequence": seq,
    })

    return questions


def extract_answer_structured(
    question_text: str,
    question_type: str,
    expected_criteria: str,
    candidate_answer: str,
    job_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Extracts structured entities, scores response (0-100), and checks opt-out status.
    """
    if check_is_opt_out(candidate_answer):
        return {
            "extracted_value": {"opt_out": True},
            "ai_score": 0.0,
            "ai_reason": "Candidate opted out of automated pre-screening messages.",
            "is_opt_out": True,
        }

    system_prompt = (
        "You are an AI Screening Evaluation Agent. Analyze a candidate's answer to a screening question.\n"
        "Return ONLY a valid JSON object with keys:\n"
        "- 'extracted_entities': dict of extracted numeric/boolean facts (e.g. {'experience_years': 4, 'confirmed': true})\n"
        "- 'score': float (0.0 to 100.0) evaluating how well the response satisfies expected criteria\n"
        "- 'reason': brief 1-sentence evaluation justification"
    )

    user_prompt = (
        f"Question ({question_type}): \"{question_text}\"\n"
        f"Expected Criteria: \"{expected_criteria}\"\n"
        f"Candidate Answer: \"{candidate_answer}\"\n"
        f"Extract facts and evaluate match."
    )

    llm_output = llm_service.generate(system_prompt, user_prompt, max_tokens=300)
    if llm_output:
        try:
            clean_json = re.sub(r"^```json\s*", "", llm_output, flags=re.MULTILINE)
            clean_json = re.sub(r"```$", "", clean_json, flags=re.MULTILINE).strip()
            parsed = json.loads(clean_json)
            return {
                "extracted_value": parsed.get("extracted_entities", {}),
                "ai_score": float(parsed.get("score", 75.0)),
                "ai_reason": parsed.get("reason", "Answer parsed successfully."),
                "is_opt_out": False,
            }
        except Exception as err:
            logger.warning(f"Error parsing LLM answer extraction: {err}. Using rule-based fallback.")

    # --- Rule-Based Deterministic Extraction Fallback ---
    extracted = {}
    score = 75.0
    reason = "Candidate response recorded."

    # Extract numbers (years of exp, notice days, salary)
    numbers = re.findall(r"\d+(?:\.\d+)?", candidate_answer)
    num_val = float(numbers[0]) if numbers else None

    if question_type == "experience":
        if num_val is not None:
            extracted["experience_years"] = num_val
            req = (job_data or {}).get("experience_required") or 0.0
            if num_val >= req:
                score = 95.0
                reason = f"Candidate confirmed {num_val} years experience, meeting requirements ({req} yrs)."
            else:
                score = max(40.0, (num_val / max(req, 1.0)) * 90.0)
                reason = f"Candidate has {num_val} years experience, below required {req} years."
        else:
            score = 70.0
            reason = "Experience stated in narrative format."

    elif question_type == "notice_period":
        if num_val is not None:
            extracted["notice_period_days"] = int(num_val)
            if num_val <= 30:
                score = 95.0
                reason = f"Notice period of {int(num_val)} days is acceptable."
            else:
                score = 70.0
                reason = f"Notice period of {int(num_val)} days is longer than preferred 30 days."
        else:
            extracted["immediate"] = "immediate" in candidate_answer.lower() or "yes" in candidate_answer.lower()
            score = 90.0 if extracted["immediate"] else 75.0
            reason = "Availability response captured."

    elif question_type == "location":
        affirmatives = {"yes", "sure", "comfortable", "ready", "relocate", "open", "yeah", "ok", "okay"}
        is_yes = any(aff in candidate_answer.lower() for aff in affirmatives)
        extracted["location_confirmed"] = is_yes
        score = 95.0 if is_yes else 40.0
        reason = "Location/relocation willingness confirmed." if is_yes else "Location requirement not confirmed."

    elif question_type == "salary":
        if num_val is not None:
            extracted["expected_salary"] = num_val
            score = 85.0
            reason = f"Expected salary of {num_val} recorded."
        else:
            score = 80.0
            reason = "Salary expectations recorded."
    else:
        score = 85.0
        reason = "Relevant candidate response recorded."

    return {
        "extracted_value": extracted,
        "ai_score": score,
        "ai_reason": reason,
        "is_opt_out": False,
    }
