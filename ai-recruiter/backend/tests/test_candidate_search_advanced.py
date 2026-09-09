"""
test_candidate_search_advanced.py — Comprehensive tests for Recruiter Candidate Search, Advanced Filtering,
ATS Thresholding, Job-Specific Matching, Saved Searches, Direct Invitations, and Resume Security.
"""
import uuid
import pytest
from app.models.user import User, UserRole
from app.models.candidate import CandidateProfile, Skill, CandidateSkill
from app.models.job import Job
from app.models.application import Application
from app.models.saved_search import SavedCandidateSearch, CandidateInvitation, CandidateShortlist
from app.services.candidate_search_service import (
    search_and_rank_candidates,
    save_candidate_search,
    get_saved_searches,
    delete_saved_search,
    invite_candidate,
    bulk_invite_candidates,
    shortlist_candidate,
    bulk_shortlist_candidates,
)
from app.core.security import create_access_token


def test_candidate_search_skills_and_or(db_session):
    u_recruiter = User(email=f"rec_{uuid.uuid4()}@test.com", password_hash="hash", name="Recruiter 1", role=UserRole.recruiter)
    u_cand1 = User(email=f"c1_{uuid.uuid4()}@test.com", password_hash="hash", name="Python Dev", role=UserRole.candidate)
    u_cand2 = User(email=f"c2_{uuid.uuid4()}@test.com", password_hash="hash", name="Java Dev", role=UserRole.candidate)

    db_session.add_all([u_recruiter, u_cand1, u_cand2])
    db_session.commit()

    sk_python = Skill(skill_name="Python", category="IT")
    sk_fastapi = Skill(skill_name="FastAPI", category="IT")
    sk_java = Skill(skill_name="Java", category="IT")
    db_session.add_all([sk_python, sk_fastapi, sk_java])
    db_session.commit()

    cp1 = CandidateProfile(user_id=u_cand1.id, headline="Python Developer", experience_years=4.0, location="Chennai")
    cp2 = CandidateProfile(user_id=u_cand2.id, headline="Java Lead", experience_years=7.0, location="Bangalore")
    db_session.add_all([cp1, cp2])
    db_session.commit()

    cs1 = CandidateSkill(candidate_id=cp1.id, skill_id=sk_python.id)
    cs2 = CandidateSkill(candidate_id=cp1.id, skill_id=sk_fastapi.id)
    cs3 = CandidateSkill(candidate_id=cp2.id, skill_id=sk_java.id)
    db_session.add_all([cs1, cs2, cs3])
    db_session.commit()

    # Application for candidates
    j1 = Job(recruiter_id=u_recruiter.id, title="Software Engineer", description="Coding job", experience_required=2.0)
    db_session.add(j1)
    db_session.commit()

    app1 = Application(candidate_id=cp1.id, job_id=j1.id, match_score=88.0)
    app2 = Application(candidate_id=cp2.id, job_id=j1.id, match_score=75.0)
    db_session.add_all([app1, app2])
    db_session.commit()

    # 1. Search with Match All (AND) mode for Python + FastAPI
    res_all = search_and_rank_candidates(
        db=db_session,
        filters={"skills": ["Python", "FastAPI"], "skill_match_mode": "all"},
        recruiter_id=u_recruiter.id
    )
    returned_cand_ids = [r["candidate_id"] for r in res_all["results"]]
    assert str(cp1.id) in returned_cand_ids
    assert str(cp2.id) not in returned_cand_ids

    # 2. Search with Match Any (OR) mode for Python or Java
    res_any = search_and_rank_candidates(
        db=db_session,
        filters={"skills": ["Python", "Java"], "skill_match_mode": "any"},
        recruiter_id=u_recruiter.id
    )
    returned_any_ids = [r["candidate_id"] for r in res_any["results"]]
    assert str(cp1.id) in returned_any_ids
    assert str(cp2.id) in returned_any_ids


def test_candidate_search_experience_and_location(db_session):
    u_rec = User(email=f"rec_{uuid.uuid4()}@test.com", password_hash="hash", name="Recruiter Exp", role=UserRole.recruiter)
    u_c1 = User(email=f"c1_{uuid.uuid4()}@test.com", password_hash="hash", name="Junior Dev", role=UserRole.candidate)
    u_c2 = User(email=f"c2_{uuid.uuid4()}@test.com", password_hash="hash", name="Senior Dev", role=UserRole.candidate)

    db_session.add_all([u_rec, u_c1, u_c2])
    db_session.commit()

    cp1 = CandidateProfile(user_id=u_c1.id, headline="Frontend Dev", experience_years=1.5, location="Chennai, Tamil Nadu")
    cp2 = CandidateProfile(user_id=u_c2.id, headline="Backend Dev", experience_years=5.5, location="Bangalore, Karnataka")
    db_session.add_all([cp1, cp2])
    db_session.commit()

    j1 = Job(recruiter_id=u_rec.id, title="General Developer", description="Dev job", experience_required=1.0)
    db_session.add(j1)
    db_session.commit()

    db_session.add_all([
        Application(candidate_id=cp1.id, job_id=j1.id, match_score=70.0),
        Application(candidate_id=cp2.id, job_id=j1.id, match_score=90.0)
    ])
    db_session.commit()

    # Search Experience >= 3
    res_exp = search_and_rank_candidates(
        db=db_session,
        filters={"minimum_experience": 3.0},
        recruiter_id=u_rec.id
    )
    exp_cand_ids = [r["candidate_id"] for r in res_exp["results"]]
    assert str(cp2.id) in exp_cand_ids
    assert str(cp1.id) not in exp_cand_ids

    # Search Location Partial match "Chennai"
    res_loc = search_and_rank_candidates(
        db=db_session,
        filters={"location": "Chennai"},
        recruiter_id=u_rec.id
    )
    loc_cand_ids = [r["candidate_id"] for r in res_loc["results"]]
    assert str(cp1.id) in loc_cand_ids
    assert str(cp2.id) not in loc_cand_ids


