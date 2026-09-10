"""
blind_screening.py — API Router for Blind Screening Mode.

Provides REST endpoints for fetching & updating blind screening configurations,
querying server-side anonymized candidate DTOs (strictly omitting name, photo, email, phone, age, gender, location, college),
sanitizing resume text representations, recording decisions (shortlist, hold, reject, next_round),
and executing controlled identity reveals with audit logging.
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
from app.models.audit_log import AuditLog
from app.models.blind_screening import BlindScreeningCandidate, BlindScreeningConfig
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job
from app.models.user import User, UserRole
from app.schemas.blind_screening import (
    BlindCandidateDetailOut,
    BlindCandidateOut,
    BlindDecisionRequest,
    BlindScreeningConfigOut,
    BlindScreeningConfigUpdate,
    BlindStatisticsOut,
    EducationSanitizedItem,
)
from app.services.blind_resume_service import (
    get_or_create_blind_candidate,
    get_or_create_blind_config,
    sanitize_education_text,
    sanitize_resume_text,
)

logger = logging.getLogger("ai_recruiter.routers.blind_screening")

router = APIRouter(prefix="", tags=["Blind Screening Mode"])


@router.get("/jobs/{job_id}/blind-screening/config", response_model=BlindScreeningConfigOut)
def get_blind_screening_config(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves job-level blind screening configuration settings."""
    config = get_or_create_blind_config(db, job_id)
    return config


