"""
Pydantic schemas used by the auth endpoints.
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.user import UserRole

# Admins are never created through public self-registration — only via the
# create_admin bootstrap script/service (app/services/admin_service.py) run
# by someone with server access. This is enforced below, not just by the
# frontend only offering candidate/recruiter as choices.
PUBLIC_REGISTRATION_ROLES = {UserRole.candidate, UserRole.recruiter}


from typing import Optional


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.candidate

    # Recruiter & Company Registration Details
    job_title: Optional[str] = None
    phone: Optional[str] = None
    recruiter_linkedin_url: Optional[str] = None
    company_name: Optional[str] = None
    company_website: Optional[str] = None
    company_linkedin_url: Optional[str] = None
    company_location: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    company_description: Optional[str] = None
    company_logo: Optional[str] = None

    @field_validator("email", mode="before")
    @classmethod
    def sanitize_and_validate_email(cls, v: str) -> str:
        from app.utils.email_validation import validate_strict_email
        return validate_strict_email(v)

    @field_validator("role")
    @classmethod
    def restrict_public_registration_role(cls, value: UserRole) -> UserRole:
        if value not in PUBLIC_REGISTRATION_ROLES:
            raise ValueError("role must be 'candidate' or 'recruiter'")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    expected_role: Optional[UserRole] = None

    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("expected_role", mode="before")
    @classmethod
    def sanitize_expected_role(cls, v):
        if not v or (isinstance(v, str) and not v.strip()):
            return None
        return v




class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: UserRole
    verification_status: Optional[str] = "approved"
    is_email_verified: Optional[bool] = False
    is_profile_complete: Optional[bool] = True
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)



class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshRequest(BaseModel):
    refresh_token: str


class GoogleLoginRequest(BaseModel):
    credential: str
    role: UserRole = UserRole.candidate

    @field_validator("role")
    @classmethod
    def restrict_public_registration_role(cls, value: UserRole) -> UserRole:
        if value not in PUBLIC_REGISTRATION_ROLES:
            raise ValueError("role must be 'candidate' or 'recruiter'")
        return value


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=128)


class VerifyEmailRequest(BaseModel):
    token: str = Field(min_length=1)


class ResendVerificationRequest(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)

    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("otp", mode="before")
    @classmethod
    def sanitize_otp(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return str(v)


class ResendOTPRequest(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


