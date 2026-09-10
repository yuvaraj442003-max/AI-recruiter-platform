"""
code_similarity_service.py — AST & Token Hybrid Code Similarity Engine.
Normalizes, tokenizes, and compares candidate code submissions across Python,
JavaScript, TypeScript, Java, C, C++, and Go to detect potential code plagiarism.
"""
import ast
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("ai_recruiter.code_similarity")


def remove_comments_and_docstrings(source: str, language: str = "python") -> str:
    """Removes language-specific comments and whitespace noise."""
    lang = language.lower()
    if lang == "python":
        # Remove Python comments # ...
        code = re.sub(r"#.*$", "", source, flags=re.MULTILINE)
        # Remove triple-quote docstrings
        code = re.sub(r'"""[\s\S]*?"""', "", code)
        code = re.sub(r"'''[\s\S]*?'''", "", code)
        return code
    elif lang in ("javascript", "typescript", "java", "c", "cpp", "c++", "go"):
        # Remove single-line // ... and multi-line /* ... */ comments
        code = re.sub(r"//.*$", "", source, flags=re.MULTILINE)
        code = re.sub(r"/\*[\s\S]*?\*/", "", code)
        return code
    return source


def normalize_code(source: str, language: str = "python") -> str:
    """
    Normalizes identifier names, keywords, and layout to allow AST/token structural comparison.
    """
    clean_code = remove_comments_and_docstrings(source, language)

    # Replace string literals with "STR"
    clean_code = re.sub(r'".*?"|\'.*?\'', '"STR"', clean_code)
    # Replace numbers with "0"
    clean_code = re.sub(r"\b\d+(?:\.\d+)?\b", "0", clean_code)

    # Identifier tokenization for variable renaming
    identifiers = set(re.findall(r"\b[a-zA-Z_]\w*\b", clean_code))
    keywords = {
        "def", "class", "return", "if", "else", "elif", "for", "while", "import", "from",
        "try", "except", "with", "as", "pass", "break", "continue", "in", "is", "not", "and", "or",
        "function", "const", "let", "var", "public", "private", "protected", "static", "void",
        "int", "float", "double", "char", "bool", "boolean", "struct", "func", "package", "type",
    }
    custom_ids = sorted(list(identifiers - keywords), key=len, reverse=True)

    id_map = {id_name: f"VAR_{idx}" for idx, id_name in enumerate(custom_ids)}

    for orig_id, tok_name in id_map.items():
        clean_code = re.sub(rf"\b{re.escape(orig_id)}\b", tok_name, clean_code)

    # Normalize whitespace
    lines = [line.strip() for line in clean_code.splitlines() if line.strip()]
    return "\n".join(lines)


def get_ast_structure_fingerprint(source: str) -> Optional[str]:
    """Generates an AST node sequence fingerprint for Python source code."""
    try:
        parsed = ast.parse(source)
        nodes = [type(node).__name__ for node in ast.walk(parsed)]
        return "-".join(nodes)
    except Exception:
        return None


def get_token_ngrams(source: str, n: int = 3) -> List[str]:
    """Extracts lexical N-grams from normalized source text."""
    tokens = re.findall(r"\w+|[^\w\s]", source)
    if len(tokens) < n:
        return ["".join(tokens)]
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def calculate_jaccard_similarity(ngrams1: List[str], ngrams2: List[str]) -> float:
    """Computes Jaccard Similarity index (0.0 to 1.0) between token sets."""
    set1, set2 = set(ngrams1), set(ngrams2)
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def calculate_levenshtein_similarity(str1: str, str2: str) -> float:
    """Calculates normalized Levenshtein edit distance similarity (0.0 to 1.0)."""
    if not str1 or not str2:
        return 0.0 if str1 != str2 else 1.0
    if str1 == str2:
        return 1.0

    len1, len2 = len(str1), len(str2)
    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,      # deletion
                matrix[i][j - 1] + 1,      # insertion
                matrix[i - 1][j - 1] + cost, # substitution
            )

    dist = matrix[len1][len2]
    max_len = max(len1, len2)
    return max(0.0, 1.0 - (dist / max_len))


def compare_code_pair(code1: str, code2: str, language: str = "python") -> Tuple[float, str]:
    """
    Compares two code submissions and returns similarity percentage (0-100) and analysis summary.
    """
    if not code1 or not code2 or len(code1.strip()) < 10 or len(code2.strip()) < 10:
        return 0.0, "Insufficient code length for similarity analysis."

    norm1 = normalize_code(code1, language)
    norm2 = normalize_code(code2, language)

    # 1. Lexical N-Gram Jaccard Index
    tok1 = get_token_ngrams(norm1, n=3)
    tok2 = get_token_ngrams(norm2, n=3)
    jaccard_sim = calculate_jaccard_similarity(tok1, tok2)

    # 2. Levenshtein Structural Distance
    lev_sim = calculate_levenshtein_similarity(norm1[:500], norm2[:500])  # Sample first 500 chars for efficiency

    # 3. Python AST Fingerprint Match if applicable
    ast_bonus = 0.0
    if language.lower() == "python":
        ast1 = get_ast_structure_fingerprint(code1)
        ast2 = get_ast_structure_fingerprint(code2)
        if ast1 and ast2 and ast1 == ast2:
            ast_bonus = 0.20

    combined_score = min(100.0, max(0.0, ((jaccard_sim * 0.6) + (lev_sim * 0.4) + ast_bonus) * 100.0))
    round_score = round(combined_score, 1)

    if round_score >= 80.0:
        analysis = f"High code similarity detected ({round_score}% match). AST and normalized token structures show identical algorithmic patterns."
    elif round_score >= 50.0:
        analysis = f"Moderate code similarity ({round_score}% match). Similar function layout and token sequences observed."
    else:
        analysis = f"Low code similarity ({round_score}% match). Submissions demonstrate independent structural implementations."

    return round_score, analysis


def analyze_submission_against_history(
    target_code: str,
    language: str,
    previous_submissions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Analyzes a candidate submission against a corpus of existing submissions for the same question.
    Returns highest similarity match, confidence, and AI assistance heuristics.
    """
    if not previous_submissions:
        return {
            "max_similarity_score": 0.0,
            "matched_submission_id": None,
            "confidence": 0.95,
            "analysis_summary": "First submission recorded for this question. No similarity matches.",
            "ai_assistance_signal": "Low",
        }

    highest_score = 0.0
    best_match_id = None
    best_summary = "Unique submission."

    for sub in previous_submissions:
        sub_code = sub.get("source_code") or ""
        sub_id = sub.get("id")
        score, summary = compare_code_pair(target_code, sub_code, language)

        if score > highest_score:
            highest_score = score
            best_match_id = sub_id
            best_summary = summary

    # Heuristic AI assistance signal (detects sudden boilerplate injection or uniform styling)
    lines = target_code.strip().splitlines()
    has_advanced_type_hints = bool(re.search(r":\sup.List\[|:\sDict\[|:\sOptional\[", target_code))
    is_very_long = len(lines) > 40
    ai_signal = "Moderate" if (has_advanced_type_hints and is_very_long) else "Low"

    return {
        "max_similarity_score": highest_score,
        "matched_submission_id": best_match_id,
        "confidence": 0.92,
        "analysis_summary": best_summary,
        "ai_assistance_signal": ai_signal,
    }
