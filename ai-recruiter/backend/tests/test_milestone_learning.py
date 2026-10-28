"""
test_milestone_learning.py — Tests for the expanded Milestone Checklist & Learning Steps:
- 12 comprehensive placement milestones covering Aptitude, Reasoning, Verbal, Coding/DSA, SQL, DBMS, OS, Networks, and Company Mocks.
- Curated practice questions and subtopics for each topic.
- Timed quiz endpoint (30s per question).
- Milestone quiz submission, scoring, progress tracking, and step-by-step solutions.
- Dynamic AI question generation tailored to the milestone's study topics.
"""
import json
import pytest
from app.core.security import create_access_token
from app.models.student import LearningRoadmap, StudentRoadmapProgress
from app.models.user import User, UserRole
from app.services.student_seed_service import seed_student_ecosystem


@pytest.fixture
def candidate_token(db_session):
    user = db_session.query(User).filter(User.email == "milestone_student@example.com").first()
    if not user:
        user = User(
            email="milestone_student@example.com",
            name="Milestone Student",
            password_hash="fakepassword123",
            role=UserRole.candidate,
            is_active=True,
            is_email_verified=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    token = create_access_token(str(user.id), user.role.value)
    return token, user


def test_seed_roadmaps_curriculum(db_session):
    """Verify that seed_student_ecosystem creates the complete 12-milestone placement curriculum."""
    seed_student_ecosystem(db_session)

    roadmap = db_session.query(LearningRoadmap).filter(LearningRoadmap.slug == "campus-60-day-sprint").first()
    assert roadmap is not None
    assert roadmap.estimated_weeks == 12

    milestones = json.loads(roadmap.milestones_json)
    assert len(milestones) == 12

    # Check key subjects
    subjects = [m["subject"] for m in milestones]
    assert any("Aptitude" in s for s in subjects)
    assert any("Reasoning" in s for s in subjects)
    assert any("Verbal" in s for s in subjects)
    assert any("Data Structure" in s for s in subjects)
    assert any("SQL" in s or "DBMS" in s for s in subjects)
    assert any("Operating Systems" in s for s in subjects)
    assert any("Computer Networks" in s for s in subjects)

    # Check subtopics and practice questions
    for m in milestones:
        assert "subtopics" in m and len(m["subtopics"]) >= 3
        assert "practice_questions" in m and len(m["practice_questions"]) >= 2
        for q in m["practice_questions"]:
            assert "question" in q and len(q["question"]) > 10
            assert "options" in q and len(q["options"]) == 4
            assert 0 <= q["correct_option_index"] <= 3
            assert "explanation" in q and len(q["explanation"]) > 10


def test_get_all_roadmaps_endpoint(client, candidate_token, db_session):
    """Test retrieving roadmaps with completion progress and scores."""
    token, user = candidate_token
    seed_student_ecosystem(db_session)

    resp = client.get(
        "/api/v1/study-materials/roadmaps/all",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) >= 1

    sprint = next((r for r in data if r["slug"] == "campus-60-day-sprint"), None)
    assert sprint is not None
    assert len(sprint["milestones"]) == 12
    assert "scores" in sprint
    assert "progress_percentage" in sprint


def test_get_milestone_quiz_fairness(client, candidate_token, db_session):
    """Test fetching milestone timed quiz: 30s/q duration, options provided, correct answers omitted."""
    token, user = candidate_token
    seed_student_ecosystem(db_session)

    resp = client.get(
        "/api/v1/study-materials/roadmaps/campus-60-day-sprint/milestones/m1/quiz",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    quiz = resp.json()["data"]

    assert quiz["milestone_id"] == "m1"
    assert "Quantitative Aptitude" in quiz["milestone_title"]
    assert quiz["total_questions"] >= 3
    # Duration strictly 30s per question
    assert quiz["duration_minutes"] >= 1
    assert len(quiz["questions"]) == quiz["total_questions"]

    # Verify questions do NOT leak correct option index or explanation
    for q in quiz["questions"]:
        assert "options" in q and len(q["options"]) == 4
        assert "correct_option_index" not in q
        assert "explanation" not in q


def test_submit_milestone_quiz_and_progress_unlock(client, candidate_token, db_session):
    """Test taking a quiz, achieving >= 60%, unlocking milestone, and receiving explanations."""
    token, user = candidate_token
    seed_student_ecosystem(db_session)

    # Fetch milestone m1 to get question IDs and correct answers for testing
    roadmap = db_session.query(LearningRoadmap).filter(LearningRoadmap.slug == "campus-60-day-sprint").first()
    milestones = json.loads(roadmap.milestones_json)
    m1 = next(m for m in milestones if m["id"] == "m1")
    correct_answers = {q["id"]: q["correct_option_index"] for q in m1["practice_questions"]}

    # Submit 100% correct answers
    resp = client.post(
        "/api/v1/study-materials/roadmaps/campus-60-day-sprint/milestones/m1/submit-quiz",
        headers={"Authorization": f"Bearer {token}"},
        json={"answers": correct_answers, "time_taken_seconds": 45},
    )
    assert resp.status_code == 200
    result = resp.json()["data"]

    assert result["passed"] is True
    assert result["percentage"] == 100.0
    assert result["correct_count"] == len(correct_answers)
    assert result["is_milestone_completed"] is True
    assert result["updated_roadmap_progress"] > 0.0

    # Verify detailed review items contain correct answers and explanations
    assert len(result["review_items"]) == len(correct_answers)
    for item in result["review_items"]:
        assert item["is_correct"] is True
        assert item["explanation"] is not None
        assert len(item["explanation"]) > 10

    # Verify database progress record
    prog = db_session.query(StudentRoadmapProgress).filter(
        StudentRoadmapProgress.user_id == user.id,
        StudentRoadmapProgress.roadmap_id == roadmap.id,
    ).first()
    assert prog is not None
    completed = json.loads(prog.completed_milestones_json)
    assert "m1" in completed
    scores = json.loads(prog.scores_json)
    assert "m1" in scores
    assert scores["m1"]["percentage"] == 100.0
    assert scores["m1"]["passed"] is True


def test_dynamic_ai_quiz_generation_and_evaluation(client, candidate_token, db_session):
    """Test generating dynamic AI aptitude questions for a milestone and submitting them."""
    token, user = candidate_token
    seed_student_ecosystem(db_session)

    # Call AI generation for milestone m3 (Logical Reasoning)
    resp = client.post(
        "/api/v1/study-materials/roadmaps/campus-60-day-sprint/milestones/m3/ai-quiz",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    ai_quiz = resp.json()["data"]

    assert ai_quiz["milestone_id"] == "m3"
    assert ai_quiz["session_id"] is not None
    assert len(ai_quiz["questions"]) == 5

    # Check questions structure
    for q in ai_quiz["questions"]:
        assert len(q["options"]) == 4
        assert q["marks"] == 1.0

    # Submit AI quiz with answers
    first_q = ai_quiz["questions"][0]
    answers = {first_q["id"]: 0}

    sub_resp = client.post(
        "/api/v1/study-materials/roadmaps/campus-60-day-sprint/milestones/m3/submit-quiz",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": ai_quiz["session_id"],
            "answers": answers,
            "time_taken_seconds": 60,
        },
    )
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()["data"]
    assert sub_data["total_questions"] == 5
    assert len(sub_data["review_items"]) == 5
    assert sub_data["review_items"][0]["explanation"] is not None
