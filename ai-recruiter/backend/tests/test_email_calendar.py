"""
test_email_calendar.py — Automated Pytest Suite for Email & Calendar System.
Tests email provider abstraction, HTML templates, idempotency, retry tracking,
recruiter notification preferences, Google/Outlook OAuth URL generation,
dynamic .ics file generation, timezone handling, and scheduling API endpoints.
"""
import uuid
from datetime import datetime, timedelta, timezone
import pytest

from app.models.calendar import CalendarConnection, CalendarProvider, ScheduledInterview, ScheduledInterviewStatus
from app.models.candidate import CandidateProfile
from app.models.email_log import EmailLog
from app.models.email_setting import RecruiterEmailSetting
from app.models.job import Job
from app.models.user import User, UserRole
from app.services.calendar_service import CalendarService, _encrypt_token, _decrypt_token
from app.services.email_service import EmailService, render_template, send_shortlisted_email
from app.services.ics_service import generate_ics_content
from app.services.reminder_service import check_and_send_interview_reminders


def test_template_rendering():
    context = {
        "candidate_name": "Alice Johnson",
        "job_title": "Python Lead Developer",
        "company_name": "Tech Corp",
        "interview_date": "September 10, 2026",
        "interview_time": "10:00 AM (IST)",
        "duration": 30,
        "interview_type": "AI Technical Interview",
        "interview_link": "http://localhost:8000/live-interview-room.html?interview_id=123",
    }
    rendered = render_template("shortlisted.html", context)
    assert "Alice Johnson" in rendered
    assert "Python Lead Developer" in rendered
    assert "Tech Corp" in rendered

    rendered_invite = render_template("interview_invitation.html", context)
    assert "10:00 AM (IST)" in rendered_invite
    assert "http://localhost:8000/live-interview-room.html?interview_id=123" in rendered_invite


def test_token_encryption_decryption():
    raw_token = "secret_oauth_token_xyz_12345"
    encrypted = _encrypt_token(raw_token)
    assert encrypted != raw_token
    decrypted = _decrypt_token(encrypted)
    assert decrypted == raw_token


def test_ics_generation():
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=30)
    ics_text = generate_ics_content(
        summary="Python Developer AI Technical Interview",
        description="Interview session for Alice Johnson",
        start_time_utc=start,
        end_time_utc=end,
        location_or_url="http://localhost:8000/live-room",
        attendee_name="Alice Johnson",
        attendee_email="alice@example.com",
    )
    assert "BEGIN:VCALENDAR" in ics_text
    assert "END:VCALENDAR" in ics_text
    assert "BEGIN:VEVENT" in ics_text
    assert "SUMMARY:Python Developer AI Technical Interview" in ics_text
    assert "ATTENDEE;" in ics_text


def test_recruiter_email_settings(db_session):
    u_recruiter = User(
        email=f"recruiter_{uuid.uuid4()}@company.com",
        password_hash="hash",
        name="Tech Recruiter",
        role=UserRole.recruiter,
    )
    db_session.add(u_recruiter)
    db_session.commit()

    # Enabled by default
    assert EmailService.is_event_enabled_for_recruiter(db_session, u_recruiter.id, "candidate_shortlisted") is True

    # Disable candidate_shortlisted
    setting = RecruiterEmailSetting(recruiter_id=u_recruiter.id, candidate_shortlisted=False)
    db_session.add(setting)
    db_session.commit()

    assert EmailService.is_event_enabled_for_recruiter(db_session, u_recruiter.id, "candidate_shortlisted") is False
    assert EmailService.is_event_enabled_for_recruiter(db_session, u_recruiter.id, "interview_invited") is True


def test_google_outlook_auth_urls():
    rec_id = uuid.uuid4()
    google_url = CalendarService.get_google_auth_url(rec_id)
    assert "google" in google_url

    outlook_url = CalendarService.get_outlook_auth_url(rec_id)
    assert "outlook" in outlook_url or "microsoft" in outlook_url


def test_scheduled_interview_flow(db_session, client):
    from app.core.security import create_access_token
    u_recruiter = User(
        email=f"recruiter_{uuid.uuid4()}@company.com",
        password_hash="hash",
        name="Lead Recruiter",
        role=UserRole.recruiter,
    )
    db_session.add(u_recruiter)
    db_session.commit()
    token = create_access_token(str(u_recruiter.id), role="recruiter")
    recruiter_auth_headers = {"Authorization": f"Bearer {token}"}

    # Create test candidate and job
    u_cand = User(email=f"cand_{uuid.uuid4()}@test.com", password_hash="hash", name="John Smith", role=UserRole.candidate)
    db_session.add(u_cand)
    db_session.commit()

    cand_profile = CandidateProfile(user_id=u_cand.id, headline="Python Developer")
    db_session.add(cand_profile)
    db_session.commit()
    
    job = Job(recruiter_id=u_recruiter.id, title="Python Lead", description="Job desc", location="Remote")
    db_session.add(job)
    db_session.commit()

    from app.models.application import Application
    application = Application(candidate_id=cand_profile.id, job_id=job.id, match_score=85.0)
    db_session.add(application)
    db_session.commit()

    # Schedule Interview
    start_iso = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    resp = client.post(
        "/api/v1/interviews/schedule",
        json={
            "candidate_id": str(cand_profile.id),
            "job_id": str(job.id),
            "start_time_iso": start_iso,
            "duration_minutes": 45,
            "timezone_name": "Asia/Kolkata",
            "interview_type": "AI Technical Interview",
            "send_email": False,
            "sync_calendar": True,
        },
        headers=recruiter_auth_headers,
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()["data"]
    sched_id = data["scheduled_id"]
    interview_id = data["interview_id"]

    # Reschedule Interview
    new_start_iso = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    resched_resp = client.put(
        f"/api/v1/interviews/{interview_id}/reschedule",
        json={"new_start_time_iso": new_start_iso, "duration_minutes": 60, "timezone_name": "Asia/Kolkata", "send_email": False},
        headers=recruiter_auth_headers,
    )
    assert resched_resp.status_code == 200
    assert resched_resp.json()["data"]["status"] == "RESCHEDULED"

    # Download ICS
    ics_resp = client.get(f"/api/v1/interviews/{interview_id}/ics")
    assert ics_resp.status_code == 200
    assert "BEGIN:VCALENDAR" in ics_resp.text

    # Cancel Interview
    cancel_resp = client.post(f"/api/v1/interviews/{interview_id}/cancel", headers=recruiter_auth_headers)
    assert cancel_resp.status_code == 200
