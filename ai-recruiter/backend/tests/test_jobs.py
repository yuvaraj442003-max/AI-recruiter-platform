"""
Tests for job CRUD, resume-based applications, ad-hoc match scoring,
ranking, and job recommendations.
"""
import io

import pymupdf  # PyMuPDF

RESUME_TEXT = (
    "Jordan Lee\n"
    "jordan.lee@example.com\n"
    "+1 (555) 987-6543\n\n"
    "Summary\n"
    "Backend developer with 4 years of experience building REST APIs.\n\n"
    "Skills\n"
    "Python, Django, FastAPI, PostgreSQL, Docker\n\n"
    "Education\n"
    "Bachelor of Science in Computer Science, Tech University\n"
)

JOB_DESCRIPTION = (
    "We are looking for a Python Developer to join our backend team. "
    "You'll build and maintain REST APIs using FastAPI and PostgreSQL, "
    "and work closely with our infrastructure team on Docker deployments."
)


def make_pdf_bytes(text: str) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def _register(client, role: str, email: str, name: str = "Test User") -> str:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": name, "email": email, "password": "SecurePass123", "role": role},
    )
    assert res.status_code == 201, res.text
    return res.json()["data"]["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _create_job(client, recruiter_token, **overrides) -> dict:
    payload = {
        "title": "Python Developer",
        "description": JOB_DESCRIPTION,
        "location": "Remote",
        "employment_type": "full_time",
        "experience_required": 3,
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "AWS"],
    }
    payload.update(overrides)
    res = client.post("/api/v1/jobs", json=payload, headers=_auth(recruiter_token))
    assert res.status_code == 201, res.text
    return res.json()["data"]


def _upload_resume(client, candidate_token):
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    res = client.post(
        "/api/v1/resumes/upload",
        headers=_auth(candidate_token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    assert res.status_code == 200, res.text
    return res.json()["data"]


def test_recruiter_can_create_job(client):
    token = _register(client, "recruiter", "recruiter.create@example.com")
    job = _create_job(client, token)
    assert job["title"] == "Python Developer"
    assert "Python" in job["required_skills"]
    assert "Docker" in job["preferred_skills"]
    assert job["status"] == "published"


def test_candidate_cannot_create_job(client):
    token = _register(client, "candidate", "candidate.createjob@example.com")
    res = client.post(
        "/api/v1/jobs",
        json={"title": "Hack Job", "description": "x" * 20},
        headers=_auth(token),
    )
    assert res.status_code == 403
    assert res.json()["error_code"] == "PERMISSION_DENIED"


def test_job_skills_auto_extracted_when_not_provided(client):
    token = _register(client, "recruiter", "recruiter.autoextract@example.com")
    res = client.post(
        "/api/v1/jobs",
        json={
            "title": "Backend Engineer",
            "description": "Looking for a Python and Django expert with PostgreSQL knowledge.",
        },
        headers=_auth(token),
    )
    assert res.status_code == 201, res.text
    skills = res.json()["data"]["required_skills"]
    assert "Python" in skills
    assert "Django" in skills
    assert "PostgreSQL" in skills


def test_candidates_only_see_published_jobs(client):
    recruiter_token = _register(client, "recruiter", "recruiter.visibility@example.com")
    _create_job(client, recruiter_token, title="Draft Job", status="draft")
    _create_job(client, recruiter_token, title="Published Job", status="published")

    candidate_token = _register(client, "candidate", "candidate.visibility@example.com")
    res = client.get("/api/v1/jobs", headers=_auth(candidate_token))
    titles = [j["title"] for j in res.json()["data"]]
    assert "Published Job" in titles
    assert "Draft Job" not in titles


def test_recruiter_sees_own_draft_jobs(client):
    recruiter_token = _register(client, "recruiter", "recruiter.owndraft@example.com")
    _create_job(client, recruiter_token, title="My Draft Job", status="draft")

    res = client.get("/api/v1/jobs", headers=_auth(recruiter_token))
    titles = [j["title"] for j in res.json()["data"]]
    assert "My Draft Job" in titles


def test_recruiter_can_update_own_job(client):
    token = _register(client, "recruiter", "recruiter.update@example.com")
    job = _create_job(client, token)
    res = client.put(
        f"/api/v1/jobs/{job['id']}",
        json={"title": "Senior Python Developer"},
        headers=_auth(token),
    )
    assert res.status_code == 200
    assert res.json()["data"]["title"] == "Senior Python Developer"


def test_recruiter_cannot_update_others_job(client):
    owner_token = _register(client, "recruiter", "recruiter.owner@example.com")
    job = _create_job(client, owner_token)

    other_token = _register(client, "recruiter", "recruiter.intruder@example.com")
    res = client.put(
        f"/api/v1/jobs/{job['id']}", json={"title": "Hijacked"}, headers=_auth(other_token)
    )
    assert res.status_code == 403


def test_candidate_can_apply_and_gets_match_score(client):
    recruiter_token = _register(client, "recruiter", "recruiter.apply@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.apply@example.com")
    _upload_resume(client, candidate_token)

    res = client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))
    assert res.status_code == 201, res.text
    data = res.json()["data"]
    assert data["status"] in ("applied", "shortlisted")
    assert data["match_score"] is not None
    assert 0 <= data["match_score"] <= 100
    # Strong overlap (Python/FastAPI/PostgreSQL/Docker all present) should score well.
    assert data["match_score"] > 50


