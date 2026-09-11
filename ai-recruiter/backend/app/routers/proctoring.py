"""
proctoring.py — API Router for AI-Assisted Proctored Assessment & Integrity Monitoring.
Provides endpoints for candidate consents, real-time monitoring event logs, AST code similarity analysis,
integrity score calculation, recruiter manual review actions, and WebSocket live event streaming.
"""
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Request, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.application import Application
from app.models.coding import CandidateCodingAttempt, CodingAssessment, CodingSubmission
from app.models.candidate import CandidateProfile
from app.models.proctoring import AssessmentConsent, AssessmentEvent, EventSeverity, IntegrityResult
from app.models.user import User, UserRole
from app.schemas.proctoring import (
    AssessmentConsentRequest,
    AssessmentConsentResponse,
    IntegrityResultResponse,
    ProctoringEventCreate,
    ProctoringEventResponse,
    RecruiterDecisionRequest,
)
from app.services.code_similarity_service import analyze_submission_against_history
from app.services.integrity_scoring_service import calculate_attempt_integrity

logger = logging.getLogger("ai_recruiter.routers.proctoring")

router = APIRouter(prefix="/proctoring", tags=["Proctored Assessment"])

# In-memory active WebSocket connections for live proctoring
active_proctoring_connections: Dict[str, List[WebSocket]] = {}


@router.post("/attempts/{attempt_id}/consent", response_model=AssessmentConsentResponse, status_code=status.HTTP_201_CREATED)
def record_candidate_consent(
    attempt_id: uuid.UUID,
    consent_req: AssessmentConsentRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Records explicit candidate consent before starting a proctored assessment."""
    attempt = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment attempt not found.")

    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not candidate or attempt.candidate_id != candidate.id:
        raise HTTPException(status_code=403, detail="Not authorized to submit consent for this attempt.")

    consent = db.query(AssessmentConsent).filter(AssessmentConsent.attempt_id == attempt_id).first()
    if not consent:
        consent = AssessmentConsent(
            attempt_id=attempt_id,
            candidate_id=candidate.id,
        )
        db.add(consent)

    consent.consent_given = True
    consent.camera_consent = consent_req.camera_consent
    consent.microphone_consent = consent_req.microphone_consent
    consent.browser_consent = consent_req.browser_consent
    consent.clipboard_consent = consent_req.clipboard_consent
    consent.ip_address = request.client.host if request.client else "127.0.0.1"
    consent.user_agent = request.headers.get("user-agent", "Unknown")

    db.commit()
    db.refresh(consent)
    return consent


@router.post("/attempts/{attempt_id}/events", response_model=ProctoringEventResponse, status_code=status.HTTP_201_CREATED)
async def record_proctoring_event(
    attempt_id: uuid.UUID,
    event_data: ProctoringEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Records a browser, webcam, audio, or clipboard integrity event during an assessment."""
    attempt = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment attempt not found.")

    try:
        sev = EventSeverity(event_data.severity.lower())
    except ValueError:
        sev = EventSeverity.low

    ev_obj = AssessmentEvent(
        attempt_id=attempt_id,
        candidate_id=attempt.candidate_id,
        question_id=event_data.question_id,
        event_type=event_data.event_type.upper(),
        severity=sev,
        confidence=event_data.confidence,
        metadata_json=json.dumps(event_data.metadata_json) if event_data.metadata_json else None,
    )
    db.add(ev_obj)
    db.commit()
    db.refresh(ev_obj)

    # Recalculate integrity score in real-time
    try:
        calculate_attempt_integrity(db, str(attempt_id))
    except Exception as err:
        logger.warning(f"Failed to update real-time integrity score: {err}")

    # Broadcast event to active WebSockets for recruiter monitoring
    attempt_str = str(attempt_id)
    if attempt_str in active_proctoring_connections:
        broadcast_msg = {
            "event_type": ev_obj.event_type,
            "severity": ev_obj.severity.value,
            "confidence": ev_obj.confidence,
            "occurred_at": ev_obj.occurred_at.isoformat() if ev_obj.occurred_at else None,
        }
        for ws in active_proctoring_connections[attempt_str]:
            try:
                await ws.send_json(broadcast_msg)
            except Exception:
                pass

    return ev_obj


def _resolve_attempt(db: Session, attempt_id: uuid.UUID) -> Optional[CandidateCodingAttempt]:
    """Helper to resolve CandidateCodingAttempt by attempt_id, application_id, or assessment_id."""
    # 1. Direct attempt match
    attempt = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.id == attempt_id).first()
    if attempt:
        return attempt

    # 2. Check if attempt_id is an application_id
    app = db.query(Application).filter(Application.id == attempt_id).first()
    if app:
        attempt = (
            db.query(CandidateCodingAttempt)
            .join(CodingAssessment, CandidateCodingAttempt.assessment_id == CodingAssessment.id)
            .filter(CandidateCodingAttempt.candidate_id == app.candidate_id, CodingAssessment.job_id == app.job_id)
            .order_by(CandidateCodingAttempt.created_at.desc())
            .first()
        )
        if attempt:
            return attempt

    # 3. Check if attempt_id is an assessment_id
    attempt = (
        db.query(CandidateCodingAttempt)
        .filter(CandidateCodingAttempt.assessment_id == attempt_id)
        .order_by(CandidateCodingAttempt.created_at.desc())
        .first()
    )
    return attempt


