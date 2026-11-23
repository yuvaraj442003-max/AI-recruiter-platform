"""
question_balancer.py — Universal Option Balancing & Randomization Utility.

Ensures test/exam questions in Campus Hub, Textbooks, Daily Assessments,
and Company Mock Tests have correct answers distributed evenly across
all four options (A: 0, B: 1, C: 2, D: 3) instead of always defaulting to Option A.
Keeps question options, correct index, explanation, and evaluation strictly synchronized.
"""

import copy
import json
import random
from typing import Any, Dict, List, Optional, Union


def balance_and_randomize_options(
    question: Any,
    target_idx: Optional[int] = None,
) -> Any:
    """
    Evenly distributes and randomizes the correct option position across A, B, C, D (0, 1, 2, 3).
    Supports dicts and Pydantic models (AptitudeQuestionGeneratedItem, MilestoneQuizQuestionOut, etc.).
    Preserves exact correctness: options[correct_option_index] will always be the true answer.
    """
    if question is None:
        return question

    is_dict = isinstance(question, dict)
    options = question.get("options") if is_dict else getattr(question, "options", None)

    # Parse options if serialized as string
    if isinstance(options, str):
        try:
            options = json.loads(options)
        except Exception:
            options = None

    if not isinstance(options, list) or len(options) < 2:
        return question

    # Standardize options to string list
    raw_options = [str(o) for o in options]
    n_opts = len(raw_options)

    # Get original correct option index
    orig_idx_raw = question.get("correct_option_index") if is_dict else getattr(question, "correct_option_index", None)
    try:
        orig_idx = int(orig_idx_raw) if orig_idx_raw is not None else 0
    except (ValueError, TypeError):
        orig_idx = 0

    if orig_idx < 0 or orig_idx >= n_opts:
        orig_idx = 0

    # Pick or validate target index
    if target_idx is None or target_idx < 0 or target_idx >= n_opts:
        target_idx = random.randint(0, n_opts - 1)

    correct_val = raw_options[orig_idx]
    other_vals = [opt for idx, opt in enumerate(raw_options) if idx != orig_idx]
    random.shuffle(other_vals)

    new_options = []
    other_pointer = 0
    for slot in range(n_opts):
        if slot == target_idx:
            new_options.append(correct_val)
        else:
            new_options.append(other_vals[other_pointer])
            other_pointer += 1

    if is_dict:
        question["options"] = new_options
        question["correct_option_index"] = target_idx
    else:
        try:
            question.options = new_options
            question.correct_option_index = target_idx
        except Exception:
            pass

    return question


def balance_question_list(
    questions: List[Any],
) -> List[Any]:
    """
    Takes an entire list of questions (dicts or Pydantic models) and distributes
    correct answers across A (0), B (1), C (2), and D (3) using randomized cycles.
    Guarantees ~25% representation for each option letter and eliminates Option A bias.
    """
    if not questions:
        return questions

    n = len(questions)
    slots: List[int] = []
    while len(slots) < n:
        chunk = [0, 1, 2, 3]
        random.shuffle(chunk)
        slots.extend(chunk)

    for i, q in enumerate(questions):
        balance_and_randomize_options(q, target_idx=slots[i])

    return questions
