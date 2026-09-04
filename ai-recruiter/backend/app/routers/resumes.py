"""
Resume endpoints: upload (candidate-only), and fetch the parsed profile.
"""
import io
import json
import os
import uuid
import zipfile
import hashlib
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Query, Form
from fastapi.responses import FileResponse, HTMLResponse, Response
from sqlalchemy.orm import Session, joinedload

from app.ai.resume_summarizer import generate_resume_summary
from app.core.database import get_db
from app.core.deps import require_role, oauth2_scheme, get_current_user
from app.core.exceptions import NotFoundError, AuthError, PermissionDeniedError, AppError
from app.core.security import decode_token
from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job
from app.models.user import User, UserRole
from app.nlp.resume_parser import extract_resume_text
from app.nlp.skill_extractor import parse_resume_fields
from app.schemas.candidate import CandidateProfileResponse, CandidateProfileUpdate
from app.schemas.common import APIResponse
from app.services.resume_service import (
    delete_candidate_profile,
    process_resume,
    save_uploaded_file,
    update_candidate_profile,
    _compute_profile_score,
    _sync_candidate_skills,
    seed_skills,
)
from app.utils.file_validation import secure_filename
from xhtml2pdf import pisa

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=APIResponse[CandidateProfileResponse])
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    file_bytes = await file.read()
    profile = process_resume(db, current_user.id, file_bytes, file.filename)

    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == profile.id)
        .first()
    )

    return APIResponse(
        success=True,
        message="Resume uploaded and parsed successfully",
        data=CandidateProfileResponse.from_profile(profile),
    )


