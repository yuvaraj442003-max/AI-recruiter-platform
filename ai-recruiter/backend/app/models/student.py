"""
student.py — Models for College Student Placement & Preparation Ecosystem.
Includes:
- Aptitude Topics & Question Bank
- Aptitude Practice Tests & Student Attempts
- Study Materials, Cheat Sheets & Learning Roadmaps
- Student Roadmap Progress Tracking
"""
import uuid
from typing import Optional
from datetime import datetime

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


class AptitudeTopic(Base, TimestampMixin):
    __tablename__ = "aptitude_topics"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="📊", nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    questions: Mapped[list["AptitudeQuestion"]] = relationship("AptitudeQuestion", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AptitudeTopic {self.name}>"


class AptitudeQuestion(Base, TimestampMixin):
    __tablename__ = "aptitude_questions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), ForeignKey("aptitude_topics.id", ondelete="SET NULL"), nullable=True, index=True)
    test_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), ForeignKey("aptitude_tests.id", ondelete="CASCADE"), nullable=True, index=True)
    subtopic: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    topic_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    options_json: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array of 4 options e.g. ["A", "B", "C", "D"]
    correct_option_index: Mapped[int] = mapped_column(Integer, nullable=False)  # 0, 1, 2, or 3
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)  # easy, medium, hard
    marks: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    company_tag: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)  # TCS, Infosys, Amazon, Wipro, General
    status: Mapped[str] = mapped_column(String(50), default="approved", nullable=False)  # approved, pending_review, draft
    week_assigned: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)  # e.g. "2026-W42"

    topic: Mapped[Optional["AptitudeTopic"]] = relationship("AptitudeTopic", back_populates="questions")
    test: Mapped[Optional["AptitudeTest"]] = relationship("AptitudeTest", back_populates="questions")
    options: Mapped[list["AptitudeOption"]] = relationship("AptitudeOption", back_populates="question", cascade="all, delete-orphan", order_by="AptitudeOption.order_index")

    def __repr__(self) -> str:
        return f"<AptitudeQuestion {self.subtopic} ({self.difficulty}) status={self.status}>"


class AptitudeOption(Base, TimestampMixin):
    __tablename__ = "aptitude_options"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("aptitude_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    option_letter: Mapped[str] = mapped_column(String(5), nullable=False)  # A, B, C, D
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    question: Mapped["AptitudeQuestion"] = relationship("AptitudeQuestion", back_populates="options")

    def __repr__(self) -> str:
        return f"<AptitudeOption {self.option_letter}: {self.option_text[:20]} is_correct={self.is_correct}>"


class AptitudeTest(Base, TimestampMixin):
    __tablename__ = "aptitude_tests"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), default="topic_test", nullable=False)  # recruiter_test, daily_practice, topic_test, company_mock
    company_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g. TCS NQT, Infosys SP, Cognizant
    topics_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list of topic names
    difficulty: Mapped[str] = mapped_column(String(50), default="mixed", nullable=False)  # easy, medium, hard, mixed
    duration_minutes: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    marks_per_question: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, default=15.0, nullable=False)
    passing_percentage: Mapped[float] = mapped_column(Float, default=60.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="published", nullable=False)  # draft, published, archived
    question_ids_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list of question UUIDs
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    questions: Mapped[list["AptitudeQuestion"]] = relationship("AptitudeQuestion", back_populates="test", cascade="all, delete-orphan")
    attempts: Mapped[list["AptitudeAttempt"]] = relationship("AptitudeAttempt", back_populates="test", cascade="all, delete-orphan")
    candidate_attempts: Mapped[list["CandidateTestAttempt"]] = relationship("CandidateTestAttempt", back_populates="test", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AptitudeTest {self.title} status={self.status}>"


class CandidateTestAttempt(Base, TimestampMixin):
    __tablename__ = "candidate_test_attempts"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    test_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("aptitude_tests.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="In Progress", nullable=False)  # In Progress, Submitted, Evaluated, Expired
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    test: Mapped["AptitudeTest"] = relationship("AptitudeTest", back_populates="candidate_attempts")
    answers: Mapped[list["CandidateAnswer"]] = relationship("CandidateAnswer", back_populates="attempt", cascade="all, delete-orphan")
    result: Mapped[Optional["AptitudeTestResult"]] = relationship("AptitudeTestResult", back_populates="attempt", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CandidateTestAttempt user={self.user_id} test={self.test_id} status={self.status}>"


class CandidateAnswer(Base, TimestampMixin):
    __tablename__ = "candidate_answers"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("candidate_test_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("aptitude_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_option_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), ForeignKey("aptitude_options.id", ondelete="SET NULL"), nullable=True)
    selected_option_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0, 1, 2, 3
    selected_option_letter: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)  # A, B, C, D
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    marks_awarded: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    attempt: Mapped["CandidateTestAttempt"] = relationship("CandidateTestAttempt", back_populates="answers")
    question: Mapped["AptitudeQuestion"] = relationship("AptitudeQuestion")
    selected_option: Mapped[Optional["AptitudeOption"]] = relationship("AptitudeOption")

    def __repr__(self) -> str:
        return f"<CandidateAnswer attempt={self.attempt_id} question={self.question_id} is_correct={self.is_correct}>"


class AptitudeTestResult(Base, TimestampMixin):
    __tablename__ = "aptitude_test_results"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("candidate_test_attempts.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    test_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("aptitude_tests.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wrong_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unanswered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    percentile_estimate: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    topic_breakdown_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feedback_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    attempt: Mapped["CandidateTestAttempt"] = relationship("CandidateTestAttempt", back_populates="result")
    test: Mapped["AptitudeTest"] = relationship("AptitudeTest")

    def __repr__(self) -> str:
        return f"<AptitudeTestResult attempt={self.attempt_id} score={self.score} ({self.percentage}%)>"


class AptitudeAttempt(Base, TimestampMixin):
    __tablename__ = "aptitude_attempts"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    test_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), ForeignKey("aptitude_tests.id", ondelete="SET NULL"), nullable=True, index=True)
    topic_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wrong_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unanswered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    answers_summary_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON records of question details, user choice, correct choice

    test: Mapped[Optional["AptitudeTest"]] = relationship("AptitudeTest", back_populates="attempts")

    def __repr__(self) -> str:
        return f"<AptitudeAttempt user={self.user_id} score={self.score_percentage}%>"


