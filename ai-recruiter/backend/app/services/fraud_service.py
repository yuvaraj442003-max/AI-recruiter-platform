"""
Fraud Detection Service — analyzes job postings for scam indicators, payment demands, and suspicious language.
"""
import re
import json
from typing import Dict, Any, List


SCAM_KEYWORDS = [
    (r"registration fee", 35, "Requests registration or application fee"),
    (r"interview fee", 35, "Requests interview processing fee"),
    (r"security deposit", 30, "Requires security deposit"),
    (r"training fee", 25, "Requires upfront training fee"),
    (r"pay before", 30, "Requests payment before hiring"),
    (r"send money", 35, "Requests money transfer"),
    (r"bank account details", 25, "Requests bank credentials or account details upfront"),
    (r"otp|one time password", 40, "Requests OTP or password sharing"),
    (r"credit card|debit card", 30, "Requests payment card details"),
    (r"earn \$?\d+,\d+ (a|per) (day|hour)", 25, "Unrealistic high earnings promise per day/hour"),
    (r"no experience required.*\$[1-9]\d{4,}", 20, "Absurd salary for zero experience"),
    (r"contact (via|on) whatsapp only", 15, "Requests communication via personal messaging apps only"),
    (r"contact (via|on) telegram only", 20, "Requests application via Telegram only"),
    (r"send resume to .*@gmail\.com", 10, "Directs candidates to submit resume to personal gmail instead of portal"),
]


def detect_job_fraud(
    title: str,
    description: str,
    salary_range: str = None,
    company_website: str = None,
    recruiter_email: str = None,
) -> Dict[str, Any]:
    """
    Scans job title, description, and metadata for scam indicators.
    Returns:
    {
        "risk_score": float (0-100),
        "risk_level": "LOW" | "MEDIUM" | "HIGH",
        "reasons": list[str],
    }
    """
    full_text = f"{title or ''}\n{description or ''}\n{salary_range or ''}".lower()
    score = 0
    reasons: List[str] = []

    for pattern, weight, reason in SCAM_KEYWORDS:
        if re.search(pattern, full_text, re.IGNORECASE):
            score += weight
            if reason not in reasons:
                reasons.append(reason)

    # Additional check: Unrealistic salary check
    if salary_range:
        sal_lower = salary_range.lower()
        if re.search(r"(\$|₹|eur|gbp)?\s*([5-9]\d{5,}|[1-9]\d{6,})", sal_lower) and "year" not in sal_lower and "annum" not in sal_lower:
            score += 20
            reasons.append("Extremely high unverified compensation amount")

    # Additional check: Suspicious generic contact
    if recruiter_email and ("@gmail.com" in recruiter_email or "@yahoo.com" in recruiter_email) and ("pay" in full_text or "fee" in full_text):
        score += 15
        reasons.append("Recruiter uses public email domain while discussing financial requirements")

    # Cap score at 100
    final_score = min(100.0, float(score))

    if final_score >= 60.0:
        risk_level = "HIGH"
    elif final_score >= 30.0:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if not reasons:
        reasons = ["No suspicious scam indicators detected."]

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "reasons": reasons,
    }
