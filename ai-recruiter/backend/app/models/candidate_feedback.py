"""
candidate_feedback.py — ORM Models for Automated Candidate Feedback System.
Stores personalized feedback drafts, approved candidate feedback messages,
structured feedback reasons, and evidence references.
"""
import enum
import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID


class FeedbackStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class FeedbackType(str, enum.Enum):
    basic = "basic"
    personalized = "personalized"
    detailed = "detailed"


class CandidateFeedback(Base):
    __tablename__ = "candidate_feedback"
    __table_args__ = (UniqueConstraint("application_id", name="uq_application_candidate_feedback"),)

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    feedback_type: Mapped[FeedbackType] = mapped_column(
        Enum(FeedbackType, name="candidate_feedback_type"), default=FeedbackType.personalized, nullable=False
    )
    feedback_status: Mapped[FeedbackStatus] = mapped_column(
        Enum(FeedbackStatus, name="candidate_feedback_status"), default=FeedbackStatus.PENDING_REVIEW, nullable=False, index=True
    )

    ai_generated: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    recruiter_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string list
    areas_for_improvement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string list
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    draft_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    final_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    generated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reasons: Mapped[List["CandidateFeedbackReason"]] = relationship(
        "CandidateFeedbackReason", back_populates="feedback", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CandidateFeedback app={self.application_id} status={self.feedback_status}>"


class CandidateFeedbackReason(Base):
    __tablename__ = "candidate_feedback_reasons"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    feedback_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_feedback.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reason_code: Mapped[str] = mapped_column(String(100), nullable=False)
    reason_text: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    evidence_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    feedback: Mapped["CandidateFeedback"] = relationship("CandidateFeedback", back_populates="reasons")

    def __repr__(self) -> str:
        return f"<CandidateFeedbackReason code={self.reason_code}>"
