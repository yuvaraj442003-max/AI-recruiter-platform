"""
Ad-hoc match score endpoint — computes a candidate/job match without
creating an Application, so either side can preview it (e.g. a
candidate checking their fit, or a recruiter spot-checking a candidate
against a job they haven't applied to yet).
"""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.ml.ranking import compute_match
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job, JobSkill
from app.models.user import User, UserRole
from app.schemas.application import MatchScoreResponse
from app.schemas.common import APIResponse

router = APIRouter(prefix="/matching", tags=["Matching"])


@router.get("/{candidate_id}/{job_id}", response_model=APIResponse[MatchScoreResponse])
def get_match_score(
    candidate_id: str,
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        parsed_candidate_id = uuid.UUID(candidate_id)
        parsed_job_id = uuid.UUID(job_id)
    except ValueError:
        raise NotFoundError("Candidate or job not found")

    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == parsed_candidate_id)
        .first()
    )
    if not profile:
        raise NotFoundError("Candidate profile not found")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == parsed_job_id)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found")

    is_owning_candidate = current_user.role == UserRole.candidate and profile.user_id == current_user.id
    is_owning_recruiter = current_user.role == UserRole.recruiter and job.recruiter_id == current_user.id
    is_admin = current_user.role == UserRole.admin
    if not (is_owning_candidate or is_owning_recruiter or is_admin):
        raise PermissionDeniedError("You don't have access to this match score.")

    result = compute_match(profile, job)
    return APIResponse(success=True, message="Match score", data=MatchScoreResponse(**result.to_dict()))
