"""
Tests for Phase 5 — AI Interview: starting an interview (auto-generates
questions), submitting answers (auto-evaluated per-answer), automatic
completion + final evaluation once all questions are answered, the
report endpoint, and speech-to-text's graceful no-provider behavior.
"""
import io

import pymupdf  # PyMuPDF

RESUME_TEXT = (
    "Morgan Chen\n"
    "morgan.chen@example.com\n\n"
    "Summary\n"
    "Backend developer with 5 years of experience building REST APIs.\n\n"
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


def _register(client, role: str, email: str, name: str = "Test User") -> str:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": name, "email": email, "password": "SecurePass123", "role": role},
    )
    assert res.status_code == 201, res.text
    return res.json()["data"]["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _setup_application(client, recruiter_email, candidate_email):
    """Registers a recruiter+candidate, posts a job, uploads a resume, and applies.
    Returns (recruiter_token, candidate_token, job_id, candidate_profile_id)."""
    recruiter_token = _register(client, "recruiter", recruiter_email)
    job_res = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "description": "Build REST APIs using FastAPI and PostgreSQL, with Docker deployments.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
        headers=_auth(recruiter_token),
    )
    assert job_res.status_code == 201, job_res.text
    job_id = job_res.json()["data"]["id"]

    candidate_token = _register(client, "candidate", candidate_email, name="Interview Candidate")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    upload_res = client.post(
        "/api/v1/resumes/upload",
        headers=_auth(candidate_token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    assert upload_res.status_code == 200, upload_res.text
    candidate_profile_id = upload_res.json()["data"]["id"]

    apply_res = client.post(f"/api/v1/jobs/{job_id}/apply", headers=_auth(candidate_token))
    assert apply_res.status_code == 201, apply_res.text

    return recruiter_token, candidate_token, job_id, candidate_profile_id


def test_recruiter_can_start_interview_with_generated_questions(client):
    recruiter_token, _, job_id, candidate_id = _setup_application(
        client, "recruiter.startint@example.com", "candidate.startint@example.com"
    )

    res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "interview_type": "mixed", "num_questions": 5},
        headers=_auth(recruiter_token),
    )
    assert res.status_code == 201, res.text
    data = res.json()["data"]
    assert data["status"] == "in_progress"
    assert len(data["questions"]) == 5
    assert data["started_at"] is not None


def test_cannot_start_interview_without_application(client):
    recruiter_token = _register(client, "recruiter", "recruiter.noapp@example.com")
    job_res = client.post(
        "/api/v1/jobs",
        json={"title": "Backend Role", "description": "Python backend role needing FastAPI skills.", "required_skills": ["Python"]},
        headers=_auth(recruiter_token),
    )
    job_id = job_res.json()["data"]["id"]

    candidate_token = _register(client, "candidate", "candidate.noapp@example.com")
    pdf_bytes = make_pdf_bytes(RESUME_TEXT)
    upload_res = client.post(
        "/api/v1/resumes/upload",
        headers=_auth(candidate_token),
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )
    candidate_id = upload_res.json()["data"]["id"]

    # Note: candidate never applied to the job.
    res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id},
        headers=_auth(recruiter_token),
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "NO_APPLICATION"


def test_cannot_start_duplicate_interview(client):
    recruiter_token, _, job_id, candidate_id = _setup_application(
        client, "recruiter.dupint@example.com", "candidate.dupint@example.com"
    )
    payload = {"candidate_id": candidate_id, "job_id": job_id}
    first = client.post("/api/v1/interviews", json=payload, headers=_auth(recruiter_token))
    assert first.status_code == 201

    second = client.post("/api/v1/interviews", json=payload, headers=_auth(recruiter_token))
    assert second.status_code == 409


def test_candidate_can_view_and_answer_own_interview(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.answer@example.com", "candidate.answer@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 3},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]
    questions = start_res.json()["data"]["questions"]

    # Candidate can view their own interview.
    get_res = client.get(f"/api/v1/interviews/{interview_id}", headers=_auth(candidate_token))
    assert get_res.status_code == 200
    assert get_res.json()["data"]["status"] == "in_progress"

    # Answer the first question.
    first_question = questions[0]
    answer_res = client.post(
        f"/api/v1/interviews/{interview_id}/answers",
        json={"question_id": first_question["id"], "answer_text": "I have built REST APIs with FastAPI and PostgreSQL for 5 years."},
        headers=_auth(candidate_token),
    )
    assert answer_res.status_code == 201, answer_res.text
    answer_data = answer_res.json()["data"]
    assert answer_data["answer_score"] is not None
    assert answer_data["interview_status"] == "in_progress"  # not all questions answered yet


