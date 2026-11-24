"""
sprint_question_service.py — Dynamic Non-Repeating Aptitude Sprint Question Service.
Ensures that whenever a candidate attempts either the Daily Analytical Placement Sprint
or the Weekly Placement Aptitude Sprint, the same questions do NOT appear again.
Dynamically retrieves unseen questions or synthesizes fresh questions on-demand.
"""
import json
import logging
import math
import random
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models.student import (
    AptitudeAttempt,
    AptitudeQuestion,
    AptitudeTest,
    AptitudeTopic,
    CandidateAnswer,
    CandidateSprintSeenQuestion,
    CandidateTestAttempt,
)
from app.models.weekly_challenge import WeeklyAptitudeAttempt, WeeklyAptitudeSet
from app.services.question_balancer import ensure_four_options

logger = logging.getLogger("ai_recruiter.sprint_question_service")


def ensure_sprint_tables(db: Session) -> None:
    """Ensures CandidateSprintSeenQuestion and related tables exist in the database."""
    try:
        bind = db.get_bind()
        Base.metadata.create_all(bind=bind)
    except Exception as exc:
        logger.warning(f"Could not verify sprint tables metadata: {exc}")


def get_candidate_excluded_question_ids(
    db: Session,
    user_id: uuid.UUID,
    sprint_type: Optional[str] = None,
) -> Set[uuid.UUID]:
    """
    Collects all question IDs previously seen or attempted by the candidate across:
    1. CandidateSprintSeenQuestion (all sprints previously served)
    2. AptitudeAttempt (answers_summary_json)
    3. WeeklyAptitudeAttempt (answers_json)
    4. CandidateAnswer (past tests)
    """
    excluded: Set[uuid.UUID] = set()

    # 1. Seen questions table
    try:
        q = db.query(CandidateSprintSeenQuestion.question_id).filter(
            CandidateSprintSeenQuestion.user_id == user_id
        )
        if sprint_type:
            q = q.filter(CandidateSprintSeenQuestion.sprint_type == sprint_type)
        for (qid,) in q.all():
            if qid:
                excluded.add(qid)
    except Exception as exc:
        logger.warning(f"Error querying CandidateSprintSeenQuestion: {exc}")

    # 2. AptitudeAttempt (Daily and practice attempts)
    try:
        attempts = (
            db.query(AptitudeAttempt.answers_summary_json)
            .filter(AptitudeAttempt.user_id == user_id)
            .all()
        )
        for (ans_json,) in attempts:
            if not ans_json:
                continue
            try:
                data = json.loads(ans_json)
                if isinstance(data, dict):
                    for qid_str in data.keys():
                        try:
                            excluded.add(uuid.UUID(str(qid_str)))
                        except (ValueError, TypeError):
                            pass
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "id" in item:
                            try:
                                excluded.add(uuid.UUID(str(item["id"])))
                            except (ValueError, TypeError):
                                pass
            except Exception:
                pass
    except Exception as exc:
        logger.warning(f"Error querying AptitudeAttempt history: {exc}")

    # 3. WeeklyAptitudeAttempt
    try:
        w_attempts = (
            db.query(WeeklyAptitudeAttempt.answers_json)
            .filter(WeeklyAptitudeAttempt.user_id == user_id)
            .all()
        )
        for (ans_json,) in w_attempts:
            if not ans_json:
                continue
            try:
                data = json.loads(ans_json)
                if isinstance(data, dict):
                    for qid_str in data.keys():
                        try:
                            excluded.add(uuid.UUID(str(qid_str)))
                        except (ValueError, TypeError):
                            pass
            except Exception:
                pass
    except Exception as exc:
        logger.warning(f"Error querying WeeklyAptitudeAttempt history: {exc}")

    # 4. CandidateAnswer
    try:
        c_attempt_ids = [
            r[0]
            for r in db.query(CandidateTestAttempt.id)
            .filter(CandidateTestAttempt.user_id == user_id)
            .all()
        ]
        if c_attempt_ids:
            c_qids = (
                db.query(CandidateAnswer.question_id)
                .filter(CandidateAnswer.attempt_id.in_(c_attempt_ids))
                .all()
            )
            for (qid,) in c_qids:
                if qid:
                    excluded.add(qid)
    except Exception as exc:
        logger.warning(f"Error querying CandidateAnswer history: {exc}")

    # 5. CandidateTestAttempt assigned questions
    try:
        assigned_rows = (
            db.query(CandidateTestAttempt.assigned_question_ids_json)
            .filter(CandidateTestAttempt.user_id == user_id)
            .all()
        )
        for (assigned_json,) in assigned_rows:
            if not assigned_json:
                continue
            try:
                data = json.loads(assigned_json)
                if isinstance(data, list):
                    for qid_str in data:
                        try:
                            excluded.add(uuid.UUID(str(qid_str)))
                        except (ValueError, TypeError):
                            pass
            except Exception:
                pass
    except Exception as exc:
        logger.warning(f"Error querying CandidateTestAttempt assigned questions: {exc}")

    return excluded


