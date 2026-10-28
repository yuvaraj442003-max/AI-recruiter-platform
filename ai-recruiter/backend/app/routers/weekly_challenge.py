"""
weekly_challenge.py — REST API router for Weekly Aptitude and Coding Challenges,
Candidate Submissions, Sandbox Code Execution, Competitive Leaderboards, and Admin Question Management.
"""
import json
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError, BadRequestError
from app.models.coding import CodingQuestion, CodingTestCase
from app.models.student import AptitudeQuestion, AptitudeTopic
from app.models.user import User, UserRole
from app.models.weekly_challenge import (
    WeeklyAptitudeAttempt,
    WeeklyAptitudeSet,
    WeeklyCodingAttempt,
    WeeklyCodingChallenge,
)
from app.schemas.common import APIResponse
from app.schemas.weekly_challenge import (
    AptitudePreparationTopicOut,
    AptitudeQuestionAdminCreate,
    AptitudeQuestionAdminUpdate,
    CodingQuestionAdminCreate,
    CodingQuestionAdminUpdate,
    LeaderboardEntry,
    ProgrammingTopicOut,
    WeeklyAptitudeAttemptResult,
    WeeklyAptitudeQuestionOut,
    WeeklyAptitudeQuestionReviewOut,
    WeeklyAptitudeSetOut,
    WeeklyAptitudeSubmissionRequest,
    WeeklyCodingChallengeOut,
    WeeklyCodingQuestionItem,
    WeeklyCodingRunRequest,
    WeeklyCodingSubmitRequest,
    WeeklyLeaderboardResponse,
    WeeklyOverviewResponse,
    WeeklyScheduleStatusOut,
)
from app.services.coding_evaluation_service import evaluate_question_submission
from app.services.weekly_challenge_service import (
    ensure_all_weekly_challenges,
    ensure_weekly_aptitude_set,
    ensure_weekly_coding_challenge,
    generate_ai_aptitude_question,
    get_aptitude_leaderboard,
    get_aptitude_topics_catalog,
    get_coding_leaderboard,
    get_coding_problem_detail,
    get_current_week_code,
    get_current_week_label,
    get_programming_topics_catalog,
    get_topic_aptitude_questions,
    get_topic_coding_problems,
    get_weekly_aptitude_curriculum,
    get_weekly_schedule_status,
    validate_aptitude_question_payload,
    validate_coding_question_payload,
)

router = APIRouter(prefix="/weekly", tags=["Weekly Challenges & Question Engine"])


# -------------------------------------------------------------------------
# CANDIDATE WEEKLY OVERVIEW & PORTAL
# -------------------------------------------------------------------------

