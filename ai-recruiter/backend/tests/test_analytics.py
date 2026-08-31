"""
Tests for Phase 6 — Professional Dashboard analytics: recruiter and
candidate aggregate stats computed from real jobs/applications/
interviews/skills data.
"""
import pymupdf  # PyMuPDF

RESUME_TEXT = (
    "Casey Park\n"
    "casey.park@example.com\n\n"
    "Summary\n"
    "Backend developer with 4 years of experience.\n\n"
    "Skills\n"
    "Python, FastAPI, PostgreSQL, Docker\n\n"
    "Education\n"
    "Bachelor of Science in Computer Science, State University\n"
)


def make_pdf_bytes(text: str) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


import uuid

def _register(client, role: str, email: str, name: str = "Test User") -> str:
    unique_email = f"{uuid.uuid4().hex[:8]}_{email}"
    res = client.post(
        "/api/v1/auth/register",
        json={"name": name, "email": unique_email, "password": "SecurePass123", "role": role},
    )
    assert res.status_code == 201, res.text
    return res.json()["data"]["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_recruiter_analytics_with_no_jobs(client):
    token = _register(client, "recruiter", "recruiter.analyticsempty@example.com")
    res = client.get("/api/v1/analytics/recruiter", headers=_auth(token))
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["total_jobs"] == 0
    assert data["total_applications"] == 0
    assert data["applications_by_job"] == []


def test_candidate_analytics_with_no_resume(client):
    token = _register(client, "candidate", "candidate.analyticsempty@example.com")
    res = client.get("/api/v1/analytics/candidate", headers=_auth(token))
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["profile_completion"] == 0
    assert data["resume_uploaded"] is False
    assert data["interview_status"] == "no_resume"


def test_recruiter_analytics_reflects_real_activity(client):
    recruiter_token = _register(client, "recruiter", "recruiter.analytics@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "description": "Build APIs with FastAPI and PostgreSQL.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
        headers=_auth(recruiter_token),
    )
    job_id = job_res.json()["data"]["id"]

    candidate_token = _register(client, "candidate", "candidate.analytics@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    upload_res = client.post(
        "/api/v1/resumes/upload",
        headers=_auth(candidate_token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    candidate_id = upload_res.json()["data"]["id"]

    apply_res = client.post(f"/api/v1/jobs/{job_id}/apply", headers=_auth(candidate_token))
    assert apply_res.status_code == 201
    application_id = apply_res.json()["data"]["id"]

    client.patch(
        f"/api/v1/applications/{application_id}/status",
        json={"status": "shortlisted"},
        headers=_auth(recruiter_token),
    )

    res = client.get("/api/v1/analytics/recruiter", headers=_auth(recruiter_token))
    assert res.status_code == 200, res.text
    data = res.json()["data"]

    assert data["total_jobs"] == 1
    assert data["total_applications"] == 1
    assert data["total_candidates"] == 1
    assert data["shortlisted_count"] == 1
    assert data["hiring_funnel"]["shortlisted"] == 1
    assert data["avg_match_score"] is not None
    assert data["applications_by_job"][0]["job_title"] == "Python Developer"
    assert data["applications_by_job"][0]["count"] == 1
    skill_names = {s["skill"] for s in data["top_skills"]}
    assert "Python" in skill_names
    assert data["job_performance"][0]["applications"] == 1


def test_recruiter_analytics_only_counts_own_jobs(client):
    recruiter_a_token = _register(client, "recruiter", "recruiter.analyticsA@example.com")
    client.post(
        "/api/v1/jobs",
        json={"title": "Job A", "description": "Python role for recruiter A team.", "required_skills": ["Python"]},
        headers=_auth(recruiter_a_token),
    )

    recruiter_b_token = _register(client, "recruiter", "recruiter.analyticsB@example.com")
    res = client.get("/api/v1/analytics/recruiter", headers=_auth(recruiter_b_token))
    assert res.json()["data"]["total_jobs"] == 0


def test_candidate_analytics_reflects_real_activity(client):
    recruiter_token = _register(client, "recruiter", "recruiter.candanalytics@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "description": "Build APIs with FastAPI and PostgreSQL.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
        headers=_auth(recruiter_token),
    )
    job_id = job_res.json()["data"]["id"]

    candidate_token = _register(client, "candidate", "candidate.candanalytics@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    client.post(
        "/api/v1/resumes/upload",
        headers=_auth(candidate_token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    client.post(f"/api/v1/jobs/{job_id}/apply", headers=_auth(candidate_token))

    res = client.get("/api/v1/analytics/candidate", headers=_auth(candidate_token))
    assert res.status_code == 200, res.text
    data = res.json()["data"]

    assert data["resume_uploaded"] is True
    assert data["profile_completion"] > 0
    assert "Python" in data["skills"]
    assert data["applications_count"] == 1
    assert data["applications_by_status"].get("applied", 0) + data["applications_by_status"].get("shortlisted", 0) == 1
    assert data["interview_status"] == "not_started"


def test_candidate_analytics_shows_completed_interview_score(client):
    recruiter_token = _register(client, "recruiter", "recruiter.candanalyticsint@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "description": "Build APIs with FastAPI and PostgreSQL.",
            "required_skills": ["Python", "FastAPI"],
        },
        headers=_auth(recruiter_token),
    )
    job_id = job_res.json()["data"]["id"]

    candidate_token = _register(client, "candidate", "candidate.candanalyticsint@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    upload_res = client.post(
        "/api/v1/resumes/upload",
        headers=_auth(candidate_token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    candidate_id = upload_res.json()["data"]["id"]
    client.post(f"/api/v1/jobs/{job_id}/apply", headers=_auth(candidate_token))

    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 1},
        headers=_auth(recruiter_token),
    )
    question_id = start_res.json()["data"]["questions"][0]["id"]
    interview_id = start_res.json()["data"]["id"]
    client.post(
        f"/api/v1/interviews/{interview_id}/answers",
        json={"question_id": question_id, "answer_text": "I have strong Python and FastAPI experience."},
        headers=_auth(candidate_token),
    )

    res = client.get("/api/v1/analytics/candidate", headers=_auth(candidate_token))
    data = res.json()["data"]
    assert data["interviews_count"] == 1
    assert data["interview_status"] == "completed"
    assert data["latest_interview_score"] is not None


def test_analytics_requires_correct_role(client):
    recruiter_token = _register(client, "recruiter", "recruiter.wrongrole@example.com")
    candidate_token = _register(client, "candidate", "candidate.wrongrole@example.com")

    res1 = client.get("/api/v1/analytics/candidate", headers=_auth(recruiter_token))
    assert res1.status_code == 403

    res2 = client.get("/api/v1/analytics/recruiter", headers=_auth(candidate_token))
    assert res2.status_code == 403
