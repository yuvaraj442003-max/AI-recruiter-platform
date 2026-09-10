"""
interview_scorecard.py — Database models for AI Executive Candidate Scorecard & Interview Intelligence.
Stores overall candidate scorecards, job-specific evaluation categories, timestamped key moments,
interview chapters, question evaluations, and evidence links to exact video/audio timestamps.
"""
import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class CandidateRecommendation(str, enum.Enum):
    strong_candidate = "Strong Candidate"
    recommended = "Recommended"
    consider = "Consider"
    review_required = "Review Required"
    not_recommended = "Not Recommended"


class MomentImportance(str, enum.Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class InterviewScorecard(Base, TimestampMixin):
    __tablename__ = "interview_scorecards"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    interview_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )

    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    recommendation: Mapped[CandidateRecommendation] = mapped_column(
        Enum(CandidateRecommendation, name="candidate_recommendation_enum"),
        default=CandidateRecommendation.recommended,
        nullable=False,
    )
    executive_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[str] = mapped_column(String(50), default="High", nullable=False)  # High, Medium, Low

    # Strengths and Areas to Review (JSON string arrays)
    strengths_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weaknesses_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Recruiter Override & Final Decision
    recruiter_decision: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Strong Candidate, Shortlist, Hold, Reject
    recruiter_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    interview: Mapped["Interview"] = relationship("Interview")
    categories: Mapped[list["InterviewScoreCategory"]] = relationship(
        "InterviewScoreCategory", back_populates="scorecard", cascade="all, delete-orphan"
    )
    key_moments: Mapped[list["InterviewKeyMoment"]] = relationship(
        "InterviewKeyMoment", back_populates="scorecard", cascade="all, delete-orphan", order_by="InterviewKeyMoment.timestamp_start"
    )
    chapters: Mapped[list["InterviewChapter"]] = relationship(
        "InterviewChapter", back_populates="scorecard", cascade="all, delete-orphan", order_by="InterviewChapter.sequence"
    )
    question_evaluations: Mapped[list["InterviewQuestionEvaluation"]] = relationship(
        "InterviewQuestionEvaluation", back_populates="scorecard", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<InterviewScorecard interview={self.interview_id} score={self.overall_score} rec={self.recommendation}>"


class InterviewScoreCategory(Base):
    __tablename__ = "interview_score_categories"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    scorecard_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interview_scorecards.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped[str] = mapped_column(String(100), nullable=False)  # Technical Knowledge, Problem Solving, Communication, Soft Skills, Role Fit
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), default="High", nullable=False)  # High, Medium, Low, Insufficient Evidence
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    evidence_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    scorecard: Mapped["InterviewScorecard"] = relationship("InterviewScorecard", back_populates="categories")


class InterviewKeyMoment(Base):
    __tablename__ = "interview_key_moments"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    scorecard_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interview_scorecards.id", ondelete="CASCADE"), nullable=False
    )

    timestamp_start: Mapped[int] = mapped_column(Integer, nullable=False)  # timestamp in seconds
    timestamp_end: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # Technical Insight, Strong Answer, Weak Area, System Design, Communication
    importance: Mapped[MomentImportance] = mapped_column(
        Enum(MomentImportance, name="moment_importance_enum"), default=MomentImportance.high, nullable=False
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    transcript_reference: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.90, nullable=False)

    scorecard: Mapped["InterviewScorecard"] = relationship("InterviewScorecard", back_populates="key_moments")


class InterviewChapter(Base):
    __tablename__ = "interview_chapters"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    scorecard_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interview_scorecards.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp_start: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_end: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    scorecard: Mapped["InterviewScorecard"] = relationship("InterviewScorecard", back_populates="chapters")


class InterviewQuestionEvaluation(Base):
    __tablename__ = "interview_question_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    scorecard_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("interview_scorecards.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("interview_questions.id", ondelete="SET NULL"), nullable=True
    )

    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_answer: Mapped[str] = mapped_column(Text, nullable=False)
    technical_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    accuracy_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    completeness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    clarity_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    evaluation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    timestamp_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    scorecard: Mapped["InterviewScorecard"] = relationship("InterviewScorecard", back_populates="question_evaluations")
