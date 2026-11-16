from pathlib import Path
"""
portfolio.py — FastAPI Router endpoints for Candidate Portfolio Generator & Public Display.
Enforces candidate authentication & ownership for all modifications.
Only publishes safe candidate data for the public URL endpoint.
"""
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session, joinedload

from app.nlp.resume_parser import extract_resume_text
from app.nlp.skill_extractor import parse_resume_fields
from app.ai.portfolio_ai_service import (
    extract_structured_portfolio_data,
    generate_headline_options,
    generate_impact_metrics,
    generate_value_services,
    improve_about_text,
    improve_experience_item,
    improve_project_item,
    organize_skills_into_categories,
)
from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import BadRequestError, NotFoundError, PermissionDeniedError
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.portfolio import Portfolio
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.portfolio import (
    CandidateDetailsVerificationResponse,
    CheckSlugResponse,
    GeneratePortfolioCodeRequest,
    GeneratePortfolioCodeResponse,
    HeadlineGenerateRequest,
    HeadlineGenerateResponse,
    ImproveAboutRequest,
    ImproveAboutResponse,
    ImproveExperienceRequest,
    ImproveExperienceResponse,
    ImproveProjectRequest,
    ImproveProjectResponse,
    OrganizeSkillsRequest,
    OrganizeSkillsResponse,
    PortfolioCustomizeUpdateRequest,
    PortfolioResponse,
    PortfolioThemeUpdateRequest,
    PortfolioUpdateRequest,
    PromptGenerateRequest,
    PublicPortfolioResponse,
    RefineSectionRequest,
)
from app.ai.portfolio_prompt_service import (
    generate_portfolio_from_prompt,
    generate_portfolio_html_code_with_gemini,
    refine_portfolio_section,
)
from app.services.portfolio_service import (
    DOMAIN_BACKGROUND_PRESETS,
    build_portfolio_from_candidate_profile,
    format_portfolio_dict,
    get_candidate_portfolio,
    get_public_portfolio,
    is_slug_available,
    publish_candidate_portfolio,
    sanitize_slug,
    unpublish_candidate_portfolio,
    update_candidate_portfolio,
)

router = APIRouter(prefix="/portfolio", tags=["Portfolio Builder"])


def _get_or_create_candidate_profile(db: Session, current_user: User) -> CandidateProfile:
    """Finds candidate profile or creates initial profile record for user."""
    cand = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )
    if not cand:
        cand = CandidateProfile(
            user_id=current_user.id,
            headline=None,
            current_role=None,
            summary=None,
        )
        db.add(cand)
        db.commit()
        db.refresh(cand)
    return cand