def test_cannot_apply_without_resume(client):
    recruiter_token = _register(client, "recruiter", "recruiter.noresumejob@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.noresume2@example.com")
    res = client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))
    assert res.status_code == 400
    assert res.json()["error_code"] == "NO_RESUME"


def test_cannot_apply_twice(client):
    recruiter_token = _register(client, "recruiter", "recruiter.duplicateapply@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.duplicateapply@example.com")
    _upload_resume(client, candidate_token)

    first = client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))
    assert first.status_code == 201

    second = client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))
    assert second.status_code == 409
    assert second.json()["error_code"] == "CONFLICT"


def test_ranking_orders_by_match_score(client):
    recruiter_token = _register(client, "recruiter", "recruiter.ranking@example.com")
    job = _create_job(client, recruiter_token)

    strong_token = _register(client, "candidate", "candidate.strong@example.com")
    _upload_resume(client, strong_token)  # has Python/FastAPI/PostgreSQL/Docker
    client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(strong_token))

    weak_token = _register(client, "candidate", "candidate.weak@example.com")
    weak_pdf = make_pdf_bytes("Sam Weak\nsam.weak@example.com\n\nSkills\nPHP, WordPress\n")
    client.post(
        "/api/v1/resumes/upload",
        headers=_auth(weak_token),
        files={"file": ("resume.pdf", weak_pdf, "application/pdf")},
    )
    client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(weak_token))

    res = client.get(f"/api/v1/jobs/{job['id']}/ranking", headers=_auth(recruiter_token))
    assert res.status_code == 200
    ranking = res.json()["data"]
    assert len(ranking) == 2
    assert ranking[0]["rank"] == 1
    assert ranking[0]["match_score"] >= ranking[1]["match_score"]


def test_non_owner_recruiter_cannot_view_ranking(client):
    owner_token = _register(client, "recruiter", "recruiter.rankowner@example.com")
    job = _create_job(client, owner_token)

    other_token = _register(client, "recruiter", "recruiter.ranksnooper@example.com")
    res = client.get(f"/api/v1/jobs/{job['id']}/ranking", headers=_auth(other_token))
    assert res.status_code == 403


def test_job_applications_listing_includes_candidate_info(client):
    recruiter_token = _register(client, "recruiter", "recruiter.applist@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.applist@example.com", name="Applicant One")
    _upload_resume(client, candidate_token)
    client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))

    res = client.get(f"/api/v1/jobs/{job['id']}/applications", headers=_auth(recruiter_token))
    assert res.status_code == 200
    apps = res.json()["data"]
    assert len(apps) == 1
    assert apps[0]["candidate_name"] == "Applicant One"
    assert apps[0]["job_title"] == job["title"]


def test_candidate_can_list_own_applications(client):
    recruiter_token = _register(client, "recruiter", "recruiter.myapps@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.myapps@example.com")
    _upload_resume(client, candidate_token)
    client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))

    res = client.get("/api/v1/applications", headers=_auth(candidate_token))
    assert res.status_code == 200
    apps = res.json()["data"]
    assert len(apps) == 1
    assert apps[0]["job_title"] == job["title"]


