"""
test_candidate_comparison.py — Integration tests for Candidate Comparison and AI Recommendation endpoints.
"""
from app.services.candidate_comparison_service import RECOMMENDATION_WEIGHTS


def test_recommendation_weights_sum_to_one():
    total_weight = sum(RECOMMENDATION_WEIGHTS.values())
    assert abs(total_weight - 1.0) < 1e-6


def test_candidate_comparison_validation(client):
    # Test invalid count (< 2 candidates) without token
    res = client.post(
        "/api/v1/candidates/compare",
        json={"job_id": "00000000-0000-0000-0000-000000000001", "candidate_ids": ["00000000-0000-0000-0000-000000000002"]}
    )
    assert res.status_code in (401, 422, 400)
