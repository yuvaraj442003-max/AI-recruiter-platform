"""
coding_evaluation_service.py — Test case evaluation, code quality analysis,
time/space complexity estimation, AI code review, and candidate score computation.
"""
import ast
import json
import logging
import re
from typing import Any, Dict, List, Optional

from app.ai.llm_service import generate as generate_llm
from app.services.code_executor import execute_code

logger = logging.getLogger("ai_recruiter.coding_eval")


def normalize_output(text: str) -> str:
    """Normalizes stdout text for clean string comparison."""
    if text is None:
        return ""
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines)


def analyze_complexity(source_code: str, language: str) -> Dict[str, str]:
    """
    Estimates time and space complexity using static analysis (AST/regex).
    """
    lang = language.lower()
    time_comp = "O(n)"
    space_comp = "O(1)"

    if lang in ("python", "py"):
        try:
            tree = ast.parse(source_code)
            loop_depth = 0

            class LoopVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.max_depth = 0
                    self.current_depth = 0
                    self.has_recursion = False

                def visit_For(self, node):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    self.generic_visit(node)
                    self.current_depth -= 1

                def visit_While(self, node):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    self.generic_visit(node)
                    self.current_depth -= 1

            visitor = LoopVisitor()
            visitor.visit(tree)

            if visitor.max_depth == 0:
                time_comp = "O(1)"
            elif visitor.max_depth == 1:
                time_comp = "O(n)"
            elif visitor.max_depth == 2:
                time_comp = "O(n²)"
            elif visitor.max_depth >= 3:
                time_comp = f"O(n^{visitor.max_depth})"

            if "append" in source_code or "dict" in source_code or "[" in source_code:
                space_comp = "O(n)"
            else:
                space_comp = "O(1)"

        except Exception:
            pass
    else:
        # Regex heuristics for non-Python languages
        for_loops = len(re.findall(r'\bfor\b', source_code)) + len(re.findall(r'\bwhile\b', source_code))
        if for_loops == 0:
            time_comp = "O(1)"
        elif for_loops == 1:
            time_comp = "O(n)"
        elif for_loops >= 2:
            time_comp = "O(n²)"

        if "new" in source_code or "[]" in source_code or "vector" in source_code:
            space_comp = "O(n)"

    return {"time_complexity": time_comp, "space_complexity": space_comp}


def analyze_code_quality(source_code: str, language: str) -> float:
    """
    Computes heuristic quality score (0-100) based on length, naming, comments, and structure.
    """
    score = 80.0
    lines = [l.strip() for l in source_code.splitlines() if l.strip()]
    if not lines:
        return 0.0

    # Readability: reasonable line length and function structure
    if len(lines) > 5 and len(lines) < 100:
        score += 5
    if any(line.startswith("#") or line.startswith("//") or "/*" in line for line in lines):
        score += 5  # Has comments
    if any("def " in l or "function " in l or "class " in l or "public static" in l for l in lines):
        score += 5  # Modular code

    # Deductions
    long_lines = [l for l in lines if len(l) > 120]
    if long_lines:
        score -= min(10, len(long_lines) * 2)

    return max(10.0, min(100.0, score))


