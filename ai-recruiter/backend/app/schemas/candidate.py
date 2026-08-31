"""
Schemas for the candidate profile and resume upload responses.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SkillOut(BaseModel):
    id: uuid.UUID
    skill_name: str
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CandidateProfileUpdate(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    summary: Optional[str] = None
    experience_years: Optional[float] = None
    education: Optional[str] = None
    work_experience: Optional[str] = None
    skills: Optional[list[str]] = None

    # LinkedIn-Style Professional Profile Fields
    profile_photo: Optional[str] = None
    headline: Optional[str] = None
    current_role: Optional[str] = None
    certifications: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    other_links: Optional[str] = None


class CandidateProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    phone: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    summary: Optional[str] = None
    experience_years: Optional[float] = None
    education: Optional[str] = None
    work_experience: Optional[str] = None
    resume_original_filename: Optional[str] = None
    ai_summary: Optional[str] = None
    profile_score: Optional[int] = None
    skills: list[str] = []

    # LinkedIn-Style Professional Profile Fields
    profile_photo: Optional[str] = None
    headline: Optional[str] = None
    current_role: Optional[str] = None
    certifications: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    other_links: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_profile(cls, profile) -> "CandidateProfileResponse":
        return cls(
            id=profile.id,
            user_id=profile.user_id,
            phone=profile.phone,
            location=profile.location,
            address=getattr(profile, "address", None),
            summary=profile.summary,
            experience_years=profile.experience_years,
            education=profile.education,
            work_experience=getattr(profile, "work_experience", None),
            resume_original_filename=profile.resume_original_filename,
            ai_summary=profile.ai_summary,
            profile_score=profile.profile_score,
            skills=sorted({cs.skill.skill_name for cs in profile.candidate_skills}),
            profile_photo=getattr(profile, "profile_photo", None),
            headline=getattr(profile, "headline", None),
            current_role=getattr(profile, "current_role", None),
            certifications=getattr(profile, "certifications", None),
            portfolio_url=getattr(profile, "portfolio_url", None),
            linkedin_url=getattr(profile, "linkedin_url", None),
            github_url=getattr(profile, "github_url", None),
            other_links=getattr(profile, "other_links", None),
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )


class RecruiterProfileUpdate(BaseModel):
    profile_photo: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    company_description: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    other_links: Optional[str] = None


class RecruiterProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    recruiter_name: Optional[str] = None
    email: Optional[str] = None
    profile_photo: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    company_description: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    other_links: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

