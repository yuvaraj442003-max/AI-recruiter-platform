"""
study_materials.py — REST API router for Study Materials, Cheatsheets, Learning Roadmaps, and Milestone Quizzes.
"""
from datetime import datetime, timezone
import json
import logging
import math
import time
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Query, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError
from app.models.student import (
    StudyMaterial,
    LearningRoadmap,
    StudentRoadmapProgress,
    StudentLearningPreference,
)
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.student import (
    StudyMaterialListItem,
    StudyMaterialDetail,
    LearningRoadmapOut,
    RoadmapProgressUpdateRequest,
    MilestoneQuizQuestionOut,
    MilestoneQuizStartResponse,
    MilestoneQuizSubmitRequest,
    MilestoneQuizReviewItem,
    MilestoneQuizResultResponse,
    AvailableTopicItem,
    StudentTopicsPreferenceRequest,
    StudentTopicsPreferenceResponse,
    DailyAssessmentStartResponse,
    DailyAssessmentSubmitRequest,
    DailyAssessmentResultResponse,
    PersonalizedLearningFeedResponse,
)
from app.services.ai_aptitude_service import generate_aptitude_questions_ai

logger = logging.getLogger("ai_recruiter.study_materials")

router = APIRouter(prefix="/study-materials", tags=["Study Materials & Roadmaps"])

# In-memory storage for active dynamic AI milestone quiz sessions
ACTIVE_AI_QUIZZES: Dict[str, Dict[str, Any]] = {}


