"""
student.py — API Router for College Student Academic Profile & Placement Readiness Score.
"""
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError
from app.models.candidate import CandidateProfile
from app.models.coding import CandidateCodingAttempt
from app.models.interview import Interview, InterviewStatus
from app.models.student import (
    AptitudeAttempt,
    CandidateTestAttempt,
    StudentRoadmapProgress,
    StudentLearningPreference,
)
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.student import (
    StudentAcademicProfileResponse,
    StudentAcademicProfileUpdate,
    StudentReadinessStats,
    StudentAptitudeAttemptItem,
    StudentLearningMonitorItem,
    RecruiterStudentMonitorSummary,
    RecruiterStudentMonitorResponse,
)

router = APIRouter(prefix="/student", tags=["College Student Placement Hub"])


@router.get("/profile", response_model=APIResponse[StudentAcademicProfileResponse])
def get_student_profile(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Fetches the logged-in candidate's college student and academic details."""
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        # Create empty candidate profile if not yet created
        profile = CandidateProfile(user_id=current_user.id, is_student=True)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    skills_list = [cs.skill.skill_name for cs in profile.candidate_skills if cs.skill]

    # Ensure profile.full_name and current_user.name reflect resume name
    cand_name = getattr(profile, "full_name", None)
    if not cand_name and getattr(profile, "resume_text", None):
        from app.nlp.skill_extractor import parse_resume_fields
        try:
            cand_name = parse_resume_fields(profile.resume_text).get("name")
            if cand_name and isinstance(cand_name, str) and len(cand_name.strip()) >= 2:
                profile.full_name = cand_name.strip()
                db.add(profile)
        except Exception:
            pass
    if not cand_name:
        cand_name = current_user.name

    if cand_name and current_user.name != cand_name.strip():
        current_user.name = cand_name.strip()
        db.add(current_user)
        try:
            db.commit()
        except Exception:
            db.rollback()

    data = StudentAcademicProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        name=cand_name,
        email=current_user.email,
        is_student=profile.is_student if profile.is_student is not None else True,
        college_name=profile.college_name,
        degree=profile.degree,
        branch=profile.branch,
        graduation_year=profile.graduation_year,
        cgpa=profile.cgpa,
        current_semester=profile.current_semester,
        target_role=profile.target_role or profile.headline,
        headline=profile.headline,
        skills=skills_list,
        resume_path=profile.resume_path,
        portfolio_url=profile.portfolio_url,
        linkedin_url=profile.linkedin_url,
        github_url=profile.github_url,
        twelfth_school=getattr(profile, "twelfth_school", None),
        twelfth_board=getattr(profile, "twelfth_board", None),
        twelfth_year=getattr(profile, "twelfth_year", None),
        twelfth_percentage=getattr(profile, "twelfth_percentage", None),
        tenth_school=getattr(profile, "tenth_school", None),
        tenth_board=getattr(profile, "tenth_board", None),
        tenth_year=getattr(profile, "tenth_year", None),
        tenth_percentage=getattr(profile, "tenth_percentage", None),
    )
    return APIResponse(success=True, message="Student academic profile", data=data)


