"""
email_validation.py — strict email format and domain structure validator.
"""
import re
from app.core.exceptions import AppError

# Strict RFC email pattern requiring valid domain name and standard TLD
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$"
)

# Reserved or invalid local/test TLDs that are not real email domains
INVALID_TLDS = {"test", "example", "invalid", "localhost", "local"}


def validate_strict_email(email: str) -> str:
    """
    Strictly validates an email string.
    Raises AppError (HTTP 400) if format, syntax, or TLD is invalid.
    """
    if not email or not isinstance(email, str):
        raise AppError("Email address is required.", "INVALID_EMAIL", 400)

    cleaned = email.strip().lower()

    if not EMAIL_REGEX.match(cleaned):
        raise AppError(
            f"Invalid email address format: '{email}'. Please enter a valid email address (e.g. user@example.com).",
            "INVALID_EMAIL",
            400,
        )

    if ".." in cleaned or ".@" in cleaned or "@." in cleaned:
        raise AppError(
            f"Invalid email address syntax: '{email}' contains invalid punctuation sequences.",
            "INVALID_EMAIL",
            400,
        )

    parts = cleaned.split("@")
    if len(parts) != 2:
        raise AppError("Email address must contain exactly one '@' character.", "INVALID_EMAIL", 400)

    domain = parts[1]
    domain_parts = domain.split(".")

    if len(domain_parts) < 2 or not domain_parts[-1]:
        raise AppError(f"Email domain '{domain}' is incomplete or missing a valid domain extension.", "INVALID_EMAIL", 400)

    tld = domain_parts[-1]
    if tld in INVALID_TLDS:
        raise AppError(f"Email domain '.{tld}' is not a valid email server domain. Please use a valid email address.", "INVALID_EMAIL", 400)

    return cleaned


PUBLIC_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "ymail.com", "hotmail.com", "outlook.com",
    "live.com", "icloud.com", "aol.com", "protonmail.com", "zoho.com",
    "mail.com", "gmx.com", "rediffmail.com"
}


def validate_role_email(email: str, role_str: str) -> str:
    """
    Validates email format and enforces role-specific domain rules:
    - Recruiter: Must use a company domain (not in PUBLIC_EMAIL_DOMAINS).
    - Candidate: Personal / public domains like @gmail.com are permitted.
    """
    cleaned = validate_strict_email(email)
    domain = cleaned.split("@")[1].lower()

    if role_str in ["recruiter", "company_admin"]:
        if domain in PUBLIC_EMAIL_DOMAINS:
            raise AppError(
                f"Recruiters must use a company email address (e.g. name@companyname.com). Public email domains like @{domain} are not permitted for Recruiter accounts.",
                "RECRUITER_EMAIL_DOMAIN_INVALID",
                400,
            )
    return cleaned
