"""
AI Recruiter — FastAPI application entrypoint (Phase 1: auth foundation, Phase 2: resume AI).
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.core.exceptions import register_exception_handlers
from app.middleware.security_headers import SecurityHeadersMiddleware
# Import all models to ensure metadata registration
from app.models import user, candidate, job, application, interview, interview_scorecard, talent_rediscovery, candidate_feedback, audit_log, recruiter, notification, application_history, message, saved_search
from app.routers import (
    admin,
    analytics,
    applications,
    ats,
    auth,
    candidate_comparison,
    candidate_search,
    calendar,
    coding,
    email_settings,
    interviews,
    interview_ws,
    interview_scorecard as interview_scorecard_router,
    talent_rediscovery as talent_rediscovery_router,
    feedback as feedback_router,
    jobs,
    matching,
    messages,
    notifications,
    recommendations,
    recruiter_profile,
    resumes,
    screening,
    proctoring,
    speech,
)
from app.services.resume_service import seed_skills

logging.basicConfig(level=logging.INFO)


from sqlalchemy import inspect, text

def _auto_migrate_db(target_engine=None):
    """Ensure all tables and newly added columns exist in database without data loss."""
    active_engine = target_engine or engine
    Base.metadata.create_all(bind=active_engine)

    is_pg = active_engine.dialect.name == "postgresql"
    uuid_type = "UUID" if is_pg else "VARCHAR(36)"

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
        ("jobs", "status", "VARCHAR(50) DEFAULT 'DRAFT'"),
        ("jobs", "anti_cheat_rules", "TEXT"),
        ("jobs", "anti_cheat_score", "INTEGER DEFAULT 0"),

        ("companies", "ssl_details", "TEXT"),
        ("companies", "verification_notes", "TEXT"),

        ("candidate_profiles", "profile_photo", "VARCHAR(500)"),
        ("candidate_profiles", "headline", "VARCHAR(255)"),
        ("candidate_profiles", "current_role", "VARCHAR(255)"),
        ("candidate_profiles", "skills", "TEXT"),
        ("candidate_profiles", "experience_years", "INTEGER DEFAULT 0"),
        ("candidate_profiles", "status", "VARCHAR(50) DEFAULT 'ACTIVE'"),
        ("candidate_profiles", "certifications", "TEXT"),
        ("candidate_profiles", "portfolio_url", "VARCHAR(255)"),
        ("candidate_profiles", "linkedin_url", "VARCHAR(255)"),
        ("candidate_profiles", "github_url", "VARCHAR(255)"),
        ("candidate_profiles", "other_links", "TEXT"),
        ("candidate_profiles", "created_by_recruiter_id", uuid_type),
        ("candidate_profiles", "source", "VARCHAR(100) DEFAULT 'direct_candidate'"),

        # ATS Screening & Composite Scores for applications
        ("applications", "ats_score", "FLOAT"),
        ("applications", "coding_score", "FLOAT"),
        ("applications", "interview_score", "FLOAT"),
        ("applications", "overall_score", "FLOAT"),
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
        ("applications", "uploaded_by_recruiter_id", uuid_type),
        ("applications", "source", "VARCHAR(100) DEFAULT 'direct_candidate'"),

        # Live Interview fields
        ("interviews", "duration_minutes", "INTEGER DEFAULT 30"),
        ("interviews", "camera_required", "BOOLEAN DEFAULT FALSE"),
        ("interviews", "adaptive", "BOOLEAN DEFAULT TRUE"),
        ("interviews", "live_transcript", "TEXT"),
        ("interviews", "expires_at", "TIMESTAMP"),

        # Email Logs extended fields
        ("email_logs", "provider_message_id", "VARCHAR(255)"),
        ("email_logs", "idempotency_key", "VARCHAR(255)"),
        ("email_logs", "retry_count", "INTEGER DEFAULT 0"),
        ("email_logs", "candidate_id", uuid_type),
        ("email_logs", "job_id", uuid_type),
        ("email_logs", "interview_id", uuid_type),
        ("email_logs", "failed_at", "TIMESTAMP"),

        # Coding Assessments proctoring & monitoring fields
        ("coding_assessments", "enable_tab_monitoring", "BOOLEAN DEFAULT TRUE"),
        ("coding_assessments", "enable_fullscreen", "BOOLEAN DEFAULT TRUE"),
        ("coding_assessments", "enable_webcam", "BOOLEAN DEFAULT TRUE"),
        ("coding_assessments", "enable_audio", "BOOLEAN DEFAULT TRUE"),
        ("coding_assessments", "enable_code_similarity", "BOOLEAN DEFAULT TRUE"),
        ("coding_assessments", "clipboard_policy", "VARCHAR(20) DEFAULT 'monitor'"),

        # Scheduled Interviews extended fields
        ("scheduled_interviews", "application_id", uuid_type),
        ("scheduled_interviews", "meeting_room_id", "VARCHAR(255)"),
        ("scheduled_interviews", "join_url", "TEXT"),
        ("scheduled_interviews", "recruiter_joined_at", "TIMESTAMP"),
        ("scheduled_interviews", "candidate_joined_at", "TIMESTAMP"),
        ("scheduled_interviews", "calendar_provider", "VARCHAR(50)"),
        ("scheduled_interviews", "calendar_event_id", "VARCHAR(255)"),
        ("scheduled_interviews", "calendar_event_url", "TEXT"),
        ("scheduled_interviews", "calendar_sync_status", "VARCHAR(50) DEFAULT 'synced'"),
        ("scheduled_interviews", "reminder_sent", "BOOLEAN DEFAULT FALSE"),
        ("scheduled_interviews", "reminder_24h_sent", "BOOLEAN DEFAULT FALSE"),
        ("scheduled_interviews", "reminder_1h_sent", "BOOLEAN DEFAULT FALSE"),
        ("scheduled_interviews", "invitation_sent", "BOOLEAN DEFAULT FALSE"),
        ("scheduled_interviews", "calendar_synced", "BOOLEAN DEFAULT FALSE"),
        ("scheduled_interviews", "cancelled_at", "TIMESTAMP"),
        ("scheduled_interviews", "cancellation_reason", "TEXT"),
        ("scheduled_interviews", "rescheduled_from_id", uuid_type),

        # Chat Audio Messages
        ("chat_messages", "is_audio", "BOOLEAN DEFAULT FALSE"),
        ("chat_messages", "audio_url", "VARCHAR(500)"),

        # Email Settings
        ("recruiter_email_settings", "candidate_selected", "BOOLEAN DEFAULT TRUE"),

        # Proctoring & Integrity monitoring extended fields
        ("assessment_events", "interview_id", uuid_type),
        ("assessment_events", "assessment_id", uuid_type),
        ("assessment_events", "duration_seconds", "FLOAT"),
        ("assessment_consents", "interview_id", uuid_type),
        ("integrity_results", "interview_id", uuid_type),
        ("integrity_results", "assessment_id", uuid_type),
    ]

    with active_engine.begin() as conn:
        inspector = inspect(conn)
        for table, col, col_type in columns_to_ensure:
            try:
                if inspector.has_table(table):
                    cols_info = {r["name"]: r for r in inspector.get_columns(table)}
                    if col not in cols_info:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}"))
                        logging.info(f"Auto-migrated: Added {col} to {table}")
                    elif is_pg and col_type == "UUID":
                        current_type = str(cols_info[col]["type"]).lower()
                        if "varchar" in current_type or "char" in current_type:
                            conn.execute(text(f"ALTER TABLE {table} ALTER COLUMN {col} TYPE UUID USING (NULLIF({col}, '')::UUID)"))
                            logging.info(f"Auto-migrated: Converted {table}.{col} to UUID")
            except Exception as e:
                logging.warning(f"Auto-migration check for {table}.{col} skipped: {e}")

        # Relax attempt_id NOT NULL for proctoring tables so interview events can be stored without an attempt_id
        if is_pg:
            for p_table in ["assessment_events", "assessment_consents", "integrity_results"]:
                try:
                    if inspector.has_table(p_table):
                        conn.execute(text(f"ALTER TABLE {p_table} ALTER COLUMN attempt_id DROP NOT NULL"))
                except Exception as e:
                    logging.warning(f"Could not drop NOT NULL on {p_table}.attempt_id: {e}")


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

    try:
        from app.services.redis_service import init_redis_client
        init_redis_client()
    except Exception as err:
        logging.getLogger("ai_recruiter").warning(f"Redis initialization notice: {err}")

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
app.include_router(candidate_search.recruiter_candidates_router, prefix="/api/v1")
app.include_router(coding.router, prefix="/api/v1")
app.include_router(interview_ws.router, prefix="/api/v1")
app.include_router(calendar.router, prefix="/api/v1")
app.include_router(email_settings.router, prefix="/api/v1")
app.include_router(screening.router, prefix="/api/v1")
app.include_router(proctoring.router, prefix="/api/v1")
app.include_router(interview_scorecard_router.router, prefix="/api/v1")
app.include_router(talent_rediscovery_router.router, prefix="/api/v1")
app.include_router(feedback_router.router)

# Serve frontend HTML pages statically for direct verification / reset links
_frontend_dir = Path(__file__).parent.parent.parent / "frontend-html"
if _frontend_dir.exists():
    from fastapi.responses import FileResponse
    @app.get("/{page_name}.html", include_in_schema=False)
    def serve_frontend_page(page_name: str):
        file_path = _frontend_dir / f"{page_name}.html"
        if file_path.exists():
            return FileResponse(str(file_path))
        from fastapi.exceptions import HTTPException
        raise HTTPException(status_code=404, detail="Page not found")

    app.mount("/static-frontend", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend-html")

# Serve uploaded files (e.g. audio messages, resumes, logos)
_uploads_dir = Path(__file__).parent.parent / "uploads"
_uploads_dir.mkdir(parents=True, exist_ok=True)
(_uploads_dir / "audio_messages").mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_uploads_dir)), name="uploads")

def root():
    return {"success": True, "message": f"{settings.APP_NAME} API is running", "data": {"version": "0.1.0"}}


@app.get("/health", tags=["Health"])
def health():
    return {"success": True, "message": "healthy", "data": {"environment": settings.ENVIRONMENT}}


@app.get("/api/v1/system/status", tags=["System Status"])
def system_status():
    from app.core.database import get_db_status
    from app.services.redis_service import get_redis_status

    db_info = get_db_status()
    redis_info = get_redis_status()

    return {
        "success": True,
        "message": "System status retrieved successfully",
        "data": {
            "app_name": settings.APP_NAME,
            "environment": settings.ENVIRONMENT,
            "databases": {
                "active_engine": db_info.get("dialect"),
                "is_postgres_active": db_info.get("is_postgres"),
                "is_sqlite_active": db_info.get("is_sqlite"),
                "connected": db_info.get("connected"),
                "active_url": db_info.get("active_url"),
                "supported": ["postgresql", "sqlite"],
            },
            "redis_cache": {
                "enabled": redis_info.get("enabled"),
                "connected": redis_info.get("connected"),
                "backend_type": redis_info.get("backend_type"),
                "keys_cached": redis_info.get("keys_cached", 0),
                "host": redis_info.get("host"),
                "port": redis_info.get("port"),
            },
        },
    }

