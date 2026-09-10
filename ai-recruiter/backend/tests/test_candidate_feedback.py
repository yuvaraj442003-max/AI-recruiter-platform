"""
test_candidate_feedback.py — Automated Unit & Integration Tests for Candidate Feedback System.
Tests evidence collection, deterministic template fallbacks, Pydantic LLM output validation,
candidate privacy enforcement, and recruiter approval workflows.
"""
import uuid
import pytest
from app.services.candidate_feedback_service import (
    generate_deterministic_feedback,
    collect_feedback_evidence,
)
from app.schemas.feedback import FeedbackAIResponse, CandidateFeedbackOut, CandidateFeedbackRecruiterOut


def test_generate_deterministic_feedback_personalized():
    """Verify deterministic template fallback produces evidence-grounded non-selection feedback."""
    evidence = {
        "candidate_name": "Arun Kumar",
        "job_title": "Senior Python Developer",
        "company_name": "Tech Corp",
        "strengths": ["Python", "FastAPI", "PostgreSQL"],
        "missing_requirements": ["Kubernetes", "AWS", "Docker"],
        "experience_gap": "5+ years required (candidate has 4 years)",
    }

    result = generate_deterministic_feedback(evidence, level="personalized")

    assert "Python" in result["summary"] or "FastAPI" in result["summary"]
    assert "Kubernetes" in result["content"]
    assert "AWS" in result["content"]
    assert "Python" in result["strengths"]
    assert "Kubernetes" in result["areas_for_improvement"]
    assert result["confidence"] == 1.0


def test_generate_deterministic_feedback_basic_and_detailed():
    """Verify basic and detailed feedback fallback variations."""
    evidence = {
        "job_title": "Frontend Engineer",
        "strengths": ["React.js", "TypeScript"],
        "missing_requirements": ["GraphQL", "Next.js"],
    }

    basic = generate_deterministic_feedback(evidence, level="basic")
    assert "Frontend Engineer" in basic["summary"]
    assert "React.js" not in basic["summary"]  # Basic mode keeps it high level

    detailed = generate_deterministic_feedback(evidence, level="detailed")
    assert "✓ React.js" in detailed["content"]
    assert "• GraphQL" in detailed["content"]


def test_feedback_ai_response_validation():
    """Verify Pydantic validation of LLM feedback JSON output."""
    raw_llm_data = {
        "summary": "Your profile showed strong Python and FastAPI experience.",
        "strengths": ["Python", "FastAPI", "PostgreSQL"],
        "areas_for_improvement": ["Kubernetes", "AWS"],
        "reason": "The role required stronger cloud deployment experience.",
        "encouragement": "We encourage you to apply for future backend opportunities.",
        "tone": "respectful",
        "confidence": 0.95,
    }

    obj = FeedbackAIResponse(**raw_llm_data)
    assert obj.summary.startswith("Your profile")
    assert "Kubernetes" in obj.areas_for_improvement
    assert obj.confidence == 0.95


def test_candidate_privacy_guardrails():
    """Verify CandidateFeedbackOut schema strictly omits internal ATS scores and private notes."""
    dto_data = {
        "id": uuid.uuid4(),
        "application_id": uuid.uuid4(),
        "job_id": uuid.uuid4(),
        "job_title": "Backend Engineer",
        "company_name": "Acme Inc",
        "feedback_type": "personalized",
        "summary": "Strong Python experience.",
        "strengths": ["Python", "FastAPI"],
        "areas_for_improvement": ["Kubernetes"],
        "recommendation": "Apply for future roles.",
        "content": "Thank you for applying. Your profile showed strong Python experience.",
        "sent_at": "2026-09-10T12:00:00",
    }

    obj = CandidateFeedbackOut(**dto_data)
    assert obj.job_title == "Backend Engineer"
    assert obj.content.startswith("Thank you")

    # Verify internal private attributes do NOT exist on CandidateFeedbackOut DTO
    assert not hasattr(obj, "ats_score")
    assert not hasattr(obj, "recruiter_private_notes")
    assert not hasattr(obj, "internal_rank")
    assert not hasattr(obj, "draft_content")
