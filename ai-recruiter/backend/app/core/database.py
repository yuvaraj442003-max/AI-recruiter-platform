"""
database.py — Dual-Database Engine Manager supporting both PostgreSQL & SQLite.
Handles connection pooling, engine initialization, dialect detection,
and automatic fallback.
"""
import logging
from typing import Generator

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.database")


def _create_database_engine(url: str):
    """Creates a SQLAlchemy engine with dialect-specific optimizations."""
    is_sqlite = url.startswith("sqlite")
    
    if is_sqlite:
        eng = create_engine(
            url,
            connect_args={"check_same_thread": False, "timeout": 30},
            future=True,
        )

        @event.listens_for(eng, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA busy_timeout=30000;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.close()

        return eng
    else:
        return create_engine(
            url,
            connect_args={"connect_timeout": 2},
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            future=True,
        )


# Initialize primary engine based on DATABASE_URL setting
target_url = settings.DATABASE_URL or settings.POSTGRES_DATABASE_URL or settings.SQLITE_DATABASE_URL
active_url = target_url

try:
    engine = _create_database_engine(target_url)
    # Quick connectivity test
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info(f"Database connected successfully using: {target_url.split('@')[-1] if '@' in target_url else target_url}")
except Exception as err:
    logger.warning(f"Failed to connect to primary database ({target_url}): {err}. Falling back to SQLite database ({settings.SQLITE_DATABASE_URL}).")
    active_url = settings.SQLITE_DATABASE_URL
    engine = _create_database_engine(active_url)

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
    """Returns status details about the active database engine (PostgreSQL or SQLite)."""
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
        "is_postgres": dialect_name == "postgresql",
        "is_sqlite": dialect_name == "sqlite",
        "connected": connected,
    }