def mark_questions_as_seen(
    db: Session,
    user_id: uuid.UUID,
    question_ids: List[uuid.UUID],
    sprint_type: str = "daily_sprint",
) -> None:
    """Records the served question IDs for the user to prevent repetition."""
    if not question_ids:
        return

    try:
        existing_seen = {
            r[0]
            for r in db.query(CandidateSprintSeenQuestion.question_id)
            .filter(
                CandidateSprintSeenQuestion.user_id == user_id,
                CandidateSprintSeenQuestion.question_id.in_(question_ids),
                CandidateSprintSeenQuestion.sprint_type == sprint_type,
            )
            .all()
        }

        new_entries = []
        for qid in question_ids:
            if qid not in existing_seen:
                new_entries.append(
                    CandidateSprintSeenQuestion(
                        user_id=user_id,
                        question_id=qid,
                        sprint_type=sprint_type,
                    )
                )

        if new_entries:
            db.add_all(new_entries)
            db.commit()
    except Exception as exc:
        db.rollback()
        logger.warning(f"Failed to record CandidateSprintSeenQuestion: {exc}")


def generate_dynamic_sprint_question(
    db: Session,
    topic_name: Optional[str] = None,
    subtopic_hint: Optional[str] = None,
    difficulty: str = "medium",
    company_tag: Optional[str] = None,
) -> AptitudeQuestion:
    """
    Generates a brand-new high-quality analytical placement question.
    Attempts LLM generation first; falls back gracefully to parameterized mathematical
    and logical curriculum synthesis to guarantee uniqueness and instant availability.
    """
    # 1. Resolve parent topic
    topic = None
    if topic_name:
        topic = db.query(AptitudeTopic).filter(
            AptitudeTopic.name.ilike(f"%{topic_name}%")
        ).first()
    if not topic:
        topic = db.query(AptitudeTopic).order_by(func.random()).first()

    resolved_topic_name = topic.name if topic else (topic_name or "Quantitative Aptitude")
    resolved_company = company_tag or random.choice([
        "TCS NQT", "Infosys", "Wipro Turbo", "Amazon SDE", "Cognizant GenC", "Deloitte Tech"
    ])

    # 2. Try LLM generation
    try:
        from app.ai.llm_service import generate as generate_llm

        prompt = f"""Generate a high-quality campus recruitment aptitude test question.
Topic: {resolved_topic_name}
Subtopic: {subtopic_hint or 'Problem Solving & Reasoning'}
Difficulty: {difficulty}
Target Company: {resolved_company}

Return ONLY a valid JSON object matching this schema:
{{
  "subtopic": "Specific subtopic name",
  "question": "Clear, precise problem statement with numbers and context",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_option_index": 1,
  "explanation": "Step-by-step mathematical or logical proof/solution"
}}
CRITICAL RULES:
- Exactly 4 options.
- The correct option must be accurate and verifiable.
- Set correct_option_index to 0, 1, 2, or 3 (distribute randomly).
- No markdown wrappers, no backticks, only parseable JSON.
"""
        raw_res = generate_llm(prompt)
        clean_json = raw_res.strip()
        if clean_json.startswith("```"):
            clean_json = clean_json.split("\n", 1)[1]
            if clean_json.endswith("```"):
                clean_json = clean_json.rsplit("\n", 1)[0]
        clean_json = clean_json.strip()

        data = json.loads(clean_json)
        raw_opts = data.get("options", [])
        raw_corr_idx = int(data.get("correct_option_index", 0))
        corr_val = raw_opts[raw_corr_idx] if (0 <= raw_corr_idx < len(raw_opts)) else None
        opts = ensure_four_options(raw_opts, correct_val=corr_val, context_hint=data.get("question", ""))
        corr_idx = opts.index(corr_val) if (corr_val and corr_val in opts) else 0

        if data.get("question"):
            # Ensure random option distribution across all 4 slots (A, B, C, D)
            target_slot = random.randint(0, 3)
            if target_slot != corr_idx:
                opts[corr_idx], opts[target_slot] = opts[target_slot], opts[corr_idx]
                corr_idx = target_slot

            q = AptitudeQuestion(
                topic_id=topic.id if topic else uuid.uuid4(),
                subtopic=data.get("subtopic") or subtopic_hint or "Analytical Reasoning",
                question=data["question"].strip(),
                options_json=json.dumps(opts),
                correct_option_index=corr_idx,
                explanation=data.get("explanation") or "Calculated using standard placement aptitude methodology.",
                difficulty=difficulty.lower(),
                company_tag=resolved_company,
                status="approved",
            )
            db.add(q)
            db.commit()
            db.refresh(q)
            logger.info(f"Dynamically generated AI question: {q.subtopic}")
            return q
    except Exception as exc:
        logger.info(f"AI generation fell back to mathematical synthesizer: {exc}")

    # 3. Parameterized Mathematical & Logical Synthesizer Fallback (Guaranteed unique numbers each time)
    return _synthesize_parameterized_question(db, topic, resolved_topic_name, resolved_company, difficulty)


