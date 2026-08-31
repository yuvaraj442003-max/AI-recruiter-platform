"""
test_resume_skill_matching.py — tests resume extraction and skill matching for candidate applications.
"""
from app.nlp.skill_extractor import extract_skills
from app.nlp.skills_data import get_all_skill_variants
from app.services.ats_scoring_service import calculate_job_specific_ats, normalize_skill

from app.models.candidate import CandidateProfile, CandidateSkill, Skill
from app.models.job import Job, JobSkill, JobStatus


def test_frontend_developer_skill_extraction():
    resume_text = """
    Jane Doe
    Frontend Developer
    Email: jane.doe@example.com | Phone: +1 555-0199
    Summary: Experienced Frontend Engineer specializing in building responsive web apps with HTML5, CSS3, JavaScript (ES6+), and React.js.
    Technical Skills:
    - Web Technologies: HTML5, CSS3, JavaScript, React.js, Tailwind CSS, TypeScript
    - Tools & Version Control: Git, VS Code, Webpack
    Experience:
    Frontend Developer at Tech Corp (2021 - Present)
    - Developed UI components using React.js and CSS3.
    """
    extracted = extract_skills(resume_text)

    # Check canonical extracted skills
    assert "HTML" in extracted
    assert "CSS" in extracted
    assert "JavaScript" in extracted
    assert "React.js" in extracted or "React" in extracted
    assert "TypeScript" in extracted
    assert "Git" in extracted


def test_bidirectional_variant_matching():
    # Test HTML5 <-> HTML
    html_variants = get_all_skill_variants("HTML5")
    assert "html" in html_variants
    assert "html5" in html_variants

    # Test CSS3 <-> CSS
    css_variants = get_all_skill_variants("CSS3")
    assert "css" in css_variants
    assert "css3" in css_variants

    # Test React.js <-> React
    react_variants = get_all_skill_variants("React.js")
    assert "react" in react_variants
    assert "react.js" in react_variants
    assert "reactjs" in react_variants

    # Test JavaScript <-> JS
    js_variants = get_all_skill_variants("JavaScript")
    assert "javascript" in js_variants
    assert "js" in js_variants


def test_job_application_skill_matching_ats():
    # Setup candidate profile
    candidate = CandidateProfile(
        id="cand-1234",
        resume_text="Frontend Developer with expertise in HTML, CSS, JavaScript, React.js, and Redux.",
        summary="Building web apps using HTML5, CSS3, JavaScript, and React.",
        work_experience="Built responsive interfaces using HTML5, CSS3, JS, React.js",
        experience_years=3.5,
        education="Bachelor of Science in Computer Science",
        location="New York",
    )

    # Setup Job requiring HTML5, CSS3, JavaScript, React.js
    skill_html = Skill(id=1, skill_name="HTML5", category="Frontend")
    skill_css = Skill(id=2, skill_name="CSS3", category="Frontend")
    skill_js = Skill(id=3, skill_name="JavaScript", category="Programming")
    skill_react = Skill(id=4, skill_name="React.js", category="Frontend")

    job = Job(
        id="job-5678",
        title="Frontend Developer",
        description="Looking for a Frontend Developer skilled in HTML5, CSS3, JavaScript, and React.js.",
        experience_required=2.0,
        location="New York",
        job_skills=[
            JobSkill(skill=skill_html, required=True),
            JobSkill(skill=skill_css, required=True),
            JobSkill(skill=skill_js, required=True),
            JobSkill(skill=skill_react, required=True),
        ]
    )

    result = calculate_job_specific_ats(candidate, job)

    matched = result["matched_skills"]
    missing = result["missing_skills"]
    score_breakdown = result["score_breakdown"]

    # All required skills should match
    assert "HTML" in matched or "HTML5" in matched
    assert "CSS" in matched or "CSS3" in matched
    assert "JavaScript" in matched
    assert "React" in matched or "React.js" in matched
    assert score_breakdown["skills"] == 100.0
