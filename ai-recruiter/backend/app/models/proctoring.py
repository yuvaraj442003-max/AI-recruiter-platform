"""
proctoring.py — Database models for AI-Assisted Proctored Assessment & Integrity Monitoring.
Stores candidate consents, real-time monitoring events (tab switches, webcam, audio),
AST code similarity analysis, and explainable integrity results.
"""
import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class EventSeverity(str, enum.Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class RiskLevel(str, enum.Enum):
    low_risk = "Low Risk"
    review_recommended = "Review Recommended"
    high_risk = "High Risk"


class AssessmentConsent(Base, TimestampMixin):
    __tablename__ = "assessment_consents"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_coding_attempts.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )

    consent_given: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    consent_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    camera_consent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    microphone_consent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    browser_consent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    clipboard_consent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    ip_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    attempt: Mapped["CandidateCodingAttempt"] = relationship("CandidateCodingAttempt")


class AssessmentEvent(Base):
    __tablename__ = "assessment_events"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_coding_attempts.id", ondelete="CASCADE"), nullable=False
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("coding_questions.id", ondelete="SET NULL"), nullable=True
    )

    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # TAB_SWITCH, WINDOW_BLUR, FULLSCREEN_EXIT, COPY, PASTE, CUT, NO_FACE, MULTIPLE_FACES, FACE_LOST, ADDITIONAL_VOICE, SUSPICIOUS_AUDIO, CODE_SIMILARITY

    severity: Mapped[EventSeverity] = mapped_column(
        Enum(EventSeverity, name="event_severity_enum"), default=EventSeverity.low, nullable=False
    )
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON details e.g. {"duration_seconds": 8, "face_count": 2}
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    attempt: Mapped["CandidateCodingAttempt"] = relationship("CandidateCodingAttempt")


class CodeSimilarityResult(Base, TimestampMixin):
    __tablename__ = "code_similarity_results"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_coding_attempts.id", ondelete="CASCADE"), nullable=False
    )
    submission_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("coding_submissions.id", ondelete="CASCADE"), nullable=False
    )
    matched_submission_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("coding_submissions.id", ondelete="SET NULL"), nullable=True
    )

    comparison_type: Mapped[str] = mapped_column(String(50), default="AST_TOKEN_HYBRID", nullable=False)
    similarity_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # 0.0 to 100.0
    confidence: Mapped[float] = mapped_column(Float, default=0.90, nullable=False)
    analysis_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    attempt: Mapped["CandidateCodingAttempt"] = relationship("CandidateCodingAttempt")
    submission: Mapped["CodingSubmission"] = relationship("CodingSubmission", foreign_keys=[submission_id])


class IntegrityResult(Base, TimestampMixin):
    __tablename__ = "integrity_results"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_coding_attempts.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    browser_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    webcam_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    audio_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    code_similarity_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    behavior_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)

    overall_integrity_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum"), default=RiskLevel.low_risk, nullable=False
    )

    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Recruiter Manual Review & Audit Log
    recruiter_decision: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # accepted, flagged, rejected
    recruiter_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    attempt: Mapped["CandidateCodingAttempt"] = relationship("CandidateCodingAttempt")

    def __repr__(self) -> str:
        return f"<IntegrityResult score={self.overall_integrity_score} risk={self.risk_level}>"
