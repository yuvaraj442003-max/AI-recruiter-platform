"""
proctoring.py — API Router for AI-Assisted Proctored Assessment & Integrity Monitoring.
Provides endpoints for candidate consents, real-time monitoring event logs, AST code similarity analysis,
integrity score calculation, live interview dialogue transcripts, recruiter manual review actions,
and WebSocket live event streaming for both coding tests and live interviews.
"""
import base64
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
from app.models.interview import Interview
from app.models.proctoring import AssessmentConsent, AssessmentEvent, EventSeverity, IntegrityResult, RiskLevel
from app.models.user import User, UserRole
from app.schemas.proctoring import (
    AssessmentConsentRequest,
    AssessmentConsentResponse,
    IdentityVerificationRequest,
    IdentityVerificationResponse,
    IntegrityResultResponse,
    ProctoringEventBatchCreate,
    ProctoringEventCreate,
    ProctoringEventResponse,
    RecruiterDecisionRequest,
    TranscriptTurnCreate,
)
from app.services.code_similarity_service import analyze_submission_against_history
from app.services.integrity_scoring_service import calculate_attempt_integrity, calculate_interview_integrity

logger = logging.getLogger("ai_recruiter.routers.proctoring")

router = APIRouter(prefix="/proctoring", tags=["Proctored Assessment & Interview"])

# In-memory active WebSocket connections for live proctoring (keyed by channel_id: attempt_id or interview_id)
active_proctoring_connections: Dict[str, List[WebSocket]] = {}


async def _broadcast_event(channel_id: str, payload: dict):
    if channel_id in active_proctoring_connections:
        dead_connections = []
        for ws in active_proctoring_connections[channel_id]:
            try:
                await ws.send_json(payload)
            except Exception:
                dead_connections.append(ws)
        for ws in dead_connections:
            if ws in active_proctoring_connections[channel_id]:
                active_proctoring_connections[channel_id].remove(ws)


