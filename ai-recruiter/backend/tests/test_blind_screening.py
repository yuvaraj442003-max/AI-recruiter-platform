"""
test_blind_screening.py — Automated Unit & Integration Tests for Blind Screening Mode.
Tests candidate code generation, university/institution sanitization, resume text PII scrubbing,
sanitized AI prompt generation, and BlindCandidate anonymization guarantees.
"""
import uuid
import pytest
from app.services.blind_resume_service import (
    generate_candidate_code,
    sanitize_education_text,
    sanitize_resume_text,
    build_sanitized_ai_prompt,
)
from app.schemas.blind_screening import BlindCandidateOut, EducationSanitizedItem


def test_generate_candidate_code():
    """Verify non-identifying candidate code generation is formatted and repeatable for same candidate ID + job ID."""
    cand_id = uuid.UUID("12345678-1234-5678-1234-567812345678")
    job_id = uuid.UUID("87654321-4321-8765-4321-876543218765")
    code1 = generate_candidate_code(cand_id, job_id)
    code2 = generate_candidate_code(cand_id, job_id)

    assert code1.startswith("CAND-")
    assert code1 == code2  # Repeatable for same candidate ID and job ID
    assert len(code1) == 10  # CAND-XXXXX (5 digits)


def test_sanitize_education_text():
    """Verify university/college names are masked into degree & field of study pairs."""
    raw_edu = "Bachelor of Technology in Computer Science from Anna University, Chennai"
    sanitized_items = sanitize_education_text(raw_edu)

    assert isinstance(sanitized_items, list)
    assert len(sanitized_items) > 0
    item = sanitized_items[0]
    assert "degree" in item
    assert "field" in item
    # Ensure raw university name is not in the output
    assert "Anna University" not in item["degree"]
    assert "Anna University" not in item["field"]


def test_sanitize_resume_text_redacts_pii():
    """Verify emails, phone numbers, URLs, and university names are redacted from resume text."""
    raw_resume = (
        "John Doe\n"
        "Email: john.doe@example.com, Phone: +91 9876543210\n"
        "Graduated from Indian Institute of Technology Madras with a B.Tech in Electrical Engineering.\n"
        "LinkedIn: https://linkedin.com/in/johndoe\n"
        "Proficient in Python, FastApi, PostgreSQL, and Machine Learning."
    )

    sanitized = sanitize_resume_text(
        raw_resume,
        candidate_name="John Doe",
        email="john.doe@example.com",
        phone="+91 9876543210",
    )

    # Sensitive identity items must be scrubbed
    assert "john.doe@example.com" not in sanitized
    assert "+91 9876543210" not in sanitized
    assert "https://linkedin.com/in/johndoe" not in sanitized
    assert "[REDACTED" in sanitized or "Accredited Higher Education Institution" in sanitized

    # Skill content must remain intact
    assert "Python" in sanitized
    assert "FastApi" in sanitized
    assert "PostgreSQL" in sanitized


def test_build_sanitized_ai_prompt():
    """Verify AI prompt contains only anonymized code and scrubbed resume text."""
    cand_code = "CAND-99999"
    prompt_dict = build_sanitized_ai_prompt(
        candidate_code=cand_code,
        experience_years=5.0,
        skills=["React.js", "Node.js"],
        work_exp_summary="Built scalable web apps",
        job_title="Senior Frontend Engineer"
    )

    assert prompt_dict["candidate_code"] == "CAND-99999"
    assert prompt_dict["experience_years"] == 5.0
    assert "React.js" in prompt_dict["normalized_skills"]
    assert prompt_dict["target_job"] == "Senior Frontend Engineer"


def test_blind_candidate_out_schema_fields():
    """Verify BlindCandidateOut DTO enforces anonymized fields."""
    dto_data = {
        "candidate_code": "CAND-12345",
        "job_id": str(uuid.uuid4()),
        "experience_years": 4.5,
        "skills": ["Python", "FastAPI"],
        "ats_score": 85.5,
        "role_match_score": 88.0,
        "skills_match": 90.0,
        "experience_match": 85.0,
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["Docker"],
        "education": [
            {"degree": "Bachelor's Degree", "field": "Computer Science"}
        ],
        "sanitized_resume_summary": "Experienced backend developer",
        "screening_status": "pending",
        "recruiter_decision": "shortlist",
        "revealed": False,
    }

    obj = BlindCandidateOut(**dto_data)
    assert obj.candidate_code == "CAND-12345"
    assert obj.ats_score == 85.5
    assert obj.education[0].degree == "Bachelor's Degree"
    assert obj.education[0].field == "Computer Science"

    # Verify PII attributes strictly do NOT exist on BlindCandidateOut DTO
    assert not hasattr(obj, "candidate_name")
    assert not hasattr(obj, "email")
    assert not hasattr(obj, "phone")
    assert not hasattr(obj, "photo")
    assert not hasattr(obj, "exact_location")
    assert not hasattr(obj, "college_name")
