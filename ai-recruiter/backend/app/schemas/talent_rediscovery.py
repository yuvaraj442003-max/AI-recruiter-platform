"""
talent_rediscovery.py — Pydantic schemas for Talent Pool Auto-Rediscovery & Silver Medalist Matching System.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class TalentRediscoveryRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    status: str
    total_candidates: int
    processed_candidates: int
    matched_candidates: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class TalentRediscoveryResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_headline: Optional[str] = None
    candidate_location: Optional[str] = None
    experience_years: Optional[float] = None
    overall_score: float
    skills_score: float
    experience_score: float
    semantic_score: float
    responsibility_score: float
    keyword_score: float
    location_score: float
    education_score: float
    rank: int
    is_silver_medalist: bool
    previous_job_id: Optional[uuid.UUID] = None
    previous_job_title: Optional[str] = None
    previous_application_status: Optional[str] = None
    previous_ats_score: Optional[float] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []
    match_explanation: Optional[str] = None
    status: str
    created_at: datetime


class TalentRediscoverySummaryOut(BaseModel):
    job_id: uuid.UUID
    job_title: Optional[str] = None
    total_candidates_analyzed: int
    matched_candidates_count: int
    silver_medalists_count: int
    top_match_score: float
    average_match_score: float
    status: str


class SmartSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Natural language search query e.g. 'Senior React developers with 5+ years'")
    min_score: float = Field(default=50.0, ge=0.0, le=100.0)
    silver_medalist_only: bool = Field(default=False)
