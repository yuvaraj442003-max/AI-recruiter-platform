"""
comparison.py — Pydantic schemas for Candidate Comparison endpoints.
"""
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class CandidateComparisonRequest(BaseModel):
    job_id: str
    candidate_ids: List[str] = Field(..., min_length=2, max_length=5)


class CandidateComparisonItem(BaseModel):
    candidate_id: str
    application_id: Optional[str] = None
    candidate_name: str
    candidate_email: Optional[str] = None
    headline: Optional[str] = None
    experience_years: float
    education: str
    location: str
    overall_ats_score: float
    skills_match: float
    experience_match: float
    keywords_match: float
    responsibilities_match: float
    education_match: float
    location_match: float
    interview_score: Optional[float] = None
    matched_skills: List[str]
    missing_skills: List[str]
    matched_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]

    model_config = ConfigDict(from_attributes=True)


class RecommendationData(BaseModel):
    best_candidate_id: str
    best_candidate_name: str
    recommendation_score: float
    reason: List[str]
    concerns: List[str]

    model_config = ConfigDict(from_attributes=True)


class CandidateComparisonResponse(BaseModel):
    job_id: str
    job_title: str
    candidates: List[CandidateComparisonItem]
    recommendation: RecommendationData

    model_config = ConfigDict(from_attributes=True)


# Aliases for analytics and legacy routes
CandidateCompareRequest = CandidateComparisonRequest
CandidateCompareResponse = CandidateComparisonResponse
