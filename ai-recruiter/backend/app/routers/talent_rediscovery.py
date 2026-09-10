"""
talent_rediscovery.py — API Router for Talent Pool Auto-Rediscovery & Silver Medalist Matching System.

Provides REST endpoints for manually triggering rediscovery, querying ranked candidate matches,
checking real-time Redis status, executing natural-language talent searches, and taking recruiter actions.
"""
import json
import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.application import Application, ApplicationStatus
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.models.talent_rediscovery import TalentRediscoveryResult, TalentRediscoveryRun, RediscoveryRunStatus
from app.models.user import User, UserRole
from app.schemas.talent_rediscovery import (
    SmartSearchRequest,
    TalentRediscoveryResultOut,
    TalentRediscoveryRunOut,
    TalentRediscoverySummaryOut,
)
from app.services.redis_service import cache_get_json
from app.services.talent_rediscovery_service import (
    run_rediscovery_for_job,
    trigger_rediscovery_async,
)

logger = logging.getLogger("ai_recruiter.routers.talent_rediscovery")

router = APIRouter(prefix="", tags=["Talent Pool Auto-Rediscovery"])


@router.post("/jobs/{job_id}/rediscover", status_code=status.HTTP_202_ACCEPTED)
def trigger_job_rediscovery(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Triggers asynchronous Talent Pool Auto-Rediscovery for a job. Returns 202 Accepted.
    Recruiter can poll progress via GET /jobs/{job_id}/rediscovery/status.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin) and job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to trigger rediscovery for this job.")

    trigger_rediscovery_async(job_id)
    return {
        "success": True,
        "message": f"Talent Rediscovery started asynchronously for job '{job.title}'.",
        "job_id": job_id,
        "status": "QUEUED",
    }


@router.get("/jobs/{job_id}/rediscovery/status")
def get_rediscovery_status(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves real-time processing progress from Redis or database."""
    progress = cache_get_json(f"rediscovery:job:{job_id}:progress")
    if progress:
        return progress

    run = db.query(TalentRediscoveryRun).filter(TalentRediscoveryRun.job_id == job_id).order_by(TalentRediscoveryRun.created_at.desc()).first()
    if not run:
        return {"status": "NOT_STARTED", "processed": 0, "total": 0, "matched": 0}

    return {
        "status": run.status.value if hasattr(run.status, "value") else str(run.status),
        "processed": run.processed_candidates,
        "total": run.total_candidates,
        "matched": run.matched_candidates,
    }


@router.get("/jobs/{job_id}/rediscovery", response_model=TalentRediscoverySummaryOut)
def get_rediscovery_summary(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves summary metrics for talent rediscovery on a job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    results = db.query(TalentRediscoveryResult).filter(TalentRediscoveryResult.job_id == job_id).all()
    run = db.query(TalentRediscoveryRun).filter(TalentRediscoveryRun.job_id == job_id).order_by(TalentRediscoveryRun.created_at.desc()).first()

    run_status = run.status.value if (run and hasattr(run.status, "value")) else ("COMPLETED" if results else "NOT_STARTED")
    total_analyzed = run.total_candidates if run else db.query(CandidateProfile).count()

    scores = [r.overall_score for r in results]
    top_score = max(scores) if scores else 0.0
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    silver_count = sum(1 for r in results if r.is_silver_medalist)

    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates_analyzed": total_analyzed,
        "matched_candidates_count": len(results),
        "silver_medalists_count": silver_count,
        "top_match_score": top_score,
        "average_match_score": avg_score,
        "status": run_status,
    }


@router.get("/jobs/{job_id}/rediscovery/candidates", response_model=List[TalentRediscoveryResultOut])
def get_rediscovered_candidates(
    job_id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    min_score: float = Query(default=0.0, ge=0.0, le=100.0),
    silver_medalist: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves ranked rediscovered candidates with filtering and pagination."""
    query = (
        db.query(TalentRediscoveryResult)
        .options(
            joinedload(TalentRediscoveryResult.candidate).joinedload(CandidateProfile.user),
            joinedload(TalentRediscoveryResult.previous_job),
        )
        .filter(TalentRediscoveryResult.job_id == job_id)
    )

    if min_score > 0.0:
        query = query.filter(TalentRediscoveryResult.overall_score >= min_score)
    if silver_medalist is not None:
        query = query.filter(TalentRediscoveryResult.is_silver_medalist == silver_medalist)

    query = query.order_by(TalentRediscoveryResult.rank.asc())

    offset = (page - 1) * page_size
    results = query.offset(offset).limit(page_size).all()

    return [_format_result_item(r) for r in results]


@router.get("/jobs/{job_id}/rediscovery/{candidate_id}", response_model=TalentRediscoveryResultOut)
def get_rediscovered_candidate_detail(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves detailed match breakdown & AI explanation for a single rediscovered candidate."""
    result = (
        db.query(TalentRediscoveryResult)
        .options(
            joinedload(TalentRediscoveryResult.candidate).joinedload(CandidateProfile.user),
            joinedload(TalentRediscoveryResult.previous_job),
        )
        .filter(TalentRediscoveryResult.job_id == job_id, TalentRediscoveryResult.candidate_id == candidate_id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Rediscovered candidate result not found.")

    return _format_result_item(result)


@router.post("/jobs/{job_id}/rediscovery/{candidate_id}/shortlist")
def shortlist_rediscovered_candidate(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Shortlists a rediscovered candidate, adding them as an active Application for the job."""
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters can shortlist candidates.")

    # Check if application already exists
    app = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == candidate_id).first()
    if not app:
        app = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            status=ApplicationStatus.shortlisted,
            is_shortlisted=True,
            source="talent_rediscovery",
        )
        db.add(app)
    else:
        app.status = ApplicationStatus.shortlisted
        app.is_shortlisted = True

    # Update result status
    res = db.query(TalentRediscoveryResult).filter(TalentRediscoveryResult.job_id == job_id, TalentRediscoveryResult.candidate_id == candidate_id).first()
    if res:
        res.status = "shortlisted"

    db.commit()
    return {"success": True, "message": "Candidate shortlisted successfully.", "application_id": app.id}


