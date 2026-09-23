"""
proctoring.py — Pydantic schemas for AI-Assisted Proctored Assessment & Integrity Monitoring.
Defines serializers for candidate consent, monitoring event batching, AST code similarity, and recruiter integrity reviews.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field


class AssessmentConsentRequest(BaseModel):
    camera_consent: bool = True
    microphone_consent: bool = True
    browser_consent: bool = True
    clipboard_consent: bool = True
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    assessment_id: Optional[uuid.UUID] = None
    identity_reference_image: Optional[str] = None


class AssessmentConsentResponse(BaseModel):
    id: uuid.UUID
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    candidate_id: uuid.UUID
    consent_given: bool
    camera_consent: bool
    microphone_consent: bool
    browser_consent: bool
    clipboard_consent: bool
    consent_timestamp: datetime
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True


class ProctoringEventCreate(BaseModel):
    event_type: str = Field(..., description="e.g., TAB_SWITCH, TAB_RETURN, NO_FACE_DETECTED, MULTIPLE_FACES_DETECTED, COPY_ATTEMPT, PASTE_ATTEMPT")
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    assessment_id: Optional[uuid.UUID] = None
    question_id: Optional[uuid.UUID] = None
    severity: str = "low"  # info, low, medium, high, critical
    confidence: float = 1.0
    duration_seconds: Optional[float] = None
    metadata_json: Optional[Dict[str, Any]] = None
    occurred_at: Optional[datetime] = None


class ProctoringEventBatchCreate(BaseModel):
    events: List[ProctoringEventCreate]
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    assessment_id: Optional[uuid.UUID] = None


class ProctoringEventResponse(BaseModel):
    id: uuid.UUID
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    assessment_id: Optional[uuid.UUID] = None
    candidate_id: uuid.UUID
    question_id: Optional[uuid.UUID] = None
    event_type: str
    severity: str
    confidence: float
    duration_seconds: Optional[float] = None
    metadata_json: Optional[str] = None
    occurred_at: datetime

    class Config:
        from_attributes = True


class CodeSimilarityResultResponse(BaseModel):
    id: uuid.UUID
    attempt_id: uuid.UUID
    submission_id: uuid.UUID
    matched_submission_id: Optional[uuid.UUID] = None
    comparison_type: str
    similarity_score: float
    confidence: float
    analysis_summary: Optional[str] = None

    class Config:
        from_attributes = True


class IntegrityResultResponse(BaseModel):
    id: uuid.UUID
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    assessment_id: Optional[uuid.UUID] = None
    browser_score: float
    webcam_score: float
    audio_score: float
    code_similarity_score: float
    behavior_score: float
    overall_integrity_score: float
    risk_level: str
    ai_summary: Optional[str] = None
    recruiter_decision: Optional[str] = None
    recruiter_notes: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecruiterDecisionRequest(BaseModel):
    decision: str = Field(..., description="accepted, flagged, rejected")
    notes: Optional[str] = Field(None, description="Explanation for recruiter decision")


class IdentityVerificationRequest(BaseModel):
    attempt_id: Optional[uuid.UUID] = None
    interview_id: Optional[uuid.UUID] = None
    snapshot_image: str = Field(..., description="Base64 encoded frame from webcam")


class IdentityVerificationResponse(BaseModel):
    verified: bool
    confidence: float
    message: str


class TranscriptTurnCreate(BaseModel):
    speaker: str = "Candidate"
    text: str
    timestamp: Optional[str] = None
