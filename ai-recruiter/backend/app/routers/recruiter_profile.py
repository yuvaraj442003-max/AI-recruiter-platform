"""
Recruiter Profile Router — view & update recruiter / company profile.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.recruiter import RecruiterProfile
from app.models.user import User, UserRole
from app.schemas.candidate import RecruiterProfileResponse, RecruiterProfileUpdate
from app.schemas.common import APIResponse

router = APIRouter(prefix="/recruiter-profile", tags=["Recruiter Profile"])


def _get_or_create_recruiter_profile(db: Session, user: User) -> RecruiterProfile:
    profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user.id).first()
    if not profile:
        profile = RecruiterProfile(
            user_id=user.id,
            company_name=None,
            job_title="Recruiter / Talent Acquisition",
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("", response_model=APIResponse[RecruiterProfileResponse])
def get_recruiter_profile(
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_recruiter_profile(db, current_user)
    resp = RecruiterProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        recruiter_name=current_user.name,
        email=current_user.email,
        profile_photo=profile.profile_photo,
        job_title=profile.job_title,
        company_name=profile.company_name,
        company_logo=profile.company_logo,
        company_description=profile.company_description,
        industry=profile.industry,
        company_size=profile.company_size,
        location=profile.location,
        website=profile.website,
        linkedin_url=profile.linkedin_url,
        github_url=profile.github_url,
        other_links=profile.other_links,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )
    return APIResponse(success=True, message="Recruiter profile retrieved", data=resp)


@router.put("", response_model=APIResponse[RecruiterProfileResponse])
def update_recruiter_profile(
    payload: RecruiterProfileUpdate,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_recruiter_profile(db, current_user)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(profile, k, v)
    db.commit()
    db.refresh(profile)

    resp = RecruiterProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        recruiter_name=current_user.name,
        email=current_user.email,
        profile_photo=profile.profile_photo,
        job_title=profile.job_title,
        company_name=profile.company_name,
        company_logo=profile.company_logo,
        company_description=profile.company_description,
        industry=profile.industry,
        company_size=profile.company_size,
        location=profile.location,
        website=profile.website,
        linkedin_url=profile.linkedin_url,
        github_url=profile.github_url,
        other_links=profile.other_links,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )
    return APIResponse(success=True, message="Recruiter profile updated successfully", data=resp)


from app.models.company import Company
from app.services.verification_service import verify_company_domain, verify_website_ssl, verify_company_government


def _get_or_create_company(db: Session, recruiter_profile: RecruiterProfile, user: User) -> Company:
    company = None
    if recruiter_profile.company_name:
        company = db.query(Company).filter(Company.name == recruiter_profile.company_name).first()
    if not company:
        company = Company(
            name=recruiter_profile.company_name or f"{user.name}'s Company",
            website=recruiter_profile.website,
            official_email=user.email,
            verification_status="unverified",
        )
        db.add(company)
        db.commit()
        db.refresh(company)
    return company


@router.post("/verify-domain", response_model=APIResponse[dict])
def trigger_domain_verification(
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_recruiter_profile(db, current_user)
    company = _get_or_create_company(db, profile, current_user)

    status_code, reason = verify_company_domain(current_user.email, profile.website or company.website)
    if status_code == "domain_verified":
        company.verification_status = "domain_verified"
        company.official_email = current_user.email
        if profile.website:
            company.website = profile.website
        db.commit()

    return APIResponse(
        success=True,
        message=reason,
        data={
            "verification_status": company.verification_status,
            "recruiter_email": current_user.email,
            "website": profile.website,
            "details": reason,
        },
    )


@router.post("/verify-website", response_model=APIResponse[dict])
def trigger_website_verification(
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_recruiter_profile(db, current_user)
    company = _get_or_create_company(db, profile, current_user)

    ssl_ok, details = verify_website_ssl(profile.website or company.website)
    company.ssl_verified = ssl_ok
    company.ssl_details = details
    db.commit()

    return APIResponse(
        success=True,
        message="Website & SSL verification completed",
        data={
            "ssl_verified": company.ssl_verified,
            "website": profile.website or company.website,
            "ssl_details": details,
        },
    )


@router.post("/submit-company-verification", response_model=APIResponse[dict])
def submit_company_verification(
    cin_gstin: str = None,
    registration_number: str = None,
    country: str = None,
    address: str = None,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_recruiter_profile(db, current_user)
    company = _get_or_create_company(db, profile, current_user)

    if cin_gstin:
        company.cin_gstin = cin_gstin
    if registration_number:
        company.registration_number = registration_number
    if country:
        company.country = country
    if address:
        company.address = address

    # Perform automated government format verification check
    gov_status, notes = verify_company_government(company.cin_gstin or company.registration_number, company.name)
    company.verification_notes = notes
    if gov_status == "government_verified":
        company.verification_status = "government_verified"

    db.commit()

    return APIResponse(
        success=True,
        message="Company verification details updated",
        data={
            "company_name": company.name,
            "verification_status": company.verification_status,
            "cin_gstin": company.cin_gstin,
            "notes": notes,
        },
    )

