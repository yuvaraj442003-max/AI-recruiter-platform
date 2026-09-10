"""
screening_scoring_service.py — Deterministic Scoring Engine & Recommendation Generator.
Calculates transparent weighted sub-scores and overall recommendation categories
without relying solely on unconstrained LLM opinions.
"""
import logging
from typing import Any, Dict, List

from app.models.screening import ScreeningAnswer, ScreeningQuestion, ScreeningResult, ScreeningSession

logger = logging.getLogger("ai_recruiter.screening_scoring")

# Default weight breakdown across evaluation criteria
DEFAULT_WEIGHTS = {
    "technical": 0.30,
    "experience": 0.20,
    "requirements": 0.20,
    "location": 0.10,
    "notice_period": 0.10,
    "salary": 0.05,
    "communication": 0.05,
}


def calculate_session_scores(session: ScreeningSession) -> Dict[str, Any]:
    """
    Computes deterministic sub-scores and overall match score for a completed screening session.
    """
    question_map = {q.id: q for q in session.questions}
    answers = session.answers

    category_scores = {
        "technical": [],
        "experience": [],
        "requirements": [],
        "location": [],
        "notice_period": [],
        "salary": [],
        "communication": [],
    }

    summary_bullets = []

    for ans in answers:
        q = question_map.get(ans.screening_question_id)
        if not q:
            continue

        score_val = ans.ai_score
        q_type = q.question_type.lower()

        if q_type == "technical":
            category_scores["technical"].append(score_val)
        elif q_type == "experience":
            category_scores["experience"].append(score_val)
        elif q_type == "location" or q_type == "work_mode":
            category_scores["location"].append(score_val)
        elif q_type == "notice_period":
            category_scores["notice_period"].append(score_val)
        elif q_type == "salary":
            category_scores["salary"].append(score_val)
        else:
            category_scores["requirements"].append(score_val)

        # Baseline communication score based on answer responsiveness
        comm_score = 90.0 if len(ans.candidate_answer.strip()) > 3 else 50.0
        category_scores["communication"].append(comm_score)

        # Add itemized bullet summary
        symbol = "✓" if score_val >= 70.0 else "⚠"
        summary_bullets.append(f"{symbol} {q_type.title()}: {ans.ai_reason or 'Response evaluated.'}")

    # Compute category averages
    def get_avg(cat: str, fallback: float = 75.0) -> float:
        vals = category_scores.get(cat, [])
        return round(sum(vals) / len(vals), 1) if vals else fallback

    tech_score = get_avg("technical")
    exp_score = get_avg("experience")
    req_score = get_avg("requirements")
    loc_score = get_avg("location")
    sal_score = get_avg("salary")
    avail_score = get_avg("notice_period")
    comm_score = get_avg("communication")

    # Weighted Overall Score
    overall_score = round(
        (tech_score * DEFAULT_WEIGHTS["technical"])
        + (exp_score * DEFAULT_WEIGHTS["experience"])
        + (req_score * DEFAULT_WEIGHTS["requirements"])
        + (loc_score * DEFAULT_WEIGHTS["location"])
        + (avail_score * DEFAULT_WEIGHTS["notice_period"])
        + (sal_score * DEFAULT_WEIGHTS["salary"])
        + (comm_score * DEFAULT_WEIGHTS["communication"]),
        1,
    )

    # Determine Recommendation Category
    if overall_score >= 85.0:
        recommendation = "Strong Match"
    elif overall_score >= 70.0:
        recommendation = "Shortlist"
    elif overall_score >= 50.0:
        recommendation = "Recruiter Review"
    else:
        recommendation = "Not Recommended"

    ai_summary_text = "\n".join(summary_bullets)

    return {
        "technical_score": tech_score,
        "experience_score": exp_score,
        "location_score": loc_score,
        "salary_score": sal_score,
        "availability_score": avail_score,
        "communication_score": comm_score,
        "overall_score": overall_score,
        "recommendation": recommendation,
        "ai_summary": ai_summary_text,
    }