@router.post("/generate", response_model=APIResponse[PortfolioResponse])
async def generate_portfolio_endpoint(
    theme_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Generates or updates candidate's portfolio.
    Reuses existing candidate resume/profile if no file uploaded.
    If resume file (PDF/DOCX) is uploaded, parses file and updates portfolio.
    """
    cand = _get_or_create_candidate_profile(db, current_user)

    file_bytes = None
    filename = None
    if file:
        file_bytes = await file.read()
        filename = file.filename
        from app.services.resume_service import process_resume
        cand = process_resume(db, current_user.id, file_bytes, filename)

    portfolio = build_portfolio_from_candidate_profile(
        db=db,
        candidate=cand,
        theme_id=theme_id,
        file_bytes=file_bytes,
        filename=filename,
    )

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(
        success=True,
        message="Portfolio generated successfully from candidate profile",
        data=PortfolioResponse(**data),
    )


@router.get("/verify-candidate-details", response_model=APIResponse[CandidateDetailsVerificationResponse])
def verify_candidate_details_endpoint(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Validates and extracts candidate's authentic information prior to portfolio generation.
    Checks name, headline, contact email, location, core skills, experience, and education.
    """
    import json
    cand = _get_or_create_candidate_profile(db, current_user)
    
    # 1. Candidate Full Name
    raw_name = (cand.full_name or current_user.name or "").strip()

    # 2. Headline / Role
    headline = (cand.headline or cand.current_role or "").strip()
    
    # 3. Email & Phone & Location
    email = (cand.resume_email or current_user.email or "").strip()
    phone = (cand.phone or "").strip()
    location = (cand.location or "").strip()
    summary = (cand.summary or cand.ai_summary or "").strip()

    # 4. Skills
    skills = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill] if cand.candidate_skills else []

    # 5. Extract structured data from resume or portfolio if available
    raw_text = cand.resume_text or ""
    if not raw_text and cand.resume_path and os.path.exists(cand.resume_path):
        try:
            with open(cand.resume_path, "rb") as f:
                raw_text = extract_resume_text(f.read(), os.path.basename(cand.resume_path))
        except Exception:
            pass

    extracted = {}
    if raw_text:
        try:
            parsed_fields = parse_resume_fields(raw_text)
            extracted = extract_structured_portfolio_data(raw_text, parsed_fields)
        except Exception:
            pass

    if (not raw_name or raw_name.lower() in ("candidate", "user")) and extracted.get("name"):
        raw_name = extracted.get("name").strip()
    if not headline and extracted.get("professional_headline"):
        headline = extracted.get("professional_headline").strip()
    if not skills and extracted.get("skills"):
        s_val = extracted.get("skills")
        if isinstance(s_val, dict):
            skills = [item for sub in s_val.values() for item in (sub if isinstance(sub, list) else [sub])]
        elif isinstance(s_val, list):
            skills = s_val
    if not summary and extracted.get("about"):
        summary = extracted.get("about").strip()

    experience = extracted.get("experience") or []
    projects = extracted.get("projects") or []
    education = extracted.get("education") or []
    certifications = extracted.get("certifications") or []

    # Also check if existing portfolio has details
    portfolio = get_candidate_portfolio(db, cand.id)
    if portfolio:
        if (not raw_name or raw_name.lower() in ("candidate", "user")) and portfolio.candidate_name:
            raw_name = portfolio.candidate_name.strip()
        if not headline and portfolio.professional_headline:
            headline = portfolio.professional_headline.strip()
        if not summary and portfolio.about:
            summary = portfolio.about.strip()
        if not skills and portfolio.skills:
            try:
                ps = json.loads(portfolio.skills)
                if isinstance(ps, dict):
                    skills = [item for sub in ps.values() for item in (sub if isinstance(sub, list) else [sub])]
                elif isinstance(ps, list):
                    skills = ps
            except Exception:
                pass
        if not experience and portfolio.experience:
            try:
                experience = json.loads(portfolio.experience)
            except Exception:
                pass
        if not projects and portfolio.projects:
            try:
                projects = json.loads(portfolio.projects)
            except Exception:
                pass
        if not education and portfolio.education:
            try:
                education = json.loads(portfolio.education)
            except Exception:
                pass
        if not certifications and portfolio.certifications:
            try:
                certifications = json.loads(portfolio.certifications)
            except Exception:
                pass

    # Issues checklist
    issues = []
    score = 100
    if not raw_name or raw_name.lower() in ("candidate", "user", "anonymous"):
        issues.append("Candidate full name is required.")
        score -= 30
    if not headline:
        issues.append("Professional headline or target role is required.")
        score -= 25
    if not email or "@" not in email:
        issues.append("Valid contact email address is required.")
        score -= 20
    if not skills:
        issues.append("At least 1-2 core technical skills must be provided.")
        score -= 15
    if not experience and not projects:
        score -= 10

    is_valid = len(issues) == 0

    return APIResponse(
        success=True,
        message="Candidate details verified" if is_valid else "Candidate details require verification before generation",
        data=CandidateDetailsVerificationResponse(
            is_valid=is_valid,
            candidate_name=raw_name or (current_user.name if current_user.name and current_user.name.lower() not in ("candidate", "user") else "Candidate"),
            professional_headline=headline or (cand.target_role or "Software Engineer & Technologist"),
            email=email or current_user.email,
            phone=phone or cand.phone,
            location=location or cand.location or "Global / Remote",
            summary=summary,
            skills=skills,
            experience=experience if isinstance(experience, list) else [],
            projects=projects if isinstance(projects, list) else [],
            education=education if isinstance(education, list) else [],
            certifications=certifications if isinstance(certifications, list) else [],
            has_resume=bool(cand.resume_path or cand.resume_text),
            validation_score=max(0, score),
            validation_issues=issues,
        ),
    )