@router.post("/jobs/{job_id}/rediscovery/{candidate_id}/contact")
def contact_rediscovered_candidate(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Initiates recruiter contact workflow for a rediscovered candidate."""
    candidate = db.query(CandidateProfile).options(joinedload(CandidateProfile.user)).filter(CandidateProfile.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    job = db.query(Job).filter(Job.id == job_id).first()
    res = db.query(TalentRediscoveryResult).filter(TalentRediscoveryResult.job_id == job_id, TalentRediscoveryResult.candidate_id == candidate_id).first()
    if res:
        res.status = "contacted"
        db.commit()

    return {
        "success": True,
        "message": f"Candidate contact workflow initiated for {candidate.user.name if candidate.user else 'Candidate'}.",
        "candidate_email": candidate.user.email if candidate.user else None,
        "candidate_user_id": str(candidate.user_id),
    }


@router.post("/talent-rediscovery/smart-search")
def smart_search_talent_pool(
    body: SmartSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Parses natural-language queries into structured filters across existing candidates."""
    query_str = body.query.lower().strip()

    query = (
        db.query(CandidateProfile)
        .join(User, CandidateProfile.user_id == User.id)
        .options(joinedload(CandidateProfile.user))
        .filter(User.is_active == True)
    )

    # Basic text filter across headline, summary, work_experience
    tokens = [t for t in query_str.split() if len(t) > 2]
    if tokens:
        for t in tokens:
            p = f"%{t}%"
            query = query.filter(
                (CandidateProfile.headline.ilike(p))
                | (CandidateProfile.summary.ilike(p))
                | (CandidateProfile.work_experience.ilike(p))
                | (User.name.ilike(p))
            )

    candidates = query.limit(30).all()

    results = []
    for c in candidates:
        results.append({
            "candidate_id": c.id,
            "candidate_name": c.user.name if c.user else "Candidate",
            "headline": c.headline or "Software Professional",
            "location": c.location,
            "experience_years": c.experience_years or 0.0,
            "skills": [cs.skill.skill_name for cs in c.candidate_skills if cs.skill] if c.candidate_skills else [],
        })

    return {"query": body.query, "total_found": len(results), "candidates": results}


@router.get("/talent-rediscovery/analytics")
def get_talent_pool_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves overall talent pool rediscovery analytics."""
    total_candidates = db.query(CandidateProfile).count()
    all_results = db.query(TalentRediscoveryResult).all()

    silver_count = sum(1 for r in all_results if r.is_silver_medalist)
    high_match_count = sum(1 for r in all_results if r.overall_score >= 80.0)

    avg_score = round(sum(r.overall_score for r in all_results) / len(all_results), 1) if all_results else 0.0

    return {
        "total_candidates_in_pool": total_candidates,
        "rediscovered_matches": len(all_results),
        "high_quality_matches": high_match_count,
        "silver_medalists": silver_count,
        "average_match_score": avg_score,
    }


def _format_result_item(r: TalentRediscoveryResult) -> dict:
    cand_name = r.candidate.user.name if (r.candidate and r.candidate.user) else "Candidate"
    cand_email = r.candidate.user.email if (r.candidate and r.candidate.user) else None
    cand_headline = r.candidate.headline if r.candidate else None
    cand_loc = r.candidate.location if r.candidate else None
    exp_years = r.candidate.experience_years if r.candidate else 0.0

    prev_job_title = r.previous_job.title if r.previous_job else r.previous_job_title

    return {
        "id": r.id,
        "job_id": r.job_id,
        "candidate_id": r.candidate_id,
        "candidate_name": cand_name,
        "candidate_email": cand_email,
        "candidate_headline": cand_headline,
        "candidate_location": cand_loc,
        "experience_years": exp_years,
        "overall_score": r.overall_score,
        "skills_score": r.skills_score,
        "experience_score": r.experience_score,
        "semantic_score": r.semantic_score,
        "responsibility_score": r.responsibility_score,
        "keyword_score": r.keyword_score,
        "location_score": r.location_score,
        "education_score": r.education_score,
        "rank": r.rank,
        "is_silver_medalist": r.is_silver_medalist,
        "previous_job_id": r.previous_job_id,
        "previous_job_title": prev_job_title,
        "previous_application_status": r.previous_application_status,
        "previous_ats_score": r.previous_ats_score,
        "matched_skills": json.loads(r.matched_skills) if r.matched_skills else [],
        "missing_skills": json.loads(r.missing_skills) if r.missing_skills else [],
        "matched_keywords": json.loads(r.matched_keywords) if r.matched_keywords else [],
        "missing_keywords": json.loads(r.missing_keywords) if r.missing_keywords else [],
        "match_explanation": r.match_explanation,
        "status": r.status,
        "created_at": r.created_at,
    }
