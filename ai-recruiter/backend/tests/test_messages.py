"""
Tests for Messaging & Chat endpoints between Candidates and Recruiters.
"""
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


def test_messaging_workflow_candidate_and_recruiter(client):
    # 1. Register Recruiter
    recruiter_token = _register(client, "recruiter", "recruiter.msg@example.com", name="Sarah Recruiter")
    rec_me = client.get("/api/v1/auth/me", headers=_auth(recruiter_token)).json()["data"]
    recruiter_id = rec_me["id"]

    # 2. Register Candidate
    candidate_token = _register(client, "candidate", "candidate.msg@example.com", name="Alex Candidate")
    cand_me = client.get("/api/v1/auth/me", headers=_auth(candidate_token)).json()["data"]
    candidate_id = cand_me["id"]

    # 3. Candidate sends message to Recruiter
    send1 = client.post(
        "/api/v1/messages/send",
        json={"receiver_id": recruiter_id, "content": "Hello Sarah, I am interested in your open position!"},
        headers=_auth(candidate_token),
    )
    assert send1.status_code == 201, send1.text
    assert send1.json()["data"]["content"] == "Hello Sarah, I am interested in your open position!"

    # 4. Recruiter checks unread count & thread
    unread_rec = client.get("/api/v1/messages/unread-count", headers=_auth(recruiter_token)).json()["data"]
    assert unread_rec["unread_count"] >= 1

    thread_rec = client.get(f"/api/v1/messages/thread/{candidate_id}", headers=_auth(recruiter_token))
    assert thread_rec.status_code == 200, thread_rec.text
    messages = thread_rec.json()["data"]
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello Sarah, I am interested in your open position!"

    # 5. Recruiter sends reply to Candidate staying in messenger
    send2 = client.post(
        "/api/v1/messages/send",
        json={"receiver_id": candidate_id, "content": "Hi Alex! Thanks for reaching out. Let's schedule a call."},
        headers=_auth(recruiter_token),
    )
    assert send2.status_code == 201, send2.text

    # 6. Candidate retrieves thread
    thread_cand = client.get(f"/api/v1/messages/thread/{recruiter_id}", headers=_auth(candidate_token))
    assert thread_cand.status_code == 200, thread_cand.text
    cand_messages = thread_cand.json()["data"]
    assert len(cand_messages) == 2
    assert cand_messages[1]["content"] == "Hi Alex! Thanks for reaching out. Let's schedule a call."

    # 7. Check conversations list for both candidate & recruiter
    convos_rec = client.get("/api/v1/messages/conversations", headers=_auth(recruiter_token))
    assert convos_rec.status_code == 200
    assert len(convos_rec.json()["data"]) >= 1

    convos_cand = client.get("/api/v1/messages/conversations", headers=_auth(candidate_token))
    assert convos_cand.status_code == 200
    assert len(convos_cand.json()["data"]) >= 1
