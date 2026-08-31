"""
test_smart_search.py — Unit & Integration tests for Smart Candidate Search, Query Parsing & Ranking.
"""
from app.services.candidate_search_service import CANDIDATE_SEARCH_WEIGHTS, search_and_rank_candidates
from app.services.search_query_parser import parse_search_query


def test_ranking_weights_sum_to_one():
    total = sum(CANDIDATE_SEARCH_WEIGHTS.values())
    assert abs(total - 1.0) < 1e-6


def test_parse_search_query_complex():
    query = "Python + FastAPI + PostgreSQL, 3+ years experience, Chennai, ATS > 75"
    parsed = parse_search_query(query)

    assert "Python" in parsed["skills"] or "python" in [s.lower() for s in parsed["skills"]]
    assert parsed["minimum_experience"] == 3.0
    assert parsed["location"] == "Chennai"
    assert parsed["minimum_ats_score"] == 75.0


def test_parse_search_query_experience_range():
    query = "2 to 5 years experience Bangalore"
    parsed = parse_search_query(query)

    assert parsed["minimum_experience"] == 2.0
    assert parsed["maximum_experience"] == 5.0
    assert parsed["location"] == "Bangalore"


def test_smart_search_api_validation(client):
    # Search candidates without token should return 401
    res = client.post(
        "/api/v1/candidates/smart-search",
        json={"query": "Python 3+ years"}
    )
    assert res.status_code in (401, 422, 400)
