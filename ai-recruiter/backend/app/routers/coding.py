"""
coding.py — REST API router for coding questions, assessments, sandbox code execution,
candidate attempts, AI code reviews, and composite scoring.
"""
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.application import Application
from app.models.candidate import CandidateProfile
from app.models.coding import (
    CandidateCodingAttempt,
    CodingAssessment,
    CodingAssessmentQuestion,
    CodingQuestion,
    CodingSubmission,
    CodingTestCase,
)
from app.models.job import Job
from app.models.user import User, UserRole
from app.schemas.coding import (
    CandidateCodingAttemptResponse,
    CodingAssessmentCreate,
    CodingAssessmentResponse,
    CodingQuestionCreate,
    CodingQuestionResponse,
    CodingTestCaseResponse,
    CodingResultReportResponse,
    RunCodeRequest,
    RunCodeResponse,
    SubmitCodeRequest,
)
from app.schemas.common import APIResponse
from app.services.coding_evaluation_service import (
    evaluate_question_submission,
    generate_ai_code_review,
)

router = APIRouter(prefix="/coding", tags=["Coding Assessment Module"])


# --- SEED DATA DEFAULT QUESTIONS ---
DEFAULT_QUESTIONS = [
    {
        "title": "Find Duplicate Numbers",
        "description": "Given an array of integers `nums`, find and return all duplicate values as a list.",
        "difficulty": "Easy",
        "category": "Arrays",
        "programming_languages": json.dumps(["python", "javascript", "java", "cpp", "csharp"]),
        "starter_code": json.dumps({
            "python": "def find_duplicates(nums):\n    # Write code here\n    pass\n\nimport sys, json\nnums = json.loads(sys.stdin.read().strip())\nprint(json.dumps(find_duplicates(nums)))",
            "javascript": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\nconst nums = JSON.parse(input);\nfunction findDuplicates(arr) {\n    // Write code here\n    const seen = new Set(), dupes = [];\n    for (let x of arr) { if (seen.has(x)) dupes.push(x); else seen.add(x); }\n    return dupes;\n}\nconsole.log(JSON.stringify(findDuplicates(nums)));"
        }),
        "test_cases": [
            {"input_data": "[1, 2, 3, 2, 4, 5, 1]", "expected_output": "[2, 1]", "is_hidden": False, "points": 10},
            {"input_data": "[4, 3, 2, 7, 8, 2, 3, 1]", "expected_output": "[2, 3]", "is_hidden": True, "points": 15}
        ]
    },
    {
        "title": "Two Sum Problem",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "category": "Hash Maps",
        "programming_languages": json.dumps(["python", "javascript", "java", "cpp"]),
        "starter_code": json.dumps({
            "python": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n\nimport sys, json\ndata = json.loads(sys.stdin.read().strip())\nprint(json.dumps(two_sum(data['nums'], data['target'])))"
        }),
        "test_cases": [
            {"input_data": "{\"nums\": [2, 7, 11, 15], \"target\": 9}", "expected_output": "[0, 1]", "is_hidden": False, "points": 10},
            {"input_data": "{\"nums\": [3, 2, 4], \"target\": 6}", "expected_output": "[1, 2]", "is_hidden": True, "points": 15}
        ]
    },
    {
        "title": "Reverse Words in a String",
        "description": "Given an input string `s`, reverse the order of words.",
        "difficulty": "Medium",
        "category": "Strings",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "import sys\ns = sys.stdin.read().strip()\nwords = s.split()\nprint(' '.join(reversed(words)))"
        }),
        "test_cases": [
            {"input_data": "the sky is blue", "expected_output": "blue is sky the", "is_hidden": False, "points": 10},
            {"input_data": "  hello world  ", "expected_output": "world hello", "is_hidden": True, "points": 15}
        ]
    }
]


def _seed_default_questions_if_empty(db: Session):
    """Seed initial questions if table is empty."""
    count = db.scalar(select(CodingQuestion))
    if not count:
        for dq in DEFAULT_QUESTIONS:
            tc_data = dq.pop("test_cases")
            q = CodingQuestion(**dq)
            db.add(q)
            db.flush()
            for tc in tc_data:
                t_case = CodingTestCase(question_id=q.id, **tc)
                db.add(t_case)
        db.commit()