@router.put("/profile", response_model=APIResponse[StudentAcademicProfileResponse])
def update_student_profile(
    payload: StudentAcademicProfileUpdate,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Updates academic details: college name, degree, branch, graduation year, CGPA, target role, 10th & 12th credentials."""
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=current_user.id)
        db.add(profile)

    if payload.is_student is not None:
        profile.is_student = payload.is_student
    if payload.college_name is not None:
        profile.college_name = payload.college_name.strip()
    if payload.degree is not None:
        profile.degree = payload.degree.strip()
    if payload.branch is not None:
        profile.branch = payload.branch.strip()
    if payload.graduation_year is not None:
        profile.graduation_year = payload.graduation_year
    if payload.cgpa is not None:
        profile.cgpa = payload.cgpa
    if payload.current_semester is not None:
        profile.current_semester = payload.current_semester
    if payload.target_role is not None:
        profile.target_role = payload.target_role.strip()
        if not profile.headline:
            profile.headline = payload.target_role.strip()

    if payload.twelfth_school is not None:
        profile.twelfth_school = payload.twelfth_school.strip()
    if payload.twelfth_board is not None:
        profile.twelfth_board = payload.twelfth_board.strip()
    if payload.twelfth_year is not None:
        profile.twelfth_year = payload.twelfth_year
    if payload.twelfth_percentage is not None:
        profile.twelfth_percentage = payload.twelfth_percentage

    if payload.tenth_school is not None:
        profile.tenth_school = payload.tenth_school.strip()
    if payload.tenth_board is not None:
        profile.tenth_board = payload.tenth_board.strip()
    if payload.tenth_year is not None:
        profile.tenth_year = payload.tenth_year
    if payload.tenth_percentage is not None:
        profile.tenth_percentage = payload.tenth_percentage

    db.commit()
    db.refresh(profile)

    skills_list = [cs.skill.skill_name for cs in profile.candidate_skills if cs.skill]

    # Ensure profile.full_name and current_user.name reflect resume name
    cand_name = getattr(profile, "full_name", None)
    if not cand_name and getattr(profile, "resume_text", None):
        from app.nlp.skill_extractor import parse_resume_fields
        try:
            cand_name = parse_resume_fields(profile.resume_text).get("name")
            if cand_name and isinstance(cand_name, str) and len(cand_name.strip()) >= 2:
                profile.full_name = cand_name.strip()
                db.add(profile)
        except Exception:
            pass
    if not cand_name:
        cand_name = current_user.name

    if cand_name and current_user.name != cand_name.strip():
        current_user.name = cand_name.strip()
        db.add(current_user)
        try:
            db.commit()
        except Exception:
            db.rollback()

    data = StudentAcademicProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        name=cand_name,
        email=current_user.email,
        is_student=profile.is_student,
        college_name=profile.college_name,
        degree=profile.degree,
        branch=profile.branch,
        graduation_year=profile.graduation_year,
        cgpa=profile.cgpa,
        current_semester=profile.current_semester,
        target_role=profile.target_role,
        headline=profile.headline,
        skills=skills_list,
        resume_path=profile.resume_path,
        portfolio_url=profile.portfolio_url,
        linkedin_url=profile.linkedin_url,
        github_url=profile.github_url,
        twelfth_school=getattr(profile, "twelfth_school", None),
        twelfth_board=getattr(profile, "twelfth_board", None),
        twelfth_year=getattr(profile, "twelfth_year", None),
        twelfth_percentage=getattr(profile, "twelfth_percentage", None),
        tenth_school=getattr(profile, "tenth_school", None),
        tenth_board=getattr(profile, "tenth_board", None),
        tenth_year=getattr(profile, "tenth_year", None),
        tenth_percentage=getattr(profile, "tenth_percentage", None),
    )
    return APIResponse(success=True, message="Student academic profile updated successfully", data=data)


@router.get("/readiness", response_model=APIResponse[StudentReadinessStats])
def get_student_readiness_score(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Calculates placement readiness score based on aptitude, coding, mock interviews, and roadmaps."""
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()

    # 1. Aptitude statistics
    attempts = db.query(AptitudeAttempt).filter(AptitudeAttempt.user_id == current_user.id).all()
    tests_completed = len(attempts)
    avg_aptitude = sum(a.score_percentage for a in attempts) / tests_completed if tests_completed > 0 else 0.0

    # 2. Coding statistics
    coding_count = 0
    if profile:
        coding_count = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.candidate_id == profile.id).count()

    # 3. Interview statistics
    interview_count = 0
    if profile:
        interview_count = (
            db.query(Interview)
            .filter(Interview.candidate_id == profile.id, Interview.status == InterviewStatus.completed)
            .count()
        )

    # 4. Roadmap progress
    progress_records = db.query(StudentRoadmapProgress).filter(StudentRoadmapProgress.user_id == current_user.id).all()
    roadmap_avg = sum(p.progress_percent for p in progress_records) / len(progress_records) if progress_records else 0.0

    # 5. Profile completeness
    profile_factor = 20 if (profile and profile.college_name and profile.graduation_year and profile.resume_path) else 10

    # Composite Readiness Calculation (0 to 100)
    # Weights: Aptitude 30%, Coding 25%, Mock Interview 20%, Roadmap 15%, Profile 10%
    aptitude_component = min(30.0, (avg_aptitude / 100.0) * 30.0)
    coding_component = min(25.0, coding_count * 8.0)
    interview_component = min(20.0, interview_count * 10.0)
    roadmap_component = min(15.0, (roadmap_avg / 100.0) * 15.0)
    profile_component = min(10.0, profile_factor)

    overall_score = int(round(aptitude_component + coding_component + interview_component + roadmap_component + profile_component))
    overall_score = max(5, min(100, overall_score))

    # Weak & Strong Areas
    weak_areas = []
    strong_areas = []
    if tests_completed == 0:
        weak_areas.append("Aptitude Practice (No mock tests taken yet)")
    elif avg_aptitude < 65:
        weak_areas.append("Quantitative Aptitude & Speed")
    else:
        strong_areas.append("Aptitude & Problem Solving")

    if coding_count == 0:
        weak_areas.append("Hands-on Coding Assessment")
    else:
        strong_areas.append("Technical Programming")

    if interview_count == 0:
        weak_areas.append("AI Mock Interview Experience")
    else:
        strong_areas.append("Interview Communication")

    # Recommended Actions
    actions = []
    if tests_completed == 0:
        actions.append({"title": "Take Daily Aptitude Sprint", "link": "aptitude-test.html", "badge": "High Priority"})
    if not (profile and profile.resume_path):
        actions.append({"title": "Upload Resume for ATS Score", "link": "upload-resume.html", "badge": "Important"})
    if coding_count == 0:
        actions.append({"title": "Solve Technical Coding Challenge", "link": "coding-assessment.html", "badge": "Practice"})
    if interview_count == 0:
        actions.append({"title": "Attempt AI Mock HR Interview", "link": "interview.html", "badge": "Recommended"})
    actions.append({"title": "Explore Placement Roadmaps", "link": "study-materials.html", "badge": "Learning"})

    data = StudentReadinessStats(
        overall_readiness_score=overall_score,
        aptitude_score_avg=round(avg_aptitude, 1),
        tests_completed=tests_completed,
        coding_challenges_completed=coding_count,
        mock_interviews_completed=interview_count,
        roadmap_progress_percentage=round(roadmap_avg, 1),
        streak_days=max(1, min(14, tests_completed + coding_count)),
        weak_areas=weak_areas,
        strong_areas=strong_areas,
        recommended_actions=actions,
    )
    return APIResponse(success=True, message="Student placement readiness metrics", data=data)


