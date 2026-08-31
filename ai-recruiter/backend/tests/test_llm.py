"""
Tests for Phase 4 — LLM service layer: resume AI summary, job
description analysis, and interview question generation. Since no LLM
API key is configured in the test environment, these tests exercise
the template fallback path end-to-end (which is exactly what runs in
any deployment without an LLM configured) — and separately assert the
provider-selection logic in llm_service directly.
"""
import io

import pymupdf  # PyMuPDF

from app.ai import llm_service

RESUME_TEXT = (
    "Taylor Kim\n"
    "taylor.kim@example.com\n\n"
    "Summary\n"
    "Backend developer with 4 years of experience building REST APIs.\n\n"
    "Skills\n"
    "Python, Django, FastAPI, PostgreSQL, Docker\n\n"
    "Education\n"
    "Bachelor of Science in Computer Science, Tech University\n"
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


# --- llm_service provider selection (unit-level, no network) ---


def test_no_provider_configured_by_default(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "LLM_PROVIDER", "")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    monkeypatch.setattr(settings, "HF_API_KEY", "")
    monkeypatch.setattr(settings, "LLM_API_KEY", "")
    assert llm_service.get_active_provider() is None
    assert llm_service.is_configured() is False


def test_generate_returns_none_when_unconfigured(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "LLM_PROVIDER", "")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    monkeypatch.setattr(settings, "HF_API_KEY", "")
    monkeypatch.setattr(settings, "LLM_API_KEY", "")
    assert llm_service.generate("system", "user") is None


def test_provider_detection_from_gemini_key(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "LLM_PROVIDER", "")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "AIza-fake-gemini-key")
    assert llm_service.get_active_provider() == "gemini"
    assert llm_service.is_configured() is True


def test_provider_detection_from_openai_key(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "LLM_PROVIDER", "")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-fake")
    assert llm_service.get_active_provider() == "openai"
    assert llm_service.is_configured() is True


def test_provider_detection_from_hf_key(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "LLM_PROVIDER", "")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    monkeypatch.setattr(settings, "HF_API_KEY", "hf-fake")
    assert llm_service.get_active_provider() == "huggingface"


def test_explicit_provider_overrides_key_detection(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-fake")
    monkeypatch.setattr(settings, "LLM_PROVIDER", "huggingface")
    assert llm_service.get_active_provider() == "huggingface"


def test_openai_call_fails_gracefully_with_bad_key(monkeypatch):
    """With a fake key and no real network access, the call should fail
    and return None rather than raising — never break the calling endpoint."""
    from app.core.config import settings

    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-definitely-fake-and-invalid")
    result = llm_service.generate("system prompt", "user prompt", max_tokens=50)
    assert result is None


# --- Resume AI summary (template fallback path) ---


def test_generate_resume_summary_endpoint(client):
    token = _register(client, "candidate", "candidate.summary@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    client.post(
        "/api/v1/resumes/upload",
        headers=_auth(token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )

    res = client.post("/api/v1/resumes/summary", headers=_auth(token))
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["ai_summary"]
    assert "AI summary generated" in res.json()["message"]


def test_generate_summary_without_resume_returns_404(client):
    token = _register(client, "candidate", "candidate.nosummary@example.com")
    res = client.post("/api/v1/resumes/summary", headers=_auth(token))
    assert res.status_code == 404


def test_recruiter_cannot_generate_resume_summary(client):
    token = _register(client, "recruiter", "recruiter.summary@example.com")
    res = client.post("/api/v1/resumes/summary", headers=_auth(token))
    assert res.status_code == 403


# --- Job description analysis (template fallback path) ---


def test_analyze_job_description(client):
    token = _register(client, "recruiter", "recruiter.analyze@example.com")
    res = client.post(
        "/api/v1/jobs/analyze",
        json={"description": "Looking for a Python developer skilled in Django and PostgreSQL."},
        headers=_auth(token),
    )
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["source"] in ["llm", "template"]
    assert "Python" in data["required_skills"]
    assert "Django" in data["required_skills"]



def test_candidate_cannot_analyze_job_description(client):
    token = _register(client, "candidate", "candidate.analyze@example.com")
    res = client.post(
        "/api/v1/jobs/analyze",
        json={"description": "Looking for a Python developer with Django experience."},
        headers=_auth(token),
    )
    assert res.status_code == 403


# --- Interview question generation (template fallback path) ---


def test_generate_questions_for_job(client):
    recruiter_token = _register(client, "recruiter", "recruiter.questions@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "description": "Build REST APIs using FastAPI and PostgreSQL.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
        headers=_auth(recruiter_token),
    )
    job_id = job_res.json()["data"]["id"]

    res = client.post(
        f"/api/v1/jobs/{job_id}/generate-questions?num_questions=5",
        headers=_auth(recruiter_token),
    )
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["source"] == "template"
    assert len(data["questions"]) == 5
    types = {q["type"] for q in data["questions"]}
    assert "behavioral" in types
    for q in data["questions"]:
        assert q["question"]
        assert q["difficulty"] in {"easy", "medium", "hard"}


def test_non_owner_cannot_generate_questions(client):
    owner_token = _register(client, "recruiter", "recruiter.qowner@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={"title": "Backend Role", "description": "Python backend role.", "required_skills": ["Python"]},
        headers=_auth(owner_token),
    )
    job_id = job_res.json()["data"]["id"]

    other_token = _register(client, "recruiter", "recruiter.qintruder@example.com")
    res = client.post(f"/api/v1/jobs/{job_id}/generate-questions", headers=_auth(other_token))
    assert res.status_code == 403


def test_candidate_cannot_generate_questions(client):
    recruiter_token = _register(client, "recruiter", "recruiter.qcand@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={"title": "Backend Role", "description": "Python backend role.", "required_skills": ["Python"]},
        headers=_auth(recruiter_token),
    )
    job_id = job_res.json()["data"]["id"]

    candidate_token = _register(client, "candidate", "candidate.qgen@example.com")
    res = client.post(f"/api/v1/jobs/{job_id}/generate-questions", headers=_auth(candidate_token))
    assert res.status_code == 403
