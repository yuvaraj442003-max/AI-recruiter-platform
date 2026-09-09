"""
test_coding.py — Unit and integration tests for the Coding Assessment module:
- Sandbox code execution (Python/JS)
- Question & Assessment CRUD
- Candidate start, run code, submit assessment
- Evaluation & Composite overall score calculation
"""
import pytest
from app.services.code_executor import execute_code
from app.services.coding_evaluation_service import evaluate_question_submission


def test_code_executor_python_success():
    """Test executing valid Python code in sandbox."""
    code = "import sys\nprint('Hello ' + sys.stdin.read().strip())"
    res = execute_code("python", code, input_data="World", timeout_seconds=5.0)
    assert res["status"] == "Success"
    assert "Hello World" in res["stdout"]


def test_code_executor_python_timeout():
    """Test sandbox timeout enforcement."""
    code = "import time\ntime.sleep(10)"
    res = execute_code("python", code, timeout_seconds=1.0)
    assert res["status"] == "Timeout"


def test_code_executor_env_scrubbing():
    """Test sensitive credentials are scrubbed from sandbox process."""
    code = "import os\nprint(os.environ.get('DATABASE_URL'))"
    res = execute_code("python", code, timeout_seconds=5.0)
    assert res["status"] == "Success"
    assert res["stdout"].strip() in ("None", "")


def test_evaluation_service_passed():
    """Test functional and quality evaluation logic."""
    test_cases = [
        {"input_data": "5", "expected_output": "10", "is_hidden": False, "points": 10},
        {"input_data": "3", "expected_output": "6", "is_hidden": True, "points": 10}
    ]
    code = "import sys\nn = int(sys.stdin.read().strip())\nprint(n * 2)"
    res = evaluate_question_submission("Double Number", test_cases, "python", code)

    assert res["passed"] == 2
    assert res["total"] == 2
    assert res["functional_score"] == 100.0
    assert res["final_score"] >= 80.0
    assert res["time_complexity"] == "O(1)"


from app.core.security import create_access_token
from app.models.user import User, UserRole

def test_coding_router_flow(client, db_session):
    """Integration test for questions listing endpoint with authenticated user."""
    test_user = db_session.query(User).filter_map({"email": "test_coding_user@example.com"}).first() if hasattr(db_session.query(User), "filter_map") else None
    if not test_user:
        test_user = db_session.query(User).filter(User.email == "test_coding_user@example.com").first()
    if not test_user:
        test_user = User(
            email="test_coding_user@example.com",
            password_hash="hashedpassword123",
            name="Test Coding Candidate",
            role=UserRole.candidate
        )
        db_session.add(test_user)
        db_session.commit()
        db_session.refresh(test_user)

    token = create_access_token(str(test_user.id), role=test_user.role)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/coding/questions", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
