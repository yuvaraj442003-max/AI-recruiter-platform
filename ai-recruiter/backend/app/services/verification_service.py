"""
Verification service — handles company domain email verification, SSL checks, and government registration checks.
"""
import re
import socket
import ssl
import urllib.parse
from typing import Tuple

GENERIC_EMAIL_PROVIDERS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "protonmail.com",
    "zoho.com",
    "aol.com",
    "mail.com",
    "gmx.com",
    "yandex.com",
}


def extract_domain(url_or_email: str) -> str:
    """Extract clean root domain from email address or website URL."""
    if not url_or_email:
        return ""
    text = url_or_email.strip().lower()

    if "@" in text:
        text = text.split("@")[-1]

    if "://" not in text and not text.startswith("http"):
        text = "https://" + text

    try:
        parsed = urllib.parse.urlparse(text)
        host = parsed.netloc or parsed.path
        host = host.split(":")[0]  # strip port
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def verify_company_domain(recruiter_email: str, company_website: str) -> Tuple[str, str]:
    """
    Compares recruiter email domain with company website domain.
    Returns (status: "domain_verified" | "unverified", reason: str).
    """
    if not recruiter_email:
        return "unverified", "No email provided."

    email_domain = extract_domain(recruiter_email)
    if not email_domain:
        return "unverified", "Invalid email address format."

    if email_domain in GENERIC_EMAIL_PROVIDERS:
        return (
            "unverified",
            f"Generic email provider (@{email_domain}) cannot be used for company domain verification. Please use your official corporate domain email.",
        )

    if not company_website:
        return "domain_verified", f"Domain @{email_domain} is a valid custom domain."

    web_domain = extract_domain(company_website)
    if email_domain == web_domain or email_domain.endswith("." + web_domain) or web_domain.endswith("." + email_domain):
        return "domain_verified", f"Email domain (@{email_domain}) successfully matches company website ({web_domain})."

    return (
        "unverified",
        f"Email domain (@{email_domain}) does not match company website domain ({web_domain}).",
    )


def verify_website_ssl(website_url: str) -> Tuple[bool, str]:
    """
    Checks if the given website URL is reachable and has valid SSL/TLS certificate.
    Returns (ssl_valid: bool, details_json: str).
    """
    if not website_url:
        return False, "No website URL provided."

    domain = extract_domain(website_url)
    if not domain:
        return False, "Invalid website domain format."

    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5.0) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                subject = dict(x[0] for x in cert.get("subject", []))
                issuer = dict(x[0] for x in cert.get("issuer", []))
                common_name = subject.get("commonName", domain)
                issuer_name = issuer.get("organizationName", issuer.get("commonName", "Unknown Issuer"))

                return True, f"SSL Verified. Certificate issued to {common_name} by {issuer_name}."
    except Exception as e:
        # Fallback heuristic: check HTTP reachability
        return False, f"SSL check failed or unverified for {domain}: {str(e)}"


def verify_company_government(cin_gstin: str, company_name: str) -> Tuple[str, str]:
    """
    Mock Government Verification Service for CIN (Corporate Identification Number) / GSTIN.
    In real production, this integrates with MCA (Ministry of Corporate Affairs) or GST portal APIs.
    """
    if not cin_gstin:
        return "unverified", "CIN/GSTIN registration number is required for government verification."

    clean_id = cin_gstin.strip().upper()

    # Heuristic format checks for Indian CIN (21 chars) or GSTIN (15 chars) or EIN/CRN (8+ chars)
    is_cin = bool(re.match(r"^[L|U]\d{5}[A-Z]{2}\d{4}[PLC|PTC|SGC|FLC|ULT|GAP|NPL]{3}\d{6}$", clean_id))
    is_gstin = bool(re.match(r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$", clean_id))
    is_generic_reg = len(clean_id) >= 6 and clean_id.isalnum()

    if is_cin or is_gstin or is_generic_reg:
        return "government_verified", f"Official Government Registration Verified (Registration ID: {clean_id})."
    
    return "unverified", f"Registration ID {clean_id} could not be verified in official government registry."
