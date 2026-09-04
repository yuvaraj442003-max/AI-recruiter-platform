"""
test_resume_form_mismatch.py — Unit tests for strict email validation and Candidate Form vs Resume Mismatch blocking.
"""
import pytest
from app.utils.email_validation import validate_strict_email
from app.services.resume_verification_service import verify_resume_against_form
from app.core.exceptions import AppError


def test_strict_email_validation_valid():
    assert validate_strict_email("candidate@example.com") == "candidate@example.com"
    assert validate_strict_email("user.name+tag@techcorp.co.in") == "user.name+tag@techcorp.co.in"


def test_strict_email_validation_invalid():
    invalid_emails = [
        "user@test",
        "user@localhost",
        "user@@domain.com",
        "invalid-email",
        "user@.com",
        "user@domain..com",
        "user@example",
    ]
    for email in invalid_emails:
        with pytest.raises(AppError) as exc_info:
            validate_strict_email(email)
        assert exc_info.value.status_code == 400


def test_verify_resume_against_form_matching():
    fields = {
        "name": "Alice Johnson",
        "phone": "+1 (555) 123-4567",
        "experience_years": 4.0,
        "skills": ["Python", "FastAPI", "SQL"],
        "resume_text": "Alice Johnson. Phone: 555-123-4567. 4 years of software development in Python, FastAPI, SQL.",
    }
    form_data = {
        "name": "Alice Johnson",
        "phone": "+1 555-123-4567",
        "experience_years": 4.0,
        "skills": ["Python", "SQL"],
    }
    is_valid, mismatches = verify_resume_against_form(fields, form_data)
    assert is_valid is True
    assert len(mismatches) == 0


def test_verify_resume_against_form_phone_mismatch():
    fields = {
        "name": "Alice Johnson",
        "phone": "+1 (555) 999-8888",
        "experience_years": 4.0,
        "skills": ["Python", "SQL"],
        "resume_text": "Alice Johnson. Phone: 555-999-8888.",
    }
    form_data = {
        "name": "Alice Johnson",
        "phone": "+1 (555) 123-4567",  # Mismatched phone
        "experience_years": 4.0,
        "skills": ["Python", "SQL"],
    }
    is_valid, mismatches = verify_resume_against_form(fields, form_data)
    assert is_valid is False
    assert any("Phone Number Mismatch" in m for m in mismatches)


def test_verify_resume_against_form_skills_mismatch():
    fields = {
        "name": "Bob Smith",
        "phone": "+1 (555) 123-4567",
        "skills": ["Figma", "Adobe Photoshop", "UI UX Design"],
        "resume_text": "Bob Smith UI UX Designer skilled in Figma and Photoshop.",
    }
    form_data = {
        "name": "Bob Smith",
        "phone": "+1 (555) 123-4567",
        "skills": ["Java", "Spring Boot", "Kubernetes"],  # Completely mismatched skills
    }
    is_valid, mismatches = verify_resume_against_form(fields, form_data)
    assert is_valid is False
    assert any("Key Skills Mismatch" in m for m in mismatches)


def test_verify_resume_against_form_name_mismatch():
    fields = {
        "name": "Charlie Brown",
        "phone": "+1 (555) 123-4567",
        "skills": ["Python"],
        "resume_text": "Charlie Brown Resume",
    }
    form_data = {
        "name": "David Williams",  # Contradicting candidate name
        "phone": "+1 (555) 123-4567",
        "skills": ["Python"],
    }
    is_valid, mismatches = verify_resume_against_form(fields, form_data)
    assert is_valid is False
    assert any("Candidate Name Mismatch" in m for m in mismatches)
