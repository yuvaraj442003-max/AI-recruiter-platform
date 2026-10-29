"""
database.py — PostgreSQL Database Engine Manager.
Exclusively manages PostgreSQL connections, connection pooling, and session lifecycles
across the entire application.
"""
import logging
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.database")


def _create_database_engine(url: str):
    """Creates a SQLAlchemy engine configured exclusively for PostgreSQL with production pooling."""
    return create_engine(
        url,
        connect_args={"connect_timeout": 10},
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        future=True,
    )


# PostgreSQL is the sole primary database
target_url = (settings.DATABASE_URL or settings.POSTGRES_DATABASE_URL).strip()
active_url = target_url

try:
    engine = _create_database_engine(target_url)
    # Quick connectivity test
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info(f"PostgreSQL database connected successfully using: {target_url.split('@')[-1] if '@' in target_url else target_url}")
except Exception as err:
    logger.error(f"Failed to connect to PostgreSQL database ({target_url}): {err}")
    # Still initialize engine so startup can log/report appropriately
    engine = _create_database_engine(target_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a database session.
    Ensures session closes cleanly after request execution.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_status() -> dict:
    """Returns status details about the active PostgreSQL database engine."""
    dialect_name = engine.dialect.name
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        connected = True
    except Exception:
        connected = False

    return {
        "active_url": active_url.split("@")[-1] if "@" in active_url else active_url,
        "dialect": dialect_name,
        "is_postgres": True,
        "connected": connected,
    }
