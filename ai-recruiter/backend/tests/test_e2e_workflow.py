import io
from docx import Document
from fastapi.testclient import TestClient

def make_docx_bytes(text: str) -> bytes:
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def test_full_e2e_candidate_and_recruiter_workflow(client: TestClient):
    # 1. Register Recruiter
    rec_email = "e2e_recruiter@techcorp.com"
    rec_pass = "Password123!"
    r_reg = client.post("/api/v1/auth/register", json={
        "email": rec_email,
        "password": rec_pass,
        "name": "E2E Recruiter",
        "role": "recruiter",
    })
    assert r_reg.status_code == 201, r_reg.text

    # Login Recruiter
    r_login = client.post("/api/v1/auth/login", json={"email": rec_email, "password": rec_pass})
    assert r_login.status_code == 200
    r_token = r_login.json()["data"]["access_token"]
    r_headers = {"Authorization": f"Bearer {r_token}"}

    # Recruiter posts a job
    job_resp = client.post("/api/v1/jobs", headers=r_headers, json={
        "title": "E2E Senior Python Developer",
        "description": "We need a Python developer experienced with FastAPI, React, and SQL database optimization.",
        "location": "Remote",
        "employment_type": "full_time",
        "experience_range": "3-5 years",
        "required_skills": ["Python", "FastAPI", "React", "SQL"]
    })
    assert job_resp.status_code == 201, job_resp.text
    job_id = job_resp.json()["data"]["id"]

    # 2. Register Candidate
    cand_email = "e2e_candidate@example.com"
    cand_pass = "Password123!"
    c_reg = client.post("/api/v1/auth/register", json={
        "email": cand_email,
        "password": cand_pass,
        "name": "E2E Candidate",
        "role": "candidate",
    })
    assert c_reg.status_code == 201, c_reg.text

    # Login Candidate
    c_login = client.post("/api/v1/auth/login", json={"email": cand_email, "password": cand_pass})
    assert c_login.status_code == 200
    c_token = c_login.json()["data"]["access_token"]
    c_user_id = c_login.json()["data"]["user"]["id"]
    c_headers = {"Authorization": f"Bearer {c_token}"}

    # Candidate uploads resume
    resume_text = "E2E Candidate\nEmail: e2e_candidate@example.com\nSkills: Python, FastAPI, React, SQL, PostgreSQL, Docker\nExperience: 4 years as Full Stack Engineer building APIs."
    resume_bytes = make_docx_bytes(resume_text)
    files = {"file": ("e2e_resume.docx", io.BytesIO(resume_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    upload_resp = client.post("/api/v1/resumes/upload", headers=c_headers, files=files)
    assert upload_resp.status_code == 200, upload_resp.text
    cand_profile_id = upload_resp.json()["data"]["id"]

    # Candidate applies to job
    app_resp = client.post(f"/api/v1/jobs/{job_id}/apply", headers=c_headers)
    assert app_resp.status_code == 201, app_resp.text
    app_id = app_resp.json()["data"]["id"]
    assert app_resp.json()["data"]["match_score"] > 0

    # 3. Recruiter starts AI interview for candidate
    inv_start = client.post("/api/v1/interviews", headers=r_headers, json={
        "candidate_id": cand_profile_id,
        "job_id": job_id,
        "application_id": app_id
    })
    assert inv_start.status_code == 201, inv_start.text
    interview_id = inv_start.json()["data"]["id"]

    # Candidate fetches interview
    inv_get = client.get(f"/api/v1/interviews/{interview_id}", headers=c_headers)
    assert inv_get.status_code == 200
    questions = inv_get.json()["data"]["questions"]
    assert len(questions) > 0

    # Candidate answers every question
    for q in questions:
        ans_resp = client.post(f"/api/v1/interviews/{interview_id}/answers", headers=c_headers, json={
            "question_id": q["id"],
            "answer_text": "I utilize async/await in FastAPI to prevent blocking the main loop during I/O operations."
        })
        assert ans_resp.status_code in (200, 201), ans_resp.text

    # Candidate or Recruiter fetches evaluation report
    report_resp = client.get(f"/api/v1/interviews/{interview_id}/report", headers=r_headers)
    assert report_resp.status_code == 200, report_resp.text
    rep_data = report_resp.json()["data"]
    assert rep_data["status"] == "completed"
    assert rep_data["evaluation"]["overall_score"] is not None

    # 4. Messaging System Integration Tests
    # Recruiter sends message to candidate
    msg_send = client.post("/api/v1/messages/send", headers=r_headers, json={
        "receiver_id": c_user_id,
        "content": "Hello! We loved your interview responses.",
        "application_id": app_id
    })
    assert msg_send.status_code == 201, msg_send.text

    # Candidate checks unread count
    unread_resp = client.get("/api/v1/messages/unread-count", headers=c_headers)
    assert unread_resp.status_code == 200
    assert unread_resp.json()["data"]["unread_count"] >= 1

    # Candidate gets thread (marks read)
    r_user_id = r_login.json()["data"]["user"]["id"]
    thread_resp = client.get(f"/api/v1/messages/thread/{r_user_id}", headers=c_headers)
    assert thread_resp.status_code == 200
    assert len(thread_resp.json()["data"]) >= 1

    # Check unread count is now 0
    unread_resp2 = client.get("/api/v1/messages/unread-count", headers=c_headers)
    assert unread_resp2.json()["data"]["unread_count"] == 0

    # Candidate fetches contacts and conversations
    convos_resp = client.get("/api/v1/messages/conversations", headers=c_headers)
    assert convos_resp.status_code == 200
    contacts_resp = client.get("/api/v1/messages/contacts", headers=c_headers)
    assert contacts_resp.status_code == 200

    # 5. Bulk Resume Upload Test for Recruiter
    bulk_bytes = make_docx_bytes("Candidate One\nPython, FastAPI, SQL")
    bulk_file1 = ("candidate1.docx", io.BytesIO(bulk_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    # We test single/multiple upload
    bulk_resp = client.post("/api/v1/resumes/bulk-upload", headers=r_headers, files=[("files", bulk_file1)])
    assert bulk_resp.status_code == 200, bulk_resp.text
    assert bulk_resp.json()["data"]["successful"] >= 1