def _save_and_store_bulk_resume(
    db: Session,
    file_bytes: bytes,
    filename: str,
    job_id_str: Optional[str] = None,
    custom_jd_data: Optional[dict] = None,
    recruiter_id: Optional[uuid.UUID] = None,
) -> dict:
    """Saves bulk resume to disk, checks for duplicates, creates/updates candidate User & Profile in DB, and evaluates ATS scores."""
    resume_hash = hashlib.sha256(file_bytes).hexdigest()
    file_path, safe_name = save_uploaded_file(file_bytes, filename)
    raw_text = extract_resume_text(file_bytes, filename)
    fields = parse_resume_fields(raw_text)
    score = _compute_profile_score(fields)
    fields["completeness_score"] = score

    cand_email = fields.get("email")
    if not cand_email or not isinstance(cand_email, str) or "@" not in cand_email:
        cand_email_clean = None
    else:
        cand_email_clean = cand_email.strip().lower()

    cand_name = fields.get("name")
    if not cand_name or not isinstance(cand_name, str) or len(cand_name.strip()) < 2:
        base_name = os.path.splitext(os.path.basename(filename))[0]
        cand_name = base_name.replace("_", " ").replace("-", " ").title()

    cand_phone = fields.get("phone")
    clean_phone = str(cand_phone).strip() if cand_phone and len(str(cand_phone).strip()) >= 7 else None

    # Resume & Candidate Deduplication Check
    is_duplicate = False
    duplicate_reason = None
    profile = None
    user = None

    # Check 1: Exact File Content Hash
    existing_profile = db.query(CandidateProfile).filter(CandidateProfile.resume_hash == resume_hash).first()
    if existing_profile:
        is_duplicate = True
        duplicate_reason = "Identical file hash match"
        profile = existing_profile
        user = db.query(User).filter(User.id == profile.user_id).first()

    # Check 2: Email Match
    if not is_duplicate and cand_email_clean:
        existing_user = db.query(User).filter(User.email == cand_email_clean).first()
        if existing_user:
            is_duplicate = True
            duplicate_reason = f"Matching candidate email ({cand_email_clean})"
            user = existing_user
            profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()

    # Check 3: Phone Match
    if not is_duplicate and clean_phone:
        existing_phone_profile = db.query(CandidateProfile).filter(CandidateProfile.phone == clean_phone).first()
        if existing_phone_profile:
            is_duplicate = True
            duplicate_reason = f"Matching candidate phone ({clean_phone})"
            profile = existing_phone_profile
            user = db.query(User).filter(User.id == profile.user_id).first()

    # Create new Candidate User if not a duplicate
    if not user:
        if not cand_email_clean:
            cand_email_clean = f"bulk_cand_{uuid.uuid4().hex[:8]}@uploaded-resume.local"

        from app.core.security import hash_password
        user = User(
            name=cand_name,
            email=cand_email_clean,
            password_hash=hash_password(uuid.uuid4().hex),
            role=UserRole.candidate,
            is_active=True,
            verification_status="approved",
            is_email_verified=True,
        )
        db.add(user)
        db.flush()
    else:
        if cand_name and (not user.name or user.name.strip() in ("", "Candidate", "Test User", "User")):
            user.name = cand_name
            db.add(user)

    if not profile:
        profile = CandidateProfile(user_id=user.id)
        db.add(profile)
        db.flush()

    # Update candidate profile fields and resume hash
    profile.resume_path = file_path
    profile.resume_text = raw_text
    profile.resume_original_filename = filename
    profile.resume_hash = resume_hash

    if fields.get("phone"): profile.phone = fields.get("phone")
    if fields.get("location"): profile.location = fields.get("location")
    if fields.get("address"): profile.address = fields.get("address")
    if fields.get("summary"): profile.summary = fields.get("summary")
    if fields.get("experience_years") is not None: profile.experience_years = fields.get("experience_years")
    if fields.get("education"): profile.education = fields.get("education")
    if fields.get("work_experience"): profile.work_experience = fields.get("work_experience")
    profile.profile_score = score

    extracted_certs = fields.get("certifications")
    if extracted_certs:
        profile.certifications = ", ".join(extracted_certs) if isinstance(extracted_certs, list) else str(extracted_certs)

    extracted_skills = fields.get("skills") or []
    if extracted_skills:
        top_skills = extracted_skills[:4]
        profile.headline = f"{top_skills[0]} Specialist | {', '.join(top_skills)}"
        profile.current_role = f"{top_skills[0]} Specialist"

    fields["resume_text"] = raw_text
    try:
        ai_res = generate_resume_summary(fields)
        profile.ai_summary = ai_res.get("summary")
    except Exception:
        pass

    db.flush()

    seed_skills(db)
    fresh_skills = sorted(list(set(extracted_skills)))
    _sync_candidate_skills(db, profile, fresh_skills)

    # Job / Custom JD Association & ATS Scoring
    ats_res = None
    target_job = None
    if job_id_str:
        try:
            j_uuid = uuid.UUID(job_id_str)
            target_job = db.query(Job).filter(Job.id == j_uuid).first()
        except Exception:
            target_job = None

    if not target_job and custom_jd_data and (custom_jd_data.get("title") or custom_jd_data.get("description") or custom_jd_data.get("skills")):
        # Store persistent Job in DB for custom JD
        jd_title = custom_jd_data.get("title") or "Custom Target Role"
        if recruiter_id:
            target_job = db.query(Job).filter(Job.recruiter_id == recruiter_id, Job.title == jd_title).first()
            if not target_job:
                from app.models.job import JobStatus
                target_job = Job(
                    id=uuid.uuid4(),
                    recruiter_id=recruiter_id,
                    title=jd_title,
                    description=f"{custom_jd_data.get('description') or ''}\nRequired Skills: {custom_jd_data.get('skills') or ''}",
                    experience_required=float(custom_jd_data.get("min_experience") or 0.0),
                    status=JobStatus.published,
                )
                db.add(target_job)
                db.flush()

    if not target_job and recruiter_id:
        # Fallback to General Candidate Talent Pool job requisition
        target_job = db.query(Job).filter(Job.recruiter_id == recruiter_id, Job.title == "General Candidate Talent Pool").first()
        if not target_job:
            from app.models.job import JobStatus
            target_job = Job(
                id=uuid.uuid4(),
                recruiter_id=recruiter_id,
                title="General Candidate Talent Pool",
                description="General candidate talent pool for bulk resume uploads",
                status=JobStatus.published,
            )
            db.add(target_job)
            db.flush()

    if recruiter_id:
        profile.created_by_recruiter_id = str(recruiter_id)
        profile.source = "recruiter_bulk_upload"

    if target_job:
        try:
            from app.services.ats_scoring_service import calculate_job_specific_ats
            from app.models.application import Application, ApplicationStatus
            ats_res = calculate_job_specific_ats(profile, target_job)

            # Store/update Application record in DB
            app_rec = db.query(Application).filter(
                Application.candidate_id == profile.id, Application.job_id == target_job.id
            ).first()

            overall_score = ats_res.get("overall_ats_score", 0.0) if isinstance(ats_res, dict) else 0.0
            score_bk = ats_res.get("score_breakdown", {}) if isinstance(ats_res, dict) else {}
            matched_s = json.dumps(ats_res.get("matched_skills", [])) if isinstance(ats_res, dict) else "[]"
            missing_s = json.dumps(ats_res.get("missing_skills", [])) if isinstance(ats_res, dict) else "[]"
            bk_json = json.dumps(ats_res) if isinstance(ats_res, dict) else "{}"

            if not app_rec:
                app_rec = Application(
                    candidate_id=profile.id,
                    job_id=target_job.id,
                    status=ApplicationStatus.applied,
                    match_score=overall_score,
                    ats_score=overall_score,
                    skills_match_score=score_bk.get("skills", 0.0),
                    experience_match_score=score_bk.get("experience", 0.0),
                    education_match_score=score_bk.get("education", 0.0),
                    location_match_score=score_bk.get("location", 0.0),
                    keyword_match_score=score_bk.get("keywords", 0.0),
                    matched_skills=matched_s,
                    missing_skills=missing_s,
                    match_breakdown=bk_json,
                    uploaded_by_recruiter_id=str(recruiter_id) if recruiter_id else None,
                    source="recruiter_bulk_upload",
                )
                db.add(app_rec)
            else:
                app_rec.match_score = overall_score
                app_rec.ats_score = overall_score
                app_rec.skills_match_score = score_bk.get("skills", 0.0)
                app_rec.experience_match_score = score_bk.get("experience", 0.0)
                app_rec.education_match_score = score_bk.get("education", 0.0)
                app_rec.location_match_score = score_bk.get("location", 0.0)
                app_rec.keyword_match_score = score_bk.get("keywords", 0.0)
                app_rec.matched_skills = matched_s
                app_rec.missing_skills = missing_s
                app_rec.match_breakdown = bk_json
                if recruiter_id:
                    app_rec.uploaded_by_recruiter_id = str(recruiter_id)
                    app_rec.source = "recruiter_bulk_upload"
        except Exception as err:
            print("Error during ATS score calculation:", err)

    db.commit()
    db.refresh(profile)

    overall_score = 0.0
    if ats_res and isinstance(ats_res, dict):
        overall_score = ats_res.get("overall_ats_score", 0.0)
    else:
        overall_score = float(fields.get("completeness_score", 0))

    return {
        "filename": filename,
        "status": "completed",
        "is_duplicate": is_duplicate,
        "duplicate_reason": duplicate_reason,
        "candidate_id": str(profile.id),
        "user_id": str(user.id),
        "error": None,
        "extracted_data": fields,
        "ats_analysis": ats_res,
        "overall_match_score": overall_score,
    }


