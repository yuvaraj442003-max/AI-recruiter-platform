"""
ats.py — Router for job-specific ATS Analysis endpoints.
"""
import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job, JobSkill, JobStatus
from app.models.user import User, UserRole
from app.schemas.ats import ATSAnalysisResponse, JobMatchItem
from app.schemas.common import APIResponse
from app.services.ats_scoring_service import calculate_job_specific_ats

router = APIRouter(prefix="/ats", tags=["ATS Analysis"])


@router.get("/candidate/{candidate_id}/job/{job_id}", response_model=APIResponse[ATSAnalysisResponse])
def get_job_specific_ats_analysis(
    candidate_id: str,
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns full job-specific ATS score analysis breakdown for a candidate & job pair.
    """
    try:
        cand_uuid = uuid.UUID(candidate_id)
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise NotFoundError("Invalid candidate or job ID format.")

    candidate = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == cand_uuid)
        .first()
    )
    if not candidate:
        raise NotFoundError("Candidate profile not found.")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == job_uuid)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found.")

    # Permissions
    is_owning_candidate = current_user.role == UserRole.candidate and candidate.user_id == current_user.id
    is_recruiter = current_user.role in [UserRole.recruiter, UserRole.company_admin] and job.recruiter_id == current_user.id
    is_admin = current_user.role in [UserRole.admin, UserRole.superadmin]

    if not (is_owning_candidate or is_recruiter or is_admin):
        raise PermissionDeniedError("You do not have permission to view this ATS analysis.")

    analysis = calculate_job_specific_ats(candidate, job)
    return APIResponse(success=True, message="ATS Score Analysis", data=ATSAnalysisResponse(**analysis))


@router.get("/candidate/{candidate_id}/matching-jobs", response_model=APIResponse[List[JobMatchItem]])
def get_candidate_job_matches(
    candidate_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Ranks published jobs for candidate based on job-specific ATS match scores.
    """
    try:
        cand_uuid = uuid.UUID(candidate_id)
    except ValueError:
        raise NotFoundError("Invalid candidate ID format.")

    candidate = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == cand_uuid)
        .first()
    )
    if not candidate:
        raise NotFoundError("Candidate profile not found.")

    published_jobs = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.status == JobStatus.published)
        .all()
    )

    results = []
    for job in published_jobs:
        ats_res = calculate_job_specific_ats(candidate, job)
        score = ats_res["overall_ats_score"]
        if score >= 90:
            status_label = "Excellent Match"
        elif score >= 75:
            status_label = "Strong Match"
        elif score >= 60:
            status_label = "Moderate Match"
        else:
            status_label = "Low Match"

        results.append(
            JobMatchItem(
                job_id=str(job.id),
                job_title=job.title,
                company_name=job.company_name,
                location=job.location,
                employment_type=job.employment_type.value if hasattr(job.employment_type, "value") else str(job.employment_type),
                overall_ats_score=score,
                screening_status=status_label,
            )
        )

    results.sort(key=lambda x: x.overall_ats_score, reverse=True)
    return APIResponse(success=True, message="Matching Jobs", data=results)
