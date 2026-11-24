"""
question_balancer.py — Universal Option Balancing, 4-Option Enforcement & Randomization Utility.

Ensures test/exam questions in Campus Hub, Textbooks, Daily Assessments,
Company Mock Tests, Weekly Challenges, and Aptitude Tests have ALL FOUR
answer options (A, B, C, and D) and that correct answers are distributed evenly
across all four options (A: 0, B: 1, C: 2, D: 3) instead of defaulting to Option A.
Keeps question options, correct index, explanation, and evaluation strictly synchronized.
"""

import copy
import json
import random
import re
from typing import Any, Dict, List, Optional, Union


def ensure_four_options(
    options: Any,
    correct_val: Optional[str] = None,
    context_hint: str = "",
) -> List[str]:
    """
    Guarantees that ANY question option list has EXACTLY 4 distinct, non-empty options
    corresponding to A (index 0), B (index 1), C (index 2), and D (index 3).

    - If options has > 4: trims down to 4 while strictly preserving the correct answer.
    - If options has < 4: pads with context-appropriate, high-quality distractors
      (e.g. realistic boolean choices, math alternatives, or standard corporate placement choices)
      so every assessment question always provides all four options (A, B, C, and D).
    - If options is empty/invalid: provides standard 4-option placement choices.
    """
    if options is None:
        opts_list = []
    elif isinstance(options, str):
        try:
            parsed = json.loads(options)
            opts_list = parsed if isinstance(parsed, list) else [options]
        except Exception:
            opts_list = [options]
    elif isinstance(options, (list, tuple)):
        opts_list = list(options)
    else:
        opts_list = [str(options)]

    # Clean and stringify each option
    cleaned: List[str] = []
    for opt in opts_list:
        if isinstance(opt, dict):
            # E.g. {"A": "text"} or {"option_text": "text"}
            val = opt.get("option_text") or (list(opt.values())[0] if opt else "")
        else:
            val = str(opt)
        s = val.strip()
        if s and s not in cleaned:
            cleaned.append(s)

    # If correct_val is specified and not present, ensure it's in cleaned
    if correct_val is not None:
        c_str = str(correct_val).strip()
        if c_str and c_str not in cleaned:
            cleaned.insert(0, c_str)

    # Distractor pools based on existing options
    lower_opts = [o.lower() for o in cleaned]
    is_boolean = any(o in ["true", "false", "yes", "no"] for o in lower_opts)
    is_numeric = all(re.match(r"^[\d\.\+\-\*/%\$₹\s]+$", o) for o in cleaned) if cleaned else False

    if is_boolean:
        distractor_pool = [
            "Cannot be determined from the given information",
            "Partially true / conditionally depends on input",
            "Insufficient data provided",
            "None of the above",
            "Both statements are valid",
        ]
    elif is_numeric:
        distractor_pool = [
            "None of these",
            "Cannot be determined",
            "Data insufficient",
            "Undefined / Infinite",
            "Zero",
        ]
    else:
        distractor_pool = [
            "None of the above",
            "Both A and B",
            "Cannot be determined from the provided conditions",
            "Data is insufficient to conclude",
            "All of the above",
            "Independent of the given parameters",
        ]

    # If we have more than 4, retain correct_val and take up to 4
    if len(cleaned) > 4:
        if correct_val is not None and str(correct_val).strip() in cleaned:
            c_str = str(correct_val).strip()
            others = [o for o in cleaned if o != c_str]
            cleaned = [c_str] + others[:3]
        else:
            cleaned = cleaned[:4]

    # If we have fewer than 4, pad until exactly 4
    if len(cleaned) < 4:
        for distractor in distractor_pool:
            if len(cleaned) >= 4:
                break
            if distractor not in cleaned and distractor.lower() not in [o.lower() for o in cleaned]:
                cleaned.append(distractor)

        # Fallback padding if needed
        letters = ["A", "B", "C", "D"]
        pad_idx = len(cleaned)
        while len(cleaned) < 4:
            fallback_name = f"Option {letters[pad_idx] if pad_idx < 4 else pad_idx + 1}"
            if fallback_name not in cleaned:
                cleaned.append(fallback_name)
            else:
                cleaned.append(f"Alternative {pad_idx + 1}")
            pad_idx += 1

    return cleaned[:4]


def balance_and_randomize_options(
    question: Any,
    target_idx: Optional[int] = None,
) -> Any:
    """
    Evenly distributes and randomizes the correct option position across A, B, C, D (0, 1, 2, 3).
    Supports dicts and Pydantic models (AptitudeQuestionGeneratedItem, MilestoneQuizQuestionOut, etc.).
    Preserves exact correctness: options[correct_option_index] will always be the true answer.
    Guarantees EVERY question has ALL FOUR options (A, B, C, and D).
    """
    if question is None:
        return question

    is_dict = isinstance(question, dict)
    raw_options = question.get("options") if is_dict else getattr(question, "options", None)

    # Determine original correct index
    orig_idx_raw = question.get("correct_option_index") if is_dict else getattr(question, "correct_option_index", None)
    try:
        orig_idx = int(orig_idx_raw) if orig_idx_raw is not None else 0
    except (ValueError, TypeError):
        orig_idx = 0

    # Extract original correct answer string before any padding
    orig_correct_val = None
    if isinstance(raw_options, list) and 0 <= orig_idx < len(raw_options):
        orig_correct_val = str(raw_options[orig_idx]).strip()

    # Enforce strictly 4 options (A, B, C, D)
    options = ensure_four_options(raw_options, correct_val=orig_correct_val)

    # Determine index of correct answer in the 4 options
    if orig_correct_val is not None and orig_correct_val in options:
        curr_corr_idx = options.index(orig_correct_val)
    else:
        curr_corr_idx = min(max(0, orig_idx), 3)

    correct_val = options[curr_corr_idx]

    # Pick or validate target index (0, 1, 2, or 3)
    if target_idx is None or target_idx < 0 or target_idx >= 4:
        target_idx = random.randint(0, 3)

    other_vals = [opt for idx, opt in enumerate(options) if idx != curr_corr_idx]
    random.shuffle(other_vals)

    new_options = []
    other_pointer = 0
    for slot in range(4):
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
    Takes an entire list of questions (dicts or Pydantic models) and ensures
    EVERY question has all four answer options (A, B, C, and D), with correct answers
    distributed evenly across A (0), B (1), C (2), and D (3) using randomized cycles.
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
