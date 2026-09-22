"""
screening.py — API Router for AI Candidate Pre-Screening & Communication Webhooks.
Includes REST endpoints for starting, managing, retrieving screening score breakdowns,
updating recruiter overrides, candidate consents, and receiving Twilio WhatsApp/SMS webhooks.
"""
import logging
from typing import Any, Dict, List
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.application import Application
from app.models.candidate import CandidateProfile
from app.models.screening import CandidateConsent, ScreeningResult, ScreeningSession, ScreeningStatus
from app.models.user import User, UserRole
from app.schemas.screening import (
    CandidateAnswerSubmission,
    ScreeningConsentRequest,
    ScreeningConsentResponse,
    ScreeningResultResponse,
    ScreeningSessionDetailResponse,
    ScreeningSessionResponse,
)
from app.services.screening_worker import process_candidate_response_task, start_screening_session_task

logger = logging.getLogger("ai_recruiter.routers.screening")

router = APIRouter(prefix="/screening", tags=["AI Pre-Screening"])


@router.post("/applications/{application_id}/start", response_model=ScreeningSessionResponse, status_code=status.HTTP_201_CREATED)
def start_screening(
    application_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Triggers an automated AI pre-screening session for a job application."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    # Access check: candidate who applied or job recruiter/admin
    is_candidate = current_user.role == UserRole.candidate and app.candidate.user_id == current_user.id
    is_recruiter = current_user.role in (UserRole.recruiter, UserRole.admin, UserRole.superadmin)
    if not is_candidate and not is_recruiter:
        raise HTTPException(status_code=403, detail="Not authorized to trigger screening for this application.")

    session = start_screening_session_task(db, str(application_id))
    if not session:
        raise HTTPException(status_code=400, detail="Could not initialize screening session. Candidate may have opted out.")

    return session


@router.get("/applications/{application_id}", response_model=ScreeningSessionDetailResponse)
def get_application_screening(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves screening session details, questions, answers, and scores for an application."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    session = db.query(ScreeningSession).filter(ScreeningSession.application_id == application_id).first()
    if not session:
        # Auto-initialize screening session if not created yet
        session = start_screening_session_task(db, str(application_id))

    if not session:
        raise HTTPException(status_code=404, detail="No screening session found for this application.")

    return session


@router.get("/{screening_id}", response_model=ScreeningSessionDetailResponse)
def get_screening_session(
    screening_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves detailed screening session by session ID."""
    session = db.query(ScreeningSession).filter(ScreeningSession.id == screening_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Screening session not found.")
    return session


@router.post("/{screening_id}/answer")
def submit_answer_manually(
    screening_id: uuid.UUID,
    submission: CandidateAnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Allows submitting an answer via web interface or test client."""
    session = db.query(ScreeningSession).filter(ScreeningSession.id == screening_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Screening session not found.")

    res = process_candidate_response_task(db, str(screening_id), submission.answer)
    return res


@router.post("/{screening_id}/cancel", response_model=ScreeningSessionResponse)
def cancel_screening(
    screening_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cancels an active screening session."""
    session = db.query(ScreeningSession).filter(ScreeningSession.id == screening_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Screening session not found.")

    session.status = ScreeningStatus.cancelled
    db.commit()
    db.refresh(session)
    return session


@router.post("/{screening_id}/resume", response_model=ScreeningSessionResponse)
def resume_screening(
    screening_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Resumes an interrupted or paused screening session."""
    session = db.query(ScreeningSession).filter(ScreeningSession.id == screening_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Screening session not found.")

    if session.status in (ScreeningStatus.completed, ScreeningStatus.cancelled):
        session.status = ScreeningStatus.waiting_for_answer
        db.commit()
        db.refresh(session)

    return session


@router.get("/{screening_id}/result", response_model=ScreeningResultResponse)
def get_screening_result(
    screening_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns overall screening scores, sub-score breakdown, and AI summary."""
    result = db.query(ScreeningResult).filter(ScreeningResult.screening_session_id == screening_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Screening result not available yet.")
    return result


@router.post("/{screening_id}/override", response_model=ScreeningResultResponse)
def recruiter_override_recommendation(
    screening_id: uuid.UUID,
    override_recommendation: str = Form(...),
    reason: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Allows recruiters to manually override the AI screening recommendation."""
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters can override recommendations.")

    result = db.query(ScreeningResult).filter(ScreeningResult.screening_session_id == screening_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Screening result not found.")

    result.recruiter_override = override_recommendation
    result.override_reason = reason

    # Also update application status and send candidate notification/email if selected or shortlisted
    session = db.query(ScreeningSession).filter(ScreeningSession.id == screening_id).first()
    if session and session.application_id:
        app = db.query(Application).filter(Application.id == session.application_id).first()
        if app:
            rec_low = (override_recommendation or "").lower()
            if rec_low in ("selected", "select", "hire"):
                app.status = ApplicationStatus.selected
                app.is_shortlisted = True
                app.recruiter_override = True
                app.override_reason = reason or "Selected via recruiter override"
            elif rec_low in ("shortlisted", "shortlist"):
                app.status = ApplicationStatus.shortlisted
                app.is_shortlisted = True
                app.recruiter_override = True
                app.override_reason = reason or "Shortlisted via recruiter override"
            elif rec_low in ("rejected", "reject"):
                app.status = ApplicationStatus.rejected

            # Trigger email notification if selected or shortlisted
            if rec_low in ("selected", "select", "hire") and app.candidate and app.candidate.user:
                try:
                    from app.services.email_service import send_selected_email
                    comp_name = getattr(app.job, "company_name", None) or f"{current_user.name}'s Company"
                    job_title = app.job.title if app.job else "Position"
                    send_selected_email(
                        to_email=app.candidate.user.email,
                        candidate_name=app.candidate.user.name,
                        job_title=job_title,
                        company_name=comp_name,
                        notes=reason,
                        candidate_id=app.candidate_id,
                        job_id=app.job_id,
                        recruiter_id=current_user.id,
                        db=db,
                    )
                except Exception as err:
                    logger.warning(f"Failed to send selected email on screening override: {err}")
            elif rec_low in ("shortlisted", "shortlist") and app.candidate and app.candidate.user:
                try:
                    from app.services.email_service import send_shortlisted_email
                    comp_name = getattr(app.job, "company_name", None) or f"{current_user.name}'s Company"
                    job_title = app.job.title if app.job else "Position"
                    send_shortlisted_email(
                        to_email=app.candidate.user.email,
                        candidate_name=app.candidate.user.name,
                        job_title=job_title,
                        company_name=comp_name,
                        candidate_id=app.candidate_id,
                        job_id=app.job_id,
                        recruiter_id=current_user.id,
                        db=db,
                    )
                except Exception as err:
                    logger.warning(f"Failed to send shortlisted email on screening override: {err}")

    db.commit()
    db.refresh(result)
    return result


@router.post("/consent", response_model=ScreeningConsentResponse)
def update_candidate_consent(
    consent_data: ScreeningConsentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Updates candidate communication preferences (opt-in / opt-out)."""
    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    consent = db.query(CandidateConsent).filter(CandidateConsent.candidate_id == candidate.id).first()
    if not consent:
        consent = CandidateConsent(candidate_id=candidate.id)
        db.add(consent)

    consent.whatsapp_opt_in = consent_data.whatsapp_opt_in
    consent.sms_opt_in = consent_data.sms_opt_in
    consent.voice_opt_in = consent_data.voice_opt_in
    consent.opted_out_all = consent_data.opted_out_all
    if consent_data.opt_out_reason:
        consent.opt_out_reason = consent_data.opt_out_reason

    db.commit()
    db.refresh(consent)
    return consent


@router.get("/consent/me", response_model=ScreeningConsentResponse)
def get_my_consent(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves active candidate's consent preferences."""
    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    consent = db.query(CandidateConsent).filter(CandidateConsent.candidate_id == candidate.id).first()
    if not consent:
        consent = CandidateConsent(candidate_id=candidate.id)
        db.add(consent)
        db.commit()
        db.refresh(consent)

    return consent


# --- Twilio Webhook Endpoints ---

@router.post("/webhook/whatsapp")
async def twilio_whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Public webhook receiver for incoming WhatsApp candidate messages from Twilio.
    """
    clean_phone = From.replace("whatsapp:", "").strip()
    logger.info(f"Incoming WhatsApp message from {clean_phone}: '{Body}'")

    # Find active screening session for candidate with this phone number
    candidate = db.query(CandidateProfile).filter(CandidateProfile.phone.contains(clean_phone)).first()
    if not candidate:
        logger.warning(f"No candidate profile matched phone {clean_phone}")
        return Response(content="<Response></Response>", media_type="application/xml")

    session = (
        db.query(ScreeningSession)
        .filter(
            ScreeningSession.candidate_id == candidate.id,
            ScreeningSession.status.in_([ScreeningStatus.in_progress, ScreeningStatus.waiting_for_answer, ScreeningStatus.contacted]),
        )
        .order_by(ScreeningSession.created_at.desc())
        .first()
    )

    if session:
        process_candidate_response_task(db, str(session.id), Body)

    # Return empty TwiML response
    return Response(content="<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response></Response>", media_type="application/xml")


@router.post("/webhook/sms")
async def twilio_sms_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db),
):
    """Public webhook receiver for incoming SMS candidate replies from Twilio."""
    clean_phone = From.strip()
    logger.info(f"Incoming SMS from {clean_phone}: '{Body}'")

    candidate = db.query(CandidateProfile).filter(CandidateProfile.phone.contains(clean_phone)).first()
    if candidate:
        session = (
            db.query(ScreeningSession)
            .filter(
                ScreeningSession.candidate_id == candidate.id,
                ScreeningSession.status.in_([ScreeningStatus.in_progress, ScreeningStatus.waiting_for_answer, ScreeningStatus.contacted]),
            )
            .order_by(ScreeningSession.created_at.desc())
            .first()
        )
        if session:
            process_candidate_response_task(db, str(session.id), Body)

    return Response(content="<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response></Response>", media_type="application/xml")
