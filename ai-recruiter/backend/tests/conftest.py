"""
Shared test fixtures. A single PostgreSQL test database and a single
FastAPI dependency override are used across the whole test suite so
multiple test files never race to control app.dependency_overrides.
"""
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

DEFAULT_PG_URL = "postgresql+psycopg2://postgres:postgres234@localhost:5432/ai_recruiter"
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", os.getenv("DATABASE_URL", DEFAULT_PG_URL))

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def _setup_test_database():
    # Import here (not at module load) so every model is registered on
    # Base.metadata before we create tables.
    from app.main import app as fastapi_app
    from app.core.database import Base, get_db
    from app.core import rate_limit
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    rate_limit._clear_all_state_for_tests()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()



@pytest.fixture(scope="session")
def client():
    from app.main import app as fastapi_app

    return TestClient(fastapi_app)


@pytest.fixture()
def db_session():
    """A DB session bound to the test SQLite engine (never the real Postgres one)."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
