"""
test_ai_aptitude_generator.py — Comprehensive automated test suite for AI-Based Aptitude Question Generator:
- AI Question Generation (Topics, Options, 1 Correct Answer, Explanations, Validation)
- Recruiter Test Generation & Draft Status
- Recruiter Question Studio (Edit Question, Delete Question, Regenerate Question)
- Approval and Test Publishing
- Candidate Assessment: Start Session, Secure Option Display (No Correct Answers Leaked)
- Automatic Server-Side Evaluation, Anti-Cheat Scoring, and Full Explanations Review
- Role-Based Access Control (Candidate forbidden from generating/publishing)
- Recruiter Assessment Results View
"""
import json
import uuid
import pytest
from app.core.security import create_access_token
from app.models.student import (
    AptitudeTest,
    AptitudeQuestion,
    AptitudeOption,
    CandidateTestAttempt,
    CandidateAnswer,
    AptitudeTestResult,
)
from app.models.user import User, UserRole
from app.services.ai_aptitude_service import (
    generate_aptitude_questions_ai,
    regenerate_single_question_ai,
)


@pytest.fixture
def recruiter_user(db_session):
    recruiter = db_session.query(User).filter(User.email == "aptitude_recruiter@example.com").first()
    if not recruiter:
        recruiter = User(
            email="aptitude_recruiter@example.com",
            password_hash="hashedpass123",
            name="Sarah Recruiter",
            role=UserRole.recruiter,
        )
        db_session.add(recruiter)
        db_session.commit()
        db_session.refresh(recruiter)
    return recruiter


