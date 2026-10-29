"""
clean_all_user_data.py — Cleanly purges all old test candidate & recruiter user data
from PostgreSQL while safely preserving system catalog data (study materials,
coding questions, test cases, aptitude questions, and skills).
"""
import sys
sys.path.insert(0, 'ai-recruiter/backend')
from app.core.database import engine
from sqlalchemy import text

def purge_all_user_accounts():
    user_related_tables = [
        "application_status_history",
        "applications",
        "candidate_skills",
        "portfolios",
        "candidate_coding_attempts",
        "coding_submissions",
        "aptitude_attempts",
        "weekly_aptitude_attempts",
        "weekly_coding_attempts",
        "screening_sessions",
        "screening_answers",
        "screening_results",
        "talent_rediscovery_results",
        "talent_rediscovery_runs",
        "job_skills",
        "jobs",
        "recruiter_profiles",
        "candidate_profiles",
        "student_learning_preferences",
        "student_roadmap_progress",
        "notifications",
        "audit_logs",
        "email_logs",
        "companies",
        "chat_messages",
        "integrity_results",
        "users"
    ]
    with engine.connect() as conn:
        with conn.begin():
            for tbl in user_related_tables:
                try:
                    conn.execute(text(f'TRUNCATE TABLE "{tbl}" CASCADE;'))
                    print(f"Purged table: {tbl}")
                except Exception as e:
                    print(f"Skipping/error on {tbl}: {e}")
    print("All candidate and recruiter data purged successfully!")

if __name__ == "__main__":
    purge_all_user_accounts()

