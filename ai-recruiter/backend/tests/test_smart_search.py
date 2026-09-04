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


def test_smart_search_filters_only_applied_candidates(db_session):
    import uuid
    from app.models.user import User, UserRole
    from app.models.candidate import CandidateProfile
    from app.models.job import Job
    from app.models.application import Application
    from app.services.candidate_search_service import search_and_rank_candidates

    # Create dummy users & profiles
    u_recruiter = User(email=f"recruiter_{uuid.uuid4()}@test.com", password_hash="hash", name="Recruiter", role=UserRole.recruiter)
    u_cand1 = User(email=f"cand1_{uuid.uuid4()}@test.com", password_hash="hash", name="Applied Candidate 1", role=UserRole.candidate)
    u_cand2 = User(email=f"cand2_{uuid.uuid4()}@test.com", password_hash="hash", name="Unapplied Candidate 2", role=UserRole.candidate)
    
    db_session.add_all([u_recruiter, u_cand1, u_cand2])
    db_session.commit()

    cp1 = CandidateProfile(user_id=u_cand1.id, headline="Python Developer", experience_years=3.0)
    cp2 = CandidateProfile(user_id=u_cand2.id, headline="Python Developer", experience_years=3.0)
    db_session.add_all([cp1, cp2])
    db_session.commit()

    job1 = Job(recruiter_id=u_recruiter.id, title="Python Lead", description="Python job", location="Remote", experience_required=2.0)
    db_session.add(job1)
    db_session.commit()

    # Candidate 1 applies to Job 1, Candidate 2 does NOT apply to any job
    app1 = Application(candidate_id=cp1.id, job_id=job1.id, match_score=85.0)
    db_session.add(app1)
    db_session.commit()

    # 1. Search all jobs (job_id = None): only Candidate 1 (who applied) should be returned
    res_all = search_and_rank_candidates(db=db_session, job_id=None)
    returned_ids = [r["candidate_id"] for r in res_all["results"]]
    assert str(cp1.id) in returned_ids
    assert str(cp2.id) not in returned_ids

    # 2. Search specific job (job_id = job1.id): only Candidate 1 (who applied for job1) should be returned
    res_job1 = search_and_rank_candidates(db=db_session, job_id=str(job1.id))
    returned_job1_ids = [r["candidate_id"] for r in res_job1["results"]]
    assert str(cp1.id) in returned_job1_ids
    assert str(cp2.id) not in returned_job1_ids

