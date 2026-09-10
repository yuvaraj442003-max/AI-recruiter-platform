"""
feedback.py — Pydantic Schemas for Automated Candidate Feedback System.
Defines serializers for candidate-facing feedback, recruiter review drawers,
structured LLM JSON response validation, and bulk feedback payloads.
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class CandidateFeedbackReasonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reason_code: str
    reason_text: str
    evidence_type: Optional[str] = None
    evidence_reference: Optional[str] = None


class CandidateFeedbackOut(BaseModel):
    """Candidate-facing feedback representation (hides private internal scores & recruiter notes)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
    job_id: uuid.UUID
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    feedback_type: str
    summary: Optional[str] = None
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    recommendation: Optional[str] = None
    content: Optional[str] = None  # Maps to final_content or draft_content
    sent_at: Optional[datetime] = None


class CandidateFeedbackRecruiterOut(BaseModel):
    """Recruiter-facing detailed feedback review representation."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
    candidate_id: uuid.UUID
    candidate_name: Optional[str] = None
    candidate_code: Optional[str] = None
    job_id: uuid.UUID
    job_title: Optional[str] = None
    feedback_type: str
    feedback_status: str
    ai_generated: bool
    recruiter_approved: bool
    summary: Optional[str] = None
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    reason: Optional[str] = None
    recommendation: Optional[str] = None
    draft_content: Optional[str] = None
    final_content: Optional[str] = None
    reasons: List[CandidateFeedbackReasonOut] = Field(default_factory=list)
    generated_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None


class CandidateFeedbackUpdate(BaseModel):
    """Recruiter edit payload for feedback."""
    final_content: Optional[str] = Field(None, description="Edited final text content to be sent")
    feedback_status: Optional[str] = Field(None, description="APPROVED, DRAFT, SENT, or CANCELLED")


class FeedbackAIResponse(BaseModel):
    """Strict JSON schema required for LLM feedback generation validation."""
    summary: str = Field(..., description="Respectful overview statement summarizing application review")
    strengths: List[str] = Field(default_factory=list, description="Verified candidate strengths matching job requirements")
    areas_for_improvement: List[str] = Field(default_factory=list, description="Top 2 to 5 specific missing job requirements or gaps")
    reason: str = Field(..., description="Primary job-relevant reason for non-selection")
    encouragement: str = Field(..., description="Encouraging recommendation for future applications")
    tone: str = Field(default="professional", description="Tone of output e.g. professional, encouraging")
    confidence: float = Field(default=0.9, description="Confidence score between 0 and 1")


class BulkFeedbackRequest(BaseModel):
    application_ids: List[uuid.UUID] = Field(..., min_length=1, description="List of rejected application IDs")
    regeneration_prompt: Optional[str] = Field(None, description="Optional custom direction for generation")
    auto_approve: bool = Field(False, description="Whether to automatically approve and send generated feedback")


class BulkFeedbackStatusOut(BaseModel):
    job_id: Optional[uuid.UUID] = None
    total_requested: int
    completed: int
    pending: int
    failed: int
    status: str  # processing, completed, failed
    results: List[Dict[str, Any]] = Field(default_factory=list)