def test_interview_auto_completes_after_all_questions_answered(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.autocomplete@example.com", "candidate.autocomplete@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 2},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]
    questions = start_res.json()["data"]["questions"]

    last_status = None
    for q in questions:
        res = client.post(
            f"/api/v1/interviews/{interview_id}/answers",
            json={"question_id": q["id"], "answer_text": "I have hands-on experience with Python, FastAPI, and PostgreSQL in production."},
            headers=_auth(candidate_token),
        )
        assert res.status_code == 201, res.text
        last_status = res.json()["data"]["interview_status"]

    assert last_status == "completed"

    # Interview detail should now show overall_score and full answers.
    detail = client.get(f"/api/v1/interviews/{interview_id}", headers=_auth(candidate_token))
    assert detail.json()["data"]["status"] == "completed"
    assert detail.json()["data"]["overall_score"] is not None


def test_cannot_answer_same_question_twice(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.dupanswer@example.com", "candidate.dupanswer@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 3},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]
    question_id = start_res.json()["data"]["questions"][0]["id"]

    first = client.post(
        f"/api/v1/interviews/{interview_id}/answers",
        json={"question_id": question_id, "answer_text": "First answer."},
        headers=_auth(candidate_token),
    )
    assert first.status_code == 201

    second = client.post(
        f"/api/v1/interviews/{interview_id}/answers",
        json={"question_id": question_id, "answer_text": "Trying again."},
        headers=_auth(candidate_token),
    )
    assert second.status_code == 409


def test_other_candidate_cannot_answer_someone_elses_interview(client):
    recruiter_token, _, job_id, candidate_id = _setup_application(
        client, "recruiter.intruderowner@example.com", "candidate.owner@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 2},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]
    question_id = start_res.json()["data"]["questions"][0]["id"]

    intruder_token = _register(client, "candidate", "candidate.intruder@example.com")
    res = client.post(
        f"/api/v1/interviews/{interview_id}/answers",
        json={"question_id": question_id, "answer_text": "Sneaky answer."},
        headers=_auth(intruder_token),
    )
    assert res.status_code == 403


def test_full_report_after_completion(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.report@example.com", "candidate.report@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 2},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]
    questions = start_res.json()["data"]["questions"]

    for q in questions:
        client.post(
            f"/api/v1/interviews/{interview_id}/answers",
            json={"question_id": q["id"], "answer_text": "Experienced with Python, FastAPI, and PostgreSQL."},
            headers=_auth(candidate_token),
        )

    report_res = client.get(f"/api/v1/interviews/{interview_id}/report", headers=_auth(candidate_token))
    assert report_res.status_code == 200, report_res.text
    report = report_res.json()["data"]
    assert report["status"] == "completed"
    assert report["human_review_required"] is True
    assert report["evaluation"]["overall_score"] is not None
    assert len(report["questions"]) == 2
    assert all(q["answer_text"] for q in report["questions"])

    # Recruiter can view the same report.
    recruiter_view = client.get(f"/api/v1/interviews/{interview_id}/report", headers=_auth(recruiter_token))
    assert recruiter_view.status_code == 200


def test_recruiter_can_force_reevaluate(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.forceeval@example.com", "candidate.forceeval@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 1},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]
    question_id = start_res.json()["data"]["questions"][0]["id"]

    client.post(
        f"/api/v1/interviews/{interview_id}/answers",
        json={"question_id": question_id, "answer_text": "Python and FastAPI expert."},
        headers=_auth(candidate_token),
    )

    res = client.post(f"/api/v1/interviews/{interview_id}/evaluate", headers=_auth(recruiter_token))
    assert res.status_code == 200
    assert res.json()["data"]["overall_score"] is not None


def test_candidate_cannot_start_interview(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.candnostart@example.com", "candidate.candnostart@example.com"
    )
    res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id},
        headers=_auth(candidate_token),
    )
    assert res.status_code == 403


def test_non_owner_recruiter_cannot_view_interview(client):
    recruiter_token, candidate_token, job_id, candidate_id = _setup_application(
        client, "recruiter.viewowner@example.com", "candidate.viewowner@example.com"
    )
    start_res = client.post(
        "/api/v1/interviews",
        json={"candidate_id": candidate_id, "job_id": job_id, "num_questions": 1},
        headers=_auth(recruiter_token),
    )
    interview_id = start_res.json()["data"]["id"]

    other_recruiter_token = _register(client, "recruiter", "recruiter.viewintruder@example.com")
    res = client.get(f"/api/v1/interviews/{interview_id}", headers=_auth(other_recruiter_token))
    assert res.status_code == 403


# --- Speech-to-text: no provider configured in the test environment ---


def test_transcription_unavailable_without_provider(client):
    candidate_token = _register(client, "candidate", "candidate.speech@example.com")
    res = client.post(
        "/api/v1/speech/transcribe",
        headers=_auth(candidate_token),
        files={"file": ("answer.wav", b"fake-audio-bytes", "audio/wav")},
    )
    assert res.status_code == 503
    assert res.json()["error_code"] == "TRANSCRIPTION_UNAVAILABLE"


def test_recruiter_cannot_use_speech_endpoint(client):
    recruiter_token = _register(client, "recruiter", "recruiter.speech@example.com")
    res = client.post(
        "/api/v1/speech/transcribe",
        headers=_auth(recruiter_token),
        files={"file": ("answer.wav", b"fake-audio-bytes", "audio/wav")},
    )
    assert res.status_code == 403
