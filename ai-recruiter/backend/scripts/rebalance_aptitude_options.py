"""
rebalance_aptitude_options.py — Normalizes and redistributes correct option indices
across all aptitude questions so that correct answers are evenly spread across
Option A (0), Option B (1), Option C (2), and Option D (3) (~25% each).
"""
import sys
import os
import json
from collections import Counter

import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine, Base
from app.models.student import AptitudeQuestion, AptitudeOption
from app.models.weekly_challenge import WeeklyAptitudeSet


def rebalance_aptitude_options(db=None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        questions = db.query(AptitudeQuestion).order_by(AptitudeQuestion.created_at.asc(), AptitudeQuestion.id.asc()).all()
        total = len(questions)
        print(f"[*] Found {total} aptitude questions in database.")

        before_counts = Counter(q.correct_option_index for q in questions)
        print(f"[*] Distribution BEFORE rebalancing: {dict(before_counts)}")

        rebalanced_count = 0

        for i, q in enumerate(questions):
            if not q.options_json:
                continue
            try:
                opts = json.loads(q.options_json)
            except Exception:
                continue

            if not isinstance(opts, list) or len(opts) != 4:
                continue

            # Deterministic, balanced target index (0=A, 1=B, 2=C, 3=D)
            target_idx = i % 4
            curr_idx = q.correct_option_index
            if curr_idx < 0 or curr_idx >= len(opts):
                curr_idx = 0

            if curr_idx != target_idx:
                # Identify the exact correct answer text
                correct_text = opts[curr_idx]
                target_text = opts[target_idx]

                # Swap the options so correct answer text is now at target_idx
                opts[curr_idx] = target_text
                opts[target_idx] = correct_text

                q.options_json = json.dumps(opts)
                q.correct_option_index = target_idx
                rebalanced_count += 1

                # Update any associated AptitudeOption rows if present
                if q.options:
                    for opt in q.options:
                        if 0 <= opt.order_index < len(opts):
                            opt.option_text = opts[opt.order_index]
                            opt.is_correct = (opt.order_index == target_idx)

        # Specifically balance each weekly aptitude challenge set in rotation (0, 1, 2, 3...)
        weekly_sets = db.query(WeeklyAptitudeSet).all()
        for wset in weekly_sets:
            if wset.question_ids_json:
                try:
                    q_ids = json.loads(wset.question_ids_json)
                    for idx, q_id_val in enumerate(q_ids):
                        q_id = uuid.UUID(str(q_id_val)) if not isinstance(q_id_val, uuid.UUID) else q_id_val
                        sq = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == q_id).first()
                        if not sq or not sq.options_json:
                            continue
                        opts = json.loads(sq.options_json)
                        if not isinstance(opts, list) or len(opts) != 4:
                            continue
                        target_idx = idx % 4
                        curr_idx = sq.correct_option_index
                        if curr_idx < 0 or curr_idx >= len(opts):
                            curr_idx = 0
                        if curr_idx != target_idx:
                            opts[curr_idx], opts[target_idx] = opts[target_idx], opts[curr_idx]
                            sq.options_json = json.dumps(opts)
                            sq.correct_option_index = target_idx
                            if sq.options:
                                for opt in sq.options:
                                    if 0 <= opt.order_index < len(opts):
                                        opt.option_text = opts[opt.order_index]
                                        opt.is_correct = (opt.order_index == target_idx)
                except Exception as e:
                    print(f"[!] Error balancing weekly set {wset.week_code}: {e}")

        db.commit()

        # Verify new distribution across entire database
        updated_questions = db.query(AptitudeQuestion).all()
        after_counts = Counter(q.correct_option_index for q in updated_questions)
        print(f"[*] Distribution AFTER rebalancing: {dict(after_counts)}")
        print(f"[+] Successfully rebalanced {rebalanced_count} questions out of {total}!")

        # Verify weekly aptitude challenge set distributions
        weekly_sets = db.query(WeeklyAptitudeSet).all()
        for wset in weekly_sets:
            if wset.question_ids_json:
                try:
                    q_ids = json.loads(wset.question_ids_json)
                    set_q_ids = [uuid.UUID(str(qid)) for qid in q_ids]
                    set_qs = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(set_q_ids)).all()
                    set_counts = Counter(sq.correct_option_index for sq in set_qs)
                    print(f"[*] Weekly Set '{wset.title}' ({wset.week_code}) option distribution: {dict(set_counts)}")
                except Exception as e:
                    print(f"[!] Error inspecting weekly set: {e}")

        return after_counts

    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    rebalance_aptitude_options()
