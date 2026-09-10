"""
Coding models — tables supporting coding question banks, test cases,
assessments, candidate attempts, code submissions, and execution metrics.
"""
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class CodingQuestion(Base, TimestampMixin):
    __tablename__ = "coding_questions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), default="Medium", nullable=False)  # Easy, Medium, Hard
    category: Mapped[str] = mapped_column(String(100), default="Algorithms", nullable=False)
    programming_languages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array string e.g. ["python","javascript"]
    starter_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON object mapping lang -> starter_code
    expected_output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    constraints: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    test_cases: Mapped[List["CodingTestCase"]] = relationship(
        "CodingTestCase", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CodingQuestion id={self.id} title={self.title} difficulty={self.difficulty}>"


class CodingTestCase(Base, TimestampMixin):
    __tablename__ = "coding_test_cases"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("coding_questions.id", ondelete="CASCADE"), nullable=False
    )
    input_data: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    question: Mapped["CodingQuestion"] = relationship("CodingQuestion", back_populates="test_cases")


class CodingAssessment(Base, TimestampMixin):
    __tablename__ = "coding_assessments"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    passing_score: Mapped[float] = mapped_column(Float, default=60.0, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    allowed_languages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string e.g. ["python","javascript","java"]

    # AI-Assisted Integrity Monitoring Configuration
    enable_tab_monitoring: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_fullscreen: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_webcam: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_audio: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_code_similarity: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    clipboard_policy: Mapped[str] = mapped_column(String(20), default="monitor", nullable=False)  # monitor, block, flag

    job: Mapped[Optional["Job"]] = relationship("Job", back_populates="coding_assessments")
    questions: Mapped[List["CodingAssessmentQuestion"]] = relationship(
        "CodingAssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan", order_by="CodingAssessmentQuestion.question_order"
    )
    attempts: Mapped[List["CandidateCodingAttempt"]] = relationship(
        "CandidateCodingAttempt", back_populates="assessment", cascade="all, delete-orphan"
    )


class CodingAssessmentQuestion(Base):
    __tablename__ = "coding_assessment_questions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("coding_assessments.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("coding_questions.id", ondelete="CASCADE"), nullable=False
    )
    question_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    points: Mapped[float] = mapped_column(Float, default=20.0, nullable=False)

    assessment: Mapped["CodingAssessment"] = relationship("CodingAssessment", back_populates="questions")
    question: Mapped["CodingQuestion"] = relationship("CodingQuestion")


class CandidateCodingAttempt(Base, TimestampMixin):
    __tablename__ = "candidate_coding_attempts"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("coding_assessments.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="Not Started", nullable=False)  # Not Started, In Progress, Submitted, Evaluated, Expired
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    time_taken: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in seconds

    candidate: Mapped["CandidateProfile"] = relationship("CandidateProfile")
    assessment: Mapped["CodingAssessment"] = relationship("CodingAssessment", back_populates="attempts")
    submissions: Mapped[List["CodingSubmission"]] = relationship(
        "CodingSubmission", back_populates="attempt", cascade="all, delete-orphan"
    )
    integrity_result: Mapped[Optional["IntegrityResult"]] = relationship(
        "IntegrityResult", back_populates="attempt", uselist=False, cascade="all, delete-orphan"
    )
    events: Mapped[List["AssessmentEvent"]] = relationship(
        "AssessmentEvent", back_populates="attempt", cascade="all, delete-orphan"
    )


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_coding_attempts.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("coding_questions.id", ondelete="CASCADE"), nullable=False
    )
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    source_code: Mapped[str] = mapped_column(Text, nullable=False)
    execution_status: Mapped[str] = mapped_column(String(50), default="Success", nullable=False)
    test_cases_passed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    test_cases_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    functional_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    efficiency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    complexity_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    time_complexity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    space_complexity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ai_review: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    execution_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    memory_used: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    attempt: Mapped["CandidateCodingAttempt"] = relationship("CandidateCodingAttempt", back_populates="submissions")
    question: Mapped["CodingQuestion"] = relationship("CodingQuestion")