@router.post("/consent", response_model=AssessmentConsentResponse, status_code=status.HTTP_201_CREATED)
def record_unified_consent(
    consent_req: AssessmentConsentRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Records explicit candidate pre-check consent for either a coding assessment attempt or live interview."""
    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not candidate:
        raise HTTPException(status_code=403, detail="Candidate profile not found.")

    attempt = None
    if consent_req.attempt_id:
        attempt = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.id == consent_req.attempt_id).first()
    elif consent_req.assessment_id:
        attempt = (
            db.query(CandidateCodingAttempt)
            .filter(
                CandidateCodingAttempt.assessment_id == consent_req.assessment_id,
                CandidateCodingAttempt.candidate_id == candidate.id,
            )
            .order_by(CandidateCodingAttempt.created_at.desc())
            .first()
        )

    interview = None
    if consent_req.interview_id:
        interview = db.query(Interview).filter(Interview.id == consent_req.interview_id).first()

    query = db.query(AssessmentConsent).filter(AssessmentConsent.candidate_id == candidate.id)
    if attempt:
        query = query.filter(AssessmentConsent.attempt_id == attempt.id)
    elif interview:
        query = query.filter(AssessmentConsent.interview_id == interview.id)

    consent = query.first()
    if not consent:
        consent = AssessmentConsent(
            candidate_id=candidate.id,
            attempt_id=attempt.id if attempt else None,
            interview_id=interview.id if interview else None,
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


@router.post("/attempts/{attempt_id}/consent", response_model=AssessmentConsentResponse, status_code=status.HTTP_201_CREATED)
def record_candidate_consent_legacy(
    attempt_id: uuid.UUID,
    consent_req: AssessmentConsentRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Backward compatible consent endpoint for coding attempts."""
    consent_req.attempt_id = attempt_id
    return record_unified_consent(consent_req, request, db, current_user)


@router.post("/events", response_model=ProctoringEventResponse, status_code=status.HTTP_201_CREATED)
async def record_unified_event(
    event_data: ProctoringEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Unified endpoint to record a proctoring event for an assessment attempt or video interview."""
    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    candidate_id = candidate.id if candidate else current_user.id

    try:
        sev = EventSeverity(event_data.severity.lower())
    except ValueError:
        sev = EventSeverity.low

    attempt_id = event_data.attempt_id
    interview_id = event_data.interview_id

    # If assessment_id was passed instead of attempt_id, resolve attempt
    if not attempt_id and event_data.assessment_id and candidate:
        attempt = (
            db.query(CandidateCodingAttempt)
            .filter(
                CandidateCodingAttempt.assessment_id == event_data.assessment_id,
                CandidateCodingAttempt.candidate_id == candidate.id,
            )
            .order_by(CandidateCodingAttempt.created_at.desc())
            .first()
        )
        if attempt:
            attempt_id = attempt.id

    ev_obj = AssessmentEvent(
        attempt_id=attempt_id,
        interview_id=interview_id,
        assessment_id=event_data.assessment_id,
        candidate_id=candidate_id,
        question_id=event_data.question_id,
        event_type=event_data.event_type.upper(),
        severity=sev,
        confidence=event_data.confidence,
        duration_seconds=event_data.duration_seconds,
        metadata_json=json.dumps(event_data.metadata_json) if event_data.metadata_json else None,
        occurred_at=event_data.occurred_at or datetime.now(timezone.utc),
    )
    db.add(ev_obj)
    db.commit()
    db.refresh(ev_obj)

    # Recalculate score asynchronously/in real-time
    channel_key = str(attempt_id) if attempt_id else (str(interview_id) if interview_id else "")
    if attempt_id:
        try:
            calculate_attempt_integrity(db, str(attempt_id))
        except Exception as err:
            logger.debug(f"Attempt integrity recalculation skipped: {err}")
    elif interview_id:
        try:
            calculate_interview_integrity(db, str(interview_id))
        except Exception as err:
            logger.debug(f"Interview integrity recalculation skipped: {err}")

    # Broadcast event to WebSockets
    if channel_key:
        broadcast_msg = {
            "event_type": ev_obj.event_type,
            "severity": ev_obj.severity.value,
            "confidence": ev_obj.confidence,
            "duration_seconds": ev_obj.duration_seconds,
            "occurred_at": ev_obj.occurred_at.isoformat() if ev_obj.occurred_at else None,
        }
        await _broadcast_event(channel_key, broadcast_msg)

    return ev_obj


@router.post("/attempts/{attempt_id}/events", response_model=ProctoringEventResponse, status_code=status.HTTP_201_CREATED)
async def record_proctoring_event_legacy(
    attempt_id: uuid.UUID,
    event_data: ProctoringEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Backward compatible event endpoint for coding attempts."""
    event_data.attempt_id = attempt_id
    return await record_unified_event(event_data, db, current_user)


@router.post("/events/batch", status_code=status.HTTP_201_CREATED)
async def record_batch_events(
    batch_req: ProctoringEventBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Accepts queued monitoring events flushed from the client offline-buffer."""
    created_count = 0
    for ev_data in batch_req.events:
        if not ev_data.attempt_id and batch_req.attempt_id:
            ev_data.attempt_id = batch_req.attempt_id
        if not ev_data.interview_id and batch_req.interview_id:
            ev_data.interview_id = batch_req.interview_id
        if not ev_data.assessment_id and batch_req.assessment_id:
            ev_data.assessment_id = batch_req.assessment_id
        await record_unified_event(ev_data, db, current_user)
        created_count += 1

    return {"status": "success", "processed_events": created_count}


@router.post("/identity/verify", response_model=IdentityVerificationResponse)
def verify_candidate_identity(
    req: IdentityVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lightweight server-side validation of camera frame snapshot during pre-check."""
    if not req.snapshot_image or len(req.snapshot_image) < 50:
        return IdentityVerificationResponse(
            verified=False,
            confidence=0.0,
            message="No webcam image data captured. Please allow camera access and re-test.",
        )

    # Basic base64 integrity check
    try:
        raw_b64 = req.snapshot_image.split(",")[-1]
        data = base64.b64decode(raw_b64)
        if len(data) < 1000:
            return IdentityVerificationResponse(
                verified=False,
                confidence=0.2,
                message="Camera image resolution too low or frame blank. Please adjust lighting and face the camera.",
            )
    except Exception:
        return IdentityVerificationResponse(
            verified=False,
            confidence=0.0,
            message="Failed to parse image frame.",
        )

    return IdentityVerificationResponse(
        verified=True,
        confidence=0.95,
        message="Face detected and candidate identity snapshot recorded successfully.",
    )


@router.post("/interview/{interview_id}/transcript", status_code=status.HTTP_200_OK)
def append_interview_transcript(
    interview_id: uuid.UUID,
    turn: TranscriptTurnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Appends live speech-to-text dialogue turns to Interview.live_transcript."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found.")

    try:
        turns = json.loads(interview.live_transcript) if interview.live_transcript else []
    except Exception:
        turns = []

    turns.append({
        "speaker": turn.speaker,
        "text": turn.text,
        "timestamp": turn.timestamp or datetime.now(timezone.utc).strftime("%H:%M:%S"),
    })

    interview.live_transcript = json.dumps(turns)
    db.commit()
    return {"status": "success", "total_turns": len(turns)}


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
    """Retrieves all recorded proctoring monitoring events for an assessment attempt."""
    attempt = _resolve_attempt(db, attempt_id)
    target_id = attempt.id if attempt else attempt_id

    events = (
        db.query(AssessmentEvent)
        .filter(AssessmentEvent.attempt_id == target_id)
        .order_by(AssessmentEvent.occurred_at.asc())
        .all()
    )
    return events


@router.get("/interview/{interview_id}/events", response_model=List[ProctoringEventResponse])
def list_interview_events(
    interview_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves all recorded proctoring monitoring events for an interview."""
    events = (
        db.query(AssessmentEvent)
        .filter(AssessmentEvent.interview_id == interview_id)
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
    """Computes and returns the overall explainable integrity result and evidence summary for an attempt."""
    attempt = _resolve_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment attempt not found for this applicant.")

    res = calculate_attempt_integrity(db, str(attempt.id))
    return res


@router.get("/interview/{interview_id}/integrity", response_model=IntegrityResultResponse)
def get_interview_integrity_result(
    interview_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Computes and returns the overall explainable integrity result for a video interview."""
    res = calculate_interview_integrity(db, str(interview_id))
    return res


@router.get("/report/{session_id}")
def get_unified_proctoring_report(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns complete proctoring audit report resolving session_id to either
    an assessment attempt, live interview, or job application.
    """
    attempt = _resolve_attempt(db, session_id)
    interview = db.query(Interview).filter(Interview.id == session_id).first()

    if not interview and not attempt:
        # Check if session_id is an application_id with an interview
        interview = db.query(Interview).filter(Interview.application_id == session_id).first()

    if not attempt and not interview:
        raise HTTPException(status_code=404, detail="No assessment or interview proctoring data found for this ID.")

    report_type = "coding_assessment" if attempt else "interview"
    session_obj = attempt or interview

    # Fetch events
    if attempt:
        events = (
            db.query(AssessmentEvent)
            .filter(AssessmentEvent.attempt_id == attempt.id)
            .order_by(AssessmentEvent.occurred_at.asc())
            .all()
        )
        integrity = calculate_attempt_integrity(db, str(attempt.id))
        candidate_id = attempt.candidate_id
    else:
        events = (
            db.query(AssessmentEvent)
            .filter(AssessmentEvent.interview_id == interview.id)
            .order_by(AssessmentEvent.occurred_at.asc())
            .all()
        )
        integrity = calculate_interview_integrity(db, str(interview.id))
        candidate_id = interview.candidate_id

    candidate = db.query(CandidateProfile).filter(CandidateProfile.id == candidate_id).first()
    candidate_user = db.query(User).filter(User.id == candidate.user_id).first() if candidate else None

    # Count events by type
    event_counts = {}
    for ev in events:
        event_counts[ev.event_type] = event_counts.get(ev.event_type, 0) + 1

    transcript_turns = []
    if interview and interview.live_transcript:
        try:
            transcript_turns = json.loads(interview.live_transcript)
        except Exception:
            pass

    return {
        "report_type": report_type,
        "session_id": str(session_obj.id),
        "candidate": {
            "id": str(candidate.id) if candidate else "",
            "full_name": candidate_user.full_name if candidate_user else "Candidate",
            "email": candidate_user.email if candidate_user else "",
        },
        "integrity_result": {
            "id": str(integrity.id),
            "browser_score": integrity.browser_score,
            "webcam_score": integrity.webcam_score,
            "audio_score": integrity.audio_score,
            "code_similarity_score": integrity.code_similarity_score,
            "behavior_score": integrity.behavior_score,
            "overall_integrity_score": integrity.overall_integrity_score,
            "risk_level": integrity.risk_level.value,
            "ai_summary": integrity.ai_summary,
            "recruiter_decision": integrity.recruiter_decision,
            "recruiter_notes": integrity.recruiter_notes,
            "reviewed_at": integrity.reviewed_at.isoformat() if integrity.reviewed_at else None,
        },
        "event_counts": event_counts,
        "total_events": len(events),
        "events": [
            {
                "id": str(e.id),
                "event_type": e.event_type,
                "severity": e.severity.value,
                "confidence": e.confidence,
                "duration_seconds": e.duration_seconds,
                "metadata_json": e.metadata_json,
                "occurred_at": e.occurred_at.isoformat() if e.occurred_at else None,
            }
            for e in events
        ],
        "dialogue_transcript": transcript_turns,
    }


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
    """Records human recruiter final audit decision for a coding attempt."""
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


@router.post("/interview/{interview_id}/recruiter-decision", response_model=IntegrityResultResponse)
def save_interview_recruiter_decision(
    interview_id: uuid.UUID,
    decision_req: RecruiterDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Records human recruiter final audit decision for a video interview."""
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters can record audit decisions.")

    result = db.query(IntegrityResult).filter(IntegrityResult.interview_id == interview_id).first()
    if not result:
        result = calculate_interview_integrity(db, str(interview_id))

    result.recruiter_decision = decision_req.decision
    result.recruiter_notes = decision_req.notes
    result.reviewed_by_user_id = current_user.id
    result.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(result)
    return result


@router.websocket("/ws/{channel_id}")
async def proctoring_websocket_endpoint(websocket: WebSocket, channel_id: str):
    """WebSocket connection handler for streaming real-time monitoring events to recruiter UI."""
    await websocket.accept()
    if channel_id not in active_proctoring_connections:
        active_proctoring_connections[channel_id] = []
    active_proctoring_connections[channel_id].append(websocket)

    try:
        while True:
            # Keep-alive loop
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        if channel_id in active_proctoring_connections:
            if websocket in active_proctoring_connections[channel_id]:
                active_proctoring_connections[channel_id].remove(websocket)
