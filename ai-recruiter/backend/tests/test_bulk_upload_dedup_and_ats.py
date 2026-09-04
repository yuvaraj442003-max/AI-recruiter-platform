import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.models.user import User, UserRole
from app.models.candidate import CandidateProfile
from app.core.security import hash_password

client = TestClient(app)

def make_docx(text: str) -> bytes:
    import docx
    doc = docx.Document()
    doc.add_paragraph(text)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def test_bulk_upload_custom_jd_and_deduplication(db_session):
    # 1. Create Recruiter
    rec = User(
        name="ATS Test Recruiter",
        email="ats_recruiter@test.com",
        password_hash=hash_password("pass123"),
        role=UserRole.recruiter,
        is_active=True,
        verification_status="approved",
    )
    db_session.add(rec)
    db_session.commit()
    db_session.refresh(rec)

    token = create_access_token(subject=str(rec.id), role="recruiter")
    headers = {"Authorization": f"Bearer {token}"}

    # Candidate 1: High match for Python & FastAPI Senior role
    res1 = make_docx("Alice Backend\nEmail: alice.backend@example.com\nPhone: +1 555 123 4567\nSkills: Python, FastAPI, PostgreSQL, Docker, Redis\nExperience: Senior Backend Engineer with 6 years experience building REST APIs.")
    
    # Candidate 2: Low match for Backend role
    res2 = make_docx("Bob Designer\nEmail: bob.designer@example.com\nPhone: +1 555 987 6543\nSkills: Figma, UI/UX, Photoshop, Graphic Design\nExperience: Graphic Designer with 1 year experience.")

    files = [
        ("files", ("alice.docx", io.BytesIO(res1), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
        ("files", ("bob.docx", io.BytesIO(res2), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
    ]

    data_payload = {
        "custom_jd_title": "Senior Python FastAPI Developer",
        "custom_jd_skills": "Python, FastAPI, SQL",
        "custom_jd_exp": "5",
        "custom_jd_description": "We are seeking a Senior Backend Engineer proficient in Python and FastAPI to build scalable microservices.",
    }

    # First upload: Process both resumes against custom JD
    res = client.post("/api/v1/resumes/bulk-upload", headers=headers, files=files, data=data_payload)
    assert res.status_code == 200, res.text
    res_json = res.json()
    assert res_json["success"] is True
    data = res_json["data"]

    assert data["total"] == 2
    assert data["successful"] == 2, f"Failed results: {data['results']}"
    assert data["duplicates"] == 0
    assert data["best_match"] is not None
    assert "Alice" in data["best_match"]["candidate_name"]

    results = data["results"]
    assert len(results) == 2
    # Verify ranking: Alice (high match) should be rank 1 and best match
    assert results[0]["rank"] == 1
    assert results[0]["is_best_match"] is True
    assert results[0]["overall_match_score"] > results[1]["overall_match_score"]

    # 2. Second upload: Upload duplicate resume for Alice to test deduplication
    duplicate_files = [
        ("files", ("alice_copy.docx", io.BytesIO(res1), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
    ]

    res_dup = client.post("/api/v1/resumes/bulk-upload", headers=headers, files=duplicate_files, data=data_payload)
    assert res_dup.status_code == 200, res_dup.text
    dup_json = res_dup.json()["data"]

    assert dup_json["total"] == 1
    assert dup_json["duplicates"] == 1
    assert dup_json["results"][0]["is_duplicate"] is True
    assert "file hash match" in dup_json["results"][0]["duplicate_reason"].lower() or "email" in dup_json["results"][0]["duplicate_reason"].lower()

    # Verify no duplicate user created in DB
    alice_users = db_session.query(User).filter(User.email == "alice.backend@example.com").all()
    assert len(alice_users) == 1
