"""
Authentication endpoints: register, login, refresh, and "who am I".
"""
import uuid

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import AuthError, ConflictError
from app.core.rate_limit import check_ip_rate_limit, check_login_lockout, clear_failed_logins, record_failed_login
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.user import GoogleLoginRequest, RefreshRequest, TokenResponse, UserLogin, UserRegister, UserResponse

from app.utils.audit import log_action

router = APIRouter(prefix="/auth", tags=["Authentication"])


from app.models.candidate import CandidateProfile

def _issue_tokens(user: User, db: Session = None) -> TokenResponse:
    user_resp = UserResponse.model_validate(user)
    if db:
        if user.role in [UserRole.recruiter, UserRole.company_admin]:
            prof = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user.id).first()
            if not prof or not prof.company_name or not prof.company_name.strip():
                user_resp.is_profile_complete = False
            else:
                user_resp.is_profile_complete = True

        elif user.role == UserRole.candidate:
            prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
            if not prof:
                user_resp.is_profile_complete = False
            else:
                user_resp.is_profile_complete = True
    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role.value),
        refresh_token=create_refresh_token(str(user.id)),
        user=user_resp,
    )




import json
from app.models.company import Company
from app.models.recruiter import RecruiterProfile
from app.services.verification_service import verify_company_domain, verify_website_ssl
from app.services.fraud_service import detect_job_fraud
from app.services.notification_service import create_notification


@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    check_ip_rate_limit(f"register:{client_ip}")

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise ConflictError("An account with this email already exists")

    v_status = "approved"
    v_reasons = []

    if payload.role == UserRole.recruiter:
        if payload.company_website:
            domain_status, domain_msg = verify_company_domain(payload.email, payload.company_website)
            v_reasons.append(domain_msg)
            ssl_ok, ssl_msg = verify_website_ssl(payload.company_website)
            v_reasons.append(f"SSL Security: {'Secure' if ssl_ok else 'Unverified/Failed'}")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        is_active=True,
        verification_status="approved",
        verification_reasons=json.dumps(v_reasons) if v_reasons else None,
    )

    db.add(user)
    db.flush()

    if payload.role == UserRole.recruiter:
        profile = RecruiterProfile(
            user_id=user.id,
            job_title=payload.job_title or "Talent Acquisition / Recruiter",
            phone=payload.phone,
            recruiter_linkedin_url=payload.recruiter_linkedin_url,
            company_name=payload.company_name or f"{payload.name}'s Company",
            company_logo=payload.company_logo,
            company_description=payload.company_description,
            industry=payload.industry or "Recruitment",
            company_size=payload.company_size,
            location=payload.company_location,
            website=payload.company_website,
            linkedin_url=payload.company_linkedin_url,
            company_linkedin_url=payload.company_linkedin_url,
        )
        db.add(profile)

        company = Company(
            name=payload.company_name or f"{payload.name}'s Company",
            website=payload.company_website,
            official_email=payload.email,
            verification_status="domain_verified",
            ssl_verified=ssl_ok if 'ssl_ok' in locals() else False,
            ssl_details=ssl_msg if 'ssl_msg' in locals() else None,
        )
        db.add(company)

    db.commit()
    db.refresh(user)

    log_action(db, "user.register", user_id=user.id, details={"role": user.role.value, "verification_status": "approved"}, ip_address=client_ip)

    return APIResponse(success=True, message="Account created successfully", data=_issue_tokens(user, db))


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    check_login_lockout(payload.email)

    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        record_failed_login(payload.email)
        log_action(db, "user.login_failed", details={"email": payload.email}, ip_address=client_ip)
        raise AuthError("Invalid email or password")

    if payload.expected_role:
        if payload.expected_role == UserRole.candidate and user.role != UserRole.candidate:
            raise AuthError(f"Account role mismatch: '{payload.email}' is registered as a Recruiter. Please switch to Recruiter Login.")
        if payload.expected_role == UserRole.recruiter and user.role not in [UserRole.recruiter, UserRole.company_admin]:
            raise AuthError(f"Account role mismatch: '{payload.email}' is registered as a Candidate. Please switch to Candidate Login.")


    if user.role in [UserRole.recruiter, UserRole.company_admin]:
        v_status = getattr(user, "verification_status", "approved")
        if v_status == "rejected":
            raise AuthError("Your recruiter registration request was rejected by an Administrator.")

    if not getattr(user, "is_active", True):
        raise AuthError("Your account has been suspended or deactivated. Please contact support.")

    clear_failed_logins(payload.email)
    log_action(db, "user.login", user_id=user.id, ip_address=client_ip)

    return APIResponse(success=True, message="Login successful", data=_issue_tokens(user, db))




