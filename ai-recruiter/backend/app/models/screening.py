"""
screening.py — Database models for AI Candidate Pre-Screening.
Tracks screening sessions, job-tailored questions, extracted candidate answers,
deterministic scoring results, communication logs, and candidate opt-in consents.
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


class ScreeningStatus(str, enum.Enum):
    pending = "pending"
    contacted = "contacted"
    in_progress = "in_progress"
    waiting_for_answer = "waiting_for_answer"
    processing_answer = "processing_answer"
    next_question = "next_question"
    completed = "completed"
    failed = "failed"
    expired = "expired"
    cancelled = "cancelled"
    opted_out = "opted_out"


class ScreeningChannel(str, enum.Enum):
    whatsapp = "whatsapp"
    sms = "sms"
    voice = "voice"


class ScreeningSession(Base, TimestampMixin):
    __tablename__ = "screening_sessions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[ScreeningStatus] = mapped_column(
        Enum(ScreeningStatus, name="screening_status_enum"), default=ScreeningStatus.pending, nullable=False
    )
    channel: Mapped[ScreeningChannel] = mapped_column(
        Enum(ScreeningChannel, name="screening_channel_enum"), default=ScreeningChannel.whatsapp, nullable=False
    )

    current_question_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    screening_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    questions: Mapped[list["ScreeningQuestion"]] = relationship(
        "ScreeningQuestion", back_populates="session", cascade="all, delete-orphan", order_by="ScreeningQuestion.sequence"
    )
    answers: Mapped[list["ScreeningAnswer"]] = relationship(
        "ScreeningAnswer", back_populates="session", cascade="all, delete-orphan"
    )
    result: Mapped[Optional["ScreeningResult"]] = relationship(
        "ScreeningResult", back_populates="session", uselist=False, cascade="all, delete-orphan"
    )
    logs: Mapped[list["CommunicationLog"]] = relationship(
        "CommunicationLog", back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ScreeningSession id={self.id} status={self.status} score={self.screening_score}>"


class ScreeningQuestion(Base):
    __tablename__ = "screening_questions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    screening_session_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("screening_sessions.id", ondelete="CASCADE"), nullable=False
    )

    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), nullable=False)  # technical, experience, location, notice_period, salary, work_mode
    expected_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ScreeningSession"] = relationship("ScreeningSession", back_populates="questions")
    answer: Mapped[Optional["ScreeningAnswer"]] = relationship(
        "ScreeningAnswer", back_populates="question_ref", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ScreeningQuestion seq={self.sequence} type={self.question_type}>"


class ScreeningAnswer(Base):
    __tablename__ = "screening_answers"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    screening_question_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("screening_questions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    screening_session_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("screening_sessions.id", ondelete="CASCADE"), nullable=False
    )

    candidate_answer: Mapped[str] = mapped_column(Text, nullable=False)  # raw text response
    extracted_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    ai_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ai_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ScreeningSession"] = relationship("ScreeningSession", back_populates="answers")
    question_ref: Mapped["ScreeningQuestion"] = relationship("ScreeningQuestion", back_populates="answer")

    def __repr__(self) -> str:
        return f"<ScreeningAnswer score={self.ai_score}>"


class ScreeningResult(Base, TimestampMixin):
    __tablename__ = "screening_results"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    screening_session_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("screening_sessions.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    technical_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    experience_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    location_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    salary_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    availability_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    communication_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    recommendation: Mapped[str] = mapped_column(String(100), nullable=False)  # Strong Match, Shortlist, Review, Not Recommended
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recruiter_override: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    override_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    session: Mapped["ScreeningSession"] = relationship("ScreeningSession", back_populates="result")

    def __repr__(self) -> str:
        return f"<ScreeningResult overall={self.overall_score} rec={self.recommendation}>"


class CommunicationLog(Base):
    __tablename__ = "communication_logs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    screening_session_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("screening_sessions.id", ondelete="CASCADE"), nullable=False
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )

    channel: Mapped[str] = mapped_column(String(50), nullable=False)  # whatsapp, sms, voice
    direction: Mapped[str] = mapped_column(String(20), nullable=False)  # outbound, inbound
    message: Mapped[str] = mapped_column(Text, nullable=False)
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    delivery_status: Mapped[str] = mapped_column(String(50), default="sent", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ScreeningSession"] = relationship("ScreeningSession", back_populates="logs")


class CandidateConsent(Base, TimestampMixin):
    __tablename__ = "candidate_consents"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    whatsapp_opt_in: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sms_opt_in: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    voice_opt_in: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    opted_out_all: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    opt_out_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