def _seed_default_assessment_if_empty(db: Session) -> CodingAssessment:
    """Seed initial 25 aptitude and 5 coding questions and 75-minute assessment."""
    from app.services.assessment_bank_service import seed_full_assessment_bank
    return seed_full_assessment_bank(db)



# --- QUESTION MANAGEMENT ENDPOINTS ---

@router.post("/questions", response_model=APIResponse[CodingQuestionResponse])
def create_question(
    payload: CodingQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin))
):
    """Recruiter / Admin creates a coding question with public & hidden test cases."""
    question = CodingQuestion(
        title=payload.title,
        description=payload.description,
        difficulty=payload.difficulty,
        category=payload.category,
        programming_languages=json.dumps(payload.programming_languages),
        starter_code=json.dumps(payload.starter_code or {}),
        expected_output=payload.expected_output,
        constraints=payload.constraints,
        explanation=payload.explanation,
    )
    db.add(question)
    db.flush()

    for tc in payload.test_cases:
        test_case = CodingTestCase(
            question_id=question.id,
            input_data=tc.input_data,
            expected_output=tc.expected_output,
            is_hidden=tc.is_hidden,
            points=tc.points
        )
        db.add(test_case)

    db.commit()
    db.refresh(question)

    return APIResponse(
        success=True,
        message="Coding question created successfully.",
        data=_format_question_response(question)
    )


@router.get("/questions", response_model=APIResponse[List[CodingQuestionResponse]])
def list_questions(
    difficulty: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List coding questions."""
    _seed_default_questions_if_empty(db)
    query = select(CodingQuestion).options(joinedload(CodingQuestion.test_cases))
    if difficulty:
        query = query.where(CodingQuestion.difficulty == difficulty)
    if category:
        query = query.where(CodingQuestion.category == category)

    questions = db.scalars(query).unique().all()
    res = [_format_question_response(q, is_candidate=(current_user.role == UserRole.candidate)) for q in questions]

    return APIResponse(success=True, message="Questions retrieved successfully.", data=res)


@router.get("/questions/{question_id}", response_model=APIResponse[CodingQuestionResponse])
def get_question(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get single question details."""
    question = db.scalar(
        select(CodingQuestion)
        .options(joinedload(CodingQuestion.test_cases))
        .where(CodingQuestion.id == question_id)
    )
    if not question:
        raise NotFoundError("Coding question not found.")

    return APIResponse(
        success=True,
        message="Question retrieved.",
        data=_format_question_response(question, is_candidate=(current_user.role == UserRole.candidate))
    )


# --- ASSESSMENT MANAGEMENT ENDPOINTS ---

@router.post("/assessments", response_model=APIResponse[CodingAssessmentResponse])
def create_assessment(
    payload: CodingAssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin))
):
    """Create a new Coding Assessment linked to a job."""
    if payload.job_id:
        job = db.scalar(select(Job).where(Job.id == payload.job_id))
        if not job:
            raise NotFoundError("Linked job not found.")

    assessment = CodingAssessment(
        job_id=payload.job_id,
        title=payload.title,
        description=payload.description,
        duration_minutes=payload.duration_minutes,
        passing_score=payload.passing_score,
        total_score=payload.total_score,
        max_attempts=payload.max_attempts,
        allowed_languages=json.dumps(payload.allowed_languages),
    )
    db.add(assessment)
    db.flush()

    for item in payload.questions:
        aq = CodingAssessmentQuestion(
            assessment_id=assessment.id,
            question_id=item.question_id,
            question_order=item.question_order,
            points=item.points
        )
        db.add(aq)

    db.commit()
    db.refresh(assessment)

    return APIResponse(
        success=True,
        message="Coding assessment created successfully.",
        data=_format_assessment_response(assessment, db)
    )


