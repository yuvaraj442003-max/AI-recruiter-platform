"""
blind_screening.py — Pydantic schemas for Blind Screening Mode.
Defines server-side anonymized candidate response DTOs (strictly omitting name, photo, email, phone, age, gender, location, college).
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class EducationSanitizedItem(BaseModel):
    degree: str
    field: str


class BlindCandidateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    candidate_code: str = Field(..., description="Stable non-identifying candidate code e.g. CAND-10452")
    job_id: uuid.UUID
    experience_years: float = Field(default=0.0)
    skills: List[str] = Field(default_factory=list)
    ats_score: float = Field(default=0.0)
    role_match_score: float = Field(default=0.0)
    skills_match: float = Field(default=0.0)
    experience_match: float = Field(default=0.0)
    technical_assessment_score: Optional[float] = None
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    relevant_experience: List[str] = Field(default_factory=list)
    education: List[EducationSanitizedItem] = Field(default_factory=list)
    sanitized_resume_summary: Optional[str] = None
    screening_status: str = Field(default="pending")
    recruiter_decision: Optional[str] = None
    revealed: bool = Field(default=False)


class BlindCandidateDetailOut(BlindCandidateOut):
    sanitized_resume_text: Optional[str] = None
    match_explanation: Optional[str] = None


class BlindScreeningConfigOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    enabled: bool
    hide_name: bool
    hide_photo: bool
    hide_age: bool
    hide_gender: bool
    hide_location: bool
    hide_college: bool
    hide_email: bool
    hide_phone: bool
    hide_address: bool
    hide_social_links: bool
    reveal_policy: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class BlindScreeningConfigUpdate(BaseModel):
    enabled: Optional[bool] = None
    hide_name: Optional[bool] = None
    hide_photo: Optional[bool] = None
    hide_age: Optional[bool] = None
    hide_gender: Optional[bool] = None
    hide_location: Optional[bool] = None
    hide_college: Optional[bool] = None
    hide_email: Optional[bool] = None
    hide_phone: Optional[bool] = None
    hide_address: Optional[bool] = None
    hide_social_links: Optional[bool] = None
    reveal_policy: Optional[str] = Field(default=None, description="reveal_after_shortlist, manual, reveal_after_interview")


class BlindDecisionRequest(BaseModel):
    decision: str = Field(..., description="shortlist, hold, reject, or next_round")


class BlindStatisticsOut(BaseModel):
    job_id: uuid.UUID
    job_title: Optional[str] = None
    blind_screening_enabled: bool
    total_candidates: int
    shortlisted_count: int
    hold_count: int
    rejected_count: int
    revealed_count: int