@router.get("/attempts/{attempt_id}/events", response_model=List[ProctoringEventResponse])
def list_attempt_events(
    attempt_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves all recorded proctoring monitoring events for an attempt."""
    attempt = _resolve_attempt(db, attempt_id)
    target_id = attempt.id if attempt else attempt_id

    events = (
        db.query(AssessmentEvent)
        .filter(AssessmentEvent.attempt_id == target_id)
        .order_by(AssessmentEvent.occurred_at.asc())
        .all()
    )
    return events


@router.get("/attempts/{attempt_id}/integrity", response_model=IntegrityResultResponse)
def get_attempt_integrity_result(
    attempt_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Computes and returns the overall explainable integrity result and evidence summary."""
    attempt = _resolve_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment attempt not found for this applicant.")

    res = calculate_attempt_integrity(db, str(attempt.id))
    return res


@router.post("/attempts/{attempt_id}/code-similarity")
def analyze_code_similarity(
    attempt_id: uuid.UUID,
    submission_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Executes AST code similarity check for a candidate submission against history."""
    submission = db.query(CodingSubmission).filter(CodingSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Coding submission not found.")

    # Retrieve other candidate submissions for the same question
    history_subs = (
        db.query(CodingSubmission)
        .filter(
            CodingSubmission.question_id == submission.question_id,
            CodingSubmission.id != submission_id,
        )
        .all()
    )

    history_dicts = [{"id": str(s.id), "source_code": s.source_code} for s in history_subs]
    sim_res = analyze_submission_against_history(submission.source_code, submission.language, history_dicts)

    # Recalculate integrity score
    calculate_attempt_integrity(db, str(attempt_id))

    return {
        "submission_id": str(submission_id),
        "similarity_analysis": sim_res,
    }


@router.post("/attempts/{attempt_id}/recruiter-decision", response_model=IntegrityResultResponse)
def save_recruiter_decision(
    attempt_id: uuid.UUID,
    decision_req: RecruiterDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Records human recruiter final audit decision (accept, flag, reject)."""
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters can record audit decisions.")

    result = db.query(IntegrityResult).filter(IntegrityResult.attempt_id == attempt_id).first()
    if not result:
        result = calculate_attempt_integrity(db, str(attempt_id))

    result.recruiter_decision = decision_req.decision
    result.recruiter_notes = decision_req.notes
    result.reviewed_by_user_id = current_user.id
    result.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(result)
    return result


@router.websocket("/ws/{attempt_id}")
async def proctoring_websocket_endpoint(websocket: WebSocket, attempt_id: str):
    """WebSocket connection handler for streaming real-time monitoring events to recruiter UI."""
    await websocket.accept()
    if attempt_id not in active_proctoring_connections:
        active_proctoring_connections[attempt_id] = []
    active_proctoring_connections[attempt_id].append(websocket)

    try:
        while True:
            # Keep-alive loop
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        if attempt_id in active_proctoring_connections:
            active_proctoring_connections[attempt_id].remove(websocket)