@router.put("/jobs/{job_id}/blind-screening/config", response_model=BlindScreeningConfigOut)
def update_blind_screening_config(
    job_id: uuid.UUID,
    body: BlindScreeningConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Updates job-level blind screening settings."""
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters can update screening configuration.")

    config = get_or_create_blind_config(db, job_id)

    if body.enabled is not None:
        config.enabled = body.enabled
    if body.hide_name is not None:
        config.hide_name = body.hide_name
    if body.hide_photo is not None:
        config.hide_photo = body.hide_photo
    if body.hide_age is not None:
        config.hide_age = body.hide_age
    if body.hide_gender is not None:
        config.hide_gender = body.hide_gender
    if body.hide_location is not None:
        config.hide_location = body.hide_location
    if body.hide_college is not None:
        config.hide_college = body.hide_college
    if body.hide_email is not None:
        config.hide_email = body.hide_email
    if body.hide_phone is not None:
        config.hide_phone = body.hide_phone
    if body.hide_address is not None:
        config.hide_address = body.hide_address
    if body.hide_social_links is not None:
        config.hide_social_links = body.hide_social_links
    if body.reveal_policy is not None:
        config.reveal_policy = body.reveal_policy

    db.commit()
    db.refresh(config)
    return config


@router.get("/jobs/{job_id}/blind-screening/candidates", response_model=List[BlindCandidateOut])
def get_blind_screening_candidates(
    job_id: uuid.UUID,
    min_ats: float = Query(default=0.0, ge=0.0, le=100.0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieves server-side anonymized candidate DTOs for a job.
    Strictly omits name, email, phone, photo, age, gender, exact location, and college names.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    applications = (
        db.query(Application)
        .options(
            joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
            joinedload(Application.candidate).joinedload(CandidateProfile.user),
        )
        .filter(Application.job_id == job_id)
        .all()
    )

    results = []
    for app in applications:
        cand = app.candidate
        if not cand:
            continue

        ats_sc = app.ats_score or app.match_score or 0.0
        if ats_sc < min_ats:
            continue

        blind_cand = get_or_create_blind_candidate(db, job_id, cand.id)

        # Build server-side anonymized payload
        skills_list = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill] if cand.candidate_skills else []
        matched_sk = json.loads(app.matched_skills) if app.matched_skills else skills_list
        missing_sk = json.loads(app.missing_skills) if app.missing_skills else []

        edu_items = [EducationSanitizedItem(**item) for item in sanitize_education_text(cand.education)]

        # Work experience summary (sanitized role titles only)
        work_exp = [w.strip() for w in (cand.work_experience or "").split("\n") if len(w.strip()) > 3][:3]

        results.append(
            BlindCandidateOut(
                candidate_code=blind_cand.candidate_code,
                job_id=job_id,
                experience_years=cand.experience_years or 0.0,
                skills=skills_list,
                ats_score=round(ats_sc, 1),
                role_match_score=round(app.job_match_score or ats_sc, 1),
                skills_match=round(app.skills_match_score or ats_sc, 1),
                experience_match=round(app.experience_match_score or ats_sc, 1),
                technical_assessment_score=app.coding_score,
                matched_skills=matched_sk,
                missing_skills=missing_sk,
                relevant_experience=work_exp,
                education=edu_items,
                sanitized_resume_summary=cand.ai_summary or cand.summary,
                screening_status=blind_cand.screening_status,
                recruiter_decision=blind_cand.recruiter_decision,
                revealed=blind_cand.revealed,
            )
        )

    # Sort descending by ATS / role match score
    results.sort(key=lambda c: c.ats_score, reverse=True)

    offset = (page - 1) * page_size
    return results[offset : offset + page_size]


@router.get("/jobs/{job_id}/blind-screening/candidates/{candidate_code}", response_model=BlindCandidateDetailOut)
def get_blind_candidate_detail(
    job_id: uuid.UUID,
    candidate_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves full anonymized candidate breakdown and sanitized resume text representation."""
    blind_cand = (
        db.query(BlindScreeningCandidate)
        .options(
            joinedload(BlindScreeningCandidate.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
            joinedload(BlindScreeningCandidate.candidate).joinedload(CandidateProfile.user),
        )
        .filter(BlindScreeningCandidate.job_id == job_id, BlindScreeningCandidate.candidate_code == candidate_code)
        .first()
    )

    if not blind_cand:
        raise HTTPException(status_code=404, detail="Blind candidate record not found.")

    cand = blind_cand.candidate
    app = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == cand.id).first()

    ats_sc = (app.ats_score or app.match_score) if app else 75.0
    skills_list = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill] if cand.candidate_skills else []
    matched_sk = json.loads(app.matched_skills) if (app and app.matched_skills) else skills_list
    missing_sk = json.loads(app.missing_skills) if (app and app.missing_skills) else []
    edu_items = [EducationSanitizedItem(**item) for item in sanitize_education_text(cand.education)]
    work_exp = [w.strip() for w in (cand.work_experience or "").split("\n") if len(w.strip()) > 3][:3]

    # Generate sanitized resume text
    cand_name = cand.user.name if (cand and cand.user) else None
    sanitized_resume = sanitize_resume_text(
        resume_text=cand.raw_resume_text or cand.summary or "Resume text unavailable.",
        candidate_name=cand_name,
        email=cand.user.email if (cand and cand.user) else None,
        phone=cand.phone,
    )

    return BlindCandidateDetailOut(
        candidate_code=blind_cand.candidate_code,
        job_id=job_id,
        experience_years=cand.experience_years or 0.0,
        skills=skills_list,
        ats_score=round(ats_sc, 1),
        role_match_score=round(app.job_match_score or ats_sc, 1) if app else 75.0,
        skills_match=round(app.skills_match_score or ats_sc, 1) if app else 75.0,
        experience_match=round(app.experience_match_score or ats_sc, 1) if app else 75.0,
        technical_assessment_score=app.coding_score if app else None,
        matched_skills=matched_sk,
        missing_skills=missing_sk,
        relevant_experience=work_exp,
        education=edu_items,
        sanitized_resume_summary=cand.ai_summary or cand.summary,
        sanitized_resume_text=sanitized_resume,
        match_explanation=app.recommendation if app else "Strong technical alignment.",
        screening_status=blind_cand.screening_status,
        recruiter_decision=blind_cand.recruiter_decision,
        revealed=blind_cand.revealed,
    )


