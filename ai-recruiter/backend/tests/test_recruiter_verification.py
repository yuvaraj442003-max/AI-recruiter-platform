"""
test_recruiter_verification.py — Tests for Recruiter Instant Registration & Approval workflow.
"""


def test_recruiter_registration_instant_approval(client):
    """All recruiters registering get instant approval and can log in immediately."""
    res = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Jane Corp",
            "email": "jane@acmetech.com",
            "password": "SecurePass123",
            "role": "recruiter",
        },
    )
    assert res.status_code == 201, res.text
    data = res.json()["data"]
    assert data["user"]["verification_status"] == "approved"
    assert "access_token" in data

    # Immediate login succeeds
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "jane@acmetech.com", "password": "SecurePass123"},
    )
    assert login_res.status_code == 200
    assert login_res.json()["data"]["user"]["verification_status"] == "approved"


def test_recruiter_registration_generic_email_instant_approval(client):
    """Recruiters registering with generic email (@gmail.com) get instant approval."""
    res = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Fast Recruiter",
            "email": "fastrecruiter@gmail.com",
            "password": "SecurePass123",
            "role": "recruiter",
        },
    )
    assert res.status_code == 201, res.text
    assert res.json()["data"]["user"]["verification_status"] == "approved"

    # Immediate login succeeds
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "fastrecruiter@gmail.com", "password": "SecurePass123"},
    )
    assert login_res.status_code == 200
