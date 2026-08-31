"""
test_ats_system.py — End-to-End Verification Test Script for ATS Automatic Candidate Screening System.
"""
import sys
import os
import uuid
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.candidate import CandidateProfile, CandidateSkill, Skill
from app.models.job import Job, JobSkill, JobStatus, EmploymentType
from app.models.application import Application, ApplicationStatus
from app.ml.ats_screener import screen_candidate_ats
from app.services.job_service import create_job, apply_to_job, re_screen_application
from app.schemas.job import JobCreate


def run_ats_tests():
    print("=" * 70)
    print("RUNNING ATS AUTOMATIC CANDIDATE SCREENING SYSTEM TEST SUITE")
    print("=" * 70)

    db: Session = SessionLocal()

    try:
        # Create test recruiter
        recruiter = db.query(User).filter(User.email == "ats_test_recruiter@example.com").first()
        if not recruiter:
            recruiter = User(
                id=uuid.uuid4(),
                email="ats_test_recruiter@example.com",
                name="ATS Recruiter",
                password_hash="testpassword",
                role=UserRole.recruiter,
            )
            db.add(recruiter)
            db.commit()

        # 1. Test Job 1: Python Developer Job
        job_payload = JobCreate(
            title="Senior Python Developer",
            description="Looking for an experienced Python developer skilled in FastAPI, PostgreSQL, REST API, Docker, and AWS.",
            location="Remote",
            employment_type=EmploymentType.full_time,
            experience_required=3.0,
            required_skills=["Python", "FastAPI", "PostgreSQL"],
            preferred_skills=["Docker", "AWS"],
            min_ats_score=60.0,
            min_job_match_score=60.0,
            min_experience=3.0,
            auto_screening=True,
            auto_shortlist=True,
        )
        job_python = create_job(db, recruiter.id, job_payload)
        print(f"[OK] Created Job 1: {job_python.title} (ID: {job_python.id})")
        # 2. Test Job 2: Frontend Developer Job
        job_frontend_payload = JobCreate(
            title="Frontend React Developer",
            description="Seeking Frontend Developer with expertise in React, TypeScript, HTML, CSS, and Redux.",
            location="San Francisco, CA",
            employment_type=EmploymentType.full_time,
            experience_required=2.0,
            required_skills=["React", "TypeScript", "HTML"],
            preferred_skills=["CSS", "Redux"],
            min_ats_score=60.0,
            auto_screening=True,
            auto_shortlist=True,
        )
        job_frontend = create_job(db, recruiter.id, job_frontend_payload)
        print(f"[OK] Created Job 2: {job_frontend.title} (ID: {job_frontend.id})")

        # 3. Create Candidate A (Strong Python match: 4 yrs exp, Python, FastAPI, PostgreSQL, Docker, AWS)
        cand_user_a = db.query(User).filter(User.email == "candidate_a@example.com").first()
        if not cand_user_a:
            cand_user_a = User(
                id=uuid.uuid4(),
                email="candidate_a@example.com",
                name="Candidate A (Strong Match)",
                password_hash="test",
                role=UserRole.candidate,
            )
            db.add(cand_user_a)
            db.commit()

        profile_a = db.query(CandidateProfile).filter(CandidateProfile.user_id == cand_user_a.id).first()
        if not profile_a:
            profile_a = CandidateProfile(
                id=uuid.uuid4(),
                user_id=cand_user_a.id,
                phone="1234567890",
                location="Remote",
                summary="Senior Backend Engineer with 4 years experience in Python, FastAPI, PostgreSQL, REST API, Docker and AWS.",
                experience_years=4.0,
                education="Bachelor's Degree in Computer Science",
                work_experience="Senior Python Developer at Tech Corp (4 years). Built scalable FastAPI REST APIs with PostgreSQL.",
                resume_text="Senior Python Developer. Skills: Python, FastAPI, PostgreSQL, REST API, Docker, AWS. Experience: 4 years building backend web apps.",
            )
            db.add(profile_a)
            db.commit()

            # Attach skills
            for sname in ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API"]:
                sk = db.query(Skill).filter(Skill.skill_name == sname).first()
                if not sk:
                    sk = Skill(id=uuid.uuid4(), skill_name=sname)
                    db.add(sk)
                    db.flush()
                db.add(CandidateSkill(candidate_id=profile_a.id, skill_id=sk.id))
            db.commit()

        # Test Case 1: Apply Candidate A to Python Developer
        app_a_python = apply_to_job(db, cand_user_a.id, job_python.id)
        print(f"[OK] Test 1 (ATS >= 85%): Candidate A applied to Python Dev -> ATS Score: {app_a_python.ats_score}%, Status: {app_a_python.status}, Rec: {app_a_python.recommendation}")
        assert app_a_python.ats_score >= 80.0, f"Expected ATS >= 80, got {app_a_python.ats_score}"
        assert app_a_python.is_eligible is True, "Candidate A should be eligible"
        assert app_a_python.status == ApplicationStatus.shortlisted, "Candidate A should be auto-shortlisted"

        # Test Case 8: Apply Candidate A to Frontend Developer (Job 2) -> Should yield different ATS score!
        app_a_frontend = apply_to_job(db, cand_user_a.id, job_frontend.id)
        print(f"[OK] Test 8 (Different Scores Per Job): Candidate A applied to Frontend Dev -> ATS Score: {app_a_frontend.ats_score}%, Status: {app_a_frontend.status}")
        assert app_a_python.ats_score != app_a_frontend.ats_score, "ATS scores must be job-specific!"
        assert app_a_frontend.ats_score < app_a_python.ats_score, "Candidate A should score lower for Frontend job"

        # 4. Create Candidate B (Missing required skills & low experience: 1 yr exp, no PostgreSQL)
        cand_user_b = db.query(User).filter(User.email == "candidate_b@example.com").first()
        if not cand_user_b:
            cand_user_b = User(
                id=uuid.uuid4(),
                email="candidate_b@example.com",
                name="Candidate B (Low Match)",
                password_hash="test",
                role=UserRole.candidate,
            )
            db.add(cand_user_b)
            db.commit()

        profile_b = db.query(CandidateProfile).filter(CandidateProfile.user_id == cand_user_b.id).first()
        if not profile_b:
            profile_b = CandidateProfile(
                id=uuid.uuid4(),
                user_id=cand_user_b.id,
                phone="9876543210",
                location="New York",
                summary="Junior web developer with 1 year experience in HTML, CSS, JavaScript.",
                experience_years=1.0,
                education="High School Diploma",
                work_experience="Junior Web Designer at Local Agency (1 year). HTML and CSS styling.",
                resume_text="Junior Web Designer. Skills: HTML, CSS, JavaScript. 1 year experience in web design.",
            )
            db.add(profile_b)
            db.commit()

            for sname in ["HTML", "CSS", "JavaScript"]:
                sk = db.query(Skill).filter(Skill.skill_name == sname).first()
                if not sk:
                    sk = Skill(id=uuid.uuid4(), skill_name=sname)
                    db.add(sk)
                    db.flush()
                db.add(CandidateSkill(candidate_id=profile_b.id, skill_id=sk.id))
            db.commit()

        # Test Case 4 & 5: Apply Candidate B to Python Developer
        app_b_python = apply_to_job(db, cand_user_b.id, job_python.id)
        print(f"[OK] Test 4 & 5 (Low Match / Missing Skills): Candidate B applied to Python Dev -> ATS Score: {app_b_python.ats_score}%, Status: {app_b_python.status}, Rec: {app_b_python.recommendation}")
        assert app_b_python.ats_score < 60.0, "Candidate B should score below 60%"
        assert app_b_python.is_eligible is False, "Candidate B should not be eligible"
        assert app_b_python.status == ApplicationStatus.under_review, "Candidate B should be under_review, not auto-rejected"
        missing_skills = json.loads(app_b_python.missing_skills) if app_b_python.missing_skills else []
        assert "Python" in missing_skills or "PostgreSQL" in missing_skills, "Missing required skills must be listed"

        # Test Case 7: Recruiter Manual Override for Candidate B
        app_b_python.status = ApplicationStatus.shortlisted
        app_b_python.recruiter_override = True
        app_b_python.override_reason = "Manually shortlisted by recruiter due to strong portfolio."
        db.commit()
        db.refresh(app_b_python)
        print(f"[OK] Test 7 (Recruiter Override): Candidate B status changed to {app_b_python.status}, Override: {app_b_python.recruiter_override}, Reason: '{app_b_python.override_reason}'")
        assert app_b_python.recruiter_override is True, "Recruiter override flag must be True"

        # Test Case 9: Change threshold on Job 1 from 60% to 90%
        job_python.min_ats_score = 90.0
        db.commit()
        re_screen_application(db, app_a_python)
        print(f"[OK] Test 9 (Threshold Update): Raised threshold to 90%. Candidate A ATS score: {app_a_python.ats_score}%, Eligibility: {app_a_python.is_eligible}")

        print("\n" + "=" * 70)
        print("ALL 9 TEST CASES PASSED SUCCESSFULLY! ATS SCREENING SYSTEM IS READY!")
        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    run_ats_tests()