# ---------------------------------------------------------------------------
# Recruiter Student Learning & Career Guidance Monitoring Endpoints
# (Strictly View & Monitor Only — No Question Generation)
# ---------------------------------------------------------------------------

from app.core.deps import get_current_user


def _require_recruiter_or_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.recruiter, UserRole.company_admin, UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recruiter authorization required to view student learning monitor",
        )
    return current_user


def _build_student_monitor_item(u: User, db: Session) -> StudentLearningMonitorItem:
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == u.id).first()
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == u.id).first()

    # 1. Preparing topics
    topics = []
    if pref:
        try:
            sel = json.loads(pref.selected_topics_json) if pref.selected_topics_json else []
            cust = json.loads(pref.custom_topics_json) if pref.custom_topics_json else []
            topics = list(dict.fromkeys(sel + cust))
        except Exception:
            pass

    # 2. Aptitude Attempts
    raw_attempts = db.query(AptitudeAttempt).filter(AptitudeAttempt.user_id == u.id).order_by(AptitudeAttempt.created_at.asc()).all()
    test_attempts = db.query(CandidateTestAttempt).filter(CandidateTestAttempt.user_id == u.id).order_by(CandidateTestAttempt.started_at.asc()).all()

    combined_attempts = []
    for a in raw_attempts:
        combined_attempts.append({
            "id": str(a.id),
            "title": a.topic_name or "Aptitude Assessment",
            "score_percentage": float(a.score_percentage or 0.0),
            "is_passed": bool(a.is_passed),
            "total_questions": int(a.total_questions or 10),
            "correct_count": int(a.correct_count or 0),
            "wrong_count": int(a.wrong_count or 0),
            "time_taken_seconds": int(a.time_taken_seconds or 0),
            "date": a.created_at.strftime("%Y-%m-%d %H:%M") if a.created_at else "Recently",
            "created_at_dt": a.created_at or datetime.min.replace(tzinfo=timezone.utc),
        })

    for ta in test_attempts:
        combined_attempts.append({
            "id": str(ta.id),
            "title": ta.test.title if ta.test else "Standard Aptitude Test",
            "score_percentage": float(ta.percentage or 0.0),
            "is_passed": bool(ta.passed),
            "total_questions": int(ta.test.total_questions if ta.test else 15),
            "correct_count": int(round((ta.percentage or 0) / 100.0 * (ta.test.total_questions if ta.test else 15))),
            "wrong_count": int(max(0, (ta.test.total_questions if ta.test else 15) - int(round((ta.percentage or 0) / 100.0 * (ta.test.total_questions if ta.test else 15))))),
            "time_taken_seconds": int(ta.time_taken_seconds or 0),
            "date": ta.started_at.strftime("%Y-%m-%d %H:%M") if ta.started_at else "Recently",
            "created_at_dt": ta.started_at or datetime.min.replace(tzinfo=timezone.utc),
        })

    combined_attempts.sort(key=lambda x: x["created_at_dt"])

    # If no topics selected but attempts exist, infer from attempted tests
    if not topics and combined_attempts:
        topics = list(dict.fromkeys([a["title"] for a in combined_attempts if a["title"]]))
    if not topics:
        topics = ["Quantitative Aptitude & Logic"]

    scores = [a["score_percentage"] for a in combined_attempts]
    tests_count = len(scores)
    avg_score = round(sum(scores) / tests_count, 1) if tests_count > 0 else 0.0
    latest_score = round(scores[-1], 1) if tests_count > 0 else 0.0
    best_score = round(max(scores), 1) if tests_count > 0 else 0.0
    passed_count = sum(1 for a in combined_attempts if a["is_passed"])
    failed_count = tests_count - passed_count
    pass_rate = round((passed_count / tests_count) * 100.0, 1) if tests_count > 0 else 0.0
    total_time_mins = round(sum(a["time_taken_seconds"] for a in combined_attempts) / 60.0, 1)

    # 3. Roadmap Progress
    progress_records = db.query(StudentRoadmapProgress).filter(StudentRoadmapProgress.user_id == u.id).all()
    if progress_records:
        roadmap_progress = round(sum(p.progress_percent for p in progress_records) / float(len(progress_records)), 1)
        roadmaps_enrolled = len(progress_records)
        milestones_count = 0
        for p in progress_records:
            try:
                m_list = json.loads(p.completed_milestones_json) if p.completed_milestones_json else []
                milestones_count += len(m_list)
            except Exception:
                pass
    else:
        roadmap_progress = 0.0
        roadmaps_enrolled = 0
        milestones_count = 0

    # 4. Consistency & Streak
    streak = pref.daily_streak if pref else (1 if tests_count > 0 else 0)
    last_active = pref.last_assessment_date if (pref and pref.last_assessment_date) else (
        combined_attempts[-1]["date"][:10] if combined_attempts else None
    )
    is_consistent = streak >= 2 or (tests_count >= 2 and roadmap_progress >= 20.0)
    if streak >= 3:
        c_label = f"Consistent ({streak}d streak)"
        c_badge = "success"
    elif streak >= 1 or tests_count > 0:
        c_label = f"Active ({streak}d streak)"
        c_badge = "primary"
    else:
        c_label = "Needs Engagement"
        c_badge = "secondary"

    # 5. Trend Analysis (Improving vs Declining)
    if len(scores) >= 3:
        recent_avg = sum(scores[-2:]) / 2.0
        earlier_avg = sum(scores[:-2]) / float(len(scores[:-2]))
        diff = recent_avg - earlier_avg
        if diff >= 5.0:
            trend = "improving"
            trend_label = "Improving ↗"
            trend_badge = "success"
        elif diff <= -5.0:
            trend = "declining"
            trend_label = "Declining ↘"
            trend_badge = "danger"
        else:
            trend = "steady"
            trend_label = "Steady ➔"
            trend_badge = "info"
    elif len(scores) == 2:
        diff = scores[1] - scores[0]
        if diff >= 5.0:
            trend = "improving"
            trend_label = "Improving ↗"
            trend_badge = "success"
        elif diff <= -5.0:
            trend = "declining"
            trend_label = "Declining ↘"
            trend_badge = "danger"
        else:
            trend = "steady"
            trend_label = "Steady ➔"
            trend_badge = "info"
    elif len(scores) == 1:
        trend = "steady"
        trend_label = "Baseline (1 test)"
        trend_badge = "info"
    else:
        trend = "none"
        trend_label = "No Attempts"
        trend_badge = "secondary"

    # 6. Overall Performance Evaluation (Performing Well vs Needs Improvement)
    if avg_score >= 70.0 or (avg_score >= 60.0 and roadmap_progress >= 40.0):
        perf_status = "Performing Well"
        status_badge = "success"
        rating_stars = "⭐⭐⭐⭐"
    elif avg_score >= 45.0 or roadmap_progress >= 25.0 or tests_count >= 1:
        perf_status = "Moderate Progress"
        status_badge = "warning"
        rating_stars = "⭐⭐"
    else:
        perf_status = "Needs Improvement"
        status_badge = "danger"
        rating_stars = "⭐"

    # 7. Strengths and Weaknesses
    weak_areas = []
    strong_areas = []
    if tests_count == 0:
        weak_areas.append("Has not attempted any aptitude mock tests")
    elif avg_score < 60.0:
        weak_areas.append(f"Aptitude accuracy ({avg_score}%) below 60% passing benchmark")
    else:
        strong_areas.append(f"Strong aptitude test performance ({avg_score}% average)")

    if roadmap_progress < 25.0:
        weak_areas.append("Low milestone completion on career roadmaps (< 25%)")
    else:
        strong_areas.append(f"Steady learning roadmap completion ({roadmap_progress}%)")

    if trend == "improving":
        strong_areas.append("Demonstrating positive score trajectory (improving over time)")
    elif trend == "declining":
        weak_areas.append("Recent assessment performance is declining compared to past tests")

    if not is_consistent and streak <= 0:
        weak_areas.append("Inconsistent practice attendance (no active streak)")
    elif streak >= 3:
        strong_areas.append(f"High dedication with active {streak}-day practice streak")

    recent_items = [
        StudentAptitudeAttemptItem(
            id=a["id"],
            title=a["title"],
            score_percentage=a["score_percentage"],
            is_passed=a["is_passed"],
            total_questions=a["total_questions"],
            correct_count=a["correct_count"],
            wrong_count=a["wrong_count"],
            time_taken_seconds=a["time_taken_seconds"],
            date=a["date"],
        )
        for a in reversed(combined_attempts[-10:])
    ]

    return StudentLearningMonitorItem(
        user_id=str(u.id),
        name=u.name or "Candidate",
        email=u.email,
        college_name=(profile.college_name if profile and profile.college_name else "University Institute of Technology"),
        degree=(profile.degree if profile and profile.degree else "B.Tech / B.E."),
        branch=(profile.branch if profile and profile.branch else "Computer Science"),
        graduation_year=(profile.graduation_year if profile else 2026),
        cgpa=(profile.cgpa if profile else None),
        target_role=((profile.target_role or profile.headline) if profile and (profile.target_role or profile.headline) else "Software Engineer"),
        preparing_topics=topics,
        topics_count=len(topics),
        tests_count=tests_count,
        avg_score=avg_score,
        latest_score=latest_score,
        best_score=best_score,
        passed_count=passed_count,
        failed_count=failed_count,
        pass_rate=pass_rate,
        total_time_spent_mins=total_time_mins,
        roadmap_progress=roadmap_progress,
        roadmaps_enrolled=roadmaps_enrolled,
        milestones_completed_count=milestones_count,
        daily_streak=streak,
        last_active_date=last_active,
        is_consistent=is_consistent,
        consistency_label=c_label,
        consistency_badge=c_badge,
        trend=trend,
        trend_label=trend_label,
        trend_badge=trend_badge,
        performance_status=perf_status,
        status_badge=status_badge,
        rating_stars=rating_stars,
        weak_areas=weak_areas,
        strong_areas=strong_areas,
        recent_attempts=recent_items,
    )


