"""
candidate_search_service.py — Smart Candidate Search & Weighted Ranking Engine.

Executes multi-criteria candidate filtering, IT/non-IT skill normalization,
job-specific ATS score calculation, weighted candidate ranking, and pagination.
"""
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.interview import Interview
from app.models.job import Job
from app.models.user import User
from app.services.ats_scoring_service import calculate_job_specific_ats, normalize_skill
from app.services.search_query_parser import parse_search_query

# Configurable ranking weights
CANDIDATE_SEARCH_WEIGHTS: Dict[str, float] = {
    "ats_score": 0.40,
    "skills_match": 0.25,
    "experience_match": 0.15,
    "interview_score": 0.10,
    "education_match": 0.10,
}


def search_and_rank_candidates(
    db: Session,
    query_text: Optional[str] = None,
    job_id: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "best_match",
) -> Dict[str, Any]:
    """
    Executes smart candidate search, parses query, applies filters,
    calculates dynamic job-specific ATS scores, ranks candidates, and paginates.
    """
    # 1. Parse natural language query
    parsed_query_filters = parse_search_query(query_text or "")
    explicit_filters = filters or {}

    # Merge filters (explicit filters override parsed query)
    skills = explicit_filters.get("skills") or parsed_query_filters.get("skills") or []
    skill_match_mode = (explicit_filters.get("skill_match_mode") or "all").lower()

    min_exp = explicit_filters.get("minimum_experience")
    if min_exp is None:
        min_exp = parsed_query_filters.get("minimum_experience")

    max_exp = explicit_filters.get("maximum_experience")
    if max_exp is None:
        max_exp = parsed_query_filters.get("maximum_experience")

    location = explicit_filters.get("location") or parsed_query_filters.get("location")
    min_ats = explicit_filters.get("minimum_ats_score")
    if min_ats is None:
        min_ats = parsed_query_filters.get("minimum_ats_score")

    min_interview = explicit_filters.get("minimum_interview_score")
    education_filter = explicit_filters.get("education")
    job_role_filter = explicit_filters.get("job_role") or parsed_query_filters.get("job_role")

    # Normalize requested skills
    norm_requested_skills = [normalize_skill(s) for s in skills if s]

    # Retrieve selected job if job_id provided
    target_job = None
    explicit_job_id = None
    if job_id:
        try:
            j_uuid = uuid.UUID(job_id)
            target_job = db.query(Job).options(joinedload(Job.job_skills)).filter(Job.id == j_uuid).first()
            explicit_job_id = j_uuid
        except ValueError:
            target_job = None

    # Fallback to first available job if ATS filter is used without job_id
    if not target_job and min_ats is not None:
        target_job = db.query(Job).order_by(Job.created_at.desc()).first()

    # 2. Query Candidate Profiles (Only candidates who have actually applied for jobs)
    query_db = db.query(CandidateProfile).options(
        joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
        joinedload(CandidateProfile.user),
    )

    if explicit_job_id:
        # Target job specified: return ONLY candidates who applied for this specific job
        applied_cand_ids = db.query(Application.candidate_id).filter(Application.job_id == explicit_job_id)
        query_db = query_db.filter(CandidateProfile.id.in_(applied_cand_ids))
    elif job_id:
        # job_id was provided but invalid format/not found -> return no candidates
        applied_cand_ids = db.query(Application.candidate_id).filter(Application.job_id == uuid.uuid4())
        query_db = query_db.filter(CandidateProfile.id.in_(applied_cand_ids))
    else:
        # All Jobs: return all candidates saved in the system database
        pass

    all_candidates = query_db.all()

    matched_results = []

    for cand in all_candidates:
        cand_user = cand.user
        cand_name = cand_user.name if cand_user else "Candidate"
        cand_email = cand_user.email if cand_user else ""

        cand_skills_list = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill]
        cand_skills_norm = {normalize_skill(s).lower(): s for s in cand_skills_list}

        # Skill Matching
        matched_skills = []
        missing_skills = []

        if norm_requested_skills:
            for req_skill in norm_requested_skills:
                req_lower = req_skill.lower()
                if req_lower in cand_skills_norm:
                    matched_skills.append(cand_skills_norm[req_lower])
                else:
                    missing_skills.append(req_skill)

            if skill_match_mode == "all" and len(matched_skills) < len(norm_requested_skills):
                continue
            elif skill_match_mode == "any" and len(matched_skills) == 0:
                continue

        skills_match_pct = (len(matched_skills) / max(len(norm_requested_skills), 1)) * 100.0 if norm_requested_skills else 100.0

        # Experience Filter
        exp_years = float(cand.experience_years or 0.0)
        if min_exp is not None and exp_years < float(min_exp):
            continue
        if max_exp is not None and exp_years > float(max_exp):
            continue

        # Location Filter
        cand_loc = cand.location or ""
        if location and location.strip():
            loc_query = location.strip().lower()
            if loc_query not in cand_loc.lower() and loc_query != "remote":
                continue

        # Job Role Filter
        cand_headline = (cand.headline or cand.current_role or "").lower()
        if job_role_filter and job_role_filter.strip():
            if job_role_filter.strip().lower() not in cand_headline:
                continue

        # Education Filter
        cand_edu = (cand.education or "").lower()
        if education_filter and education_filter.strip():
            if education_filter.strip().lower() not in cand_edu:
                continue

        # Job-Specific ATS Score Calculation
        ats_score = 0.0
        if target_job:
            ats_res = calculate_job_specific_ats(cand, target_job)
            ats_score = float(ats_res["overall_ats_score"])
        else:
            # Baseline ATS quality score
            ats_score = float(cand.profile_score or 75.0)

        # ATS Score Filter
        if min_ats is not None and ats_score < float(min_ats):
            continue

        # Latest Interview Score Retrieval
        latest_interview = (
            db.query(Interview)
            .filter(Interview.candidate_id == cand.id)
            .order_by(Interview.created_at.desc())
            .first()
        )
        interview_score = float(latest_interview.overall_score) if (latest_interview and latest_interview.overall_score is not None) else None

        if min_interview is not None:
            if interview_score is None or interview_score < float(min_interview):
                continue

        # Experience Match Sub-score (100% if meets required exp)
        req_exp = target_job.experience_required if target_job else 2.0
        exp_match_pct = min(100.0, (exp_years / max(req_exp, 1.0)) * 100.0)

        # Education Sub-score
        edu_score = 100.0 if cand.education else 80.0

        # Interview Sub-score
        effective_interview_score = interview_score if interview_score is not None else 75.0

        # Weighted Ranking Score Calculation
        ranking_score = round(
            ats_score * CANDIDATE_SEARCH_WEIGHTS["ats_score"]
            + skills_match_pct * CANDIDATE_SEARCH_WEIGHTS["skills_match"]
            + exp_match_pct * CANDIDATE_SEARCH_WEIGHTS["experience_match"]
            + effective_interview_score * CANDIDATE_SEARCH_WEIGHTS["interview_score"]
            + edu_score * CANDIDATE_SEARCH_WEIGHTS["education_match"],
            1,
        )

        matched_results.append({
            "candidate_id": str(cand.id),
            "candidate_name": cand_name,
            "candidate_email": cand_email,
            "headline": cand.headline or cand.current_role or "Software Professional",
            "job_role": cand.current_role or cand.headline or "Candidate",
            "location": cand.location or "Not Specified",
            "experience_years": exp_years,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "ats_score": round(ats_score, 1),
            "interview_score": round(interview_score, 1) if interview_score is not None else None,
            "ranking_score": ranking_score,
            "education": cand.education or "Not Specified",
        })

    # 3. Sort Results
    if sort_by == "ats_score":
        matched_results.sort(key=lambda x: x["ats_score"], reverse=True)
    elif sort_by == "experience":
        matched_results.sort(key=lambda x: x["experience_years"], reverse=True)
    elif sort_by == "interview_score":
        matched_results.sort(key=lambda x: (x["interview_score"] or 0), reverse=True)
    else:
        # Default: best_match
        matched_results.sort(key=lambda x: x["ranking_score"], reverse=True)

    # 4. Pagination
    total_results = len(matched_results)
    page_size = max(1, page_size)
    total_pages = max(1, (total_results + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * page_size
    paginated_results = matched_results[start_idx : start_idx + page_size]

    return {
        "total_results": total_results,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "filters_applied": {
            "query": query_text,
            "skills": norm_requested_skills,
            "skill_match_mode": skill_match_mode,
            "minimum_experience": min_exp,
            "maximum_experience": max_exp,
            "location": location,
            "minimum_ats_score": min_ats,
            "minimum_interview_score": min_interview,
            "education": education_filter,
            "job_role": job_role_filter,
            "job_id": job_id,
        },
        "results": paginated_results,
    }
