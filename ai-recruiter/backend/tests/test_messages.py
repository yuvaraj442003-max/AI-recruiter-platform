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


def test_audio_message_workflow(client):
    recruiter_token = _register(client, "recruiter", "recruiter.audio@example.com", name="Voice Recruiter")
    candidate_token = _register(client, "candidate", "candidate.audio@example.com", name="Voice Candidate")

    cand_me = client.get("/api/v1/auth/me", headers=_auth(candidate_token)).json()["data"]
    rec_me = client.get("/api/v1/auth/me", headers=_auth(recruiter_token)).json()["data"]

    # Candidate uploads dummy audio file
    fake_audio = b"RIFF....WAVEfmt ....data........"
    res_audio = client.post(
        "/api/v1/messages/send-audio",
        data={"receiver_id": rec_me["id"]},
        files={"file": ("voice_note.webm", fake_audio, "audio/webm")},
        headers=_auth(candidate_token),
    )
    assert res_audio.status_code == 201, res_audio.text
    data = res_audio.json()["data"]
    assert data["is_audio"] is True
    assert data["audio_url"].startswith("/uploads/audio_messages/")

    # Recruiter reads thread
    thread = client.get(f"/api/v1/messages/thread/{cand_me['id']}", headers=_auth(recruiter_token))
    assert thread.status_code == 200
    msgs = thread.json()["data"]
    assert len(msgs) == 1
    assert msgs[0]["is_audio"] is True
    assert msgs[0]["audio_url"] == data["audio_url"]


def test_delete_and_edit_messages(client):
    recruiter_token = _register(client, "recruiter", "recruiter.edit@example.com", name="Edit Recruiter")
    candidate_token = _register(client, "candidate", "candidate.edit@example.com", name="Edit Candidate")

    cand_me = client.get("/api/v1/auth/me", headers=_auth(candidate_token)).json()["data"]
    rec_me = client.get("/api/v1/auth/me", headers=_auth(recruiter_token)).json()["data"]

    # 1. Candidate sends text message
    send1 = client.post(
        "/api/v1/messages/send",
        json={"receiver_id": rec_me["id"], "content": "Original message text"},
        headers=_auth(candidate_token),
    )
    assert send1.status_code == 201
    msg_id = send1.json()["data"]["id"]

    # 2. Candidate edits message
    edit_res = client.put(
        f"/api/v1/messages/{msg_id}",
        json={"content": "Updated message text"},
        headers=_auth(candidate_token),
    )
    assert edit_res.status_code == 200
    assert edit_res.json()["data"]["content"] == "Updated message text"

    # 3. Candidate sends audio message and attempts to edit it
    fake_audio = b"RIFF....WAVEfmt ....data........"
    res_audio = client.post(
        "/api/v1/messages/send-audio",
        data={"receiver_id": rec_me["id"]},
        files={"file": ("voice_note.webm", fake_audio, "audio/webm")},
        headers=_auth(candidate_token),
    )
    assert res_audio.status_code == 201
    audio_msg_id = res_audio.json()["data"]["id"]

    audio_edit_res = client.put(
        f"/api/v1/messages/{audio_msg_id}",
        json={"content": "Attempt edit audio"},
        headers=_auth(candidate_token),
    )
    assert audio_edit_res.status_code == 400

    # 4. Candidate deletes both messages
    del1 = client.delete(f"/api/v1/messages/{msg_id}", headers=_auth(candidate_token))
    assert del1.status_code == 200

    del2 = client.delete(f"/api/v1/messages/{audio_msg_id}", headers=_auth(candidate_token))
    assert del2.status_code == 200

    # 5. Verify thread is now empty
    thread = client.get(f"/api/v1/messages/thread/{cand_me['id']}", headers=_auth(recruiter_token))
    assert thread.status_code == 200
    assert len(thread.json()["data"]) == 0


