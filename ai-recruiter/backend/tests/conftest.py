"""
Shared test fixtures for AI Recruiter test suite.
"""
import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401
from app.core.config import settings
from app.core.database import Base, get_db

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_ai_recruiter.db")

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def _setup_test_database():
    settings.SMTP_USER = "test@gmail.com"
    settings.SMTP_PASSWORD = "testpassword1234"

    patcher = patch("app.services.email_service._send_smtp_email", return_value=True)
    patcher.start()

    Base.metadata.drop_all(bind=engine)
    from app.main import _auto_migrate_db, app as fastapi_app
    _auto_migrate_db(engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    yield

    patcher.stop()


@pytest.fixture(scope="session")
def client():
    from app.main import app as fastapi_app
    return TestClient(fastapi_app)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
