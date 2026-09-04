"""
test_password_reset_and_verification.py — Comprehensive tests covering all 8 required email verification & password reset test cases.
"""
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User, UserRole
from app.core.security import verify_password, hash_password

client = TestClient(app)


# TEST 1: Candidate registration with a valid Gmail address
@patch("app.services.email_service._send_smtp_email", return_value=True)
def test_1_candidate_registration_valid_gmail(mock_send, db_session: Session):
    email = f"cand_test_{uuid.uuid4().hex[:6]}@gmail.com"
    res = client.post("/api/v1/auth/register", json={
        "name": "Gmail Candidate",
        "email": email,
        "password": "Password123!",
        "role": "candidate"
    })
    assert res.status_code == 201
    assert "verification email has been sent" in res.json()["message"]

    # Verify user token in DB and mock email dispatch
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.is_email_verified is False
    assert user.verification_token is not None
    assert user.verification_token_expires_at is not None
    assert mock_send.called


# TEST 2: Recruiter registration with a valid company email
@patch("app.services.email_service._send_smtp_email", return_value=True)
def test_2_recruiter_registration_valid_company_email(mock_send, db_session: Session):
    email = f"recruiter_{uuid.uuid4().hex[:6]}@vgensoft.com"
    res = client.post("/api/v1/auth/register", json={
        "name": "Recruiter User",
        "email": email,
        "password": "Password123!",
        "role": "recruiter",
        "company_name": "VGen Soft Tech",
        "company_website": "https://vgensoft.com"
    })
    assert res.status_code == 201
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.role == UserRole.recruiter
    assert user.verification_token is not None
    assert mock_send.called


# TEST 3: Register using an already existing email -> Registration must be blocked
@patch("app.services.email_service._send_smtp_email", return_value=True)
def test_3_register_existing_email_blocked(mock_send, db_session: Session):
    email = f"dup_{uuid.uuid4().hex[:6]}@gmail.com"
    # First registration
    client.post("/api/v1/auth/register", json={
        "name": "First Candidate",
        "email": email,
        "password": "Password123!",
        "role": "candidate"
    })

    # Duplicate registration attempt
    res = client.post("/api/v1/auth/register", json={
        "name": "Duplicate Candidate",
        "email": email,
        "password": "Password456!",
        "role": "candidate"
    })
    assert res.status_code == 409
    assert "already registered" in res.json()["message"].lower()


# TEST 4: Forgot password using a registered email
@patch("app.services.email_service._send_smtp_email", return_value=True)
def test_4_forgot_password_registered_email(mock_send, db_session: Session):
    email = f"forgot_{uuid.uuid4().hex[:6]}@vgensoft.com"
    user = User(
        name="Forgot Recruiter",
        email=email,
        password_hash=hash_password("OldPassword123!"),
        role=UserRole.recruiter,
        is_active=True,
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()

    res = client.post("/api/v1/auth/forgot-password", json={"email": email})
    assert res.status_code == 200
    assert "instructions have been sent" in res.json()["message"].lower()

    db_session.refresh(user)
    assert user.reset_token is not None
    assert user.reset_token_expires_at is not None
    # Verify reset token is NOT exposed in response payload data
    assert "reset_token" not in res.json().get("data", {})
    assert mock_send.called


# TEST 5: Forgot password using an unregistered email -> Return safe generic response
def test_5_forgot_password_unregistered_email_generic_response():
    email = f"unregistered_{uuid.uuid4().hex[:6]}@vgensoft.com"
    res = client.post("/api/v1/auth/forgot-password", json={"email": email})
    assert res.status_code == 200
    assert "instructions have been sent" in res.json()["message"].lower()
    # Does not expose whether email exists or not
    assert res.json()["data"] == {}


# TEST 6: Expired verification token -> Verification must fail
def test_6_expired_verification_token(db_session: Session):
    email = f"expired_verify_{uuid.uuid4().hex[:6]}@gmail.com"
    past_time = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=1)
    user = User(
        name="Expired User",
        email=email,
        password_hash=hash_password("Password123!"),
        role=UserRole.candidate,
        is_active=True,
        is_email_verified=False,
        verification_token="expired_token_12345",
        verification_token_expires_at=past_time
    )
    db_session.add(user)
    db_session.commit()

    res = client.get("/api/v1/auth/verify-email?token=expired_token_12345")
    assert res.status_code == 401
    assert "expired" in res.json()["message"].lower()


# TEST 7: Expired reset token -> Password reset must fail
def test_7_expired_reset_token(db_session: Session):
    email = f"expired_reset_{uuid.uuid4().hex[:6]}@vgensoft.com"
    past_time = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=10)
    user = User(
        name="Expired Reset User",
        email=email,
        password_hash=hash_password("OldPassword123!"),
        role=UserRole.recruiter,
        is_active=True,
        is_email_verified=True,
        reset_token="expired_reset_token_999",
        reset_token_expires_at=past_time
    )
    db_session.add(user)
    db_session.commit()

    res = client.post("/api/v1/auth/reset-password", json={
        "token": "expired_reset_token_999",
        "new_password": "NewPassword456!"
    })
    assert res.status_code == 401
    assert "expired" in res.json()["message"].lower()


# TEST 8: Reuse an already-used reset/verification token -> Must be rejected
def test_8_token_reuse_rejected(db_session: Session):
    # 1. Register & verify user
    email = f"reuse_{uuid.uuid4().hex[:6]}@gmail.com"
    user = User(
        name="Token Reuse User",
        email=email,
        password_hash=hash_password("Password123!"),
        role=UserRole.candidate,
        is_active=True,
        is_email_verified=False,
        verification_token="valid_once_token",
        verification_token_expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=24)
    )
    db_session.add(user)
    db_session.commit()

    # First verification attempt -> SUCCEEDS
    res1 = client.get("/api/v1/auth/verify-email?token=valid_once_token")
    assert res1.status_code == 200

    # Second verification attempt with same token -> REJECTED
    res2 = client.get("/api/v1/auth/verify-email?token=valid_once_token")
    assert res2.status_code == 401
    assert "invalid or expired" in res2.json()["message"].lower()