@router.get("/assessments", response_model=APIResponse[List[CodingAssessmentResponse]])
def list_assessments(
    job_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List coding assessments."""
    query = select(CodingAssessment)
    if job_id:
        query = query.where(CodingAssessment.job_id == job_id)

    assessments = db.scalars(query).all()
    res = [_format_assessment_response(a, db) for a in assessments]

    return APIResponse(success=True, message="Coding assessments retrieved.", data=res)


@router.get("/assessments/{assessment_id}", response_model=APIResponse[CodingAssessmentResponse])
def get_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get single assessment details."""
    assessment = db.scalar(select(CodingAssessment).where(CodingAssessment.id == assessment_id))
    if not assessment:
        raise NotFoundError("Assessment not found.")

    return APIResponse(
        success=True,
        message="Assessment details retrieved.",
        data=_format_assessment_response(assessment, db)
    )


# --- CANDIDATE ASSESSMENT FLOW ---

@router.get("/candidate/assessments", response_model=APIResponse[List[Dict[str, Any]]])
def candidate_list_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate))
):
    """List role-specific assessments assigned to candidate applications."""
    cand = db.scalar(select(CandidateProfile).where(CandidateProfile.user_id == current_user.id))
    if not cand:
        return APIResponse(success=True, message="No candidate profile.", data=[])

    from app.services.assessment_bank_service import get_or_create_assessment_for_job, classify_job_role

    # Find applications with assessments
    apps = db.scalars(select(Application).where(Application.candidate_id == cand.id)).all()
    assessments_map = {}  # assessment.id -> (assessment, job)

    for app in apps:
        if app.job:
            ass = get_or_create_assessment_for_job(db, app.job)
            if ass and ass.id not in assessments_map:
                assessments_map[ass.id] = (ass, app.job)

    if not assessments_map:
        def_assessment = _seed_default_assessment_if_empty(db)
        assessments_map[def_assessment.id] = (def_assessment, None)

    out = []
    for ass_id, (a, job) in assessments_map.items():
        # Check attempts
        attempt = db.scalar(
            select(CandidateCodingAttempt)
            .where(CandidateCodingAttempt.candidate_id == cand.id, CandidateCodingAttempt.assessment_id == a.id)
        )

        role_type = classify_job_role(job.title if job else "")
        has_coding = any(q.question and q.question.category not in ("Aptitude", "Recruiter Aptitude") for q in a.questions)
        is_dev = role_type in ("developer", "frontend_developer", "ai_developer") or has_coding
        assessment_type = "coding" if is_dev else "aptitude"

        out.append({
            "id": str(a.id),
            "job_id": str(a.job_id) if a.job_id else None,
            "job_title": job.title if job else None,
            "title": a.title,
            "description": a.description,
            "duration_minutes": a.duration_minutes,
            "passing_score": a.passing_score,
            "questions_count": len(a.questions),
            "assessment_type": assessment_type,
            "role_type": role_type,
            "status": attempt.status if attempt else "Not Started",
            "attempt_id": str(attempt.id) if attempt else None,
            "score": attempt.score if attempt else None,
            "passed": attempt.passed if attempt else False,
        })

    return APIResponse(success=True, message="Candidate assessments retrieved.", data=out)