@router.get("/recruiter/monitor", response_model=APIResponse[RecruiterStudentMonitorResponse])
def get_recruiter_student_learning_monitor(
    search: Optional[str] = Query(None, description="Search by student name, college, email, or topic"),
    performance: Optional[str] = Query(None, description="well, moderate, improvement, all"),
    trend: Optional[str] = Query(None, description="improving, steady, declining, all"),
    current_user: User = Depends(_require_recruiter_or_admin),
    db: Session = Depends(get_db),
):
    """
    Recruiter monitor view for student career guidance activities,
    aptitude tests taken, scores, performance trends (improving/declining),
    consistency, and roadmap progress.
    Strictly view/monitor only (no question generation capabilities).
    """
    candidates = db.query(User).filter(User.role == UserRole.candidate).all()
    all_items = [_build_student_monitor_item(u, db) for u in candidates]

    # Calculate Summary metrics
    total_students = len(all_items)
    active_learners = [it for it in all_items if it.tests_count > 0 or it.roadmap_progress > 0 or it.topics_count > 0]
    active_count = len(active_learners)

    avg_apt = round(sum(it.avg_score for it in all_items) / total_students, 1) if total_students > 0 else 0.0
    avg_rm = round(sum(it.roadmap_progress for it in all_items) / total_students, 1) if total_students > 0 else 0.0

    well_count = sum(1 for it in all_items if it.performance_status == "Performing Well")
    mod_count = sum(1 for it in all_items if it.performance_status == "Moderate Progress")
    imp_count = sum(1 for it in all_items if it.performance_status == "Needs Improvement")
    consistent_count = sum(1 for it in all_items if it.is_consistent)

    # Topic frequency counts
    topic_map: Dict[str, int] = {}
    for it in all_items:
        for t in it.preparing_topics:
            topic_map[t] = topic_map.get(t, 0) + 1
    top_topics = [{"topic": k, "count": v} for k, v in sorted(topic_map.items(), key=lambda x: x[1], reverse=True)[:8]]

    summary = RecruiterStudentMonitorSummary(
        total_students=total_students,
        active_learners_count=active_count,
        avg_aptitude_score=avg_apt,
        avg_roadmap_progress=avg_rm,
        performing_well_count=well_count,
        moderate_count=mod_count,
        needs_improvement_count=imp_count,
        consistent_learners_count=consistent_count,
        top_preparing_topics=top_topics,
    )

    # Apply filtering
    filtered_items = all_items
    if search:
        s = search.lower().strip()
        filtered_items = [
            it for it in filtered_items
            if s in it.name.lower()
            or s in it.email.lower()
            or s in it.college_name.lower()
            or any(s in t.lower() for t in it.preparing_topics)
            or s in it.target_role.lower()
        ]

    if performance and performance.lower() != "all":
        p = performance.lower().strip()
        if p == "well":
            filtered_items = [it for it in filtered_items if it.performance_status == "Performing Well"]
        elif p == "moderate":
            filtered_items = [it for it in filtered_items if it.performance_status == "Moderate Progress"]
        elif p == "improvement":
            filtered_items = [it for it in filtered_items if it.performance_status == "Needs Improvement"]

    if trend and trend.lower() != "all":
        tr = trend.lower().strip()
        filtered_items = [it for it in filtered_items if it.trend == tr]

    data = RecruiterStudentMonitorResponse(
        summary=summary,
        students=filtered_items,
    )
    return APIResponse(success=True, message="Recruiter student learning monitor retrieved successfully", data=data)


@router.get("/recruiter/candidate/{candidate_user_id}", response_model=APIResponse[StudentLearningMonitorItem])
def get_recruiter_single_student_activity(
    candidate_user_id: str,
    current_user: User = Depends(_require_recruiter_or_admin),
    db: Session = Depends(get_db),
):
    """Returns detailed learning and career guidance activity metrics for a single student."""
    try:
        u_uuid = uuid.UUID(candidate_user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid candidate user ID")

    candidate = db.query(User).filter(User.id == u_uuid, User.role == UserRole.candidate).first()
    if not candidate:
        raise NotFoundError("Candidate student not found")

    item = _build_student_monitor_item(candidate, db)
    return APIResponse(success=True, message="Candidate detailed learning activity retrieved", data=item)

