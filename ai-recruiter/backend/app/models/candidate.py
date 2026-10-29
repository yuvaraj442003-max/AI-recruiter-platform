"""
Candidate-side models: the candidate's profile (built from their parsed
resume), the shared skills knowledge base, and the join table linking
candidates to the skills found in their resume.
"""
import uuid
from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class CandidateProfile(Base, TimestampMixin):
    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    _full_name: Mapped[Optional[str]] = mapped_column("full_name", String(255), nullable=True)  # Extracted from resume (source of truth)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)          # full address block
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    experience_years: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    education: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    work_experience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # raw work-history text

    resume_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resume_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resume_original_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resume_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    profile_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # LinkedIn-Style Professional Profile Fields
    profile_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    current_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    certifications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    portfolio_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    other_links: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # College Student & Academic Information
    is_student: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    college_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    degree: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # B.Tech, BCA, MCA, B.Sc, M.Tech
    branch: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)  # Computer Science, IT, AI & Data Science
    graduation_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 2024, 2025, 2026, 2027
    cgpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 8.75
    current_semester: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1 to 8
    target_role: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)  # SDE, Frontend, Data Analyst

    # 12th Grade / HSC / Intermediate Credentials
    twelfth_school: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    twelfth_board: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    twelfth_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    twelfth_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # 10th Grade / SSLC Credentials
    tenth_school: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tenth_board: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tenth_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tenth_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Recruiter Upload & Source Tracking
    created_by_recruiter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    source: Mapped[Optional[str]] = mapped_column(String(100), default="direct_candidate", nullable=True)

    candidate_skills: Mapped[list["CandidateSkill"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    portfolio: Mapped[Optional["Portfolio"]] = relationship(
        "Portfolio", back_populates="candidate", uselist=False, cascade="all, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        # Strict Guarantee: Extract candidate name directly from uploaded resume as single source of truth
        val = getattr(self, "_full_name", None)
        if val and isinstance(val, str) and val.strip():
            return val.strip()
        if self.resume_text:
            try:
                from app.nlp.skill_extractor import parse_resume_fields
                fields = parse_resume_fields(self.resume_text[:2500])
                if fields.get("name") and len(fields["name"].strip()) >= 2:
                    return fields["name"].strip()
            except Exception:
                pass
        return self.user.name if (self.user and self.user.name) else "Candidate"

    @full_name.setter
    def full_name(self, value: Optional[str]):
        self._full_name = value.strip() if (value and isinstance(value, str)) else None

    def __repr__(self) -> str:
        return f"<CandidateProfile user_id={self.user_id}>"


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    skill_name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<Skill {self.skill_name}>"


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    __table_args__ = (UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skill"),)

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    proficiency: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    years_of_experience: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    candidate: Mapped["CandidateProfile"] = relationship(back_populates="candidate_skills")
    skill: Mapped["Skill"] = relationship()
