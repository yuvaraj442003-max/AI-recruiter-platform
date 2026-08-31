"""
candidate_comparison.py — Router for Candidate Comparison and AI Recommendation endpoints.
"""
import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job, JobSkill
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.comparison import (
    CandidateComparisonItem,
    CandidateComparisonRequest,
    CandidateComparisonResponse,
    RecommendationData,
)
from app.services.ats_scoring_service import calculate_job_specific_ats
from app.services.candidate_comparison_service import compare_candidates, generate_recommendation

router = APIRouter(prefix="", tags=["Candidate Comparison"])


@router.post("/candidates/compare", response_model=APIResponse[CandidateComparisonResponse])
def compare_candidates_endpoint(
    payload: CandidateComparisonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Compares 2 to 5 candidates for a specific job side-by-side.
    """
    rec_id = current_user.id if current_user.role in [UserRole.recruiter, UserRole.company_admin] else None
    result = compare_candidates(
        db=db,
        recruiter_id=rec_id,
        job_id_str=payload.job_id,
        candidate_ids_str=payload.candidate_ids
    )
    return APIResponse(success=True, message="Candidate Comparison", data=CandidateComparisonResponse(**result))


@router.post("/candidates/recommend", response_model=APIResponse[RecommendationData])
def recommend_candidate_endpoint(
    payload: CandidateComparisonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generates AI Recommendation for candidate selection among compared candidates.
    """
    rec_id = current_user.id if current_user.role in [UserRole.recruiter, UserRole.company_admin] else None
    comp_result = compare_candidates(
        db=db,
        recruiter_id=rec_id,
        job_id_str=payload.job_id,
        candidate_ids_str=payload.candidate_ids
    )
    rec = comp_result["recommendation"]
    return APIResponse(success=True, message="AI Recommendation", data=RecommendationData(**rec))


@router.get("/jobs/{job_id}/matching-candidates", response_model=APIResponse[List[CandidateComparisonItem]])
def get_job_matching_candidates(
    job_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """
    Returns all applicants for a job, pre-analyzed with ATS score breakdowns for comparison selection.
    """
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise NotFoundError("Invalid job ID format.")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == job_uuid)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found.")

    if job.recruiter_id != current_user.id and current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise PermissionDeniedError("You can only view candidates for your own job postings.")

    applications = (
        db.query(Application)
        .options(
            joinedload(Application.candidate).joinedload(CandidateProfile.user),
            joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
        )
        .filter(Application.job_id == job.id)
        .all()
    )

    results = []
    for app in applications:
        cand = app.candidate
        if not cand:
            continue
        user = cand.user
        ats_res = calculate_job_specific_ats(cand, job)
        bd = ats_res["score_breakdown"]

        results.append(
            CandidateComparisonItem(
                candidate_id=str(cand.id),
                application_id=str(app.id),
                candidate_name=user.name if user else "Candidate",
                candidate_email=user.email if user else None,
                headline=getattr(cand, "headline", None) or getattr(cand, "current_role", None) or "Candidate",
                experience_years=cand.experience_years or 0.0,
                education=cand.education or "Not specified",
                location=cand.location or "Not specified",
                overall_ats_score=ats_res["overall_ats_score"],
                skills_match=bd["skills"],
                experience_match=bd["experience"],
                keywords_match=bd["keywords"],
                responsibilities_match=bd["responsibilities"],
                education_match=bd["education"],
                location_match=bd["location"],
                interview_score=app.match_score if hasattr(app, "match_score") else None,
                matched_skills=ats_res["matched_skills"],
                missing_skills=ats_res["missing_skills"],
                matched_keywords=ats_res["matched_keywords"],
                missing_keywords=ats_res["missing_keywords"],
                suggestions=ats_res["suggestions"],
            )
        )

    results.sort(key=lambda x: x.overall_ats_score, reverse=True)
    return APIResponse(success=True, message="Matching Candidates", data=results)
