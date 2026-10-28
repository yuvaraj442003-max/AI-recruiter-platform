"""
test_portfolio.py — Comprehensive tests for Portfolio Builder module.
Tests:
- Portfolio generation from candidate profile
- AI section improvements (headline, about, project, experience, skills)
- Theme switching across 8 themes
- Customization options (colors, fonts, background, button style, card style)
- Live slug checking, publish, unpublish
- Public portfolio view and security filtering (no sensitive data leakage)
- Recruiter viewing candidate portfolio
"""
import pytest
from app.models.user import User, UserRole
from app.models.candidate import CandidateProfile, Skill, CandidateSkill
from app.models.portfolio import Portfolio
from app.core.security import hash_password, create_access_token
from app.services.portfolio_service import build_portfolio_from_candidate_profile


import uuid

@pytest.fixture
def test_candidate(db_session):
    u_id = uuid.uuid4().hex[:8]
    # Create user
    user = User(
        email=f"cand_{u_id}@example.com",
        password_hash=hash_password("Password123!"),
        name="Jane Doe",
        role=UserRole.candidate,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    # Create candidate profile
    profile = CandidateProfile(
        user_id=user.id,
        current_role="Senior Full Stack Engineer",
        experience_years=5.0,
        summary="Experienced engineer building scalable cloud systems.",
        education="B.S. in Computer Science",
        portfolio_url="https://janedoe.dev",
        linkedin_url="https://linkedin.com/in/janedoe",
        github_url="https://github.com/janedoe",
    )
    db_session.add(profile)
    db_session.flush()

    for s_name in ["Python", "FastAPI", "React", "Docker", "PostgreSQL"]:
        skill = db_session.query(Skill).filter_by(skill_name=s_name).first()
        if not skill:
            skill = Skill(skill_name=s_name)
            db_session.add(skill)
            db_session.flush()
        db_session.add(CandidateSkill(candidate_id=profile.id, skill_id=skill.id))

    db_session.commit()
    db_session.refresh(user)
    db_session.refresh(profile)

    portfolio = build_portfolio_from_candidate_profile(db_session, profile)
    token = create_access_token(subject=str(user.id), role=user.role.value)
    return {"user": user, "profile": profile, "token": token, "portfolio": portfolio}


@pytest.fixture
def test_recruiter(db_session):
    u_id = uuid.uuid4().hex[:8]
    user = User(
        email=f"recruiter_{u_id}@example.com",
        password_hash=hash_password("Password123!"),
        name="Bob Recruiter",
        role=UserRole.recruiter,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(subject=str(user.id), role=user.role.value)
    return {"user": user, "token": token}


def test_generate_portfolio_from_profile(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}
    response = client.post(
        "/api/v1/portfolio/generate",
        data={"use_existing_resume": "true"},
        headers=headers,
    )
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    data = res_data["data"]
    assert data["candidate_name"] == "Jane Doe"
    assert "Full Stack" in data["professional_headline"]
    assert len(data["skills"]) > 0
    assert data["theme_id"] in ["modern", "developer"] or "tech" in data["theme_id"] or "dev" in data["theme_id"]


def test_get_and_update_portfolio_me(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}
    # Fetch
    get_res = client.get("/api/v1/portfolio/me", headers=headers)
    assert get_res.status_code == 200
    data = get_res.json()["data"]

    # Update
    update_payload = {
        "candidate_name": "Jane Doe Updated",
        "professional_headline": "Lead AI Architect | Distributed Systems",
        "about": "Updated about text with full accuracy.",
        "skills": ["Python", "FastAPI", "Kubernetes", "PyTorch"],
    }
    put_res = client.put("/api/v1/portfolio/me", json=update_payload, headers=headers)
    assert put_res.status_code == 200
    updated = put_res.json()["data"]
    assert updated["candidate_name"] == "Jane Doe Updated"
    assert updated["professional_headline"] == "Lead AI Architect | Distributed Systems"
    assert updated["about"] == "Updated about text with full accuracy."
    assert "Kubernetes" in updated["skills"]


def test_switch_all_eight_themes(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}
    themes = ["modern", "minimal", "creative", "corporate", "developer", "ai_tech", "dark", "elegant"]

    for theme in themes:
        res = client.put("/api/v1/portfolio/theme", json={"theme_id": theme}, headers=headers)
        assert res.status_code == 200
        assert res.json()["data"]["theme_id"] == theme

    # Check that switching themes did NOT alter content
    me_res = client.get("/api/v1/portfolio/me", headers=headers)
    assert me_res.json()["data"]["theme_id"] == "elegant"
    assert me_res.json()["data"]["candidate_name"] == "Jane Doe"


def test_customize_portfolio(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}
    customize_payload = {
        "primary_color": "#10b981",
        "secondary_color": "#6366f1",
        "font": "Fira Code",
        "dark_mode": True,
        "background_style": "grid",
        "button_style": "pill",
        "card_style": "bordered",
        "section_order": ["home", "skills", "projects", "experience", "about", "contact"],
        "section_visibility": {"home": True, "skills": True, "services": False},
    }
    res = client.put("/api/v1/portfolio/customize", json=customize_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["primary_color"] == "#10b981"
    assert data["font"] == "Fira Code"
    assert data["dark_mode"] is True
    assert data["button_style"] == "pill"
    assert data["card_style"] == "bordered"
    assert data["section_visibility"]["services"] is False


def test_ai_section_improvements(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}

    # 1. AI Headline options
    res_head = client.post("/api/v1/portfolio/generate-headline", headers=headers)
    assert res_head.status_code == 200
    headlines = res_head.json()["data"]["headlines"]
    assert len(headlines) >= 3

    # 2. AI Improve About Me
    res_about = client.post(
        "/api/v1/portfolio/improve-about",
        json={"about_text": "I build backend systems and APIs in Python."},
        headers=headers,
    )
    assert res_about.status_code == 200
    assert len(res_about.json()["data"]["improved_about"]) > 20

    # 3. AI Improve Project
    res_proj = client.post(
        "/api/v1/portfolio/improve-project",
        json={
            "project_item": {
                "name": "Cloud Platform",
                "description": "Built cloud backend with FastAPI and Docker",
                "technologies": ["Python", "FastAPI", "Docker"],
            }
        },
        headers=headers,
    )
    assert res_proj.status_code == 200
    proj_data = res_proj.json()["data"]
    assert "improved_project" in proj_data

    # 4. AI Organize Skills
    res_skills = client.post(
        "/api/v1/portfolio/organize-skills",
        json={"skills": ["Python", "Docker", "PostgreSQL", "FastAPI", "React"]},
        headers=headers,
    )
    assert res_skills.status_code == 200
    categorized = res_skills.json()["data"]["categorized_skills"]
    assert isinstance(categorized, dict)
    assert len(categorized) > 0


def test_slug_management_and_publishing(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}

    # Check slug availability
    check_res = client.get("/api/v1/portfolio/check-slug?slug=jane-doe-engineer", headers=headers)
    assert check_res.status_code == 200
    assert check_res.json()["data"]["is_available"] is True

    # Update custom slug
    update_slug_res = client.put("/api/v1/portfolio/me", json={"slug": "jane-doe-engineer"}, headers=headers)
    assert update_slug_res.status_code == 200
    assert update_slug_res.json()["data"]["slug"] == "jane-doe-engineer"

    # Publish portfolio
    pub_res = client.post("/api/v1/portfolio/publish", headers=headers)
    assert pub_res.status_code == 200
    pub_data = pub_res.json()["data"]
    assert pub_data["is_published"] is True
    assert pub_data["slug"] == "jane-doe-engineer"
    assert "/portfolio/jane-doe-engineer" in pub_data["public_url"]

    # Public access
    public_res = client.get("/api/v1/portfolio/public/jane-doe-engineer")
    assert public_res.status_code == 200
    pub_view = public_res.json()["data"]
    assert pub_view["is_published"] is True
    assert pub_view["candidate_name"] == "Jane Doe"
    # Verify sensitive data is NOT exposed
    assert "password" not in pub_view
    assert "hashed_password" not in pub_view
    assert "user_id" not in pub_view
    assert "candidate_id" not in pub_view

    # Unpublish
    unpub_res = client.post("/api/v1/portfolio/unpublish", headers=headers)
    assert unpub_res.status_code == 200
    assert unpub_res.json()["data"]["is_published"] is False

    # Public access should now be forbidden / not found
    public_res_after = client.get("/api/v1/portfolio/public/jane-doe-engineer")
    assert public_res_after.status_code == 404


def test_recruiter_view_candidate_portfolio(client, test_candidate, test_recruiter):
    cand_headers = {"Authorization": f"Bearer {test_candidate['token']}"}
    recruiter_headers = {"Authorization": f"Bearer {test_recruiter['token']}"}

    # Initially unpublished -> recruiter receives None data
    candidate_id = str(test_candidate["profile"].id)
    rec_view_unpub = client.get(f"/api/v1/portfolio/candidate/{candidate_id}", headers=recruiter_headers)
    assert rec_view_unpub.status_code == 200
    assert rec_view_unpub.json()["data"] is None

    # Publish portfolio
    client.post("/api/v1/portfolio/publish", json={"slug": "jane-doe-engineer"}, headers=cand_headers)

    # Recruiter can now view published portfolio
    rec_view_pub = client.get(f"/api/v1/portfolio/candidate/{candidate_id}", headers=recruiter_headers)
    assert rec_view_pub.status_code == 200
    assert rec_view_pub.json()["data"]["candidate_name"] == "Jane Doe"


def test_generate_services_and_metrics(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}

    # Test AI generation of services / value proposition pillars
    res_services = client.post("/api/v1/portfolio/generate-services", headers=headers)
    assert res_services.status_code == 200
    services_data = res_services.json()["data"]["services"]
    assert isinstance(services_data, list)
    assert len(services_data) >= 3
    assert "title" in services_data[0]
    assert "description" in services_data[0]

    # Test AI generation of impact metrics & KPIs
    res_metrics = client.post("/api/v1/portfolio/generate-metrics", headers=headers)
    assert res_metrics.status_code == 200
    metrics_data = res_metrics.json()["data"]["metrics"]
    assert isinstance(metrics_data, list)
    assert len(metrics_data) == 4
    assert "value" in metrics_data[0]
    assert "title" in metrics_data[0]

    # Test saving services and achievements
    custom_achievements = [
        {"type": "metric", "title": "Production Uptime", "value": "99.99%", "description": "High reliability", "icon": "⚡"},
        {"type": "testimonial", "author": "Alice Boss", "role": "VP Eng", "company": "Tech Corp", "quote": "Remarkable delivery", "rating": 5}
    ]
    update_res = client.put(
        "/api/v1/portfolio/me",
        json={
            "services": services_data,
            "achievements": custom_achievements,
        },
        headers=headers,
    )
    assert update_res.status_code == 200
    saved_data = update_res.json()["data"]
    assert len(saved_data["services"]) >= 3
    assert len(saved_data["achievements"]) == 2


def test_portfolio_uses_resume_email_address_over_account_email(client, db_session):
    u_id = uuid.uuid4().hex[:8]
    user = User(
        email=f"account_login_{u_id}@gmail.com",
        password_hash=hash_password("Password123!"),
        name="Kumaresan T",
        role=UserRole.candidate,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    resume_text_content = """Kumaresan T
Full Stack Developer (MERN)
Phone: +91 7339004824 | Email: tkumaresantech@gmail.com
Salem, Tamil Nadu

Summary
Junior software developer with experience in React.js, Node.js, Express.js and MongoDB.

Skills
React.js, Node.js, Express.js, MongoDB, JavaScript
"""

    profile = CandidateProfile(
        user_id=user.id,
        current_role="Full Stack Developer",
        resume_text=resume_text_content,
        phone="+91 7339004824",
        location="Salem",
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)
    db_session.refresh(profile)

    # Generate portfolio from candidate profile with resume
    portfolio = build_portfolio_from_candidate_profile(db_session, profile)
    token = create_access_token(subject=str(user.id), role=user.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/portfolio/me", headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]

    # Verify that the resume's email address is used, NOT the account login email
    assert data["social_links"]["email"] == "tkumaresantech@gmail.com"
    assert data["social_links"]["email"] != user.email


def test_delete_portfolio_endpoint(client, test_candidate):
    headers = {"Authorization": f"Bearer {test_candidate['token']}"}

    # Verify portfolio exists initially
    get_res = client.get("/api/v1/portfolio/me", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"] is not None

    # Delete portfolio
    del_res = client.delete("/api/v1/portfolio/me", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Verify portfolio is now deleted / returns None
    get_after = client.get("/api/v1/portfolio/me", headers=headers)
    assert get_after.status_code == 200
    assert get_after.json()["data"] is None

    # Attempting to delete again returns 404
    del_again = client.delete("/api/v1/portfolio/me", headers=headers)
    assert del_again.status_code == 404