def test_automatic_qualification_threshold(db_session):
    u_rec = User(email=f"rec_{uuid.uuid4()}@test.com", password_hash="hash", name="Recruiter Thresh", role=UserRole.recruiter)
    u_c1 = User(email=f"c1_{uuid.uuid4()}@test.com", password_hash="hash", name="High ATS Candidate", role=UserRole.candidate)
    u_c2 = User(email=f"c2_{uuid.uuid4()}@test.com", password_hash="hash", name="Low ATS Candidate", role=UserRole.candidate)

    db_session.add_all([u_rec, u_c1, u_c2])
    db_session.commit()

    cp1 = CandidateProfile(user_id=u_c1.id, headline="Lead Engineer", experience_years=6.0, profile_score=85)
    cp2 = CandidateProfile(user_id=u_c2.id, headline="Intern Engineer", experience_years=0.5, profile_score=45)
    db_session.add_all([cp1, cp2])
    db_session.commit()

    j1 = Job(recruiter_id=u_rec.id, title="Lead Role", description="Role", experience_required=5.0)
    db_session.add(j1)
    db_session.commit()

    db_session.add_all([
        Application(candidate_id=cp1.id, job_id=j1.id, match_score=85.0),
        Application(candidate_id=cp2.id, job_id=j1.id, match_score=45.0)
    ])
    db_session.commit()

    res = search_and_rank_candidates(
        db=db_session,
        qualification_threshold=60.0,
        recruiter_id=u_rec.id
    )

    item1 = next(r for r in res["results"] if r["candidate_id"] == str(cp1.id))
    item2 = next(r for r in res["results"] if r["candidate_id"] == str(cp2.id))

    assert item1["is_qualified"] is True
    assert item1["qualification_badge"] == "✓ Qualified"

    assert item2["is_qualified"] is False
    assert item2["qualification_badge"] == "Below Threshold"


def test_saved_searches_crud(db_session):
    u_rec = User(email=f"rec_{uuid.uuid4()}@test.com", password_hash="hash", name="Saved Recruiter", role=UserRole.recruiter)
    db_session.add(u_rec)
    db_session.commit()

    saved = save_candidate_search(
        db=db_session,
        recruiter_id=u_rec.id,
        name="Python Experts",
        query="Python 3+ years",
        filters={"skills": ["Python"], "minimum_experience": 3.0}
    )
    assert saved.id is not None
    assert saved.name == "Python Experts"

    searches = get_saved_searches(db_session, u_rec.id)
    assert len(searches) >= 1
    assert searches[0].name == "Python Experts"

    del_res = delete_saved_search(db_session, u_rec.id, saved.id)
    assert del_res is True
    remaining = get_saved_searches(db_session, u_rec.id)
    assert len(remaining) == 0


def test_direct_invitations_and_shortlists(db_session):
    u_rec = User(email=f"rec_{uuid.uuid4()}@test.com", password_hash="hash", name="Inviter Recruiter", role=UserRole.recruiter)
    u_cand = User(email=f"cand_{uuid.uuid4()}@test.com", password_hash="hash", name="Target Candidate", role=UserRole.candidate)
    db_session.add_all([u_rec, u_cand])
    db_session.commit()

    cp = CandidateProfile(user_id=u_cand.id, headline="Full Stack Engineer")
    j = Job(recruiter_id=u_rec.id, title="Full Stack Opening", description="Opening")
    db_session.add_all([cp, j])
    db_session.commit()

    inv = invite_candidate(db_session, u_rec.id, cp.id, j.id, "Please apply!")
    assert inv.id is not None
    assert inv.status == "invited"

    short = shortlist_candidate(db_session, u_rec.id, cp.id, j.id, "Strong fit")
    assert short.id is not None

    bulk_inv_res = bulk_invite_candidates(db_session, u_rec.id, [str(cp.id)], j.id, "Bulk invite")
    assert bulk_inv_res["invited_count"] >= 1

    bulk_short_res = bulk_shortlist_candidates(db_session, u_rec.id, [str(cp.id)], j.id)
    assert bulk_short_res["shortlisted_count"] >= 1


def test_candidate_role_forbidden_search_api(client, db_session):
    u_cand = User(email=f"cand_user_{uuid.uuid4()}@test.com", password_hash="hash", name="Candidate User", role=UserRole.candidate)
    db_session.add(u_cand)
    db_session.commit()

    token = create_access_token(str(u_cand.id), u_cand.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post(
        "/api/v1/candidates/smart-search",
        json={"query": "Python"},
        headers=headers
    )
    assert res.status_code == 403
