"""
Tests for register/login/me. Uses the shared session-scoped test
database and client from conftest.py.
"""


def test_register_new_user(client, db_session):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Jane Doe", "email": "jane@example.com", "password": "SecurePass123", "role": "candidate"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["user"]["email"] == "jane@example.com"
    assert "access_token" in body["data"]

    from app.models.user import User
    user = db_session.query(User).filter(User.email == "jane@example.com").first()
    if user:
        user.is_email_verified = True
        db_session.commit()


def test_register_duplicate_email_fails(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Jane Two", "email": "jane@example.com", "password": "SecurePass123", "role": "candidate"},
    )
    assert response.status_code == 409
    assert response.json()["error_code"] == "CONFLICT"


def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={"email": "jane@example.com", "password": "SecurePass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]


def test_login_wrong_password(client):
    response = client.post("/api/v1/auth/login", json={"email": "jane@example.com", "password": "WrongPass"})
    assert response.status_code == 401


def test_me_requires_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token(client):
    login = client.post("/api/v1/auth/login", json={"email": "jane@example.com", "password": "SecurePass123"})
    token = login.json()["data"]["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "jane@example.com"


def test_google_login_existing_user(client):
    response = client.post("/api/v1/auth/google", json={"credential": "jane@example.com", "role": "candidate"})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["user"]["email"] == "jane@example.com"


def test_candidate_cannot_login_as_recruiter(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Candidate Separated", "email": "candidate.sep@example.com", "password": "SecurePass123", "role": "candidate"},
    )
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "candidate.sep@example.com", "password": "SecurePass123", "expected_role": "recruiter"},
    )
    assert res.status_code == 401
    assert "Access Denied" in res.json()["message"]


def test_recruiter_cannot_login_as_candidate(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Recruiter Separated", "email": "recruiter.sep@vgensoft.com", "password": "SecurePass123", "role": "recruiter"},
    )
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "recruiter.sep@vgensoft.com", "password": "SecurePass123", "expected_role": "candidate"},
    )
    assert res.status_code == 401
    assert "Access Denied" in res.json()["message"]


def test_recruiter_gmail_domain_rejected(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Recruiter Gmail", "email": "recruiter@gmail.com", "password": "SecurePass123", "role": "recruiter"},
    )
    assert res.status_code == 400
    assert "Recruiters must use a company email address" in res.json()["message"]


def test_recruiter_company_domain_accepted(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Recruiter Company", "email": "yuva@vgensoft.com", "password": "SecurePass123", "role": "recruiter"},
    )
    assert res.status_code == 201
    assert res.json()["success"] is True


def test_candidate_gmail_accepted(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Candidate Gmail", "email": "candidate@gmail.com", "password": "SecurePass123", "role": "candidate"},
    )
    assert res.status_code == 201
    assert res.json()["success"] is True


