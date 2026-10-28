"""
aptitude.py — REST API router for AI-Based Aptitude Question Generation,
Recruiter Question Studio (Review/Edit/Regenerate/Publish), Placement Practice Tests,
Daily Sprints, and Candidate Evaluation.
"""
import datetime
import json
import logging
import math
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError, BadRequestError
from app.models.student import (
    AptitudeTopic,
    AptitudeQuestion,
    AptitudeOption,
    AptitudeTest,
    AptitudeAttempt,
    CandidateTestAttempt,
    CandidateAnswer,
    AptitudeTestResult,
)
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.student import (
    AptitudeTopicOut,
    AptitudeTopicCreate,
    AptitudeTopicUpdate,
    AptitudeQuestionCreateStandalone,
    AptitudeVectorSearchRequest,
    AptitudeQuestionTakingOut,
    AptitudeQuestionReviewOut,
    AptitudeTestOut,
    AptitudeSubmissionRequest,
    AptitudeAttemptResult,
)
from app.schemas.aptitude_generator import (
    AptitudeGenerateRequest,
    AptitudeQuestionGeneratedItem,
    AptitudeQuestionUpdate,
    AptitudeOptionOut,
    AptitudeQuestionDetail,
    AptitudeTestDetail,
    AptitudeTestSummary,
    CandidateTakingOption,
    CandidateTakingQuestion,
    CandidateTakingTestResponse,
    CandidateAptitudeSubmitRequest,
    CandidateAnswerReviewItem,
    CandidateTestResultResponse,
)
from app.services.ai_aptitude_service import (
    generate_aptitude_questions_ai,
    regenerate_single_question_ai,
)
from app.services.qdrant_service import (
    COLLECTION_APTITUDE,
    check_aptitude_question_duplicate,
    delete_document,
    search as vector_search,
    sync_all_from_db,
    upsert_batch,
    upsert_document,
)

logger = logging.getLogger("ai_recruiter.aptitude")

router = APIRouter(prefix="/aptitude", tags=["Aptitude & AI Generator"])

RECRUITER_ROLES = (UserRole.recruiter, UserRole.admin, UserRole.company_admin, UserRole.superadmin)


def _serialize_test_detail(test: AptitudeTest, db: Session) -> AptitudeTestDetail:
    """Helper to convert AptitudeTest ORM model to AptitudeTestDetail response schema."""
    topics = []
    if test.topics_json:
        try:
            topics = json.loads(test.topics_json)
        except Exception:
            topics = []

    questions_out: List[AptitudeQuestionDetail] = []
    for q in test.questions:
        options_out: List[AptitudeOptionOut] = []
        if q.options:
            for opt in q.options:
                options_out.append(
                    AptitudeOptionOut(
                        id=opt.id,
                        option_letter=opt.option_letter,
                        option_text=opt.option_text,
                        is_correct=opt.is_correct,
                        order_index=opt.order_index,
                    )
                )
        elif q.options_json:
            try:
                raw_opts = json.loads(q.options_json)
                letters = ["A", "B", "C", "D"]
                for idx, opt_str in enumerate(raw_opts):
                    options_out.append(
                        AptitudeOptionOut(
                            id=None,
                            option_letter=letters[idx] if idx < 4 else f"Opt {idx+1}",
                            option_text=str(opt_str),
                            is_correct=(idx == q.correct_option_index),
                            order_index=idx,
                        )
                    )
            except Exception:
                options_out = []

        questions_out.append(
            AptitudeQuestionDetail(
                id=q.id,
                test_id=q.test_id,
                topic_name=q.topic_name or q.subtopic,
                subtopic=q.subtopic,
                question=q.question,
                options=options_out,
                correct_option_index=q.correct_option_index,
                explanation=q.explanation,
                difficulty=q.difficulty,
                marks=q.marks,
                status=q.status,
            )
        )

    attempts_count = db.query(CandidateTestAttempt).filter(CandidateTestAttempt.test_id == test.id).count()

    return AptitudeTestDetail(
        id=test.id,
        title=test.title,
        description=test.description,
        category=test.category,
        topics=topics,
        difficulty=test.difficulty,
        duration_minutes=test.duration_minutes,
        total_questions=test.total_questions,
        marks_per_question=test.marks_per_question,
        total_marks=test.total_marks,
        passing_percentage=test.passing_percentage,
        status=test.status,
        is_active=test.is_active,
        created_at=test.created_at,
        questions=questions_out,
        attempts_count=attempts_count,
    )


# ==============================================================================
# 1. AI QUESTION GENERATOR & RECRUITER STUDIO
# ==============================================================================