def evaluate_question_submission(
    question_title: str,
    test_cases: List[Dict[str, Any]],
    language: str,
    source_code: str,
    run_only_public: bool = False
) -> Dict[str, Any]:
    """
    Runs candidate code against test cases and evaluates functional, quality, and complexity metrics.
    """
    if run_only_public:
        eval_cases = [tc for tc in test_cases if not tc.get("is_hidden", False)]
    else:
        eval_cases = test_cases

    if not eval_cases:
        eval_cases = test_cases

    passed_count = 0
    total_count = len(eval_cases)
    total_points = sum(tc.get("points", 10) for tc in eval_cases) or 1
    earned_points = 0

    results_detail = []
    max_exec_time = 0.0

    for idx, tc in enumerate(eval_cases, 1):
        input_data = str(tc.get("input_data", ""))
        expected = str(tc.get("expected_output", ""))
        is_hidden = tc.get("is_hidden", False)
        pts = tc.get("points", 10)

        exec_res = execute_code(language, source_code, input_data=input_data, timeout_seconds=5.0)
        max_exec_time = max(max_exec_time, exec_res.get("execution_time", 0.0))

        actual_stdout = exec_res.get("stdout", "")
        norm_actual = normalize_output(actual_stdout)
        norm_expected = normalize_output(expected)

        passed = (exec_res["status"] == "Success") and (norm_actual == norm_expected)
        if not passed and norm_expected.upper() in ["A", "B", "C", "D"]:
            import re
            cleaned_source = source_code.strip().strip("'\"").strip().upper()
            found_letter = None
            # Check for print("X"), console.log("X"), Option X, or just X
            m = re.search(r'(?:print|console\.log|option|answer|\b)\s*\(?[\'"]?([A-D])[\'"]?\)?\b', cleaned_source, re.IGNORECASE)
            if m:
                found_letter = m.group(1).upper()
            if cleaned_source == norm_expected.upper() or norm_actual.strip().upper() == norm_expected.upper() or found_letter == norm_expected.upper():
                passed = True

        if passed:
            passed_count += 1
            earned_points += pts

        # Protect hidden test case input/output details
        if is_hidden and not passed:
            detail = {
                "test_case": idx,
                "status": "Failed",
                "is_hidden": True,
                "message": "Hidden test case failed."
            }
        elif is_hidden and passed:
            detail = {
                "test_case": idx,
                "status": "Passed",
                "is_hidden": True,
                "message": "Hidden test case passed."
            }
        else:
            detail = {
                "test_case": idx,
                "status": "Passed" if passed else "Failed",
                "is_hidden": False,
                "input_data": input_data,
                "expected_output": expected,
                "actual_output": norm_actual,
                "error": exec_res.get("stderr", "") if exec_res["status"] != "Success" else ""
            }
        results_detail.append(detail)

    functional_score = round((earned_points / total_points) * 100.0, 2)
    quality_score = analyze_code_quality(source_code, language)
    complexity = analyze_complexity(source_code, language)

    # Efficiency score based on execution time
    efficiency_score = 90.0 if max_exec_time < 1.0 else (70.0 if max_exec_time < 3.0 else 50.0)
    complexity_score = 90.0 if complexity["time_complexity"] in ("O(1)", "O(n)") else 70.0

    # Formula: 70% Functional + 15% Quality + 10% Efficiency + 5% Complexity
    final_score = round(
        (functional_score * 0.70) +
        (quality_score * 0.15) +
        (efficiency_score * 0.10) +
        (complexity_score * 0.05),
        2
    )

    return {
        "passed": passed_count,
        "total": total_count,
        "functional_score": functional_score,
        "quality_score": quality_score,
        "efficiency_score": efficiency_score,
        "complexity_score": complexity_score,
        "final_score": final_score,
        "time_complexity": complexity["time_complexity"],
        "space_complexity": complexity["space_complexity"],
        "execution_time": max_exec_time,
        "memory_used": 15.0,
        "test_case_details": results_detail
    }


def generate_ai_code_review(
    question_title: str,
    language: str,
    source_code: str,
    functional_score: float,
    time_complexity: str,
    space_complexity: str
) -> Dict[str, Any]:
    """
    Generates structured AI review of candidate code via LLM, with fallback template.
    """
    system_prompt = "You are an expert technical interviewer and code reviewer. Provide concise, constructive JSON evaluation of candidate code."
    user_prompt = f"""
    Review this {language} solution for question '{question_title}'.
    Functional Test Score: {functional_score}%
    Detected Time Complexity: {time_complexity}
    Detected Space Complexity: {space_complexity}

    Source Code:
    ```
    {source_code}
    ```

    Respond strictly in JSON format with keys:
    "code_quality" (number 0-100),
    "readability" (number 0-100),
    "maintainability" (number 0-100),
    "efficiency" (number 0-100),
    "time_complexity" (string),
    "space_complexity" (string),
    "strengths" (list of strings),
    "weaknesses" (list of strings),
    "suggestions" (list of strings)
    """

    llm_resp = generate_llm(system_prompt=system_prompt, user_prompt=user_prompt)
    if llm_resp:
        try:
            # Extract JSON block
            json_str = llm_resp.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            parsed = json.loads(json_str)
            return parsed
        except Exception:
            pass

    # Deterministic fallback review
    return {
        "code_quality": int(functional_score * 0.9 + 10),
        "readability": 85,
        "maintainability": 80,
        "efficiency": 85 if functional_score > 70 else 60,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "strengths": [
            f"Successfully handled {int(functional_score)}% of functional test cases",
            f"Implemented clean logic in {language.capitalize()}"
        ],
        "weaknesses": [
            "Edge case handling could be enhanced",
            "Consider adding input boundary validations"
        ],
        "suggestions": [
            "Add comments documenting complex logic sections",
            "Optimize memory usage for larger datasets"
        ]
    }
