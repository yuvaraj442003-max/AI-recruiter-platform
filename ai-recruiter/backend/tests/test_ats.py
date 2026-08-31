"""
test_ats.py — Unit and Integration tests for ATS Score Analysis, Skill Normalization & Job Matching.
"""
from app.services.ats_scoring_service import (
    ATS_WEIGHTS,
    calculate_job_specific_ats,
    extract_keywords_from_text,
    generate_ai_suggestions,
    normalize_skill,
)


def test_ats_weights_sum_to_one():
    total_weight = sum(ATS_WEIGHTS.values())
    assert abs(total_weight - 1.0) < 1e-6


def test_skill_normalization():
    assert normalize_skill("py") == "Python"
    assert normalize_skill("postgres") == "PostgreSQL"
    assert normalize_skill("js") == "JavaScript"
    assert normalize_skill("ts") == "TypeScript"
    assert normalize_skill("k8s") == "Kubernetes"
    assert normalize_skill("ga4") == "Google Analytics"


def test_extract_keywords_from_text():
    text = "We are looking for a Senior Python and FastAPI Developer with PostgreSQL, Docker, and REST API experience for building scalable cloud microservices."
    keywords = extract_keywords_from_text(text, max_keywords=10)
    assert "Python" in keywords or "python" in [k.lower() for k in keywords]
    assert "FastAPI" in keywords or "fastapi" in [k.lower() for k in keywords]
    assert "and" not in keywords
    assert "the" not in keywords


def test_generate_ai_suggestions():
    suggestions = generate_ai_suggestions(
        job_title="Senior Data Analyst",
        missing_skills=["Power BI", "Tableau"],
        missing_keywords=["Data Visualization", "ETL"],
        candidate_exp=2.0,
        required_exp=5.0,
        job_description="Looking for an experienced Data Analyst proficient in SQL, Python, and Power BI."
    )
    assert len(suggestions) > 0
    assert any("Power BI" in s or "Tableau" in s for s in suggestions)