@router.post("/candidate/assessments/{assessment_id}/start", response_model=APIResponse[CandidateCodingAttemptResponse])
def start_assessment_attempt(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate))
):
    """Candidate starts a coding assessment (initializes backend timer)."""
    cand = db.scalar(select(CandidateProfile).where(CandidateProfile.user_id == current_user.id))
    if not cand:
        raise NotFoundError("Candidate profile not found.")

    assessment = db.scalar(select(CodingAssessment).where(CodingAssessment.id == assessment_id))
    if not assessment:
        assessment = _seed_default_assessment_if_empty(db)
        assessment_id = assessment.id

    # Check existing attempts
    attempt = db.scalar(
        select(CandidateCodingAttempt)
        .where(CandidateCodingAttempt.candidate_id == cand.id, CandidateCodingAttempt.assessment_id == assessment_id)
    )

    now = datetime.now(timezone.utc)

    if not attempt:
        attempt = CandidateCodingAttempt(
            candidate_id=cand.id,
            assessment_id=assessment_id,
            status="In Progress",
            started_at=now
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
    elif attempt.status == "Not Started":
        attempt.status = "In Progress"
        attempt.started_at = now
        db.commit()
        db.refresh(attempt)
    elif attempt.status == "Terminated":
        # Assessment was already terminated
        remaining_seconds = 0
        resp_data = CandidateCodingAttemptResponse(
            id=attempt.id,
            candidate_id=attempt.candidate_id,
            assessment_id=attempt.assessment_id,
            status="Terminated",
            started_at=attempt.started_at,
            submitted_at=attempt.submitted_at,
            score=attempt.score or 0.0,
            percentage=attempt.percentage or 0.0,
            passed=False,
            time_taken=attempt.time_taken,
            remaining_seconds=0,
            assessment=_format_assessment_response(assessment, db)
        )
        return APIResponse(success=False, message="Assessment has been terminated due to policy violation.", data=resp_data)

    # Compute remaining time
    elapsed = int((datetime.now(timezone.utc) - attempt.started_at.replace(tzinfo=timezone.utc)).total_seconds()) if attempt.started_at else 0
    total_seconds = assessment.duration_minutes * 60
    remaining_seconds = max(0, total_seconds - elapsed)

    if remaining_seconds <= 0 and attempt.status == "In Progress":
        attempt.status = "Expired"
        db.commit()

    resp_data = CandidateCodingAttemptResponse(
        id=attempt.id,
        candidate_id=attempt.candidate_id,
        assessment_id=attempt.assessment_id,
        status=attempt.status,
        started_at=attempt.started_at,
        submitted_at=attempt.submitted_at,
        score=attempt.score,
        percentage=attempt.percentage,
        passed=attempt.passed,
        time_taken=attempt.time_taken,
        remaining_seconds=remaining_seconds,
        assessment=_format_assessment_response(assessment, db)
    )

    return APIResponse(success=True, message="Assessment session active.", data=resp_data)


@router.post("/candidate/attempts/{attempt_id}/run", response_model=APIResponse[RunCodeResponse])
def run_candidate_code(
    attempt_id: uuid.UUID,
    payload: RunCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate))
):
    """Runs candidate code against PUBLIC test cases only."""
    attempt = db.scalar(select(CandidateCodingAttempt).where(CandidateCodingAttempt.id == attempt_id))
    if not attempt:
        raise NotFoundError("Coding attempt not found.")

    question = db.scalar(
        select(CodingQuestion)
        .options(joinedload(CodingQuestion.test_cases))
        .where(CodingQuestion.id == payload.question_id)
    )
    if not question:
        raise NotFoundError("Question not found.")

    # Convert test cases
    tc_dicts = [
        {
            "input_data": tc.input_data,
            "expected_output": tc.expected_output,
            "is_hidden": tc.is_hidden,
            "points": tc.points
        }
        for tc in question.test_cases
    ]

    res = evaluate_question_submission(
        question_title=question.title,
        test_cases=tc_dicts,
        language=payload.language,
        source_code=payload.source_code,
        run_only_public=True
    )

    # During the assessment, candidate should not see test case scores or correctness
    has_error = any(tc.get("error") for tc in res.get("test_case_details", []))
    status = "error" if has_error else "success"

    output_lines = []
    for tc in res.get("test_case_details", []):
        if tc.get("error"):
            output_lines.append(f"Error: {tc['error']}")
        elif tc.get("actual_output"):
            output_lines.append(f"Output: {tc['actual_output']}")

    clean_output = "\n".join(output_lines) if output_lines else "Code executed successfully without runtime errors."
    clean_output += "\n\n🔒 Note: Scores and answer correctness are hidden during the assessment. Your final score and detailed report will be displayed after complete submission."

    return APIResponse(
        success=True,
        message="Code run executed.",
        data=RunCodeResponse(
            status=status,
            passed=0,
            total=0,
            execution_time=res["execution_time"],
            output=clean_output,
            test_case_details=[]
        )
    )


