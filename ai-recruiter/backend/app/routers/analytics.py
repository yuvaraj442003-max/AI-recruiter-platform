"""
Analytics & Recruiter tools endpoints for the recruiter and candidate dashboards.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole
from app.schemas.analytics import CandidateAnalytics, RecruiterAnalytics
from app.schemas.comparison import CandidateCompareRequest, CandidateCompareResponse
from app.schemas.common import APIResponse
from app.services.analytics_service import get_candidate_analytics, get_recruiter_analytics
from app.services.comparison_service import compare_candidates

router = APIRouter(prefix="/analytics", tags=["Analytics"])
recruiter_router = APIRouter(prefix="/recruiter", tags=["Recruiter Tools"])


@router.get("/recruiter", response_model=APIResponse[RecruiterAnalytics])
@recruiter_router.get("/analytics", response_model=APIResponse[RecruiterAnalytics])
def recruiter_analytics(
    job_id: Optional[str] = Query(None, description="Optional job ID filter"),
    start_date: Optional[str] = Query(None, description="Optional start date ISO string"),
    end_date: Optional[str] = Query(None, description="Optional end date ISO string"),
    status: Optional[str] = Query(None, description="Optional status filter"),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin)),
    db: Session = Depends(get_db),
):
    data = get_recruiter_analytics(
        db,
        current_user.id,
        job_id=job_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )
    return APIResponse(success=True, message="Recruiter analytics", data=RecruiterAnalytics(**data))


@recruiter_router.post("/candidates/compare", response_model=APIResponse[CandidateCompareResponse])
def compare_candidates_endpoint(
    payload: CandidateCompareRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin)),
    db: Session = Depends(get_db),
):
    data = compare_candidates(db, current_user.id, payload.job_id, payload.candidate_ids)
    return APIResponse(success=True, message="Candidate comparison report generated", data=CandidateCompareResponse(**data))


@router.get("/candidate", response_model=APIResponse[CandidateAnalytics])
def candidate_analytics(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    data = get_candidate_analytics(db, current_user.id)
    return APIResponse(success=True, message="Candidate analytics", data=CandidateAnalytics(**data))
