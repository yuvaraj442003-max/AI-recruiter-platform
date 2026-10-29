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
    name: Optional[str] = None
    full_name: Optional[str] = None
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

    # College Academic Credentials
    college_name: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None

    # 12th Grade / HSC / Intermediate Credentials
    twelfth_school: Optional[str] = None
    twelfth_board: Optional[str] = None
    twelfth_year: Optional[int] = None
    twelfth_percentage: Optional[float] = None

    # 10th Grade / SSLC Credentials
    tenth_school: Optional[str] = None
    tenth_board: Optional[str] = None
    tenth_year: Optional[int] = None
    tenth_percentage: Optional[float] = None


class CandidateProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: Optional[str] = None
    full_name: Optional[str] = None
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
    portfolio_slug: Optional[str] = None
    is_portfolio_published: Optional[bool] = False
    published_portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    other_links: Optional[str] = None

    # College Academic Credentials
    college_name: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None

    # 12th Grade / HSC / Intermediate Credentials
    twelfth_school: Optional[str] = None
    twelfth_board: Optional[str] = None
    twelfth_year: Optional[int] = None
    twelfth_percentage: Optional[float] = None

    # 10th Grade / SSLC Credentials
    tenth_school: Optional[str] = None
    tenth_board: Optional[str] = None
    tenth_year: Optional[int] = None
    tenth_percentage: Optional[float] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_profile(cls, profile) -> "CandidateProfileResponse":
        port = getattr(profile, "portfolio", None)
        is_published = bool(port and port.is_published)
        port_slug = port.slug if is_published else None

        cand_name = getattr(profile, "full_name", None)
        if not cand_name and getattr(profile, "resume_text", None):
            from app.nlp.skill_extractor import parse_resume_fields
            try:
                cand_name = parse_resume_fields(profile.resume_text).get("name")
            except Exception:
                pass
        if not cand_name:
            cand_name = getattr(getattr(profile, "user", None), "name", None)

        return cls(
            id=profile.id,
            user_id=profile.user_id,
            name=cand_name,
            full_name=cand_name,
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
            portfolio_slug=port_slug,
            is_portfolio_published=is_published,
            published_portfolio_url=f"/portfolio/{port_slug}" if port_slug else None,
            linkedin_url=getattr(profile, "linkedin_url", None),
            github_url=getattr(profile, "github_url", None),
            other_links=getattr(profile, "other_links", None),
            college_name=getattr(profile, "college_name", None),
            degree=getattr(profile, "degree", None),
            branch=getattr(profile, "branch", None),
            graduation_year=getattr(profile, "graduation_year", None),
            cgpa=getattr(profile, "cgpa", None),
            twelfth_school=getattr(profile, "twelfth_school", None),
            twelfth_board=getattr(profile, "twelfth_board", None),
            twelfth_year=getattr(profile, "twelfth_year", None),
            twelfth_percentage=getattr(profile, "twelfth_percentage", None),
            tenth_school=getattr(profile, "tenth_school", None),
            tenth_board=getattr(profile, "tenth_board", None),
            tenth_year=getattr(profile, "tenth_year", None),
            tenth_percentage=getattr(profile, "tenth_percentage", None),
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