@router.post("/candidate/attempts/{attempt_id}/submit", response_model=APIResponse[Dict[str, Any]])
def submit_candidate_assessment(
    attempt_id: uuid.UUID,
    submissions: List[SubmitCodeRequest],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate))
):
    """
    Submits candidate coding assessment solutions, evaluates against ALL test cases (public + hidden),
    runs AI code review, and updates overall application composite score.
    """
    attempt = db.scalar(select(CandidateCodingAttempt).where(CandidateCodingAttempt.id == attempt_id))
    if not attempt:
        raise NotFoundError("Coding attempt not found.")

    assessment = db.scalar(select(CodingAssessment).where(CodingAssessment.id == attempt.assessment_id))
    if not assessment:
        raise NotFoundError("Assessment not found.")

    if attempt.status == "Terminated":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Assessment has been terminated due to anti-cheat policy violation (unauthorized tab switch). Submission is disallowed."
        )

    now = datetime.now(timezone.utc)
    started_at = attempt.started_at.replace(tzinfo=timezone.utc) if attempt.started_at else now
    time_taken_sec = int((now - started_at).total_seconds())

    total_possible_points = 0.0
    total_earned_score = 0.0

    # Process each question submission
    for sub in submissions:
        question = db.scalar(
            select(CodingQuestion)
            .options(joinedload(CodingQuestion.test_cases))
            .where(CodingQuestion.id == sub.question_id)
        )
        if not question:
            continue

        tc_dicts = [
            {
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_hidden": tc.is_hidden,
                "points": tc.points
            }
            for tc in question.test_cases
        ]

        eval_res = evaluate_question_submission(
            question_title=question.title,
            test_cases=tc_dicts,
            language=sub.language,
            source_code=sub.source_code,
            run_only_public=False
        )

        ai_review = generate_ai_code_review(
            question_title=question.title,
            language=sub.language,
            source_code=sub.source_code,
            functional_score=eval_res["functional_score"],
            time_complexity=eval_res["time_complexity"],
            space_complexity=eval_res["space_complexity"]
        )

        submission_obj = CodingSubmission(
            attempt_id=attempt.id,
            question_id=question.id,
            language=sub.language,
            source_code=sub.source_code,
            execution_status="Success",
            test_cases_passed=eval_res["passed"],
            test_cases_total=eval_res["total"],
            score=eval_res["final_score"],
            functional_score=eval_res["functional_score"],
            quality_score=eval_res["quality_score"],
            efficiency_score=eval_res["efficiency_score"],
            complexity_score=eval_res["complexity_score"],
            time_complexity=eval_res["time_complexity"],
            space_complexity=eval_res["space_complexity"],
            ai_review=json.dumps(ai_review),
            execution_time=eval_res["execution_time"],
            memory_used=eval_res["memory_used"]
        )
        db.add(submission_obj)

        total_earned_score += eval_res["final_score"]
        total_possible_points += 100.0

    avg_percentage = round((total_earned_score / max(1.0, total_possible_points)) * 100.0, 2)
    passed = avg_percentage >= assessment.passing_score

    attempt.status = "Evaluated"
    attempt.submitted_at = now
    attempt.score = total_earned_score
    attempt.percentage = avg_percentage
    attempt.passed = passed
    attempt.time_taken = time_taken_sec

    # Update candidate application composite score if linked to job
    if assessment.job_id:
        app = db.scalar(
            select(Application)
            .where(Application.candidate_id == attempt.candidate_id, Application.job_id == assessment.job_id)
        )
        if app:
            app.coding_score = avg_percentage
            ats = app.ats_score or app.match_score or 70.0
            coding = avg_percentage
            interview = app.interview_score or 70.0
            app.overall_score = round((ats * 0.40) + (coding * 0.35) + (interview * 0.25), 2)
            from app.services.assessment_bank_service import classify_job_role
            role_type = classify_job_role(app.job.title if app.job else "")
            has_coding = any(q.question and q.question.category not in ("Aptitude", "Recruiter Aptitude") for q in assessment.questions)
            assessment_label = "Coding Assessment" if (role_type == "developer" or has_coding) else "Aptitude Assessment"

            if not passed:
                app.status = ApplicationStatus.rejected
                app.recommendation = f"Failed {assessment_label} ({round(avg_percentage, 1)}% < {assessment.passing_score}%)"
            else:
                if app.status in (ApplicationStatus.applied, ApplicationStatus.under_review):
                    app.status = ApplicationStatus.shortlisted
                app.recommendation = f"Passed {assessment_label} ({round(avg_percentage, 1)}%)"

    db.commit()
    db.refresh(attempt)

    return APIResponse(
        success=True,
        message="Coding assessment submitted and evaluated successfully.",
        data={
            "attempt_id": str(attempt.id),
            "score": avg_percentage,
            "passed": passed,
            "status": attempt.status
        }
    )


