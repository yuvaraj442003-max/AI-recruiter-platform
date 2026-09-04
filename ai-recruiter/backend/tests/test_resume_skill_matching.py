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


def test_no_javascript_no_false_positive_skill_extraction():
    resume_no_js = """
    John Doe
    Python Backend Engineer
    Email: john@example.com
    Summary: Dedicated software engineer looking for the next step in my career. Passionate about collaborating with the rest of the team to express innovative ideas.
    Experience:
    Backend Developer at Cloud Tech
    - Built microservices using Python, FastAPI, and PostgreSQL.
    - Used Docker for containerization and Git for version control.
    - Always willing to go above and beyond for project deliverables.
    Skills: Python, FastAPI, PostgreSQL, Docker, Git
    """
    extracted = extract_skills(resume_no_js)

    assert "JavaScript" not in extracted
    assert "Express.js" not in extracted
    assert "REST API" not in extracted
    assert "Go" not in extracted
    assert "Next.js" not in extracted
    assert "Python" in extracted
    assert "Docker" in extracted
    assert "PostgreSQL" in extracted


def test_job_matching_candidate_without_javascript():
    skill_py = Skill(id=1, skill_name="Python", category="Programming")
    skill_js = Skill(id=2, skill_name="JavaScript", category="Programming")

    candidate = CandidateProfile(
        id="cand-py",
        resume_text="Backend Engineer specializing in Python, PostgreSQL, and Docker.",
        summary="Python microservices developer.",
        work_experience="Developed Python microservices.",
        experience_years=3.0,
        candidate_skills=[
            CandidateSkill(skill=skill_py)
        ]
    )

    job_js_req = Job(
        id="job-js",
        title="Full Stack Developer",
        description="Looking for JavaScript and Python developer.",
        experience_required=2.0,
        job_skills=[
            JobSkill(skill=skill_js, required=True),
            JobSkill(skill=skill_py, required=True),
        ]
    )

    result = calculate_job_specific_ats(candidate, job_js_req)

    assert "JavaScript" in result["missing_skills"]
    assert "JavaScript" not in result["matched_skills"]
    assert "Python" in result["matched_skills"]
    assert result["score_breakdown"]["skills"] == 50.0


def test_react_js_as_individual_skill():
    # 1. Extraction Test: Resume containing both JavaScript and React.js extracts both distinct skills
    resume_text = "Frontend Developer skilled in JavaScript (ES6+), React.js, and HTML5."
    extracted = extract_skills(resume_text)
    assert "React.js" in extracted
    assert "JavaScript" in extracted

    # 2. ATS Score Matching Test: Job requires React.js and JavaScript separately
    skill_js = Skill(id=1, skill_name="JavaScript", category="Programming")
    skill_react = Skill(id=2, skill_name="React.js", category="Frontend")

    candidate_with_react = CandidateProfile(
        id="cand-react",
        resume_text=resume_text,
        summary="Building UI with JavaScript and React.js",
        work_experience="Developed Web Apps using React.js and JavaScript",
        experience_years=3.0,
    )

    job_react_req = Job(
        id="job-react",
        title="React Developer",
        description="Looking for a Frontend Engineer with strong React.js and JavaScript skills.",
        experience_required=2.0,
        job_skills=[
            JobSkill(skill=skill_js, required=True),
            JobSkill(skill=skill_react, required=True),
        ]
    )

    res = calculate_job_specific_ats(candidate_with_react, job_react_req)

    assert "React.js" in res["matched_skills"]
    assert "JavaScript" in res["matched_skills"]
    assert res["score_breakdown"]["skills"] == 100.0

    # 3. Candidate with JavaScript BUT NOT React.js has React.js listed in missing_skills
    candidate_js_only = CandidateProfile(
        id="cand-js-only",
        resume_text="Developer experienced in JavaScript, HTML5, CSS3.",
        summary="Vanilla JavaScript frontend developer.",
        work_experience="Built websites using JavaScript.",
        experience_years=2.0,
    )

    res_js_only = calculate_job_specific_ats(candidate_js_only, job_react_req)

    assert "JavaScript" in res_js_only["matched_skills"]
    assert "React.js" in res_js_only["missing_skills"]
    assert "React.js" not in res_js_only["matched_skills"]
    assert res_js_only["score_breakdown"]["skills"] == 50.0


def test_react_js_does_not_infer_javascript_if_not_present():
    from app.nlp.skill_extractor import extract_skills

    resume_text_react = "SKILLS\nReact.js, Node.js, Python, HTML, CSS"
    skills = extract_skills(resume_text_react)
    assert "React.js" in skills
    assert "JavaScript" not in skills

    resume_text_react_js_spaced = "TECHNICAL SKILLS\nReact JS, Python, Azure, REST API"
    skills_spaced = extract_skills(resume_text_react_js_spaced)
    assert "React.js" in skills_spaced
    assert "JavaScript" not in skills_spaced

    resume_text_with_both = "TECHNICAL SKILLS\nJavaScript, React JS, Python"
    skills_both = extract_skills(resume_text_with_both)
    assert "React.js" in skills_both
    assert "JavaScript" in skills_both


