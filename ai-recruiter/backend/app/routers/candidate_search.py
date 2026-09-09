"""
candidate_search.py — FastAPI Router endpoints for Recruiter Candidate Search & Advanced Filtering.
"""
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError, BadRequestError
from app.models.user import User, UserRole
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.schemas.candidate_search import (
    CandidateSearchRequest,
    CandidateSearchResponse,
    SavedSearchCreate,
    SavedSearchResponse,
    CandidateInviteRequest,
    BulkInviteRequest,
    CandidateShortlistRequest,
    BulkShortlistRequest,
)
from app.schemas.common import APIResponse
from app.services.candidate_search_service import (
    search_and_rank_candidates,
    save_candidate_search,
    get_saved_searches,
    delete_saved_search,
    get_recent_searches,
    clear_search_history,
    invite_candidate,
    bulk_invite_candidates,
    shortlist_candidate,
    bulk_shortlist_candidates,
    get_candidate_resume_file,
)
from app.services.search_query_parser import parse_search_query
from app.services.ats_scoring_service import calculate_job_specific_ats
from app.models.audit_log import AuditLog

router = APIRouter(prefix="/candidates", tags=["Recruiter Candidate Search"])


@router.post("/smart-search", response_model=APIResponse[CandidateSearchResponse])
def smart_search_candidates_endpoint(
    payload: CandidateSearchRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """
    Performs multi-criteria smart candidate search using natural language query,
    structured filters, IT/non-IT skill normalization, ATS match scoring, qualification thresholding, and weighted ranking.
    """
    filters_dict = payload.filters.model_dump(exclude_none=True) if payload.filters else {}
    thresh = payload.qualification_threshold or (payload.filters.qualification_threshold if payload.filters else 60.0)

    result = search_and_rank_candidates(
        db=db,
        query_text=payload.query,
        job_id=payload.job_id,
        filters=filters_dict,
        qualification_threshold=thresh,
        page=payload.page,
        page_size=payload.page_size,
        sort_by=payload.sort_by,
        recruiter_id=current_user.id,
    )
    return APIResponse(success=True, message="Recruiter Candidate Search Results", data=CandidateSearchResponse(**result))


@router.get("/search", response_model=APIResponse[CandidateSearchResponse])
def search_candidates_get_endpoint(
    q: Optional[str] = Query(None, description="Search query string"),
    job_id: Optional[str] = Query(None, description="Target job ID"),
    min_experience: Optional[float] = Query(None, description="Minimum experience years"),
    max_experience: Optional[float] = Query(None, description="Maximum experience years"),
    location: Optional[str] = Query(None, description="Location text"),
    skills: Optional[str] = Query(None, description="Comma-separated skills"),
    min_ats_score: Optional[float] = Query(None, description="Minimum ATS score"),
    max_ats_score: Optional[float] = Query(None, description="Maximum ATS score"),
    qualification_threshold: Optional[float] = Query(60.0, description="Qualification threshold ATS %"),
    sort: Optional[str] = Query("best_match", description="Sort criteria"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """GET endpoint alias for Recruiter Candidate Search."""
    skill_list = [s.strip() for s in skills.split(",") if s.strip()] if skills else []
    filters_dict = {
        "skills": skill_list,
        "minimum_experience": min_experience,
        "maximum_experience": max_experience,
        "location": location,
        "minimum_ats_score": min_ats_score,
        "maximum_ats_score": max_ats_score,
        "qualification_threshold": qualification_threshold,
    }

    result = search_and_rank_candidates(
        db=db,
        query_text=q or "",
        job_id=job_id,
        filters=filters_dict,
        qualification_threshold=qualification_threshold or 60.0,
        page=page,
        page_size=page_size,
        sort_by=sort or "best_match",
        recruiter_id=current_user.id,
    )
    return APIResponse(success=True, message="Recruiter Candidate Search Results", data=CandidateSearchResponse(**result))


@router.post("/parse-query")
def parse_query_endpoint(
    payload: dict,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
):
    """Extracts structured filters from natural language search query string."""
    query_str = payload.get("query", "")
    extracted = parse_search_query(query_str)
    return APIResponse(success=True, message="Natural language query parsed", data=extracted)


@router.get("/{candidate_id}/resume")
def download_candidate_resume_endpoint(
    candidate_id: str = Path(..., description="Candidate Profile UUID"),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin, UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Securely fetches and downloads candidate resume file.
    Verifies authentication & access permissions. Public static URLs are forbidden.
    """
    try:
        c_uuid = uuid.UUID(candidate_id)
    except ValueError:
        raise BadRequestError("Invalid candidate ID format")

    file_path, filename, media_type = get_candidate_resume_file(db, c_uuid, current_user)
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename,
        headers={"Content-Disposition": f'inline; filename="{filename}"'}
    )


@router.get("/{candidate_id}/ats-report")
def get_candidate_ats_report_endpoint(
    candidate_id: str = Path(..., description="Candidate Profile UUID"),
    job_id: Optional[str] = Query(None, description="Optional target job ID"),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Generates detailed 6-dimension ATS analysis report for candidate."""
    try:
        c_uuid = uuid.UUID(candidate_id)
    except ValueError:
        raise BadRequestError("Invalid candidate ID format")

    profile = db.query(CandidateProfile).filter(CandidateProfile.id == c_uuid).first()
    if not profile:
        raise NotFoundError("Candidate profile not found")

    target_job = None
    if job_id:
        try:
            j_uuid = uuid.UUID(job_id)
            target_job = db.query(Job).filter(Job.id == j_uuid).first()
        except ValueError:
            pass

    if not target_job:
        target_job = db.query(Job).order_by(Job.created_at.desc()).first()

    if not target_job:
        # Construct baseline mock job for report
        target_job = Job(title="Software Engineer", description="General software development position", experience_required=2.0)

    report_data = calculate_job_specific_ats(profile, target_job)

    # Log audit
    db.add(AuditLog(
        user_id=current_user.id,
        action="ats_report_viewed",
        details=f"Viewed ATS report for candidate {candidate_id}",
    ))
    db.commit()

    return APIResponse(success=True, message="Candidate ATS Analysis Report", data=report_data)


# Saved Searches Endpoints
@router.post("/saved-searches", response_model=APIResponse[SavedSearchResponse])
def create_saved_search_endpoint(
    payload: SavedSearchCreate,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    saved = save_candidate_search(
        db=db,
        recruiter_id=current_user.id,
        name=payload.name,
        query=payload.query,
        job_id=payload.job_id,
        filters=payload.filters,
    )
    return APIResponse(
        success=True,
        message="Search criteria saved successfully",
        data=SavedSearchResponse(
            id=str(saved.id),
            recruiter_id=str(saved.recruiter_id),
            name=saved.name,
            query=saved.query,
            job_id=str(saved.job_id) if saved.job_id else None,
            filters=saved.filters or {},
            created_at=saved.created_at,
        ),
    )


@router.get("/saved-searches", response_model=APIResponse[List[SavedSearchResponse]])
def list_saved_searches_endpoint(
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    searches = get_saved_searches(db, current_user.id)
    resp = [
        SavedSearchResponse(
            id=str(s.id),
            recruiter_id=str(s.recruiter_id),
            name=s.name,
            query=s.query,
            job_id=str(s.job_id) if s.job_id else None,
            filters=s.filters or {},
            created_at=s.created_at,
        )
        for s in searches
    ]
    return APIResponse(success=True, message="Saved searches retrieved", data=resp)


@router.delete("/saved-searches/{search_id}")
def delete_saved_search_endpoint(
    search_id: str = Path(...),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        s_uuid = uuid.UUID(search_id)
    except ValueError:
        raise BadRequestError("Invalid saved search ID")

    delete_saved_search(db, current_user.id, s_uuid)
    return APIResponse(success=True, message="Saved search deleted successfully", data={})


# Search History Endpoints
@router.get("/recent-searches")
def get_recent_searches_endpoint(
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    history = get_recent_searches(db, current_user.id)
    return APIResponse(success=True, message="Recent candidate searches", data=history)


@router.delete("/recent-searches")
def clear_recent_searches_endpoint(
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    clear_search_history(db, current_user.id)
    return APIResponse(success=True, message="Search history cleared", data={})


# Direct Invitation & Shortlisting Endpoints
@router.post("/invite")
def invite_candidate_endpoint(
    payload: CandidateInviteRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        c_uuid = uuid.UUID(payload.candidate_id)
        j_uuid = uuid.UUID(payload.job_id)
    except ValueError:
        raise BadRequestError("Invalid candidate or job ID")

    inv = invite_candidate(db, current_user.id, c_uuid, j_uuid, payload.message)
    return APIResponse(success=True, message="Candidate invitation sent successfully", data={"invitation_id": str(inv.id)})


@router.post("/bulk-invite")
def bulk_invite_endpoint(
    payload: BulkInviteRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        j_uuid = uuid.UUID(payload.job_id)
    except ValueError:
        raise BadRequestError("Invalid job ID")

    res = bulk_invite_candidates(db, current_user.id, payload.candidate_ids, j_uuid, payload.message)
    return APIResponse(success=True, message=res["message"], data=res)


@router.post("/shortlist")
def shortlist_candidate_endpoint(
    payload: CandidateShortlistRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        c_uuid = uuid.UUID(payload.candidate_id)
        j_uuid = uuid.UUID(payload.job_id) if payload.job_id else None
    except ValueError:
        raise BadRequestError("Invalid candidate or job ID")

    short = shortlist_candidate(db, current_user.id, c_uuid, j_uuid, payload.notes)
    return APIResponse(success=True, message="Candidate shortlisted successfully", data={"shortlist_id": str(short.id)})


@router.post("/bulk-shortlist")
def bulk_shortlist_endpoint(
    payload: BulkShortlistRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    j_uuid = None
    if payload.job_id:
        try:
            j_uuid = uuid.UUID(payload.job_id)
        except ValueError:
            pass

    res = bulk_shortlist_candidates(db, current_user.id, payload.candidate_ids, j_uuid)
    return APIResponse(success=True, message=res["message"], data=res)


# Singular alias router /api/v1/candidate/smart-search
candidate_singular_router = APIRouter(prefix="/candidate", tags=["Recruiter Candidate Search"])


@candidate_singular_router.post("/smart-search", response_model=APIResponse[CandidateSearchResponse])
def smart_search_candidates_singular_endpoint(
    payload: CandidateSearchRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    return smart_search_candidates_endpoint(payload=payload, current_user=current_user, db=db)


# Recruiter namespace router /api/v1/recruiter/candidates/search
recruiter_candidates_router = APIRouter(prefix="/recruiter/candidates", tags=["Recruiter Candidate Search"])


@recruiter_candidates_router.get("/search", response_model=APIResponse[CandidateSearchResponse])
def recruiter_search_candidates_endpoint(
    q: Optional[str] = Query(None),
    job_id: Optional[str] = Query(None),
    min_experience: Optional[float] = Query(None),
    max_experience: Optional[float] = Query(None),
    location: Optional[str] = Query(None),
    skills: Optional[str] = Query(None),
    min_ats_score: Optional[float] = Query(None),
    max_ats_score: Optional[float] = Query(None),
    qualification_threshold: Optional[float] = Query(60.0),
    sort: Optional[str] = Query("best_match"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    return search_candidates_get_endpoint(
        q=q,
        job_id=job_id,
        min_experience=min_experience,
        max_experience=max_experience,
        location=location,
        skills=skills,
        min_ats_score=min_ats_score,
        max_ats_score=max_ats_score,
        qualification_threshold=qualification_threshold,
        sort=sort,
        page=page,
        page_size=page_size,
        current_user=current_user,
        db=db,
    )