@router.post("/candidate/attempts/{attempt_id}/terminate", response_model=APIResponse[Dict[str, Any]])
def terminate_candidate_assessment(
    attempt_id: uuid.UUID,
    reason: str = Query("TAB_SWITCH", description="Reason for automatic termination"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate))
):
    """
    Candidate switched tabs or violated anti-cheat rules during proctored assessment.
    Immediately terminates assessment, assigns score 0, and flags integrity report.
    """
    cand = db.scalar(select(CandidateProfile).where(CandidateProfile.user_id == current_user.id))
    if not cand:
        raise NotFoundError("Candidate profile not found.")

    attempt = db.scalar(
        select(CandidateCodingAttempt)
        .where(CandidateCodingAttempt.id == attempt_id, CandidateCodingAttempt.candidate_id == cand.id)
    )
    if not attempt:
        raise NotFoundError("Coding attempt not found.")

    now = datetime.now(timezone.utc)
    started_at = attempt.started_at.replace(tzinfo=timezone.utc) if attempt.started_at else now
    time_taken_sec = int((now - started_at).total_seconds())

    attempt.status = "Terminated"
    attempt.score = 0.0
    attempt.percentage = 0.0
    attempt.passed = False
    attempt.time_taken = time_taken_sec
    attempt.submitted_at = now

    # Record critical proctoring event
    from app.models.proctoring import AssessmentEvent, EventSeverity, IntegrityResult, RiskLevel
    event_reason = "Unauthorized browser tab switch or window blur detected." if reason == "TAB_SWITCH" else reason
    ev = AssessmentEvent(
        attempt_id=attempt.id,
        candidate_id=cand.id,
        event_type="TAB_SWITCH_TERMINATED",
        severity=EventSeverity.critical,
        confidence=1.0,
        metadata_json=json.dumps({
            "violation": reason,
            "description": event_reason,
            "terminated_at": now.isoformat(),
            "final_score": 0.0
        })
    )
    db.add(ev)

    # Flag integrity report
    integrity = db.scalar(select(IntegrityResult).where(IntegrityResult.attempt_id == attempt.id))
    if not integrity:
        integrity = IntegrityResult(
            attempt_id=attempt.id,
            browser_score=0.0,
            webcam_score=100.0,
            audio_score=100.0,
            code_similarity_score=100.0,
            behavior_score=0.0,
            overall_integrity_score=0.0,
            risk_level=RiskLevel.high_risk,
            recruiter_decision="rejected",
            ai_summary=f"DISQUALIFIED: {event_reason}"
        )
        db.add(integrity)
    else:
        integrity.browser_score = 0.0
        integrity.overall_integrity_score = 0.0
        integrity.risk_level = RiskLevel.high_risk
        integrity.recruiter_decision = "rejected"
        integrity.ai_summary = f"DISQUALIFIED: {event_reason}"

    # Also update application status if present
    assessment = db.scalar(select(CodingAssessment).where(CodingAssessment.id == attempt.assessment_id))
    if assessment and assessment.job_id:
        from app.models.application import Application, ApplicationStatus
        app = db.scalar(
            select(Application)
            .where(Application.candidate_id == cand.id, Application.job_id == assessment.job_id)
        )
        if app:
            app.coding_score = 0.0
            app.status = ApplicationStatus.rejected
            app.recommendation = f"Disqualified from assessment: {event_reason}"

    db.commit()
    db.refresh(attempt)

    return APIResponse(
        success=True,
        message="Assessment has been terminated due to anti-cheat policy violation.",
        data={
            "attempt_id": str(attempt.id),
            "status": "Terminated",
            "score": 0.0,
            "passed": False,
            "reason": reason,
            "message": "Assessment immediately terminated and disqualified due to unauthorized tab switch."
        }
    )


