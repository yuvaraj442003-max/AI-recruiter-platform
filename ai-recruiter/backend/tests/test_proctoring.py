"""
test_proctoring.py — Automated Unit & Integration Tests for AI-Assisted Proctored Assessment & Integrity Monitoring.
Tests multi-language AST code similarity analysis, token normalization, and evidence-based integrity scoring.
"""
import pytest

from app.services.code_similarity_service import compare_code_pair, normalize_code, remove_comments_and_docstrings
from app.services.integrity_scoring_service import calculate_attempt_integrity


def test_remove_comments_and_docstrings():
    """Verify comments and docstrings are removed correctly."""
    python_code = "# This is a comment\ndef foo():\n    \"\"\"Docstring\"\"\"\n    return 42"
    clean = remove_comments_and_docstrings(python_code, "python")
    assert "# This is a comment" not in clean
    assert '"""Docstring"""' not in clean
    assert "def foo():" in clean


def test_normalize_code_variable_renaming():
    """Verify identifier normalization renames local variables consistently."""
    code1 = "def calculate_total(price, tax):\n    subtotal = price * tax\n    return subtotal"
    code2 = "def compute_sum(val, rate):\n    res = val * rate\n    return res"

    norm1 = normalize_code(code1, "python")
    norm2 = normalize_code(code2, "python")

    # Identifiers should be mapped to generic tokens VAR_0, VAR_1 etc.
    assert "VAR_" in norm1
    assert "VAR_" in norm2


def test_code_similarity_variable_renamed():
    """Test AST & Token hybrid similarity engine on renamed variable code."""
    code1 = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
"""

    code2 = """
# Candidate solution
def solve(arr, val):
    lookup = {}
    for index, item in enumerate(arr):
        remainder = val - item
        if remainder in lookup:
            return [lookup[remainder], index]
        lookup[item] = index
    return []
"""

    score, summary = compare_code_pair(code1, code2, "python")
    assert score >= 50.0
    assert "similarity" in summary.lower()


def test_code_similarity_distinct():
    """Test that distinct algorithm solutions return low similarity."""
    code1 = "def is_even(n):\n    return n % 2 == 0"
    code2 = "def quicksort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)"

    score, summary = compare_code_pair(code1, code2, "python")
    assert score < 40.0


def test_integrity_scoring_camera_and_audio_violations(db_session):
    """Verify integrity scoring correctly calculates deductions for MULTIPLE_FACES and NOISE_DETECTED events."""
    from app.models.coding import CandidateCodingAttempt, CodingAssessment
    from app.models.candidate import CandidateProfile
    from app.models.user import User, UserRole
    from app.models.proctoring import AssessmentEvent, EventSeverity
    from app.services.integrity_scoring_service import calculate_attempt_integrity
    import uuid

    # Create user & candidate profile
    test_user = User(
        id=uuid.uuid4(),
        email=f"test_proc_{uuid.uuid4().hex[:6]}@example.com",
        password_hash="hashed_pass_123",
        name="Test Proctor Candidate",
        role=UserRole.candidate,
    )
    db_session.add(test_user)
    db_session.commit()

    candidate = CandidateProfile(id=uuid.uuid4(), user_id=test_user.id)
    db_session.add(candidate)
    db_session.commit()

    assessment = CodingAssessment(
        id=uuid.uuid4(),
        title="Test Proctoring Assessment",
        description="Assessment",
        duration_minutes=60,
    )
    db_session.add(assessment)
    db_session.commit()

    attempt = CandidateCodingAttempt(
        id=uuid.uuid4(),
        candidate_id=candidate.id,
        assessment_id=assessment.id,
        status="in_progress",
    )
    db_session.add(attempt)
    db_session.commit()

    # Record MULTIPLE_FACES and NOISE_DETECTED events
    ev1 = AssessmentEvent(
        id=uuid.uuid4(),
        attempt_id=attempt.id,
        candidate_id=candidate.id,
        event_type="MULTIPLE_FACES",
        severity=EventSeverity.high,
        confidence=0.95,
    )
    ev2 = AssessmentEvent(
        id=uuid.uuid4(),
        attempt_id=attempt.id,
        candidate_id=candidate.id,
        event_type="NOISE_DETECTED",
        severity=EventSeverity.medium,
        confidence=0.90,
    )
    db_session.add_all([ev1, ev2])
    db_session.commit()

    # Calculate integrity
    result = calculate_attempt_integrity(db_session, str(attempt.id))

    assert result.webcam_score == 75.0  # 100 - 25
    assert result.audio_score == 90.0   # 100 - 10
    assert "Multiple faces detected on webcam" in result.ai_summary
    assert "External background noise or suspicious audio detected" in result.ai_summary

