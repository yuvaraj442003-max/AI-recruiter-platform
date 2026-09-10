"""
test_screening.py — Automated Unit & Integration Tests for AI Candidate Pre-Screening.
Tests question generation, natural language entity extraction, opt-out logic, and scoring.
"""
import pytest

from app.services.screening_ai_service import check_is_opt_out, extract_answer_structured, generate_job_questions
from app.services.screening_scoring_service import calculate_session_scores


def test_opt_out_detection():
    """Verify candidate opt-out keywords are detected accurately."""
    assert check_is_opt_out("STOP") is True
    assert check_is_opt_out("Please opt out") is True
    assert check_is_opt_out("unsubscribe me") is True
    assert check_is_opt_out("I have 4 years of experience in Python.") is False


def test_question_generation():
    """Test job-tailored question generation."""
    job_dict = {
        "title": "Senior Python Developer",
        "description": "Building FastAPI microservices with PostgreSQL and Docker.",
        "experience_required": 4.0,
        "location": "Chennai",
        "salary_range": "12-18 LPA",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    }

    questions = generate_job_questions(job_dict)
    assert len(questions) >= 4
    q_types = [q["question_type"] for q in questions]
    assert "experience" in q_types
    assert "location" in q_types
    assert "salary" in q_types


def test_answer_extraction_experience():
    """Test natural language answer extraction for experience question."""
    res = extract_answer_structured(
        question_text="How many years of Python experience do you have?",
        question_type="experience",
        expected_criteria="At least 3 years",
        candidate_answer="I have around 5 years of experience building Python backend APIs.",
        job_data={"experience_required": 3.0},
    )

    assert res["is_opt_out"] is False
    assert res["ai_score"] >= 80.0
    assert "experience_years" in res["extracted_value"] or res["ai_score"] > 50


def test_answer_extraction_location():
    """Test location willingness extraction."""
    res = extract_answer_structured(
        question_text="Are you willing to work from Chennai?",
        question_type="location",
        expected_criteria="Willing to work at Chennai",
        candidate_answer="Yes, I am comfortable relocating to Chennai.",
    )

    assert res["ai_score"] >= 90.0
    assert res["extracted_value"].get("location_confirmed") is True


class DummyQuestion:
    def __init__(self, q_id, q_type):
        self.id = q_id
        self.question_type = q_type


class DummyAnswer:
    def __init__(self, q_id, candidate_answer, ai_score, ai_reason=""):
        self.screening_question_id = q_id
        self.candidate_answer = candidate_answer
        self.ai_score = ai_score
        self.ai_reason = ai_reason


class DummySession:
    def __init__(self, questions, answers):
        self.questions = questions
        self.answers = answers


def test_scoring_engine_calculation():
    """Test deterministic weighted scoring engine."""
    q1 = DummyQuestion("q1", "technical")
    q2 = DummyQuestion("q2", "experience")
    q3 = DummyQuestion("q3", "location")
    q4 = DummyQuestion("q4", "notice_period")
    q5 = DummyQuestion("q5", "salary")

    a1 = DummyAnswer("q1", "I know Python and FastAPI very well.", 95.0, "Skills confirmed")
    a2 = DummyAnswer("q2", "I have 5 years experience.", 90.0, "Experience confirmed")
    a3 = DummyAnswer("q3", "Yes, Chennai is fine.", 100.0, "Location confirmed")
    a4 = DummyAnswer("q4", "30 days notice.", 85.0, "30 days notice")
    a5 = DummyAnswer("q5", "15 LPA expected.", 85.0, "Salary acceptable")

    session = DummySession([q1, q2, q3, q4, q5], [a1, a2, a3, a4, a5])
    result = calculate_session_scores(session)

    assert result["overall_score"] >= 85.0
    assert result["recommendation"] == "Strong Match"
    assert "technical_score" in result
    assert "experience_score" in result
