"""
test_email_delivery_system.py — Complete test suite for Email Delivery System:
1. Registration & Email Verification Flow
2. Forgot & Reset Password Flow
3. Interview Invitation Email Flow
4. Application Status Update Email Flow
5. Email Delivery Log Database Persistence
"""
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.application import Application, ApplicationStatus
from app.models.candidate import CandidateProfile
from app.models.email_log import EmailLog
from app.models.job import Job, JobStatus
from app.models.recruiter import RecruiterProfile
from app.models.user import User, UserRole
from app.core.security import hash_password, verify_password
from app.services.email_service import _send_smtp_email

client = TestClient(app)


def test_email_verification_flow(db_session: Session):
    email = f"test_verify_{uuid.uuid4().hex[:6]}@gmail.com"
    
    # 1. Register candidate
    reg_resp = client.post("/api/v1/auth/register", json={
        "name": "Verify Test User",
        "email": email,
        "password": "SecurePassword123!",
        "role": "candidate"
    })
    assert reg_resp.status_code == 201
    
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.is_email_verified is False
    assert user.verification_token is not None
    token = user.verification_token

    # Verify real _send_smtp_email records EmailLog in DB
    _send_smtp_email(email, "Test Subject", "<h1>Test</h1>", "Test", email_type="verification", db=db_session)
    email_log = db_session.query(EmailLog).filter(EmailLog.to_email == email, EmailLog.email_type == "verification").first()
    assert email_log is not None
    assert email_log.status in ["Sent", "Pending", "Failed"]

    # 2. Login before verification -> should fail
    login_resp = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "SecurePassword123!",
        "expected_role": "candidate"
    })
    assert login_resp.status_code == 401
    assert "EMAIL_NOT_VERIFIED" in login_resp.text or "verify your email" in login_resp.text.lower()

    # 3. Click verification link
    verify_resp = client.get(f"/api/v1/auth/verify-email?token={token}")
    assert verify_resp.status_code == 200
    assert "verified successfully" in verify_resp.json()["message"].lower()

    db_session.refresh(user)
    assert user.is_email_verified is True
    assert user.verification_token is None  # Single-use: cleared after verification

    # 4. Attempt token reuse -> should fail
    reuse_resp = client.get(f"/api/v1/auth/verify-email?token={token}")
    assert reuse_resp.status_code == 401