@router.post("/jobs/{job_id}/blind-screening/candidates/{candidate_code}/decision")
def save_blind_decision(
    job_id: uuid.UUID,
    candidate_code: str,
    body: BlindDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Records recruiter decision (shortlist, hold, reject, next_round) against internal candidate ID.
    Auto-reveals identity if reveal_policy == 'reveal_after_shortlist' and decision == 'shortlist'.
    """
    valid_decisions = ["shortlist", "hold", "reject", "next_round"]
    if body.decision not in valid_decisions:
        raise HTTPException(status_code=400, detail=f"Invalid decision '{body.decision}'. Must be one of: {', '.join(valid_decisions)}")

    blind_cand = (
        db.query(BlindScreeningCandidate)
        .filter(BlindScreeningCandidate.job_id == job_id, BlindScreeningCandidate.candidate_code == candidate_code)
        .first()
    )

    if not blind_cand:
        raise HTTPException(status_code=404, detail="Blind candidate not found.")

    blind_cand.recruiter_decision = body.decision
    blind_cand.screening_status = "completed"

    # Update parent Application status
    app = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == blind_cand.candidate_id).first()
    if app:
        if body.decision == "shortlist":
            app.status = ApplicationStatus.shortlisted
            app.is_shortlisted = True
        elif body.decision == "reject":
            app.status = ApplicationStatus.rejected

    # Check auto-reveal policy
    config = get_or_create_blind_config(db, job_id)
    if config.reveal_policy == "reveal_after_shortlist" and body.decision == "shortlist":
        blind_cand.revealed = True
        blind_cand.revealed_at = db.func.now()
        blind_cand.revealed_by_user_id = current_user.id

        # Audit log identity reveal
        audit = AuditLog(
            user_id=current_user.id,
            action="BLIND_SCREENING_IDENTITY_REVEALED",
            entity_type="candidate_profile",
            entity_id=str(blind_cand.candidate_id),
            details=f"Identity revealed after shortlist decision for candidate code {candidate_code}.",
        )
        db.add(audit)

    db.commit()
    return {
        "success": True,
        "message": f"Recorded decision '{body.decision}' for candidate {candidate_code}.",
        "candidate_code": candidate_code,
        "decision": body.decision,
        "revealed": blind_cand.revealed,
    }


@router.post("/jobs/{job_id}/blind-screening/candidates/{candidate_code}/reveal")
def reveal_candidate_identity(
    job_id: uuid.UUID,
    candidate_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Executes controlled identity reveal of a blind candidate. Writes to audit_logs.
    """
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters or admins can reveal candidate identity.")

    blind_cand = (
        db.query(BlindScreeningCandidate)
        .options(
            joinedload(BlindScreeningCandidate.candidate).joinedload(CandidateProfile.user)
        )
        .filter(BlindScreeningCandidate.job_id == job_id, BlindScreeningCandidate.candidate_code == candidate_code)
        .first()
    )

    if not blind_cand:
        raise HTTPException(status_code=404, detail="Blind candidate record not found.")

    blind_cand.revealed = True
    blind_cand.revealed_at = db.func.now()
    blind_cand.revealed_by_user_id = current_user.id

    # Record Audit Log
    audit = AuditLog(
        user_id=current_user.id,
        action="BLIND_SCREENING_IDENTITY_REVEALED",
        entity_type="candidate_profile",
        entity_id=str(blind_cand.candidate_id),
        details=f"Explicit identity reveal executed by user {current_user.id} for candidate {candidate_code}.",
    )
    db.add(audit)
    db.commit()

    cand = blind_cand.candidate
    cand_user = cand.user if (cand and cand.user) else None

    return {
        "success": True,
        "message": f"Identity revealed for candidate {candidate_code}.",
        "candidate_code": candidate_code,
        "candidate_id": str(blind_cand.candidate_id),
        "name": cand_user.name if cand_user else "Candidate",
        "email": cand_user.email if cand_user else None,
        "phone": cand.phone,
        "location": cand.location,
    }


@router.get("/jobs/{job_id}/blind-screening/statistics", response_model=BlindStatisticsOut)
def get_blind_screening_statistics(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves aggregate screening metrics for a job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    config = get_or_create_blind_config(db, job_id)
    records = db.query(BlindScreeningCandidate).filter(BlindScreeningCandidate.job_id == job_id).all()

    total = len(records)
    shortlisted = sum(1 for r in records if r.recruiter_decision == "shortlist")
    hold = sum(1 for r in records if r.recruiter_decision == "hold")
    rejected = sum(1 for r in records if r.recruiter_decision == "reject")
    revealed = sum(1 for r in records if r.revealed)

    return {
        "job_id": job_id,
        "job_title": job.title,
        "blind_screening_enabled": config.enabled,
        "total_candidates": total,
        "shortlisted_count": shortlisted,
        "hold_count": hold,
        "rejected_count": rejected,
        "revealed_count": revealed,
    }
