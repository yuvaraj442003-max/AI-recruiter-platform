"""
cleanup_fake_data.py
---------------------
Deletes ALL demo/fake data from the Postgres database.

Run from the backend/ directory:
    venv\\Scripts\\python.exe cleanup_fake_data.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv('.env')

import psycopg2
from psycopg2.extras import register_uuid

register_uuid()

DEMO_EMAILS = [
    'recruiter1@techcorp.com',
    'recruiter2@innovate.io',
    'alice@example.com',
    'bob@example.com',
    'charlie@example.com',
    'diana@example.com',
    'evan@example.com',
]

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='ai_recruiter',
    user='postgres',
    password='postgres234'
)
conn.autocommit = False
c = conn.cursor()

print("=== Checking for demo accounts ===")
c.execute("SELECT id, name, email, role FROM users WHERE email = ANY(%s)", (DEMO_EMAILS,))
demo_users = c.fetchall()
print(f"Found {len(demo_users)} demo users in DB.")
for u in demo_users:
    print(f"  {u[2]} ({u[3]})")

if not demo_users:
    print("No demo users found. Nothing to clean up.")
    conn.close()
    sys.exit(0)

demo_user_ids = [u[0] for u in demo_users]

try:
    print("\n=== Deleting demo data ===")

    # Get candidate profile IDs
    c.execute("SELECT id FROM candidate_profiles WHERE user_id = ANY(%s::uuid[])", (demo_user_ids,))
    demo_cp_ids = [r[0] for r in c.fetchall()]
    print(f"  Demo candidate profiles: {len(demo_cp_ids)}")

    # Get application IDs
    demo_app_ids = []
    if demo_cp_ids:
        c.execute("SELECT id FROM applications WHERE candidate_id = ANY(%s::uuid[])", (demo_cp_ids,))
        demo_app_ids = [r[0] for r in c.fetchall()]
        print(f"  Demo applications: {len(demo_app_ids)}")

    # Get job IDs
    c.execute("SELECT id FROM jobs WHERE recruiter_id = ANY(%s::uuid[])", (demo_user_ids,))
    demo_job_ids = [r[0] for r in c.fetchall()]
    print(f"  Demo jobs: {len(demo_job_ids)}")

    # Get interview IDs
    demo_interview_ids = []
    if demo_app_ids:
        c.execute("SELECT id FROM interviews WHERE application_id = ANY(%s::uuid[])", (demo_app_ids,))
        demo_interview_ids = [r[0] for r in c.fetchall()]
        print(f"  Demo interviews: {len(demo_interview_ids)}")

    # --- Delete in correct dependency order ---

    # 1. Chat messages
    c.execute(
        "DELETE FROM chat_messages WHERE sender_id = ANY(%s::uuid[]) OR receiver_id = ANY(%s::uuid[])",
        (demo_user_ids, demo_user_ids)
    )
    print(f"  Deleted {c.rowcount} chat messages")

    # 2. Interview scorecards and their children
    if demo_interview_ids:
        # Get scorecard IDs
        c.execute("SELECT id FROM interview_scorecards WHERE interview_id = ANY(%s::uuid[])", (demo_interview_ids,))
        scorecard_ids = [r[0] for r in c.fetchall()]
        if scorecard_ids:
            c.execute("DELETE FROM interview_key_moments WHERE scorecard_id = ANY(%s::uuid[])", (scorecard_ids,))
            print(f"  Deleted {c.rowcount} interview key moments")
            c.execute("DELETE FROM interview_question_evaluations WHERE scorecard_id = ANY(%s::uuid[])", (scorecard_ids,))
            print(f"  Deleted {c.rowcount} interview question evaluations")
            c.execute("DELETE FROM interview_chapters WHERE scorecard_id = ANY(%s::uuid[])", (scorecard_ids,))
            print(f"  Deleted {c.rowcount} interview chapters")
            c.execute("DELETE FROM interview_score_categories WHERE scorecard_id = ANY(%s::uuid[])", (scorecard_ids,))
            print(f"  Deleted {c.rowcount} interview score categories")
            c.execute("DELETE FROM interview_scorecards WHERE id = ANY(%s::uuid[])", (scorecard_ids,))
            print(f"  Deleted {c.rowcount} interview scorecards")

        # Interview evaluations
        c.execute("DELETE FROM interview_evaluations WHERE interview_id = ANY(%s::uuid[])", (demo_interview_ids,))
        print(f"  Deleted {c.rowcount} interview evaluations")

        # Interview questions and answers
        c.execute("SELECT id FROM interview_questions WHERE interview_id = ANY(%s::uuid[])", (demo_interview_ids,))
        q_ids = [r[0] for r in c.fetchall()]
        if q_ids:
            c.execute("DELETE FROM interview_answers WHERE question_id = ANY(%s::uuid[])", (q_ids,))
            print(f"  Deleted {c.rowcount} interview answers")
            c.execute("DELETE FROM interview_questions WHERE id = ANY(%s::uuid[])", (q_ids,))
            print(f"  Deleted {c.rowcount} interview questions")

        # Interviews themselves
        c.execute("DELETE FROM interviews WHERE id = ANY(%s::uuid[])", (demo_interview_ids,))
        print(f"  Deleted {c.rowcount} interviews")

    # 3. Screening data for demo applications
    if demo_app_ids:
        # Get screening session IDs first
        c.execute("SELECT id FROM screening_sessions WHERE application_id = ANY(%s::uuid[])", (demo_app_ids,))
        sess_ids = [r[0] for r in c.fetchall()]
        if sess_ids:
            c.execute("DELETE FROM screening_answers WHERE screening_session_id = ANY(%s::uuid[])", (sess_ids,))
            print(f"  Deleted {c.rowcount} screening answers")
            c.execute("DELETE FROM screening_results WHERE screening_session_id = ANY(%s::uuid[])", (sess_ids,))
            print(f"  Deleted {c.rowcount} screening results")
            c.execute("DELETE FROM screening_sessions WHERE id = ANY(%s::uuid[])", (sess_ids,))
            print(f"  Deleted {c.rowcount} screening sessions")
        c.execute("DELETE FROM application_status_history WHERE application_id = ANY(%s::uuid[])", (demo_app_ids,))
        print(f"  Deleted {c.rowcount} application status histories")
        c.execute("DELETE FROM applications WHERE candidate_id = ANY(%s::uuid[])", (demo_cp_ids,))
        print(f"  Deleted {c.rowcount} applications")

    # 4. Jobs and job-related data
    if demo_job_ids:
        c.execute("DELETE FROM job_skills WHERE job_id = ANY(%s::uuid[])", (demo_job_ids,))
        print(f"  Deleted {c.rowcount} job skills")
        # screening_questions linked to sessions (already deleted above), not jobs directly
        c.execute("DELETE FROM candidate_invitations WHERE job_id = ANY(%s::uuid[])", (demo_job_ids,))
        print(f"  Deleted {c.rowcount} candidate invitations")
        c.execute("DELETE FROM candidate_shortlists WHERE job_id = ANY(%s::uuid[])", (demo_job_ids,))
        print(f"  Deleted {c.rowcount} candidate shortlists")
        c.execute("DELETE FROM saved_candidate_searches WHERE job_id = ANY(%s::uuid[])", (demo_job_ids,))
        print(f"  Deleted {c.rowcount} saved candidate searches")
        c.execute("DELETE FROM jobs WHERE id = ANY(%s::uuid[])", (demo_job_ids,))
        print(f"  Deleted {c.rowcount} jobs")

    # 5. Candidate skills and profiles
    if demo_cp_ids:
        c.execute("DELETE FROM candidate_skills WHERE candidate_id = ANY(%s::uuid[])", (demo_cp_ids,))
        print(f"  Deleted {c.rowcount} candidate skills")
        c.execute("DELETE FROM candidate_profiles WHERE id = ANY(%s::uuid[])", (demo_cp_ids,))
        print(f"  Deleted {c.rowcount} candidate profiles")

    # 6. Recruiter profiles
    c.execute("DELETE FROM recruiter_profiles WHERE user_id = ANY(%s::uuid[])", (demo_user_ids,))
    print(f"  Deleted {c.rowcount} recruiter profiles")

    # 7. Notifications and audit logs
    c.execute("DELETE FROM notifications WHERE user_id = ANY(%s::uuid[])", (demo_user_ids,))
    print(f"  Deleted {c.rowcount} notifications")
    c.execute("DELETE FROM audit_logs WHERE user_id = ANY(%s::uuid[])", (demo_user_ids,))
    print(f"  Deleted {c.rowcount} audit logs")

    # 8. Delete demo user accounts
    c.execute("DELETE FROM users WHERE email = ANY(%s)", (DEMO_EMAILS,))
    print(f"  Deleted {c.rowcount} demo user accounts")

    conn.commit()
    print("\nSUCCESS: All demo/fake data deleted from the database!")

    # Final state
    c.execute("SELECT name, email, role FROM users ORDER BY created_at")
    remaining = c.fetchall()
    print(f"\nRemaining {len(remaining)} real users:")
    for u in remaining:
        print(f"  {u[0]} <{u[1]}> [{u[2]}]")

    c.execute("SELECT title, company_name, status FROM jobs")
    remaining_jobs = c.fetchall()
    print(f"\nRemaining {len(remaining_jobs)} jobs:")
    for j in remaining_jobs:
        print(f"  {j[0]} @ {j[1]} [{j[2]}]")

    c.execute("SELECT count(*) FROM chat_messages")
    print(f"\nRemaining chat messages: {c.fetchone()[0]}")

except Exception as e:
    conn.rollback()
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
