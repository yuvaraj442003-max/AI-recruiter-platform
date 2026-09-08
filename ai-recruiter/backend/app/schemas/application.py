"""
Schemas for job applications and match-score responses.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

from app.models.application import ApplicationStatus


class MatchBreakdown(BaseModel):
    skill_match: Optional[float] = None
    skills_match: Optional[float] = None
    experience_match: Optional[float] = None
    tfidf_match: Optional[float] = None
    semantic_match: Optional[float] = None
    preferred_skill_match: Optional[float] = None
    keyword_match: Optional[float] = None
    responsibility_match: Optional[float] = None
    education_match: Optional[float] = None
    location_match: Optional[float] = None
    readability: Optional[float] = None


class MatchExplanation(BaseModel):
    matched_required_skills: Optional[list[str]] = []
    missing_required_skills: Optional[list[str]] = []
    matched_preferred_skills: Optional[list[str]] = []
    missing_preferred_skills: Optional[list[str]] = []
    candidate_experience_years: Optional[float] = None
    required_experience_years: Optional[float] = None


class MatchScoreResponse(BaseModel):
    final_score: float
    breakdown: Union[MatchBreakdown, Dict[str, Any]]
    explanation: Union[MatchExplanation, Dict[str, Any], str]


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    status: ApplicationStatus
    match_score: Optional[float] = None
    applied_at: datetime
    updated_at: datetime

    # ATS Screening Breakdown Fields
    ats_score: Optional[float] = None
    job_match_score: Optional[float] = None
    skills_match_score: Optional[float] = None
    experience_match_score: Optional[float] = None
    education_match_score: Optional[float] = None
    location_match_score: Optional[float] = None
    keyword_match_score: Optional[float] = None
    responsibility_match_score: Optional[float] = None

    matched_skills: Optional[list[str]] = []
    missing_skills: Optional[list[str]] = []
    matched_keywords: Optional[list[str]] = []
    missing_keywords: Optional[list[str]] = []

    recommendation: Optional[str] = None
    screening_status: Optional[str] = None
    is_eligible: Optional[bool] = False
    is_shortlisted: Optional[bool] = False
    screened_at: Optional[datetime] = None
    screening_version: Optional[str] = "v1.0"

    recruiter_override: Optional[bool] = False
    override_reason: Optional[str] = None

    source: Optional[str] = "direct_candidate"
    uploaded_by_recruiter_id: Optional[Union[uuid.UUID, str]] = None

    # Denormalized display fields
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    job_title: Optional[str] = None


class ApplicationDetailResponse(ApplicationResponse):
    breakdown: Optional[Dict[str, Any]] = None
    explanation: Optional[Union[Dict[str, Any], str]] = None
    ats_report: Optional[Dict[str, Any]] = None
    candidate_profile: Optional[Dict[str, Any]] = None
    job_details: Optional[Dict[str, Any]] = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    override_reason: Optional[str] = None