@router.post("/generate-from-prompt", response_model=APIResponse[PortfolioResponse])
def generate_portfolio_from_prompt_endpoint(
    payload: PromptGenerateRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Creates or updates candidate portfolio based on natural language prompt instructions
    powered by Gemini AI. Enforces candidate details validation prior to generation.
    """
    import json
    cand = _get_or_create_candidate_profile(db, current_user)

    candidate_context = None
    if payload.include_resume and cand:
        raw_text = cand.resume_text or ""
        if not raw_text and cand.resume_path and os.path.exists(cand.resume_path):
            try:
                with open(cand.resume_path, "rb") as f:
                    raw_text = extract_resume_text(f.read(), os.path.basename(cand.resume_path))
            except Exception:
                pass
        
        parsed_fields = parse_resume_fields(raw_text) if raw_text else {}
        extracted = extract_structured_portfolio_data(raw_text, parsed_fields) if raw_text else {}

        resume_name = extracted.get("name") or (cand.full_name if cand else current_user.name) or "Candidate"
        candidate_context = {
            "name": resume_name,
            "headline": extracted.get("professional_headline") or cand.headline or cand.current_role or "",
            "skills": [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill] if cand.candidate_skills else list(extracted.get("skills", {}).values()),
            "summary": extracted.get("about") or cand.summary or cand.ai_summary or "",
            "experience": extracted.get("experience") or [],
            "projects": extracted.get("projects") or [],
            "education": extracted.get("education") or [],
            "certifications": extracted.get("certifications") or [],
            "metrics": extracted.get("achievements") or [],
            "resume_text": raw_text[:2500] if raw_text else "",
        }

    # Apply and persist verified candidate data if submitted
    v_data = payload.verified_candidate_data or {}
    if v_data and isinstance(v_data, dict):
        v_name = (v_data.get("name") or v_data.get("candidate_name") or "").strip()
        v_headline = (v_data.get("headline") or v_data.get("professional_headline") or "").strip()
        v_email = (v_data.get("email") or "").strip()
        v_location = (v_data.get("location") or "").strip()
        v_skills = v_data.get("skills") or []
        v_summary = (v_data.get("summary") or "").strip()

        if v_name and v_name.lower() not in ("candidate", "user", "anonymous"):
            cand._full_name = v_name
            current_user.name = v_name
        if v_headline:
            cand.headline = v_headline
            cand.current_role = v_headline
        if v_email:
            cand.resume_email = v_email
        if v_location:
            cand.location = v_location
        if v_summary:
            cand.summary = v_summary

        if not candidate_context:
            candidate_context = {}
        if v_name: candidate_context["name"] = v_name
        if v_headline: candidate_context["headline"] = v_headline
        if v_location: candidate_context["location"] = v_location
        if v_summary: candidate_context["summary"] = v_summary
        if v_skills and isinstance(v_skills, list):
            candidate_context["skills"] = v_skills

        db.commit()

    # Strict Validation Check: Ensure candidate name and headline are valid before generating
    verified_name = (candidate_context.get("name") if candidate_context else (cand.full_name or current_user.name)) or ""
    verified_headline = (candidate_context.get("headline") if candidate_context else (cand.headline or cand.current_role)) or ""
    if not verified_name.strip() or verified_name.strip().lower() in ("candidate", "user", "anonymous"):
        raise BadRequestError("Candidate details verification failed: Candidate full name is required before generating portfolio. Please verify candidate details.")
    if not verified_headline.strip():
        # Fallback to sensible professional default
        if not candidate_context:
            candidate_context = {}
        candidate_context["headline"] = cand.target_role or "Software Engineer & Technologist"

    # Fetch previous portfolio if refinement mode
    portfolio = get_candidate_portfolio(db, cand.id)
    prev_dict = format_portfolio_dict(portfolio, public_only=False, db=db) if portfolio else None

    # Generate with Gemini AI
    gen_data = generate_portfolio_from_prompt(
        prompt=payload.prompt,
        candidate_name=verified_name,
        candidate_context=candidate_context,
        previous_portfolio=prev_dict,
        is_refinement=payload.refinement,
    )

    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(
            db=db,
            candidate=cand,
            theme_id=gen_data.get("theme_id", "modern"),
        )

    # Apply generated fields
    portfolio.theme_id = gen_data.get("theme_id", portfolio.theme_id or "modern")
    portfolio.primary_color = gen_data.get("primary_color", portfolio.primary_color or "#4f46e5")
    portfolio.secondary_color = gen_data.get("secondary_color", portfolio.secondary_color or "#06b6d4")
    portfolio.font = gen_data.get("font", portfolio.font or "Plus Jakarta Sans")
    portfolio.background_style = gen_data.get("background_style", portfolio.background_style or "mesh")
    if "background_image" in gen_data and gen_data["background_image"] is not None:
        portfolio.background_image = gen_data["background_image"]
    if "custom_css" in gen_data and gen_data["custom_css"]:
        portfolio.custom_css = gen_data["custom_css"]
    elif "portrait_mask" in gen_data and gen_data["portrait_mask"]:
        portfolio.custom_css = json.dumps({"portrait_mask": gen_data["portrait_mask"]})
    if "custom_html" in gen_data and gen_data["custom_html"]:
        portfolio.custom_html = gen_data["custom_html"]
    portfolio.generation_prompt = payload.prompt
    portfolio.card_style = gen_data.get("card_style", portfolio.card_style or "glass")
    portfolio.button_style = gen_data.get("button_style", portfolio.button_style or "rounded")
    portfolio.dark_mode = bool(gen_data.get("dark_mode", portfolio.dark_mode))
    portfolio.layout = gen_data.get("layout", portfolio.layout or "modern")
    if "profile_image" in gen_data and gen_data["profile_image"]:
        portfolio.profile_image = gen_data["profile_image"]
    elif not portfolio.profile_image and cand and cand.profile_photo:
        portfolio.profile_image = cand.profile_photo

    portfolio.professional_headline = gen_data.get("professional_headline", portfolio.professional_headline)
    if "headline_options" in gen_data:
        portfolio.headline_options = json.dumps(gen_data["headline_options"])
    if "about" in gen_data:
        portfolio.about = gen_data["about"]
    if "skills" in gen_data:
        portfolio.skills = json.dumps(gen_data["skills"])
    if "projects" in gen_data:
        portfolio.projects = json.dumps(gen_data["projects"])
    if "experience" in gen_data:
        portfolio.experience = json.dumps(gen_data["experience"])
    if "education" in gen_data:
        portfolio.education = json.dumps(gen_data["education"])
    if "certifications" in gen_data:
        portfolio.certifications = json.dumps(gen_data["certifications"])
    if "services" in gen_data:
        portfolio.services = json.dumps(gen_data["services"])
    if "impact_metrics" in gen_data:
        portfolio.achievements = json.dumps(gen_data["impact_metrics"])
    if "social_links" in gen_data:
        portfolio.social_links = json.dumps(gen_data["social_links"])

    # Update slug if new slug suggested and available
    suggested = gen_data.get("suggested_slug")
    if suggested:
        clean = sanitize_slug(suggested)
        if clean and is_slug_available(db, clean, exclude_portfolio_id=portfolio.id):
            portfolio.slug = clean

    db.commit()
    db.refresh(portfolio)

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(
        success=True,
        message="Portfolio generated successfully with Gemini AI!",
        data=PortfolioResponse(**data),
    )


@router.post("/refine-section", response_model=APIResponse[PortfolioResponse])
def refine_section_endpoint(
    payload: RefineSectionRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Selectively refines or rewrites a single portfolio section using Gemini AI.
    """
    import json
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(db, cand)

    sec = payload.section.lower().strip()
    current_data = None
    if sec == "about":
        current_data = portfolio.about or ""
    elif sec in ("headline", "professional_headline"):
        current_data = portfolio.professional_headline or ""
    elif sec == "skills":
        try:
            current_data = json.loads(portfolio.skills) if portfolio.skills else {}
        except Exception:
            current_data = {}
    elif sec == "projects":
        try:
            current_data = json.loads(portfolio.projects) if portfolio.projects else []
        except Exception:
            current_data = []
    elif sec == "experience":
        try:
            current_data = json.loads(portfolio.experience) if portfolio.experience else []
        except Exception:
            current_data = []
    elif sec in ("metrics", "achievements"):
        try:
            current_data = json.loads(portfolio.achievements) if portfolio.achievements else []
        except Exception:
            current_data = []
    elif sec == "services":
        try:
            current_data = json.loads(portfolio.services) if portfolio.services else []
        except Exception:
            current_data = []

    refined = refine_portfolio_section(
        section=sec,
        instruction=payload.instruction,
        current_data=current_data,
        candidate_name=current_user.name or "Candidate",
    )

    if sec == "about":
        portfolio.about = refined if isinstance(refined, str) else str(refined)
    elif sec in ("headline", "professional_headline"):
        portfolio.professional_headline = refined if isinstance(refined, str) else str(refined)
    elif sec == "skills":
        portfolio.skills = json.dumps(refined) if not isinstance(refined, str) else refined
    elif sec == "projects":
        portfolio.projects = json.dumps(refined) if not isinstance(refined, str) else refined
    elif sec == "experience":
        portfolio.experience = json.dumps(refined) if not isinstance(refined, str) else refined
    elif sec in ("metrics", "achievements"):
        portfolio.achievements = json.dumps(refined) if not isinstance(refined, str) else refined
    elif sec == "services":
        portfolio.services = json.dumps(refined) if not isinstance(refined, str) else refined

    db.commit()
    db.refresh(portfolio)

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(
        success=True,
        message=f"Section '{payload.section}' refined successfully with Gemini AI!",
        data=PortfolioResponse(**data),
    )


@router.get("/me", response_model=APIResponse[Optional[PortfolioResponse]])
def get_my_portfolio_endpoint(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Fetches currently logged in candidate's portfolio."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        return APIResponse(success=True, message="No candidate profile created yet", data=None)

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        # Auto-build portfolio if candidate has resume or profile details
        if cand.resume_path or cand.resume_text or cand.headline or cand.college_name or cand.candidate_skills:
            try:
                portfolio = build_portfolio_from_candidate_profile(db=db, candidate=cand)
            except Exception as e:
                logger.warning(f"Auto-generating portfolio on GET /me failed: {e}")
        if not portfolio:
            return APIResponse(success=True, message="No portfolio generated yet", data=None)

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(success=True, message="Candidate portfolio retrieved", data=PortfolioResponse(**data))


@router.put("/me", response_model=APIResponse[PortfolioResponse])
def update_my_portfolio_endpoint(
    payload: PortfolioUpdateRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Updates candidate portfolio content, layout, styling, and custom slug."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(db, cand)

    update_dict = payload.model_dump(exclude_unset=True)
    portfolio = update_candidate_portfolio(db, portfolio, update_dict)

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(success=True, message="Portfolio updated successfully", data=PortfolioResponse(**data))

@router.post("/upload-profile-image", response_model=APIResponse[PortfolioResponse])
async def upload_profile_image_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Uploads or replaces candidate profile image / headshot.
    Validates file type (JPG/PNG/WEBP/GIF) and max 10MB size,
    saves into static /uploads/portfolios/ directory, and updates candidate portfolio.
    """
    cand = _get_or_create_candidate_profile(db, current_user)
    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(db, cand)

    filename = file.filename or "avatar.jpg"
    ext = Path(filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        ext = ".jpg"

    content_bytes = await file.read()
    if not content_bytes or len(content_bytes) < 50:
        raise BadRequestError("Uploaded image file is empty or invalid.")
    if len(content_bytes) > 10 * 1024 * 1024:
        raise BadRequestError("Profile image exceeds 10MB maximum limit.")

    upload_dir = Path(__file__).resolve().parent.parent.parent / "uploads" / "portfolios"
    upload_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"avatar_{cand.id}_{uuid.uuid4().hex[:8]}{ext}"
    dest_path = upload_dir / stored_name
    with open(dest_path, "wb") as f:
        f.write(content_bytes)

    img_url = f"/uploads/portfolios/{stored_name}"
    portfolio.profile_image = img_url
    if cand:
        cand.profile_photo = img_url

    db.commit()
    db.refresh(portfolio)

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(
        success=True,
        message="Profile image updated successfully!",
        data=PortfolioResponse(**data),
    )



@router.delete("/me", response_model=APIResponse[None])
def delete_my_portfolio_endpoint(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Deletes / resets candidate's portfolio."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        raise NotFoundError("No portfolio found to delete")

    if hasattr(cand, "portfolio_url") and cand.portfolio_url:
        cand.portfolio_url = None
        db.add(cand)

    db.delete(portfolio)
    db.commit()
    return APIResponse(success=True, message="Portfolio deleted successfully", data=None)


@router.post("/publish", response_model=APIResponse[PortfolioResponse])
def publish_my_portfolio_endpoint(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Publishes candidate's portfolio and activates public URL."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(db, cand)

    portfolio = publish_candidate_portfolio(db, portfolio)
    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(success=True, message="Portfolio published successfully! URL is now live.", data=PortfolioResponse(**data))


@router.post("/unpublish", response_model=APIResponse[PortfolioResponse])
def unpublish_my_portfolio_endpoint(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Unpublishes candidate's portfolio and deactivates public URL."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        raise NotFoundError("No portfolio found")

    portfolio = unpublish_candidate_portfolio(db, portfolio)
    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(success=True, message="Portfolio unpublished. Public URL is now inactive.", data=PortfolioResponse(**data))


@router.put("/theme", response_model=APIResponse[PortfolioResponse])
def update_portfolio_theme_endpoint(
    payload: PortfolioThemeUpdateRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Switches active theme without altering candidate portfolio data."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(db, cand, theme_id=payload.theme_id)
    else:
        portfolio = update_candidate_portfolio(db, portfolio, {"theme_id": payload.theme_id})

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(success=True, message=f"Theme switched to '{payload.theme_id}' successfully", data=PortfolioResponse(**data))


@router.put("/customize", response_model=APIResponse[PortfolioResponse])
def customize_portfolio_endpoint(
    payload: PortfolioCustomizeUpdateRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Updates visual customization tokens: colors, font, background, card style, button style, section order, visibility."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not cand:
        raise NotFoundError("Candidate profile not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio:
        portfolio = build_portfolio_from_candidate_profile(db, cand)

    update_dict = payload.model_dump(exclude_unset=True)
    portfolio = update_candidate_portfolio(db, portfolio, update_dict)

    data = format_portfolio_dict(portfolio, public_only=False, db=db)
    return APIResponse(success=True, message="Portfolio customization saved", data=PortfolioResponse(**data))


@router.post("/generate-headline", response_model=APIResponse[HeadlineGenerateResponse])
def generate_headline_endpoint(
    payload: Optional[HeadlineGenerateRequest] = None,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Generates 3-5 professional headline options for candidate selection."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    role = (payload.current_role if payload else None) or (cand.current_role if cand else None) or (cand.headline if cand else None) or ""
    skills = (payload.key_skills if payload and payload.key_skills else None) or ([cs.skill.skill_name for cs in cand.candidate_skills] if cand and cand.candidate_skills else [])
    exp_years = cand.experience_years if cand else 0.0

    headlines = generate_headline_options(
        candidate_name=current_user.name or "Candidate",
        current_role=role,
        skills=skills,
        experience_years=exp_years,
    )
    return APIResponse(success=True, message="Headline options generated", data=HeadlineGenerateResponse(headlines=headlines))


@router.post("/improve-about", response_model=APIResponse[ImproveAboutResponse])
def improve_about_endpoint(
    payload: ImproveAboutRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Improves candidate's About Me text preserving facts and core experience."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    skills = [cs.skill.skill_name for cs in cand.candidate_skills] if cand and cand.candidate_skills else []
    role = cand.current_role if cand else "Software Engineer"
    base_text = payload.about_text or (cand.summary if cand else "")

    improved = improve_about_text(
        original_text=base_text,
        candidate_name=current_user.name or "Candidate",
        role=role,
        skills=skills,
        tone=payload.tone or "professional",
    )
    return APIResponse(
        success=True,
        message="About Me improved successfully",
        data=ImproveAboutResponse(improved_about=improved, original_about=base_text, tone=payload.tone or "professional"),
    )


@router.post("/improve-experience", response_model=APIResponse[ImproveExperienceResponse])
def improve_experience_endpoint(
    payload: ImproveExperienceRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
):
    """Improves an experience entry with action verbs and impact phrasing."""
    improved = improve_experience_item(payload.experience_item)
    return APIResponse(
        success=True,
        message="Experience description improved",
        data=ImproveExperienceResponse(improved_experience=improved, original_experience=payload.experience_item),
    )


@router.post("/improve-project", response_model=APIResponse[ImproveProjectResponse])
def improve_project_endpoint(
    payload: ImproveProjectRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
):
    """Improves project description and key features."""
    improved = improve_project_item(payload.project_item)
    return APIResponse(
        success=True,
        message="Project details improved",
        data=ImproveProjectResponse(improved_project=improved, original_project=payload.project_item),
    )


@router.post("/organize-skills", response_model=APIResponse[OrganizeSkillsResponse])
def organize_skills_endpoint(
    payload: Optional[OrganizeSkillsRequest] = None,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Organizes skills into categories."""
    raw_skills: list[str] = []

    # 1. Check payload skills
    if payload and payload.skills is not None:
        if isinstance(payload.skills, list):
            raw_skills = [str(s).strip() for s in payload.skills if s and str(s).strip()]
        elif isinstance(payload.skills, dict):
            for v in payload.skills.values():
                if isinstance(v, list):
                    raw_skills.extend([str(s).strip() for s in v if s and str(s).strip()])
                elif isinstance(v, str) and v.strip():
                    raw_skills.append(v.strip())
        elif isinstance(payload.skills, str):
            raw_skills = [s.strip() for s in payload.skills.split(",") if s.strip()]

    # 2. If no skills passed from payload, check candidate's portfolio and profile
    if not raw_skills:
        cand = (
            db.query(CandidateProfile)
            .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
            .filter(CandidateProfile.user_id == current_user.id)
            .first()
        )
        if cand:
            portfolio = get_candidate_portfolio(db, cand.id)
            if portfolio and portfolio.skills:
                try:
                    p_skills = json.loads(portfolio.skills)
                    if isinstance(p_skills, list):
                        raw_skills = [str(s).strip() for s in p_skills if s]
                    elif isinstance(p_skills, dict):
                        for v in p_skills.values():
                            if isinstance(v, list):
                                raw_skills.extend([str(s).strip() for s in v if s])
                except Exception:
                    pass

            # 3. If still empty, check candidate_skills safely
            if not raw_skills and cand.candidate_skills:
                raw_skills = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill and cs.skill.skill_name]

            # 4. If still empty, check cand.skills column
            if not raw_skills and cand.skills:
                raw_skills = [s.strip() for s in cand.skills.split(",") if s.strip()]

            # 5. If still empty, extract from resume_text
            if not raw_skills and cand.resume_text:
                try:
                    from app.nlp.skill_extractor import extract_skills_from_text
                    extracted = extract_skills_from_text(cand.resume_text)
                    if extracted:
                        raw_skills = extracted
                except Exception:
                    pass

    # Deduplicate preserving order
    seen = set()
    clean_skills = []
    for s in raw_skills:
        s_clean = s.strip()
        if s_clean and s_clean.lower() not in seen:
            seen.add(s_clean.lower())
            clean_skills.append(s_clean)

    categorized = organize_skills_into_categories(clean_skills)
    return APIResponse(success=True, message="Skills organized into categories", data=OrganizeSkillsResponse(categorized_skills=categorized))


@router.get("/check-slug", response_model=APIResponse[CheckSlugResponse])
def check_slug_availability_endpoint(
    slug: str = Query(..., description="Slug to check"),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Validates if requested slug is available for publishing."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    portfolio = get_candidate_portfolio(db, cand.id) if cand else None
    exclude_id = portfolio.id if portfolio else None

    clean = sanitize_slug(slug)
    available = is_slug_available(db, clean, exclude_portfolio_id=exclude_id)
    msg = f"Slug '{clean}' is available!" if available else f"Slug '{clean}' is already in use or reserved."
    return APIResponse(success=True, message=msg, data=CheckSlugResponse(slug=clean, is_available=available, message=msg))


@router.get("/domain-backgrounds", response_model=APIResponse[Dict[str, Any]])
def get_domain_backgrounds_endpoint():
    """Returns curated professional domain background presets for candidate portfolios."""
    from app.services.portfolio_service import DOMAIN_BACKGROUND_PRESETS
    return APIResponse(success=True, message="Domain backgrounds retrieved successfully", data=DOMAIN_BACKGROUND_PRESETS)


@router.post("/generate-services")
def generate_services_endpoint(
    payload: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Generates 3 tailored value proposition pillars / services for candidate portfolio."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    role = (payload.get("role") if payload else None) or (cand.current_role if cand else None) or (cand.headline if cand else None) or ""
    skills = (payload.get("skills") if payload else None) or ([cs.skill.skill_name for cs in cand.candidate_skills] if cand and cand.candidate_skills else [])
    exp_years = cand.experience_years if cand else 0.0
    services = generate_value_services(role, skills, exp_years)
    return APIResponse(success=True, message="Services generated successfully", data={"services": services})


@router.post("/generate-metrics")
def generate_metrics_endpoint(
    payload: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Generates 4 quantified impact metrics / KPIs for candidate hero section grounded strictly in resume."""
    cand = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    role = (payload.get("role") if payload else None) or (cand.current_role if cand else None) or (cand.headline if cand else None) or ""
    skills = (payload.get("skills") if payload else None) or ([cs.skill.skill_name for cs in cand.candidate_skills] if cand and cand.candidate_skills else [])
    exp_years = cand.experience_years if cand else 0.0

    project_count = 0
    metrics_and_impact = []
    if cand and cand.resume_text:
        from app.nlp.skill_extractor import parse_projects_items, extract_metrics_and_impact
        proj_items = parse_projects_items(cand.resume_text)
        project_count = len(proj_items)
        metrics_and_impact = extract_metrics_and_impact(cand.resume_text)

    metrics = generate_impact_metrics(role, skills, exp_years, project_count=project_count, verified_metrics=metrics_and_impact)
    return APIResponse(success=True, message="Impact metrics generated successfully", data={"metrics": metrics})


@router.get("/domain-backgrounds", response_model=APIResponse[Dict[str, Any]])
def get_domain_backgrounds_endpoint():
    """Returns curated presets for domain-specific portfolio background images."""
    return APIResponse(
        success=True,
        message="Domain background presets retrieved successfully",
        data={"presets": DOMAIN_BACKGROUND_PRESETS}
    )


@router.get("/public/{slug}", response_model=APIResponse[PublicPortfolioResponse])
def get_public_portfolio_endpoint(
    slug: str,
    db: Session = Depends(get_db),
):
    """
    Public Portfolio Endpoint.
    Only accessible if portfolio is published (is_published == True).
    Never exposes internal IDs, passwords, tokens, ATS scores, or recruiter notes.
    """
    portfolio, cand_name = get_public_portfolio(db, slug)
    data = format_portfolio_dict(portfolio, public_only=True, db=db)
    return APIResponse(success=True, message="Public portfolio retrieved successfully", data=PublicPortfolioResponse(**data))


@router.get("/candidate/{candidate_id}", response_model=APIResponse[Optional[PublicPortfolioResponse]])
def get_recruiter_candidate_portfolio_endpoint(
    candidate_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """
    Recruiter endpoint to view a candidate's portfolio.
    Only returns portfolio data if the candidate has published it.
    """
    try:
        cand_uuid = uuid.UUID(candidate_id)
    except ValueError:
        raise BadRequestError("Invalid candidate ID format")

    cand = db.query(CandidateProfile).filter((CandidateProfile.id == cand_uuid) | (CandidateProfile.user_id == cand_uuid)).first()
    if not cand:
        raise NotFoundError("Candidate not found")

    portfolio = get_candidate_portfolio(db, cand.id)
    if not portfolio or not portfolio.is_published:
        return APIResponse(success=True, message="Candidate has no published portfolio", data=None)

    data = format_portfolio_dict(portfolio, public_only=True, db=db)
    return APIResponse(success=True, message="Candidate published portfolio", data=PublicPortfolioResponse(**data))