@router.get("/overview", response_model=APIResponse[WeeklyOverviewResponse])
def get_weekly_overview(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Returns candidate's weekly dashboard overview:
    - Active ISO week code and label
    - Current weekly aptitude set metadata, completion state, and candidate score
    - Current weekly coding challenge metadata, completion state, and candidate score
    - Overall placement readiness progress
    """
    week_code = get_current_week_code()
    week_label = get_current_week_label(week_code)

    apt_set, coding_chal = ensure_all_weekly_challenges(db)

    # Check candidate aptitude attempt
    apt_attempt = (
        db.query(WeeklyAptitudeAttempt)
        .filter(
            WeeklyAptitudeAttempt.weekly_set_id == apt_set.id,
            WeeklyAptitudeAttempt.user_id == current_user.id
        )
        .first()
    )

    apt_out = WeeklyAptitudeSetOut(
        id=apt_set.id,
        week_code=apt_set.week_code,
        year=apt_set.year,
        week_number=apt_set.week_number,
        title=apt_set.title,
        description=apt_set.description,
        duration_minutes=apt_set.duration_minutes,
        passing_percentage=apt_set.passing_percentage,
        total_questions=apt_set.total_questions,
        is_active=apt_set.is_active,
        user_completed=apt_attempt is not None,
        user_score_percentage=apt_attempt.score_percentage if apt_attempt else None,
        user_passed=apt_attempt.is_passed if apt_attempt else None,
    )

    # Check candidate coding attempt
    coding_attempt = (
        db.query(WeeklyCodingAttempt)
        .filter(
            WeeklyCodingAttempt.challenge_id == coding_chal.id,
            WeeklyCodingAttempt.user_id == current_user.id
        )
        .first()
    )

    coding_out = WeeklyCodingChallengeOut(
        id=coding_chal.id,
        week_code=coding_chal.week_code,
        year=coding_chal.year,
        week_number=coding_chal.week_number,
        title=coding_chal.title,
        description=coding_chal.description,
        duration_minutes=coding_chal.duration_minutes,
        passing_score=coding_chal.passing_score,
        total_score=coding_chal.total_score,
        difficulty=coding_chal.difficulty,
        allowed_languages=json.loads(coding_chal.allowed_languages),
        questions=[],  # Summarized in overview
        user_completed=coding_attempt is not None,
        user_score=coding_attempt.score if coding_attempt else None,
        user_passed=coding_attempt.passed if coding_attempt else None,
    )

    # Compute overall weekly readiness
    scores = []
    if apt_attempt:
        scores.append(apt_attempt.score_percentage)
    if coding_attempt:
        scores.append(coding_attempt.percentage)
    readiness = round(sum(scores) / len(scores), 1) if scores else 0.0

    sched_status = get_weekly_schedule_status(db)
    coding_summary = get_programming_topics_catalog(db)[:6]
    aptitude_summary = get_aptitude_topics_catalog(db)
    weekly_focus = get_weekly_aptitude_curriculum(week_code)["current_focus"]

    return APIResponse(
        success=True,
        message="Weekly challenge overview loaded",
        data=WeeklyOverviewResponse(
            current_week_code=week_code,
            week_label=week_label,
            aptitude=apt_out,
            coding=coding_out,
            overall_readiness_pct=readiness,
            schedule=WeeklyScheduleStatusOut(**sched_status),
            coding_topics_summary=coding_summary,
            aptitude_topics_summary=aptitude_summary,
            aptitude_weekly_focus=weekly_focus,
        ),
    )


# -------------------------------------------------------------------------
# WEEKLY SCHEDULE STATUS & TOPIC CATALOGS
# -------------------------------------------------------------------------

@router.get("/status", response_model=APIResponse[WeeklyScheduleStatusOut])
def get_weekly_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """
    Returns real-time weekly rotation schedule, active ISO week, countdown to next update,
    and available coding & aptitude topic metrics.
    """
    ensure_all_weekly_challenges(db)
    status_data = get_weekly_schedule_status(db)
    return APIResponse(success=True, message="Weekly schedule status loaded", data=WeeklyScheduleStatusOut(**status_data))


@router.get("/topics/coding", response_model=APIResponse[List[ProgrammingTopicOut]])
def list_programming_topics_for_coding(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """
    Returns the complete catalog of Programming Topics for coding practice:
    Arrays, Strings, Hash Maps, Linked Lists, Stacks & Queues, Binary Search, Trees, Graphs, DP, Greedy, etc.
    """
    catalog = get_programming_topics_catalog(db)
    topics = [ProgrammingTopicOut(**t) for t in catalog]
    return APIResponse(success=True, message="Programming topics catalog for coding practice", data=topics)


@router.get("/topics/coding/{topic_slug}/problems", response_model=APIResponse[List[Dict[str, Any]]])
def get_coding_problems_by_topic(
    topic_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """
    Retrieves practice coding problems for a specific programming topic with constraints,
    descriptions, starter templates (Python, JS, Java, C++), and test cases.
    """
    problems = get_topic_coding_problems(db, topic_slug=topic_slug)
    return APIResponse(success=True, message=f"Coding problems for topic '{topic_slug}'", data=problems)


@router.get("/topics/coding/problem/{problem_id}", response_model=APIResponse[Dict[str, Any]])
def get_coding_problem_by_id(
    problem_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """Retrieves full details of a single coding problem by ID for direct solving."""
    prob = get_coding_problem_detail(db, problem_id=problem_id)
    if not prob:
        raise NotFoundError("Coding problem not found")
    return APIResponse(success=True, message="Coding problem loaded", data=prob)


@router.get("/topics/aptitude", response_model=APIResponse[List[AptitudePreparationTopicOut]])
def list_aptitude_topics_catalog(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """
    Returns the comprehensive catalog of Aptitude Topics prepared in the same structured way:
    Quantitative Aptitude, Logical Reasoning, Verbal Ability, Core CS & Data Interpretation.
    """
    catalog = get_aptitude_topics_catalog(db)
    topics = [AptitudePreparationTopicOut(**t) for t in catalog]
    return APIResponse(success=True, message="Aptitude preparation topics catalog", data=topics)


@router.get("/topics/aptitude/{topic_slug}/questions", response_model=APIResponse[List[Dict[str, Any]]])
def get_aptitude_questions_by_topic(
    topic_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """Retrieves practice questions for a specific aptitude topic."""
    questions = get_topic_aptitude_questions(db, topic_slug=topic_slug)
    return APIResponse(success=True, message=f"Aptitude questions for topic '{topic_slug}'", data=questions)


@router.get("/curriculum", response_model=APIResponse[Dict[str, Any]])
def get_aptitude_curriculum_rotation(
    week_code: Optional[str] = Query(None, description="Optional week code, e.g. 2026-W43"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
):
    """
    Returns the complete 52-week rotation curriculum derived from the RS Aggarwal Aptitude syllabus:
    - Current week's focus topic, chapters, and reasoning domain
    - Upcoming weeks' preview
    - Full 12-cycle curriculum breakdown
    """
    ensure_weekly_aptitude_set(db, week_code=week_code)
    data = get_weekly_aptitude_curriculum(week_code=week_code)
    return APIResponse(success=True, message="RS Aggarwal weekly aptitude curriculum", data=data)


# -------------------------------------------------------------------------
# WEEKLY APTITUDE TEST RUNNER & EVALUATION
# -------------------------------------------------------------------------

@router.get("/aptitude/current", response_model=APIResponse[Dict[str, Any]])
def get_current_weekly_aptitude_test(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Returns current week's Aptitude test questions for test runner.
    Hides correct answers and explanations during the exam session.
    """
    apt_set = ensure_weekly_aptitude_set(db)
    q_ids = []
    if apt_set.question_ids_json:
        try:
            q_ids = [uuid.UUID(qid) for qid in json.loads(apt_set.question_ids_json)]
        except Exception:
            q_ids = []

    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(q_ids)).all() if q_ids else []

    questions_out = []
    for q in questions:
        opts = json.loads(q.options_json) if q.options_json else []
        questions_out.append(
            WeeklyAptitudeQuestionOut(
                id=q.id,
                subtopic=q.subtopic,
                question=q.question,
                options=opts,
                difficulty=q.difficulty,
                company_tag=q.company_tag,
            ).model_dump(mode="json")
        )

    # Check if candidate has already attempted this week
    attempt = (
        db.query(WeeklyAptitudeAttempt)
        .filter(
            WeeklyAptitudeAttempt.weekly_set_id == apt_set.id,
            WeeklyAptitudeAttempt.user_id == current_user.id
        )
        .first()
    )

    return APIResponse(
        success=True,
        message="Weekly aptitude test loaded",
        data={
            "test": {
                "id": str(apt_set.id),
                "week_code": apt_set.week_code,
                "title": apt_set.title,
                "description": apt_set.description,
                "duration_minutes": apt_set.duration_minutes,
                "total_questions": len(questions_out),
                "passing_percentage": apt_set.passing_percentage,
                "already_attempted": attempt is not None,
                "previous_score": attempt.score_percentage if attempt else None,
            },
            "questions": questions_out,
        },
    )


