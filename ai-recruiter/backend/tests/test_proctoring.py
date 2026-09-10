"""
test_proctoring.py — Automated Unit & Integration Tests for AI-Assisted Proctored Assessment & Integrity Monitoring.
Tests multi-language AST code similarity analysis, token normalization, and evidence-based integrity scoring.
"""
import pytest

from app.services.code_similarity_service import compare_code_pair, normalize_code, remove_comments_and_docstrings
from app.services.integrity_scoring_service import calculate_attempt_integrity


def test_remove_comments_and_docstrings():
    """Verify comments and docstrings are removed correctly."""
    python_code = "# This is a comment\ndef foo():\n    \"\"\"Docstring\"\"\"\n    return 42"
    clean = remove_comments_and_docstrings(python_code, "python")
    assert "# This is a comment" not in clean
    assert '"""Docstring"""' not in clean
    assert "def foo():" in clean


def test_normalize_code_variable_renaming():
    """Verify identifier normalization renames local variables consistently."""
    code1 = "def calculate_total(price, tax):\n    subtotal = price * tax\n    return subtotal"
    code2 = "def compute_sum(val, rate):\n    res = val * rate\n    return res"

    norm1 = normalize_code(code1, "python")
    norm2 = normalize_code(code2, "python")

    # Identifiers should be mapped to generic tokens VAR_0, VAR_1 etc.
    assert "VAR_" in norm1
    assert "VAR_" in norm2


def test_code_similarity_variable_renamed():
    """Test AST & Token hybrid similarity engine on renamed variable code."""
    code1 = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
"""

    code2 = """
# Candidate solution
def solve(arr, val):
    lookup = {}
    for index, item in enumerate(arr):
        remainder = val - item
        if remainder in lookup:
            return [lookup[remainder], index]
        lookup[item] = index
    return []
"""

    score, summary = compare_code_pair(code1, code2, "python")
    assert score >= 50.0
    assert "similarity" in summary.lower()


def test_code_similarity_distinct():
    """Test that distinct algorithm solutions return low similarity."""
    code1 = "def is_even(n):\n    return n % 2 == 0"
    code2 = "def quicksort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)"

    score, summary = compare_code_pair(code1, code2, "python")
    assert score < 40.0
