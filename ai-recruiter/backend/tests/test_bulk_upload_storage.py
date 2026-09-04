import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)

def make_test_resume_bytes(text: str) -> bytes:
    import docx
    doc = docx.Document()
    doc.add_paragraph(text)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def test_bulk_resume_upload_and_storage(db_session):
    from app.models.user import User, UserRole
    from app.models.candidate import CandidateProfile
    from app.core.security import hash_password

    # Create recruiter user
    rec_user = User(
        name="Test Recruiter",
        email="test_rec_bulk@test.com",
        password_hash=hash_password("password123"),
        role=UserRole.recruiter,
        is_active=True,
        verification_status="approved",
    )
    db_session.add(rec_user)
    db_session.commit()
    db_session.refresh(rec_user)

    token = create_access_token(subject=str(rec_user.id), role="recruiter")
    headers = {"Authorization": f"Bearer {token}"}

    # Prepare bulk resume files
    resume1_bytes = make_test_resume_bytes("John Doe\nEmail: john.doe.bulk@example.com\nSkills: Python, FastAPI, SQL\nExperience: Senior Developer with 5 years experience.")
    resume2_bytes = make_test_resume_bytes("Jane Smith\nEmail: jane.smith.bulk@example.com\nSkills: React, JavaScript, Node.js\nExperience: Frontend Engineer with 4 years experience.")

    files = [
        ("files", ("john_doe.docx", io.BytesIO(resume1_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
        ("files", ("jane_smith.docx", io.BytesIO(resume2_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
    ]

    response = client.post("/api/v1/resumes/bulk-upload", headers=headers, files=files)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["success"] is True
    assert data["data"]["successful"] == 2
    assert len(data["data"]["results"]) == 2

    # Verify candidates are stored in database
    cand1_user = db_session.query(User).filter(User.email == "john.doe.bulk@example.com").first()
    assert cand1_user is not None
    assert cand1_user.name == "John Doe"

    cand1_profile = db_session.query(CandidateProfile).filter(CandidateProfile.user_id == cand_user.id if 'cand_user' in locals() else CandidateProfile.user_id == cand1_user.id).first()
    assert cand1_profile is not None
    assert cand1_profile.resume_path is not None
    assert "Python" in [cs.skill.skill_name for cs in cand1_profile.candidate_skills if cs.skill]

    cand2_user = db_session.query(User).filter(User.email == "jane.smith.bulk@example.com").first()
    assert cand2_user is not None
    assert cand2_user.name == "Jane Smith"
