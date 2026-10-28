"""
test_company_intelligence_and_textbooks.py — Tests for:
1. 12 Top Recruiters Intelligence (TCS, Infosys, Cognizant, Accenture, Wipro, Amazon, Deloitte, Capgemini, Goldman Sachs, Zoho, Google, Microsoft).
2. Company exam patterns, cutoffs, selection rounds, packages, topic weightages & tips, 4-week prep strategies, and analyzed questions.
3. Timed Company Mock Tests (strict 30s/question speed simulation protocol).
4. Company mock test submission, scoring, pass/fail evaluation, and detailed explanations review.
5. All 13 Prescribed In-App Textbooks (DSA, SQL, Quant, Reasoning, Java, Python, JS, OS, CN, DBMS, Verbal, Data Eng, AI/ML).
6. Grounded textbook assessment questions for newly added core subjects (OS, CN, DBMS, Verbal).
"""
import pytest
from app.core.security import create_access_token
from app.models.user import User, UserRole


@pytest.fixture
def candidate_user(db_session):
    user = db_session.query(User).filter(User.email == "campus_student@example.com").first()
    if not user:
        user = User(
            email="campus_student@example.com",
            name="Campus Student",
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


def test_list_all_12_companies(client, candidate_user):
    token, _ = candidate_user
    resp = client.get(
        "/api/v1/study-materials/companies",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["total"] == 12

    companies = data["data"]
    slugs = [c["slug"] for c in companies]
    expected_slugs = [
        "tcs", "infosys", "cognizant", "accenture", "wipro",
        "amazon", "deloitte", "capgemini", "goldman-sachs", "zoho",
        "google", "microsoft"
    ]
    for es in expected_slugs:
        assert es in slugs

    # Validate structure of each company summary
    for c in companies:
        assert "name" in c
        assert "slug" in c
        assert "difficulty" in c
        assert "avg_package" in c
        assert "exam_pattern" in c
        assert "rounds" in c
        assert len(c["rounds"]) >= 3
        assert len(c["topic_weightages"]) >= 3


def test_company_detail_deep_dive(client, candidate_user):
    token, _ = candidate_user

    # Test TCS
    resp = client.get(
        "/api/v1/study-materials/companies/tcs",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    tcs = resp.json()["data"]
    assert tcs["slug"] == "tcs"
    assert len(tcs["analyzed_questions"]) >= 5
    assert len(tcs["four_week_strategy"]) == 4

    # Test Google
    resp = client.get(
        "/api/v1/study-materials/companies/google",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    google = resp.json()["data"]
    assert google["slug"] == "google"
    assert "Google" in google["name"]
    assert len(google["analyzed_questions"]) >= 4

    # Test Microsoft
    resp = client.get(
        "/api/v1/study-materials/companies/microsoft",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    msft = resp.json()["data"]
    assert msft["slug"] == "microsoft"
    assert len(msft["analyzed_questions"]) >= 4


def test_company_mock_test_lifecycle(client, candidate_user):
    token, _ = candidate_user

    # 1. Start company mock test for TCS
    start_resp = client.post(
        "/api/v1/study-materials/companies/tcs/start-test",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert start_resp.status_code == 200
    test_data = start_resp.json()["data"]
    assert test_data["company_slug"] == "tcs"
    assert "session_id" in test_data
    questions = test_data["questions"]
    assert len(questions) >= 5
    # Strict 30s/question speed duration
    assert test_data["duration_seconds"] == len(questions) * 30

    session_id = test_data["session_id"]

    # 2. Submit answers
    # Answer the first question with option 0 or 1
    user_answers = {}
    for i, q in enumerate(questions):
        # Pick first option key or '0'
        keys = list(q["options"].keys())
        user_answers[str(q["id"])] = keys[0]

    submit_payload = {
        "session_id": session_id,
        "answers": user_answers,
        "time_taken_seconds": 120,
    }

    submit_resp = client.post(
        "/api/v1/study-materials/companies/tcs/submit-test",
        headers={"Authorization": f"Bearer {token}"},
        json=submit_payload,
    )
    assert submit_resp.status_code == 200
    result = submit_resp.json()["data"]
    assert "score" in result
    assert "total" in result
    assert "percentage" in result
    assert "passed" in result
    assert "cutoff_percentage" in result
    assert "review" in result
    assert len(result["review"]) == len(questions)
    # Check that each review item has explanation
    for rev in result["review"]:
        assert "explanation" in rev
        assert "correct_option" in rev


def test_all_13_prescribed_textbooks(client, candidate_user):
    token, _ = candidate_user
    resp = client.get(
        "/api/v1/study-materials/books/prescribed",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 13

    subjects = [b["subject"] for b in data]
    expected_subjects = [
        "dsa", "sql", "quant", "reasoning", "java", "python",
        "javascript", "os", "cn", "dbms", "verbal", "data-engineering", "ai-ml"
    ]
    for es in expected_subjects:
        assert es in subjects


def test_core_cs_book_assessments(client, candidate_user):
    token, _ = candidate_user

    for subject in ["os", "cn", "dbms", "verbal"]:
        resp = client.get(
            f"/api/v1/study-materials/books/prescribed/{subject}/assessment",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["subject"] == subject
        assert len(data["questions"]) >= 5
        # 30 seconds per question speed protocol
        assert data["duration_seconds"] == len(data["questions"]) * 30
        for q in data["questions"]:
            assert "textbook_ref" in q
            assert len(q["options"]) == 4

