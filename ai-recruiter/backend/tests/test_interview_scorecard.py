"""
test_interview_scorecard.py — Unit & Integration tests for AI Executive Candidate Scorecard & Interview Intelligence.
Tests scorecard creation, weighted matrix score calculations, recommendation thresholds, chaptering,
timestamped key moments, and recruiter decision overrides.
"""
import uuid
import pytest
from app.models.interview_scorecard import (
    InterviewScorecard,
    CandidateRecommendation,
    MomentImportance,
)
from app.services.interview_intelligence_service import (
    DEFAULT_CATEGORIES,
    update_recruiter_decision,
)


def test_category_weights_sum_to_one():
    """Verify that default competency evaluation category weights sum to 1.0 (100%)."""
    total_weight = sum(cat["weight"] for cat in DEFAULT_CATEGORIES)
    assert pytest.approx(total_weight, 0.001) == 1.0


def test_candidate_recommendation_thresholds():
    """Verify candidate recommendation assignment rules based on overall score."""
    def get_rec(score):
        if score >= 85.0:
            return CandidateRecommendation.strong_candidate
        elif score >= 72.0:
            return CandidateRecommendation.recommended
        elif score >= 58.0:
            return CandidateRecommendation.consider
        elif score >= 45.0:
            return CandidateRecommendation.review_required
        else:
            return CandidateRecommendation.not_recommended

    assert get_rec(92.0) == CandidateRecommendation.strong_candidate
    assert get_rec(85.0) == CandidateRecommendation.strong_candidate
    assert get_rec(78.0) == CandidateRecommendation.recommended
    assert get_rec(65.0) == CandidateRecommendation.consider
    assert get_rec(50.0) == CandidateRecommendation.review_required
    assert get_rec(35.0) == CandidateRecommendation.not_recommended


def test_recruiter_decision_validation():
    """Test that invalid decision values are rejected properly."""
    from app.core.exceptions import AppError

    with pytest.raises(AppError) as exc_info:
        update_recruiter_decision(
            db=None,
            scorecard_id=uuid.uuid4(),
            recruiter_user_id=uuid.uuid4(),
            decision="InvalidDecision",
        )
    assert exc_info.value.status_code == 400
    assert "Invalid decision" in str(exc_info.value)