@router.post("/generate", response_model=APIResponse[AptitudeTestDetail])
def generate_aptitude_test_endpoint(
    payload: AptitudeGenerateRequest,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    AI-Powered Aptitude Test Generator.
    Recruiter/Admin enters test title, topics, question count, difficulty, duration, and marks.
    Google Gemini (or resilient mathematical engine) generates verified MCQs.
    Test is saved in 'draft' status ready for recruiter preview and approval.
    """
    try:
        # 1. Generate questions using AI service
        generated_questions: List[AptitudeQuestionGeneratedItem] = generate_aptitude_questions_ai(
            topics=payload.topics,
            num_questions=payload.num_questions,
            difficulty=payload.difficulty,
            marks_per_question=payload.marks_per_question,
        )

        if not generated_questions:
            raise BadRequestError("AI was unable to generate questions for the specified topics. Please retry.")

        # 2. Determine duration if not explicitly provided
        duration = payload.duration_minutes
        if not duration or duration <= 0:
            # Default to 1 minute per question or minimum 5 minutes
            duration = max(5, int(payload.num_questions * 1))

        total_questions = len(generated_questions)
        total_marks = round(total_questions * payload.marks_per_question, 2)

        # 3. Create AptitudeTest record in 'draft' status
        test = AptitudeTest(
            title=payload.title.strip(),
            description=f"AI Generated Aptitude Test on {', '.join(payload.topics)}",
            category="recruiter_test",
            topics_json=json.dumps(payload.topics),
            difficulty=payload.difficulty.lower(),
            duration_minutes=duration,
            total_questions=total_questions,
            marks_per_question=payload.marks_per_question,
            total_marks=total_marks,
            passing_percentage=60.0,
            status="draft",  # Do not automatically publish without recruiter approval
            is_active=True,
            created_by_user_id=current_user.id,
        )
        db.add(test)
        db.flush()

        # 4. Create AptitudeQuestion and AptitudeOption records
        letters = ["A", "B", "C", "D"]
        for item in generated_questions:
            question_rec = AptitudeQuestion(
                test_id=test.id,
                subtopic=item.subtopic,
                topic_name=item.topic_name,
                question=item.question,
                options_json=json.dumps(item.options),
                correct_option_index=item.correct_option_index,
                explanation=item.explanation,
                difficulty=item.difficulty,
                marks=item.marks,
                status="draft",
            )
            db.add(question_rec)
            db.flush()

            # Create 4 relational options
            for idx, opt_text in enumerate(item.options):
                opt_rec = AptitudeOption(
                    question_id=question_rec.id,
                    option_letter=letters[idx],
                    option_text=opt_text,
                    is_correct=(idx == item.correct_option_index),
                    order_index=idx,
                )
                db.add(opt_rec)

        db.commit()
        db.refresh(test)

        logger.info(
            f"Recruiter {current_user.email} generated test '{test.title}' with {total_questions} questions (draft)."
        )

        serialized = _serialize_test_detail(test, db)
        return APIResponse(
            success=True,
            message="Aptitude test generated successfully. Review questions in the studio before publishing.",
            data=serialized,
        )

    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to generate aptitude test: {exc}", exc_info=True)
        if isinstance(exc, (BadRequestError, HTTPException)):
            raise exc
        raise HTTPException(status_code=500, detail=f"Failed to generate aptitude test: {str(exc)}")


@router.put("/questions/{question_id}", response_model=APIResponse[AptitudeQuestionDetail])
def edit_aptitude_question_endpoint(
    question_id: str,
    payload: AptitudeQuestionUpdate,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Recruiter/Admin modifies an AI-generated question (question text, options, correct answer, explanation).
    """
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise NotFoundError("Invalid question ID format")

    question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == qid).first()
    if not question:
        raise NotFoundError("Question not found")

    # Update basic fields if provided
    if payload.question is not None and payload.question.strip():
        question.question = payload.question.strip()
    if payload.topic_name is not None:
        question.topic_name = payload.topic_name.strip()
    if payload.difficulty is not None:
        question.difficulty = payload.difficulty.lower()
    if payload.explanation is not None:
        question.explanation = payload.explanation.strip()
    if payload.marks is not None:
        question.marks = payload.marks

    # Update options and correct answer
    letters = ["A", "B", "C", "D"]
    corr_idx = payload.correct_option_index if payload.correct_option_index is not None else question.correct_option_index

    if payload.options is not None:
        if len(payload.options) != 4:
            raise BadRequestError("Exactly 4 options must be provided.")
        question.options_json = json.dumps(payload.options)
        question.correct_option_index = corr_idx

        # Update or recreate aptitude_options
        existing_options = db.query(AptitudeOption).filter(AptitudeOption.question_id == question.id).order_by(AptitudeOption.order_index).all()
        if len(existing_options) == 4:
            for idx, opt_rec in enumerate(existing_options):
                opt_rec.option_text = payload.options[idx].strip()
                opt_rec.is_correct = (idx == corr_idx)
        else:
            for opt_rec in existing_options:
                db.delete(opt_rec)
            db.flush()
            for idx, opt_text in enumerate(payload.options):
                new_opt = AptitudeOption(
                    question_id=question.id,
                    option_letter=letters[idx],
                    option_text=opt_text.strip(),
                    is_correct=(idx == corr_idx),
                    order_index=idx,
                )
                db.add(new_opt)

    elif payload.correct_option_index is not None:
        question.correct_option_index = payload.correct_option_index
        # Update existing options is_correct flag
        options = db.query(AptitudeOption).filter(AptitudeOption.question_id == question.id).order_by(AptitudeOption.order_index).all()
        for idx, opt_rec in enumerate(options):
            opt_rec.is_correct = (idx == payload.correct_option_index)

    # Re-calculate test total marks if marks changed
    if question.test:
        test = question.test
        all_qs = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
        test.total_marks = round(sum(q.marks for q in all_qs), 2)

    db.commit()
    db.refresh(question)

    # Synchronize updated question to Qdrant vector database
    try:
        topic_str = question.topic_name or (question.topic.name if question.topic else "")
        full_text = f"Topic: {topic_str}\nSubtopic: {question.subtopic}\nQuestion: {question.question}"
        upsert_document(
            collection_name=COLLECTION_APTITUDE,
            doc_id=question.id,
            text=full_text,
            metadata={
                "question_id": str(question.id),
                "topic_name": topic_str,
                "subtopic": question.subtopic,
                "difficulty": question.difficulty,
                "company_tag": question.company_tag,
            },
        )
    except Exception as exc:
        logger.warning("Qdrant: Failed to update aptitude question vector %s: %s", question.id, exc)

    # Format return
    opts_out = [
        AptitudeOptionOut(
            id=opt.id,
            option_letter=opt.option_letter,
            option_text=opt.option_text,
            is_correct=opt.is_correct,
            order_index=opt.order_index,
        )
        for opt in sorted(question.options, key=lambda o: o.order_index)
    ]

    return APIResponse(
        success=True,
        message="Question updated successfully",
        data=AptitudeQuestionDetail(
            id=question.id,
            test_id=question.test_id,
            topic_name=question.topic_name,
            subtopic=question.subtopic,
            question=question.question,
            options=opts_out,
            correct_option_index=question.correct_option_index,
            explanation=question.explanation,
            difficulty=question.difficulty,
            marks=question.marks,
            status=question.status,
        ),
    )


