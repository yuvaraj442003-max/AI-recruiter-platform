"""
candidate_search.py — Fast-API Router endpoints for Smart Candidate Search.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole
from app.schemas.candidate_search import CandidateSearchRequest, CandidateSearchResponse
from app.schemas.common import APIResponse
from app.services.candidate_search_service import search_and_rank_candidates
from app.services.search_query_parser import parse_search_query

router = APIRouter(prefix="/candidates", tags=["Smart Candidate Search"])


@router.post("/smart-search", response_model=APIResponse[CandidateSearchResponse])
def smart_search_candidates_endpoint(
    payload: CandidateSearchRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """
    Performs multi-criteria smart candidate search using natural language query,
    structured filters, IT/non-IT skill normalization, ATS match scoring, and weighted ranking.
    """
    filters_dict = payload.filters.model_dump(exclude_none=True) if payload.filters else {}
    result = search_and_rank_candidates(
        db=db,
        query_text=payload.query,
        job_id=payload.job_id,
        filters=filters_dict,
        page=payload.page,
        page_size=payload.page_size,
        sort_by=payload.sort_by,
    )
    return APIResponse(success=True, message="Smart Candidate Search Results", data=CandidateSearchResponse(**result))


@router.post("/parse-query")
def parse_query_endpoint(
    payload: dict,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
):
    """Extracts structured filters from natural language search query string."""
    query_str = payload.get("query", "")
    extracted = parse_search_query(query_str)
    return APIResponse(success=True, message="Natural language query parsed", data=extracted)


# Singular alias router /api/v1/candidate/smart-search
candidate_singular_router = APIRouter(prefix="/candidate", tags=["Smart Candidate Search"])


@candidate_singular_router.post("/smart-search", response_model=APIResponse[CandidateSearchResponse])
def smart_search_candidates_singular_endpoint(
    payload: CandidateSearchRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    return smart_search_candidates_endpoint(payload=payload, current_user=current_user, db=db)
