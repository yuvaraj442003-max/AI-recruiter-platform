"""
test_student_topics_track.py — Tests for Student Topic Customization & Daily Placement Assessments:
1. Available topics catalog (Java, Python, DSA, Aptitude, Reasoning, SQL, OS, Networks, etc.).
2. Topic preferences & custom topics beyond predefined list.
3. Curated learning feed matching student's chosen topics.
4. 10-Question Daily Placement Assessment with strict 30s-per-question timer (5 mins).
5. Assessment submission, scoring, streak increment, and step-by-step explanations review.
"""
import pytest
from app.core.security import create_access_token
from app.models.user import User, UserRole
from app.services.student_seed_service import seed_student_ecosystem


@pytest.fixture
def candidate_user(db_session):
    user = db_session.query(User).filter(User.email == "topic_student@example.com").first()
    if not user:
        user = User(
            email="topic_student@example.com",
            name="Topic Student",
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


def test_list_available_topics(client, candidate_user):
    token, _ = candidate_user
    resp = client.get(
        "/api/v1/study-materials/topics/available",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) >= 10

    topic_ids = [t["id"] for t in data]
    assert "java" in topic_ids
    assert "python" in topic_ids
    assert "dsa" in topic_ids
    assert "sql" in topic_ids
    assert "quantitative-aptitude" in topic_ids
    assert "logical-reasoning" in topic_ids
    assert "verbal-ability" in topic_ids
    assert "operating-systems" in topic_ids
    assert "computer-networks" in topic_ids
    assert "ai-machine-learning" in topic_ids
    assert "data-engineering" in topic_ids
    assert "cloud-computing" in topic_ids


def test_update_and_get_topic_preferences(client, candidate_user):
    token, user = candidate_user

    # Choose predefined topics + custom topics beyond predefined list
    payload = {
        "selected_topics": ["java", "python", "dsa", "sql", "aptitude"],
        "custom_topics": ["Spring Boot Microservices", "Docker & Kubernetes", "System Design Patterns"],
    }
    resp = client.post(
        "/api/v1/study-materials/topics/preferences",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert resp.status_code == 200
    res = resp.json()["data"]
    assert res["selected_topics"] == payload["selected_topics"]
    assert res["custom_topics"] == payload["custom_topics"]
    assert "daily_streak" in res

    # Fetch preferences
    get_resp = client.get(
        "/api/v1/study-materials/topics/preferences",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_resp.status_code == 200
    pref = get_resp.json()["data"]
    assert "java" in pref["selected_topics"]
    assert "Docker & Kubernetes" in pref["custom_topics"]
    assert pref["daily_streak"] >= 0


def test_curated_learning_feed(client, candidate_user, db_session):
    seed_student_ecosystem(db_session)
    token, user = candidate_user

    # Set student topics to Python & DSA
    client.post(
        "/api/v1/study-materials/topics/preferences",
        headers={"Authorization": f"Bearer {token}"},
        json={"selected_topics": ["python", "dsa"], "custom_topics": ["Django REST Framework"]},
    )

    resp = client.get(
        "/api/v1/study-materials/topics/curated-feed",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    feed = resp.json()["data"]

    assert "matched_materials" in feed
    assert "practice_questions_sample" in feed
    assert "selected_topics" in feed
    assert len(feed["matched_materials"]) >= 1


def test_daily_assessment_flow(client, candidate_user, db_session):
    seed_student_ecosystem(db_session)
    token, user = candidate_user

    # Configure student topics
    client.post(
        "/api/v1/study-materials/topics/preferences",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "selected_topics": ["java", "python", "dsa", "sql", "aptitude"],
            "custom_topics": ["FastAPI Backend"],
        },
    )

    # 1. Start Daily Assessment
    start_resp = client.post(
        "/api/v1/study-materials/topics/daily-assessment/start",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert start_resp.status_code == 200
    start_data = start_resp.json()["data"]

    assert start_data["total_questions"] == 10
    # Strict 30s per question -> 5 minutes total
    assert start_data["duration_minutes"] == 5
    assert len(start_data["questions"]) == 10
    assert start_data["session_id"] is not None

    # Verify no correct answer leak to the candidate
    for q in start_data["questions"]:
        assert "options" in q and len(q["options"]) == 4
        assert "correct_option_index" not in q
        assert "explanation" not in q

    # 2. Submit Daily Assessment
    first_q_id = start_data["questions"][0]["id"]
    answers = {first_q_id: 0}

    submit_resp = client.post(
        "/api/v1/study-materials/topics/daily-assessment/submit",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": start_data["session_id"],
            "answers": answers,
            "time_taken_seconds": 120,
        },
    )
    assert submit_resp.status_code == 200
    sub_data = submit_resp.json()["data"]

    assert sub_data["total_questions"] == 10
    assert "score" in sub_data
    assert "percentage" in sub_data
    assert "passed" in sub_data
    assert sub_data["daily_streak"] >= 1
    assert len(sub_data["review_items"]) == 10

    # Verify each review item has an explanation
    for rev in sub_data["review_items"]:
        assert "question" in rev
        assert "options" in rev
        assert "correct_option_index" in rev
        assert rev["explanation"] is not None
        assert len(rev["explanation"]) > 5


def test_filtered_feed_by_topic(client, candidate_user, db_session):
    seed_student_ecosystem(db_session)
    token, _ = candidate_user

    # Request curated feed specifically for Java
    resp = client.get(
        "/api/v1/study-materials/topics/curated-feed?topic=Java",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    feed = resp.json()["data"]

    assert feed["active_filter_topic"] == "Java"
    assert feed["featured_guide_slug"] == "java-core-placement-guide"
    assert len(feed["matched_materials"]) >= 1
    assert any("java" in m["title"].lower() or "java" in m["slug"].lower() for m in feed["matched_materials"])


def test_get_or_generate_topic_guide(client, candidate_user, db_session):
    seed_student_ecosystem(db_session)
    token, _ = candidate_user

    # 1. Fetch pre-seeded guide for Java
    resp = client.get(
        "/api/v1/study-materials/topics/guide?topic=Java",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    guide = resp.json()["data"]
    assert "Java" in guide["title"]
    assert "Collections" in guide["content_markdown"]

    # 2. Fetch/generate guide for custom topic (e.g. Docker & Containers)
    custom_resp = client.get(
        "/api/v1/study-materials/topics/guide?topic=Docker%20and%20Kubernetes",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert custom_resp.status_code == 200
    custom_guide = custom_resp.json()["data"]
    assert "Docker and Kubernetes" in custom_guide["title"] or "Cloud" in custom_guide["title"]
    assert "Placement" in custom_guide["title"]
    assert len(custom_guide["content_markdown"]) > 200


def test_get_prescribed_books_api(client, candidate_user):
    token, _ = candidate_user
    resp = client.get(
        "/api/v1/study-materials/books/prescribed",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) >= 9
    subjects = [b["subject"].lower() for b in data]
    assert any("java" in s and "javascript" not in s for s in subjects)
    assert any("python" in s for s in subjects)
    assert any("data structures" in s or "dsa" in s for s in subjects)
    assert any("sql" in s for s in subjects)
    assert any("quantitative" in s for s in subjects)
    assert any("logical" in s for s in subjects)
    assert any("javascript" in s for s in subjects)
    assert any("data engineering" in s for s in subjects)
    assert any("artificial intelligence" in s or "ai" in s for s in subjects)

    for b in data:
        assert b["chapters_count"] == 9
        assert len(b["chapters"]) == 9
        assert "exam_grounding_policy" in b


def test_get_book_chapters_api(client, candidate_user):
    token, _ = candidate_user
    test_subjects = ["java", "python", "dsa", "sql", "quantitative aptitude", "logical reasoning", "javascript", "data engineering", "ai / ml"]
    for sub in test_subjects:
        resp = client.get(
            f"/api/v1/study-materials/books/{sub}/chapters",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["chapters_count"] == 9
        assert len(data["chapters"]) == 9
        assert "chapters" in data
        assert data["chapters"][0]["chapter_num"] == 1


def test_daily_assessment_single_subject_book_grounding(client, candidate_user):
    token, _ = candidate_user
    resp = client.post(
        "/api/v1/study-materials/topics/daily-assessment/start?topic=Data%20Structures%20%26%20Algorithms%20(DSA)",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_questions"] == 10
    assert len(data["questions"]) == 10
    # Every question must be for Data Structures & Algorithms (DSA)
    for q in data["questions"]:
        assert q["topic"] == "Data Structures & Algorithms (DSA)"



