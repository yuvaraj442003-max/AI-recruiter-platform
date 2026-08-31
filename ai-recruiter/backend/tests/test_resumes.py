"""
Tests for the resume upload pipeline: file validation, PDF/DOCX text
extraction, and skill/field extraction — using fixture files generated
in-memory so the suite has no external file dependencies. Uses the
shared session-scoped test database and client from conftest.py.
"""
import io

import pymupdf
from docx import Document

RESUME_TEXT = (
    "Jane Doe\n"
    "jane.doe@example.com\n"
    "+1 (555) 123-4567\n\n"
    "Summary\n"
    "Backend developer with 3 years of experience building APIs.\n\n"
    "Skills\n"
    "Python, Django, FastAPI, PostgreSQL, Docker, Machine Learning\n\n"
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


def make_docx_bytes(text: str) -> bytes:
    document = Document()
    for line in text.split("\n"):
        document.add_paragraph(line)
    buf = io.BytesIO()
    document.save(buf)
    return buf.getvalue()


def _register_candidate(client, email: str) -> str:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Jane Doe", "email": email, "password": "SecurePass123", "role": "candidate"},
    )
    assert res.status_code == 201
    return res.json()["data"]["access_token"]


def _register_recruiter(client, email: str) -> str:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Rita Recruiter", "email": email, "password": "SecurePass123", "role": "recruiter"},
    )
    assert res.status_code == 201
    return res.json()["data"]["access_token"]


def test_upload_pdf_resume_extracts_fields(client):
    token = _register_candidate(client, "candidate.pdf@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)

    res = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    assert res.status_code == 200, res.text
    data = res.json()["data"]

    assert "Python" in data["skills"]
    assert "FastAPI" in data["skills"]
    assert "PostgreSQL" in data["skills"]
    assert data["experience_years"] == 3.0
    assert data["resume_original_filename"] == "resume.pdf"
    assert data["profile_score"] > 0


def test_upload_docx_resume_extracts_fields(client):
    token = _register_candidate(client, "candidate.docx@example.com")
    docx_bytes = make_docx_bytes(RESUME_TEXT)

    res = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "file": (
                "resume.docx",
                docx_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert "Django" in data["skills"]
    assert "Docker" in data["skills"]


def test_upload_rejects_unsupported_file_type(client):
    token = _register_candidate(client, "candidate.badfile@example.com")
    res = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.txt", b"just some text", "text/plain")},
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "UNSUPPORTED_FILE_TYPE"


def test_recruiter_cannot_upload_resume(client):
    token = _register_recruiter(client, "recruiter.upload@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    res = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    assert res.status_code == 403
    assert res.json()["error_code"] == "PERMISSION_DENIED"


def test_get_my_profile_after_upload(client):
    token = _register_candidate(client, "candidate.me@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )

    res = client.get("/api/v1/resumes/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "Python" in res.json()["data"]["skills"]


def test_get_my_profile_without_upload_returns_404(client):
    token = _register_candidate(client, "candidate.noresume@example.com")
    res = client.get("/api/v1/resumes/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
    assert res.json()["error_code"] == "NOT_FOUND"


def test_recruiter_can_view_candidate_profile_by_id(client):
    candidate_token = _register_candidate(client, "candidate.viewedby@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    upload_res = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {candidate_token}"},
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    profile_id = upload_res.json()["data"]["id"]

    recruiter_token = _register_recruiter(client, "recruiter.viewer@example.com")
    res = client.get(
        f"/api/v1/resumes/{profile_id}", headers={"Authorization": f"Bearer {recruiter_token}"}
    )
    assert res.status_code == 200
    assert "Python" in res.json()["data"]["skills"]


def test_candidate_can_edit_profile(client):
    candidate_token = _register_candidate(client, "candidate.edit@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {candidate_token}"},
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )

    update_payload = {
        "location": "Salem, India",
        "phone": "+91 9876543210",
        "skills": ["Python", "FastAPI", "React", "Docker"],
        "experience_years": 4.5,
    }
    res = client.put(
        "/api/v1/resumes/me",
        headers={"Authorization": f"Bearer {candidate_token}"},
        json=update_payload,
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["location"] == "Salem, India"
    assert data["phone"] == "+91 9876543210"
    assert data["experience_years"] == 4.5
    assert "React" in data["skills"]


def test_candidate_can_delete_profile(client):
    candidate_token = _register_candidate(client, "candidate.delete@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {candidate_token}"},
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )

    del_res = client.delete("/api/v1/resumes/me", headers={"Authorization": f"Bearer {candidate_token}"})
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Verify profile is gone
    get_res = client.get("/api/v1/resumes/me", headers={"Authorization": f"Bearer {candidate_token}"})
    assert get_res.status_code == 404
