"""
analytics_service.py — aggregates existing data (jobs, applications,
interviews, skills) into dashboard-ready summaries. No new tables:
everything here is a query/aggregation over data the platform already
has, computed on request rather than cached, since dashboard traffic
is low-volume relative to the rest of the API.
"""
import uuid
from collections import Counter

from sqlalchemy.orm import Session, joinedload

from app.models.application import Application, ApplicationStatus
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.interview import Interview, InterviewStatus
from app.models.job import Job


import json
import datetime

def get_recruiter_analytics(
    db: Session,
    recruiter_id,
    job_id: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    status: str | None = None,
) -> dict:
    jobs = db.query(Job).filter(Job.recruiter_id == recruiter_id).all()

    if job_id and str(job_id).strip() and str(job_id).strip().lower() != "all":
        try:
            parsed_job_id = uuid.UUID(str(job_id).strip())
            jobs = [j for j in jobs if j.id == parsed_job_id]
        except ValueError:
            pass

    job_ids = [j.id for j in jobs]
    jobs_by_id = {j.id: j for j in jobs}

    app_query = (
        db.query(Application)
        .options(joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(Application.job_id.in_(job_ids))
        if job_ids
        else None
    )

    applications = app_query.all() if app_query is not None else []

    # Date filtering
    if start_date and str(start_date).strip():
        try:
            s_dt = datetime.datetime.fromisoformat(str(start_date).strip().replace("Z", "+00:00"))
            applications = [a for a in applications if a.applied_at and a.applied_at >= s_dt]
        except ValueError:
            pass

    if end_date and str(end_date).strip():
        try:
            e_dt = datetime.datetime.fromisoformat(str(end_date).strip().replace("Z", "+00:00"))
            applications = [a for a in applications if a.applied_at and a.applied_at <= e_dt]
        except ValueError:
            pass

    # Status filtering
    if status and str(status).strip() and str(status).strip().lower() != "all":
        target_st = str(status).strip().lower()
        applications = [
            a for a in applications
            if (a.status.value if hasattr(a.status, "value") else str(a.status)).lower() == target_st
        ]

    interviews = db.query(Interview).filter(Interview.job_id.in_(job_ids)).all() if job_ids else []
    completed_interviews = [i for i in interviews if i.status == InterviewStatus.completed]

    # Top-line stats
    total_jobs = len(jobs)
    published_jobs = sum(1 for j in jobs if (j.status.value if hasattr(j.status, "value") else str(j.status)) == "published")
    total_applications = len(applications)
    total_candidates = len({a.candidate_id for a in applications})

    # Funnel counts
    hired_count = sum(1 for a in applications if (a.status.value if hasattr(a.status, "value") else str(a.status)) == "selected")
    shortlisted_count = sum(
        1 for a in applications
        if (a.status.value if hasattr(a.status, "value") else str(a.status)) in ["shortlisted", "interview", "selected"] or a.is_shortlisted
    )
    interviewed_cand_ids = {i.candidate_id for i in interviews}
    interview_count = sum(
        1 for a in applications
        if (a.status.value if hasattr(a.status, "value") else str(a.status)) in ["interview", "selected"] or a.candidate_id in interviewed_cand_ids
    )

    conversion_rate = round((hired_count / total_applications * 100), 2) if total_applications > 0 else 0.0

    match_scores = [a.ats_score or a.match_score for a in applications if (a.ats_score or a.match_score) is not None]
    avg_match_score = round(sum(match_scores) / len(match_scores), 2) if match_scores else None

    # Hiring Funnel by DB status string (backwards-compatible)
    hiring_funnel = {st.value: 0 for st in ApplicationStatus}
    for a in applications:
        st_val = a.status.value if hasattr(a.status, "value") else str(a.status)
        hiring_funnel[st_val] = hiring_funnel.get(st_val, 0) + 1

    # Structured Funnel Stages (Applied -> Shortlisted -> Interviewed -> Hired)
    funnel_stages = {
        "Applied": total_applications,
        "Shortlisted": shortlisted_count,
        "Interviewed": interview_count,
        "Hired": hired_count,
    }

    # Match Score Distribution Histogram
    match_score_distribution = {
        "90_100": 0,
        "80_89": 0,
        "70_79": 0,
        "60_69": 0,
        "below_60": 0,
    }
    for score in match_scores:
        if score >= 90:
            match_score_distribution["90_100"] += 1
        elif score >= 80:
            match_score_distribution["80_89"] += 1
        elif score >= 70:
            match_score_distribution["70_79"] += 1
        elif score >= 60:
            match_score_distribution["60_69"] += 1
        else:
            match_score_distribution["below_60"] += 1

    # Top Missing Skills Analysis
    missing_skill_counter: Counter = Counter()
    for a in applications:
        if a.missing_skills:
            try:
                m_list = json.loads(a.missing_skills) if isinstance(a.missing_skills, str) else a.missing_skills
                for sk in m_list:
                    if sk:
                        missing_skill_counter[sk.strip()] += 1
            except Exception:
                pass
    missing_skills_analysis = [
        {"skill": sk_name, "count": count}
        for sk_name, count in missing_skill_counter.most_common(10)
    ]

    # Applications by job
    applications_by_job_counter = Counter(a.job_id for a in applications)
    applications_by_job = [
        {"job_title": jobs_by_id[j_id].title, "count": count}
        for j_id, count in applications_by_job_counter.items()
        if j_id in jobs_by_id
    ]
    applications_by_job.sort(key=lambda x: x["count"], reverse=True)

    # Top applicant skills
    skill_counter: Counter = Counter()
    for a in applications:
        if a.candidate and a.candidate.candidate_skills:
            for cs in a.candidate.candidate_skills:
                if cs and cs.skill:
                    skill_counter[cs.skill.skill_name] += 1
    top_skills = [{"skill": name, "count": count} for name, count in skill_counter.most_common(10)]

    # Interview scores
    interview_scores = [
        {
            "job_title": jobs_by_id.get(i.job_id).title if jobs_by_id.get(i.job_id) else None,
            "overall_score": i.overall_score,
        }
        for i in completed_interviews
        if i.overall_score is not None
    ]
    avg_interview_score = (
        round(sum(s["overall_score"] for s in interview_scores) / len(interview_scores), 2)
        if interview_scores
        else None
    )

    # Job performance table
    job_performance = []
    for job in jobs:
        job_apps = [a for a in applications if a.job_id == job.id]
        job_interviews = [i for i in interviews if i.job_id == job.id and i.status == InterviewStatus.completed]
        job_scores = [a.ats_score or a.match_score for a in job_apps if (a.ats_score or a.match_score) is not None]
        st_val = job.status.value if hasattr(job.status, "value") else str(job.status)
        job_performance.append(
            {
                "job_id": str(job.id),
                "job_title": job.title,
                "status": st_val,
                "applications": len(job_apps),
                "avg_match_score": round(sum(job_scores) / len(job_scores), 2) if job_scores else None,
                "interviews_completed": len(job_interviews),
            }
        )
    job_performance.sort(key=lambda x: x["applications"], reverse=True)

    return {
        "total_jobs": total_jobs,
        "published_jobs": published_jobs,
        "total_applications": total_applications,
        "total_candidates": total_candidates,
        "shortlisted_count": shortlisted_count,
        "interview_count": interview_count,
        "selected_count": hired_count,
        "hired_count": hired_count,
        "conversion_rate": conversion_rate,
        "avg_match_score": avg_match_score,
        "avg_interview_score": avg_interview_score,
        "hiring_funnel": hiring_funnel,
        "funnel_stages": funnel_stages,
        "match_score_distribution": match_score_distribution,
        "missing_skills_analysis": missing_skills_analysis,
        "applications_by_job": applications_by_job,
        "top_skills": top_skills,
        "interview_scores": interview_scores,
        "job_performance": job_performance,
    }


def _compute_candidate_profile_completion(profile: CandidateProfile) -> int:
    """Computes account Profile Completion percentage (0-100%) based on filled profile fields:
    Resume (25%), Contact Details (20%), Work Experience (20%), Education (15%), Skills (10%), Summary (10%)."""
    if not profile:
        return 0

    completion = 0
    if profile.resume_text or profile.resume_path:
        completion += 25
    if profile.phone:
        completion += 10
    if profile.location or profile.address:
        completion += 10
    if profile.work_experience or (profile.experience_years and profile.experience_years > 0):
        completion += 20
    if profile.education:
        completion += 15
    if profile.candidate_skills and len(profile.candidate_skills) >= 1:
        completion += 10
    if profile.summary:
        completion += 10

    return min(completion, 100)


def get_candidate_analytics(db: Session, candidate_user_id) -> dict:
    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == candidate_user_id)
        .first()
    )

    if not profile:
        return {
            "profile_completion": 0,
            "ats_resume_score": 0,
            "resume_uploaded": False,
            "skills": [],
            "applications_count": 0,
            "applications_by_status": {status.value: 0 for status in ApplicationStatus},
            "interviews_count": 0,
            "interview_status": "no_resume",
            "latest_interview_score": None,
            "shortlisted_count": 0,
            "selected_count": 0,
            "recommended_jobs_count": 0,
        }

    applications = db.query(Application).filter(Application.candidate_id == profile.id).all()
    interviews = db.query(Interview).filter(Interview.candidate_id == profile.id).all()
    completed = [i for i in interviews if i.status == InterviewStatus.completed]

    applications_by_status = {status.value: 0 for status in ApplicationStatus}
    shortlisted_count = 0
    selected_count = 0

    for a in applications:
        st_val = a.status.value if hasattr(a.status, "value") else str(a.status)
        if st_val in applications_by_status:
            applications_by_status[st_val] += 1
        if st_val == "selected":
            selected_count += 1
        elif st_val == "shortlisted" or a.is_shortlisted:
            shortlisted_count += 1

    if completed:
        latest = max(completed, key=lambda i: i.completed_at or i.created_at)
        interview_status = "completed"
        latest_interview_score = latest.overall_score
    elif interviews:
        interview_status = "in_progress"
        latest_interview_score = None
    else:
        interview_status = "not_started"
        latest_interview_score = None

    # Jobs the candidate would be a strong match for, as a lightweight
    # "worth applying to" signal on the dashboard.
    from app.services.job_service import recommend_jobs_for_candidate

    recommended = recommend_jobs_for_candidate(db, candidate_user_id, limit=50)
    recommended_jobs_count = sum(1 for r in recommended if r["match_score"] >= 60)

    from app.nlp.best_role_evaluator import find_best_suited_position
    best_role_data = find_best_suited_position(db, candidate_user_id).to_dict()
    profile_completion = _compute_candidate_profile_completion(profile)

    return {
        "profile_completion": profile_completion,
        "ats_resume_score": profile.profile_score or 0,
        "best_suited_role": best_role_data,
        "resume_uploaded": bool(profile.resume_text),
        "skills": sorted({cs.skill.skill_name for cs in profile.candidate_skills if cs and cs.skill}),
        "applications_count": len(applications),
        "applications_by_status": applications_by_status,
        "shortlisted_count": shortlisted_count,
        "selected_count": selected_count,
        "interviews_count": len(interviews),
        "interview_status": interview_status,
        "latest_interview_score": latest_interview_score,
        "recommended_jobs_count": recommended_jobs_count,
    }
