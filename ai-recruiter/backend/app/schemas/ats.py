"""
ats.py — Pydantic schemas for ATS Analysis endpoints.
"""
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ATSBreakdown(BaseModel):
    skills: float
    experience: float
    keywords: float
    responsibilities: float
    education: float
    location: float


class ATSAnalysisResponse(BaseModel):
    candidate_id: str
    job_id: str
    overall_ats_score: float
    score_breakdown: ATSBreakdown
    matched_skills: List[str]
    missing_skills: List[str]
    matched_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
    candidate_experience: Optional[float] = 0.0
    required_experience: Optional[float] = 0.0
    education_matched: Optional[bool] = True
    location_matched: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class JobMatchItem(BaseModel):
    job_id: str
    job_title: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    overall_ats_score: float
    screening_status: str

    model_config = ConfigDict(from_attributes=True)
