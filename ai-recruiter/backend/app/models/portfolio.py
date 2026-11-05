"""
portfolio.py — Candidate Portfolio Model.
Stores candidate-customized portfolio website content, theme selection,
styling tokens, section ordering/visibility, and public URL slug.
"""
import uuid
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class Portfolio(Base, TimestampMixin):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )

    # Public accessibility
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Theme and visual presentation tokens
    theme_id: Mapped[str] = mapped_column(String(50), default="modern", nullable=False)
    primary_color: Mapped[str] = mapped_column(String(50), default="#4f46e5", nullable=False)
    secondary_color: Mapped[str] = mapped_column(String(50), default="#06b6d4", nullable=False)
    font: Mapped[str] = mapped_column(String(50), default="Plus Jakarta Sans", nullable=False)
    background_style: Mapped[str] = mapped_column(String(50), default="mesh", nullable=False)
    background_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    dark_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    button_style: Mapped[str] = mapped_column(String(50), default="rounded", nullable=False)
    card_style: Mapped[str] = mapped_column(String(50), default="glass", nullable=False)
    layout: Mapped[str] = mapped_column(String(50), default="standard", nullable=False)

    # Sections configuration (JSON stringified)
    section_order: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    section_visibility: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Candidate Profile & Content Presentation (JSON stringified for structured entities)
    profile_image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    professional_headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    headline_options: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    about: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    education: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    projects: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    certifications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    achievements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    services: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    social_links: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_css: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generation_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship to CandidateProfile
    candidate: Mapped["CandidateProfile"] = relationship(back_populates="portfolio")

    def __repr__(self) -> str:
        return f"<Portfolio candidate_id={self.candidate_id} slug={self.slug} theme={self.theme_id} published={self.is_published}>"