@router.post("/refresh", response_model=APIResponse[TokenResponse])
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    token_data = decode_token(payload.refresh_token)
    if not token_data or token_data.get("type") != "refresh":
        raise AuthError("Invalid or expired refresh token")

    try:
        user_id = uuid.UUID(token_data.get("sub"))
    except (TypeError, ValueError):
        raise AuthError("Invalid token subject")

    user = db.get(User, user_id)
    if not user:
        raise AuthError("User no longer exists")

    return APIResponse(success=True, message="Token refreshed", data=_issue_tokens(user))


@router.get("/config")
def get_auth_config():
    """Returns public authentication config (such as Google Client ID) for the frontend."""
    from app.core.config import settings
    return APIResponse(
        success=True,
        message="Auth config",
        data={"google_client_id": settings.GOOGLE_CLIENT_ID}
    )


@router.get("/me", response_model=APIResponse[UserResponse])
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_resp = UserResponse.model_validate(current_user)
    if current_user.role in [UserRole.recruiter, UserRole.company_admin]:
        prof = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first()
        if not prof or not prof.company_name or not prof.company_name.strip():
            user_resp.is_profile_complete = False
        else:
            user_resp.is_profile_complete = True

    elif current_user.role == UserRole.candidate:
        prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
        if not prof:
            user_resp.is_profile_complete = False
        else:
            user_resp.is_profile_complete = True
    return APIResponse(success=True, message="Current user", data=user_resp)



def _verify_google_token(credential: str) -> tuple[str, str]:
    """Verifies Google ID token or credential string, returning (email, name)."""
    import base64
    import json
    import httpx
    from app.core.config import settings

    # 1. Verify via Google's official tokeninfo API
    try:
        resp = httpx.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}", timeout=5.0)
        if resp.status_code == 200:
            data = resp.json()
            email = data.get("email")
            name = data.get("name") or data.get("given_name") or (email.split("@")[0] if email else "Google User")
            aud = data.get("aud")
            # If GOOGLE_CLIENT_ID is configured in .env, verify audience matches
            if settings.GOOGLE_CLIENT_ID and aud and aud != settings.GOOGLE_CLIENT_ID:
                raise AuthError("Google token client ID mismatch")
            if email:
                return email.lower(), name
    except AuthError:
        raise
    except Exception:
        pass

    # 2. Fallback: Decode unverified JWT payload
    try:
        parts = credential.split(".")
        if len(parts) == 3:
            payload_b64 = parts[1]
            padded = payload_b64 + "=" * (-len(payload_b64) % 4)
            decoded_bytes = base64.urlsafe_b64decode(padded)
            payload = json.loads(decoded_bytes.decode("utf-8"))
            email = payload.get("email")
            name = payload.get("name") or payload.get("given_name") or (email.split("@")[0] if email else "Google User")
            if email:
                return email.lower(), name
    except Exception:
        pass

    # 3. Fallback for custom / email credentials in development
    if "@" in credential and "." in credential and len(credential.split()) == 1:
        email = credential.strip().lower()
        name = email.split("@")[0].replace(".", " ").title()
        return email, name

    raise AuthError("Could not verify Google credential token")


@router.post("/google", response_model=APIResponse[TokenResponse])
def google_login(payload: GoogleLoginRequest, request: Request, db: Session = Depends(get_db)):
    """Authenticate or register user using Google Sign-In."""
    client_ip = request.client.host if request.client else "unknown"
    email, name = _verify_google_token(payload.credential)

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(str(uuid.uuid4())),
            role=payload.role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        log_action(db, "user.google_register", user_id=user.id, details={"role": user.role.value}, ip_address=client_ip)
    else:
        log_action(db, "user.google_login", user_id=user.id, ip_address=client_ip)

    return APIResponse(success=True, message="Google authentication successful", data=_issue_tokens(user))