class StudyMaterial(Base, TimestampMixin):
    __tablename__ = "study_materials"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # dsa, core_cs, web_dev, aptitude, interview_prep, company_guide
    content_type: Mapped[str] = mapped_column(String(50), default="guide", nullable=False)  # cheatsheet, guide, roadmap, notes
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    company_tag: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="beginner", nullable=False)  # beginner, intermediate, advanced
    estimated_read_time: Mapped[str] = mapped_column(String(50), default="10 mins", nullable=False)
    tags_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of tags
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<StudyMaterial {self.title}>"


class LearningRoadmap(Base, TimestampMixin):
    __tablename__ = "learning_roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    role_target: Mapped[str] = mapped_column(String(150), nullable=False)  # Full-Stack, Data Analyst, Campus 60-Day Sprint
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="🎯", nullable=False)
    estimated_weeks: Mapped[int] = mapped_column(Integer, default=8, nullable=False)
    milestones_json: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array of milestone objects

    progress_records: Mapped[list["StudentRoadmapProgress"]] = relationship("StudentRoadmapProgress", back_populates="roadmap", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<LearningRoadmap {self.title}>"


class StudentRoadmapProgress(Base, TimestampMixin):
    __tablename__ = "student_roadmap_progress"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    roadmap_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("learning_roadmaps.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_milestones_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)  # JSON array of milestone ids or step indexes
    scores_json: Mapped[Optional[str]] = mapped_column(Text, default="{}", nullable=True)  # JSON map of milestone_id -> {score, total, percentage, passed, timestamp}
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    roadmap: Mapped["LearningRoadmap"] = relationship("LearningRoadmap", back_populates="progress_records")

    def __repr__(self) -> str:
        return f"<StudentRoadmapProgress user={self.user_id} progress={self.progress_percent}%>"


class StudentLearningPreference(Base, TimestampMixin):
    __tablename__ = "student_learning_preferences"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    selected_topics_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)  # JSON list of chosen topic strings
    custom_topics_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)    # JSON list of user-added custom topics
    daily_streak: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    last_assessment_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # e.g. "2026-10-15"
    history_json: Mapped[Optional[str]] = mapped_column(Text, default="[]", nullable=True) # JSON list of past assessments
    journey_state_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # Stage-gated roadmap, recommendations, daily plan, strengths

    def __repr__(self) -> str:
        return f"<StudentLearningPreference user={self.user_id}>"