@pytest.fixture
def recruiter_headers(recruiter_user):
    token = create_access_token(str(recruiter_user.id), role=recruiter_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def candidate_user(db_session):
    candidate = db_session.query(User).filter(User.email == "aptitude_candidate@example.com").first()
    if not candidate:
        candidate = User(
            email="aptitude_candidate@example.com",
            password_hash="hashedpass123",
            name="Rohan Sharma",
            role=UserRole.candidate,
        )
        db_session.add(candidate)
        db_session.commit()
        db_session.refresh(candidate)
    return candidate


@pytest.fixture
def candidate_headers(candidate_user):
    token = create_access_token(str(candidate_user.id), role=candidate_user.role)
    return {"Authorization": f"Bearer {token}"}


# ==============================================================================
# 1. AI GENERATION ENGINE DIRECT TESTS
# ==============================================================================

def test_ai_generator_engine_structure():
    """Validates that the AI generation engine produces valid MCQs strictly adhering to requirements."""
    topics = ["Percentages", "Profit and Loss", "Time and Work"]
    questions = generate_aptitude_questions_ai(
        topics=topics,
        num_questions=5,
        difficulty="mixed",
        marks_per_question=2.0,
    )

    assert len(questions) == 5
    for q in questions:
        assert q.topic_name in topics or any(t.lower() in q.topic_name.lower() for t in topics)
        assert len(q.options) == 4, "Every question must have exactly 4 options"
        assert 0 <= q.correct_option_index <= 3, "correct_option_index must be 0, 1, 2, or 3"
        assert len(set(q.options)) == 4, "All 4 options must be distinct"
        assert len(q.explanation.strip()) > 10, "A clear explanation must be provided"
        assert q.marks == 2.0


def test_regenerate_single_question_engine():
    """Validates single question regeneration."""
    item = regenerate_single_question_ai(
        topic="Logical Reasoning",
        difficulty="hard",
        marks_per_question=1.5,
    )
    assert len(item.options) == 4
    assert 0 <= item.correct_option_index <= 3
    assert item.difficulty == "hard"
    assert item.marks == 1.5
    assert len(item.explanation) > 10


# ==============================================================================
# 2. RECRUITER TEST GENERATION & RBAC
# ==============================================================================

def test_recruiter_generate_test_endpoint(client, recruiter_headers):
    """Recruiter successfully generates a draft aptitude test via API."""
    payload = {
        "title": "Placement Aptitude Assessment 2026",
        "topics": ["Percentages", "Profit and Loss", "Logical Reasoning"],
        "num_questions": 5,
        "difficulty": "medium",
        "duration_minutes": 15,
        "marks_per_question": 2.0,
    }

    response = client.post("/api/v1/aptitude/generate", json=payload, headers=recruiter_headers)
    assert response.status_code == 200, response.text
    res_data = response.json()
    assert res_data["success"] is True

    test_data = res_data["data"]
    assert test_data["title"] == "Placement Aptitude Assessment 2026"
    assert test_data["status"] == "draft", "Test must be generated in draft status, requiring recruiter review"
    assert test_data["total_questions"] == 5
    assert test_data["total_marks"] == 10.0
    assert len(test_data["questions"]) == 5

    # Check first question structure
    q0 = test_data["questions"][0]
    assert len(q0["options"]) == 4
    assert 0 <= q0["correct_option_index"] <= 3
    assert q0["explanation"] is not None
    # Check option letters
    letters = [opt["option_letter"] for opt in q0["options"]]
    assert letters == ["A", "B", "C", "D"]
    assert sum(1 for opt in q0["options"] if opt["is_correct"]) == 1


def test_dual_prefix_route_compatibility(client, recruiter_headers):
    """Verifies that /api/aptitude/generate works equivalently to /api/v1/aptitude/generate."""
    payload = {
        "title": "Prefix Test",
        "topics": ["Number Series"],
        "num_questions": 5,
        "difficulty": "easy",
        "marks_per_question": 1.0,
    }
    response = client.post("/api/aptitude/generate", json=payload, headers=recruiter_headers)
    assert response.status_code == 200, response.text
    assert response.json()["success"] is True


def test_candidate_cannot_generate_test(client, candidate_headers):
    """Candidate should receive 403 Forbidden when attempting to generate tests."""
    payload = {
        "title": "Unauthorized Test",
        "topics": ["Percentages"],
        "num_questions": 5,
    }
    response = client.post("/api/v1/aptitude/generate", json=payload, headers=candidate_headers)
    assert response.status_code == 403


# ==============================================================================
# 3. QUESTION STUDIO: EDIT, DELETE, REGENERATE, PUBLISH
# ==============================================================================

def test_question_studio_lifecycle(client, recruiter_headers, db_session):
    """Full lifecycle: Generate -> Edit Question -> Regenerate Question -> Delete Question -> Publish."""
    # 1. Generate test with 5 questions
    payload = {
        "title": "Studio Lifecycle Test",
        "topics": ["Time and Work", "Probability"],
        "num_questions": 5,
        "difficulty": "medium",
        "marks_per_question": 2.0,
    }
    gen_resp = client.post("/api/v1/aptitude/generate", json=payload, headers=recruiter_headers)
    assert gen_resp.status_code == 200
    test_data = gen_resp.json()["data"]
    test_id = test_data["id"]
    q1 = test_data["questions"][0]
    q2 = test_data["questions"][1]

    # 2. Edit Question 1
    edit_payload = {
        "question": "Modified: If 6 workers take 12 days, how long do 9 workers take?",
        "options": ["6 days", "8 days", "10 days", "12 days"],
        "correct_option_index": 1,
        "explanation": "Work = 6 * 12 = 72 man-days. Days for 9 workers = 72 / 9 = 8 days.",
        "difficulty": "medium",
    }
    edit_resp = client.put(f"/api/v1/aptitude/questions/{q1['id']}", json=edit_payload, headers=recruiter_headers)
    assert edit_resp.status_code == 200
    q1_updated = edit_resp.json()["data"]
    assert "Modified" in q1_updated["question"]
    assert q1_updated["correct_option_index"] == 1
    assert q1_updated["options"][1]["is_correct"] is True

    # 3. Regenerate Question 2
    regen_resp = client.post(f"/api/v1/aptitude/questions/{q2['id']}/regenerate", headers=recruiter_headers)
    assert regen_resp.status_code == 200
    q2_regen = regen_resp.json()["data"]
    assert len(q2_regen["options"]) == 4
    assert 0 <= q2_regen["correct_option_index"] <= 3

    # 4. Delete Question 3
    q3 = test_data["questions"][2]
    del_resp = client.delete(f"/api/v1/aptitude/questions/{q3['id']}", headers=recruiter_headers)
    assert del_resp.status_code == 200
    del_data = del_resp.json()["data"]
    assert del_data["remaining_questions"] == 4
    assert del_data["total_marks"] == 8.0

    # 5. Publish Test
    pub_resp = client.post(f"/api/v1/aptitude/tests/{test_id}/publish", headers=recruiter_headers)
    assert pub_resp.status_code == 200
    published_test = pub_resp.json()["data"]
    assert published_test["status"] == "published"
    assert published_test["total_questions"] == 4


# ==============================================================================
# 4. CANDIDATE ASSESSMENT & SERVER-SIDE EVALUATION
# ==============================================================================

def test_candidate_test_taking_and_evaluation(client, recruiter_headers, candidate_headers, db_session):
    """
    Candidate takes published test:
    - Verifies NO correct answers or explanations are leaked in the taking payload.
    - Submits answers and checks server-side scoring.
    - Confirms full review and explanations are provided only AFTER submission.
    """
    # 1. Recruiter creates and publishes test
    payload = {
        "title": "Candidate Analytical Exam",
        "topics": ["Percentages", "Data Interpretation"],
        "num_questions": 5,
        "difficulty": "easy",
        "duration_minutes": 10,
        "marks_per_question": 2.0,
    }
    gen_resp = client.post("/api/v1/aptitude/generate", json=payload, headers=recruiter_headers)
    test_id = gen_resp.json()["data"]["id"]
    client.post(f"/api/v1/aptitude/tests/{test_id}/publish", headers=recruiter_headers)

    # 2. Candidate starts test
    start_resp = client.post(f"/api/v1/aptitude/tests/{test_id}/start", headers=candidate_headers)
    assert start_resp.status_code == 200, start_resp.text
    session_data = start_resp.json()["data"]
    attempt_id = session_data["attempt_id"]
    assert session_data["total_questions"] == 5
    assert session_data["remaining_seconds"] > 0

    # Verify SECURITY: No correct answer or explanation leaked to candidate
    for q in session_data["questions"]:
        assert "explanation" not in q or q.get("explanation") is None
        assert "correct_option_index" not in q
        for opt in q["options"]:
            assert "is_correct" not in opt

    # 3. Fetch actual questions from DB to simulate 1 correct and 1 wrong answer
    db_questions = db_session.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == uuid.UUID(test_id)).all()
    assert len(db_questions) == 5

    q0 = db_questions[0]
    q1 = db_questions[1]

    # Select correct option for q0, and strictly wrong option for q1
    q0_corr = q0.correct_option_index
    q1_wrong = (q1.correct_option_index + 1) % 4
    letters = ["A", "B", "C", "D"]
    answers_payload = [
        {
            "question_id": str(q0.id),
            "selected_option_index": q0_corr,
            "selected_option_letter": letters[q0_corr],
        },
        {
            "question_id": str(q1.id),
            "selected_option_index": q1_wrong,
            "selected_option_letter": letters[q1_wrong],
        },
    ]

    # 4. Candidate submits test
    submit_payload = {
        "attempt_id": attempt_id,
        "answers": answers_payload,
        "time_taken_seconds": 120,
    }
    sub_resp = client.post(f"/api/v1/aptitude/tests/{test_id}/submit", json=submit_payload, headers=candidate_headers)
    assert sub_resp.status_code == 200, sub_resp.text
    eval_result = sub_resp.json()["data"]

    # Verify score: q0 correct (2 marks), q1 wrong (0 marks), remaining 3 unanswered
    assert eval_result["correct_count"] == 1
    assert eval_result["wrong_count"] == 1
    assert eval_result["unanswered_count"] == 3
    assert eval_result["score"] == 2.0
    assert eval_result["total_marks"] == 10.0
    assert eval_result["percentage"] == 20.0
    assert eval_result["passed"] is False  # cutoff is 60%
    assert eval_result["feedback_message"] is not None

    # Verify that explanations ARE now provided in post-submission review
    assert len(eval_result["review_items"]) == 5
    for rev in eval_result["review_items"]:
        assert rev["explanation"] is not None
        assert rev["correct_option_letter"] in ["A", "B", "C", "D"]

    # 5. Recruiter views test results
    results_resp = client.get(f"/api/v1/aptitude/tests/{test_id}/results", headers=recruiter_headers)
    assert results_resp.status_code == 200
    attempts_list = results_resp.json()["data"]
    assert len(attempts_list) == 1
    assert attempts_list[0]["score"] == 2.0
    assert attempts_list[0]["candidate_email"] == "aptitude_candidate@example.com"
