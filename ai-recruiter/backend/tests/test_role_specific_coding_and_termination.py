"""
test_role_specific_coding_and_termination.py — Tests for role-specific assessment provisioning,
60-minute duration enforcement, and immediate tab-switch disqualification/termination.
"""
import pytest
from app.services.assessment_bank_service import (
    classify_job_role,
    get_or_create_assessment_for_job,
    FRONTEND_CODING_QUESTIONS,
    AI_CODING_QUESTIONS
)
from app.models.job import Job
from app.models.application import Application, ApplicationStatus
from app.models.user import User, UserRole
from app.models.candidate import CandidateProfile
from app.models.coding import CandidateCodingAttempt, CodingAssessment
from app.core.security import create_access_token


def test_classify_job_role_frontend_and_ai():
    """Verify role classifier detects Frontend Developer and AI Developer accurately."""
    assert classify_job_role("Frontend Developer", ["React", "CSS", "HTML"]) == "frontend_developer"
    assert classify_job_role("Senior React Engineer", ["TypeScript", "Next.js", "Redux"]) == "frontend_developer"
    assert classify_job_role("AI Developer", ["PyTorch", "Python", "LLMs"]) == "ai_developer"
    assert classify_job_role("Machine Learning Specialist", ["TensorFlow", "Scikit-Learn"]) == "ai_developer"
    assert classify_job_role("Backend Software Engineer", ["Golang", "Docker"]) == "developer"
    assert classify_job_role("Talent Acquisition Recruiter", ["Sourcing", "HR"]) == "recruiter"


def test_role_specific_assessment_creation_and_60m_duration(db_session):
    """Verify frontend and AI assessments are created with 60 minutes and distinct role questions."""
    recruiter = User(
        email="recruiter_test_fe_ai@example.com",
        password_hash="hashedpassword123",
        name="Test Recruiter",
        role=UserRole.recruiter
    )
    db_session.add(recruiter)
    db_session.commit()
    db_session.refresh(recruiter)

    # 1. Frontend Job
    fe_job = Job(
        recruiter_id=recruiter.id,
        title="Frontend Web Specialist",
        description="Build responsive and accessible UI components",
        experience_required=3.0
    )
    db_session.add(fe_job)
    db_session.commit()
    db_session.refresh(fe_job)

    fe_assessment = get_or_create_assessment_for_job(db_session, fe_job.id)
    assert fe_assessment.duration_minutes == 60
    assert "Frontend" in fe_assessment.title
    assert len(fe_assessment.questions) == 30
    # Confirm frontend question titles match frontend challenges
    fe_titles = [aq.question.title for aq in fe_assessment.questions]
    assert any("Virtual DOM" in t for t in fe_titles)
    assert any("Debounce" in t for t in fe_titles)

    # 2. AI Job
    ai_job = Job(
        recruiter_id=recruiter.id,
        title="AI Research Developer",
        description="Develop deep learning models and NLP pipelines",
        experience_required=3.0
    )
    db_session.add(ai_job)
    db_session.commit()
    db_session.refresh(ai_job)

    ai_assessment = get_or_create_assessment_for_job(db_session, ai_job.id)
    assert ai_assessment.duration_minutes == 60
    assert "AI" in ai_assessment.title
    assert len(ai_assessment.questions) == 30
    # Confirm AI question titles match AI challenges
    ai_titles = [aq.question.title for aq in ai_assessment.questions]
    assert any("Cosine Similarity" in t for t in ai_titles)
    assert any("Precision" in t for t in ai_titles)

    # 3. Ensure frontend coding questions and AI coding questions are distinct (last 5 challenges)
    assert set(fe_titles[25:]).isdisjoint(set(ai_titles[25:]))


def test_tab_switch_termination_flow(client, db_session):
    """Verify immediate termination upon tab switch: attempt finalized to 0%, candidate rejected."""
    recruiter = User(
        email="recruiter_term_test@example.com",
        password_hash="hashedpassword123",
        name="Test Recruiter 2",
        role=UserRole.recruiter
    )
    db_session.add(recruiter)
    db_session.commit()
    db_session.refresh(recruiter)

    # Create candidate user & profile
    candidate = User(
        email="tabswitch_candidate@example.com",
        password_hash="hashedpassword123",
        name="TabSwitch Candidate",
        role=UserRole.candidate
    )
    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    cand_profile = CandidateProfile(
        user_id=candidate.id,
        phone="555-0199"
    )
    db_session.add(cand_profile)
    db_session.commit()

    # Create job & application
    job = Job(
        recruiter_id=recruiter.id,
        title="Frontend UI Architect",
        description="Frontend application development",
        experience_required=4.0
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    app = Application(
        job_id=job.id,
        candidate_id=cand_profile.id,
        status=ApplicationStatus.interview
    )
    db_session.add(app)
    db_session.commit()
    db_session.refresh(app)

    assessment = get_or_create_assessment_for_job(db_session, job.id)
    token = create_access_token(str(candidate.id), role=candidate.role)
    headers = {"Authorization": f"Bearer {token}"}

    # Start assessment attempt
    start_resp = client.post(f"/api/v1/coding/candidate/assessments/{assessment.id}/start", headers=headers)
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    assert start_data["success"] is True
    attempt_id = start_data["data"]["id"]

    # Candidate triggers tab switch -> call terminate endpoint
    term_resp = client.post(
        f"/api/v1/coding/candidate/attempts/{attempt_id}/terminate?reason=TAB_SWITCH",
        headers=headers
    )
    assert term_resp.status_code == 200
    term_data = term_resp.json()
    assert term_data["success"] is True
    assert term_data["data"]["status"] == "Terminated"
    assert term_data["data"]["score"] == 0.0
    assert term_data["data"]["passed"] is False

    # Check attempt in DB
    db_attempt = db_session.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.id == attempt_id).first()
    assert db_attempt.status == "Terminated"
    assert db_attempt.score == 0.0
    assert db_attempt.passed is False

    # Verify application status was set to rejected
    db_app = db_session.query(Application).filter(Application.id == app.id).first()
    assert db_app.status == ApplicationStatus.rejected

    # Attempting to start again should return Terminated and 0 remaining seconds
    re_start_resp = client.post(f"/api/v1/coding/candidate/assessments/{assessment.id}/start", headers=headers)
    assert re_start_resp.status_code == 200
    assert re_start_resp.json()["data"]["status"] == "Terminated"
    assert re_start_resp.json()["data"]["remaining_seconds"] == 0

    # Attempting to submit should be rejected with 403 Forbidden or 400 Bad Request
    sub_resp = client.post(
        f"/api/v1/coding/candidate/attempts/{attempt_id}/submit",
        json=[],
        headers=headers
    )
    assert sub_resp.status_code in (400, 403)
    sub_data = sub_resp.json()
    msg = sub_data.get("detail") or sub_data.get("message") or ""
    assert "terminated" in msg.lower()
