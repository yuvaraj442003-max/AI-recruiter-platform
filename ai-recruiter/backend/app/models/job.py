"""
Job model — a recruiter's job posting — and JobSkill, the join table
linking a job to required/preferred skills (mirrors CandidateSkill).
"""
import enum
import uuid
from typing import Optional

from sqlalchemy import Boolean, Enum, Float, ForeignKey, String, Text, UniqueConstraint
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class EmploymentType(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"


class JobStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    closed = "closed"
    paused = "paused"
    pending_review = "pending_review"
    flagged = "flagged"


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType, name="employment_type"), default=EmploymentType.full_time, nullable=False
    )
    experience_required: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, name="job_status"), default=JobStatus.published, nullable=False
    )

    # Experience, Skills & Company Requirements Breakdown
    relevant_work_experience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    non_technical_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_experience_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Fraud Detection & Risk Scoring
    fraud_risk_score: Mapped[Optional[float]] = mapped_column(Float, default=0.0, nullable=True)
    fraud_risk_level: Mapped[Optional[str]] = mapped_column(String(20), default="LOW", nullable=True) # LOW, MEDIUM, HIGH
    fraud_reasons: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # JSON list

    # Company Details
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_logo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    company_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    linkedin_profile: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    github_profile: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    other_links: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Candidate Screening Settings
    min_ats_score: Mapped[Optional[float]] = mapped_column(Float, default=60.0, nullable=True)
    min_job_match_score: Mapped[Optional[float]] = mapped_column(Float, default=60.0, nullable=True)
    min_experience: Mapped[Optional[float]] = mapped_column(Float, default=0.0, nullable=True)
    auto_screening: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, nullable=True)
    auto_shortlist: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, nullable=True)

    job_skills: Mapped[list["JobSkill"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    applications: Mapped[list["Application"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    coding_assessments: Mapped[list["CodingAssessment"]] = relationship("CodingAssessment", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job {self.title}>"


class JobSkill(Base):
    __tablename__ = "job_skills"
    __table_args__ = (UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),)

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    job: Mapped["Job"] = relationship(back_populates="job_skills")
    skill: Mapped["Skill"] = relationship()