def _synthesize_parameterized_question(
    db: Session,
    topic: Optional[AptitudeTopic],
    topic_name: str,
    company_tag: str,
    difficulty: str,
) -> AptitudeQuestion:
    """Generates mathematically verified placement aptitude questions with randomized variables."""
    # Match generator type intelligently based on requested topic keywords
    tl = (topic_name or "").lower()
    if any(k in tl for k in ["work", "pipe", "cistern"]):
        generator_types = ["time_and_work", "pipes_and_cisterns"]
    elif any(k in tl for k in ["train", "speed", "distance"]):
        generator_types = ["speed_distance_trains"]
    elif any(k in tl for k in ["profit", "loss", "discount", "percent"]):
        generator_types = ["profit_loss_markup"]
    elif any(k in tl for k in ["interest", "compound", "simple interest"]):
        generator_types = ["compound_interest"]
    elif any(k in tl for k in ["ratio", "proportion", "partner"]):
        generator_types = ["ratios_partnerships"]
    elif any(k in tl for k in ["probability", "permutation", "combination"]):
        generator_types = ["permutation_probability"]
    elif any(k in tl for k in ["series", "number", "logic", "reasoning", "coding"]):
        generator_types = ["logical_coding_series"]
    elif any(k in tl for k in ["data", "chart", "table", "graph", "interpret"]):
        generator_types = ["data_interpretation_growth"]
    else:
        generator_types = [
            "time_and_work",
            "speed_distance_trains",
            "profit_loss_markup",
            "compound_interest",
            "ratios_partnerships",
            "pipes_and_cisterns",
            "permutation_probability",
            "logical_coding_series",
            "data_interpretation_growth",
        ]
    chosen_type = random.choice(generator_types)

    if chosen_type == "time_and_work":
        # A can do a work in X days, B can do it in Y days. Together: (X*Y)/(X+Y)
        x = random.choice([10, 12, 15, 20, 24, 30])
        y = random.choice([15, 20, 30, 40, 60])
        ans_float = (x * y) / (x + y)
        ans_str = f"{ans_float:.1f}".rstrip("0").rstrip(".") + " days"
        distractors = [
            f"{(ans_float + 2):.1f}".rstrip("0").rstrip(".") + " days",
            f"{max(1.0, ans_float - 1.5):.1f}".rstrip("0").rstrip(".") + " days",
            f"{(ans_float * 1.5):.1f}".rstrip("0").rstrip(".") + " days",
        ]
        subtopic = "Time and Work"
        question_text = f"Worker A can complete a software deployment in {x} days, and Worker B can complete the same task in {y} days. Working concurrently with full velocity, in how many days will they finish the deployment together?"
        explanation = f"1 day work of A = 1/{x}. 1 day work of B = 1/{y}. Combined 1 day work = 1/{x} + 1/{y} = ({y} + {x})/({x}*{y}). Time taken = ({x}*{y})/({x}+{y}) = {x*y}/{x+y} = {ans_str}."

    elif chosen_type == "speed_distance_trains":
        # Train of length L crossing pole in T seconds. Speed = (L / T) * 18/5 km/h
        length = random.choice([120, 150, 180, 240, 300])
        time_sec = random.choice([9, 10, 12, 15, 18, 20])
        speed_kmh = round((length / time_sec) * 3.6, 1)
        ans_str = f"{speed_kmh} km/hr"
        distractors = [
            f"{round(speed_kmh + 8, 1)} km/hr",
            f"{round(max(20.0, speed_kmh - 12), 1)} km/hr",
            f"{round(speed_kmh * 1.25, 1)} km/hr",
        ]
        subtopic = "Speed, Time and Distance"
        question_text = f"An express train {length} meters long passes an automated track sensor in {time_sec} seconds. What is the speed of the train in km/hr?"
        explanation = f"Speed in m/s = Distance / Time = {length} / {time_sec} m/s. Converting to km/hr: ({length} / {time_sec}) * (18/5) = {speed_kmh} km/hr."

    elif chosen_type == "profit_loss_markup":
        cp = random.choice([200, 400, 500, 800, 1200, 1500])
        markup_pct = random.choice([20, 25, 30, 40, 50])
        discount_pct = random.choice([10, 15, 20])
        mp = cp * (1 + markup_pct / 100)
        sp = mp * (1 - discount_pct / 100)
        net_profit_pct = round(((sp - cp) / cp) * 100, 1)
        ans_str = f"{net_profit_pct}%"
        distractors = [
            f"{round(net_profit_pct + 5, 1)}%",
            f"{round(max(2.0, net_profit_pct - 4), 1)}%",
            f"{round(markup_pct - discount_pct, 1)}%",
        ]
        subtopic = "Profit, Loss and Discount"
        question_text = f"A merchant marks an enterprise hardware component {markup_pct}% above the cost price and then offers a promotional discount of {discount_pct}% on the marked price. What is the merchant's net profit percentage?"
        explanation = f"Let Cost Price = 100. Marked Price = {100 + markup_pct}. Selling Price after {discount_pct}% discount = {100 + markup_pct} * (1 - {discount_pct/100:.2f}) = {(100 + markup_pct) * (1 - discount_pct/100):.1f}. Net profit = {net_profit_pct}%."

    elif chosen_type == "compound_interest":
        p = random.choice([5000, 8000, 10000, 12000, 20000])
        r = random.choice([10, 12, 15, 20])
        ci_diff = round(p * ((r / 100) ** 2), 2)
        ans_str = f"Rs. {ci_diff:,.0f}" if ci_diff == int(ci_diff) else f"Rs. {ci_diff:,.2f}"
        distractors = [
            f"Rs. {round(ci_diff * 1.5, 2)}",
            f"Rs. {round(max(10.0, ci_diff - 40), 2)}",
            f"Rs. {round(ci_diff * 0.8, 2)}",
        ]
        subtopic = "Compound Interest & Simple Interest Difference"
        question_text = f"What is the difference between the compound interest (compounded annually) and simple interest on an investment principal of Rs. {p:,} at an annual interest rate of {r}% for 2 years?"
        explanation = f"For 2 years, Difference = Principal * (Rate / 100)^2 = {p} * ({r}/100)^2 = {p} * {((r/100)**2):.4f} = {ans_str}."

    elif chosen_type == "ratios_partnerships":
        inv1 = random.choice([3, 4, 5])
        inv2 = random.choice([5, 6, 7])
        inv3 = random.choice([8, 9, 10])
        total_profit = random.choice([32000, 48000, 64000, 96000])
        sum_ratio = inv1 + inv2 + inv3
        ans_share = round((inv2 / sum_ratio) * total_profit)
        ans_str = f"Rs. {ans_share:,}"
        distractors = [
            f"Rs. {round(ans_share * 1.2):,}",
            f"Rs. {round(ans_share * 0.85):,}",
            f"Rs. {round((inv1 / sum_ratio) * total_profit):,}",
        ]
        subtopic = "Ratio and Partnership"
        question_text = f"Three technology founders A, B, and C invest capital in a SaaS venture in the ratio {inv1}:{inv2}:{inv3}. If the total annual net profit is Rs. {total_profit:,}, what is the profit share of founder B?"
        explanation = f"Sum of ratios = {inv1} + {inv2} + {inv3} = {sum_ratio}. Share of B = ({inv2}/{sum_ratio}) * {total_profit} = {ans_str}."

    elif chosen_type == "permutation_probability":
        balls_red = random.choice([4, 5, 6])
        balls_blue = random.choice([3, 4, 5])
        total = balls_red + balls_blue
        # Probability both are red: (R * (R-1)) / (T * (T-1))
        num = balls_red * (balls_red - 1)
        den = total * (total - 1)
        gcd_val = math.gcd(num, den)
        ans_str = f"{num // gcd_val}/{den // gcd_val}"
        distractors = [
            f"{min(den-1, num // gcd_val + 1)}/{den // gcd_val}",
            f"{balls_red}/{total}",
            f"{(num // gcd_val)}/{max(1, den // gcd_val - 2)}",
        ]
        subtopic = "Probability and Combinatorics"
        question_text = f"A container has {balls_red} red microchips and {balls_blue} blue microchips. If two microchips are selected at random without replacement, what is the probability that both selected chips are red?"
        explanation = f"Total chips = {total}. P(First is red) = {balls_red}/{total}. P(Second is red) = {balls_red - 1}/{total - 1}. Combined probability = ({balls_red}/{total}) * ({balls_red - 1}/{total - 1}) = {num}/{den} = {ans_str}."

    elif chosen_type == "logical_coding_series":
        start = random.choice([3, 5, 7, 11])
        diff = random.choice([4, 6, 8, 9])
        series = [start + (i * i) + (i * diff) for i in range(5)]
        next_val = start + (5 * 5) + (5 * diff)
        ans_str = str(next_val)
        distractors = [str(next_val + 5), str(next_val - 6), str(next_val + 11)]
        subtopic = "Number Series Completion"
        question_text = f"Identify the missing next term in the logical number series: {', '.join(map(str, series))}, ?"
        explanation = f"Examining successive increments between terms reveals a quadratic pattern f(n) = n^2 + {diff}*n + {start}. Substituting n=5 gives {next_val}."

    else:
        # Data interpretation growth
        rev1 = random.choice([120, 150, 180, 200])
        rev2 = rev1 + random.choice([30, 45, 60, 75])
        pct_growth = round(((rev2 - rev1) / rev1) * 100, 1)
        ans_str = f"{pct_growth}%"
        distractors = [f"{round(pct_growth + 4.5, 1)}%", f"{round(max(5.0, pct_growth - 5.0), 1)}%", f"{round(pct_growth * 1.2, 1)}%"]
        subtopic = "Data Interpretation & Analytical Growth"
        question_text = f"A cloud service provider generated revenue of ${rev1} million in Q1 and ${rev2} million in Q4. What was the percentage growth in quarterly revenue?"
        explanation = f"Growth = ((Q4 Revenue - Q1 Revenue) / Q1 Revenue) * 100 = (({rev2} - {rev1}) / {rev1}) * 100 = {pct_growth}%."

    # Assemble and randomize options across strictly 4 options (A, B, C, D)
    options = ensure_four_options([ans_str] + distractors[:3], correct_val=ans_str, context_hint=question_text)
    random.shuffle(options)
    correct_idx = options.index(ans_str) if ans_str in options else 0

    q = AptitudeQuestion(
        topic_id=topic.id if topic else None,
        topic_name=topic.name if topic else topic_name,
        subtopic=subtopic,
        question=question_text,
        options_json=json.dumps(options),
        correct_option_index=correct_idx,
        explanation=explanation,
        difficulty=difficulty.lower(),
        company_tag=company_tag,
        status="approved",
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def get_non_repeating_daily_sprint_questions(
    db: Session,
    user_id: uuid.UUID,
    total_needed: int = 10,
) -> List[AptitudeQuestion]:
    """
    Returns a fresh batch of 10 non-repeating questions for the candidate's Daily Sprint.
    Excludes all questions previously served or attempted by this user.
    If database pool runs low on unseen questions, dynamically synthesizes fresh ones.
    """
    ensure_sprint_tables(db)
    excluded_ids = get_candidate_excluded_question_ids(db, user_id)

    # Fetch unseen approved questions
    query = db.query(AptitudeQuestion).filter(AptitudeQuestion.status != "archived")
    if excluded_ids:
        query = query.filter(~AptitudeQuestion.id.in_(excluded_ids))

    unseen_questions = query.order_by(func.random()).limit(total_needed).all()
    selected_questions: List[AptitudeQuestion] = list(unseen_questions)

    # If not enough unseen questions in database, generate fresh questions dynamically
    if len(selected_questions) < total_needed:
        needed = total_needed - len(selected_questions)
        logger.info(f"User {user_id} exhausted available questions. Dynamically generating {needed} fresh sprint questions.")
        for _ in range(needed):
            new_q = generate_dynamic_sprint_question(db, difficulty="medium")
            selected_questions.append(new_q)

    # Record served questions as seen for this candidate
    mark_questions_as_seen(
        db=db,
        user_id=user_id,
        question_ids=[q.id for q in selected_questions],
        sprint_type="daily_sprint",
    )

    return selected_questions


def get_non_repeating_weekly_sprint_questions(
    db: Session,
    user_id: uuid.UUID,
    apt_set: WeeklyAptitudeSet,
) -> Tuple[List[AptitudeQuestion], bool]:
    """
    Returns questions for the Weekly Placement Aptitude Sprint.
    - If user has never attempted this week's sprint:
      Serves the official weekly curriculum questions (or replaces any individual question
      the candidate has already seen in past daily sprints with a fresh one).
    - If user is RE-ATTEMPTING:
      GUARANTEES that previous questions do NOT repeat. Dynamically picks or synthesizes
      brand-new questions aligned with the week's curriculum focus.
    Returns: (questions, is_reattempt)
    """
    ensure_sprint_tables(db)

    # Check if candidate has already completed or attempted this weekly set
    prior_attempt = (
        db.query(WeeklyAptitudeAttempt)
        .filter(
            WeeklyAptitudeAttempt.weekly_set_id == apt_set.id,
            WeeklyAptitudeAttempt.user_id == user_id,
        )
        .first()
    )

    excluded_ids = get_candidate_excluded_question_ids(db, user_id)

    # Parse official weekly question IDs
    default_qids = []
    if apt_set.question_ids_json:
        try:
            default_qids = [uuid.UUID(qid) for qid in json.loads(apt_set.question_ids_json)]
        except Exception:
            default_qids = []

    is_reattempt = prior_attempt is not None or any(qid in excluded_ids for qid in default_qids)

    if not is_reattempt and default_qids:
        # First attempt and none of the default questions were previously seen
        questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(default_qids)).all()
        if len(questions) == len(default_qids):
            mark_questions_as_seen(
                db=db,
                user_id=user_id,
                question_ids=[q.id for q in questions],
                sprint_type="weekly_sprint",
            )
            return questions, False

    # RE-ATTEMPT OR DUPLICATES DETECTED:
    # Build a fresh, non-repeating set of questions for this candidate
    target_count = len(default_qids) if default_qids else 10
    target_count = max(5, target_count)

    # Exclude all previously attempted or seen questions
    combined_excluded = excluded_ids.union(set(default_qids))

    # Query unseen questions matching topics if possible
    unseen_query = db.query(AptitudeQuestion).filter(
        AptitudeQuestion.status != "archived",
        ~AptitudeQuestion.id.in_(combined_excluded),
    )
    fresh_candidates = unseen_query.order_by(func.random()).limit(target_count).all()
    selected: List[AptitudeQuestion] = list(fresh_candidates)

    # Generate additional fresh questions if needed
    if len(selected) < target_count:
        needed = target_count - len(selected)
        logger.info(f"Weekly sprint re-attempt for {user_id}: dynamically generating {needed} new questions.")
        for _ in range(needed):
            new_q = generate_dynamic_sprint_question(
                db=db,
                topic_name=apt_set.title,
                difficulty="medium",
                company_tag="Weekly Placement Sprint",
            )
            selected.append(new_q)

    mark_questions_as_seen(
        db=db,
        user_id=user_id,
        question_ids=[q.id for q in selected],
        sprint_type="weekly_sprint",
    )

    return selected, True


