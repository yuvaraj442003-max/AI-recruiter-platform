"""
resume_improvement.py — Pydantic schemas for AI Resume Improvement endpoints.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class ResumeImprovementRequest(BaseModel):
    candidate_id: str
    job_id: str


class AcceptImprovementRequest(BaseModel):
    candidate_id: str
    original_text: str
    improved_text: str
    section: Optional[str] = "experience"


class WeakSentenceItem(BaseModel):
    original: str
    recommended: str
    reason: List[str]
    needs_candidate_confirmation: bool = False


class AchievementSuggestionItem(BaseModel):
    original: str
    suggestion: str
    requires_confirmation: bool = True


class GrammarCorrectionItem(BaseModel):
    original: str
    corrected: str


class ResumeQualityScores(BaseModel):
    writing_quality: float
    keyword_optimization: float
    achievement_impact: float
    grammar: float
    formatting: float
    job_relevance: float


class SectionImprovementItem(BaseModel):
    section_name: str
    current_content: str
    problems_found: List[str]
    recommended_improvements: List[str]
    improved_version: str
    note: str


class ResumeImprovementResponse(BaseModel):
    candidate_id: str
    job_id: str
    overall_resume_quality: float
    scores: ResumeQualityScores
    weak_sentences: List[WeakSentenceItem]
    missing_keywords: List[str]
    missing_skills: List[str]
    achievement_suggestions: List[AchievementSuggestionItem]
    grammar_corrections: List[GrammarCorrectionItem]
    formatting_suggestions: List[str]
    priority_improvements: List[str]
    sections: List[SectionImprovementItem]

    model_config = ConfigDict(from_attributes=True)
