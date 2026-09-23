import json
import uuid
import pytest
from app.models.proctoring import AssessmentConsent, AssessmentEvent, EventSeverity, IntegrityResult, RiskLevel
from app.models.interview import Interview, InterviewType, InterviewStatus
from app.models.job import Job
from app.models.candidate import CandidateProfile
from app.models.user import User, UserRole
from app.services.integrity_scoring_service import calculate_interview_integrity, PENALTY_RULES


def test_penalty_rules_completeness():
    assert "NO_FACE_DETECTED" in PENALTY_RULES
    assert "MULTIPLE_FACES_DETECTED" in PENALTY_RULES
    assert "TAB_SWITCH" in PENALTY_RULES
    assert "COPY_ATTEMPT" in PENALTY_RULES
    assert "PASTE_ATTEMPT" in PENALTY_RULES
    assert "HIGH_AUDIO_SPIKE" in PENALTY_RULES


def test_calculate_interview_integrity_clean(db_session):
    # Setup user & candidate
    user = User(
        email=f"candidate_test_{uuid.uuid4().hex[:6]}@example.com",
        password_hash="test",
        name="Interview Candidate",
        role=UserRole.candidate,
    )
    db_session.add(user)
    db_session.flush()

    candidate = CandidateProfile(user_id=user.id, summary="Python Developer")
    db_session.add(candidate)

    recruiter = User(
        email=f"recruiter_test_{uuid.uuid4().hex[:6]}@example.com",
        password_hash="test",
        name="Recruiter Admin",
        role=UserRole.recruiter,
    )
    db_session.add(recruiter)
    db_session.flush()

    job = Job(title="Software Engineer", description="Full stack software engineer", recruiter_id=recruiter.id)
    db_session.add(job)
    db_session.flush()

    interview = Interview(
        candidate_id=candidate.id,
        job_id=job.id,
        interview_type=InterviewType.ai_interview,
        status=InterviewStatus.in_progress,
    )
    db_session.add(interview)
    db_session.commit()

    # Calculate integrity with zero infractions
    res = calculate_interview_integrity(db_session, str(interview.id))
    assert res.overall_integrity_score == 100.0
    assert res.risk_level == RiskLevel.low_risk
    assert "No suspicious activity" in res.ai_summary

    # Add infractions
    ev1 = AssessmentEvent(
        interview_id=interview.id,
        candidate_id=candidate.id,
        event_type="TAB_SWITCH",
        severity=EventSeverity.medium,
        confidence=1.0,
    )
    ev2 = AssessmentEvent(
        interview_id=interview.id,
        candidate_id=candidate.id,
        event_type="NO_FACE_DETECTED",
        severity=EventSeverity.medium,
        confidence=0.9,
    )
    db_session.add_all([ev1, ev2])
    db_session.commit()

    res2 = calculate_interview_integrity(db_session, str(interview.id))
    assert res2.overall_integrity_score < 100.0
    assert "Tab switches detected" in res2.ai_summary
    assert "Face absence detected" in res2.ai_summary