@router.post("/bulk-upload")
async def bulk_upload_resumes(
    files: List[UploadFile] = File(...),
    job_id: Optional[str] = Form(None),
    custom_jd_title: Optional[str] = Form(None),
    custom_jd_description: Optional[str] = Form(None),
    custom_jd_skills: Optional[str] = Form(None),
    custom_jd_exp: Optional[float] = Form(None),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Processes multiple PDF/DOCX resumes or ZIP archives for recruiters and stores candidates in the system."""
    results = []
    total_files = 0
    success_count = 0
    failed_count = 0
    duplicate_count = 0

    custom_jd_data = None
    if custom_jd_title or custom_jd_description or custom_jd_skills:
        custom_jd_data = {
            "title": custom_jd_title or "Custom Job Requisition",
            "description": custom_jd_description or "",
            "skills": custom_jd_skills or "",
            "min_experience": custom_jd_exp or 0.0,
        }

    for file in files:
        file_bytes = await file.read()
        filename = file.filename or "resume.pdf"

        # Check if ZIP archive
        if filename.lower().endswith(".zip"):
            try:
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
                    for zip_info in zf.infolist():
                        if zip_info.is_dir():
                            continue
                        zip_fname = os.path.basename(zip_info.filename)
                        if zip_fname.lower().endswith((".pdf", ".docx")):
                            total_files += 1
                            item_bytes = zf.read(zip_info)
                            try:
                                item_res = _save_and_store_bulk_resume(
                                    db, item_bytes, zip_fname, job_id, custom_jd_data, current_user.id
                                )
                                results.append(item_res)
                                success_count += 1
                                if item_res.get("is_duplicate"):
                                    duplicate_count += 1
                            except Exception as exc:
                                db.rollback()
                                results.append({
                                    "filename": zip_fname,
                                    "status": "failed",
                                    "is_duplicate": False,
                                    "error": str(exc),
                                    "extracted_data": None,
                                    "overall_match_score": 0.0
                                })
                                failed_count += 1
            except Exception as zip_err:
                db.rollback()
                total_files += 1
                results.append({
                    "filename": filename,
                    "status": "failed",
                    "is_duplicate": False,
                    "error": f"Invalid zip archive: {str(zip_err)}",
                    "extracted_data": None,
                    "overall_match_score": 0.0
                })
                failed_count += 1
        else:
            total_files += 1
            try:
                item_res = _save_and_store_bulk_resume(
                    db, file_bytes, filename, job_id, custom_jd_data, current_user.id
                )
                results.append(item_res)
                success_count += 1
                if item_res.get("is_duplicate"):
                    duplicate_count += 1
            except Exception as exc:
                db.rollback()
                results.append({
                    "filename": filename,
                    "status": "failed",
                    "is_duplicate": False,
                    "error": str(exc),
                    "extracted_data": None,
                    "overall_match_score": 0.0
                })
                failed_count += 1

    # Sort results by overall_match_score descending to rank Best Match
    results.sort(key=lambda x: x.get("overall_match_score", 0.0), reverse=True)

    # Assign rank and best match indicator
    for idx, item in enumerate(results):
        item["rank"] = idx + 1
        item["is_best_match"] = (idx == 0 and item.get("status") == "completed" and item.get("overall_match_score", 0) > 0)

    best_candidate_name = None
    best_score = 0.0
    if results and results[0].get("is_best_match"):
        best_cand_data = results[0].get("extracted_data") or {}
        best_candidate_name = best_cand_data.get("name") or results[0].get("filename")
        best_score = results[0].get("overall_match_score", 0.0)

    return APIResponse(
        success=True,
        message=f"Processed and stored {total_files} resume(s): {success_count} stored ({duplicate_count} duplicate(s) linked), {failed_count} failed",
        data={
            "total": total_files,
            "successful": success_count,
            "failed": failed_count,
            "duplicates": duplicate_count,
            "best_match": {
                "candidate_name": best_candidate_name,
                "score": best_score,
            } if best_candidate_name else None,
            "results": results,
        },
    )


@router.get("/me", response_model=APIResponse[CandidateProfileResponse])
def get_my_profile(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise NotFoundError("No resume uploaded yet")

    return APIResponse(success=True, message="Candidate profile", data=CandidateProfileResponse.from_profile(profile))


@router.put("/me", response_model=APIResponse[CandidateProfileResponse])
def update_my_profile(
    body: CandidateProfileUpdate,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Allows candidate to edit their parsed profile details."""
    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise NotFoundError("No resume uploaded yet")

    update_dict = body.model_dump(exclude_unset=True)
    profile = update_candidate_profile(
        db,
        profile,
        update_dict,
        user_name=current_user.name,
        user_email=current_user.email,
    )

    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == profile.id)
        .first()
    )

    return APIResponse(
        success=True,
        message="Candidate profile updated successfully",
        data=CandidateProfileResponse.from_profile(profile),
    )