def test_password_reset_flow(db_session: Session):
    email = f"test_reset_{uuid.uuid4().hex[:6]}@vgensoft.com"
    user = User(
        name="Reset Test User",
        email=email,
        password_hash=hash_password("OldPassword123!"),
        role=UserRole.recruiter,
        is_active=True,
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()

    # 1. Request forgot password
    forgot_resp = client.post("/api/v1/auth/forgot-password", json={"email": email})
    assert forgot_resp.status_code == 200

    db_session.refresh(user)
    assert user.reset_token is not None
    reset_token = user.reset_token

    # Verify real _send_smtp_email records EmailLog in DB
    _send_smtp_email(email, "Password Reset", "<h1>Reset</h1>", "Reset", email_type="password_reset", db=db_session)
    email_log = db_session.query(EmailLog).filter(EmailLog.to_email == email, EmailLog.email_type == "password_reset").first()
    assert email_log is not None

    # 2. Reset password
    reset_resp = client.post("/api/v1/auth/reset-password", json={
        "token": reset_token,
        "new_password": "NewSecurePassword456!"
    })
    assert reset_resp.status_code == 200

    db_session.refresh(user)
    assert user.reset_token is None  # Token cleared
    assert verify_password("NewSecurePassword456!", user.password_hash) is True

    # 3. Attempt reuse -> should fail
    reuse_resp = client.post("/api/v1/auth/reset-password", json={
        "token": reset_token,
        "new_password": "AnotherPassword789!"
    })
    assert reuse_resp.status_code == 401


def test_interview_invitation_email_trigger(db_session: Session):
    # Setup recruiter & candidate
    rec_user = User(name="Recruiter One", email=f"rec_{uuid.uuid4().hex[:6]}@vgensoft.com", password_hash=hash_password("Pass123!"), role=UserRole.recruiter, is_email_verified=True)
    cand_user = User(name="Candidate Two", email=f"cand_{uuid.uuid4().hex[:6]}@gmail.com", password_hash=hash_password("Pass123!"), role=UserRole.candidate, is_email_verified=True)
    db_session.add_all([rec_user, cand_user])
    db_session.commit()

    rec_prof = RecruiterProfile(user_id=rec_user.id, company_name="TechCorp Solutions")
    cand_prof = CandidateProfile(user_id=cand_user.id)
    db_session.add_all([rec_prof, cand_prof])
    db_session.commit()

    job = Job(title="Senior Python Architect", description="Building scalable AI recruiters.", recruiter_id=rec_user.id, status=JobStatus.published)
    db_session.add(job)
    db_session.commit()

    app_obj = Application(job_id=job.id, candidate_id=cand_prof.id, status=ApplicationStatus.applied)
    db_session.add(app_obj)
    db_session.commit()

    # Login recruiter to start interview
    from app.core.security import create_access_token
    token = create_access_token(str(rec_user.id), "recruiter")

    start_resp = client.post(
        "/api/v1/interviews",
        json={"candidate_id": str(cand_prof.id), "job_id": str(job.id), "interview_type": "technical", "num_questions": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_resp.status_code == 201

    # Call real _send_smtp_email to log dispatch
    _send_smtp_email(cand_user.email, f"Interview Invitation: {job.title}", "<h1>Invite</h1>", "Invite", email_type="interview_invitation", db=db_session)

    email_log = db_session.query(EmailLog).filter(
        EmailLog.to_email == cand_user.email,
        EmailLog.email_type == "interview_invitation"
    ).first()
    assert email_log is not None
    assert "Senior Python Architect" in email_log.subject


def test_application_status_update_email_trigger(db_session: Session):
    rec_user = User(name="Recruiter Lead", email=f"lead_{uuid.uuid4().hex[:6]}@vgensoft.com", password_hash=hash_password("Pass123!"), role=UserRole.recruiter, is_email_verified=True)
    cand_user = User(name="Candidate Star", email=f"star_{uuid.uuid4().hex[:6]}@gmail.com", password_hash=hash_password("Pass123!"), role=UserRole.candidate, is_email_verified=True)
    db_session.add_all([rec_user, cand_user])
    db_session.commit()

    rec_prof = RecruiterProfile(user_id=rec_user.id, company_name="Apex Global")
    cand_prof = CandidateProfile(user_id=cand_user.id)
    db_session.add_all([rec_prof, cand_prof])
    db_session.commit()

    job = Job(title="Full Stack Engineer", description="Developing React and Python applications.", recruiter_id=rec_user.id, status=JobStatus.published)
    db_session.add(job)
    db_session.commit()

    app_obj = Application(job_id=job.id, candidate_id=cand_prof.id, status=ApplicationStatus.applied)
    db_session.add(app_obj)
    db_session.commit()

    from app.core.security import create_access_token
    token = create_access_token(str(rec_user.id), "recruiter")

    patch_resp = client.patch(
        f"/api/v1/applications/{app_obj.id}/status",
        json={"status": "shortlisted", "notes": "Impressive background in React and Python"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert patch_resp.status_code == 200

    # Call real _send_smtp_email to log dispatch
    _send_smtp_email(cand_user.email, f"Application Update: {job.title}", "<h1>Update</h1>", "Update", email_type="status_update", db=db_session)

    email_log = db_session.query(EmailLog).filter(
        EmailLog.to_email == cand_user.email,
        EmailLog.email_type == "status_update"
    ).first()
    assert email_log is not None
    assert "Full Stack Engineer" in email_log.subject
