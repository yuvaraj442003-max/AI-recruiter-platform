"""
candidate_comparison_service.py — Side-by-side candidate comparison & AI recommendation logic.

Compares 2–5 candidates for a specific job requisition against:
  - Overall ATS Score
  - 6-part ATS breakdown (skills, experience, keywords, responsibilities, education, location)
  - Interview Score
  - Matched vs Missing Skills

Applies dynamic recommendation formula with RECOMMENDATION_WEIGHTS:
  - ats_score:  40%
  - skills:     20%
  - experience: 20%
  - interview:  15%
  - education:   5%
"""
import json
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session, joinedload

from app.ai.llm_service import generate
from app.core.exceptions import AppError, NotFoundError, PermissionDeniedError
from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.interview import Interview
from app.models.job import Job, JobSkill
from app.services.ats_scoring_service import calculate_job_specific_ats

RECOMMENDATION_WEIGHTS: Dict[str, float] = {
    "ats_score": 0.40,
    "skills": 0.20,
    "experience": 0.20,
    "interview": 0.15,
    "education": 0.05,
}


def compare_candidates(
    db: Session,
    recruiter_id: Optional[uuid.UUID],
    job_id_str: str,
    candidate_ids_str: List[str]
) -> Dict[str, Any]:
    """
    Compares 2 to 5 candidates for a specific job.
    """
    if not candidate_ids_str or len(candidate_ids_str) < 2 or len(candidate_ids_str) > 5:
        raise AppError("Comparison requires between 2 and 5 candidates.", "INVALID_COMPARISON_COUNT", 400)

    # Parse Job
    try:
        job_uuid = uuid.UUID(job_id_str)
    except ValueError:
        raise NotFoundError("Invalid Job ID")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == job_uuid)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found")

    if recruiter_id and job.recruiter_id != recruiter_id:
        raise PermissionDeniedError("You can only compare candidates for your own job postings.")

    # Parse candidate / application UUIDs
    parsed_ids = []
    for c_id in candidate_ids_str:
        try:
            parsed_ids.append(uuid.UUID(c_id.strip()))
        except ValueError:
            pass

    if not parsed_ids:
        raise NotFoundError("No valid candidate or application IDs provided.")

    # Query Candidates and Applications
    candidates = (
        db.query(CandidateProfile)
        .options(
            joinedload(CandidateProfile.user),
            joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
        )
        .filter(
            (CandidateProfile.id.in_(parsed_ids) | CandidateProfile.user_id.in_(parsed_ids))
        )
        .all()
    )

    if len(candidates) < 2:
        # Fallback: check by Application IDs
        apps = (
            db.query(Application)
            .options(
                joinedload(Application.candidate).joinedload(CandidateProfile.user),
                joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
            )
            .filter(Application.id.in_(parsed_ids), Application.job_id == job.id)
            .all()
        )
        candidates = [a.candidate for a in apps if a.candidate]

    if len(candidates) < 2:
        raise NotFoundError("Fewer than 2 valid candidates found for comparison.")

    cand_ids = [c.id for c in candidates]

    # Applications for this job
    applications = (
        db.query(Application)
        .filter(Application.job_id == job.id, Application.candidate_id.in_(cand_ids))
        .all()
    )
    apps_by_cand = {a.candidate_id: a for a in applications}

    # Completed Interviews for this job
    interviews = (
        db.query(Interview)
        .options(joinedload(Interview.evaluation))
        .filter(Interview.job_id == job.id, Interview.candidate_id.in_(cand_ids))
        .all()
    )
    interviews_by_cand = {i.candidate_id: i for i in interviews}

    candidates_list: List[Dict[str, Any]] = []

    for cand in candidates:
        user = cand.user
        c_name = user.name if user else "Candidate"
        c_email = user.email if user else None

        ats_analysis = calculate_job_specific_ats(cand, job)
        app = apps_by_cand.get(cand.id)

        # Interview Score
        interview_obj = interviews_by_cand.get(cand.id)
        eval_obj = interview_obj.evaluation if interview_obj else None
        interview_score = None
        if eval_obj and eval_obj.overall_score is not None:
            interview_score = round(eval_obj.overall_score, 1)
        elif interview_obj and interview_obj.overall_score is not None:
            interview_score = round(interview_obj.overall_score, 1)

        breakdown = ats_analysis["score_breakdown"]

        cand_dict = {
            "candidate_id": str(cand.id),
            "application_id": str(app.id) if app else None,
            "candidate_name": c_name,
            "candidate_email": c_email,
            "headline": getattr(cand, "headline", None) or getattr(cand, "current_role", None) or "Candidate",
            "experience_years": cand.experience_years or 0.0,
            "education": cand.education or "Not specified",
            "location": cand.location or "Not specified",
            "overall_ats_score": ats_analysis["overall_ats_score"],
            "skills_match": breakdown["skills"],
            "experience_match": breakdown["experience"],
            "keywords_match": breakdown["keywords"],
            "responsibilities_match": breakdown["responsibilities"],
            "education_match": breakdown["education"],
            "location_match": breakdown["location"],
            "interview_score": interview_score,
            "matched_skills": ats_analysis["matched_skills"],
            "missing_skills": ats_analysis["missing_skills"],
            "matched_keywords": ats_analysis["matched_keywords"],
            "missing_keywords": ats_analysis["missing_keywords"],
            "suggestions": ats_analysis["suggestions"],
        }

        candidates_list.append(cand_dict)

    # Generate AI Recommendation
    recommendation = generate_recommendation(job, candidates_list)

    return {
        "job_id": str(job.id),
        "job_title": job.title,
        "candidates": candidates_list,
        "recommendation": recommendation,
    }


