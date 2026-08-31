"""
Tests for Phase 7 — Production: admin panel, the registration
role-restriction security fix, rate limiting / login lockout, security
headers, and audit logging.
"""
from app.core import rate_limit
from app.core.config import settings
from app.services.admin_service import create_admin_user


def _register(client, role: str, email: str, name: str = "Test User") -> str:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": name, "email": email, "password": "SecurePass123", "role": role},
    )
    assert res.status_code == 201, res.text
    return res.json()["data"]["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --- Security fix: public registration cannot create an admin ---


def test_public_registration_rejects_admin_role(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Sneaky", "email": "sneaky.admin@example.com", "password": "SecurePass123", "role": "admin"},
    )
    assert res.status_code == 422


def test_public_registration_still_allows_candidate_and_recruiter(client):
    res1 = client.post(
        "/api/v1/auth/register",
        json={"name": "Cand Idate", "email": "regrole.candidate@example.com", "password": "SecurePass123", "role": "candidate"},
    )
    assert res1.status_code == 201
    res2 = client.post(
        "/api/v1/auth/register",
        json={"name": "Rec Ruiter", "email": "regrole.recruiter@example.com", "password": "SecurePass123", "role": "recruiter"},
    )
    assert res2.status_code == 201


# --- Admin bootstrap + access control ---


def test_admin_can_only_be_created_via_service_not_api(client, db_session):
    admin = create_admin_user(db_session, name="Root Admin", email="rootadmin@example.com", password="SecurePass123")
    assert admin.role.value == "admin"

    login_res = client.post(
        "/api/v1/auth/login", json={"email": "rootadmin@example.com", "password": "SecurePass123"}
    )
    assert login_res.status_code == 200
    assert login_res.json()["data"]["user"]["role"] == "admin"


def test_create_admin_rejects_duplicate_email(client, db_session):
    create_admin_user(db_session, name="First Admin", email="dupadmin@example.com", password="SecurePass123")
    try:
        create_admin_user(db_session, name="Second Admin", email="dupadmin@example.com", password="SecurePass123")
        assert False, "should have raised"
    except Exception as exc:
        assert "already exists" in str(exc) or getattr(exc, "message", "") != ""


def test_non_admin_cannot_access_admin_endpoints(client):
    recruiter_token = _register(client, "recruiter", "recruiter.noadmin@example.com")
    candidate_token = _register(client, "candidate", "candidate.noadmin@example.com")

    for token in (recruiter_token, candidate_token):
        res = client.get("/api/v1/admin/stats", headers=_auth(token))
        assert res.status_code == 403


def test_admin_can_list_and_view_users(client, db_session):
    create_admin_user(db_session, name="List Admin", email="listadmin@example.com", password="SecurePass123")
    admin_login = client.post("/api/v1/auth/login", json={"email": "listadmin@example.com", "password": "SecurePass123"})
    admin_token = admin_login.json()["data"]["access_token"]

    _register(client, "candidate", "candidate.forlisting@example.com")

    res = client.get("/api/v1/admin/users", headers=_auth(admin_token))
    assert res.status_code == 200
    emails = [u["email"] for u in res.json()["data"]]
    assert "candidate.forlisting@example.com" in emails

    res_filtered = client.get("/api/v1/admin/users?role=candidate", headers=_auth(admin_token))
    assert all(u["role"] == "candidate" for u in res_filtered.json()["data"])


def test_admin_cannot_delete_own_account(client, db_session):
    create_admin_user(db_session, name="Self Admin", email="selfadmin@example.com", password="SecurePass123")
    login = client.post("/api/v1/auth/login", json={"email": "selfadmin@example.com", "password": "SecurePass123"})
    admin_token = login.json()["data"]["access_token"]
    admin_id = login.json()["data"]["user"]["id"]

    res = client.delete(f"/api/v1/admin/users/{admin_id}", headers=_auth(admin_token))
    assert res.status_code == 400
    assert res.json()["error_code"] == "CANNOT_DELETE_SELF"


def test_admin_can_delete_other_user(client, db_session):
    create_admin_user(db_session, name="Deleter Admin", email="deleteradmin@example.com", password="SecurePass123")
    login = client.post("/api/v1/auth/login", json={"email": "deleteradmin@example.com", "password": "SecurePass123"})
    admin_token = login.json()["data"]["access_token"]

    target_login = client.post(
        "/api/v1/auth/register",
        json={"name": "Deletable", "email": "deletable@example.com", "password": "SecurePass123", "role": "candidate"},
    )
    target_id = target_login.json()["data"]["user"]["id"]

    res = client.delete(f"/api/v1/admin/users/{target_id}", headers=_auth(admin_token))
    assert res.status_code == 200

    get_res = client.get(f"/api/v1/admin/users/{target_id}", headers=_auth(admin_token))
    assert get_res.status_code == 404


def test_admin_can_manage_skills(client, db_session):
    create_admin_user(db_session, name="Skill Admin", email="skilladmin@example.com", password="SecurePass123")
    login = client.post("/api/v1/auth/login", json={"email": "skilladmin@example.com", "password": "SecurePass123"})
    admin_token = login.json()["data"]["access_token"]

    create_res = client.post(
        "/api/v1/admin/skills",
        json={"skill_name": "Rust Programming Unique1", "category": "Programming"},
        headers=_auth(admin_token),
    )
    assert create_res.status_code == 201
    skill_id = create_res.json()["data"]["id"]

    dup_res = client.post(
        "/api/v1/admin/skills",
        json={"skill_name": "Rust Programming Unique1", "category": "Programming"},
        headers=_auth(admin_token),
    )
    assert dup_res.status_code == 409

    list_res = client.get("/api/v1/admin/skills", headers=_auth(admin_token))
    assert any(s["id"] == skill_id for s in list_res.json()["data"])

    delete_res = client.delete(f"/api/v1/admin/skills/{skill_id}", headers=_auth(admin_token))
    assert delete_res.status_code == 200


def test_admin_stats_reflect_real_platform_data(client, db_session):
    create_admin_user(db_session, name="Stats Admin", email="statsadmin@example.com", password="SecurePass123")
    login = client.post("/api/v1/auth/login", json={"email": "statsadmin@example.com", "password": "SecurePass123"})
    admin_token = login.json()["data"]["access_token"]

    res = client.get("/api/v1/admin/stats", headers=_auth(admin_token))
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["total_users"] > 0
    assert data["total_recruiters"] >= 0
    assert data["total_candidates"] >= 0
    assert "applications_by_status" in data


def test_admin_can_view_all_jobs(client, db_session):
    create_admin_user(db_session, name="Jobs Admin", email="jobsadmin@example.com", password="SecurePass123")
    login = client.post("/api/v1/auth/login", json={"email": "jobsadmin@example.com", "password": "SecurePass123"})
    admin_token = login.json()["data"]["access_token"]

    recruiter_token = _register(client, "recruiter", "recruiter.adminjobsview@example.com")
    client.post(
        "/api/v1/jobs",
        json={"title": "Admin Visible Job", "description": "A job admins should see in the list.", "required_skills": ["Python"]},
        headers=_auth(recruiter_token),
    )

    res = client.get("/api/v1/admin/jobs", headers=_auth(admin_token))
    assert res.status_code == 200
    titles = [j["title"] for j in res.json()["data"]]
    assert "Admin Visible Job" in titles


# --- Audit logging ---


def test_audit_log_recorded_on_register_and_login(client, db_session):
    create_admin_user(db_session, name="Audit Admin", email="auditadmin@example.com", password="SecurePass123")
    login = client.post("/api/v1/auth/login", json={"email": "auditadmin@example.com", "password": "SecurePass123"})
    admin_token = login.json()["data"]["access_token"]

    client.post(
        "/api/v1/auth/register",
        json={"name": "Audited User", "email": "auditeduser@example.com", "password": "SecurePass123", "role": "candidate"},
    )

    res = client.get("/api/v1/admin/audit-logs?action=user.register&limit=200", headers=_auth(admin_token))
    assert res.status_code == 200
    actions = [log["action"] for log in res.json()["data"]]
    assert "user.register" in actions


# --- Login lockout ---


def test_login_lockout_after_repeated_failures(client):
    email = "lockout.target@example.com"
    _register(client, "candidate", email)

    try:
        for _ in range(settings.LOGIN_LOCKOUT_MAX_ATTEMPTS):
            res = client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPassword1"})
            assert res.status_code == 401

        # Even the CORRECT password should now be locked out.
        locked_res = client.post("/api/v1/auth/login", json={"email": email, "password": "SecurePass123"})
        assert locked_res.status_code == 429
        assert locked_res.json()["error_code"] == "ACCOUNT_TEMPORARILY_LOCKED"
    finally:
        rate_limit.clear_failed_logins(email)


# --- IP rate limiting on registration ---


def test_registration_rate_limit_trips_when_exceeded(client, monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT_REGISTER_PER_MINUTE", 2)
    rate_limit._ip_request_log.pop("register:testclient", None)

    try:
        r1 = client.post(
            "/api/v1/auth/register",
            json={"name": "Rate Limit A", "email": "ratelimit1@example.com", "password": "SecurePass123", "role": "candidate"},
        )
        r2 = client.post(
            "/api/v1/auth/register",
            json={"name": "Rate Limit B", "email": "ratelimit2@example.com", "password": "SecurePass123", "role": "candidate"},
        )
        r3 = client.post(
            "/api/v1/auth/register",
            json={"name": "Rate Limit C", "email": "ratelimit3@example.com", "password": "SecurePass123", "role": "candidate"},
        )
        assert r1.status_code == 201
        assert r2.status_code == 201
        assert r3.status_code == 429
        assert r3.json()["error_code"] == "RATE_LIMITED"
    finally:
        rate_limit._ip_request_log.pop("register:testclient", None)


# --- Security headers ---


def test_security_headers_present(client):
    res = client.get("/health")
    assert res.headers.get("x-content-type-options") == "nosniff"
    assert res.headers.get("x-frame-options") == "DENY"
    assert res.headers.get("content-security-policy") == "default-src 'none'"
