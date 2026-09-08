"""
Interview models: an Interview belongs to a candidate+job (originating
from an Application), holds an ordered list of InterviewQuestions,
the candidate's InterviewAnswers, and one InterviewEvaluation summarizing
the whole thing once complete.
"""
import enum
import uuid
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, JSON, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InterviewType(str, enum.Enum):
    technical = "technical"
    behavioral = "behavioral"
    mixed = "mixed"
    ai_interview = "ai_interview"


class InterviewStatus(str, enum.Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("applications.id", ondelete="SET NULL"), nullable=True
    )

    interview_type: Mapped[InterviewType] = mapped_column(
        Enum(InterviewType, name="interview_type"), default=InterviewType.mixed, nullable=False
    )
    status: Mapped[InterviewStatus] = mapped_column(
        Enum(InterviewStatus, name="interview_status"), default=InterviewStatus.scheduled, nullable=False
    )
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    started_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    questions: Mapped[list["InterviewQuestion"]] = relationship(
        back_populates="interview", cascade="all, delete-orphan", order_by="InterviewQuestion.order_number"
    )
    evaluation: Mapped[Optional["InterviewEvaluation"]] = relationship(
        back_populates="interview", cascade="all, delete-orphan", uselist=False
    )
    candidate: Mapped["CandidateProfile"] = relationship()
    job: Mapped["Job"] = relationship()

    def __repr__(self) -> str:
        return f"<Interview {self.id} candidate={self.candidate_id} job={self.job_id}>"


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    interview_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(Text, nullable=False)  # technical/behavioral/problem_solving
    difficulty: Mapped[str] = mapped_column(Text, nullable=False)  # easy/medium/hard
    expected_topics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)

    interview: Mapped["Interview"] = relationship(back_populates="questions")
    answer: Mapped[Optional["InterviewAnswer"]] = relationship(back_populates="question", uselist=False)


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interview_questions.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_source: Mapped[str] = mapped_column(Text, default="text", nullable=False)  # "text" or "voice"
    answer_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON: strengths/improvements
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    question: Mapped["InterviewQuestion"] = relationship(back_populates="answer")


class InterviewEvaluation(Base):
    __tablename__ = "interview_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    interview_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interviews.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    technical_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    communication_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    relevance_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    problem_solving_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    weaknesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluation_json: Mapped[Optional[dict]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    source: Mapped[str] = mapped_column(Text, default="template", nullable=False)  # "llm" or "template"
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    interview: Mapped["Interview"] = relationship(back_populates="evaluation")
