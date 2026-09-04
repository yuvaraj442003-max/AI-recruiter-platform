"""
seed_demo_data.py — Idempotent script to seed rich demo & development data.
Generates 2 recruiters, 5 candidates, 5 jobs (Software Engineer, Data Scientist, DevOps Engineer, UI/UX Designer, HR Recruiter), candidate profiles, skills, applications, interview records, evaluations, and message threads.
"""
import sys
import os
import uuid
from datetime import datetime, timezone

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.recruiter import RecruiterProfile
from app.models.candidate import CandidateProfile, Skill, CandidateSkill
from app.models.job import Job, JobSkill
from app.models.application import Application
from app.models.interview import Interview, InterviewQuestion, InterviewAnswer, InterviewEvaluation
from app.models.message import ChatMessage
from app.services.resume_service import seed_skills


def seed_demo():
    print("[*] Starting AI Recruiter Demo Data Seeding...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Seed skills
        seed_skills(db)

        # Shared demo password: Password123!
        pass_hash = hash_password("Password123!")

        # 1. Create 2 Recruiters
        recruiters_data = [
            {
                "email": "recruiter1@techcorp.com",
                "name": "Sarah Connor",
                "role": UserRole.recruiter,
                "company_name": "TechCorp Solutions",
                "job_title": "Senior Technical Recruiter",
                "company_website": "https://techcorp.example.com",
            },
            {
                "email": "recruiter2@innovate.io",
                "name": "David Miller",
                "role": UserRole.recruiter,
                "company_name": "Innovate AI Lab",
                "job_title": "Head of Talent Acquisition",
                "company_website": "https://innovate.example.com",
            }
        ]

        recruiter_users = []
        for rdata in recruiters_data:
            u = db.query(User).filter(User.email == rdata["email"]).first()
            if not u:
                u = User(
                    email=rdata["email"],
                    password_hash=pass_hash,
                    name=rdata["name"],
                    role=rdata["role"],
                    is_active=True,
                    is_email_verified=True,
                )
                db.add(u)
                db.commit()
                db.refresh(u)
                print(f"  [+] Created Recruiter user: {u.email}")

            rp = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == u.id).first()
            if not rp:
                rp = RecruiterProfile(
                    user_id=u.id,
                    company_name=rdata["company_name"],
                    job_title=rdata["job_title"],
                    website=rdata["company_website"],
                    company_size="50-200",
                    industry="Software & Technology",
                )
                db.add(rp)
                db.commit()

            recruiter_users.append(u)

        # 2. Create 5 Candidates
        candidates_data = [
            {
                "email": "alice@example.com",
                "name": "Alice Johnson",
                "headline": "Senior Full-Stack Software Engineer (Python & React)",
                "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Git"],
                "exp_years": 5.5,
                "education": "B.S. Computer Science, Stanford University",
                "summary": "Experienced full-stack developer with expertise in building scalable APIs and modern web applications.",
                "ats_score": 88
            },
            {
                "email": "bob@example.com",
                "name": "Bob Smith",
                "headline": "Data Scientist & Machine Learning Specialist",
                "skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "SQL", "Pandas"],
                "exp_years": 4.0,
                "education": "M.S. Data Science, MIT",
                "summary": "Data scientist specializing in NLP, predictive modeling, and deep learning algorithms.",
                "ats_score": 82
            },
            {
                "email": "charlie@example.com",
                "name": "Charlie Davis",
                "headline": "Lead DevOps & Cloud Engineer (AWS / Kubernetes)",
                "skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Linux", "Python"],
                "exp_years": 6.5,
                "education": "B.S. Information Technology, UC Berkeley",
                "summary": "Cloud operations engineer focused on infrastructure automation, Kubernetes orchestration, and zero-downtime deployments.",
                "ats_score": 90
            },
            {
                "email": "diana@example.com",
                "name": "Diana Prince",
                "headline": "Lead Product & UI/UX Designer",
                "skills": ["Figma", "UI/UX", "User Research", "Wireframing", "Prototyping", "Design Systems"],
                "exp_years": 4.5,
                "education": "B.F.A. Interactive Design, RISD",
                "summary": "User-centric UI/UX designer passionate about clean typography, accessibility, and high-converting candidate flows.",
                "ats_score": 85
            },
            {
                "email": "evan@example.com",
                "name": "Evan Wright",
                "headline": "Senior Technical HR Recruiter",
                "skills": ["Technical Recruiting", "Sourcing", "Interviews", "ATS", "Talent Acquisition"],
                "exp_years": 5.0,
                "education": "B.A. Psychology & HR, NYU",
                "summary": "People-first talent recruiter with a proven track record of placing top engineering talent at high-growth startups.",
                "ats_score": 80
            }
        ]

        candidate_users = []
        candidate_profiles = []
        for cdata in candidates_data:
            u = db.query(User).filter(User.email == cdata["email"]).first()
            if not u:
                u = User(
                    email=cdata["email"],
                    password_hash=pass_hash,
                    name=cdata["name"],
                    role=UserRole.candidate,
                    is_active=True,
                    is_email_verified=True,
                )
                db.add(u)
                db.commit()
                db.refresh(u)
                print(f"  [+] Created Candidate user: {u.email}")

            cp = db.query(CandidateProfile).filter(CandidateProfile.user_id == u.id).first()
            if not cp:
                cp = CandidateProfile(
                    user_id=u.id,
                    headline=cdata["headline"],
                    current_role=cdata["headline"].split("(")[0].strip(),
                    experience_years=cdata["exp_years"],
                    education=cdata["education"],
                    summary=cdata["summary"],
                    location="San Francisco, CA",
                    profile_score=cdata["ats_score"],
                )
                db.add(cp)
                db.commit()
                db.refresh(cp)

                # Seed Candidate Skills
                for sk_name in cdata["skills"]:
                    sk_row = db.query(Skill).filter(Skill.skill_name == sk_name).first()
                    if not sk_row:
                        sk_row = Skill(skill_name=sk_name, category="General")
                        db.add(sk_row)
                        db.commit()
                        db.refresh(sk_row)
                    db.add(CandidateSkill(candidate_id=cp.id, skill_id=sk_row.id, proficiency="Advanced"))
                db.commit()

            candidate_users.append(u)
            candidate_profiles.append(cp)

        # 3. Create 5 Jobs
        jobs_data = [
            {
                "title": "Software Engineer",
                "recruiter": recruiter_users[0],
                "desc": "We are seeking a talented Senior Software Engineer to build robust FastAPI microservices and modern React user interfaces. Experience with PostgreSQL and Docker required.",
                "location": "San Francisco, CA (Remote)",
                "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
                "exp_min": 3.5,
                "relevant_exp": "3+ years of hands-on experience building REST APIs, microservices architectures, and full-stack web applications in Cloud or SaaS software environments.",
                "non_tech_skills": "Problem Solving, System Architecture, Code Review, Team Leadership, Agile/Scrum",
                "company_exp": "Experience working in High-Growth Tech Startups, Tier-1 Product Companies, or Scaled Engineering Enterprises.",
            },
            {
                "title": "Data Scientist",
                "recruiter": recruiter_users[1],
                "desc": "Join our AI research team to develop state-of-the-art NLP and machine learning models for predictive candidate matching.",
                "location": "New York, NY (Hybrid)",
                "skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn"],
                "exp_min": 2.5,
                "relevant_exp": "2+ years of experience training predictive machine learning models, NLP transformers, and feature engineering for production data pipelines.",
                "non_tech_skills": "Statistical Analysis, Critical Thinking, AI Ethics, Cross-functional Collaboration",
                "company_exp": "Experience in AI Research Labs, FinTech Analytics, or Data-driven SaaS organizations.",
            },
            {
                "title": "DevOps Engineer",
                "recruiter": recruiter_users[0],
                "desc": "Architect and maintain enterprise Kubernetes clusters, Terraform infrastructure, and automated CI/CD pipelines.",
                "location": "Austin, TX (Remote)",
                "skills": ["Docker", "Kubernetes", "AWS", "Terraform"],
                "exp_min": 4.0,
                "relevant_exp": "4+ years maintaining high-availability AWS cloud infrastructure, Docker containers, Kubernetes orchestrations, and GitOps CI/CD pipelines.",
                "non_tech_skills": "Incident Management, Infrastructure Reliability, Security Compliance, Technical Documentation",
                "company_exp": "Experience in Enterprise Cloud Providers, Managed DevOps Providers, or FinTech scale-ups.",
            },
            {
                "title": "UI/UX Designer",
                "recruiter": recruiter_users[1],
                "desc": "Design intuitive design systems, interactive Figma wireframes, and delightful user journeys for our recruitment platform.",
                "location": "Remote",
                "skills": ["Figma", "UI/UX", "User Research", "Prototyping"],
                "exp_min": 2.0,
                "relevant_exp": "2+ years designing SaaS web products, complex user workflows, design systems, and conducting user interviews.",
                "non_tech_skills": "User Empathy, Visual Storytelling, Design Thinking, Stakeholder Communication",
                "company_exp": "Experience in B2B SaaS Product Design, Digital Agencies, or Consumer Web Startups.",
            },
            {
                "title": "HR Recruiter",
                "recruiter": recruiter_users[0],
                "desc": "Lead candidate sourcing, screening, and end-to-end interviewing for key technical engineering requisitions.",
                "location": "San Francisco, CA",
                "skills": ["Technical Recruiting", "Sourcing", "Interviews"],
                "exp_min": 3.0,
                "relevant_exp": "3+ years of technical recruiting experience sourcing software engineers, data scientists, and cloud architects.",
                "non_tech_skills": "Candidate Negotiation, Active Listening, Talent Pipeline Management, Employer Branding",
                "company_exp": "Experience in Tech Recruitment Agencies, In-house Talent Acquisition for Venture-backed Tech companies.",
            }
        ]

        jobs_list = []
        for jdata in jobs_data:
            j = db.query(Job).filter(Job.title == jdata["title"], Job.recruiter_id == jdata["recruiter"].id).first()
            if not j:
                j = Job(
                    recruiter_id=jdata["recruiter"].id,
                    title=jdata["title"],
                    description=jdata["desc"],
                    location=jdata["location"],
                    employment_type="full_time",
                    experience_required=jdata["exp_min"],
                    relevant_work_experience=jdata["relevant_exp"],
                    non_technical_skills=jdata["non_tech_skills"],
                    company_experience_requirements=jdata["company_exp"],
                    company_name=jdata["recruiter"].name + "'s Team",
                    status="published",
                )
                db.add(j)
                db.commit()
                db.refresh(j)
                print(f"  [+] Created Job: {j.title}")
            else:
                j.experience_required = jdata["exp_min"]
                j.relevant_work_experience = jdata["relevant_exp"]
                j.non_technical_skills = jdata["non_tech_skills"]
                j.company_experience_requirements = jdata["company_exp"]
                db.commit()
                db.refresh(j)
                print(f"  [+] Created Job: {j.title}")

                for sk in jdata["skills"]:
                    sk_row = db.query(Skill).filter(Skill.skill_name == sk).first()
                    if not sk_row:
                        sk_row = Skill(skill_name=sk, category="General")
                        db.add(sk_row)
                        db.commit()
                        db.refresh(sk_row)
                    js_row = db.query(JobSkill).filter(JobSkill.job_id == j.id, JobSkill.skill_id == sk_row.id).first()
                    if not js_row:
                        db.add(JobSkill(job_id=j.id, skill_id=sk_row.id, required=True))
                db.commit()

            jobs_list.append(j)

        # 4. Create Applications, Match Scores & Interviews
        app1 = db.query(Application).filter(Application.candidate_id == candidate_profiles[0].id, Application.job_id == jobs_list[0].id).first()
        if not app1:
            app1 = Application(
                candidate_id=candidate_profiles[0].id,
                job_id=jobs_list[0].id,
                match_score=92.5,
                match_breakdown='{"explanation": "Strong skill match on Python, FastAPI, React and PostgreSQL", "breakdown": {"skill": 95, "experience": 90, "tfidf": 92, "semantic": 91}}',
                status="shortlisted",
            )
            db.add(app1)
            db.commit()
            db.refresh(app1)
            print(f"  [+] Created Application: {candidate_users[0].name} -> {jobs_list[0].title}")

        app2 = db.query(Application).filter(Application.candidate_id == candidate_profiles[1].id, Application.job_id == jobs_list[1].id).first()
        if not app2:
            app2 = Application(
                candidate_id=candidate_profiles[1].id,
                job_id=jobs_list[1].id,
                match_score=88.0,
                match_breakdown='{"explanation": "Excellent alignment on Python, PyTorch and ML algorithms", "breakdown": {"skill": 90, "experience": 85, "tfidf": 87, "semantic": 89}}',
                status="shortlisted",
            )
            db.add(app2)
            db.commit()
            db.refresh(app2)

        # Create completed AI Interview for Alice
        inv1 = db.query(Interview).filter(Interview.application_id == app1.id).first()
        if not inv1:
            inv1 = Interview(
                application_id=app1.id,
                candidate_id=app1.candidate_id,
                job_id=app1.job_id,
                status="completed",
                completed_at=datetime.now(timezone.utc),
            )
            db.add(inv1)
            db.commit()
            db.refresh(inv1)

            # Questions & Answers
            q1 = InterviewQuestion(
                interview_id=inv1.id,
                question="Explain the difference between synchronous and asynchronous request handling in FastAPI.",
                question_type="technical",
                difficulty="medium",
                order_number=1,
            )
            q2 = InterviewQuestion(
                interview_id=inv1.id,
                question="How do you handle relational database migrations when altering core user tables?",
                question_type="problem_solving",
                difficulty="medium",
                order_number=2,
            )
            db.add_all([q1, q2])
            db.commit()
            db.refresh(q1)
            db.refresh(q2)

            ans1 = InterviewAnswer(
                question_id=q1.id,
                candidate_id=app1.candidate_id,
                answer_text="FastAPI leverages Python's asyncio event loop with async/await definitions, allowing non-blocking I/O operations for high concurrency.",
                answer_score=90.0,
            )
            ans2 = InterviewAnswer(
                question_id=q2.id,
                candidate_id=app1.candidate_id,
                answer_text="I use Alembic migrations to generate schema upgrade/downgrade scripts, testing them in staging before applying to production.",
                answer_score=88.0,
            )
            db.add_all([ans1, ans2])
            db.commit()

            # Evaluation
            eval1 = InterviewEvaluation(
                interview_id=inv1.id,
                overall_score=89.0,
                technical_score=91.0,
                relevance_score=88.0,
                communication_score=87.0,
                problem_solving_score=90.0,
                strengths='["Deep understanding of Python asyncio and FastAPI", "Clean approach to database migration safety"]',
                weaknesses='["Could elaborate more on automated unit test coverage"]',
                recommendation="Strong Candidate — Excellent technical mastery of modern Python backend architecture.",
            )
            db.add(eval1)
            db.commit()
            print(f"  [+] Created AI Interview Evaluation for {candidate_users[0].name}")

        # 5. Create Chat Messages
        msg1 = db.query(ChatMessage).filter(ChatMessage.sender_id == recruiter_users[0].id, ChatMessage.receiver_id == candidate_users[0].id).first()
        if not msg1:
            m1 = ChatMessage(
                sender_id=recruiter_users[0].id,
                receiver_id=candidate_users[0].id,
                application_id=app1.id,
                content="Hi Alice! Your profile and AI interview report for the Software Engineer position look fantastic. Are you available for a 15-minute introductory call?",
                is_read=True,
            )
            m2 = ChatMessage(
                sender_id=candidate_users[0].id,
                receiver_id=recruiter_users[0].id,
                application_id=app1.id,
                content="Hi Sarah! Thank you so much for reaching out. Yes, I am available tomorrow afternoon!",
                is_read=False,
            )
            db.add_all([m1, m2])
            db.commit()
            print("  [+] Created initial chat conversation between Recruiter and Candidate")

        print("[+] Demo Data Seeding Completed Successfully!")
        print("  [*] Demo Credentials:")
        print("     Recruiter 1: recruiter1@techcorp.com / Password123!")
        print("     Recruiter 2: recruiter2@innovate.io / Password123!")
        print("     Candidate 1: alice@example.com / Password123!")
        print("     Candidate 2: bob@example.com / Password123!")

    except Exception as e:
        db.rollback()
        print(f"[!] Error seeding demo data: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
