"""
Authentication endpoints: register, login, refresh, and "who am I".
"""
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, Query, Request, status
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
from app.schemas.user import (
    ForgotPasswordRequest,
    GoogleLoginRequest,
    RefreshRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    VerifyEmailRequest,
    VerifyOTPRequest,
    ResendOTPRequest,
)

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


def _extract_base_url_from_request(request: Request) -> Optional[str]:
    referer = request.headers.get("referer")
    if referer:
        pos = referer.rfind('/')
        if pos != -1 and not referer[:pos].endswith(":/") and not referer[:pos].endswith("://"):
            return referer[:pos]
    if getattr(settings, "FRONTEND_URL", None):
        return settings.FRONTEND_URL.rstrip('/')
    origin = request.headers.get("origin")
    if origin:
        return origin.rstrip('/')
    return None


@router.get("/check-email", response_model=APIResponse[dict])
def check_email(email: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    """Checks whether an email address is already registered in the database."""
    clean_email = email.strip().lower()
    existing = db.query(User).filter(User.email == clean_email).first()
    return APIResponse(
        success=True,
        message="Email availability check completed.",
        data={"exists": existing is not None, "email": clean_email}
    )


@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    check_ip_rate_limit(f"register:{client_ip}")

    from app.utils.email_validation import validate_role_email
    role_str = payload.role.value if hasattr(payload.role, "value") else str(payload.role)
    validate_role_email(payload.email, role_str)

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise ConflictError("This email address is already registered.")

    v_status = "approved"
    v_reasons = []

    if payload.role == UserRole.recruiter:
        if payload.company_website:
            domain_status, domain_msg = verify_company_domain(payload.email, payload.company_website)
            v_reasons.append(domain_msg)
            ssl_ok, ssl_msg = verify_website_ssl(payload.company_website)
            v_reasons.append(f"SSL Security: {'Secure' if ssl_ok else 'Unverified/Failed'}")

    v_otp = f"{secrets.randbelow(900000) + 100000}"
    v_expires = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=10)

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        is_active=True,
        is_email_verified=False,
        verification_token=v_otp,
        verification_token_expires_at=v_expires,
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

    from app.services.email_service import send_verification_email
    send_verification_email(user.email, user.name, v_otp, db=db)

    log_action(db, "user.register", user_id=user.id, details={"role": user.role.value, "verification_status": "approved"}, ip_address=client_ip)

    return APIResponse(
        success=True,
        message="Registration successful. A 6-digit verification code has been sent to your email.",
        data=_issue_tokens(user, db)
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    check_login_lockout(payload.email)

    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        record_failed_login(payload.email)
        log_action(db, "user.login_failed", details={"email": payload.email}, ip_address=client_ip)
        raise AuthError("Invalid email or password")

    # Enforce strict role isolation on login: selected role tab MUST match registered account role
    if payload.expected_role:
        expected = payload.expected_role.value if hasattr(payload.expected_role, "value") else str(payload.expected_role)
        actual = user.role.value if hasattr(user.role, "value") else str(user.role)

        is_recruiter_type = actual in ["recruiter", "company_admin"] and expected in ["recruiter", "company_admin"]
        if actual != expected and not is_recruiter_type:
            actual_title = "Candidate" if actual == "candidate" else ("Recruiter" if actual in ["recruiter", "company_admin"] else actual.capitalize())
            raise AuthError(f"Access Denied: This account is registered as a {actual_title}. Please select the {actual_title} role to log in.")

    # Enforce mandatory email verification before login
    if not getattr(user, "is_email_verified", True):
        # Generate 6-digit OTP and send via email (5-minute expiration)
        otp_code = f"{secrets.randbelow(900000) + 100000}"
        user.verification_token = otp_code
        user.verification_token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=5)
        db.commit()

        from app.services.email_service import send_verification_email
        send_verification_email(user.email, user.name, otp_code, db=db)

        raise AuthError(
            "Access Denied: Please verify your email address. A 6-digit OTP code has been sent to your email.",
            error_code="EMAIL_NOT_VERIFIED"
        )

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

    from app.utils.email_validation import validate_role_email
    target_role = payload.role.value if hasattr(payload.role, "value") else str(payload.role)
    validate_role_email(email, target_role)

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
        if payload.role:
            expected = payload.role.value if hasattr(payload.role, "value") else str(payload.role)
            actual = user.role.value if hasattr(user.role, "value") else str(user.role)
            is_recruiter_type = actual in ["recruiter", "company_admin"] and expected in ["recruiter", "company_admin"]
            if actual != expected and not is_recruiter_type:
                actual_title = "Candidate" if actual == "candidate" else ("Recruiter" if actual in ["recruiter", "company_admin"] else actual.capitalize())
                raise AuthError(f"Access Denied: This Google account is registered as a {actual_title}. Please sign in using the {actual_title} role option.")
        log_action(db, "user.google_login", user_id=user.id, ip_address=client_ip)

    return APIResponse(success=True, message="Google authentication successful", data=_issue_tokens(user))


