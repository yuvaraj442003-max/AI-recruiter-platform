"""
test_resume_improvement.py — Unit and Integration tests for AI Resume Coach & Improvement Engine.
"""
from app.services.resume_improvement_service import (
    analyze_achievements_and_metrics,
    analyze_formatting,
    analyze_grammar_and_tense,
    detect_weak_sentences,
)


def test_detect_weak_sentences():
    weak_text = "Worked on Python projects. Responsible for managing database tasks. Helped with API design."
    weak_items = detect_weak_sentences(weak_text, "Senior Python Developer")
    
    assert len(weak_items) > 0
    first = weak_items[0]
    assert "original" in first
    assert "recommended" in first
    assert "reason" in first
    assert "Worked on" not in first["recommended"] or "Developed" in first["recommended"]


def test_analyze_achievements_and_metrics():
    text_without_metrics = "Developed backend microservices. Designed REST API endpoints. Handled database integration."
    score, suggestions = analyze_achievements_and_metrics(text_without_metrics)

    assert score < 60.0
    assert len(suggestions) > 0
    assert "[X%]" in suggestions[0]["suggestion"] or "[X]" in suggestions[0]["suggestion"]


def test_analyze_grammar_and_tense():
    bad_grammar_text = "I am worked in Python development. Develop application and managed APIs."
    score, corrections = analyze_grammar_and_tense(bad_grammar_text)

    assert len(corrections) > 0
    assert any(c["corrected"] == "I worked" for c in corrections) or any("Developed" in c["corrected"] for c in corrections)


def test_analyze_formatting():
    no_bullets_text = "Worked on backend microservices and handled database schemas. Also integrated REST APIs."
    score, suggestions = analyze_formatting(no_bullets_text)

    assert len(suggestions) > 0
    assert any("bullet points" in s.lower() for s in suggestions)