@router.delete("/questions/{question_id}", response_model=APIResponse[dict])
def delete_aptitude_question_endpoint(
    question_id: str,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Recruiter/Admin deletes an unwanted question from the generated test.
    Automatically recalculates total questions and total marks for the test.
    """
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise NotFoundError("Invalid question ID format")

    question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == qid).first()
    if not question:
        raise NotFoundError("Question not found")

    test = question.test
    db.delete(question)
    db.flush()

    if test:
        remaining_qs = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
        test.total_questions = len(remaining_qs)
        test.total_marks = round(sum(q.marks for q in remaining_qs), 2)

    db.commit()

    # Delete question vector from Qdrant vector database
    try:
        delete_document(collection_name=COLLECTION_APTITUDE, doc_id=qid)
    except Exception as exc:
        logger.warning("Qdrant: Failed to delete aptitude question vector %s: %s", qid, exc)

    return APIResponse(
        success=True,
        message="Question deleted successfully",
        data={
            "deleted_question_id": str(qid),
            "remaining_questions": test.total_questions if test else 0,
            "total_marks": test.total_marks if test else 0,
        },
    )


@router.post("/questions/{question_id}/regenerate", response_model=APIResponse[AptitudeQuestionDetail])
def regenerate_single_question_endpoint(
    question_id: str,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Regenerates a single question using AI while maintaining the same topic, difficulty, and marks.
    """
    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise NotFoundError("Invalid question ID format")

    question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == qid).first()
    if not question:
        raise NotFoundError("Question not found")

    # Determine topic from question or test
    topic = question.topic_name or question.subtopic
    if not topic and question.test and question.test.topics_json:
        try:
            topic = json.loads(question.test.topics_json)[0]
        except Exception:
            topic = "Percentages"

    diff = question.difficulty or "medium"
    marks = question.marks or 1.0

    # Regenerate using AI engine
    new_q_item = regenerate_single_question_ai(
        topic=topic,
        difficulty=diff,
        marks_per_question=marks,
    )

    question.question = new_q_item.question
    question.subtopic = new_q_item.subtopic
    question.topic_name = new_q_item.topic_name
    question.options_json = json.dumps(new_q_item.options)
    question.correct_option_index = new_q_item.correct_option_index
    question.explanation = new_q_item.explanation
    question.difficulty = new_q_item.difficulty
    question.marks = new_q_item.marks

    # Recreate aptitude_options
    letters = ["A", "B", "C", "D"]
    existing_options = db.query(AptitudeOption).filter(AptitudeOption.question_id == question.id).all()
    for opt in existing_options:
        db.delete(opt)
    db.flush()

    for idx, opt_text in enumerate(new_q_item.options):
        new_opt = AptitudeOption(
            question_id=question.id,
            option_letter=letters[idx],
            option_text=opt_text,
            is_correct=(idx == new_q_item.correct_option_index),
            order_index=idx,
        )
        db.add(new_opt)

    db.commit()
    db.refresh(question)

    # Synchronize regenerated question to Qdrant vector database
    try:
        topic_str = question.topic_name or (question.topic.name if question.topic else "")
        full_text = f"Topic: {topic_str}\nSubtopic: {question.subtopic}\nQuestion: {question.question}"
        upsert_document(
            collection_name=COLLECTION_APTITUDE,
            doc_id=question.id,
            text=full_text,
            metadata={
                "question_id": str(question.id),
                "topic_name": topic_str,
                "subtopic": question.subtopic,
                "difficulty": question.difficulty,
                "company_tag": question.company_tag,
            },
        )
    except Exception as exc:
        logger.warning("Qdrant: Failed to update regenerated aptitude question vector %s: %s", question.id, exc)

    opts_out = [
        AptitudeOptionOut(
            id=opt.id,
            option_letter=opt.option_letter,
            option_text=opt.option_text,
            is_correct=opt.is_correct,
            order_index=opt.order_index,
        )
        for opt in sorted(question.options, key=lambda o: o.order_index)
    ]

    return APIResponse(
        success=True,
        message="Question regenerated successfully",
        data=AptitudeQuestionDetail(
            id=question.id,
            test_id=question.test_id,
            topic_name=question.topic_name,
            subtopic=question.subtopic,
            question=question.question,
            options=opts_out,
            correct_option_index=question.correct_option_index,
            explanation=question.explanation,
            difficulty=question.difficulty,
            marks=question.marks,
            status=question.status,
        ),
    )