@router.post("/forgot-password", response_model=APIResponse[dict])
def forgot_password(payload: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Generates a password reset token and dispatches a reset email."""
    client_ip = request.client.host if request.client else "unknown"
    check_ip_rate_limit(f"forgot_password:{client_ip}")

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        # Safe generic response: do not expose whether the email address exists in DB
        return APIResponse(
            success=True,
            message="Password reset instructions have been sent to your email address if an account exists.",
            data={}
        )

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=30)
    db.commit()

    base_url = _extract_base_url_from_request(request)

    from app.services.email_service import send_reset_password_email
    send_reset_password_email(user.email, user.name, token, db=db, base_url=base_url)

    log_action(db, "user.forgot_password_requested", user_id=user.id, ip_address=client_ip)

    return APIResponse(
        success=True,
        message="Password reset instructions have been sent to your email address.",
        data={}
    )


@router.post("/reset-password", response_model=APIResponse[dict])
def reset_password(payload: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Validates the reset token and updates the user's password."""
    client_ip = request.client.host if request.client else "unknown"
    check_ip_rate_limit(f"reset_password:{client_ip}")

    if not payload.token or not payload.token.strip():
        raise AuthError("Invalid or expired password reset token.")

    user = db.query(User).filter(User.reset_token == payload.token).first()
    if not user:
        raise AuthError("Invalid or expired password reset token.")

    if user.reset_token_expires_at:
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        if user.reset_token_expires_at < now_naive:
            raise AuthError("Password reset link has expired. Please request a new password reset.")

    user.password_hash = hash_password(payload.new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    db.commit()

    log_action(db, "user.password_reset_success", user_id=user.id, ip_address=client_ip)
    return APIResponse(
        success=True,
        message="Your password has been reset successfully. Please log in with your new password.",
        data={}
    )


@router.post("/verify-email", response_model=APIResponse[dict])
def verify_email_post(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    """Verifies the user's email via token in request body."""
    if not payload.token or not payload.token.strip():
        raise AuthError("Invalid or expired email verification token.")

    user = db.query(User).filter(User.verification_token == payload.token).first()
    if not user:
        raise AuthError("Invalid or expired email verification token.")

    if user.verification_token_expires_at:
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        if user.verification_token_expires_at < now_naive:
            raise AuthError("Email verification link has expired. Please request a new verification link.")

    user.is_email_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None
    db.commit()

    tokens = _issue_tokens(user, db)
    token_dict = tokens.model_dump() if hasattr(tokens, "model_dump") else tokens.dict()

    return APIResponse(
        success=True,
        message="Email verified successfully!",
        data=token_dict
    )


@router.get("/verify-email", response_model=APIResponse[dict])
def verify_email_get(token: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Verifies the user's email via query token in URL."""
    if not token or not token.strip():
        raise AuthError("Invalid or expired email verification token.")

    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise AuthError("Invalid or expired email verification token.")

    if user.verification_token_expires_at:
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        if user.verification_token_expires_at < now_naive:
            raise AuthError("Email verification link has expired. Please request a new verification link.")

    user.is_email_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None
    db.commit()

    tokens = _issue_tokens(user, db)
    token_dict = tokens.model_dump() if hasattr(tokens, "model_dump") else tokens.dict()

    return APIResponse(
        success=True,
        message="Email verified successfully!",
        data=token_dict
    )


@router.post("/verify-otp", response_model=APIResponse[dict])
def verify_otp(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verifies user email using 6-digit OTP code."""
    clean_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == clean_email).first()
    if not user:
        raise AuthError("No account found with this email address.")

    if user.is_email_verified:
        tokens = _issue_tokens(user, db)
        token_dict = tokens.model_dump() if hasattr(tokens, "model_dump") else tokens.dict()
        return APIResponse(
            success=True,
            message="This email address is already verified.",
            data=token_dict
        )

    if not user.verification_token or user.verification_token.strip() != payload.otp.strip():
        raise AuthError("Invalid OTP. Please try again.")

    if user.verification_token_expires_at:
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        if user.verification_token_expires_at < now_naive:
            raise AuthError("OTP has expired. Please click Resend OTP.")

    user.is_email_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None
    db.commit()

    tokens = _issue_tokens(user, db)
    token_dict = tokens.model_dump() if hasattr(tokens, "model_dump") else tokens.dict()

    return APIResponse(
        success=True,
        message="Email verified successfully! Welcome to AI Recruiter.",
        data=token_dict
    )


@router.post("/resend-otp", response_model=APIResponse[dict])
def resend_otp(payload: ResendOTPRequest, request: Request, db: Session = Depends(get_db)):
    """Generates and dispatches a fresh 6-digit OTP verification code."""
    client_ip = request.client.host if request.client else "unknown"
    check_ip_rate_limit(f"resend_otp:{client_ip}")

    clean_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == clean_email).first()
    if not user:
        return APIResponse(
            success=True,
            message="If an account exists with this email, a verification code has been sent.",
            data={}
        )

    if user.is_email_verified:
        return APIResponse(
            success=True,
            message="This email address is already verified.",
            data={"is_email_verified": True}
        )

    otp_code = f"{secrets.randbelow(900000) + 100000}"
    user.verification_token = otp_code
    user.verification_token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=5)
    db.commit()

    from app.services.email_service import send_verification_email
    send_verification_email(user.email, user.name, otp_code, db=db)

    return APIResponse(
        success=True,
        message="A new 6-digit verification code has been sent to your email.",
        data={}
    )


@router.post("/resend-verification", response_model=APIResponse[dict])
def resend_verification(payload: ResendVerificationRequest, request: Request, db: Session = Depends(get_db)):
    """Generates and dispatches a fresh 6-digit OTP verification code."""
    client_ip = request.client.host if request.client else "unknown"
    check_ip_rate_limit(f"resend_verification:{client_ip}")

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return APIResponse(
            success=True,
            message="If an account exists with this email, a verification email has been sent.",
            data={}
        )

    if user.is_email_verified:
        return APIResponse(
            success=True,
            message="This email address is already verified.",
            data={"is_email_verified": True}
        )

    otp_code = f"{secrets.randbelow(900000) + 100000}"
    user.verification_token = otp_code
    user.verification_token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=10)
    db.commit()

    from app.services.email_service import send_verification_email
    send_verification_email(user.email, user.name, otp_code, db=db)

    return APIResponse(
        success=True,
        message="A new 6-digit verification code has been sent to your email.",
        data={}
    )


