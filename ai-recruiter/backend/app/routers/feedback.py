"""
feedback.py — REST Router for Automated Candidate Feedback System.
Provides endpoints for feedback generation, retrieval, editing, approval,
sending, regeneration, status polling, and batch feedback processing.
"""
import json
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.application import Application
from app.models.candidate_feedback import CandidateFeedback, FeedbackStatus
from app.models.job import Job
from app.models.user import User, UserRole
from app.schemas.feedback import (
    BulkFeedbackRequest,
    BulkFeedbackStatusOut,
    CandidateFeedbackOut,
    CandidateFeedbackReasonOut,
    CandidateFeedbackRecruiterOut,
    CandidateFeedbackUpdate,
)
from app.services import candidate_feedback_service

router = APIRouter(prefix="/api/v1", tags=["Candidate Feedback"])


@router.post("/applications/{application_id}/feedback/generate", response_model=CandidateFeedbackRecruiterOut)
def generate_feedback_endpoint(
    application_id: uuid.UUID,
    feedback_level: str = Query("personalized", description="basic, personalized, or detailed"),
    custom_direction: Optional[str] = Query(None, description="Optional recruiter direction"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generates an AI-assisted feedback draft for a rejected candidate application."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    if current_user.role != UserRole.recruiter and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only recruiters can trigger feedback generation.")

    feedback = candidate_feedback_service.generate_feedback_for_application(
        db, application_id, custom_direction=custom_direction, feedback_level=feedback_level
    )

    reasons_out = [
        CandidateFeedbackReasonOut(
            reason_code=r.reason_code,
            reason_text=r.reason_text,
            evidence_type=r.evidence_type,
            evidence_reference=r.evidence_reference,
        )
        for r in (feedback.reasons or [])
    ]

    return CandidateFeedbackRecruiterOut(
        id=feedback.id,
        application_id=feedback.application_id,
        candidate_id=feedback.candidate_id,
        candidate_name=app.candidate.full_name if app.candidate else "Candidate",
        candidate_code=f"CAND-{str(app.candidate_id)[:5].upper()}",
        job_id=feedback.job_id,
        job_title=app.job.title if app.job else "Position",
        feedback_type=feedback.feedback_type.value,
        feedback_status=feedback.feedback_status.value,
        ai_generated=feedback.ai_generated,
        recruiter_approved=feedback.recruiter_approved,
        summary=feedback.summary,
        strengths=json.loads(feedback.strengths) if feedback.strengths else [],
        areas_for_improvement=json.loads(feedback.areas_for_improvement) if feedback.areas_for_improvement else [],
        reason=feedback.reason,
        recommendation=feedback.recommendation,
        draft_content=feedback.draft_content,
        final_content=feedback.final_content,
        reasons=reasons_out,
        generated_at=feedback.generated_at,
        approved_at=feedback.approved_at,
        sent_at=feedback.sent_at,
    )


@router.get("/applications/{application_id}/feedback")
def get_feedback_endpoint(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieves candidate feedback. Candidates see only approved/sent candidate-facing views.
    Recruiters see full review details including draft content and reasons.
    """
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    feedback = db.query(CandidateFeedback).filter(CandidateFeedback.application_id == application_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found for this application.")

    # Candidate view check
    if current_user.role == UserRole.candidate:
        if app.candidate.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized access to candidate feedback.")
        if feedback.feedback_status != FeedbackStatus.SENT and not feedback.recruiter_approved:
            raise HTTPException(status_code=404, detail="Feedback is pending recruiter review.")

        return CandidateFeedbackOut(
            id=feedback.id,
            application_id=feedback.application_id,
            job_id=feedback.job_id,
            job_title=app.job.title if app.job else "Position",
            company_name=app.job.company.name if (app.job and app.job.company) else "Company",
            feedback_type=feedback.feedback_type.value,
            summary=feedback.summary,
            strengths=json.loads(feedback.strengths) if feedback.strengths else [],
            areas_for_improvement=json.loads(feedback.areas_for_improvement) if feedback.areas_for_improvement else [],
            recommendation=feedback.recommendation,
            content=feedback.final_content or feedback.draft_content,
            sent_at=feedback.sent_at,
        )

    # Recruiter / Admin view
    reasons_out = [
        CandidateFeedbackReasonOut(
            reason_code=r.reason_code,
            reason_text=r.reason_text,
            evidence_type=r.evidence_type,
            evidence_reference=r.evidence_reference,
        )
        for r in (feedback.reasons or [])
    ]

    return CandidateFeedbackRecruiterOut(
        id=feedback.id,
        application_id=feedback.application_id,
        candidate_id=feedback.candidate_id,
        candidate_name=app.candidate.full_name if app.candidate else "Candidate",
        candidate_code=f"CAND-{str(app.candidate_id)[:5].upper()}",
        job_id=feedback.job_id,
        job_title=app.job.title if app.job else "Position",
        feedback_type=feedback.feedback_type.value,
        feedback_status=feedback.feedback_status.value,
        ai_generated=feedback.ai_generated,
        recruiter_approved=feedback.recruiter_approved,
        summary=feedback.summary,
        strengths=json.loads(feedback.strengths) if feedback.strengths else [],
        areas_for_improvement=json.loads(feedback.areas_for_improvement) if feedback.areas_for_improvement else [],
        reason=feedback.reason,
        recommendation=feedback.recommendation,
        draft_content=feedback.draft_content,
        final_content=feedback.final_content,
        reasons=reasons_out,
        generated_at=feedback.generated_at,
        approved_at=feedback.approved_at,
        sent_at=feedback.sent_at,
    )


@router.put("/applications/{application_id}/feedback", response_model=CandidateFeedbackRecruiterOut)
def update_feedback_endpoint(
    application_id: uuid.UUID,
    payload: CandidateFeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Allows recruiters to edit AI-generated draft feedback before sending."""
    if current_user.role != UserRole.recruiter and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only recruiters can edit feedback.")

    feedback = db.query(CandidateFeedback).filter(CandidateFeedback.application_id == application_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback record not found.")

    if payload.final_content is not None:
        feedback.final_content = payload.final_content.strip()

    if payload.feedback_status is not None:
        if payload.feedback_status in FeedbackStatus.__members__:
            feedback.feedback_status = FeedbackStatus(payload.feedback_status)

    db.commit()
    db.refresh(feedback)

    app = db.query(Application).filter(Application.id == application_id).first()
    reasons_out = [
        CandidateFeedbackReasonOut(
            reason_code=r.reason_code,
            reason_text=r.reason_text,
            evidence_type=r.evidence_type,
            evidence_reference=r.evidence_reference,
        )
        for r in (feedback.reasons or [])
    ]

    return CandidateFeedbackRecruiterOut(
        id=feedback.id,
        application_id=feedback.application_id,
        candidate_id=feedback.candidate_id,
        candidate_name=app.candidate.full_name if (app and app.candidate) else "Candidate",
        candidate_code=f"CAND-{str(feedback.candidate_id)[:5].upper()}",
        job_id=feedback.job_id,
        job_title=app.job.title if (app and app.job) else "Position",
        feedback_type=feedback.feedback_type.value,
        feedback_status=feedback.feedback_status.value,
        ai_generated=feedback.ai_generated,
        recruiter_approved=feedback.recruiter_approved,
        summary=feedback.summary,
        strengths=json.loads(feedback.strengths) if feedback.strengths else [],
        areas_for_improvement=json.loads(feedback.areas_for_improvement) if feedback.areas_for_improvement else [],
        reason=feedback.reason,
        recommendation=feedback.recommendation,
        draft_content=feedback.draft_content,
        final_content=feedback.final_content,
        reasons=reasons_out,
        generated_at=feedback.generated_at,
        approved_at=feedback.approved_at,
        sent_at=feedback.sent_at,
    )


@router.post("/applications/{application_id}/feedback/approve", response_model=CandidateFeedbackRecruiterOut)
@router.post("/applications/{application_id}/feedback/send", response_model=CandidateFeedbackRecruiterOut)
def approve_and_send_endpoint(
    application_id: uuid.UUID,
    final_content_override: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approves candidate feedback draft, delivers notifications, and records audit logs."""
    if current_user.role != UserRole.recruiter and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only recruiters can approve and send feedback.")

    feedback = db.query(CandidateFeedback).filter(CandidateFeedback.application_id == application_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback record not found.")

    updated_feedback = candidate_feedback_service.approve_and_send_feedback(
        db=db,
        feedback_id=feedback.id,
        recruiter_user_id=current_user.id,
        final_content_override=final_content_override,
    )

    app = db.query(Application).filter(Application.id == application_id).first()
    reasons_out = [
        CandidateFeedbackReasonOut(
            reason_code=r.reason_code,
            reason_text=r.reason_text,
            evidence_type=r.evidence_type,
            evidence_reference=r.evidence_reference,
        )
        for r in (updated_feedback.reasons or [])
    ]

    return CandidateFeedbackRecruiterOut(
        id=updated_feedback.id,
        application_id=updated_feedback.application_id,
        candidate_id=updated_feedback.candidate_id,
        candidate_name=app.candidate.full_name if (app and app.candidate) else "Candidate",
        candidate_code=f"CAND-{str(updated_feedback.candidate_id)[:5].upper()}",
        job_id=updated_feedback.job_id,
        job_title=app.job.title if (app and app.job) else "Position",
        feedback_type=updated_feedback.feedback_type.value,
        feedback_status=updated_feedback.feedback_status.value,
        ai_generated=updated_feedback.ai_generated,
        recruiter_approved=updated_feedback.recruiter_approved,
        summary=updated_feedback.summary,
        strengths=json.loads(updated_feedback.strengths) if updated_feedback.strengths else [],
        areas_for_improvement=json.loads(updated_feedback.areas_for_improvement) if updated_feedback.areas_for_improvement else [],
        reason=updated_feedback.reason,
        recommendation=updated_feedback.recommendation,
        draft_content=updated_feedback.draft_content,
        final_content=updated_feedback.final_content,
        reasons=reasons_out,
        generated_at=updated_feedback.generated_at,
        approved_at=updated_feedback.approved_at,
        sent_at=updated_feedback.sent_at,
    )


@router.post("/applications/{application_id}/feedback/regenerate", response_model=CandidateFeedbackRecruiterOut)
def regenerate_feedback_endpoint(
    application_id: uuid.UUID,
    custom_direction: str = Query("more encouraging", description="e.g., more concise, more detailed, more encouraging, focus on skill gaps"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Regenerates AI candidate feedback with custom recruiter instructions."""
    if current_user.role != UserRole.recruiter and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only recruiters can regenerate feedback.")

    feedback = candidate_feedback_service.generate_feedback_for_application(
        db=db, application_id=application_id, custom_direction=custom_direction
    )

    app = db.query(Application).filter(Application.id == application_id).first()
    reasons_out = [
        CandidateFeedbackReasonOut(
            reason_code=r.reason_code,
            reason_text=r.reason_text,
            evidence_type=r.evidence_type,
            evidence_reference=r.evidence_reference,
        )
        for r in (feedback.reasons or [])
    ]

    return CandidateFeedbackRecruiterOut(
        id=feedback.id,
        application_id=feedback.application_id,
        candidate_id=feedback.candidate_id,
        candidate_name=app.candidate.full_name if (app and app.candidate) else "Candidate",
        candidate_code=f"CAND-{str(feedback.candidate_id)[:5].upper()}",
        job_id=feedback.job_id,
        job_title=app.job.title if (app and app.job) else "Position",
        feedback_type=feedback.feedback_type.value,
        feedback_status=feedback.feedback_status.value,
        ai_generated=feedback.ai_generated,
        recruiter_approved=feedback.recruiter_approved,
        summary=feedback.summary,
        strengths=json.loads(feedback.strengths) if feedback.strengths else [],
        areas_for_improvement=json.loads(feedback.areas_for_improvement) if feedback.areas_for_improvement else [],
        reason=feedback.reason,
        recommendation=feedback.recommendation,
        draft_content=feedback.draft_content,
        final_content=feedback.final_content,
        reasons=reasons_out,
        generated_at=feedback.generated_at,
        approved_at=feedback.approved_at,
        sent_at=feedback.sent_at,
    )


@router.post("/recruiter/feedback/bulk-generate", response_model=BulkFeedbackStatusOut)
def bulk_generate_feedback_endpoint(
    payload: BulkFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Processes asynchronous batch feedback generation for multiple rejected applications."""
    if current_user.role != UserRole.recruiter and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only recruiters can run bulk feedback generation.")

    results = []
    completed = 0
    failed = 0

    for app_id in payload.application_ids:
        try:
            fb = candidate_feedback_service.generate_feedback_for_application(
                db=db, application_id=app_id, custom_direction=payload.regeneration_prompt
            )
            if payload.auto_approve:
                candidate_feedback_service.approve_and_send_feedback(db=db, feedback_id=fb.id, recruiter_user_id=current_user.id)
            completed += 1
            results.append({"application_id": str(app_id), "status": "success", "feedback_id": str(fb.id)})
        except Exception as e:
            failed += 1
            results.append({"application_id": str(app_id), "status": "failed", "error": str(e)})

    return BulkFeedbackStatusOut(
        total_requested=len(payload.application_ids),
        completed=completed,
        pending=0,
        failed=failed,
        status="completed",
        results=results,
    )
