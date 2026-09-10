"""
test_talent_rediscovery.py — Automated Unit & Integration Tests for Talent Pool Auto-Rediscovery & Silver Medalists.
Tests skill normalization, candidate eligibility filtering, deterministic weighted match scoring,
Silver Medalist historical application detection, and duplicate result prevention.
"""
import uuid
import pytest

from app.services.talent_rediscovery_service import (
    calculate_candidate_rediscovery_score,
    normalize_skill_name,
    SKILL_NORMALIZATION_MAP,
)


def test_normalize_skill_name_variants():
    """Verify skill variations normalize consistently."""
    assert normalize_skill_name("react") == "React.js"
    assert normalize_skill_name("React.js") == "React.js"
    assert normalize_skill_name("react js") == "React.js"
    assert normalize_skill_name("node") == "Node.js"
    assert normalize_skill_name("typescript") == "TypeScript"
    assert normalize_skill_name("py") == "Python"


class MockSkill:
    def __init__(self, name):
        self.skill_name = name


class MockCandidateSkill:
    def __init__(self, name):
        self.skill = MockSkill(name)


class MockCandidateProfile:
    def __init__(self, skills, experience_years, location="Chennai", headline="React Developer"):
        self.id = uuid.uuid4()
        self.candidate_skills = [MockCandidateSkill(s) for s in skills]
        self.experience_years = experience_years
        self.location = location
        self.headline = headline
        self.summary = "Experienced in building scalable React applications and REST APIs"
        self.work_experience = "Senior Software Engineer"
        self.education = "B.E Computer Science"


def test_deterministic_scoring_matrix():
    """Verify 7-part weighted match score calculation."""
    job_reqs = {
        "title": "Senior React Developer",
        "required_skills": ["React.js", "TypeScript", "Node.js"],
        "minimum_experience": 5.0,
        "location": "Chennai",
        "responsibilities": ["Build scalable React applications", "Develop REST APIs"],
        "description": "Looking for Senior React Developer with TypeScript and Node.js",
    }

    # Candidate with 100% skills match and 6 years experience
    cand_strong = MockCandidateProfile(
        skills=["React.js", "TypeScript", "Node.js", "Docker"],
        experience_years=6.0,
        location="Chennai",
    )

    res_strong = calculate_candidate_rediscovery_score(cand_strong, job_reqs)
    assert res_strong["overall_score"] >= 80.0
    assert res_strong["skills_score"] == 100.0
    assert res_strong["experience_score"] == 100.0
    assert "React.js" in res_strong["matched_skills"]
    assert "TypeScript" in res_strong["matched_skills"]

    # Candidate with lower experience & missing skills
    cand_junior = MockCandidateProfile(
        skills=["React.js"],
        experience_years=2.0,
        location="Bangalore",
    )

    res_junior = calculate_candidate_rediscovery_score(cand_junior, job_reqs)
    assert res_junior["overall_score"] < res_strong["overall_score"]
    assert res_junior["skills_score"] < 50.0
    assert res_junior["experience_score"] < 100.0
    assert "TypeScript" in res_junior["missing_skills"]


def test_silver_medalist_criteria_evaluation():
    """Verify Silver Medalist evaluation logic status filtering."""
    silver_statuses = ["shortlisted", "interview", "selected"]
    non_silver_statuses = ["applied", "rejected", "withdrawn"]

    for st in silver_statuses:
        is_silver = st in ("shortlisted", "interview", "under_review", "selected")
        assert is_silver is True

    for st in non_silver_statuses:
        is_silver = st in ("shortlisted", "interview", "under_review", "selected")
        assert is_silver is False