def test_recruiter_can_update_application_status(client):
    recruiter_token = _register(client, "recruiter", "recruiter.statusupdate@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.statusupdate@example.com")
    _upload_resume(client, candidate_token)
    apply_res = client.post(f"/api/v1/jobs/{job['id']}/apply", headers=_auth(candidate_token))
    application_id = apply_res.json()["data"]["id"]

    res = client.patch(
        f"/api/v1/applications/{application_id}/status",
        json={"status": "shortlisted"},
        headers=_auth(recruiter_token),
    )
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "shortlisted"


def test_ad_hoc_match_score_endpoint(client):
    recruiter_token = _register(client, "recruiter", "recruiter.adhoc@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.adhoc@example.com")
    profile = _upload_resume(client, candidate_token)

    res = client.get(
        f"/api/v1/matching/{profile['id']}/{job['id']}", headers=_auth(candidate_token)
    )
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert "final_score" in data
    assert "breakdown" in data
    assert "explanation" in data
    assert "Python" in data["explanation"]["matched_required_skills"]


def test_other_candidate_cannot_view_someone_elses_match_score(client):
    recruiter_token = _register(client, "recruiter", "recruiter.adhocsnoop@example.com")
    job = _create_job(client, recruiter_token)

    candidate_token = _register(client, "candidate", "candidate.adhocowner@example.com")
    profile = _upload_resume(client, candidate_token)

    intruder_token = _register(client, "candidate", "candidate.adhocintruder@example.com")
    res = client.get(
        f"/api/v1/matching/{profile['id']}/{job['id']}", headers=_auth(intruder_token)
    )
    assert res.status_code == 403


def test_job_recommendations_for_candidate(client):
    recruiter_token = _register(client, "recruiter", "recruiter.recommend@example.com")
    _create_job(client, recruiter_token, title="Python Backend Role Unique123")
    _create_job(
        client,
        recruiter_token,
        title="Graphic Designer Unique123",
        description="Looking for a graphic designer skilled in Adobe Photoshop and Illustrator.",
        required_skills=["Communication"],
        preferred_skills=[],
    )

    candidate_token = _register(client, "candidate", "candidate.recommend@example.com")
    _upload_resume(client, candidate_token)

    res = client.get("/api/v1/recommendations/jobs?limit=50", headers=_auth(candidate_token))
    assert res.status_code == 200
    recommendations = res.json()["data"]

    by_title = {r["job"]["title"]: r["match_score"] for r in recommendations}
    assert "Python Backend Role Unique123" in by_title
    assert "Graphic Designer Unique123" in by_title
    # The Python role should score higher than the unrelated design role
    # for a Python/FastAPI/PostgreSQL/Docker candidate.
    assert by_title["Python Backend Role Unique123"] > by_title["Graphic Designer Unique123"]


def test_recruiter_can_export_full_candidate_details(client):
    recruiter_token = _register(client, "recruiter", "recruiter.export@example.com")
    candidate_token = _register(client, "candidate", "candidate.export@example.com")
    profile = _upload_resume(client, candidate_token)

    # 1. Export as ZIP Package
    res_zip = client.get(f"/api/v1/resumes/{profile['id']}/export?format=zip", headers=_auth(recruiter_token))
    assert res_zip.status_code == 200
    assert res_zip.headers["content-type"] == "application/zip"
    assert "Content-Disposition" in res_zip.headers
    assert len(res_zip.content) > 0

    # 2. Export as HTML Dossier
    res_html = client.get(f"/api/v1/resumes/{profile['id']}/export?format=html", headers=_auth(recruiter_token))
    assert res_html.status_code == 200
    assert "text/html" in res_html.headers["content-type"]
    assert "Candidate Profile" in res_html.text

    # 3. Export as JSON
    res_json = client.get(f"/api/v1/resumes/{profile['id']}/export?format=json", headers=_auth(recruiter_token))
    assert res_json.status_code == 200
    data = res_json.json()["data"]
    assert data["email"] == "candidate.export@example.com"

