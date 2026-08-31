"""
init_postgres.py — Script to set up PostgreSQL database for AI Recruiter.

Creates the `ai_recruiter` database on local PostgreSQL if it does not exist,
applies the full schema and migrations, and verifies connection.
"""
import sys
import os

# Add backend directory to python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import inspect

PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = int(os.getenv("POSTGRES_PORT", 5432))
PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres234")
DB_NAME = os.getenv("POSTGRES_DB", "ai_recruiter")


def setup_postgresql():
    print(f"Connecting to PostgreSQL server at {PG_HOST}:{PG_PORT} as '{PG_USER}'...")
    
    # 1. Connect to default 'postgres' database to ensure target database exists
    conn = psycopg2.connect(
        dbname="postgres",
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()

    if not exists:
        print(f"Database '{DB_NAME}' does not exist. Creating database '{DB_NAME}'...")
        cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"[OK] Database '{DB_NAME}' created successfully.")
    else:
        print(f"[INFO] Database '{DB_NAME}' already exists.")

    cursor.close()
    conn.close()

    # 2. Configure DATABASE_URL in environment settings
    pg_url = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"
    os.environ["DATABASE_URL"] = pg_url

    print("\nInitializing SQLAlchemy tables in PostgreSQL...")
    from app.core.database import Base, engine
    import app.models  # Ensure all models are registered

    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"[OK] Schema initialized! Created {len(tables)} tables: {', '.join(tables)}")

    # 3. Seed default skills
    from app.core.database import SessionLocal
    from app.services.resume_service import seed_skills

    db = SessionLocal()
    try:
        seed_skills(db)
        print("[OK] Default skill taxonomy seeded.")
    finally:
        db.close()

    print("\n[SUCCESS] PostgreSQL configuration & database setup complete!")


if __name__ == "__main__":
    setup_postgresql()
