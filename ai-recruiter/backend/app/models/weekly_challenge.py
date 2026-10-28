"""
weekly_challenge.py — Models for Weekly Aptitude and Coding Challenges,
Candidate Attempts, Weekly Sets, and Performance Leaderboards.
"""
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class WeeklyAptitudeSet(Base, TimestampMixin):
    __tablename__ = "weekly_aptitude_sets"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    week_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)  # e.g. "2026-W42"
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    passing_percentage: Mapped[float] = mapped_column(Float, default=60.0, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    question_ids_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)  # JSON list of UUID strings
    status: Mapped[str] = mapped_column(String(50), default="published", nullable=False)  # published, draft, archived
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    attempts: Mapped[List["WeeklyAptitudeAttempt"]] = relationship(
        "WeeklyAptitudeAttempt", back_populates="weekly_set", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WeeklyAptitudeSet {self.week_code} - {self.title}>"


class WeeklyAptitudeAttempt(Base, TimestampMixin):
    __tablename__ = "weekly_aptitude_attempts"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    weekly_set_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("weekly_aptitude_sets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    score_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wrong_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unanswered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    answers_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON question_id -> selected_index
    percentile_estimate: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    feedback_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_anonymous_leaderboard: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User")
    weekly_set: Mapped["WeeklyAptitudeSet"] = relationship("WeeklyAptitudeSet", back_populates="attempts")

    def __repr__(self) -> str:
        return f"<WeeklyAptitudeAttempt user={self.user_id} week={self.weekly_set_id} score={self.score_percentage}%>"


class WeeklyCodingChallenge(Base, TimestampMixin):
    __tablename__ = "weekly_coding_challenges"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    week_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)  # e.g. "2026-W42"
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    passing_score: Mapped[float] = mapped_column(Float, default=60.0, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), default="Mixed", nullable=False)  # Easy, Medium, Hard, Mixed
    allowed_languages: Mapped[str] = mapped_column(
        Text, default='["python","javascript","java","cpp"]', nullable=False
    )
    question_ids_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)  # JSON list of UUID strings
    status: Mapped[str] = mapped_column(String(50), default="published", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    attempts: Mapped[List["WeeklyCodingAttempt"]] = relationship(
        "WeeklyCodingAttempt", back_populates="challenge", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WeeklyCodingChallenge {self.week_code} - {self.title}>"


class WeeklyCodingAttempt(Base, TimestampMixin):
    __tablename__ = "weekly_coding_attempts"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("weekly_coding_challenges.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(50), default="Submitted", nullable=False)  # In Progress, Submitted, Evaluated
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submissions_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON detail per question
    is_anonymous_leaderboard: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User")
    challenge: Mapped["WeeklyCodingChallenge"] = relationship("WeeklyCodingChallenge", back_populates="attempts")

    def __repr__(self) -> str:
        return f"<WeeklyCodingAttempt user={self.user_id} challenge={self.challenge_id} score={self.score}>"
