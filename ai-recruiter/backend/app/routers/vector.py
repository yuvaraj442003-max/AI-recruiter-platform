"""
vector.py — API endpoints for Qdrant Vector Database operations.

Endpoints:
- GET  /api/v1/vector/health: Checks Qdrant connectivity and collection point statistics.
- POST /api/v1/vector/sync: Synchronizes relational database records (Jobs, Resumes, Aptitude, Coding, Interviews, Materials) into Qdrant.
- POST /api/v1/vector/search: Semantic similarity retrieval with metadata filtering.
- POST /api/v1/vector/check-duplicate: Semantic duplicate detection (e.g. for Aptitude questions).
"""
import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.vector import (
    VectorDuplicateCheckRequest,
    VectorDuplicateCheckResponse,
    VectorHealthResponse,
    VectorSearchRequest,
    VectorSearchResponse,
    VectorSearchResultItem,
    VectorSyncResponse,
)
from app.services.qdrant_service import (
    ALL_COLLECTIONS,
    COLLECTION_RESUMES,
    check_aptitude_question_duplicate,
    ensure_collections,
    get_health_status,
    search,
    sync_all_from_db,
)

logger = logging.getLogger("ai_recruiter.vector_router")

router = APIRouter(prefix="/vector", tags=["Vector Database (Qdrant)"])


@router.get("/health", response_model=APIResponse[VectorHealthResponse])
def get_vector_health():
    """Returns Qdrant vector database health, connectivity mode, and collection point counts."""
    health_data = get_health_status()
    return APIResponse(
        success=True,
        message="Vector database status",
        data=VectorHealthResponse(**health_data),
    )


@router.post("/sync", response_model=APIResponse[VectorSyncResponse])
def trigger_vector_sync(
    background_tasks: BackgroundTasks,
    background: bool = False,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter, UserRole.superadmin)),
    db: Session = Depends(get_db),
):
    """
    Synchronizes existing relational database entities (Jobs, Resumes, Aptitude Questions,
    Coding Challenges, Interviews, Study Materials) into their respective Qdrant collections.
    """
    ensure_collections()

    if background and background_tasks:
        # Run in background task using fresh DB session if needed
        def _run_bg_sync():
            from app.core.database import SessionLocal
            bg_db = SessionLocal()
            try:
                sync_all_from_db(bg_db)
            finally:
                bg_db.close()

        background_tasks.add_task(_run_bg_sync)
        return APIResponse(
            success=True,
            message="Vector synchronization started in background task.",
            data=VectorSyncResponse(status="started", message="Background synchronization initiated."),
        )

    res = sync_all_from_db(db)
    return APIResponse(
        success=res.get("status") == "success",
        message=res.get("message", "Synchronization executed"),
        data=VectorSyncResponse(
            status=res.get("status", "completed"),
            message=res.get("message", ""),
            counts=res.get("counts", {}),
        ),
    )


@router.post("/search", response_model=APIResponse[VectorSearchResponse])
def semantic_search_endpoint(
    payload: VectorSearchRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Performs semantic vector search across a specified collection with optional metadata filters.
    Role-based privacy: Candidates cannot query the raw 'resumes' collection.
    """
    collection = payload.collection.strip().lower()
    if collection not in ALL_COLLECTIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid collection '{collection}'. Must be one of: {', '.join(ALL_COLLECTIONS)}",
        )

    # Privacy guard: Candidate cannot search other candidate resumes
    if collection == COLLECTION_RESUMES and current_user.role not in [
        UserRole.recruiter,
        UserRole.admin,
        UserRole.superadmin,
        UserRole.company_admin,
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Candidate resume search is restricted to recruiters and administrators.",
        )

    raw_results = search(
        collection_name=collection,
        query_text=payload.query,
        limit=payload.limit,
        score_threshold=payload.score_threshold,
        filter_dict=payload.filter,
    )

    items = [
        VectorSearchResultItem(
            id=r["id"],
            score=r["score"],
            similarity_pct=r["similarity_pct"],
            payload=r["payload"],
        )
        for r in raw_results
    ]

    return APIResponse(
        success=True,
        message=f"Semantic search completed for '{collection}'. Found {len(items)} results.",
        data=VectorSearchResponse(
            collection=collection,
            query=payload.query,
            total_found=len(items),
            results=items,
        ),
    )


@router.post("/check-duplicate", response_model=APIResponse[VectorDuplicateCheckResponse])
def check_duplicate_question_endpoint(
    payload: VectorDuplicateCheckRequest,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin, UserRole.superadmin)),
):
    """
    Checks if a question or text is semantically duplicate to an existing question in Qdrant.
    """
    duplicate = check_aptitude_question_duplicate(
        question_text=payload.text,
        similarity_threshold=payload.threshold,
        topic=payload.topic,
    )

    if duplicate:
        return APIResponse(
            success=True,
            message="Semantically similar question detected in vector database.",
            data=VectorDuplicateCheckResponse(
                is_duplicate=True,
                highest_similarity=duplicate["score"],
                duplicate_document=duplicate["payload"],
            ),
        )

    return APIResponse(
        success=True,
        message="No duplicate questions detected above similarity threshold.",
        data=VectorDuplicateCheckResponse(
            is_duplicate=False,
            highest_similarity=0.0,
            duplicate_document=None,
        ),
    )
