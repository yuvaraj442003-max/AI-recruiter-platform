"""
interview_scorecard.py — API Router for AI Executive Candidate Scorecard & Interview Intelligence.

Provides REST endpoints for retrieving scorecards, triggering score recalculation,
and saving recruiter human-in-the-loop decision overrides.
"""
import json
import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.schemas.interview_scorecard import (
    InterviewScorecardOut,
    RecruiterDecisionUpdate,
)
from app.services.interview_intelligence_service import (
    generate_or_get_scorecard,
    update_recruiter_decision,
    get_scorecard_by_interview_id,
)

logger = logging.getLogger("ai_recruiter.routers.interview_scorecard")

router = APIRouter(prefix="", tags=["Interview Scorecard & Intelligence"])


@router.get("/interviews/{interview_id}/scorecard", response_model=InterviewScorecardOut)
def get_interview_scorecard(
    interview_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get or generate the AI Executive Candidate Scorecard for a completed interview.
    Contains category scores, clickable key moments, chapters, and question evaluations.
    """
    scorecard = generate_or_get_scorecard(db, interview_id, force_regenerate=False)
    return _format_scorecard_response(scorecard)


@router.post("/interviews/{interview_id}/scorecard/regenerate", response_model=InterviewScorecardOut)
def regenerate_interview_scorecard(
    interview_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Force re-analysis and re-generation of the candidate executive scorecard."""
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters or admins can trigger scorecard regeneration.")

    scorecard = generate_or_get_scorecard(db, interview_id, force_regenerate=True)
    return _format_scorecard_response(scorecard)


@router.post("/scorecards/{scorecard_id}/recruiter-decision", response_model=InterviewScorecardOut)
def save_recruiter_decision_endpoint(
    scorecard_id: uuid.UUID,
    body: RecruiterDecisionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Save recruiter decision override (Strong Candidate, Shortlist, Hold, Reject) and notes.
    Enforces human-in-the-loop audit control.
    """
    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        raise HTTPException(status_code=403, detail="Only recruiters or admins can save candidate decisions.")

    scorecard = update_recruiter_decision(
        db=db,
        scorecard_id=scorecard_id,
        recruiter_user_id=current_user.id,
        decision=body.decision,
        notes=body.notes,
    )
    return _format_scorecard_response(scorecard)


def _format_scorecard_response(scorecard) -> dict:
    """Helper to convert database model to response dict with JSON parsed lists."""
    candidate_name = None
    job_title = None
    if scorecard.interview:
        if scorecard.interview.candidate and scorecard.interview.candidate.user:
            candidate_name = scorecard.interview.candidate.user.name
        if scorecard.interview.job:
            job_title = scorecard.interview.job.title

    strengths = json.loads(scorecard.strengths_json) if scorecard.strengths_json else []
    weaknesses = json.loads(scorecard.weaknesses_json) if scorecard.weaknesses_json else []

    rec_val = scorecard.recommendation.value if hasattr(scorecard.recommendation, "value") else str(scorecard.recommendation)

    return {
        "id": scorecard.id,
        "interview_id": scorecard.interview_id,
        "candidate_id": scorecard.candidate_id,
        "job_id": scorecard.job_id,
        "candidate_name": candidate_name,
        "job_title": job_title,
        "overall_score": scorecard.overall_score,
        "recommendation": rec_val,
        "executive_summary": scorecard.executive_summary,
        "confidence": scorecard.confidence,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recruiter_decision": scorecard.recruiter_decision,
        "recruiter_notes": scorecard.recruiter_notes,
        "reviewed_at": scorecard.reviewed_at,
        "categories": [
            {
                "id": c.id,
                "category": c.category,
                "score": c.score,
                "confidence": c.confidence,
                "weight": c.weight,
                "evidence_summary": c.evidence_summary,
            }
            for c in scorecard.categories
        ],
        "key_moments": [
            {
                "id": m.id,
                "timestamp_start": m.timestamp_start,
                "timestamp_end": m.timestamp_end,
                "title": m.title,
                "category": m.category,
                "importance": m.importance.value if hasattr(m.importance, "value") else str(m.importance),
                "summary": m.summary,
                "transcript_reference": m.transcript_reference,
                "confidence": m.confidence,
            }
            for m in scorecard.key_moments
        ],
        "chapters": [
            {
                "id": ch.id,
                "title": ch.title,
                "timestamp_start": ch.timestamp_start,
                "timestamp_end": ch.timestamp_end,
                "summary": ch.summary,
                "sequence": ch.sequence,
            }
            for ch in scorecard.chapters
        ],
        "question_evaluations": [
            {
                "id": qe.id,
                "question_id": qe.question_id,
                "question_text": qe.question_text,
                "candidate_answer": qe.candidate_answer,
                "technical_score": qe.technical_score,
                "accuracy_score": qe.accuracy_score,
                "completeness_score": qe.completeness_score,
                "clarity_score": qe.clarity_score,
                "relevance_score": qe.relevance_score,
                "overall_score": qe.overall_score,
                "evaluation_summary": qe.evaluation_summary,
                "timestamp_start": qe.timestamp_start,
                "timestamp_end": qe.timestamp_end,
            }
            for qe in scorecard.question_evaluations
        ],
        "created_at": scorecard.created_at,
    }