@router.post("/tests/{test_id}/publish", response_model=APIResponse[AptitudeTestDetail])
def publish_aptitude_test_endpoint(
    test_id: str,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Recruiter publishes an approved aptitude test.
    Makes it visible and available to candidates on their dashboard.
    """
    try:
        tid = uuid.UUID(test_id)
    except ValueError:
        raise NotFoundError("Invalid test ID format")

    test = db.query(AptitudeTest).filter(AptitudeTest.id == tid).first()
    if not test:
        raise NotFoundError("Aptitude test not found")

    questions_count = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).count()
    if questions_count == 0:
        raise BadRequestError("Cannot publish an aptitude test without questions. Please generate or add questions first.")

    test.status = "published"
    test.is_active = True
    test.total_questions = questions_count

    # Mark all questions as approved
    db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).update(
        {"status": "approved"}, synchronize_session=False
    )

    db.commit()
    db.refresh(test)

    # Bulk index published test questions into Qdrant vector database
    try:
        test_questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
        apt_items = []
        for aq in test_questions:
            topic_str = aq.topic_name or (aq.topic.name if aq.topic else "")
            full_text = f"Topic: {topic_str}\nSubtopic: {aq.subtopic}\nQuestion: {aq.question}"
            apt_items.append({
                "id": str(aq.id),
                "text": full_text,
                "metadata": {
                    "question_id": str(aq.id),
                    "topic_name": topic_str,
                    "subtopic": aq.subtopic,
                    "difficulty": aq.difficulty,
                    "company_tag": aq.company_tag,
                },
            })
        if apt_items:
            upsert_batch(COLLECTION_APTITUDE, apt_items)
    except Exception as exc:
        logger.warning("Qdrant: Failed to batch index published questions: %s", exc)

    logger.info(f"Test '{test.title}' (ID: {test.id}) published by {current_user.email}.")

    serialized = _serialize_test_detail(test, db)
    return APIResponse(
        success=True,
        message="Aptitude test published successfully! Candidates can now take this assessment.",
        data=serialized,
    )


# ==============================================================================
# 2. TESTS RETRIEVAL (ROLE-AWARE)
# ==============================================================================

@router.get("/tests", response_model=APIResponse[List[AptitudeTestSummary]])
def get_aptitude_tests_endpoint(
    category: Optional[str] = Query(None, description="recruiter_test, daily_practice, topic_test, company_mock"),
    status: Optional[str] = Query(None, description="draft, published, all"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Role-aware test listing:
    - Recruiters/Admins: View all tests (draft, published) with full control and attempt counts.
    - Candidates: View published, active tests ready to take.
    """
    is_recruiter = current_user.role in RECRUITER_ROLES
    query = db.query(AptitudeTest)

    if is_recruiter:
        if status and status != "all":
            query = query.filter(AptitudeTest.status == status)
        if category:
            query = query.filter(AptitudeTest.category == category)
        # Recruiter sees tests created by them or all recruiter tests if admin
        if current_user.role == UserRole.recruiter:
            query = query.filter(
                (AptitudeTest.created_by_user_id == current_user.id) | (AptitudeTest.created_by_user_id == None)
            )
    else:
        # Candidate only sees published, active tests
        query = query.filter(AptitudeTest.status == "published", AptitudeTest.is_active == True)
        if category:
            query = query.filter(AptitudeTest.category == category)

    tests = query.order_by(AptitudeTest.created_at.desc()).all()

    data: List[AptitudeTestSummary] = []
    for t in tests:
        topics = []
        if t.topics_json:
            try:
                topics = json.loads(t.topics_json)
            except Exception:
                topics = []

        attempts_count = db.query(CandidateTestAttempt).filter(CandidateTestAttempt.test_id == t.id).count()

        data.append(
            AptitudeTestSummary(
                id=t.id,
                title=t.title,
                description=t.description,
                category=t.category,
                topics=topics,
                difficulty=t.difficulty,
                duration_minutes=t.duration_minutes,
                total_questions=t.total_questions,
                marks_per_question=t.marks_per_question,
                total_marks=t.total_marks,
                passing_percentage=t.passing_percentage,
                status=t.status,
                is_active=t.is_active,
                created_at=t.created_at,
                attempts_count=attempts_count,
            )
        )

    return APIResponse(success=True, message="Aptitude tests retrieved", data=data)


@router.get("/tests/{test_id}", response_model=APIResponse[Any])
def get_aptitude_test_by_id_endpoint(
    test_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieves a specific test:
    - If recruiter/admin: Returns complete test details including all questions, correct answers, and explanations.
    - If candidate: Returns test taking view without exposing correct answers or explanations.
    """
    try:
        tid = uuid.UUID(test_id)
    except ValueError:
        raise NotFoundError("Invalid test ID format")

    test = db.query(AptitudeTest).filter(AptitudeTest.id == tid).first()
    if not test:
        raise NotFoundError("Aptitude test not found")

    is_recruiter = current_user.role in RECRUITER_ROLES

    if is_recruiter:
        # Full recruiter review studio details
        serialized = _serialize_test_detail(test, db)
        return APIResponse(success=True, message="Test details loaded", data=serialized)

    # Candidate view: Do NOT leak correct answers or explanations!
    if test.status != "published" or not test.is_active:
        raise PermissionDeniedError("This test is not currently published for candidates.")

    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
    if not questions and test.question_ids_json:
        try:
            q_ids = [uuid.UUID(qid) for qid in json.loads(test.question_ids_json)]
            questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(q_ids)).all()
        except Exception:
            questions = []

    questions_taking = []
    for q in questions:
        raw_options = []
        if q.options:
            raw_options = [opt.option_text for opt in sorted(q.options, key=lambda o: o.order_index)]
        elif q.options_json:
            try:
                raw_options = json.loads(q.options_json)
            except Exception:
                raw_options = []

        questions_taking.append(
            AptitudeQuestionTakingOut(
                id=q.id,
                subtopic=q.subtopic,
                question=q.question,
                options=raw_options,
                difficulty=q.difficulty,
                company_tag=q.company_tag,
            ).model_dump(mode="json")
        )

    candidate_data = {
        "test": {
            "id": str(test.id),
            "title": test.title,
            "description": test.description,
            "duration_minutes": test.duration_minutes,
            "total_questions": len(questions_taking),
            "marks_per_question": test.marks_per_question,
            "total_marks": test.total_marks,
            "passing_percentage": test.passing_percentage,
        },
        "questions": questions_taking,
    }
    return APIResponse(success=True, message="Test loaded for taking", data=candidate_data)


# ==============================================================================
# 3. CANDIDATE TEST TAKING & SERVER-SIDE EVALUATION
# ==============================================================================

@router.post("/tests/{test_id}/start", response_model=APIResponse[CandidateTakingTestResponse])
def start_candidate_test_attempt(
    test_id: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Candidate starts an aptitude test session.
    Creates a CandidateTestAttempt record, begins the timer,
    and returns questions with randomized IDs and options WITHOUT exposing correct answers.
    """
    try:
        tid = uuid.UUID(test_id)
    except ValueError:
        raise NotFoundError("Invalid test ID format")

    test = db.query(AptitudeTest).filter(AptitudeTest.id == tid).first()
    if not test or test.status != "published" or not test.is_active:
        raise NotFoundError("This aptitude test is not available.")

    # Check for existing In Progress attempt
    now = datetime.datetime.now(datetime.timezone.utc)
    existing_attempt = (
        db.query(CandidateTestAttempt)
        .filter(
            CandidateTestAttempt.test_id == test.id,
            CandidateTestAttempt.user_id == current_user.id,
            CandidateTestAttempt.status == "In Progress",
        )
        .first()
    )

    if existing_attempt:
        attempt = existing_attempt
        # Check if expired
        elapsed = (now - attempt.started_at).total_seconds()
        total_allowed = test.duration_minutes * 60
        remaining_seconds = max(0, int(total_allowed - elapsed))
        if remaining_seconds <= 0:
            attempt.status = "Expired"
            db.commit()
            raise BadRequestError("Your test session has expired. Please request a re-attempt.")
    else:
        # Create new attempt
        attempt = CandidateTestAttempt(
            user_id=current_user.id,
            test_id=test.id,
            status="In Progress",
            started_at=now,
            total_marks=test.total_marks,
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        remaining_seconds = test.duration_minutes * 60

    # Fetch questions
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
    letters = ["A", "B", "C", "D"]

    taking_questions: List[CandidateTakingQuestion] = []
    for idx, q in enumerate(questions, start=1):
        taking_options: List[CandidateTakingOption] = []
        if q.options:
            for opt in sorted(q.options, key=lambda o: o.order_index):
                taking_options.append(
                    CandidateTakingOption(
                        id=opt.id,
                        option_letter=opt.option_letter,
                        option_text=opt.option_text,
                    )
                )
        elif q.options_json:
            try:
                raw_opts = json.loads(q.options_json)
                for opt_idx, opt_str in enumerate(raw_opts):
                    taking_options.append(
                        CandidateTakingOption(
                            id=q.id,
                            option_letter=letters[opt_idx],
                            option_text=opt_str,
                        )
                    )
            except Exception:
                pass

        taking_questions.append(
            CandidateTakingQuestion(
                id=q.id,
                question_number=idx,
                topic_name=q.topic_name,
                subtopic=q.subtopic,
                question=q.question,
                difficulty=q.difficulty,
                marks=q.marks,
                options=taking_options,
            )
        )

    response_data = CandidateTakingTestResponse(
        test_id=test.id,
        attempt_id=attempt.id,
        title=test.title,
        duration_minutes=test.duration_minutes,
        total_questions=len(taking_questions),
        total_marks=test.total_marks,
        passing_percentage=test.passing_percentage,
        remaining_seconds=remaining_seconds,
        questions=taking_questions,
    )

    return APIResponse(
        success=True,
        message="Test attempt started. Good luck!",
        data=response_data,
    )


@router.post("/tests/{test_id}/submit", response_model=APIResponse[CandidateTestResultResponse])
def submit_candidate_test_attempt(
    test_id: str,
    payload: CandidateAptitudeSubmitRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Submits candidate answers for automatic server-side evaluation.
    Never trusts client-side scores or correctness.
    Saves CandidateAnswer records, CandidateTestAttempt score, and AptitudeTestResult.
    Returns complete question-by-question review with explanations.
    """
    try:
        tid = uuid.UUID(test_id)
    except ValueError:
        raise NotFoundError("Invalid test ID format")

    test = db.query(AptitudeTest).filter(AptitudeTest.id == tid).first()
    if not test:
        raise NotFoundError("Aptitude test not found")

    attempt = (
        db.query(CandidateTestAttempt)
        .filter(CandidateTestAttempt.id == payload.attempt_id, CandidateTestAttempt.user_id == current_user.id)
        .first()
    )
    if not attempt:
        raise NotFoundError("Test attempt not found")

    if attempt.status == "Submitted" and attempt.result:
        # Already evaluated; return existing result to prevent double submission
        res = attempt.result
        return APIResponse(
            success=True,
            message="Test has already been submitted.",
            data=_build_test_result_response(attempt, res, test, db),
        )

    # Load all questions for this test
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
    q_map = {q.id: q for q in questions}

    # Map candidate answers by question_id
    candidate_answer_map = {item.question_id: item for item in payload.answers}

    total_marks_possible = sum(q.marks for q in questions) or test.total_marks or 1.0
    total_score = 0.0
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0

    topic_stats: Dict[str, Dict[str, Any]] = {}
    letters = ["A", "B", "C", "D"]

    # Delete any previous answers for this attempt if retrying submission
    db.query(CandidateAnswer).filter(CandidateAnswer.attempt_id == attempt.id).delete()

    for q in questions:
        topic = q.topic_name or q.subtopic or "General"
        if topic not in topic_stats:
            topic_stats[topic] = {"total": 0, "correct": 0, "marks": 0.0}
        topic_stats[topic]["total"] += 1

        ans_item = candidate_answer_map.get(q.id)
        selected_option_id = ans_item.selected_option_id if ans_item else None
        selected_index = ans_item.selected_option_index if ans_item else None
        selected_letter = ans_item.selected_option_letter if ans_item else None

        # Resolve selected letter/index if only one was provided
        if selected_option_id and q.options:
            matched_opt = next((o for o in q.options if o.id == selected_option_id), None)
            if matched_opt:
                selected_letter = matched_opt.option_letter
                selected_index = matched_opt.order_index

        if selected_index is not None and (selected_letter is None) and 0 <= selected_index < 4:
            selected_letter = letters[selected_index]

        is_correct = False
        marks_awarded = 0.0

        if selected_index is None and selected_letter is None and selected_option_id is None:
            unanswered_count += 1
        else:
            # Check correctness strictly against database question
            if selected_index is not None and selected_index == q.correct_option_index:
                is_correct = True
            elif selected_letter and selected_letter == letters[q.correct_option_index]:
                is_correct = True
            elif selected_option_id and q.options:
                correct_opt = next((o for o in q.options if o.is_correct), None)
                if correct_opt and correct_opt.id == selected_option_id:
                    is_correct = True

            if is_correct:
                correct_count += 1
                marks_awarded = q.marks
                total_score += marks_awarded
                topic_stats[topic]["correct"] += 1
                topic_stats[topic]["marks"] += marks_awarded
            else:
                wrong_count += 1

        # Record candidate answer
        cand_ans = CandidateAnswer(
            attempt_id=attempt.id,
            question_id=q.id,
            selected_option_id=selected_option_id,
            selected_option_index=selected_index,
            selected_option_letter=selected_letter,
            is_correct=is_correct,
            marks_awarded=marks_awarded,
        )
        db.add(cand_ans)

    # Compute final percentage and passing status
    pct = round((total_score / total_marks_possible) * 100.0, 1) if total_marks_possible > 0 else 0.0
    passed = pct >= test.passing_percentage
    percentile = min(99.5, max(15.0, round(pct * 0.94 + 5.0, 1)))

    if pct >= 80:
        feedback = "Exceptional analytical and aptitude performance! You demonstrated mastery of the topics."
    elif pct >= 60:
        feedback = "Good performance! You cleared the passing threshold. Review the explanations to strengthen weaker topics."
    else:
        feedback = "Practice needed. Review the step-by-step mathematical reasoning and solutions below."

    # Update attempt record
    now = datetime.datetime.now(datetime.timezone.utc)
    attempt.status = "Submitted"
    attempt.submitted_at = now
    attempt.score = total_score
    attempt.total_marks = total_marks_possible
    attempt.percentage = pct
    attempt.passed = passed
    attempt.time_taken_seconds = payload.time_taken_seconds

    # Create AptitudeTestResult record
    result = AptitudeTestResult(
        attempt_id=attempt.id,
        test_id=test.id,
        candidate_id=current_user.id,
        total_questions=len(questions),
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        score=total_score,
        total_marks=total_marks_possible,
        percentage=pct,
        passed=passed,
        percentile_estimate=percentile,
        topic_breakdown_json=json.dumps(topic_stats),
        feedback_message=feedback,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    db.refresh(attempt)

    logger.info(
        f"Candidate {current_user.email} submitted test '{test.title}' (Attempt: {attempt.id}) - Score: {total_score}/{total_marks_possible} ({pct}%)"
    )

    return APIResponse(
        success=True,
        message="Test submitted and evaluated successfully!",
        data=_build_test_result_response(attempt, result, test, db),
    )


def _build_test_result_response(
    attempt: CandidateTestAttempt,
    result: AptitudeTestResult,
    test: AptitudeTest,
    db: Session,
) -> CandidateTestResultResponse:
    """Builds the comprehensive results response with full question-by-question review."""
    letters = ["A", "B", "C", "D"]
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
    answers = db.query(CandidateAnswer).filter(CandidateAnswer.attempt_id == attempt.id).all()
    ans_by_qid = {a.question_id: a for a in answers}

    review_items: List[CandidateAnswerReviewItem] = []
    for q in questions:
        ans = ans_by_qid.get(q.id)
        options_out: List[AptitudeOptionOut] = []
        if q.options:
            for opt in sorted(q.options, key=lambda o: o.order_index):
                options_out.append(
                    AptitudeOptionOut(
                        id=opt.id,
                        option_letter=opt.option_letter,
                        option_text=opt.option_text,
                        is_correct=opt.is_correct,
                        order_index=opt.order_index,
                    )
                )
        elif q.options_json:
            try:
                for idx, text in enumerate(json.loads(q.options_json)):
                    options_out.append(
                        AptitudeOptionOut(
                            id=None,
                            option_letter=letters[idx],
                            option_text=text,
                            is_correct=(idx == q.correct_option_index),
                            order_index=idx,
                        )
                    )
            except Exception:
                pass

        review_items.append(
            CandidateAnswerReviewItem(
                question_id=q.id,
                question_text=q.question,
                topic_name=q.topic_name,
                difficulty=q.difficulty,
                marks=q.marks,
                marks_awarded=ans.marks_awarded if ans else 0.0,
                options=options_out,
                correct_option_letter=letters[q.correct_option_index],
                user_selected_letter=ans.selected_option_letter if ans else None,
                is_correct=ans.is_correct if ans else False,
                explanation=q.explanation,
            )
        )

    topic_breakdown = {}
    if result.topic_breakdown_json:
        try:
            topic_breakdown = json.loads(result.topic_breakdown_json)
        except Exception:
            pass

    return CandidateTestResultResponse(
        result_id=result.id,
        attempt_id=attempt.id,
        test_id=test.id,
        test_title=test.title,
        total_questions=result.total_questions,
        correct_count=result.correct_count,
        wrong_count=result.wrong_count,
        unanswered_count=result.unanswered_count,
        score=result.score,
        total_marks=result.total_marks,
        percentage=result.percentage,
        passed=result.passed,
        time_taken_seconds=attempt.time_taken_seconds,
        percentile_estimate=result.percentile_estimate,
        feedback_message=result.feedback_message or "Aptitude assessment evaluation completed.",
        topic_breakdown=topic_breakdown,
        review_items=review_items,
    )


@router.get("/tests/{test_id}/results", response_model=APIResponse[List[dict]])
def get_test_candidate_results_endpoint(
    test_id: str,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Recruiter/Admin endpoint to view all candidate attempts and scores for a specific test.
    """
    try:
        tid = uuid.UUID(test_id)
    except ValueError:
        raise NotFoundError("Invalid test ID format")

    test = db.query(AptitudeTest).filter(AptitudeTest.id == tid).first()
    if not test:
        raise NotFoundError("Aptitude test not found")

    attempts = (
        db.query(CandidateTestAttempt, User)
        .join(User, CandidateTestAttempt.user_id == User.id)
        .filter(CandidateTestAttempt.test_id == test.id)
        .order_by(CandidateTestAttempt.created_at.desc())
        .all()
    )

    data = []
    for att, usr in attempts:
        data.append(
            {
                "attempt_id": str(att.id),
                "candidate_id": str(usr.id),
                "candidate_name": usr.name or usr.email,
                "candidate_email": usr.email,
                "status": att.status,
                "score": att.score,
                "total_marks": att.total_marks,
                "percentage": att.percentage,
                "passed": att.passed,
                "time_taken_seconds": att.time_taken_seconds,
                "started_at": att.started_at.isoformat() if att.started_at else None,
                "submitted_at": att.submitted_at.isoformat() if att.submitted_at else None,
            }
        )

    return APIResponse(success=True, message=f"Candidate results for test '{test.title}'", data=data)


# ==============================================================================
# 4. EXISTING PRACTICE / DAILY SPRINT ENDPOINTS (PRESERVED)
# ==============================================================================

@router.get("/topics", response_model=APIResponse[List[AptitudeTopicOut]])
def get_aptitude_topics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lists all aptitude topics (Quantitative, Logical, Verbal, Core CS) with question counts."""
    topics = db.query(AptitudeTopic).order_by(AptitudeTopic.order_index).all()

    data = []
    for t in topics:
        q_count = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic_id == t.id).count()
        data.append(
            AptitudeTopicOut(
                id=t.id,
                name=t.name,
                slug=t.slug,
                description=t.description,
                icon=t.icon,
                question_count=q_count,
            )
        )
    return APIResponse(success=True, message="Aptitude topics", data=data)


@router.post("/topics", response_model=APIResponse[AptitudeTopicOut])
def create_aptitude_topic_endpoint(
    payload: AptitudeTopicCreate,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """Admin/Recruiter creates a new aptitude topic/domain."""
    import re
    slug = payload.slug or re.sub(r"[^a-z0-9]+", "-", payload.name.lower()).strip("-")
    existing = db.query(AptitudeTopic).filter((AptitudeTopic.slug == slug) | (AptitudeTopic.name.ilike(payload.name))).first()
    if existing:
        raise BadRequestError(f"Topic with name '{payload.name}' or slug '{slug}' already exists.")

    topic = AptitudeTopic(
        name=payload.name.strip(),
        slug=slug,
        description=payload.description.strip() if payload.description else None,
        icon=payload.icon or "📊",
        order_index=payload.order_index,
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)

    return APIResponse(
        success=True,
        message="Aptitude topic created successfully",
        data=AptitudeTopicOut(
            id=topic.id,
            name=topic.name,
            slug=topic.slug,
            description=topic.description,
            icon=topic.icon,
            question_count=0,
        ),
    )


@router.get("/topics/{topic_id}", response_model=APIResponse[Dict[str, Any]])
def get_aptitude_topic_detail_endpoint(
    topic_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves an aptitude topic and its subtopics and difficulty distribution."""
    try:
        tid = uuid.UUID(topic_id)
    except ValueError:
        raise BadRequestError("Invalid topic ID format")

    topic = db.query(AptitudeTopic).filter(AptitudeTopic.id == tid).first()
    if not topic:
        raise NotFoundError("Aptitude topic not found")

    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic_id == topic.id).all()
    subtopics = sorted(list(set(q.subtopic for q in questions if q.subtopic)))
    difficulties = {"easy": 0, "medium": 0, "hard": 0}
    for q in questions:
        diff = (q.difficulty or "medium").lower()
        if diff in difficulties:
            difficulties[diff] += 1

    return APIResponse(
        success=True,
        message="Aptitude topic detail",
        data={
            "id": str(topic.id),
            "name": topic.name,
            "slug": topic.slug,
            "description": topic.description,
            "icon": topic.icon,
            "order_index": topic.order_index,
            "total_questions": len(questions),
            "subtopics": subtopics,
            "difficulties": difficulties,
        },
    )


@router.get("/topics/{topic_id}/practice", response_model=APIResponse[dict])
def get_topic_practice_test_endpoint(
    topic_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns a practice exam containing all questions for the specified topic.
    Accepts topic UUID or topic slug/name.
    """
    topic = None
    try:
        tid = uuid.UUID(topic_id)
        topic = db.query(AptitudeTopic).filter(AptitudeTopic.id == tid).first()
    except (ValueError, TypeError):
        pass

    if not topic:
        topic = db.query(AptitudeTopic).filter(
            (AptitudeTopic.slug == topic_id) | (AptitudeTopic.name.ilike(topic_id))
        ).first()

    if not topic:
        raise NotFoundError("Aptitude topic not found")

    questions = db.query(AptitudeQuestion).filter(
        (AptitudeQuestion.topic_id == topic.id) | (AptitudeQuestion.topic_name == topic.name)
    ).order_by(AptitudeQuestion.created_at.asc()).all()

    if not questions:
        raise NotFoundError(f"No practice questions available for topic '{topic.name}'.")

    questions_out = []
    for q in questions:
        options = json.loads(q.options_json) if q.options_json else []
        questions_out.append(
            AptitudeQuestionTakingOut(
                id=q.id,
                subtopic=q.subtopic,
                question=q.question,
                options=options,
                difficulty=q.difficulty,
                company_tag=q.company_tag,
            ).model_dump(mode="json")
        )

    response_data = {
        "test": {
            "id": f"topic-{topic.id}",
            "topic_id": str(topic.id),
            "title": f"{topic.name} Practice Exam",
            "duration_minutes": max(1, math.ceil(len(questions_out) * 30 / 60)),
            "total_questions": len(questions_out),
            "passing_percentage": 60.0,
        },
        "questions": questions_out,
    }
    return APIResponse(
        success=True,
        message=f"{topic.name} practice test loaded with {len(questions_out)} questions.",
        data=response_data,
    )


@router.put("/topics/{topic_id}", response_model=APIResponse[AptitudeTopicOut])
def update_aptitude_topic_endpoint(
    topic_id: str,
    payload: AptitudeTopicUpdate,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """Admin/Recruiter updates an aptitude topic."""
    try:
        tid = uuid.UUID(topic_id)
    except ValueError:
        raise BadRequestError("Invalid topic ID format")

    topic = db.query(AptitudeTopic).filter(AptitudeTopic.id == tid).first()
    if not topic:
        raise NotFoundError("Aptitude topic not found")

    old_name = topic.name
    if payload.name is not None and payload.name.strip():
        topic.name = payload.name.strip()
    if payload.slug is not None and payload.slug.strip():
        topic.slug = payload.slug.strip()
    if payload.description is not None:
        topic.description = payload.description.strip()
    if payload.icon is not None and payload.icon.strip():
        topic.icon = payload.icon.strip()
    if payload.order_index is not None:
        topic.order_index = payload.order_index

    # Update questions topic_name if name changed
    if payload.name and payload.name.strip() != old_name:
        db.query(AptitudeQuestion).filter(AptitudeQuestion.topic_id == topic.id).update(
            {"topic_name": topic.name}, synchronize_session=False
        )

    db.commit()
    db.refresh(topic)

    # Re-index questions in Qdrant if topic name changed
    if payload.name and payload.name.strip() != old_name:
        try:
            questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic_id == topic.id).all()
            items = []
            for q in questions:
                items.append({
                    "id": str(q.id),
                    "text": f"Topic: {topic.name}\nSubtopic: {q.subtopic}\nQuestion: {q.question}",
                    "metadata": {
                        "question_id": str(q.id),
                        "topic_name": topic.name,
                        "subtopic": q.subtopic,
                        "difficulty": q.difficulty,
                        "company_tag": q.company_tag,
                    },
                })
            if items:
                upsert_batch(COLLECTION_APTITUDE, items)
        except Exception as exc:
            logger.warning("Qdrant: Failed to re-index topic questions: %s", exc)

    q_count = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic_id == topic.id).count()
    return APIResponse(
        success=True,
        message="Aptitude topic updated successfully",
        data=AptitudeTopicOut(
            id=topic.id,
            name=topic.name,
            slug=topic.slug,
            description=topic.description,
            icon=topic.icon,
            question_count=q_count,
        ),
    )


@router.delete("/topics/{topic_id}", response_model=APIResponse[dict])
def delete_aptitude_topic_endpoint(
    topic_id: str,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.superadmin)),
    db: Session = Depends(get_db),
):
    """Admin deletes an aptitude topic."""
    try:
        tid = uuid.UUID(topic_id)
    except ValueError:
        raise BadRequestError("Invalid topic ID format")

    topic = db.query(AptitudeTopic).filter(AptitudeTopic.id == tid).first()
    if not topic:
        raise NotFoundError("Aptitude topic not found")

    # Clean up associated questions from Qdrant vector database
    try:
        questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic_id == topic.id).all()
        for q in questions:
            delete_document(COLLECTION_APTITUDE, q.id)
    except Exception as exc:
        logger.warning("Qdrant: Failed to delete topic questions: %s", exc)

    db.delete(topic)
    db.commit()
    return APIResponse(success=True, message="Aptitude topic deleted successfully", data={"topic_id": str(tid)})


@router.post("/questions", response_model=APIResponse[AptitudeQuestionDetail])
def create_standalone_aptitude_question_endpoint(
    payload: AptitudeQuestionCreateStandalone,
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Creates a new aptitude question under a topic, checks for semantic duplicates
    against Qdrant, and indexes the question directly into the vector database.
    """
    # 1. Semantic duplicate check via Qdrant
    if payload.check_duplicates:
        dup = check_aptitude_question_duplicate(
            question_text=payload.question,
            similarity_threshold=payload.duplicate_threshold,
            topic=payload.topic_name,
        )
        if dup:
            raise BadRequestError(
                f"Semantically duplicate question detected (Similarity: {dup.get('similarity_pct', 0)}%): '{dup.get('payload', {}).get('text_snippet', '')}'"
            )

    # 2. Resolve topic
    topic = None
    if payload.topic_id:
        topic = db.query(AptitudeTopic).filter(AptitudeTopic.id == payload.topic_id).first()
    elif payload.topic_name:
        topic = db.query(AptitudeTopic).filter(AptitudeTopic.name.ilike(payload.topic_name)).first()

    topic_name = payload.topic_name or (topic.name if topic else "General Aptitude")

    # 3. Create question
    q = AptitudeQuestion(
        topic_id=topic.id if topic else None,
        subtopic=payload.subtopic.strip(),
        topic_name=topic_name,
        question=payload.question.strip(),
        options_json=json.dumps(payload.options),
        correct_option_index=payload.correct_option_index,
        explanation=payload.explanation.strip() if payload.explanation else None,
        difficulty=payload.difficulty.lower(),
        marks=payload.marks,
        company_tag=payload.company_tag or "General",
        status=payload.status,
    )
    db.add(q)
    db.flush()

    # 4. Create 4 relational options
    letters = ["A", "B", "C", "D"]
    for idx, opt_text in enumerate(payload.options):
        opt = AptitudeOption(
            question_id=q.id,
            option_letter=letters[idx],
            option_text=opt_text.strip(),
            is_correct=(idx == payload.correct_option_index),
            order_index=idx,
        )
        db.add(opt)

    db.commit()
    db.refresh(q)

    # 5. Real-time upsert into Qdrant vector database
    try:
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
        logger.warning(f"Failed to upsert created question to vector DB: {exc}")

    opts_out = [
        AptitudeOptionOut(
            id=opt.id,
            option_letter=opt.option_letter,
            option_text=opt.option_text,
            is_correct=opt.is_correct,
            order_index=opt.order_index,
        )
        for opt in sorted(q.options, key=lambda o: o.order_index)
    ]

    return APIResponse(
        success=True,
        message="Aptitude question created and indexed into vector database successfully",
        data=AptitudeQuestionDetail(
            id=q.id,
            test_id=q.test_id,
            topic_name=q.topic_name,
            subtopic=q.subtopic,
            question=q.question,
            options=opts_out,
            correct_option_index=q.correct_option_index,
            explanation=q.explanation,
            difficulty=q.difficulty,
            marks=q.marks,
            status=q.status,
        ),
    )


@router.post("/questions/search", response_model=APIResponse[List[Dict[str, Any]]])
def vector_search_aptitude_questions(
    payload: AptitudeVectorSearchRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Performs dense semantic vector similarity retrieval on the Aptitude Questions collection in Qdrant.
    """
    filters = {}
    if payload.topic_name:
        filters["topic_name"] = payload.topic_name
    if payload.difficulty:
        filters["difficulty"] = payload.difficulty
    if payload.company_tag:
        filters["company_tag"] = payload.company_tag

    results = vector_search(
        collection_name=COLLECTION_APTITUDE,
        query_text=payload.query,
        limit=payload.limit,
        score_threshold=payload.score_threshold,
        filter_dict=filters or None,
    )
    return APIResponse(
        success=True,
        message=f"Found {len(results)} semantically similar aptitude questions",
        data=results,
    )


@router.post("/sync-vectors", response_model=APIResponse[Dict[str, Any]])
def sync_aptitude_vectors(
    current_user: User = Depends(require_role(*RECRUITER_ROLES)),
    db: Session = Depends(get_db),
):
    """
    Synchronizes all Aptitude Questions from the relational database into Qdrant.
    """
    apt_questions = db.query(AptitudeQuestion).all()
    apt_items = []
    for aq in apt_questions:
        topic_str = aq.topic_name or (aq.topic.name if aq.topic else "")
        full_text = f"Topic: {topic_str}\nSubtopic: {aq.subtopic}\nQuestion: {aq.question}"
        apt_items.append({
            "id": str(aq.id),
            "text": full_text,
            "metadata": {
                "question_id": str(aq.id),
                "topic_name": topic_str,
                "subtopic": aq.subtopic,
                "difficulty": aq.difficulty,
                "company_tag": aq.company_tag,
            },
        })

    indexed_count = upsert_batch(COLLECTION_APTITUDE, apt_items) if apt_items else 0
    return APIResponse(
        success=True,
        message=f"Aptitude questions synchronized to vector database. Indexed {indexed_count} questions.",
        data={
            "collection": COLLECTION_APTITUDE,
            "total_questions_in_db": len(apt_questions),
            "vectors_indexed": indexed_count,
        },
    )


@router.get("/daily-sprint", response_model=APIResponse[dict])
def get_daily_sprint(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Returns today's 5-question high-speed daily practice test."""
    questions = db.query(AptitudeQuestion).order_by(AptitudeQuestion.created_at.desc()).limit(5).all()
    questions_out = []
    for q in questions:
        options = json.loads(q.options_json) if q.options_json else []
        questions_out.append(
            AptitudeQuestionTakingOut(
                id=q.id,
                subtopic=q.subtopic,
                question=q.question,
                options=options,
                difficulty=q.difficulty,
                company_tag=q.company_tag,
            ).model_dump(mode="json")
        )

    response_data = {
        "test": {
            "id": "daily-sprint",
            "title": "Daily Analytical Placement Sprint",
            "duration_minutes": max(1, math.ceil(len(questions_out) * 30 / 60)),
            "total_questions": len(questions_out),
            "passing_percentage": 60.0,
        },
        "questions": questions_out,
    }
    return APIResponse(success=True, message="Daily sprint loaded", data=response_data)


@router.post("/submit", response_model=APIResponse[AptitudeAttemptResult])
def submit_aptitude_test(
    payload: AptitudeSubmissionRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Evaluates candidate's submitted answers against correct answers for daily sprint/practice test.
    """
    question_ids = []
    if payload.question_ids:
        for qid_str in payload.question_ids:
            try:
                question_ids.append(uuid.UUID(str(qid_str)))
            except (ValueError, TypeError):
                continue

    for qid_str in payload.answers.keys():
        try:
            uid = uuid.UUID(str(qid_str))
            if uid not in question_ids:
                question_ids.append(uid)
        except (ValueError, TypeError):
            continue

    test = None
    if payload.test_id and payload.test_id != "daily-sprint":
        try:
            tid = uuid.UUID(str(payload.test_id))
            test = db.query(AptitudeTest).filter(AptitudeTest.id == tid).first()
        except (ValueError, TypeError):
            test = None

        if test and test.question_ids_json:
            try:
                for qid in json.loads(test.question_ids_json):
                    uid = uuid.UUID(str(qid))
                    if uid not in question_ids:
                        question_ids.append(uid)
            except Exception:
                pass

    if not question_ids and payload.test_id == "daily-sprint":
        fallback_qs = db.query(AptitudeQuestion).order_by(AptitudeQuestion.created_at.desc()).limit(10).all()
        question_ids = [q.id for q in fallback_qs]

    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all() if question_ids else []
    if not questions:
        questions = db.query(AptitudeQuestion).limit(5).all()

    total_count = len(questions)
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    reviews = []

    for q in questions:
        options = json.loads(q.options_json) if q.options_json else []
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
            AptitudeQuestionReviewOut(
                id=q.id,
                subtopic=q.subtopic,
                question=q.question,
                options=options,
                correct_option_index=q.correct_option_index,
                user_selected_index=int(user_choice) if user_choice is not None else None,
                is_correct=is_correct,
                explanation=q.explanation,
            )
        )

    score_pct = round((correct_count / total_count) * 100.0, 1) if total_count > 0 else 0.0
    pass_pct = test.passing_percentage if test else 60.0
    is_passed = score_pct >= pass_pct

    percentile = min(99.4, max(15.0, round(score_pct * 0.95 + 4.5, 1)))

    if score_pct >= 85:
        feedback = "Outstanding performance! You have demonstrated high accuracy and strong aptitude proficiency."
    elif score_pct >= 65:
        feedback = "Good work! You cleared the cutoff. Review missed questions to further boost your speed."
    else:
        feedback = "Needs practice. Go through the question explanations below and review our quantitative & logical study guides."

    attempt = AptitudeAttempt(
        user_id=current_user.id,
        test_id=test.id if test else None,
        topic_name=payload.topic_name or (test.title if test else "Practice Test"),
        total_questions=total_count,
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        score_percentage=score_pct,
        time_taken_seconds=payload.time_taken_seconds,
        is_passed=is_passed,
        answers_summary_json=json.dumps(payload.answers),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    result = AptitudeAttemptResult(
        attempt_id=attempt.id,
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
    return APIResponse(success=True, message="Test submitted and evaluated successfully", data=result)


@router.get("/history", response_model=APIResponse[list[dict]])
def get_user_attempt_history(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Returns candidate's past aptitude exam attempts and performance trend."""
    attempts = (
        db.query(AptitudeAttempt)
        .filter(AptitudeAttempt.user_id == current_user.id)
        .order_by(AptitudeAttempt.created_at.desc())
        .limit(20)
        .all()
    )

    data = [
        {
            "id": str(a.id),
            "topic_name": a.topic_name or "Aptitude Assessment",
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
    return APIResponse(success=True, message="Aptitude test history", data=data)
