"""
test_weekly_challenge.py — Unit and integration tests for Weekly Aptitude and Coding Challenges:
- Weekly questions generation, non-repeating assignment, and auto-rotation
- Candidate taking current weekly aptitude sprint
- Aptitude submission, scoring, explanations review, and progress history
- Candidate taking current weekly coding challenge with multi-language starter code
- Code execution in sandbox, test cases verification, and challenge submission
- Weekly competitive leaderboards with candidate anonymization & privacy controls
- Admin question CRUD, approval, force rotation, and AI question validation
"""
import json
import uuid
import pytest
from app.core.security import create_access_token
from app.models.coding import CodingQuestion
from app.models.student import AptitudeQuestion
from app.models.user import User, UserRole
from app.models.weekly_challenge import (
    WeeklyAptitudeAttempt,
    WeeklyAptitudeSet,
    WeeklyCodingAttempt,
    WeeklyCodingChallenge,
)
from app.services.weekly_challenge_service import (
    ensure_all_weekly_challenges,
    ensure_weekly_aptitude_set,
    ensure_weekly_coding_challenge,
    get_aptitude_leaderboard,
    get_coding_leaderboard,
    get_current_week_code,
    validate_aptitude_question_payload,
    validate_coding_question_payload,
)


@pytest.fixture
def candidate_user(db_session):
    user = db_session.query(User).filter(User.email == "weekly_candidate@example.com").first()
    if not user:
        user = User(
            email="weekly_candidate@example.com",
            password_hash="hashedpass123",
            name="Alex Morgan",
            role=UserRole.candidate,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user


@pytest.fixture
def candidate_headers(candidate_user):
    token = create_access_token(str(candidate_user.id), role=candidate_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_user(db_session):
    admin = db_session.query(User).filter(User.email == "weekly_admin@example.com").first()
    if not admin:
        admin = User(
            email="weekly_admin@example.com",
            password_hash="hashedpass123",
            name="Platform Admin",
            role=UserRole.admin,
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
    return admin


@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token(str(admin_user.id), role=admin_user.role)
    return {"Authorization": f"Bearer {token}"}


def test_question_validation_logic():
    """Test strict validation rules for aptitude and coding question generation."""
    # Valid aptitude question
    valid_apt = {
        "question": "What is the next number in series: 2, 6, 12, 20, 30, ...?",
        "options": ["42", "40", "44", "36"],
        "correct_option_index": 0,
        "difficulty": "medium",
    }
    is_valid, err = validate_aptitude_question_payload(valid_apt)
    assert is_valid is True
    assert err is None

    # Invalid: missing option
    bad_apt = {
        "question": "Sample question here?",
        "options": ["A", "B", "C"],
        "correct_option_index": 0,
    }
    is_valid, err = validate_aptitude_question_payload(bad_apt)
    assert is_valid is False
    assert "exactly 4 options" in err

    # Valid coding challenge
    valid_coding = {
        "title": "Reverse Array",
        "description": "Reverse an array of numbers in place.",
        "difficulty": "Easy",
        "public_test_cases": [{"input_data": "[1,2,3]", "expected_output": "[3,2,1]"}],
    }
    is_valid, err = validate_coding_question_payload(valid_coding)
    assert is_valid is True

    # Invalid coding challenge: no test cases
    bad_coding = {
        "title": "No Test Cases",
        "description": "A challenge with no test cases provided.",
        "difficulty": "Easy",
        "public_test_cases": [],
    }
    is_valid, err = validate_coding_question_payload(bad_coding)
    assert is_valid is False
    assert "at least one test case" in err


def test_weekly_service_generation_and_rotation(db_session):
    """Test weekly sets creation and non-repeating assignment."""
    week_code = get_current_week_code()
    apt_set, coding_chal = ensure_all_weekly_challenges(db_session)

    assert apt_set.week_code == week_code
    assert apt_set.total_questions >= 5
    assert coding_chal.week_code == week_code
    assert coding_chal.status == "published"

    # Verify questions are marked as assigned
    q_ids = json.loads(apt_set.question_ids_json)
    assigned_q = db_session.query(AptitudeQuestion).filter(AptitudeQuestion.id == uuid.UUID(q_ids[0])).first()
    assert assigned_q.week_assigned == week_code


def test_candidate_weekly_overview_endpoint(client, candidate_headers):
    """Test /api/v1/weekly/overview endpoint."""
    res = client.get("/api/v1/weekly/overview", headers=candidate_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    data = body["data"]
    assert "current_week_code" in data
    assert data["aptitude"] is not None
    assert data["coding"] is not None
    assert "overall_readiness_pct" in data


def test_weekly_aptitude_flow(client, candidate_headers, db_session):
    """Test getting current aptitude test, submitting answers, and checking history."""
    # 1. Get test questions
    get_res = client.get("/api/v1/weekly/aptitude/current", headers=candidate_headers)
    assert get_res.status_code == 200
    get_data = get_res.json()["data"]
    assert "questions" in get_data
    questions = get_data["questions"]
    assert len(questions) > 0

    # 2. Submit answers
    first_q = questions[0]
    answers_payload = {
        first_q["id"]: 0,
    }
    submit_res = client.post(
        "/api/v1/weekly/aptitude/submit",
        headers=candidate_headers,
        json={"answers": answers_payload, "time_taken_seconds": 120, "is_anonymous": False},
    )
    assert submit_res.status_code == 200
    res_data = submit_res.json()["data"]
    assert res_data["total_questions"] >= len(questions)
    assert "score_percentage" in res_data
    assert "questions_review" in res_data
    assert len(res_data["questions_review"]) > 0

    # 3. Check history
    hist_res = client.get("/api/v1/weekly/aptitude/history", headers=candidate_headers)
    assert hist_res.status_code == 200
    hist_data = hist_res.json()["data"]
    assert len(hist_data) >= 1
    assert hist_data[0]["time_taken_seconds"] == 120

    # 4. Check Leaderboard
    lb_res = client.get("/api/v1/weekly/aptitude/leaderboard", headers=candidate_headers)
    assert lb_res.status_code == 200
    lb_data = lb_res.json()["data"]
    assert lb_data["total_participants"] >= 1
    assert lb_data["current_user_rank"] is not None
    assert lb_data["entries"][0]["candidate_name"] is not None


def test_weekly_coding_flow(client, candidate_headers, db_session):
    """Test getting current coding challenge, running code snippet in sandbox, and submitting."""
    # 1. Get challenge
    get_res = client.get("/api/v1/weekly/coding/current", headers=candidate_headers)
    assert get_res.status_code == 200
    chal_data = get_res.json()["data"]
    assert "questions" in chal_data
    questions = chal_data["questions"]
    assert len(questions) > 0

    target_q = questions[0]
    q_id = str(target_q["id"])

    # 2. Run code snippet in sandbox
    run_res = client.post(
        "/api/v1/weekly/coding/run",
        headers=candidate_headers,
        json={
            "question_id": q_id,
            "language": "python",
            "source_code": "import sys\nprint('running')",
        },
    )
    assert run_res.status_code == 200
    run_data = run_res.json()["data"]
    assert "passed" in run_data
    assert "functional_score" in run_data

    # 3. Submit challenge
    starter_code = "import sys\nprint('submitted')"
    if target_q.get("starter_code") and "python" in target_q["starter_code"]:
        starter_code = target_q["starter_code"]["python"]

    submit_res = client.post(
        "/api/v1/weekly/coding/submit",
        headers=candidate_headers,
        json={
            "submissions": {
                q_id: {"language": "python", "source_code": starter_code}
            },
            "time_taken_seconds": 350,
            "is_anonymous": True,
        },
    )
    assert submit_res.status_code == 200
    sub_data = submit_res.json()["data"]
    assert "percentage" in sub_data
    assert len(sub_data["questions"]) >= 1

    # 4. Check Leaderboard anonymization
    lb_res = client.get("/api/v1/weekly/coding/leaderboard", headers=candidate_headers)
    assert lb_res.status_code == 200
    lb_data = lb_res.json()["data"]
    assert lb_data["total_participants"] >= 1
    # For current user it shows (You), for others Candidate #XXXX
    user_entry = next(e for e in lb_data["entries"] if e["is_current_user"])
    assert "(You)" in user_entry["candidate_name"]


def test_admin_weekly_question_management(client, admin_headers):
    """Test admin review, creation, editing, approval, and rotation endpoints."""
    # 1. Admin lists questions
    list_res = client.get("/api/v1/weekly/admin/questions?type=aptitude", headers=admin_headers)
    assert list_res.status_code == 200
    assert "questions" in list_res.json()["data"]

    # 2. Admin creates a new aptitude question
    new_q_payload = {
        "topic_slug": "quantitative-aptitude",
        "subtopic": "Profit Calculation",
        "question": "A shopkeeper sells an article for $240 and incurs a 20% loss. What was the cost price?",
        "options": ["$300", "$280", "$320", "$290"],
        "correct_option_index": 0,
        "explanation": "Cost Price = Selling Price / (1 - 0.20) = 240 / 0.80 = $300.",
        "difficulty": "medium",
        "company_tag": "TCS",
        "status": "pending_review",
    }
    create_res = client.post("/api/v1/weekly/admin/aptitude/question", headers=admin_headers, json=new_q_payload)
    assert create_res.status_code == 200
    created_id = create_res.json()["data"]["id"]

    # 3. Admin approves question
    approve_res = client.post(f"/api/v1/weekly/admin/aptitude/question/{created_id}/approve", headers=admin_headers)
    assert approve_res.status_code == 200
    assert approve_res.json()["data"]["status"] == "approved"

    # 4. Admin updates question
    update_res = client.put(
        f"/api/v1/weekly/admin/aptitude/question/{created_id}",
        headers=admin_headers,
        json={"difficulty": "hard"},
    )
    assert update_res.status_code == 200

    # 5. Admin forces weekly rotation
    rotate_res = client.post("/api/v1/weekly/admin/rotate-now", headers=admin_headers)
    assert rotate_res.status_code == 200
    assert "week_code" in rotate_res.json()["data"]

    # 6. Admin deletes created question
    del_res = client.delete(f"/api/v1/weekly/admin/aptitude/question/{created_id}", headers=admin_headers)
    assert del_res.status_code == 200


def test_programming_and_aptitude_topics_catalog_and_practice(client, candidate_headers):
    """Test retrieving structured programming topics, topic problems, problem detail, and aptitude topics."""
    # 1. Weekly status endpoint
    status_res = client.get("/api/v1/weekly/status", headers=candidate_headers)
    assert status_res.status_code == 200
    status_data = status_res.json()["data"]
    assert "current_week_code" in status_data
    assert "cadence" in status_data
    assert "next_update_utc" in status_data
    assert status_data["total_coding_topics"] >= 10
    assert status_data["total_aptitude_topics"] >= 4

    # 2. Overview includes schedule & topics summaries
    ov_res = client.get("/api/v1/weekly/overview", headers=candidate_headers)
    assert ov_res.status_code == 200
    ov_data = ov_res.json()["data"]
    assert "schedule" in ov_data
    assert "coding_topics_summary" in ov_data
    assert "aptitude_topics_summary" in ov_data
    assert len(ov_data["coding_topics_summary"]) >= 6

    # 3. Programming topics catalog
    topics_res = client.get("/api/v1/weekly/topics/coding", headers=candidate_headers)
    assert topics_res.status_code == 200
    coding_topics = topics_res.json()["data"]
    assert len(coding_topics) >= 10
    first_topic = coding_topics[0]
    assert "slug" in first_topic
    assert "name" in first_topic
    assert "icon" in first_topic

    # 4. Topic problems for first topic
    prob_res = client.get(f"/api/v1/weekly/topics/coding/{first_topic['slug']}/problems", headers=candidate_headers)
    assert prob_res.status_code == 200
    prob_data = prob_res.json()["data"]
    assert isinstance(prob_data, list)
    assert len(prob_data) > 0

    first_prob = prob_data[0]
    assert "title" in first_prob
    assert "starter_code" in first_prob

    # 5. Detail for single problem
    detail_res = client.get(f"/api/v1/weekly/topics/coding/problem/{first_prob['id']}", headers=candidate_headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()["data"]
    assert detail_data["id"] == first_prob["id"]
    assert "public_test_cases" in detail_data

    # 6. Aptitude topics catalog
    apt_topics_res = client.get("/api/v1/weekly/topics/aptitude", headers=candidate_headers)
    assert apt_topics_res.status_code == 200
    apt_topics = apt_topics_res.json()["data"]
    assert len(apt_topics) >= 4

    # 7. Topic aptitude questions
    apt_q_res = client.get(f"/api/v1/weekly/topics/aptitude/{apt_topics[0]['slug']}/questions", headers=candidate_headers)
    assert apt_q_res.status_code == 200
    apt_q_data = apt_q_res.json()["data"]
    assert isinstance(apt_q_data, list)
    assert len(apt_q_data) > 0


def test_admin_pdf_rag_endpoints(client, admin_headers):
    """Test administrative endpoints for RS Aggarwal PDF indexing and Qdrant RAG weekly rotation."""
    # 1. Check PDF RAG status endpoint
    status_res = client.get("/api/v1/weekly/admin/pdf-rag-status", headers=admin_headers)
    assert status_res.status_code == 200
    status_body = status_res.json()
    assert status_body["success"] is True
    data = status_body["data"]
    assert "pdf_found" in data
    assert "current_week_code" in data
    assert "focus_topic" in data

    # 2. Test rotate weekly challenge from PDF via Qdrant RAG
    rotate_res = client.post("/api/v1/weekly/admin/rotate-from-pdf?force_refresh=true", headers=admin_headers)
    assert rotate_res.status_code == 200
    rotate_body = rotate_res.json()
    assert rotate_body["success"] is True
    assert rotate_body["data"]["total_questions"] == 5
    assert "focus_topic" in rotate_body["data"]