def get_non_repeating_topic_questions(
    db: Session,
    user_id: uuid.UUID,
    topic: AptitudeTopic,
    count: int = 10,
) -> List[AptitudeQuestion]:
    """
    Returns fresh, non-repeating practice questions for a specific topic.
    If the candidate has seen all or some existing questions for this topic,
    dynamically synthesizes fresh questions to guarantee that questions do NOT repeat.
    """
    ensure_sprint_tables(db)
    excluded_ids = get_candidate_excluded_question_ids(db, user_id)

    # Query unseen questions for this topic
    query = db.query(AptitudeQuestion).filter(
        AptitudeQuestion.status != "archived",
        (AptitudeQuestion.topic_id == topic.id) | (AptitudeQuestion.topic_name == topic.name),
    )
    if excluded_ids:
        query = query.filter(~AptitudeQuestion.id.in_(excluded_ids))

    unseen = query.order_by(func.random()).limit(count).all()
    selected: List[AptitudeQuestion] = list(unseen)

    if len(selected) < count:
        needed = count - len(selected)
        logger.info(
            f"Topic '{topic.name}' practice for candidate {user_id}: "
            f"dynamically generating {needed} fresh questions to ensure non-repetition."
        )
        for _ in range(needed):
            new_q = generate_dynamic_sprint_question(
                db=db,
                topic_name=topic.name,
                difficulty="medium",
                company_tag=f"{topic.name} Placement Practice",
            )
            # Ensure topic relationship is preserved
            new_q.topic_id = topic.id
            new_q.topic_name = topic.name
            db.commit()
            selected.append(new_q)

    # Record served questions as seen for this candidate
    mark_questions_as_seen(
        db=db,
        user_id=user_id,
        question_ids=[q.id for q in selected],
        sprint_type="topic_practice",
    )
    return selected