@router.post("/aptitude/submit", response_model=APIResponse[WeeklyAptitudeAttemptResult])
def submit_weekly_aptitude_test(
    payload: WeeklyAptitudeSubmissionRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Evaluates submitted weekly aptitude answers against correct answers.
    Calculates score percentage, passed status, percentile, and generates
    detailed step-by-step explanations for each question.
    """
    apt_set = ensure_weekly_aptitude_set(db)

    # Gather question IDs
    question_ids = []
    if apt_set.question_ids_json:
        try:
            question_ids = [uuid.UUID(qid) for qid in json.loads(apt_set.question_ids_json)]
        except Exception:
            question_ids = []

    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()
    if not questions:
        raise NotFoundError("Weekly questions not found")

    total_count = len(questions)
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    reviews = []

    for q in questions:
        opts = json.loads(q.options_json) if q.options_json else []
        user_choice = payload.answers.get(str(q.id))

        if user_choice is None:
            unanswered_count += 1
            is_correct = False
        elif int(user_choice) == int(q.correct_option_index):
            correct_count += 1
            is_correct = True
        else:
            wrong_count += 1
            is_correct = False

        reviews.append(
            WeeklyAptitudeQuestionReviewOut(
                id=q.id,
                subtopic=q.subtopic,
                question=q.question,
                options=opts,
                correct_option_index=q.correct_option_index,
                user_selected_index=int(user_choice) if user_choice is not None else None,
                is_correct=is_correct,
                explanation=q.explanation,
            )
        )

    score_pct = round((correct_count / total_count) * 100.0, 1) if total_count > 0 else 0.0
    is_passed = score_pct >= apt_set.passing_percentage
    percentile = min(99.6, max(10.0, round(score_pct * 0.94 + 5.2, 1)))

    if score_pct >= 85:
        feedback = "Outstanding proficiency! High placement aptitude caliber demonstrated."
    elif score_pct >= 60:
        feedback = "Cleared weekly benchmark! Practice challenging subtopics to elevate your competitive rank."
    else:
        feedback = "Practice needed. Review the step-by-step solutions below and attempt weekly study roadmaps."

    # Record or update attempt
    existing_attempt = (
        db.query(WeeklyAptitudeAttempt)
        .filter(
            WeeklyAptitudeAttempt.weekly_set_id == apt_set.id,
            WeeklyAptitudeAttempt.user_id == current_user.id
        )
        .first()
    )

    if existing_attempt:
        existing_attempt.score_percentage = score_pct
        existing_attempt.correct_count = correct_count
        existing_attempt.wrong_count = wrong_count
        existing_attempt.unanswered_count = unanswered_count
        existing_attempt.total_questions = total_count
        existing_attempt.time_taken_seconds = payload.time_taken_seconds
        existing_attempt.is_passed = is_passed
        existing_attempt.answers_json = json.dumps(payload.answers)
        existing_attempt.percentile_estimate = percentile
        existing_attempt.feedback_message = feedback
        existing_attempt.is_anonymous_leaderboard = payload.is_anonymous
        attempt_obj = existing_attempt
    else:
        attempt_obj = WeeklyAptitudeAttempt(
            user_id=current_user.id,
            weekly_set_id=apt_set.id,
            score_percentage=score_pct,
            correct_count=correct_count,
            wrong_count=wrong_count,
            unanswered_count=unanswered_count,
            total_questions=total_count,
            time_taken_seconds=payload.time_taken_seconds,
            is_passed=is_passed,
            answers_json=json.dumps(payload.answers),
            percentile_estimate=percentile,
            feedback_message=feedback,
            is_anonymous_leaderboard=payload.is_anonymous,
        )
        db.add(attempt_obj)

    db.commit()
    db.refresh(attempt_obj)

    result = WeeklyAptitudeAttemptResult(
        attempt_id=attempt_obj.id,
        week_code=apt_set.week_code,
        total_questions=total_count,
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        score_percentage=score_pct,
        time_taken_seconds=payload.time_taken_seconds,
        is_passed=is_passed,
        feedback_message=feedback,
        percentile_estimate=percentile,
        questions_review=reviews,
    )
    return APIResponse(success=True, message="Weekly aptitude submitted and evaluated", data=result)


@router.get("/aptitude/history", response_model=APIResponse[List[Dict[str, Any]]])
def get_user_weekly_aptitude_history(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Returns candidate's past weekly aptitude exam attempts and performance trend."""
    attempts = (
        db.query(WeeklyAptitudeAttempt)
        .filter(WeeklyAptitudeAttempt.user_id == current_user.id)
        .order_by(WeeklyAptitudeAttempt.created_at.desc())
        .limit(25)
        .all()
    )

    data = [
        {
            "id": str(a.id),
            "week_code": a.weekly_set.week_code if a.weekly_set else "Past Week",
            "title": a.weekly_set.title if a.weekly_set else "Weekly Aptitude",
            "score_percentage": a.score_percentage,
            "correct_count": a.correct_count,
            "wrong_count": a.wrong_count,
            "total_questions": a.total_questions,
            "time_taken_seconds": a.time_taken_seconds,
            "is_passed": a.is_passed,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in attempts
    ]
    return APIResponse(success=True, message="Weekly aptitude history loaded", data=data)


@router.get("/aptitude/leaderboard", response_model=APIResponse[WeeklyLeaderboardResponse])
def get_weekly_aptitude_leaderboard_endpoint(
    week_code: Optional[str] = Query(None, description="ISO week e.g. 2026-W42"),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Returns the competitive performance leaderboard for the specified week."""
    target_week = week_code or get_current_week_code()
    data = get_aptitude_leaderboard(db, target_week, current_user.id)
    return APIResponse(success=True, message=f"Leaderboard for {target_week}", data=data)


# -------------------------------------------------------------------------
# WEEKLY CODING CHALLENGE RUNNER & EVALUATION
# -------------------------------------------------------------------------

@router.get("/coding/current", response_model=APIResponse[Dict[str, Any]])
def get_current_weekly_coding_challenge(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Returns the active weekly coding challenge with 3 multi-tiered algorithmic questions,
    starter templates (Python, JS, Java, C++), constraints, and public sample test cases.
    """
    chal = ensure_weekly_coding_challenge(db)

    q_ids = []
    if chal.question_ids_json:
        try:
            q_ids = [uuid.UUID(qid) for qid in json.loads(chal.question_ids_json)]
        except Exception:
            q_ids = []

    questions = db.query(CodingQuestion).filter(CodingQuestion.id.in_(q_ids)).all() if q_ids else []

    question_items = []
    for q in questions:
        starter_map = {}
        if q.starter_code:
            try:
                starter_map = json.loads(q.starter_code)
            except Exception:
                starter_map = {"python": q.starter_code}

        public_tcs = [
            {"input_data": tc.input_data, "expected_output": tc.expected_output, "points": tc.points}
            for tc in q.test_cases
            if not tc.is_hidden
        ]

        question_items.append(
            WeeklyCodingQuestionItem(
                id=q.id,
                title=q.title,
                description=q.description,
                difficulty=q.difficulty,
                category=q.category,
                starter_code=starter_map,
                expected_output=q.expected_output,
                constraints=q.constraints,
                public_test_cases=public_tcs,
            ).model_dump(mode="json")
        )

    # Check candidate's existing attempt
    attempt = (
        db.query(WeeklyCodingAttempt)
        .filter(
            WeeklyCodingAttempt.challenge_id == chal.id,
            WeeklyCodingAttempt.user_id == current_user.id
        )
        .first()
    )

    return APIResponse(
        success=True,
        message="Weekly coding challenge loaded",
        data={
            "challenge": {
                "id": str(chal.id),
                "week_code": chal.week_code,
                "title": chal.title,
                "description": chal.description,
                "duration_minutes": chal.duration_minutes,
                "total_score": chal.total_score,
                "passing_score": chal.passing_score,
                "difficulty": chal.difficulty,
                "allowed_languages": json.loads(chal.allowed_languages),
                "already_attempted": attempt is not None,
                "previous_score": attempt.score if attempt else None,
            },
            "questions": question_items,
        },
    )


@router.post("/coding/run", response_model=APIResponse[Dict[str, Any]])
def run_weekly_code_snippet(
    payload: WeeklyCodingRunRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Executes candidate's code in sandboxed runtime against public test cases.
    Returns test case pass/fail, stdout/stderr, execution time, and algorithmic complexity.
    """
    try:
        qid = uuid.UUID(payload.question_id)
    except ValueError:
        raise BadRequestError("Invalid question ID format.")

    question = db.query(CodingQuestion).filter(CodingQuestion.id == qid).first()
    if not question:
        raise NotFoundError("Coding question not found.")

    public_tcs = [
        {"input_data": tc.input_data, "expected_output": tc.expected_output, "is_hidden": False, "points": tc.points}
        for tc in question.test_cases
        if not tc.is_hidden
    ]

    result = evaluate_question_submission(
        question_title=question.title,
        test_cases=public_tcs,
        language=payload.language,
        source_code=payload.source_code,
    )

    return APIResponse(success=True, message="Code executed in sandbox", data=result)


@router.post("/coding/submit", response_model=APIResponse[Dict[str, Any]])
def submit_weekly_coding_challenge(
    payload: WeeklyCodingSubmitRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Evaluates candidate's complete weekly coding challenge submissions.
    Tests each question against ALL public and hidden test cases, computes composite scores,
    records attempt, and updates the weekly competitive leaderboard.
    """
    chal = ensure_weekly_coding_challenge(db)

    q_ids = []
    if chal.question_ids_json:
        try:
            q_ids = [uuid.UUID(qid) for qid in json.loads(chal.question_ids_json)]
        except Exception:
            q_ids = []

    questions = db.query(CodingQuestion).filter(CodingQuestion.id.in_(q_ids)).all()
    if not questions:
        raise NotFoundError("Weekly coding questions not found.")

    evaluated_questions = []
    total_earned = 0.0
    total_possible = 0.0

    for q in questions:
        sub_info = payload.submissions.get(str(q.id))
        all_tcs = [
            {"input_data": tc.input_data, "expected_output": tc.expected_output, "is_hidden": tc.is_hidden, "points": tc.points}
            for tc in q.test_cases
        ]
        q_possible = sum(tc["points"] for tc in all_tcs) or 30.0
        total_possible += q_possible

        if not sub_info or not sub_info.get("source_code"):
            evaluated_questions.append({
                "question_id": str(q.id),
                "title": q.title,
                "passed": 0,
                "total": len(all_tcs),
                "score": 0.0,
                "status": "Unanswered",
                "functional_score": 0.0,
            })
            continue

        res = evaluate_question_submission(
            question_title=q.title,
            test_cases=all_tcs,
            language=sub_info.get("language", "python"),
            source_code=sub_info["source_code"],
        )

        q_earned = (res["functional_score"] / 100.0) * q_possible
        total_earned += q_earned

        evaluated_questions.append({
            "question_id": str(q.id),
            "title": q.title,
            "passed": res["passed"],
            "total": res["total"],
            "score": round(q_earned, 1),
            "status": "Evaluated",
            "functional_score": res["functional_score"],
            "time_complexity": res.get("time_complexity", "O(n)"),
            "space_complexity": res.get("space_complexity", "O(1)"),
            "ai_review": res.get("ai_review"),
        })

    percentage = round((total_earned / total_possible) * 100.0, 1) if total_possible > 0 else 0.0
    passed = percentage >= chal.passing_score

    # Save or update attempt
    existing_attempt = (
        db.query(WeeklyCodingAttempt)
        .filter(
            WeeklyCodingAttempt.challenge_id == chal.id,
            WeeklyCodingAttempt.user_id == current_user.id
        )
        .first()
    )

    if existing_attempt:
        existing_attempt.score = total_earned
        existing_attempt.percentage = percentage
        existing_attempt.passed = passed
        existing_attempt.time_taken_seconds = payload.time_taken_seconds
        existing_attempt.status = "Evaluated"
        existing_attempt.submissions_json = json.dumps(evaluated_questions)
        existing_attempt.is_anonymous_leaderboard = payload.is_anonymous
        attempt_obj = existing_attempt
    else:
        attempt_obj = WeeklyCodingAttempt(
            user_id=current_user.id,
            challenge_id=chal.id,
            score=total_earned,
            percentage=percentage,
            passed=passed,
            time_taken_seconds=payload.time_taken_seconds,
            status="Evaluated",
            submissions_json=json.dumps(evaluated_questions),
            is_anonymous_leaderboard=payload.is_anonymous,
        )
        db.add(attempt_obj)

    db.commit()
    db.refresh(attempt_obj)

    return APIResponse(
        success=True,
        message="Weekly coding challenge submitted and evaluated successfully",
        data={
            "attempt_id": str(attempt_obj.id),
            "week_code": chal.week_code,
            "score": total_earned,
            "total_possible": total_possible,
            "percentage": percentage,
            "passed": passed,
            "time_taken_seconds": payload.time_taken_seconds,
            "questions": evaluated_questions,
        },
    )


@router.get("/coding/history", response_model=APIResponse[List[Dict[str, Any]]])
def get_user_weekly_coding_history(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Returns candidate's past weekly coding challenge attempts."""
    attempts = (
        db.query(WeeklyCodingAttempt)
        .filter(WeeklyCodingAttempt.user_id == current_user.id)
        .order_by(WeeklyCodingAttempt.created_at.desc())
        .limit(25)
        .all()
    )

    data = [
        {
            "id": str(a.id),
            "week_code": a.challenge.week_code if a.challenge else "Past Week",
            "title": a.challenge.title if a.challenge else "Weekly Coding",
            "score": a.score,
            "percentage": a.percentage,
            "passed": a.passed,
            "time_taken_seconds": a.time_taken_seconds,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in attempts
    ]
    return APIResponse(success=True, message="Weekly coding history loaded", data=data)


@router.get("/coding/leaderboard", response_model=APIResponse[WeeklyLeaderboardResponse])
def get_weekly_coding_leaderboard_endpoint(
    week_code: Optional[str] = Query(None, description="ISO week e.g. 2026-W42"),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Returns the competitive coding leaderboard for the specified week."""
    target_week = week_code or get_current_week_code()
    data = get_coding_leaderboard(db, target_week, current_user.id)
    return APIResponse(success=True, message=f"Coding Leaderboard for {target_week}", data=data)


# -------------------------------------------------------------------------
# ADMIN QUESTION REVIEW, APPROVAL, AND ROTATION MANAGEMENT
# -------------------------------------------------------------------------

@router.get("/admin/questions", response_model=APIResponse[Dict[str, Any]])
def admin_list_questions(
    type: str = Query("aptitude", description="'aptitude' or 'coding'"),
    status: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """Admin reviews, audits, and manages questions and weekly assignments."""
    if type == "aptitude":
        q_query = db.query(AptitudeQuestion)
        if status:
            q_query = q_query.filter(AptitudeQuestion.status == status)
        if difficulty:
            q_query = q_query.filter(AptitudeQuestion.difficulty == difficulty.lower())

        questions = q_query.order_by(AptitudeQuestion.created_at.desc()).limit(100).all()
        data = [
            {
                "id": str(q.id),
                "type": "aptitude",
                "subtopic": q.subtopic,
                "question": q.question,
                "options": json.loads(q.options_json) if q.options_json else [],
                "correct_option_index": q.correct_option_index,
                "explanation": q.explanation,
                "difficulty": q.difficulty,
                "status": q.status,
                "week_assigned": q.week_assigned,
                "company_tag": q.company_tag,
            }
            for q in questions
        ]
    else:
        cq_query = db.query(CodingQuestion)
        if status:
            cq_query = cq_query.filter(CodingQuestion.status == status)
        if difficulty:
            cq_query = cq_query.filter(CodingQuestion.difficulty == difficulty.title())

        questions = cq_query.order_by(CodingQuestion.created_at.desc()).limit(100).all()
        data = [
            {
                "id": str(q.id),
                "type": "coding",
                "title": q.title,
                "description": q.description,
                "difficulty": q.difficulty,
                "category": q.category,
                "status": q.status,
                "week_assigned": q.week_assigned,
                "test_cases_count": len(q.test_cases),
            }
            for q in questions
        ]

    return APIResponse(success=True, message=f"Loaded {len(data)} {type} questions", data={"questions": data})


@router.post("/admin/aptitude/question", response_model=APIResponse[Dict[str, Any]])
def admin_create_aptitude_question(
    payload: AptitudeQuestionAdminCreate,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """Admin creates a new aptitude question with validation."""
    valid, err = validate_aptitude_question_payload(payload.model_dump())
    if not valid:
        raise BadRequestError(err)

    topic = db.query(AptitudeTopic).filter(AptitudeTopic.slug == payload.topic_slug).first()
    if not topic:
        from app.services.student_seed_service import seed_student_ecosystem
        seed_student_ecosystem(db)
        topic = db.query(AptitudeTopic).filter(AptitudeTopic.slug == payload.topic_slug).first()
    if not topic:
        topic = db.query(AptitudeTopic).first()
    if not topic:
        raise NotFoundError("Aptitude topic not found.")

    q = AptitudeQuestion(
        topic_id=topic.id,
        subtopic=payload.subtopic,
        question=payload.question,
        options_json=json.dumps(payload.options),
        correct_option_index=payload.correct_option_index,
        explanation=payload.explanation,
        difficulty=payload.difficulty.lower(),
        company_tag=payload.company_tag,
        status=payload.status,
    )
    db.add(q)
    db.flush()

    # Also persist relational options
    from app.models.student import AptitudeOption
    letters = ["A", "B", "C", "D"]
    for idx, opt_text in enumerate(payload.options):
        opt = AptitudeOption(
            question_id=q.id,
            option_letter=letters[idx] if idx < len(letters) else f"Opt {idx+1}",
            option_text=str(opt_text).strip(),
            is_correct=(idx == payload.correct_option_index),
            order_index=idx,
        )
        db.add(opt)

    db.commit()
    db.refresh(q)

    # Sync to Qdrant vector database
    try:
        from app.services.qdrant_service import upsert_document, COLLECTION_APTITUDE
        topic_name = topic.name if topic else "General Aptitude"
        full_text = f"Topic: {topic_name}\nSubtopic: {q.subtopic}\nQuestion: {q.question}"
        upsert_document(
            collection_name=COLLECTION_APTITUDE,
            doc_id=q.id,
            text=full_text,
            metadata={
                "question_id": str(q.id),
                "topic_name": topic_name,
                "subtopic": q.subtopic,
                "difficulty": q.difficulty,
                "company_tag": q.company_tag,
            },
        )
    except Exception as exc:
        logger.warning("Failed to upsert aptitude question to Qdrant: %s", exc)

    return APIResponse(success=True, message="Aptitude question created", data={"id": str(q.id)})


@router.put("/admin/aptitude/question/{question_id}", response_model=APIResponse[Dict[str, Any]])
def admin_update_aptitude_question(
    question_id: str,
    payload: AptitudeQuestionAdminUpdate,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """Admin updates an aptitude question."""
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise BadRequestError("Invalid question ID.")

    q = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == qid).first()
    if not q:
        raise NotFoundError("Aptitude question not found.")

    if payload.subtopic is not None:
        q.subtopic = payload.subtopic
    if payload.question is not None:
        q.question = payload.question
    if payload.options is not None:
        q.options_json = json.dumps(payload.options)
        from app.models.student import AptitudeOption
        db.query(AptitudeOption).filter(AptitudeOption.question_id == q.id).delete()
        corr_idx = payload.correct_option_index if payload.correct_option_index is not None else q.correct_option_index
        letters = ["A", "B", "C", "D"]
        for idx, opt_text in enumerate(payload.options):
            db.add(
                AptitudeOption(
                    question_id=q.id,
                    option_letter=letters[idx] if idx < len(letters) else f"Opt {idx+1}",
                    option_text=str(opt_text).strip(),
                    is_correct=(idx == corr_idx),
                    order_index=idx,
                )
            )
    elif payload.correct_option_index is not None:
        from app.models.student import AptitudeOption
        opts = db.query(AptitudeOption).filter(AptitudeOption.question_id == q.id).order_by(AptitudeOption.order_index).all()
        for idx, opt in enumerate(opts):
            opt.is_correct = (idx == payload.correct_option_index)

    if payload.correct_option_index is not None:
        q.correct_option_index = payload.correct_option_index
    if payload.explanation is not None:
        q.explanation = payload.explanation
    if payload.difficulty is not None:
        q.difficulty = payload.difficulty.lower()
    if payload.company_tag is not None:
        q.company_tag = payload.company_tag
    if payload.status is not None:
        q.status = payload.status

    db.commit()
    db.refresh(q)

    # Sync updated question to Qdrant vector database
    try:
        from app.services.qdrant_service import upsert_document, COLLECTION_APTITUDE
        topic_name = q.topic_name or (q.topic.name if q.topic else "General Aptitude")
        full_text = f"Topic: {topic_name}\nSubtopic: {q.subtopic}\nQuestion: {q.question}"
        upsert_document(
            collection_name=COLLECTION_APTITUDE,
            doc_id=q.id,
            text=full_text,
            metadata={
                "question_id": str(q.id),
                "topic_name": topic_name,
                "subtopic": q.subtopic,
                "difficulty": q.difficulty,
                "company_tag": q.company_tag,
            },
        )
    except Exception as exc:
        logger.warning("Failed to upsert updated aptitude question to Qdrant: %s", exc)

    return APIResponse(success=True, message="Aptitude question updated", data={"id": str(q.id)})


@router.delete("/admin/aptitude/question/{question_id}", response_model=APIResponse[Dict[str, Any]])
def admin_delete_aptitude_question(
    question_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Admin deletes an aptitude question."""
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise BadRequestError("Invalid question ID.")

    q = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == qid).first()
    if not q:
        raise NotFoundError("Aptitude question not found.")

    db.delete(q)
    db.commit()

    # Delete from Qdrant vector database
    try:
        from app.services.qdrant_service import delete_document, COLLECTION_APTITUDE
        delete_document(collection_name=COLLECTION_APTITUDE, doc_id=qid)
    except Exception as exc:
        logger.warning("Failed to delete aptitude question from Qdrant: %s", exc)

    return APIResponse(success=True, message="Question deleted", data={"id": question_id})


@router.post("/admin/aptitude/question/{question_id}/approve", response_model=APIResponse[Dict[str, Any]])
def admin_approve_aptitude_question(
    question_id: str,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """Admin marks a pending question as approved for weekly rotation."""
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise BadRequestError("Invalid question ID.")

    q = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == qid).first()
    if not q:
        raise NotFoundError("Aptitude question not found.")

    q.status = "approved"
    db.commit()
    db.refresh(q)

    # Sync approved question to Qdrant
    try:
        from app.services.qdrant_service import upsert_document, COLLECTION_APTITUDE
        topic_name = q.topic_name or (q.topic.name if q.topic else "General Aptitude")
        full_text = f"Topic: {topic_name}\nSubtopic: {q.subtopic}\nQuestion: {q.question}"
        upsert_document(
            collection_name=COLLECTION_APTITUDE,
            doc_id=q.id,
            text=full_text,
            metadata={
                "question_id": str(q.id),
                "topic_name": topic_name,
                "subtopic": q.subtopic,
                "difficulty": q.difficulty,
                "company_tag": q.company_tag,
            },
        )
    except Exception as exc:
        logger.warning("Failed to upsert approved aptitude question to Qdrant: %s", exc)

    return APIResponse(success=True, message="Question approved", data={"id": question_id, "status": "approved"})


@router.post("/admin/coding/question", response_model=APIResponse[Dict[str, Any]])
def admin_create_coding_question(
    payload: CodingQuestionAdminCreate,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """Admin creates a new coding question with public and hidden test cases."""
    valid, err = validate_coding_question_payload(payload.model_dump())
    if not valid:
        raise BadRequestError(err)

    cq = CodingQuestion(
        title=payload.title,
        description=payload.description,
        difficulty=payload.difficulty.title(),
        category=payload.category,
        programming_languages=json.dumps(payload.programming_languages),
        starter_code=json.dumps(payload.starter_code) if payload.starter_code else None,
        constraints=payload.constraints,
        explanation=payload.explanation,
        status=payload.status,
    )
    db.add(cq)
    db.flush()

    for tc in payload.public_test_cases:
        db.add(
            CodingTestCase(
                question_id=cq.id,
                input_data=tc["input_data"],
                expected_output=tc["expected_output"],
                is_hidden=False,
                points=tc.get("points", 10),
            )
        )
    for tc in payload.hidden_test_cases:
        db.add(
            CodingTestCase(
                question_id=cq.id,
                input_data=tc["input_data"],
                expected_output=tc["expected_output"],
                is_hidden=True,
                points=tc.get("points", 15),
            )
        )

    db.commit()
    db.refresh(cq)
    return APIResponse(success=True, message="Coding question created", data={"id": str(cq.id)})


@router.delete("/admin/coding/question/{question_id}", response_model=APIResponse[Dict[str, Any]])
def admin_delete_coding_question(
    question_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Admin deletes a coding question."""
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise BadRequestError("Invalid question ID.")

    cq = db.query(CodingQuestion).filter(CodingQuestion.id == qid).first()
    if not cq:
        raise NotFoundError("Coding question not found.")

    db.delete(cq)
    db.commit()
    return APIResponse(success=True, message="Coding question deleted", data={"id": question_id})


@router.post("/admin/rotate-now", response_model=APIResponse[Dict[str, Any]])
def admin_force_weekly_rotation(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Admin triggers an immediate refresh/rotation of weekly questions."""
    week_code = get_current_week_code()
    apt_set = ensure_weekly_aptitude_set(db, week_code=week_code, force_refresh=True)
    coding_chal = ensure_weekly_coding_challenge(db, week_code=week_code, force_refresh=True)

    return APIResponse(
        success=True,
        message=f"Weekly questions refreshed for {week_code}",
        data={
            "week_code": week_code,
            "aptitude_set_id": str(apt_set.id),
            "coding_challenge_id": str(coding_chal.id),
            "aptitude_total_questions": apt_set.total_questions,
        },
    )


@router.post("/admin/generate-ai-question", response_model=APIResponse[Dict[str, Any]])
def admin_generate_ai_question_endpoint(
    topic_slug: str = Query("quantitative-aptitude"),
    difficulty: str = Query("medium"),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """Generates an AI placement question with automatic schema & solution validation."""
    question = generate_ai_aptitude_question(db, topic_slug=topic_slug, difficulty=difficulty)
    return APIResponse(
        success=True,
        message="AI Question generated and validated successfully",
        data={
            "id": str(question.id),
            "subtopic": question.subtopic,
            "question": question.question,
            "difficulty": question.difficulty,
            "status": question.status,
        },
    )


# -------------------------------------------------------------------------
# QDRANT PDF RAG PIPELINE ENDPOINTS
# -------------------------------------------------------------------------

@router.post("/admin/index-pdf", response_model=APIResponse[Dict[str, Any]])
def admin_index_pdf_to_qdrant_endpoint(
    max_pages: int = Query(160, ge=10, le=576),
    force: bool = Query(False),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.superadmin)),
):
    """
    Indexes the RS Aggarwal Reasoning textbook PDF into Qdrant collection `aptitude_book_knowledge`.
    """
    from app.services.aptitude_pdf_rag_service import index_reasoning_pdf_to_qdrant

    result = index_reasoning_pdf_to_qdrant(max_pages=max_pages, force=force)
    return APIResponse(
        success=result.get("success", True),
        message=result.get("message", "Reasoning PDF indexed into Qdrant."),
        data=result,
    )


@router.post("/admin/rotate-from-pdf", response_model=APIResponse[Dict[str, Any]])
def admin_rotate_weekly_from_pdf_endpoint(
    force_refresh: bool = Query(True),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.superadmin)),
    db: Session = Depends(get_db),
):
    """
    Generates and updates the active weekly aptitude challenge using Qdrant vector retrieval
    over the RS Aggarwal Reasoning textbook PDF.
    """
    from app.services.aptitude_pdf_rag_service import update_weekly_aptitude_challenge_from_pdf

    week_code = get_current_week_code()
    result = update_weekly_aptitude_challenge_from_pdf(db, week_code=week_code, force_refresh=force_refresh)
    return APIResponse(
        success=result.get("success", True),
        message=result.get("message", f"Weekly challenge updated from PDF via Qdrant for {week_code}"),
        data=result,
    )


@router.get("/admin/pdf-rag-status", response_model=APIResponse[Dict[str, Any]])
def admin_get_pdf_rag_status_endpoint(
    current_user: User = Depends(require_role(UserRole.admin, UserRole.recruiter, UserRole.superadmin)),
    db: Session = Depends(get_db),
):
    """
    Returns diagnostics for the RS Aggarwal PDF + Qdrant weekly aptitude RAG pipeline.
    """
    from app.services.aptitude_pdf_rag_service import (
        find_reasoning_pdf_path,
        get_indexed_points_count,
        retrieve_book_context,
    )

    pdf_path = find_reasoning_pdf_path()
    points_count = get_indexed_points_count()
    week_code = get_current_week_code()
    curriculum = get_weekly_aptitude_curriculum(week_code)
    focus = curriculum["current_focus"]

    sample_context = []
    if points_count > 0:
        raw_results = retrieve_book_context(query_text=focus["name"], limit=2)
        for r in raw_results:
            sample_context.append({
                "chapter": r.get("payload", {}).get("chapter"),
                "page": r.get("payload", {}).get("page"),
                "similarity_pct": r.get("similarity_pct"),
                "snippet": r.get("payload", {}).get("chunk_snippet", "")[:180],
            })

    return APIResponse(
        success=True,
        message="RS Aggarwal PDF + Qdrant RAG pipeline status",
        data={
            "pdf_found": bool(pdf_path and os.path.exists(pdf_path)),
            "pdf_path": pdf_path,
            "qdrant_points_count": points_count,
            "current_week_code": week_code,
            "focus_topic": focus["name"],
            "focus_slug": focus["slug"],
            "chapters": focus["chapters"],
            "section": focus["section"],
            "sample_retrieved_context": sample_context,
        },
    )

