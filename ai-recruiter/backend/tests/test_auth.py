"""
Tests for register/login/me. Uses the shared session-scoped test
database and client from conftest.py.
"""


def test_register_new_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Jane Doe", "email": "jane@example.com", "password": "SecurePass123", "role": "candidate"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["user"]["email"] == "jane@example.com"
    assert "access_token" in body["data"]


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


