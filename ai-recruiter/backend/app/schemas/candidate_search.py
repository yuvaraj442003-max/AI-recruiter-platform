"""
candidate_search.py — Pydantic schemas for Smart Candidate Search endpoints.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SearchFilters(BaseModel):
    skills: Optional[List[str]] = Field(default_factory=list)
    skill_match_mode: Optional[str] = "all"  # "all" or "any"
    minimum_experience: Optional[float] = None
    maximum_experience: Optional[float] = None
    location: Optional[str] = None
    minimum_ats_score: Optional[float] = None
    minimum_interview_score: Optional[float] = None
    education: Optional[str] = None
    job_role: Optional[str] = None


class CandidateSearchRequest(BaseModel):
    query: Optional[str] = ""
    job_id: Optional[str] = None
    filters: Optional[SearchFilters] = Field(default_factory=SearchFilters)
    page: int = 1
    page_size: int = 20
    sort_by: str = "best_match"  # "best_match", "ats_score", "experience", "interview_score"


class CandidateSearchResultItem(BaseModel):
    candidate_id: str
    candidate_name: str
    candidate_email: Optional[str] = ""
    headline: Optional[str] = ""
    job_role: Optional[str] = ""
    location: Optional[str] = ""
    experience_years: float
    matched_skills: List[str]
    missing_skills: List[str]
    ats_score: float
    interview_score: Optional[float] = None
    ranking_score: float
    education: Optional[str] = ""

    model_config = ConfigDict(from_attributes=True)


class CandidateSearchResponse(BaseModel):
    total_results: int
    page: int
    page_size: int
    total_pages: int
    filters_applied: Dict[str, Any]
    results: List[CandidateSearchResultItem]

    model_config = ConfigDict(from_attributes=True)