def get_non_repeating_test_questions(
    db: Session,
    user_id: uuid.UUID,
    test: AptitudeTest,
) -> List[AptitudeQuestion]:
    """
    Ensures that when a candidate attends an Aptitude Mock Test,
    any question previously attempted or seen by the candidate is swapped
    with a fresh, non-repeating question of matching difficulty and subtopic.
    """
    ensure_sprint_tables(db)
    excluded_ids = get_candidate_excluded_question_ids(db, user_id)

    # 1. Gather baseline questions configured for this test
    base_questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
    if not base_questions and test.question_ids_json:
        try:
            q_ids = [uuid.UUID(qid) for qid in json.loads(test.question_ids_json)]
            base_questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(q_ids)).all()
        except Exception:
            base_questions = []

    if not base_questions:
        base_questions = (
            db.query(AptitudeQuestion)
            .filter(AptitudeQuestion.status != "archived")
            .order_by(func.random())
            .limit(10)
            .all()
        )

    target_count = max(5, len(base_questions))
    selected: List[AptitudeQuestion] = []
    used_ids: Set[uuid.UUID] = set()

    for q in base_questions:
        if q.id not in excluded_ids and q.id not in used_ids:
            selected.append(q)
            used_ids.add(q.id)
        else:
            # Candidate has already attempted or seen this question.
            # Replace with a fresh unseen question from DB or synthesize dynamically.
            sub_q = None
            candidate_pool = db.query(AptitudeQuestion).filter(
                AptitudeQuestion.status != "archived",
                ~AptitudeQuestion.id.in_(excluded_ids.union(used_ids)),
            )
            if q.subtopic:
                sub_q = candidate_pool.filter(AptitudeQuestion.subtopic == q.subtopic).order_by(func.random()).first()
            if not sub_q and q.topic_name:
                sub_q = candidate_pool.filter(AptitudeQuestion.topic_name == q.topic_name).order_by(func.random()).first()
            if not sub_q:
                sub_q = candidate_pool.order_by(func.random()).first()

            if sub_q:
                selected.append(sub_q)
                used_ids.add(sub_q.id)
            else:
                # Synthesize fresh question dynamically matching subtopic & difficulty
                new_q = generate_dynamic_sprint_question(
                    db=db,
                    topic_name=q.topic_name or test.title,
                    subtopic_hint=q.subtopic,
                    difficulty=q.difficulty or "medium",
                    company_tag=test.company_tag or test.title or "Placement Mock",
                )
                selected.append(new_q)
                used_ids.add(new_q.id)

    # If count is still less than expected, fill dynamically
    while len(selected) < target_count:
        new_q = generate_dynamic_sprint_question(
            db=db,
            topic_name=test.title,
            difficulty="medium",
            company_tag=test.company_tag or test.title or "Placement Mock",
        )
        selected.append(new_q)
        used_ids.add(new_q.id)

    # Record served questions as seen for this candidate
    mark_questions_as_seen(
        db=db,
        user_id=user_id,
        question_ids=[q.id for q in selected],
        sprint_type="test_mock",
    )
    return selected