@router.delete("/me", response_model=APIResponse[None])
def delete_my_profile(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Deletes the current candidate's uploaded resume and parsed profile."""
    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise NotFoundError("No resume uploaded yet")

    delete_candidate_profile(db, profile)

    return APIResponse(success=True, message="Resume deleted successfully", data=None)


@router.post("/summary", response_model=APIResponse[CandidateProfileResponse])
def generate_my_summary(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Generates (or regenerates) an AI professional summary for the current
    candidate's profile via the configured LLM, falling back to a
    template built from the parsed resume data if no LLM is configured.
    """
    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise NotFoundError("No resume uploaded yet")

    fields = {
        "skills": sorted({cs.skill.skill_name for cs in profile.candidate_skills}),
        "experience_years": profile.experience_years,
        "education": profile.education,
        "resume_text": profile.resume_text,
    }
    result = generate_resume_summary(fields)

    profile.ai_summary = result["summary"]
    db.commit()
    db.refresh(profile)

    return APIResponse(
        success=True,
        message=f"AI summary generated ({result['source']})",
        data=CandidateProfileResponse.from_profile(profile),
    )


@router.get("/domains", response_model=APIResponse[list[dict]])
def list_tech_domains():
    """Lists available technology domains for targeted strict ATS resume evaluation."""
    from app.nlp.domain_data import get_available_domains

    return APIResponse(
        success=True,
        message="Available technology domains",
        data=get_available_domains(),
    )


@router.post("/analyze-domain", response_model=APIResponse[dict])
def analyze_resume_domain(
    target_domain: str | None = None,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Evaluates candidate resume strictly against explicit role & selected technology domain."""
    from app.nlp.domain_evaluator import evaluate_domain_ats_score, detect_explicit_resume_role

    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise NotFoundError("No resume uploaded yet")

    skills = [cs.skill.skill_name for cs in profile.candidate_skills]
    resume_text = profile.resume_text or profile.summary or ""

    if not target_domain or target_domain == "auto":
        explicit_info = detect_explicit_resume_role(resume_text, skills)
        target_domain = explicit_info["domain_key"]

    result = evaluate_domain_ats_score(
        candidate_skills=skills,
        resume_text=resume_text,
        target_domain=target_domain,
    )

    return APIResponse(
        success=True,
        message=f"Resume evaluated against {result.domain_title}",
        data=result.to_dict(),
    )



@router.get("/best-role", response_model=APIResponse[dict])
def get_best_suited_role(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Identifies the #1 best suited job position and role match for candidate's resume."""
    from app.nlp.best_role_evaluator import find_best_suited_position

    result = find_best_suited_position(db, current_user.id)
    return APIResponse(
        success=True,
        message=f"Best suited job position identified: {result.best_role_title}",
        data=result.to_dict(),
    )


@router.get("/{candidate_id}", response_model=APIResponse[CandidateProfileResponse])
def get_candidate_profile(
    candidate_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Recruiter/admin view of any candidate's parsed profile, by CandidateProfile id."""
    try:
        parsed_id = uuid.UUID(candidate_id)
    except ValueError:
        raise NotFoundError("Candidate profile not found")

    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == parsed_id)
        .first()
    )
    if not profile:
        raise NotFoundError("Candidate profile not found")

    return APIResponse(success=True, message="Candidate profile", data=CandidateProfileResponse.from_profile(profile))


from fastapi import Form
from app.routers.auth import _issue_tokens
from app.schemas.user import TokenResponse

@router.post("/complete-registration", response_model=APIResponse[TokenResponse])
async def complete_candidate_registration(
    name: str = Form(None),
    phone: str = Form(None),
    location: str = Form(None),
    headline: str = Form(None),
    current_role: str = Form(None),
    experience_years: Optional[str] = Form(None),
    summary: str = Form(None),
    education: str = Form(None),
    work_experience: str = Form(None),
    skills: str = Form(None),
    linkedin_url: str = Form(None),
    github_url: str = Form(None),
    portfolio_url: str = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """Submits complete candidate registration details before accessing Candidate Dashboard."""
    if name and name.strip():
        current_user.name = name.strip()
        db.add(current_user)

    parsed_exp_years = None
    if experience_years is not None and str(experience_years).strip() != "":
        try:
            parsed_exp_years = float(str(experience_years).strip())
        except (ValueError, TypeError):
            parsed_exp_years = 0.0

    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )

    if file and file.filename:
        file_bytes = await file.read()
        raw_text = extract_resume_text(file_bytes, file.filename)
        fields = parse_resume_fields(raw_text)
        fields["resume_text"] = raw_text

        form_data = {
            "name": name or current_user.name,
            "phone": phone,
            "location": location,
            "experience_years": parsed_exp_years,
            "skills": [s.strip() for s in skills.split(",") if s.strip()] if skills else [],
        }

        from app.services.resume_verification_service import verify_resume_against_form
        is_valid, mismatches = verify_resume_against_form(fields, form_data)
        if not is_valid:
            err_msg = "Candidate Registration Blocked due to Form vs Resume Mismatches:\n• " + "\n• ".join(mismatches)
            raise AppError(err_msg, "RESUME_FORM_MISMATCH", 400)

        profile = process_resume(db, current_user.id, file_bytes, file.filename)
    elif not profile:
        profile = CandidateProfile(
            user_id=current_user.id,
            phone=phone,
            location=location,
            headline=headline or current_role or "Candidate",
            current_role=current_role or headline or "Candidate",
            experience_years=parsed_exp_years or 0.0,
            summary=summary,
            education=education,
            work_experience=work_experience,
            linkedin_url=linkedin_url,
            github_url=github_url,
            portfolio_url=portfolio_url,
        )
        db.add(profile)
        db.flush()

    update_dict = {}
    if linkedin_url: update_dict["linkedin_url"] = linkedin_url
    if github_url: update_dict["github_url"] = github_url
    if portfolio_url: update_dict["portfolio_url"] = portfolio_url

    # If NO resume file was uploaded, use form inputs to populate profile
    if not (file and file.filename):
        if phone is not None: update_dict["phone"] = phone
        if location is not None: update_dict["location"] = location
        if headline is not None: update_dict["headline"] = headline
        if current_role is not None: update_dict["current_role"] = current_role
        if parsed_exp_years is not None: update_dict["experience_years"] = parsed_exp_years
        if summary is not None: update_dict["summary"] = summary
        if education is not None: update_dict["education"] = education
        if work_experience is not None: update_dict["work_experience"] = work_experience
        if skills is not None and skills.strip():
            update_dict["skills"] = [s.strip() for s in skills.split(",") if s.strip()]

    if update_dict:
        profile = update_candidate_profile(
            db,
            profile,
            update_dict,
            user_name=current_user.name,
            user_email=current_user.email,
        )

    db.commit()
    db.refresh(current_user)

    tokens = _issue_tokens(current_user, db)
    tokens.user.is_profile_complete = True

    return APIResponse(
        success=True,
        message="Candidate registration completed successfully!",
        data=tokens,
    )


def _build_candidate_dossier_html(profile: CandidateProfile, user: Optional[User], application: Optional[Application] = None) -> str:
    name = user.name if user else "Candidate Profile"
    email = user.email if user else "Not provided"
    phone = profile.phone or "Not provided"
    location = profile.location or "Not provided"
    address = profile.address or ""
    headline = profile.headline or profile.current_role or "Candidate"
    exp_years = f"{profile.experience_years} Years" if profile.experience_years is not None else "Not specified"
    score = f"{profile.profile_score}%" if profile.profile_score is not None else "N/A"

    skills = sorted({cs.skill.skill_name for cs in profile.candidate_skills}) if profile.candidate_skills else []
    skills_html = "".join([f'<span style="display:inline-block; background:#e2e8f0; color:#1e293b; padding:4px 10px; border-radius:12px; font-size:13px; font-weight:600; margin:3px;">{s}</span>' for s in skills]) if skills else "<em>No skills listed</em>"

    social_links = []
    if profile.linkedin_url: social_links.append(f'<a href="{profile.linkedin_url}" target="_blank" style="color:#0a66c2; text-decoration:none; margin-right:15px;">🔗 LinkedIn</a>')
    if profile.github_url: social_links.append(f'<a href="{profile.github_url}" target="_blank" style="color:#24292e; text-decoration:none; margin-right:15px;">💻 GitHub</a>')
    if profile.portfolio_url: social_links.append(f'<a href="{profile.portfolio_url}" target="_blank" style="color:#2563eb; text-decoration:none; margin-right:15px;">🌐 Portfolio</a>')
    if profile.other_links: social_links.append(f'<span style="color:#64748b;">🔗 {profile.other_links}</span>')
    social_html = " ".join(social_links) if social_links else "<em>No external profile links provided</em>"

    summary_text = profile.summary or profile.ai_summary or "No summary available"
    ai_summary_html = f'<div style="background:#f0f9ff; border-left:4px solid #0284c7; padding:12px 16px; border-radius:4px; margin-bottom:15px; color:#0369a1;"><strong>🤖 AI Professional Summary:</strong><br>{profile.ai_summary}</div>' if profile.ai_summary else ""

    app_html = ""
    if application:
        match_score = f"{round(application.ats_score or application.match_score or 0)}%"
        breakdown_data = {}
        if application.match_breakdown:
            try:
                breakdown_data = json.loads(application.match_breakdown)
            except Exception:
                breakdown_data = {}

        raw_exp = breakdown_data.get("explanation") if isinstance(breakdown_data, dict) else None
        exp_dict = raw_exp if isinstance(raw_exp, dict) else {}
        breakdown = (breakdown_data.get("breakdown") if isinstance(breakdown_data, dict) else {}) or {}

        matched_skills_list = []
        if application.matched_skills:
            try:
                matched_skills_list = json.loads(application.matched_skills)
            except Exception:
                matched_skills_list = []
        elif isinstance(exp_dict, dict):
            matched_skills_list = exp_dict.get("matched_required_skills") or []

        missing_skills_list = []
        if application.missing_skills:
            try:
                missing_skills_list = json.loads(application.missing_skills)
            except Exception:
                missing_skills_list = []
        elif isinstance(exp_dict, dict):
            missing_skills_list = exp_dict.get("missing_required_skills") or []

        matched = "".join([f'<span style="display:inline-block; background:#dcfce7; color:#15803d; padding:3px 8px; border-radius:8px; font-size:12px; margin:2px;">✓ {s}</span>' for s in matched_skills_list]) or "None"
        missing = "".join([f'<span style="display:inline-block; background:#fee2e2; color:#b91c1c; padding:3px 8px; border-radius:8px; font-size:12px; margin:2px;">✗ {s}</span>' for s in missing_skills_list]) or "None"

        skill_score = round(application.skills_match_score or (breakdown.get('skill_match') or breakdown.get('skills_match') or 0))
        exp_score = round(application.experience_match_score or breakdown.get('experience_match') or 0)
        kw_score = round(application.keyword_match_score or breakdown.get('semantic_match') or 0)

        app_html = f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:20px; margin-top:25px;">
            <h3 style="margin-top:0; color:#0f172a; font-size:18px;">🎯 Application & ATS Match Analysis</h3>
            <div style="display:flex; justify-content:space-between; align-items:center; background:#ffffff; padding:12px 16px; border-radius:6px; border:1px solid #cbd5e1; margin-bottom:15px;">
                <div><strong>Status:</strong> <span style="text-transform:capitalize; font-weight:bold; color:#2563eb;">{application.status}</span></div>
                <div style="font-size:20px; font-weight:bold; color:#16a34a;">Overall ATS Score: {match_score}</div>
            </div>
            <div style="font-size:13px; color:#475569; margin-bottom:10px;">
                Skill Match: <strong>{skill_score}%</strong> |
                Experience Match: <strong>{exp_score}%</strong> |
                Keyword Match: <strong>{kw_score}%</strong>
            </div>
            <div style="margin-bottom:8px;"><strong>Matched Skills:</strong><br>{matched}</div>
            <div><strong>Missing Required Skills:</strong><br>{missing}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Candidate Profile — {name}</title>
    <style>
        body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f1f5f9; color: #334155; margin: 0; padding: 30px; }}
        .container {{ max-width: 850px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: flex-start; }}
        .name {{ font-size: 28px; font-weight: 700; color: #0f172a; margin: 0 0 4px 0; }}
        .headline {{ font-size: 16px; font-weight: 600; color: #2563eb; margin: 0 0 10px 0; }}
        .meta {{ font-size: 14px; color: #64748b; line-height: 1.6; }}
        .badge-score {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 14px; font-weight: 700; padding: 6px 14px; border-radius: 20px; }}
        .section {{ margin-bottom: 25px; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; margin-bottom: 12px; }}
        .content-box {{ background: #f8fafc; padding: 15px; border-radius: 6px; font-size: 14px; line-height: 1.6; color: #334155; white-space: pre-line; }}
        .footer {{ font-size: 12px; color: #94a3b8; text-align: center; border-top: 1px solid #e2e8f0; margin-top: 30px; padding-top: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 class="name">{name}</h1>
                <div class="headline">{headline}</div>
                <div class="meta">
                    📧 {email} &bull; 📞 {phone} &bull; 📍 {location}<br>
                    💼 <strong>{exp_years}</strong> Professional Experience {f' &bull; 🏡 {address}' if address else ''}
                </div>
            </div>
            <div>
                <span class="badge-score">ATS Score: {score}</span>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🌐 Online Profiles & Portfolios</div>
            <div style="font-size: 14px;">{social_html}</div>
        </div>

        {ai_summary_html}

        <div class="section">
            <div class="section-title">📝 Executive Summary / About</div>
            <div class="content-box">{summary_text}</div>
        </div>

        <div class="section">
            <div class="section-title">🛠️ Technical & Core Skills</div>
            <div>{skills_html}</div>
        </div>

        <div class="section">
            <div class="section-title">💼 Work History & Experience</div>
            <div class="content-box">{profile.work_experience or 'No detailed work history provided.'}</div>
        </div>

        <div class="section">
            <div class="section-title">🎓 Education & Certifications</div>
            <div class="content-box">
                <strong>Education:</strong> {profile.education or 'Not specified'}<br><br>
                <strong>Certifications:</strong> {profile.certifications or 'None listed'}
            </div>
        </div>

        {app_html}

        <div class="footer">
            Generated automatically by <strong>AI Recruiter Platform</strong> &bull; Confidential Candidate Dossier
        </div>
    </div>
</body>
</html>"""
    return html


@router.get("/{candidate_id}/export")
def export_candidate_details(
    candidate_id: str,
    format: str = Query("pdf", description="Export format: pdf, html, json, or zip"),
    application_id: Optional[str] = Query(None, description="Optional application ID to include match scores"),
    token: Optional[str] = Query(None, alias="token"),
    token_header: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Exports complete candidate details including personal info, skills, experience,
    education, social links, ATS match score (if application_id given), and original resume.
    Formats: zip (complete package), html (dossier report), json (raw data).
    """
    auth_token = token_header or token
    if not auth_token:
        raise AuthError("Not authenticated")

    payload = decode_token(auth_token)
    if not payload or payload.get("type") != "access":
        raise AuthError("Invalid or expired token")

    try:
        user_id = uuid.UUID(payload.get("sub"))
    except (TypeError, ValueError):
        raise AuthError("Invalid token subject")

    current_user = db.get(User, user_id)
    if not current_user:
        raise AuthError("User no longer exists")

    try:
        parsed_id = uuid.UUID(candidate_id)
    except ValueError:
        raise NotFoundError("Candidate profile not found")

    profile = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter((CandidateProfile.id == parsed_id) | (CandidateProfile.user_id == parsed_id))
        .first()
    )
    if not profile:
        raise NotFoundError("Candidate profile not found")

    if current_user.role not in (UserRole.recruiter, UserRole.admin, UserRole.superadmin):
        if profile.user_id != current_user.id:
            raise PermissionDeniedError("You do not have permission to export this candidate's details")

    user = profile.user or db.get(User, profile.user_id)
    application = None
    if application_id:
        try:
            app_uuid = uuid.UUID(application_id)
            application = db.query(Application).filter(Application.id == app_uuid).first()
        except ValueError:
            pass

    cand_name = user.name if user else "Candidate"
    safe_name = secure_filename(cand_name.replace(" ", "_"))

    if format.lower() == "json":
        data = CandidateProfileResponse.from_profile(profile).model_dump(mode="json")
        if user:
            data["name"] = user.name
            data["email"] = user.email
        if application:
            breakdown_data = {}
            if application.match_breakdown:
                try:
                    breakdown_data = json.loads(application.match_breakdown)
                except Exception:
                    breakdown_data = {}
            data["application"] = {
                "id": str(application.id),
                "status": application.status,
                "match_score": application.match_score,
                "breakdown": breakdown_data.get("breakdown"),
                "explanation": breakdown_data.get("explanation"),
            }
        return APIResponse(success=True, message="Candidate full profile data", data=data)

    html_content = _build_candidate_dossier_html(profile, user, application)

    if format.lower() == "html":
        return HTMLResponse(
            content=html_content,
            headers={"Content-Disposition": f'attachment; filename="Candidate_Profile_{safe_name}.html"'}
        )

    if format.lower() == "zip":
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"Candidate_Profile_Dossier_{safe_name}.html", html_content)
            if profile.resume_path and os.path.exists(profile.resume_path):
                orig_filename = profile.resume_original_filename or os.path.basename(profile.resume_path)
                with open(profile.resume_path, "rb") as rf:
                    zf.writestr(f"Original_Resume_{orig_filename}", rf.read())

        zip_buffer.seek(0)
        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="Candidate_Full_Details_{safe_name}.zip"'}
        )

    # Default format: pdf (Complete candidate dossier rendered as a downloadable PDF)
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        raise AppError("Failed to generate candidate PDF dossier.", "PDF_GEN_ERROR", 500)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="Candidate_Profile_{safe_name}.pdf"'}
    )


from app.schemas.resume_improvement import ResumeImprovementRequest, ResumeImprovementResponse, AcceptImprovementRequest
from app.services.resume_improvement_service import analyze_and_improve_resume
from app.models.job import Job, JobSkill

@router.post("/improve", response_model=APIResponse[ResumeImprovementResponse])
def improve_resume_endpoint(
    payload: ResumeImprovementRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        cand_uuid = uuid.UUID(payload.candidate_id)
        job_uuid = uuid.UUID(payload.job_id)
    except ValueError:
        raise NotFoundError("Invalid candidate or job ID format.")

    candidate = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.id == cand_uuid)
        .first()
    )
    if not candidate:
        raise NotFoundError("Candidate profile not found.")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == job_uuid)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found.")

    result = analyze_and_improve_resume(candidate, job)
    return APIResponse(success=True, message="AI Resume Improvement Analysis", data=ResumeImprovementResponse(**result))


@router.post("/accept-improvement")
def accept_improvement_endpoint(
    payload: AcceptImprovementRequest,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    try:
        cand_uuid = uuid.UUID(payload.candidate_id)
    except ValueError:
        raise NotFoundError("Invalid candidate ID format.")

    candidate = db.query(CandidateProfile).filter(CandidateProfile.id == cand_uuid, CandidateProfile.user_id == current_user.id).first()
    if not candidate:
        raise NotFoundError("Candidate profile not found or permission denied.")

    if payload.section == "summary":
        candidate.summary = payload.improved_text
    else:
        if candidate.work_experience and payload.original_text in candidate.work_experience:
            candidate.work_experience = candidate.work_experience.replace(payload.original_text, payload.improved_text)
        elif candidate.resume_text and payload.original_text in candidate.resume_text:
            candidate.resume_text = candidate.resume_text.replace(payload.original_text, payload.improved_text)

    db.commit()
    return APIResponse(success=True, message="Improvement accepted and applied to candidate profile.", data={"candidate_id": str(candidate.id)})


@router.get("/recruiter/my-candidates")
def list_recruiter_uploaded_candidates(
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.company_admin, UserRole.admin)),
    db: Session = Depends(get_db),
):
    """Retrieves candidates specifically created or uploaded by the requesting recruiter."""
    profiles = (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.user))
        .filter(CandidateProfile.created_by_recruiter_id == str(current_user.id))
        .all()
    )
    results = []
    for p in profiles:
        u = p.user
        results.append({
            "candidate_id": str(p.id),
            "user_id": str(p.user_id),
            "name": u.name if u else "Candidate",
            "email": u.email if u else None,
            "phone": p.phone,
            "location": p.location,
            "headline": p.headline,
            "current_role": p.current_role,
            "experience_years": p.experience_years,
            "profile_score": p.profile_score,
            "source": p.source or "recruiter_bulk_upload",
            "created_at": p.created_at.isoformat() if p.created_at else None,
        })
    return APIResponse(success=True, message=f"Retrieved {len(results)} recruiter uploaded candidate(s)", data=results)


# Singular alias route /api/v1/resume/improve
resume_singular_router = APIRouter(prefix="/resume", tags=["Resume Coach"])

@resume_singular_router.post("/improve", response_model=APIResponse[ResumeImprovementResponse])
def improve_resume_singular_endpoint(
    payload: ResumeImprovementRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return improve_resume_endpoint(payload=payload, current_user=current_user, db=db)