@router.get("", response_model=APIResponse[List[StudyMaterialListItem]])
def list_study_materials(
    category: Optional[str] = Query(None, description="dsa, core_cs, web_dev, aptitude, interview_prep, company_guide"),
    company_tag: Optional[str] = Query(None),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Lists curated placement study materials, cheatsheets, and interview notes."""
    query = db.query(StudyMaterial)
    if category:
        query = query.filter(StudyMaterial.category == category)
    if company_tag:
        query = query.filter(StudyMaterial.company_tag == company_tag)

    materials = query.order_by(StudyMaterial.order_index).all()

    data = [
        StudyMaterialListItem(
            id=m.id,
            title=m.title,
            slug=m.slug,
            category=m.category,
            content_type=m.content_type,
            description=m.description,
            company_tag=m.company_tag,
            difficulty=m.difficulty,
            estimated_read_time=m.estimated_read_time,
            tags=json.loads(m.tags_json) if m.tags_json else [],
        )
        for m in materials
    ]
    return APIResponse(success=True, message="Study materials", data=data)


class AdvancePhaseRequest(BaseModel):
    phase_num: int = Field(..., ge=1, le=4)
    delta_percent: float = 20.0
    set_exact_percent: Optional[float] = None


class ToggleTaskRequest(BaseModel):
    task_id: str


class SelectCourseTrackRequest(BaseModel):
    course_id: str


class StartCourseRequest(BaseModel):
    course_id: Optional[str] = None


class CompleteTopicRequest(BaseModel):
    topic_id: str
    phase_num: int = 1


@router.get("/learning-journey", response_model=APIResponse[Dict[str, Any]])
def get_learning_journey(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Returns candidate's learning roadmap (with 60% completion / stage-gate progress),
    top recommendations, daily study plan, recent progress stats, strengths, and focus areas.
    """
    from app.services.candidate_learning_journey_service import get_candidate_learning_journey
    data = get_candidate_learning_journey(db, current_user.id)
    return APIResponse(success=True, message="Candidate learning journey", data=data)


@router.post("/learning-journey/advance-phase", response_model=APIResponse[Dict[str, Any]])
def advance_learning_phase(
    payload: AdvancePhaseRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Advances candidate course progress in a phase and unlocks the next stage
    (Foundations -> Advanced -> Projects -> Placement Ready).
    """
    from app.services.candidate_learning_journey_service import advance_candidate_phase
    res = advance_candidate_phase(
        db,
        current_user.id,
        phase_num=payload.phase_num,
        delta_percent=payload.delta_percent,
        set_exact_percent=payload.set_exact_percent,
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message"))
    return APIResponse(success=True, message=res.get("message"), data=res)


@router.post("/learning-journey/toggle-task", response_model=APIResponse[Dict[str, Any]])
def toggle_daily_plan_task(
    payload: ToggleTaskRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Toggles task status in Today's Plan and updates learning hours/progress."""
    from app.services.candidate_learning_journey_service import toggle_daily_task
    res = toggle_daily_task(db, current_user.id, payload.task_id)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message"))
    return APIResponse(success=True, message=res.get("message"), data=res)


@router.post("/learning-journey/reset", response_model=APIResponse[Dict[str, Any]])
def reset_learning_journey_dashboard(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Resets candidate dashboard to the reference 60% progress state."""
    from app.services.candidate_learning_journey_service import reset_to_reference_dashboard
    data = reset_to_reference_dashboard(db, current_user.id)
    return APIResponse(success=True, message="Reset to reference dashboard state", data=data)


@router.post("/learning-journey/select-course", response_model=APIResponse[Dict[str, Any]])
def select_learning_course_track(
    payload: SelectCourseTrackRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Switches the candidate's active learning roadmap & curriculum to the chosen course (e.g. Java, Python, DSA, Web Dev)."""
    from app.services.candidate_learning_journey_service import select_candidate_course
    data = select_candidate_course(db, current_user.id, payload.course_id)
    return APIResponse(success=True, message=f"Selected course {payload.course_id}", data=data)


@router.post("/learning-journey/start-course", response_model=APIResponse[Dict[str, Any]])
def start_learning_course_track(
    payload: StartCourseRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Starts the chosen course track, activating Phase 1: Foundations for step-by-step topic learning."""
    from app.services.candidate_learning_journey_service import start_course_journey
    data = start_course_journey(db, current_user.id, payload.course_id)
    return APIResponse(success=True, message="Course started successfully! Begin step-by-step topic learning.", data=data)


@router.get("/learning-journey/curriculum/{course_id}", response_model=APIResponse[Dict[str, Any]])
def get_course_curriculum_endpoint(
    course_id: str,
):
    """Returns complete 10-chapter curriculum, practical coding exercises, projects, and interview preparation for the course."""
    from app.services.candidate_learning_journey_service import get_course_curriculum_details
    data = get_course_curriculum_details(course_id)
    return APIResponse(success=True, message=f"{course_id} course curriculum", data=data)


@router.post("/learning-journey/complete-topic", response_model=APIResponse[Dict[str, Any]])
def complete_learning_topic(
    payload: CompleteTopicRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Marks a topic or exercise complete in the student's learning journey and dynamically advances progress."""
    from app.services.candidate_learning_journey_service import complete_course_topic
    res = complete_course_topic(db, current_user.id, payload.topic_id, payload.phase_num)
    return APIResponse(success=True, message=res.get("message", "Topic status updated"), data=res)


@router.get("/roadmaps/all", response_model=APIResponse[List[LearningRoadmapOut]])
def get_all_roadmaps(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Returns learning roadmaps along with the student's personal completion progress and scores."""
    roadmaps = db.query(LearningRoadmap).all()
    user_progress_map = {}
    records = db.query(StudentRoadmapProgress).filter(StudentRoadmapProgress.user_id == current_user.id).all()
    for rec in records:
        user_progress_map[rec.roadmap_id] = rec

    data = []
    for r in roadmaps:
        milestones = json.loads(r.milestones_json) if r.milestones_json else []
        prog = user_progress_map.get(r.id)
        completed = json.loads(prog.completed_milestones_json) if prog and prog.completed_milestones_json else []
        scores = json.loads(prog.scores_json) if prog and prog.scores_json else {}
        pct = prog.progress_percent if prog else 0.0

        data.append(
            LearningRoadmapOut(
                id=r.id,
                title=r.title,
                slug=r.slug,
                role_target=r.role_target,
                description=r.description,
                icon=r.icon,
                estimated_weeks=r.estimated_weeks,
                milestones=milestones,
                progress_percentage=round(pct, 1),
                completed_milestones=completed,
                scores=scores,
            )
        )
    return APIResponse(success=True, message="Learning roadmaps", data=data)


@router.post("/roadmaps/{slug}/progress", response_model=APIResponse[LearningRoadmapOut])
def update_roadmap_progress(
    slug: str,
    payload: RoadmapProgressUpdateRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Marks roadmap milestones as completed and recalculates overall percentage."""
    roadmap = db.query(LearningRoadmap).filter(LearningRoadmap.slug == slug).first()
    if not roadmap:
        raise NotFoundError(f"Roadmap '{slug}' not found")

    milestones = json.loads(roadmap.milestones_json) if roadmap.milestones_json else []
    total_milestones = len(milestones)

    completed_ids = list(set(payload.completed_milestone_ids))
    pct = (len(completed_ids) / total_milestones) * 100.0 if total_milestones > 0 else 0.0
    pct = min(100.0, max(0.0, round(pct, 1)))

    prog = (
        db.query(StudentRoadmapProgress)
        .filter(
            StudentRoadmapProgress.user_id == current_user.id,
            StudentRoadmapProgress.roadmap_id == roadmap.id,
        )
        .first()
    )

    if not prog:
        prog = StudentRoadmapProgress(
            user_id=current_user.id,
            roadmap_id=roadmap.id,
            completed_milestones_json=json.dumps(completed_ids),
            scores_json="{}",
            progress_percent=pct,
        )
        db.add(prog)
    else:
        prog.completed_milestones_json = json.dumps(completed_ids)
        prog.progress_percent = pct

    db.commit()
    db.refresh(prog)

    scores = json.loads(prog.scores_json) if prog.scores_json else {}

    data = LearningRoadmapOut(
        id=roadmap.id,
        title=roadmap.title,
        slug=roadmap.slug,
        role_target=roadmap.role_target,
        description=roadmap.description,
        icon=roadmap.icon,
        estimated_weeks=roadmap.estimated_weeks,
        milestones=milestones,
        progress_percentage=pct,
        completed_milestones=completed_ids,
        scores=scores,
    )
    return APIResponse(success=True, message="Roadmap progress updated", data=data)


@router.get("/roadmaps/{slug}/milestones/{milestone_id}/quiz", response_model=APIResponse[MilestoneQuizStartResponse])
def get_milestone_quiz(
    slug: str,
    milestone_id: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Fetches questions for a timed milestone quiz (30 seconds per question)."""
    roadmap = db.query(LearningRoadmap).filter(LearningRoadmap.slug == slug).first()
    if not roadmap:
        raise NotFoundError(f"Roadmap '{slug}' not found")

    milestones = json.loads(roadmap.milestones_json) if roadmap.milestones_json else []
    target_milestone = next((m for m in milestones if str(m.get("id")) == str(milestone_id)), None)
    if not target_milestone:
        raise NotFoundError(f"Milestone '{milestone_id}' not found in roadmap '{slug}'")

    raw_questions = target_milestone.get("practice_questions", [])
    if not raw_questions:
        raise NotFoundError(f"No practice questions available for milestone '{milestone_id}'")

    # Strictly 30 seconds per question for aptitude & placement speed practice
    total_q = len(raw_questions)
    duration_mins = max(1, math.ceil(total_q * 30 / 60))

    questions_out = [
        MilestoneQuizQuestionOut(
            id=str(q.get("id", f"{milestone_id}-q{i+1}")),
            question=q.get("question", ""),
            options=q.get("options", []),
            topic=target_milestone.get("subject", "Aptitude"),
            difficulty=q.get("difficulty", "medium"),
            marks=float(q.get("marks", 1.0)),
        )
        for i, q in enumerate(raw_questions)
    ]

    response_data = MilestoneQuizStartResponse(
        milestone_id=milestone_id,
        milestone_title=target_milestone.get("title", f"Week {target_milestone.get('week', 1)}"),
        subject=target_milestone.get("subject", "Placement Preparation"),
        topics=target_milestone.get("topics", []),
        subtopics=target_milestone.get("subtopics", []),
        duration_minutes=duration_mins,
        total_questions=total_q,
        passing_percentage=60.0,
        questions=questions_out,
        session_id=None,
    )
    return APIResponse(success=True, message="Milestone quiz loaded", data=response_data)


@router.post("/roadmaps/{slug}/milestones/{milestone_id}/ai-quiz", response_model=APIResponse[MilestoneQuizStartResponse])
def generate_milestone_ai_quiz(
    slug: str,
    milestone_id: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Automatically generates and serves fresh AI questions based on what students are studying in this milestone."""
    roadmap = db.query(LearningRoadmap).filter(LearningRoadmap.slug == slug).first()
    if not roadmap:
        raise NotFoundError(f"Roadmap '{slug}' not found")

    milestones = json.loads(roadmap.milestones_json) if roadmap.milestones_json else []
    target_milestone = next((m for m in milestones if str(m.get("id")) == str(milestone_id)), None)
    if not target_milestone:
        raise NotFoundError(f"Milestone '{milestone_id}' not found in roadmap '{slug}'")

    topics_to_generate = target_milestone.get("topics", [])
    if not topics_to_generate:
        topics_to_generate = [target_milestone.get("title", "Aptitude")]

    # Generate 5 fresh questions tailored to these milestone topics
    ai_questions = generate_aptitude_questions_ai(
        topics=topics_to_generate,
        num_questions=5,
        difficulty="medium",
        marks_per_question=1.0,
    )

    session_id = f"ai-session-{uuid.uuid4().hex[:12]}"
    stored_questions = []
    questions_out = []

    for idx, q in enumerate(ai_questions):
        qid = f"{session_id}-q{idx+1}"
        stored_questions.append({
            "id": qid,
            "question": q.question,
            "options": q.options,
            "correct_option_index": q.correct_option_index,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "marks": q.marks,
        })
        questions_out.append(
            MilestoneQuizQuestionOut(
                id=qid,
                question=q.question,
                options=q.options,
                topic=q.topic_name,
                difficulty=q.difficulty,
                marks=q.marks,
            )
        )

    ACTIVE_AI_QUIZZES[session_id] = {
        "milestone_id": milestone_id,
        "questions": stored_questions,
        "created_at": time.time(),
    }

    # Clean old sessions older than 2 hours
    now = time.time()
    stale_keys = [k for k, v in ACTIVE_AI_QUIZZES.items() if now - v.get("created_at", 0) > 7200]
    for k in stale_keys:
        ACTIVE_AI_QUIZZES.pop(k, None)

    duration_mins = max(1, math.ceil(len(questions_out) * 30 / 60))

    response_data = MilestoneQuizStartResponse(
        milestone_id=milestone_id,
        milestone_title=target_milestone.get("title", f"Week {target_milestone.get('week', 1)}"),
        subject=target_milestone.get("subject", "AI Dynamic Practice"),
        topics=target_milestone.get("topics", []),
        subtopics=target_milestone.get("subtopics", []),
        duration_minutes=duration_mins,
        total_questions=len(questions_out),
        passing_percentage=60.0,
        questions=questions_out,
        session_id=session_id,
    )
    return APIResponse(success=True, message="Fresh AI questions generated for this milestone", data=response_data)


@router.post("/roadmaps/{slug}/milestones/{milestone_id}/submit-quiz", response_model=APIResponse[MilestoneQuizResultResponse])
def submit_milestone_quiz(
    slug: str,
    milestone_id: str,
    payload: MilestoneQuizSubmitRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Submits and grades a milestone timed test or AI quiz.
    Evaluates score, records attempt in user progress, unlocks completed status if passed (>= 60%),
    and provides step-by-step explanations for each question.
    """
    roadmap = db.query(LearningRoadmap).filter(LearningRoadmap.slug == slug).first()
    if not roadmap:
        raise NotFoundError(f"Roadmap '{slug}' not found")

    milestones = json.loads(roadmap.milestones_json) if roadmap.milestones_json else []
    target_milestone = next((m for m in milestones if str(m.get("id")) == str(milestone_id)), None)
    if not target_milestone:
        raise NotFoundError(f"Milestone '{milestone_id}' not found in roadmap '{slug}'")

    # Determine question source (AI generated session or standard milestone practice questions)
    if payload.session_id and payload.session_id in ACTIVE_AI_QUIZZES:
        quiz_questions = ACTIVE_AI_QUIZZES[payload.session_id]["questions"]
    else:
        quiz_questions = target_milestone.get("practice_questions", [])

    if not quiz_questions:
        raise NotFoundError(f"No questions found to evaluate for milestone '{milestone_id}'")

    total_marks = 0.0
    score = 0.0
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    review_items: List[MilestoneQuizReviewItem] = []

    for q in quiz_questions:
        qid = str(q.get("id"))
        q_marks = float(q.get("marks", 1.0))
        total_marks += q_marks
        correct_idx = int(q.get("correct_option_index", 0))

        user_ans = payload.answers.get(qid)
        if user_ans is None:
            unanswered_count += 1
            is_correct = False
            user_selected = None
        else:
            user_selected = int(user_ans)
            if user_selected == correct_idx:
                correct_count += 1
                score += q_marks
                is_correct = True
            else:
                wrong_count += 1
                is_correct = False

        review_items.append(
            MilestoneQuizReviewItem(
                question_id=qid,
                question=q.get("question", ""),
                options=q.get("options", []),
                correct_option_index=correct_idx,
                user_selected_index=user_selected,
                is_correct=is_correct,
                explanation=q.get("explanation", "Review the relevant concept formulas and practice steps."),
            )
        )

    percentage = round((score / total_marks * 100.0) if total_marks > 0 else 0.0, 1)
    passed = percentage >= 60.0

    # Retrieve or initialize StudentRoadmapProgress
    prog = (
        db.query(StudentRoadmapProgress)
        .filter(
            StudentRoadmapProgress.user_id == current_user.id,
            StudentRoadmapProgress.roadmap_id == roadmap.id,
        )
        .first()
    )

    if not prog:
        completed_ids = []
        scores_dict = {}
        prog = StudentRoadmapProgress(
            user_id=current_user.id,
            roadmap_id=roadmap.id,
            completed_milestones_json="[]",
            scores_json="{}",
            progress_percent=0.0,
        )
        db.add(prog)
    else:
        completed_ids = json.loads(prog.completed_milestones_json) if prog.completed_milestones_json else []
        scores_dict = json.loads(prog.scores_json) if prog.scores_json else {}

    # Update scores record
    prev_entry = scores_dict.get(milestone_id, {})
    best_percentage = max(percentage, float(prev_entry.get("percentage", 0.0)))
    scores_dict[milestone_id] = {
        "score": score,
        "total_marks": total_marks,
        "percentage": best_percentage,
        "last_percentage": percentage,
        "passed": passed or prev_entry.get("passed", False),
        "attempts": int(prev_entry.get("attempts", 0)) + 1,
        "last_attempt_at": datetime.now(timezone.utc).isoformat(),
    }

    # Automatically mark milestone as completed when student achieves >= 60%
    if passed and milestone_id not in completed_ids:
        completed_ids.append(milestone_id)

    total_milestones = len(milestones)
    new_roadmap_pct = (len(completed_ids) / total_milestones) * 100.0 if total_milestones > 0 else 0.0
    new_roadmap_pct = min(100.0, max(0.0, round(new_roadmap_pct, 1)))

    prog.completed_milestones_json = json.dumps(completed_ids)
    prog.scores_json = json.dumps(scores_dict)
    prog.progress_percent = new_roadmap_pct

    db.commit()
    db.refresh(prog)

    if percentage >= 90.0:
        feedback = "Outstanding performance! You have thoroughly mastered this placement milestone."
    elif percentage >= 60.0:
        feedback = "Congratulations! You passed this milestone test and demonstrated strong conceptual ability."
    else:
        feedback = "Good practice effort! Review the detailed step-by-step explanations below and retake the quiz to boost your score."

    result_data = MilestoneQuizResultResponse(
        milestone_id=milestone_id,
        milestone_title=target_milestone.get("title", f"Week {target_milestone.get('week', 1)}"),
        total_questions=len(quiz_questions),
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        score=score,
        total_marks=total_marks,
        percentage=percentage,
        passed=passed,
        time_taken_seconds=payload.time_taken_seconds,
        feedback_message=feedback,
        review_items=review_items,
        is_milestone_completed=milestone_id in completed_ids,
        updated_roadmap_progress=new_roadmap_pct,
    )
    return APIResponse(success=True, message="Milestone test evaluated successfully", data=result_data)


# Predefined Placement & Technical Topics Catalog
PREDEFINED_AVAILABLE_TOPICS = [
    {
        "id": "java",
        "name": "Java",
        "category": "Programming Languages",
        "icon": "☕",
        "description": "Core Java, OOPs, Collections Framework, Multithreading, Exception Handling, Streams.",
        "popular": True,
        "subtopics_preview": ["Collections (ArrayList, HashMap)", "OOP & Abstraction", "Threads & Concurrency", "Exception Hierarchy"],
    },
    {
        "id": "python",
        "name": "Python",
        "category": "Programming Languages",
        "icon": "🐍",
        "description": "Python syntax, built-in data structures, list comprehensions, generators, decorators, OOP.",
        "popular": True,
        "subtopics_preview": ["List & Dict Comprehensions", "Generators & Yield", "Decorators & Closures", "Memory Management"],
    },
    {
        "id": "cpp",
        "name": "C++",
        "category": "Programming Languages",
        "icon": "⚡",
        "description": "Pointers, dynamic memory, STL containers (vectors, maps, sets), templates, and OOP.",
        "popular": False,
        "subtopics_preview": ["Pointers & References", "STL Vectors & Maps", "Virtual Functions & Polymorphism", "Smart Pointers"],
    },
    {
        "id": "javascript",
        "name": "JavaScript / TypeScript",
        "category": "Programming Languages",
        "icon": "🌐",
        "description": "Modern ES6+, Promises, async/await, closures, prototypes, DOM, event bubbling.",
        "popular": True,
        "subtopics_preview": ["Async/Await & Promises", "Closures & Scope", "Event Loop & Callbacks", "Array Higher-Order Methods"],
    },
    {
        "id": "dsa",
        "name": "Data Structures & Algorithms (DSA)",
        "category": "DSA & Problem Solving",
        "icon": "💻",
        "description": "Arrays, Strings, Two-Pointer, Sliding Window, Binary Trees, BST, Graphs, Dynamic Programming.",
        "popular": True,
        "subtopics_preview": ["Two-Pointer & Sliding Window", "Binary Trees & BST", "Graph BFS & DFS", "Dynamic Programming (DP)"],
    },
    {
        "id": "quantitative-aptitude",
        "name": "Quantitative Aptitude",
        "category": "Aptitude & Placement Reasoning",
        "icon": "📐",
        "description": "Percentages, Profit & Loss, Speed-Distance-Time, Work & Time, Ratios, Probability, Permutations.",
        "popular": True,
        "subtopics_preview": ["Percentages & Profit/Loss", "Time & Work", "Speed & Distance", "Probability & Permutations"],
    },
    {
        "id": "logical-reasoning",
        "name": "Logical Reasoning",
        "category": "Aptitude & Placement Reasoning",
        "icon": "🧩",
        "description": "Blood Relations, Direction Sense, Coding-Decoding, Syllogisms, Circular & Linear Seating Arrangements.",
        "popular": True,
        "subtopics_preview": ["Syllogisms (Venn Diagrams)", "Seating Arrangements", "Blood Relations", "Number Series & Puzzles"],
    },
    {
        "id": "verbal-ability",
        "name": "Verbal Ability & English",
        "category": "Aptitude & Placement Reasoning",
        "icon": "📖",
        "description": "Reading Comprehension, Sentence Correction, Subject-Verb Agreement, Error Spotting, Para Jumbles.",
        "popular": False,
        "subtopics_preview": ["Reading Comprehension", "Subject-Verb Agreement", "Error Spotting", "Para Jumbles & Vocabulary"],
    },
    {
        "id": "sql",
        "name": "SQL & Database Queries",
        "category": "Core CS & Database Systems",
        "icon": "🗄️",
        "description": "SELECT, INNER/LEFT/RIGHT JOINs, Window Functions, DENSE_RANK(), Subqueries, Aggregate calculations.",
        "popular": True,
        "subtopics_preview": ["JOIN Operations", "Window Functions (DENSE_RANK)", "GROUP BY & HAVING", "Subqueries & Correlated Subqueries"],
    },
    {
        "id": "dbms",
        "name": "DBMS (Database Management Systems)",
        "category": "Core CS & Database Systems",
        "icon": "💾",
        "description": "1NF/2NF/3NF/BCNF Normalization, ACID Transactions, B-Tree Indexing, Locking & Concurrency.",
        "popular": True,
        "subtopics_preview": ["ACID Properties", "1NF, 2NF, 3NF & BCNF Normalization", "B-Tree & Hash Indexing", "Deadlocks & Isolation Levels"],
    },
    {
        "id": "operating-systems",
        "name": "Operating Systems (OS)",
        "category": "Core CS & Systems",
        "icon": "⚙️",
        "description": "Processes vs Threads, CPU Scheduling, Deadlocks, Banker's Algorithm, Virtual Memory, Paging.",
        "popular": True,
        "subtopics_preview": ["Processes vs Threads", "CPU Scheduling Algorithms", "Deadlock Prevention & Detection", "Virtual Memory & Paging"],
    },
    {
        "id": "computer-networks",
        "name": "Computer Networks (CN)",
        "category": "Core CS & Systems",
        "icon": "🌐",
        "description": "OSI 7 Layers, TCP 3-Way Handshake vs UDP, DNS, HTTP/HTTPS, SSL/TLS, IP Routing.",
        "popular": True,
        "subtopics_preview": ["OSI & TCP/IP Model", "TCP 3-Way Handshake vs UDP", "DNS & HTTP/HTTPS Security", "Subnetting & IP Addressing"],
    },
    {
        "id": "oop",
        "name": "Object-Oriented Programming (OOP)",
        "category": "Software Engineering & Architecture",
        "icon": "🧱",
        "description": "Encapsulation, Inheritance, Polymorphism, Abstraction, SOLID design principles, Design Patterns.",
        "popular": True,
        "subtopics_preview": ["4 Pillars of OOP", "SOLID Design Principles", "Singleton & Factory Patterns", "Method Overriding vs Overloading"],
    },
    {
        "id": "system-design",
        "name": "System Design Fundamentals",
        "category": "Software Engineering & Architecture",
        "icon": "📐",
        "description": "Client-Server Architecture, Load Balancers, Caching (Redis), Database Sharding, Microservices.",
        "popular": False,
        "subtopics_preview": ["Load Balancing Algorithms", "Caching Strategies (Redis/Memcached)", "Horizontal vs Vertical Scaling", "Monolith vs Microservices"],
    },
    {
        "id": "web-dev",
        "name": "Web Development (Full-Stack)",
        "category": "Web & Cloud Technologies",
        "icon": "🚀",
        "description": "RESTful API design, FastAPI/Express, Authentication (JWT), CORS, Database integration.",
        "popular": False,
        "subtopics_preview": ["RESTful API Best Practices", "JWT & Stateless Auth", "CORS & Web Security Headers", "Relational ORM Integration"],
    },
    {
        "id": "cloud-devops",
        "name": "Cloud & DevOps Fundamentals",
        "category": "Web & Cloud Technologies",
        "icon": "☁️",
        "description": "Docker containerization, CI/CD pipelines, Git workflows, AWS basics, Linux command line.",
        "popular": False,
        "subtopics_preview": ["Docker & Containers", "CI/CD Pipeline Basics", "Linux Shell Commands", "Cloud Infrastructure (AWS/GCP)"],
    },
    {
        "id": "ai-machine-learning",
        "name": "Artificial Intelligence & Machine Learning (AI / ML)",
        "category": "AI, Data & Emerging Tech",
        "icon": "🤖",
        "description": "Supervised & Unsupervised Learning, Neural Networks, PyTorch/TensorFlow, NLP, Large Language Models (LLMs), Model Evaluation.",
        "popular": True,
        "subtopics_preview": ["Supervised vs Unsupervised ML", "Neural Networks & Deep Learning", "Transformers & LLMs", "Model Metrics (Precision, Recall, F1)"],
    },
    {
        "id": "data-engineering",
        "name": "Data Engineering & Big Data",
        "category": "AI, Data & Emerging Tech",
        "icon": "📊",
        "description": "ETL/ELT Data Pipelines, Apache Spark, Apache Kafka, Data Warehousing (Star/Snowflake Schema), Data Lakes, Distributed Storage.",
        "popular": True,
        "subtopics_preview": ["ETL Pipelines & Batch vs Stream", "Apache Spark & PySpark", "Apache Kafka Event Streaming", "Data Warehousing (Snowflake/BigQuery)"],
    },
    {
        "id": "cloud-computing",
        "name": "Cloud Computing & Architecture",
        "category": "Web & Cloud Technologies",
        "icon": "☁️",
        "description": "AWS, Azure, GCP core services, Cloud Design Patterns, Serverless (Lambda), Kubernetes, Microservices, Terraform (IaC).",
        "popular": True,
        "subtopics_preview": ["AWS Core Services (EC2, S3, RDS, IAM)", "Kubernetes (K8s) & Containers", "Serverless Architecture & Lambda", "Terraform & Cloud Security"],
    },
    {
        "id": "aws",
        "name": "AWS (Amazon Web Services)",
        "category": "Web & Cloud Technologies",
        "icon": "🚀",
        "description": "AWS EC2, S3, RDS, DynamoDB, Lambda, VPC, IAM, API Gateway, CloudFront, Route53, and Solutions Architecture.",
        "popular": True,
        "subtopics_preview": ["Compute & Storage (EC2, S3, EBS)", "Networking & Security (VPC, IAM)", "Databases (RDS, Aurora, DynamoDB)", "Serverless Architecture (Lambda, API Gateway)"],
    },
    {
        "id": "cybersecurity",
        "name": "Cybersecurity & Ethical Hacking",
        "category": "Security & Quality Assurance",
        "icon": "🛡️",
        "description": "Threat Modeling, OWASP Top 10, Network Defense, Cryptography, Identity & Access Management, SOC Analysis, and Incident Response.",
        "popular": True,
        "subtopics_preview": ["OWASP Top 10 Web Security", "Network Protocols & Defense", "Cryptography & PKI", "Incident Response & SOC Analysis"],
    },
    {
        "id": "devops",
        "name": "DevOps & SRE",
        "category": "Web & Cloud Technologies",
        "icon": "🔄",
        "description": "Continuous Integration / Continuous Delivery (CI/CD), Docker, Kubernetes, Terraform, Helm, Monitoring (Prometheus/Grafana), and Site Reliability Engineering.",
        "popular": True,
        "subtopics_preview": ["CI/CD Pipelines (GitHub Actions/Jenkins)", "Docker Containerization", "Kubernetes (K8s) Cluster Orchestration", "Terraform Infrastructure as Code (IaC)"],
    },
    {
        "id": "gen-ai",
        "name": "Generative AI & LLMs",
        "category": "AI, Data & Emerging Tech",
        "icon": "✨",
        "description": "Prompt Engineering, Few-Shot Prompting, Retrieval-Augmented Generation (RAG), LangChain, LlamaIndex, Vector Databases, and Autonomous Agents.",
        "popular": True,
        "subtopics_preview": ["Prompt Engineering & In-Context Learning", "Retrieval-Augmented Generation (RAG)", "Vector Embeddings & Chroma/FAISS", "Autonomous Agents & Function Calling"],
    },
    {
        "id": "deep-learning",
        "name": "Deep Learning & Neural Networks",
        "category": "AI, Data & Emerging Tech",
        "icon": "🧠",
        "description": "Backpropagation, Optimization, Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs/LSTMs), Transformers, and PyTorch.",
        "popular": True,
        "subtopics_preview": ["Multi-Layer Perceptrons & Backpropagation", "PyTorch Tensors & Training Loops", "CNNs for Computer Vision", "Transformers & Self-Attention Mechanics"],
    },
    {
        "id": "software-testing",
        "name": "Software Testing & QA Automation",
        "category": "Security & Quality Assurance",
        "icon": "🧪",
        "description": "Test Methodologies, Black/White Box, Selenium WebDriver, PyTest/JUnit, REST API Testing (Postman/RestAssured), Performance Testing, and CI Quality Gates.",
        "popular": True,
        "subtopics_preview": ["Unit & Integration Testing Principles", "Selenium WebDriver Test Automation", "REST API Automation (Postman/RestAssured)", "CI/CD Quality Gates & Test Reporting"],
    },
    {
        "id": "data-science",
        "name": "Data Science & Analytics",
        "category": "AI, Data & Emerging Tech",
        "icon": "📊",
        "description": "Exploratory Data Analysis, Pandas, NumPy, Scikit-Learn, Feature Engineering, Hypothesis Testing, and Dashboards.",
        "popular": True,
        "subtopics_preview": ["Pandas & NumPy Data Wrangling", "Exploratory Data Analysis (EDA)", "Statistical Inference & A/B Testing", "Supervised Scikit-Learn Models"],
    },
]


@router.get("/topics/available", response_model=APIResponse[List[AvailableTopicItem]])
def list_available_topics(
    current_user: User = Depends(require_role(UserRole.candidate)),
):
    """Returns catalog of placement and technical topics available for students to choose from."""
    topics = [AvailableTopicItem(**t) for t in PREDEFINED_AVAILABLE_TOPICS]
    return APIResponse(success=True, message="Available learning topics catalog", data=topics)


@router.get("/topics/preferences", response_model=APIResponse[StudentTopicsPreferenceResponse])
def get_student_topic_preferences(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Retrieves the student's selected learning topics, custom topics, streak, and assessment status."""
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == current_user.id).first()
    if not pref:
        default_selected = [
            "Java",
            "Python",
            "Data Structures & Algorithms (DSA)",
            "SQL & Database Queries",
            "Quantitative Aptitude",
            "Logical Reasoning",
        ]
        pref = StudentLearningPreference(
            user_id=current_user.id,
            selected_topics_json=json.dumps(default_selected),
            custom_topics_json="[]",
            daily_streak=1,
            history_json="[]",
        )
        db.add(pref)
        db.commit()
        db.refresh(pref)

    selected = json.loads(pref.selected_topics_json) if pref.selected_topics_json else []
    custom = json.loads(pref.custom_topics_json) if pref.custom_topics_json else []
    history = json.loads(pref.history_json) if pref.history_json else []

    all_active = list(dict.fromkeys(selected + custom))

    data = StudentTopicsPreferenceResponse(
        selected_topics=selected,
        custom_topics=custom,
        all_active_topics=all_active,
        daily_streak=pref.daily_streak,
        last_assessment_date=pref.last_assessment_date,
        total_assessments_taken=len(history),
    )
    return APIResponse(success=True, message="Student topic preferences", data=data)


@router.post("/topics/preferences", response_model=APIResponse[StudentTopicsPreferenceResponse])
def update_student_topic_preferences(
    payload: StudentTopicsPreferenceRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Saves the student's chosen placement topics and user-added custom topics."""
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == current_user.id).first()
    clean_selected = [t.strip() for t in payload.selected_topics if t.strip()]
    clean_custom = [t.strip() for t in payload.custom_topics if t.strip()]

    # If completely empty, enforce at least one topic
    if not clean_selected and not clean_custom:
        clean_selected = ["Quantitative Aptitude", "Data Structures & Algorithms (DSA)"]

    if not pref:
        pref = StudentLearningPreference(
            user_id=current_user.id,
            selected_topics_json=json.dumps(clean_selected),
            custom_topics_json=json.dumps(clean_custom),
            daily_streak=1,
            history_json="[]",
        )
        db.add(pref)
    else:
        pref.selected_topics_json = json.dumps(clean_selected)
        pref.custom_topics_json = json.dumps(clean_custom)

    db.commit()
    db.refresh(pref)

    history = json.loads(pref.history_json) if pref.history_json else []
    all_active = list(dict.fromkeys(clean_selected + clean_custom))

    data = StudentTopicsPreferenceResponse(
        selected_topics=clean_selected,
        custom_topics=clean_custom,
        all_active_topics=all_active,
        daily_streak=pref.daily_streak,
        last_assessment_date=pref.last_assessment_date,
        total_assessments_taken=len(history),
    )
    return APIResponse(success=True, message="Learning topics preferences saved", data=data)


@router.get("/topics/guide", response_model=APIResponse[StudyMaterialDetail])
def get_or_generate_topic_guide(
    topic: str = Query(..., description="Topic name to retrieve or generate study guide for"),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Retrieves an existing placement guide for a topic or dynamically generates one for custom subjects."""
    clean_topic = topic.strip()
    clean_lower = clean_topic.lower()

    # Search existing study material
    materials = db.query(StudyMaterial).all()
    target_mat = None
    for m in materials:
        tags = [t.lower() for t in (json.loads(m.tags_json) if m.tags_json else [])]
        if (clean_lower in m.title.lower() or 
            clean_lower in m.slug.lower() or 
            any(clean_lower in tg for tg in tags) or
            any(tg in clean_lower for tg in tags if len(tg) > 3)):
            target_mat = m
            break

    if not target_mat:
        safe_slug = "".join(c if c.isalnum() else "-" for c in clean_lower).strip("-")
        slug = f"guide-{safe_slug}"[:60]
        
        # Check if slug exists
        existing_with_slug = db.query(StudyMaterial).filter(StudyMaterial.slug == slug).first()
        if existing_with_slug:
            target_mat = existing_with_slug
        else:
            markdown_content = f"""# {clean_topic} Placement Study Guide & Cheatsheet

### 📌 Overview & Relevance in Placement Exams
**{clean_topic}** is a highly valuable subject in campus recruitment drives and technical rounds. Top tech recruiters evaluate candidates on conceptual clarity, real-world applicability, and architectural awareness.

---

### 🔑 1. Core Principles & Key Concepts
1. **Fundamentals & Operating Lifecycle**: Understand how {clean_topic} executes, key configurations, and architectural patterns.
2. **Best Practices & Conventions**: Idiomatic usage, maintainable structure, and standard libraries.
3. **Common Pitfalls & Memory/Performance Considerations**: Edge cases, error handling, and latency bottlenecks.
4. **Integration in Full-Stack Systems**: How {clean_topic} interacts with databases, caches, and networking components.

---

### 💬 2. Top Placement Interview Questions on {clean_topic}
1. **Explain the architecture and execution pipeline of {clean_topic}.**
2. **What are the primary pros and trade-offs of using {clean_topic} over alternatives?**
3. **How do you troubleshoot performance issues, memory leaks, or concurrency bottlenecks in {clean_topic}?**
4. **Describe a production problem you would solve using {clean_topic}.**

---

### 🚀 3. Placement Exam Preparation Tips
- Review syntax, standard library routines, and common algorithms.
- Practice explaining concepts with quick whiteboard diagrams and code snippets.
- Master the underlying trade-offs and time/space complexity implications.
"""
            target_mat = StudyMaterial(
                title=f"{clean_topic} Placement Master Guide",
                slug=slug,
                category="custom_topics",
                content_type="guide",
                description=f"Core concepts, architecture, and placement interview questions for {clean_topic}.",
                content_markdown=markdown_content,
                company_tag="General Placement",
                difficulty="intermediate",
                estimated_read_time="10 mins",
                tags_json=json.dumps([clean_topic, "Placement", "Interview"]),
                order_index=99,
            )
            db.add(target_mat)
            db.commit()
            db.refresh(target_mat)

    tags = json.loads(target_mat.tags_json) if target_mat.tags_json else []
    return APIResponse(
        success=True,
        message=f"Study guide for {clean_topic}",
        data=StudyMaterialDetail(
            id=target_mat.id,
            title=target_mat.title,
            slug=target_mat.slug,
            category=target_mat.category,
            content_type=target_mat.content_type,
            description=target_mat.description,
            company_tag=target_mat.company_tag,
            difficulty=target_mat.difficulty,
            estimated_read_time=target_mat.estimated_read_time,
            tags=tags,
            content_markdown=target_mat.content_markdown,
            order_index=target_mat.order_index,
            created_at=target_mat.created_at,
            updated_at=target_mat.updated_at,
        )
    )


@router.get("/topics/curated-feed", response_model=APIResponse[PersonalizedLearningFeedResponse])
def get_curated_learning_feed(
    topic: Optional[str] = Query(None, description="Optional topic filter (e.g. Java, Python, or 'all')"),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Returns curated learning materials, cheatsheets, and sample practice questions tailored to student topics or a specific clicked topic."""
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == current_user.id).first()
    selected = json.loads(pref.selected_topics_json) if pref and pref.selected_topics_json else ["Quantitative Aptitude", "DSA"]
    custom = json.loads(pref.custom_topics_json) if pref and pref.custom_topics_json else []
    all_topics = list(dict.fromkeys(selected + custom))

    filter_topic = topic.strip() if topic and topic.strip().lower() != "all" else None
    search_topics = [filter_topic] if filter_topic else all_topics

    # Match study materials
    all_materials = db.query(StudyMaterial).all()
    matched = []
    featured_guide_slug = None

    for m in all_materials:
        tags = [t.lower() for t in (json.loads(m.tags_json) if m.tags_json else [])]
        cat = m.category.lower()
        title = m.title.lower()
        slug = m.slug.lower()

        # Check match with search_topics
        is_match = False
        for st in search_topics:
            st_l = st.lower()
            if (st_l in title or st_l in slug or st_l in tags or st_l in cat or 
                any(st_l in tg for tg in tags) or 
                (st_l == "dsa" and "dsa" in title) or
                (st_l == "sql" and "sql" in title) or
                ("java" in st_l and "java" in title and "javascript" not in title and "javascript" not in st_l)):
                is_match = True
                if filter_topic and not featured_guide_slug:
                    featured_guide_slug = m.slug
                break

        if is_match:
            matched.append(
                StudyMaterialListItem(
                    id=m.id,
                    title=m.title,
                    slug=m.slug,
                    category=m.category,
                    content_type=m.content_type,
                    description=m.description,
                    company_tag=m.company_tag,
                    difficulty=m.difficulty,
                    estimated_read_time=m.estimated_read_time,
                    tags=json.loads(m.tags_json) if m.tags_json else [],
                )
            )

    # If no specific materials matched a custom filter_topic, look for general guides or create one
    if filter_topic and not matched:
        # Check if we can find or generate a guide
        guide_resp = get_or_generate_topic_guide(topic=filter_topic, current_user=current_user, db=db)
        if guide_resp and guide_resp.data:
            g = guide_resp.data
            featured_guide_slug = g.slug
            matched.append(
                StudyMaterialListItem(
                    id=g.id,
                    title=g.title,
                    slug=g.slug,
                    category=g.category,
                    content_type=g.content_type,
                    description=g.description,
                    company_tag=g.company_tag,
                    difficulty=g.difficulty,
                    estimated_read_time=g.estimated_read_time,
                    tags=g.tags,
                )
            )

    # If filtering for "all" and still small, add top placement guides
    if not filter_topic and len(matched) < 4:
        for m in all_materials:
            if not any(item.id == m.id for item in matched):
                matched.append(
                    StudyMaterialListItem(
                        id=m.id,
                        title=m.title,
                        slug=m.slug,
                        category=m.category,
                        content_type=m.content_type,
                        description=m.description,
                        company_tag=m.company_tag,
                        difficulty=m.difficulty,
                        estimated_read_time=m.estimated_read_time,
                        tags=json.loads(m.tags_json) if m.tags_json else [],
                    )
                )
                if len(matched) >= 6:
                    break

    # Collect sample practice questions from roadmap milestones matching search topics
    roadmaps = db.query(LearningRoadmap).all()
    sample_questions = []
    for r in roadmaps:
        milestones = json.loads(r.milestones_json) if r.milestones_json else []
        for m in milestones:
            m_subject = (m.get("subject") or "").lower()
            m_title = (m.get("title") or "").lower()
            m_topics = [t.lower() for t in m.get("topics", [])]

            matches_milestone = any(
                st.lower() in m_subject or st.lower() in m_title or any(st.lower() in mt for mt in m_topics)
                for st in search_topics
            )

            if matches_milestone:
                for q in m.get("practice_questions", [])[:3]:
                    sample_questions.append(
                        MilestoneQuizQuestionOut(
                            id=q.get("id", str(uuid.uuid4())),
                            question=q.get("question", ""),
                            options=q.get("options", []),
                            topic=m.get("subject", "Placement Prep"),
                            difficulty=q.get("difficulty", "medium"),
                            marks=float(q.get("marks", 1.0)),
                        )
                    )
            if len(sample_questions) >= 8:
                break

    # If practice questions are still fewer than 4 (especially for specific custom topics),
    # generate a few tailored practice questions dynamically
    if len(sample_questions) < 4:
        try:
            extra_qs = generate_aptitude_questions_ai(
                topics=search_topics[:2],
                num_questions=4 - len(sample_questions),
                difficulty="medium",
            )
            for eq in extra_qs:
                sample_questions.append(
                    MilestoneQuizQuestionOut(
                        id=str(eq.get("id", uuid.uuid4())),
                        question=eq.get("question", ""),
                        options=eq.get("options", []),
                        topic=filter_topic or "Technical Practice",
                        difficulty=eq.get("difficulty", "medium"),
                        marks=float(eq.get("marks", 1.0)),
                    )
                )
        except Exception:
            pass

    feed = PersonalizedLearningFeedResponse(
        selected_topics=selected,
        custom_topics=custom,
        matched_materials=matched[:8],
        practice_questions_sample=sample_questions[:8],
        active_filter_topic=filter_topic,
        featured_guide_slug=featured_guide_slug or (matched[0].slug if matched else None),
    )
    return APIResponse(success=True, message="Personalized learning materials and practice feed", data=feed)



@router.post("/topics/daily-assessment/start", response_model=APIResponse[DailyAssessmentStartResponse])
def start_daily_assessment(
    topic: Optional[str] = Query(None, description="Optional single topic focus (e.g., 'Java', 'Python')"),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Generates a daily placement assessment dynamically mixing the student's chosen topics.
    Strictly 30 seconds per question (10 questions = 5 minutes).
    Can also be focused specifically on a single subject like Java or Python.
    """
    if topic:
        all_topics = [topic.strip()]
    else:
        pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == current_user.id).first()
        selected = json.loads(pref.selected_topics_json) if pref and pref.selected_topics_json else ["Quantitative Aptitude", "Logical Reasoning", "Data Structures & Algorithms (DSA)"]
        custom = json.loads(pref.custom_topics_json) if pref and pref.custom_topics_json else []
        all_topics = list(dict.fromkeys(selected + custom))
        if not all_topics:
            all_topics = ["Quantitative Aptitude", "Logical Reasoning", "SQL & Database Queries"]

    # Generate 10 questions distributed across the student's chosen topics
    ai_questions = generate_aptitude_questions_ai(
        topics=all_topics,
        num_questions=10,
        difficulty="mixed",
        marks_per_question=1.0,
    )

    assessment_id = f"daily-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    session_id = f"session-daily-{uuid.uuid4().hex[:12]}"

    stored_questions = []
    questions_out = []

    for idx, q in enumerate(ai_questions):
        qid = f"{session_id}-q{idx+1}"
        stored_questions.append({
            "id": qid,
            "question": q.question,
            "options": q.options,
            "correct_option_index": q.correct_option_index,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "marks": q.marks,
            "topic": q.topic_name,
        })
        questions_out.append(
            MilestoneQuizQuestionOut(
                id=qid,
                question=q.question,
                options=q.options,
                topic=q.topic_name,
                difficulty=q.difficulty,
                marks=q.marks,
            )
        )

    ACTIVE_AI_QUIZZES[session_id] = {
        "assessment_id": assessment_id,
        "topics_covered": all_topics,
        "questions": stored_questions,
        "created_at": time.time(),
    }

    # Clean old sessions older than 3 hours
    now = time.time()
    for k in list(ACTIVE_AI_QUIZZES.keys()):
        if now - ACTIVE_AI_QUIZZES[k].get("created_at", 0) > 10800:
            ACTIVE_AI_QUIZZES.pop(k, None)

    # Strictly 30 seconds per question (10 Qs = 5 mins)
    duration_mins = max(1, math.ceil(len(questions_out) * 30 / 60))

    data = DailyAssessmentStartResponse(
        assessment_id=assessment_id,
        session_id=session_id,
        date_str=datetime.now(timezone.utc).strftime("%B %d, %Y"),
        topics_covered=all_topics,
        duration_minutes=duration_mins,
        total_questions=len(questions_out),
        passing_percentage=60.0,
        questions=questions_out,
    )
    return APIResponse(success=True, message="Daily placement assessment generated", data=data)


@router.post("/topics/daily-assessment/submit", response_model=APIResponse[DailyAssessmentResultResponse])
def submit_daily_assessment(
    payload: DailyAssessmentSubmitRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Submits and evaluates the student's daily placement assessment.
    Updates daily streak, tracks topic accuracy, and returns step-by-step solutions.
    """
    session_data = ACTIVE_AI_QUIZZES.get(payload.session_id)
    if not session_data:
        raise NotFoundError("Assessment session expired or not found. Please start a new daily assessment.")

    questions = session_data["questions"]
    assessment_id = session_data.get("assessment_id", f"daily-{uuid.uuid4().hex[:6]}")
    topics_covered = session_data.get("topics_covered", [])

    total_marks = 0.0
    score = 0.0
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    review_items = []

    for q in questions:
        qid = q["id"]
        q_marks = float(q.get("marks", 1.0))
        total_marks += q_marks
        correct_idx = int(q.get("correct_option_index", 0))

        user_ans = payload.answers.get(qid)
        if user_ans is None:
            unanswered_count += 1
            is_correct = False
            user_selected = None
        else:
            user_selected = int(user_ans)
            if user_selected == correct_idx:
                correct_count += 1
                score += q_marks
                is_correct = True
            else:
                wrong_count += 1
                is_correct = False

        review_items.append(
            MilestoneQuizReviewItem(
                question_id=qid,
                question=q.get("question", ""),
                options=q.get("options", []),
                correct_option_index=correct_idx,
                user_selected_index=user_selected,
                is_correct=is_correct,
                explanation=q.get("explanation", "Review the relevant concept and practice formula."),
            )
        )

    percentage = round((score / total_marks * 100.0) if total_marks > 0 else 0.0, 1)
    passed = percentage >= 60.0

    # Update StudentLearningPreference streak & history
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == current_user.id).first()
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not pref:
        pref = StudentLearningPreference(
            user_id=current_user.id,
            selected_topics_json="[]",
            custom_topics_json="[]",
            daily_streak=1,
            last_assessment_date=today_str,
            history_json="[]",
        )
        db.add(pref)
    else:
        if pref.last_assessment_date != today_str:
            pref.daily_streak = (pref.daily_streak or 0) + 1
            pref.last_assessment_date = today_str

    history = json.loads(pref.history_json) if pref.history_json else []
    history.append({
        "assessment_id": assessment_id,
        "date": today_str,
        "score": score,
        "total_marks": total_marks,
        "percentage": percentage,
        "passed": passed,
        "time_taken_seconds": payload.time_taken_seconds,
        "topics_count": len(topics_covered),
    })
    pref.history_json = json.dumps(history[-20:])  # keep last 20

    db.commit()
    db.refresh(pref)

    feedback = (
        f"Outstanding! You scored {percentage}% across your selected placement subjects. Streak increased to {pref.daily_streak} days! 🔥"
        if passed
        else f"Good effort! You scored {percentage}%. Review the step-by-step solutions below to strengthen your weak topics."
    )

    data = DailyAssessmentResultResponse(
        assessment_id=assessment_id,
        total_questions=len(questions),
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        score=score,
        total_marks=total_marks,
        percentage=percentage,
        passed=passed,
        daily_streak=pref.daily_streak,
        time_taken_seconds=payload.time_taken_seconds,
        feedback_message=feedback,
        topics_covered=topics_covered,
        review_items=review_items,
    )
    return APIResponse(success=True, message="Daily assessment submitted and evaluated", data=data)


# -----------------------------------------------------------------------------
# PRESCRIBED TEXTBOOKS & BOOK-GROUNDED EXAM CURRICULUM
# -----------------------------------------------------------------------------

@router.get("/books/prescribed", response_model=APIResponse[List[Dict[str, Any]]])
def get_prescribed_books(
    topic: Optional[str] = Query(None, description="Optional topic filter to show textbooks for a specific topic or 'all'"),
):
    """
    Returns list of official prescribed textbooks covering all active learning topics
    (DSA, SQL, Quant, Reasoning, Java, Python, JS/TS, Data Engineering, AI/ML),
    chapters, syllabus coverage, and verified physical PDF status.
    """
    from app.services.book_curriculum_service import get_prescribed_books_status
    books = get_prescribed_books_status(filter_topic=topic if isinstance(topic, str) else None)
    return APIResponse(
        success=True,
        message="Official prescribed textbooks and exam curriculum",
        data=books,
    )


@router.get("/books/chapters", response_model=APIResponse[Dict[str, Any]])
@router.get("/books/{subject:path}/chapters", response_model=APIResponse[Dict[str, Any]])
def get_book_chapters(
    subject: str = "java",
    db: Session = Depends(get_db),
):
    """Returns detailed chapter breakdown and syllabus topics for any prescribed book."""
    from app.services.book_curriculum_service import (
        SUBJECT_TO_TEXTBOOK,
        ALL_PRESCRIBED_TEXTBOOKS,
        JAVA_TEXTBOOK,
        find_prescribed_book_pdf,
    )
    norm = subject.lower().strip()
    book = None
    # 1. Exact slug or title match
    for b in ALL_PRESCRIBED_TEXTBOOKS:
        if norm == b["slug"].lower() or norm == b["subject"].lower() or norm in b["slug"].lower():
            book = b
            break
    # 2. Key matching from longest to shortest key (e.g. javascript before java)
    if not book:
        sorted_keys = sorted(SUBJECT_TO_TEXTBOOK.keys(), key=len, reverse=True)
        for k in sorted_keys:
            if k in norm or norm in k:
                book = SUBJECT_TO_TEXTBOOK[k]
                break
    if not book:
        book = JAVA_TEXTBOOK

    pdf_path = find_prescribed_book_pdf(book["subject"])

    from app.services.course_real_world_pedagogy import get_chapter_pedagogy, get_course_progression_overview
    raw_chapters = book.get("chapters", [])
    enriched_chapters = []
    for ch in raw_chapters:
        ch_copy = dict(ch)
        c_num = ch_copy.get("chapter_num") or ch_copy.get("num", 1)
        c_title = ch_copy.get("title", "")
        ped = get_chapter_pedagogy(book["subject"], c_num, c_title, len(raw_chapters))
        ch_copy["progression_stage"] = ped.get("stage_num", 1)
        ch_copy["stage_title"] = ped.get("stage_title", "Foundations")
        ch_copy["stage_badge"] = ped.get("stage_badge", "Fundamentals")
        ch_copy["stage_color"] = ped.get("stage_color", "success")
        ch_copy["stage_guidance"] = ped.get("guidance", "")
        ch_copy["real_world_application"] = ped.get("real_world_application", {})
        enriched_chapters.append(ch_copy)

    progression_overview = get_course_progression_overview(book["subject"], book["title"], len(raw_chapters))

    data = {
        "book_title": book["title"],
        "subject": book["subject"],
        "slug": book["slug"],
        "edition": book["edition"],
        "author": book["author"],
        "description": book["description"],
        "chapters_count": len(raw_chapters),
        "progression_overview": progression_overview,
        "chapters": enriched_chapters,
        "has_physical_pdf": pdf_path is not None,
        "exam_rule": "All exam questions for this subject are strictly grounded in these chapters.",
    }
    return APIResponse(success=True, message=f"{book['subject']} textbook curriculum", data=data)


@router.get("/books/{subject_or_slug:path}/download-pdf")
def download_prescribed_book_pdf(
    subject_or_slug: str,
):
    """Downloads official prescribed textbook PDF for students to study offline."""
    import os
    from pathlib import Path
    from fastapi.responses import FileResponse
    from app.services.book_curriculum_service import (
        find_prescribed_book_pdf,
        SUBJECT_TO_TEXTBOOK,
        ALL_PRESCRIBED_TEXTBOOKS,
    )

    norm = subject_or_slug.lower().strip()
    book = None
    # 1. Exact slug or title match
    for b in ALL_PRESCRIBED_TEXTBOOKS:
        if norm == b["slug"].lower() or norm == b["subject"].lower() or norm in b["slug"].lower():
            book = b
            break
    # 2. Key matching from longest to shortest key
    if not book:
        sorted_keys = sorted(SUBJECT_TO_TEXTBOOK.keys(), key=len, reverse=True)
        for k in sorted_keys:
            if k in norm or norm in k:
                book = SUBJECT_TO_TEXTBOOK[k]
                break

    pdf_path = find_prescribed_book_pdf(norm)
    if not pdf_path and book:
        pdf_path = find_prescribed_book_pdf(book["slug"]) or find_prescribed_book_pdf(book["subject"])

    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail=f"Prescribed textbook PDF not found for '{subject_or_slug}'.",
        )

    filename = Path(pdf_path).name
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=filename,
    )


@router.post("/books/upload", response_model=APIResponse[Dict[str, Any]])
async def upload_prescribed_book_pdf(
    subject: str = Form(..., description="'java' or 'python'"),
    file: UploadFile = File(..., description="PDF textbook file"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate)),
):
    """
    Uploads a physical PDF textbook for Java or Python.
    Extracts chapters via PyMuPDF and updates the prescribed book knowledge base.
    """
    from pathlib import Path
    import shutil
    from app.services.book_curriculum_service import DATASET_BOOKS_DIR, ingest_book_pdf, seed_prescribed_books_to_db

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for textbooks")

    norm_sub = subject.lower().strip()
    safe_name = f"{norm_sub}_prescribed_book.pdf"
    dest_path = DATASET_BOOKS_DIR / safe_name

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_result = ingest_book_pdf(str(dest_path), subject=norm_sub)
    seed_prescribed_books_to_db(db)

    return APIResponse(
        success=True,
        message=f"{norm_sub.title()} textbook PDF uploaded and processed successfully",
        data={
            "filename": file.filename,
            "saved_as": safe_name,
            "ingest_result": ingest_result,
            "exam_grounding_active": True,
        },
    )


# -----------------------------------------------------------------------------
# COMPANY PLACEMENT INTELLIGENCE, EXAM PATTERNS & APTITUDE ANALYSIS
# -----------------------------------------------------------------------------

@router.get("/companies", response_model=APIResponse[List[Dict[str, Any]]])
def list_company_intelligence(db: Session = Depends(get_db)):
    """
    Returns summarized intelligence for all top campus recruiters and active hiring companies:
    VGen, Vaarg, TCS, Infosys, Cognizant, Accenture, Wipro, Amazon, Deloitte, Capgemini, Goldman Sachs, Zoho, Google, Microsoft.
    """
    from app.services.company_intelligence_service import get_all_companies_intelligence
    data = get_all_companies_intelligence(db=db)
    return APIResponse(success=True, message="Top placement company intelligence", data=data)


@router.get("/companies/{slug}", response_model=APIResponse[Dict[str, Any]])
def get_company_intelligence(slug: str, db: Session = Depends(get_db)):
    """
    Returns deep-dive intelligence for a company:
    - Hiring cadres and CTC packages
    - Selection rounds
    - Exact exam patterns and sectional cutoffs
    - Aptitude question trends (Quant, Reasoning, Verbal weights & exam tips)
    - 4-week placement preparation strategy
    - Sample company placement questions with verified step-by-step explanations
    - Recent hiring process questions asked to selected/shortlisted candidates
    """
    from app.services.company_intelligence_service import get_company_intelligence_detail
    detail = get_company_intelligence_detail(slug, db=db)
    if not detail:
        raise NotFoundError(f"Company intelligence for '{slug}' not found")
    return APIResponse(success=True, message=f"{detail['name']} intelligence and exam trends", data=detail)


@router.post("/companies/{slug}/start-test", response_model=APIResponse[DailyAssessmentStartResponse])
def start_company_mock_test(
    slug: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Generates and starts a timed company-specific mock exam.
    Questions are constructed directly from analyzed company question patterns and topics.
    Strictly 30-45 seconds per question to build corporate exam speed.
    """
    from app.services.company_intelligence_service import get_company_intelligence_detail
    detail = get_company_intelligence_detail(slug, db=db)
    if not detail:
        raise NotFoundError(f"Company '{slug}' not found")

    sample_questions = detail.get("sample_questions", [])
    assessment_id = f"company-{slug}-{uuid.uuid4().hex[:6]}"
    session_id = f"session-company-{uuid.uuid4().hex[:12]}"

    stored_questions = []
    questions_out = []

    # 1. Include verified company sample questions first
    for idx, sq in enumerate(sample_questions):
        qid = f"{session_id}-q{idx+1}"
        stored_questions.append({
            "id": qid,
            "question": sq["question"],
            "options": sq["options"],
            "correct_option_index": sq["correct_option_index"],
            "explanation": sq["explanation"],
            "difficulty": sq.get("difficulty", "medium"),
            "marks": 1.0,
            "topic": sq.get("tag", detail["name"]),
        })
        questions_out.append(
            MilestoneQuizQuestionOut(
                id=qid,
                question=sq["question"],
                options=sq["options"],
                topic=sq.get("tag", detail["name"]),
                difficulty=sq.get("difficulty", "medium"),
                marks=1.0,
            )
        )

    # 2. Augment up to 8 questions using company's top quantitative and reasoning topics
    needed = 8 - len(questions_out)
    if needed > 0:
        top_topics = []
        for trend in detail.get("aptitude_analysis", {}).get("quantitative_trends", [])[:2]:
            top_topics.append(trend["topic"].split("/")[0].strip())
        for trend in detail.get("aptitude_analysis", {}).get("reasoning_trends", [])[:2]:
            top_topics.append(trend["topic"].split("/")[0].strip())
        if not top_topics:
            top_topics = ["Quantitative Aptitude", "Logical Reasoning"]

        try:
            extra_qs = generate_aptitude_questions_ai(
                topics=top_topics,
                num_questions=needed,
                difficulty="mixed",
                marks_per_question=1.0,
            )
            for idx, eq in enumerate(extra_qs):
                qid = f"{session_id}-q{len(questions_out)+1}"
                stored_questions.append({
                    "id": qid,
                    "question": eq.question,
                    "options": eq.options,
                    "correct_option_index": eq.correct_option_index,
                    "explanation": eq.explanation,
                    "difficulty": eq.difficulty,
                    "marks": eq.marks,
                    "topic": f"{detail['name']} {eq.topic_name}",
                })
                questions_out.append(
                    MilestoneQuizQuestionOut(
                        id=qid,
                        question=eq.question,
                        options=eq.options,
                        topic=f"{detail['name']} {eq.topic_name}",
                        difficulty=eq.difficulty,
                        marks=eq.marks,
                    )
                )
        except Exception as e:
            logger.warning(f"Error generating extra AI questions for {slug}: {e}")

    ACTIVE_AI_QUIZZES[session_id] = {
        "assessment_id": assessment_id,
        "company_slug": slug,
        "company_name": detail["name"],
        "questions": stored_questions,
        "created_at": time.time(),
    }

    duration_mins = max(1, math.ceil(len(questions_out) * 30 / 60))

    data = DailyAssessmentStartResponse(
        assessment_id=assessment_id,
        session_id=session_id,
        date_str=f"{detail['name']} Mock Drive",
        topics_covered=[t["section"] for t in detail.get("exam_pattern", [])[:4]],
        duration_minutes=duration_mins,
        total_questions=len(questions_out),
        passing_percentage=65.0,
        questions=questions_out,
    )
    return APIResponse(success=True, message=f"{detail['name']} mock exam generated", data=data)


@router.post("/companies/{slug}/submit-test", response_model=APIResponse[DailyAssessmentResultResponse])
def submit_company_mock_test(
    slug: str,
    payload: DailyAssessmentSubmitRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Submits and evaluates the student's company-specific mock exam.
    Returns score, percentile feedback, and question-by-question explanations.
    """
    session_data = ACTIVE_AI_QUIZZES.get(payload.session_id)
    if not session_data:
        raise NotFoundError("Assessment session expired or not found. Please start a new company mock test.")

    questions = session_data["questions"]
    assessment_id = session_data.get("assessment_id", f"company-{slug}-{uuid.uuid4().hex[:6]}")
    company_name = session_data.get("company_name", slug.upper())

    total_marks = 0.0
    score = 0.0
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    review_items = []

    for q in questions:
        qid = q["id"]
        q_marks = float(q.get("marks", 1.0))
        total_marks += q_marks
        correct_idx = int(q.get("correct_option_index", 0))

        user_ans = payload.answers.get(qid)
        if user_ans is None:
            unanswered_count += 1
            is_correct = False
            user_selected = None
        else:
            user_selected = int(user_ans)
            if user_selected == correct_idx:
                correct_count += 1
                score += q_marks
                is_correct = True
            else:
                wrong_count += 1
                is_correct = False

        review_items.append(
            MilestoneQuizReviewItem(
                question_id=qid,
                question=q.get("question", ""),
                options=q.get("options", []),
                correct_option_index=correct_idx,
                user_selected_index=user_selected,
                is_correct=is_correct,
                explanation=q.get("explanation", "Review the company question patterns and shortcut formulas."),
            )
        )

    percentage = round((score / total_marks * 100.0) if total_marks > 0 else 0.0, 1)
    passed = percentage >= 65.0

    feedback = (
        f"Outstanding! You scored {percentage}% on the {company_name} mock assessment. You meet the recruitment cutoff!"
        if passed
        else f"You scored {percentage}%. The typical {company_name} cutoff is 65-70%. Review the step-by-step solutions below and practice more questions."
    )

    data = DailyAssessmentResultResponse(
        assessment_id=assessment_id,
        total_questions=len(questions),
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        score=score,
        total_marks=total_marks,
        percentage=percentage,
        passed=passed,
        daily_streak=1,
        time_taken_seconds=payload.time_taken_seconds,
        feedback_message=feedback,
        topics_covered=[company_name, "Company Mock Test"],
        review_items=review_items,
    )
    return APIResponse(success=True, message=f"{company_name} mock test evaluated", data=data)


@router.get("/{slug}", response_model=APIResponse[StudyMaterialDetail])
def get_study_material_detail(
    slug: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Fetches complete markdown content of a study guide or cheatsheet."""
    material = db.query(StudyMaterial).filter(StudyMaterial.slug == slug).first()
    if not material:
        raise NotFoundError(f"Study material '{slug}' not found")

    data = StudyMaterialDetail(
        id=material.id,
        title=material.title,
        slug=material.slug,
        category=material.category,
        content_type=material.content_type,
        description=material.description,
        company_tag=material.company_tag,
        difficulty=material.difficulty,
        estimated_read_time=material.estimated_read_time,
        tags=json.loads(material.tags_json) if material.tags_json else [],
        content_markdown=material.content_markdown,
    )
    return APIResponse(success=True, message="Study material detail", data=data)