def generate_recommendation(job: Job, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generates weighted AI recommendation with rationale and potential concerns."""
    # Compute Weighted Recommendation Score for each candidate
    best_cand = None
    best_rec_score = -1.0

    for c in candidates:
        ats_val = c["overall_ats_score"]
        skills_val = c["skills_match"]
        exp_val = c["experience_match"]
        int_val = c["interview_score"] if c["interview_score"] is not None else ats_val
        edu_val = c["education_match"]

        rec_score = round(
            ats_val * RECOMMENDATION_WEIGHTS["ats_score"]
            + skills_val * RECOMMENDATION_WEIGHTS["skills"]
            + exp_val * RECOMMENDATION_WEIGHTS["experience"]
            + int_val * RECOMMENDATION_WEIGHTS["interview"]
            + edu_val * RECOMMENDATION_WEIGHTS["education"],
            1
        )
        c["recommendation_score"] = rec_score
        if rec_score > best_rec_score:
            best_rec_score = rec_score
            best_cand = c

    if not best_cand:
        best_cand = candidates[0]

    # Reasons & Concerns
    reasons = [
        f"Highest overall recommendation score ({best_cand['recommendation_score']}%).",
        f"Strongest skill alignment ({best_cand['skills_match']}% skills match for the selected job).",
    ]
    if best_cand["experience_years"] >= (job.experience_required or 0.0):
        reasons.append(f"Meets relevant experience requirement ({best_cand['experience_years']} yrs vs {job.experience_required or 0.0} yrs required).")
    if best_cand.get("interview_score") and best_cand["interview_score"] >= 80:
        reasons.append(f"Excellent interview evaluation score ({best_cand['interview_score']}%).")
    if best_cand["education_match"] >= 90:
        reasons.append("Meets or exceeds required education background.")

    concerns = []
    if best_cand["missing_skills"]:
        concerns.append(f"Missing specific skills: {', '.join(best_cand['missing_skills'][:3])}.")
    if best_cand["experience_years"] < (job.experience_required or 0.0):
        concerns.append(f"Experience level ({best_cand['experience_years']} yrs) is below required {job.experience_required} yrs.")
    if not concerns:
        concerns.append("No major technical or experience gaps detected.")

    # Try LLM call for extra prompt polishing if LLM is enabled
    c_summaries = []
    for c in candidates:
        c_summaries.append(
            f"- {c['candidate_name']}: ATS={c['overall_ats_score']}%, Skills={c['skills_match']}%, "
            f"Exp={c['experience_years']}yrs, Interview={c.get('interview_score') or 'N/A'}"
        )
    user_prompt = f"Job: {job.title}\nCandidates:\n" + "\n".join(c_summaries)
    system_prompt = "You are a senior talent strategist. Provide 3 short bullet reasons for choosing the best candidate."
    raw_llm = generate(system_prompt, user_prompt, max_tokens=250)
    if raw_llm:
        lines = [line.strip().lstrip("•-* ") for line in raw_llm.splitlines() if line.strip()]
        if len(lines) >= 2:
            reasons = lines[:3]

    return {
        "best_candidate_id": best_cand["candidate_id"],
        "best_candidate_name": best_cand["candidate_name"],
        "recommendation_score": best_cand["recommendation_score"],
        "reason": reasons,
        "concerns": concerns,
    }
