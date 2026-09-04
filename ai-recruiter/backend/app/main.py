"""
AI Recruiter — FastAPI application entrypoint (Phase 1: auth foundation, Phase 2: resume AI).
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.core.exceptions import register_exception_handlers
from app.middleware.security_headers import SecurityHeadersMiddleware
# Import all models to ensure metadata registration
from app.models import user, candidate, job, application, interview, audit_log, recruiter, notification, application_history, message
from app.routers import (
    admin,
    analytics,
    applications,
    ats,
    auth,
    candidate_comparison,
    candidate_search,
    interviews,
    jobs,
    matching,
    messages,
    notifications,
    recommendations,
    recruiter_profile,
    resumes,
    speech,
)
from app.services.resume_service import seed_skills

logging.basicConfig(level=logging.INFO)


from sqlalchemy import inspect, text

def _auto_migrate_db():
    """Ensure all tables and newly added columns exist in database without data loss."""
    Base.metadata.create_all(bind=engine)

    # Helper to add column to database table if missing
    columns_to_ensure = [
        # (table_name, column_name, col_type)
        ("users", "is_active", "BOOLEAN DEFAULT TRUE"),
        ("users", "verification_status", "VARCHAR(50) DEFAULT 'approved'"),
        ("users", "verification_reasons", "TEXT"),

        ("recruiter_profiles", "phone", "VARCHAR(50)"),
        ("recruiter_profiles", "recruiter_linkedin_url", "VARCHAR(255)"),
        ("recruiter_profiles", "company_linkedin_url", "VARCHAR(255)"),

        ("jobs", "company_name", "VARCHAR(255)"),
        ("jobs", "company_logo", "VARCHAR(500)"),
        ("jobs", "company_description", "TEXT"),
        ("jobs", "company_website", "VARCHAR(255)"),
        ("jobs", "company_location", "VARCHAR(255)"),
        ("jobs", "industry", "VARCHAR(150)"),
        ("jobs", "company_size", "VARCHAR(100)"),
        ("jobs", "linkedin_profile", "VARCHAR(255)"),
        ("jobs", "github_profile", "VARCHAR(255)"),
        ("jobs", "other_links", "TEXT"),
        ("jobs", "fraud_risk_score", "FLOAT DEFAULT 0.0"),
        ("jobs", "fraud_risk_level", "VARCHAR(20) DEFAULT 'LOW'"),
        ("jobs", "fraud_reasons", "TEXT"),

        ("companies", "ssl_details", "TEXT"),
        ("companies", "verification_notes", "TEXT"),

        ("candidate_profiles", "profile_photo", "VARCHAR(500)"),
        ("candidate_profiles", "headline", "VARCHAR(255)"),
        ("candidate_profiles", "current_role", "VARCHAR(255)"),
        ("candidate_profiles", "certifications", "TEXT"),
        ("candidate_profiles", "portfolio_url", "VARCHAR(255)"),
        ("candidate_profiles", "linkedin_url", "VARCHAR(255)"),
        ("candidate_profiles", "github_url", "VARCHAR(255)"),
        ("candidate_profiles", "other_links", "TEXT"),
        ("candidate_profiles", "created_by_recruiter_id", "VARCHAR(36)"),
        ("candidate_profiles", "source", "VARCHAR(100) DEFAULT 'direct_candidate'"),

        # ATS Screening fields for applications
        ("applications", "ats_score", "FLOAT"),
        ("applications", "job_match_score", "FLOAT"),
        ("applications", "skills_match_score", "FLOAT"),
        ("applications", "experience_match_score", "FLOAT"),
        ("applications", "education_match_score", "FLOAT"),
        ("applications", "location_match_score", "FLOAT"),
        ("applications", "keyword_match_score", "FLOAT"),
        ("applications", "responsibility_match_score", "FLOAT"),
        ("applications", "matched_skills", "TEXT"),
        ("applications", "missing_skills", "TEXT"),
        ("applications", "matched_keywords", "TEXT"),
        ("applications", "missing_keywords", "TEXT"),
        ("applications", "recommendation", "VARCHAR(100)"),
        ("applications", "screening_status", "VARCHAR(100)"),
        ("applications", "is_eligible", "BOOLEAN DEFAULT FALSE"),
        ("applications", "is_shortlisted", "BOOLEAN DEFAULT FALSE"),
        ("applications", "screened_at", "TIMESTAMP"),
        ("applications", "screening_version", "VARCHAR(50) DEFAULT 'v1.0'"),
        ("applications", "recruiter_override", "BOOLEAN DEFAULT FALSE"),
        ("applications", "override_reason", "TEXT"),
        ("applications", "uploaded_by_recruiter_id", "VARCHAR(36)"),
        ("applications", "source", "VARCHAR(100) DEFAULT 'direct_candidate'"),
    ]

    with engine.begin() as conn:
        inspector = inspect(conn)
        for table, col, col_type in columns_to_ensure:
            try:
                if inspector.has_table(table):
                    existing_cols = [r["name"] for r in inspector.get_columns(table)]
                    if col not in existing_cols:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}"))
                        logging.info(f"Auto-migrated: Added {col} to {table}")
            except Exception as e:
                logging.warning(f"Auto-migration check for {table}.{col} skipped: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup: ensure database schema is up-to-date and seed skills.
    try:
        _auto_migrate_db()
    except Exception:
        logging.getLogger("ai_recruiter").exception("Database migration failed at startup")

    db = SessionLocal()
    try:
        seed_skills(db)
        if db.query(user.User).count() == 0:
            logging.info("Empty database detected on startup. Auto-seeding initial demo accounts and data...")
            from scripts.seed_demo_data import seed_demo
            seed_demo()
    except Exception:
        logging.getLogger("ai_recruiter").exception("Startup initialization failed")
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Recruitment & Interview Platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)

register_exception_handlers(app)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(resumes.router, prefix="/api/v1")
app.include_router(resumes.resume_singular_router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")
app.include_router(matching.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(interviews.router, prefix="/api/v1")
app.include_router(speech.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(analytics.recruiter_router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(recruiter_profile.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(ats.router, prefix="/api/v1")
app.include_router(candidate_comparison.router, prefix="/api/v1")
app.include_router(candidate_search.router, prefix="/api/v1")
app.include_router(candidate_search.candidate_singular_router, prefix="/api/v1")




@app.get("/", tags=["Health"])
def root():
    return {"success": True, "message": f"{settings.APP_NAME} API is running", "data": {"version": "0.1.0"}}


@app.get("/health", tags=["Health"])
def health():
    return {"success": True, "message": "healthy", "data": {"environment": settings.ENVIRONMENT}}
