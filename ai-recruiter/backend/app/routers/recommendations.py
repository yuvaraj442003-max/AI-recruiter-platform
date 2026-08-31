"""
Job recommendation endpoint — ranks all published jobs against the
current candidate's profile and returns the top matches.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.job import JobResponse
from app.services.job_service import recommend_jobs_for_candidate

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/jobs", response_model=APIResponse[list[dict]])
def get_recommended_jobs(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    scored = recommend_jobs_for_candidate(db, current_user.id, limit=limit)
    data = [
        {
            "job": JobResponse.from_job(item["job"]).model_dump(mode="json"),
            "match_score": item["match_score"],
            "breakdown": item["breakdown"],
        }
        for item in scored
    ]
    return APIResponse(success=True, message="Recommended jobs", data=data)