@router.get("/candidate/attempts/{attempt_id}/result", response_model=APIResponse[CodingResultReportResponse])
def get_candidate_attempt_report(
    attempt_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get coding attempt detailed report."""
    attempt = db.scalar(
        select(CandidateCodingAttempt)
        .options(joinedload(CandidateCodingAttempt.submissions), joinedload(CandidateCodingAttempt.candidate))
        .where(CandidateCodingAttempt.id == attempt_id)
    )
    if not attempt:
        raise NotFoundError("Attempt not found.")

    assessment = db.scalar(select(CodingAssessment).where(CodingAssessment.id == attempt.assessment_id))
    submissions_resp = []
    for s in attempt.submissions:
        q = db.scalar(select(CodingQuestion).where(CodingQuestion.id == s.question_id))
        submissions_resp.append({
            "question_title": q.title if q else "Question",
            "language": s.language,
            "source_code": s.source_code,
            "test_cases_passed": s.test_cases_passed,
            "test_cases_total": s.test_cases_total,
            "functional_score": s.functional_score,
            "quality_score": s.quality_score,
            "time_complexity": s.time_complexity,
            "space_complexity": s.space_complexity,
            "ai_review": json.loads(s.ai_review) if s.ai_review else {}
        })

    app = None
    if assessment and assessment.job_id:
        app = db.scalar(
            select(Application)
            .where(Application.candidate_id == attempt.candidate_id, Application.job_id == assessment.job_id)
        )

    cand_name = "Candidate"
    if attempt.candidate:
        cand_name = f"{attempt.candidate.first_name} {attempt.candidate.last_name}".strip() or "Candidate"

    from app.services.assessment_bank_service import classify_job_role
    job = assessment.job if assessment else None
    role_type = classify_job_role(job.title if job else "")
    has_coding = any(s.question and s.question.category not in ("Aptitude", "Recruiter Aptitude") for s in attempt.submissions)
    assessment_type = "coding" if (role_type == "developer" or has_coding) else "aptitude"

    report = CodingResultReportResponse(
        attempt_id=attempt.id,
        candidate_id=attempt.candidate_id,
        candidate_name=cand_name,
        assessment_id=attempt.assessment_id,
        assessment_title=assessment.title if assessment else "Assessment",
        job_id=assessment.job_id if assessment else None,
        status=attempt.status,
        started_at=attempt.started_at,
        submitted_at=attempt.submitted_at,
        time_taken_minutes=round((attempt.time_taken or 0) / 60.0, 1),
        duration_minutes=assessment.duration_minutes if assessment else 60,
        score=attempt.score or 0.0,
        percentage=attempt.percentage or 0.0,
        passing_score=assessment.passing_score if assessment else 60.0,
        passed=attempt.passed,
        ats_score=app.ats_score if app else None,
        coding_score=app.coding_score if app else attempt.percentage,
        interview_score=app.interview_score if app else None,
        overall_score=app.overall_score if app else None,
        submissions=submissions_resp,
        assessment_type=assessment_type,
        role_type=role_type
    )

    return APIResponse(success=True, message="Attempt result loaded.", data=report)


# --- HELPER FORMATTERS ---

def _format_question_response(q: CodingQuestion, is_candidate: bool = False) -> CodingQuestionResponse:
    tc_responses = [
        CodingTestCaseResponse(
            id=tc.id,
            question_id=tc.question_id,
            input_data=None if (is_candidate and tc.is_hidden) else tc.input_data,
            expected_output=None if (is_candidate and tc.is_hidden) else tc.expected_output,
            is_hidden=tc.is_hidden,
            points=tc.points
        )
        for tc in q.test_cases
    ]
    return CodingQuestionResponse(
        id=q.id,
        title=q.title,
        description=q.description,
        difficulty=q.difficulty,
        category=q.category,
        programming_languages=json.loads(q.programming_languages) if q.programming_languages else [],
        starter_code=json.loads(q.starter_code) if q.starter_code else {},
        expected_output=q.expected_output,
        constraints=q.constraints,
        explanation=q.explanation,
        test_cases=tc_responses,
        created_at=q.created_at
    )


def _format_assessment_response(a: CodingAssessment, db: Session) -> CodingAssessmentResponse:
    q_items = []
    has_coding = False
    for aq in a.questions:
        q = db.scalar(select(CodingQuestion).where(CodingQuestion.id == aq.question_id))
        if q:
            if q.category not in ("Aptitude", "Recruiter Aptitude"):
                has_coding = True
            q_items.append({
                "id": str(q.id),
                "title": q.title,
                "description": q.description,
                "difficulty": q.difficulty,
                "category": q.category,
                "starter_code": json.loads(q.starter_code) if q.starter_code else {},
                "programming_languages": json.loads(q.programming_languages) if q.programming_languages else [],
                "points": aq.points
            })

    from app.services.assessment_bank_service import classify_job_role
    job = a.job
    role_type = classify_job_role(job.title if job else "") if job else ("developer" if has_coding else "non_developer")
    assessment_type = "coding" if (role_type == "developer" or has_coding) else "aptitude"

    return CodingAssessmentResponse(
        id=a.id,
        job_id=a.job_id,
        title=a.title,
        description=a.description,
        duration_minutes=a.duration_minutes,
        passing_score=a.passing_score,
        total_score=a.total_score,
        max_attempts=a.max_attempts,
        allowed_languages=json.loads(a.allowed_languages) if a.allowed_languages else [],
        questions=q_items,
        created_at=a.created_at,
        assessment_type=assessment_type,
        role_type=role_type
    )
