"""
skill_extractor.py — turns raw resume text into structured fields:
name, email, phone, skills, experience_years, education, summary.

Skill matching is alias-based (see skills_data.py) rather than a
statistical classifier — this keeps it fast, deterministic, and easy
to extend, which matters more than recall here since a human recruiter
always reviews the result.
"""
import re

from app.nlp.skills_data import ALIAS_INDEX
from app.nlp.text_processor import clean_text, extract_entities, sentence_split

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{3,4})")
EXPERIENCE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)\b(?:\s*of)?(?:\s*experience)?", re.IGNORECASE
)

EDUCATION_KEYWORDS = [
    "bachelor", "master", "b.tech", "m.tech", "b.sc", "m.sc", "bsc", "msc",
    "phd", "ph.d", "mba", "b.e.", "b.e ", "diploma", "university", "college",
    "institute of technology", "school of",
]

# Sorted longest-alias-first so multi-word skills ("machine learning")
# match before a shorter overlapping alias could steal the match.
_SORTED_ALIASES = sorted(ALIAS_INDEX.keys(), key=len, reverse=True)
_SKILL_PATTERNS = [
    (alias, re.compile(r"(?<![\w+#.])" + re.escape(alias) + r"(?![\w+#])", re.IGNORECASE))
    for alias in _SORTED_ALIASES
]


def extract_email(text: str) -> str | None:
    match = EMAIL_RE.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    for candidate in PHONE_RE.findall(text):
        digits = re.sub(r"\D", "", candidate)
        if 7 <= len(digits) <= 15:
            return candidate.strip()
    return None


_INVALID_NAME_TERMS = {
    "resume", "curriculum", "vitae", "cv", "summary", "profile", "contact",
    "personal", "experience", "education", "skills", "projects", "page",
    "nadu", "state", "india", "district", "street", "road", "nagar", "tamil",
    "coimbatore", "chennai", "bangalore", "mumbai", "delhi", "hyderabad",
}

def extract_name(text: str, entities: dict[str, list[str]]) -> str | None:
    """Extract candidate name from resume header / first lines."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return None

    gpe_terms = {g.lower() for g in entities.get("GPE", [])}
    for gpe in list(gpe_terms):
        for part in gpe.split():
            gpe_terms.add(part)

    # 1. Primary Strategy: Check the top 3 non-empty lines for the candidate full name.
    # Resumes standardly start with candidate's full name on line 1.
    for line in lines[:3]:
        clean_line = re.sub(r"^[^\w]+", "", line).strip()
        words = clean_line.split()
        words_lower = [w.lower() for w in words]

        # Ignore lines with phone numbers, emails, URLs, or special dividers
        if re.search(r"[\d@|/:\\]|http|www\.|github|linkedin", clean_line, re.IGNORECASE):
            continue

        # Ignore section headings or lines containing known location words or invalid header terms
        if SECTION_HEADING_RE.match(clean_line):
            continue

        if any(w in _INVALID_NAME_TERMS or w in _KNOWN_DISTRICTS or w in gpe_terms for w in words_lower):
            continue

        if 1 <= len(words) <= 5:
            return clean_line

    # 2. Secondary Strategy: Check PERSON entities extracted by spaCy, filtering out locations & invalid words
    head = text[:400]
    for person in entities.get("PERSON", []):
        person_clean = person.strip()
        p_words = [w.lower() for w in person_clean.split()]
        if not p_words or len(p_words) > 5:
            continue
        if (
            person_clean in head
            and not any(w in _KNOWN_DISTRICTS or w in _INVALID_NAME_TERMS or w in gpe_terms for w in p_words)
            and not re.search(r"[\d@|/:\\]|http|www\.|github|linkedin", person_clean, re.IGNORECASE)
        ):
            return person_clean

    # 3. Fallback Strategy: First line under 5 words without digits/email
    for line in lines[:5]:
        clean_line = re.sub(r"^[^\w]+", "", line).strip()
        words = clean_line.split()
        words_lower = [w.lower() for w in words]
        if (
            1 <= len(words) <= 5
            and not re.search(r"[\d@]", clean_line)
            and not SECTION_HEADING_RE.match(clean_line)
            and not any(w in _INVALID_NAME_TERMS or w in _KNOWN_DISTRICTS for w in words_lower)
        ):
            return clean_line

    return None


_PINCODE_DISTRICT_RE = re.compile(
    r"([A-Za-z\s,]+?)\s*(?:district|dist|dt)?\s*,?\s*\b\d{6}\b",
    re.IGNORECASE,
)

_KNOWN_DISTRICTS = {
    "salem", "namakkal", "kovilpatti", "chennai", "coimbatore", "madurai", "trichy",
    "tiruchirappalli", "erode", "tiruppur", "thanjavur", "vellore", "thoothukudi",
    "tiruvarur", "kanyakumari", "dindigul", "karur", "krishnagiri", "dharmapuri",
    "theni", "ramanathapuram", "tirunelveli", "kanchipuram", "tiruvallur", "cuddalore",
    "tamil nadu", "karnataka", "kerala", "andhra pradesh", "telangana", "maharashtra",
    "bangalore", "bengaluru", "hyderabad", "secunderabad", "pune", "mumbai", "delhi", "noida", "gurgaon", "gurugram",
    "kolkata", "ahmedabad", "jaipur", "kochi", "trivandrum", "thiruvananthapuram", "chandigarh", "indore", "bhopal",
    "nagpur", "visakhapatnam", "vizag", "mysore", "mysuru", "san francisco", "sf", "seattle", "new york", "nyc",
    "austin", "london", "toronto", "vancouver", "san jose", "sunnyvale", "mountain view", "chicago", "boston",
}


def extract_location(text: str, entities: dict[str, list[str]], skills: list[str], address: str | None = None) -> str | None:
    """Extract District / City location from address block, pin codes, GPE entities, or header."""
    # 1. Primary: Extract from the explicit address block if present
    if address:
        # 1a. Check for known districts/cities in the address block
        for line in reversed(address.splitlines()):
            # Remove punctuation and split into clean words
            cleaned_line = re.sub(r"[^\w\s]", " ", line)
            for word in cleaned_line.split():
                clean_w = word.strip()
                if clean_w.lower() in _KNOWN_DISTRICTS:
                    return clean_w.title()

        # 1b. Check for PIN code pattern inside address block
        pin_match = _PINCODE_DISTRICT_RE.search(address)
        if pin_match:
            candidate_dist = pin_match.group(1).strip(" ,.-")
            parts = [p.strip() for p in candidate_dist.split(",") if p.strip()]
            if parts:
                dist = parts[-1].strip()
                if len(dist) >= 3 and dist.lower() not in {"street", "nagar", "road", "door"}:
                    return dist.title()

    # 2. Look for district/city immediately preceding a 6-digit PIN code anywhere in document
    pin_match = _PINCODE_DISTRICT_RE.search(text)
    if pin_match:
        candidate_dist = pin_match.group(1).strip(" ,.-")
        parts = [p.strip() for p in candidate_dist.split(",") if p.strip()]
        if parts:
            dist = parts[-1].strip()
            if len(dist) >= 3 and dist.lower() not in {"street", "nagar", "road", "door"}:
                return dist.title()

    # 3. Check GPE entities found near the TOP of the document (contact info header area, first 500 chars)
    head_text = text[:500].lower()
    skill_names_lower = {s.lower() for s in skills}
    gpes = [g.strip() for g in entities.get("GPE", []) if g.lower() not in skill_names_lower and g.lower() not in ALIAS_INDEX]

    for place in gpes:
        if place.lower() in head_text and place.lower() in _KNOWN_DISTRICTS:
            return place.title()

    # 4. Check all GPE entities for known major district/city names
    for place in gpes:
        if place.lower() in _KNOWN_DISTRICTS:
            return place.title()

    # 5. Fallback to first valid GPE entity
    if gpes:
        for g in reversed(gpes):
            if len(g) >= 4:
                return g.title()
        return gpes[0].title()

    return None


_WORK_DATE_RE = re.compile(
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
    r"\s+\d{4}",
    re.IGNORECASE,
)

_YEAR_RANGE_RE = re.compile(
    r"\b(19\d\d|20\d\d)\s*[-–—to]+\s*(present|current|now|19\d\d|20\d\d)\b",
    re.IGNORECASE,
)

_WORK_HEADING_RE = re.compile(
    r"^\s*(internship experience|work experience|experience|employment history|work history|professional experience|employment)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_FRESHER_STUDENT_RE = re.compile(
    r"\b(fresher|student|final[- ]year|entry[- ]level|graduating in 20\d\d)\b",
    re.IGNORECASE,
)


def _extract_work_section_text(text: str) -> str:
    """Isolates lines under work / internship experience headings, stopping at education or projects."""
    heading_match = _WORK_HEADING_RE.search(text)
    if not heading_match:
        return ""
    after_heading = text[heading_match.end():]
    work_lines: list[str] = []
    for line in after_heading.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if _NEXT_SECTION_RE.match(stripped) and not _WORK_HEADING_RE.match(stripped):
            break
        work_lines.append(stripped)
    return "\n".join(work_lines)


def extract_experience_years(text: str) -> float | None:
    """
    Extracts professional work experience in years.
    Prioritizes explicit 'X years of experience' phrases and work/internship sections.
    Excludes education degree year ranges (e.g. SSLC, HSC, B.Sc degree years).
    """
    if not text:
        return 0.0

    # 1. First check explicit 'X years of experience' phrases
    matches = EXPERIENCE_RE.findall(text)
    if matches:
        return max(float(m) for m in matches)

    from datetime import date
    today_year = date.today().year

    work_text = _extract_work_section_text(text)
    is_fresher_or_student = bool(_FRESHER_STUDENT_RE.search(text.lower()))

    month_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    # 2. If student / fresher with internship experience: calculate internship months or return 0.0
    if is_fresher_or_student or (work_text and "intern" in work_text.lower() and not re.search(r"\b(senior|lead|manager)\b", text, re.IGNORECASE)):
        target_for_dates = work_text if work_text.strip() else text
        dates_found: list[date] = []
        for m in _WORK_DATE_RE.finditer(target_for_dates):
            parts = m.group(0).split()
            try:
                month = month_map[parts[0][:3].lower()]
                year = int(parts[1])
                if 1990 <= year <= today_year:
                    dates_found.append(date(year, month, 1))
            except (IndexError, ValueError, KeyError):
                continue

        if len(dates_found) >= 2:
            earliest = min(dates_found)
            latest = max(dates_found)
            days = (latest - earliest).days
            years = round(days / 365.25, 1)
            if years > 0.5 and is_fresher_or_student:
                return 0.0
            return max(0.0, years)
        return 0.0

    # 3. Check year ranges (e.g. "2020 - 2024") ONLY within the WORK / INTERNSHIP section
    if work_text.strip():
        year_ranges = _YEAR_RANGE_RE.findall(work_text)
        if year_ranges:
            spans = []
            for start_str, end_str in year_ranges:
                try:
                    start_yr = int(start_str)
                    end_yr = today_year if end_str.lower() in ("present", "current", "now") else int(end_str)
                    if 1990 <= start_yr <= today_year and end_yr >= start_yr:
                        spans.append(end_yr - start_yr)
                except ValueError:
                    continue
            if spans:
                total_years = float(sum(spans))
                if total_years > 0:
                    return round(total_years, 1)

    # 4. Fallback for work section date scan
    if work_text.strip():
        dates_found = []
        for m in _WORK_DATE_RE.finditer(work_text):
            parts = m.group(0).split()
            try:
                month = month_map[parts[0][:3].lower()]
                year = int(parts[1])
                if 1990 <= year <= today_year:
                    dates_found.append(date(year, month, 1))
            except (IndexError, ValueError, KeyError):
                continue
        if dates_found:
            earliest = min(dates_found)
            years = (date.today() - earliest).days / 365.25
            return round(max(0.0, years), 1) if years >= 0.25 else 0.0

    return 0.0 if is_fresher_or_student else None


def extract_education(text: str) -> str | None:
    """Extract education by first finding the EDUCATION section heading,
    then pulling the lines that follow it — until the next section heading.
    Falls back to the keyword-scan approach only if no heading is found."""
    # --- Preferred: find the EDUCATION heading and grab what follows ---
    heading_match = _EDUCATION_HEADING_RE.search(text)
    if heading_match:
        after_heading = text[heading_match.end():]
        edu_lines: list[str] = []
        for line in after_heading.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # Stop at the next recognizable section heading
            if _NEXT_SECTION_RE.match(stripped):
                break
            edu_lines.append(stripped)
        if edu_lines:
            return "\n".join(edu_lines[:12])  # up to 12 lines of education detail

    # --- Fallback: keyword scan (only if no EDUCATION heading found) ---
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    hits = [
        line for line in lines
        if any(keyword in line.lower() for keyword in EDUCATION_KEYWORDS)
    ]
    return "\n".join(hits[:6]) if hits else None


_SKILLS_HEADING_RE = re.compile(
    r"^\s*(skills|technical skills|key skills|core competencies|competencies|technologies|tools & technologies|extracted skills|skills & expertise)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

def extract_skills(text: str) -> list[str]:
    lower_text = f" {text.lower()} "
    found: set[str] = set()

    _FRAMEWORK_JS_PATTERN = re.compile(
        r"\b(react|node|vue|express|next|nest|nuxt|chart|three|vite|angular|ember|backbone|knockout)\s*[\./(-]?\s*js\b",
        re.IGNORECASE,
    )

    # 1. Alias & Knowledge Base Pattern Match
    for alias, pattern in _SKILL_PATTERNS:
        if pattern.search(lower_text):
            canonical = ALIAS_INDEX[alias]
            # Prevent 'js' alias from falsely adding 'JavaScript' when 'js' only appears as part of a framework name (e.g. React JS, Node JS)
            if canonical == "JavaScript" and alias.lower() == "js":
                js_total = len(re.findall(r"\bjs\b", lower_text))
                js_in_frameworks = len(_FRAMEWORK_JS_PATTERN.findall(lower_text))
                if js_total <= js_in_frameworks:
                    continue
            found.add(canonical)

    # 2. Section Extraction (parsing lines under SKILLS / TECHNICAL SKILLS header)
    heading_match = _SKILLS_HEADING_RE.search(text)
    if heading_match:
        after_heading = text[heading_match.end():]
        for line in after_heading.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if _NEXT_SECTION_RE.match(stripped) and not _SKILLS_HEADING_RE.match(stripped):
                break
            # Split items by commas, semicolons, pipes, bullets
            items = re.split(r"[,;|•·\n]+", stripped)
            for item in items:
                if ":" in item:
                    item = item.split(":", 1)[1]
                item_clean = re.sub(r"^[^\w+#.]+|[^\w+#.]+$", "", item.strip())
                if 2 <= len(item_clean) <= 35 and not re.search(r"@|\d{5,}", item_clean):
                    if item_clean.lower() in ALIAS_INDEX:
                        found.add(ALIAS_INDEX[item_clean.lower()])
                    elif not any(kw in item_clean.lower() for kw in ["university", "college", "school", "experience", "education", "project", "completed", "bachelor", "master", "cgp", "programming", "languages", "web", "technologies", "tools", "devops"]):
                        found.add(item_clean.title())

    return sorted(found)


SECTION_HEADING_RE = re.compile(
    r"^\s*(skills|technical skills|education|experience|work experience|"
    r"projects|certifications|employment history|career objective|objective|"
    r"professional summary|personal details|languages|hobbies|interests|"
    r"achievements|awards|references|volunteer)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Matches an EDUCATION section heading line anywhere in the doc
_EDUCATION_HEADING_RE = re.compile(
    r"^\s*(education|academic|qualifications?)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Stop collecting lines when we hit any other major section
_NEXT_SECTION_RE = re.compile(
    r"^\s*(experience|work experience|employment|projects?|certifications?|"
    r"skills|key skills|technical skills|languages|hobbies|interests|achievements|"
    r"awards|references|volunteer|career objective|objective|personal details|education)\s*:?\s*$",
    re.IGNORECASE,
)

_ADDRESS_HEADING_RE = re.compile(
    r"^\s*(personal details|address|contact information|contact details|personal info)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_WORK_HEADING_RE = re.compile(
    r"^\s*(work experience|experience|employment history|work history|professional experience)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def extract_address(text: str) -> str | None:
    """Extract full address block from PERSONAL DETAILS or ADDRESS section."""
    heading_match = _ADDRESS_HEADING_RE.search(text)
    if heading_match:
        after_heading = text[heading_match.end():]
        addr_lines: list[str] = []
        for line in after_heading.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if _NEXT_SECTION_RE.match(stripped):
                break
            # Skip pure phone / email lines if address is multi-line
            addr_lines.append(stripped)
        if addr_lines:
            return "\n".join(addr_lines[:6])

    # Fallback: scan lines for door numbers, pin codes (6 digits), or commas with city names
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    hits = [line for line in lines if re.search(r"\b\d{6}\b", line) or re.search(r"\b\d+/[A-Za-z0-9-]+", line)]
    return "\n".join(hits[:3]) if hits else None


_WORK_HEADING_RE = re.compile(
    r"^\s*(work experience|experience|employment history|work history|professional experience|employment|career history|projects & experience|experience & projects|companies|company)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def extract_work_experience(text: str, organizations: list[str] | None = None) -> str | None:
    """Extract Work Experience / Company details block."""
    heading_match = _WORK_HEADING_RE.search(text)
    if heading_match:
        after_heading = text[heading_match.end():]
        work_lines: list[str] = []
        for line in after_heading.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if _NEXT_SECTION_RE.match(stripped):
                break
            work_lines.append(stripped)
        if work_lines:
            return "\n".join(work_lines[:20])

    # Fallback 1: Scan for lines with company/role keywords (e.g. "Software Engineer at Google", "Company: ACME")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    comp_keywords = [
        "at", "company", "developer", "engineer", "manager", "lead", "consultant",
        "inc", "ltd", "corp", "corporation", "pvt", "llc", "technologies", "solutions", "systems"
    ]
    matched_lines = []
    for line in lines:
        lower = line.lower()
        if any(kw in lower for kw in comp_keywords) and len(line.split()) <= 12:
            if not EMAIL_RE.search(line) and not _NEXT_SECTION_RE.match(line):
                matched_lines.append(line)
    if matched_lines:
        return "\n".join(matched_lines[:10])

    # Fallback 2: Return extracted organization names if available
    if organizations:
        return "Companies / Organizations:\n" + ", ".join(organizations[:8])

    return None



_CAREER_OBJ_RE = re.compile(
    r"^\s*(career objective|objective|professional summary|profile|about me|summary)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Short all-uppercase lines near the top are typically name / job-title headers
_HEADER_LINE_RE = re.compile(r"^[A-Z][A-Z\s\.\-]+$")


def extract_summary(text: str, max_sentences: int = 3) -> str | None:
    """Extract a meaningful summary paragraph.

    Strategy (in order):
    1. If a "CAREER OBJECTIVE" / "PROFESSIONAL SUMMARY" heading is found,
       use the text that follows it (the actual objective body) up to the
       next section heading.
    2. Otherwise fall back to the first sentences before the first section
       heading, skipping short name/title-style header lines.
    """
    # --- Strategy 1: extract text inside career-objective section ---
    obj_match = _CAREER_OBJ_RE.search(text)
    if obj_match:
        after_obj = text[obj_match.end():]
        # Find where the next section starts
        next_section = SECTION_HEADING_RE.search(after_obj)
        obj_body = after_obj[: next_section.start()] if next_section else after_obj[:800]
        sentences = sentence_split(obj_body.strip())
        if sentences:
            return " ".join(sentences[:max_sentences])

    # --- Strategy 2: text before first section heading, skipping headers ---
    match = SECTION_HEADING_RE.search(text)
    head_text = text[: match.start()] if match else text[:600]

    # Filter out short all-uppercase name/title lines from the beginning
    lines = head_text.splitlines()
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip very short lines that look like "NAME" or "JOB TITLE" headers
        if len(stripped.split()) <= 4 and _HEADER_LINE_RE.match(stripped):
            continue
        filtered_lines.append(stripped)

    filtered_text = " ".join(filtered_lines)
    sentences = sentence_split(filtered_text)
    if not sentences:
        return None
    return " ".join(sentences[:max_sentences])




_CERTIFICATION_RE = re.compile(
    r"\b(aws certified|pmp|certified scrum master|csm|cka|ckad|cissp|comptia|gcp certified|azure certified|itil|ocpjpad|cisa|ceh)\b",
    re.IGNORECASE,
)

_METRICS_IMPACT_RE = re.compile(
    r"\b(?:\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[kKmMbB]?|\b\d+\s*\+\s*(?:users|clients|projects|systems|services|requests|microservices|servers|engineers|team members)\b|\b(?:reduced|increased|improved|scaled|optimized|decreased|accelerated)\b[^\.\n]{5,60}\b\d+)",
    re.IGNORECASE,
)


def extract_certifications(text: str) -> list[str]:
    """Extract professional certifications from text."""
    matches = set(_CERTIFICATION_RE.findall(text))
    return sorted([m.title() for m in matches])


def extract_metrics_and_impact(text: str) -> list[str]:
    """Extract quantifiable impact points (percentages, scaling metrics, load reductions)."""
    hits = _METRICS_IMPACT_RE.findall(text)
    unique_hits = list(dict.fromkeys([h.strip() for h in hits if len(h.strip()) > 3]))
    return unique_hits[:8]


def check_ats_sections(text: str) -> dict[str, bool]:
    """Check presence of essential ATS section headings."""
    lower_text = text.lower()
    return {
        "has_skills": bool(re.search(r"\b(skills|technical skills|key skills|competencies)\b", lower_text)),
        "has_experience": bool(re.search(r"\b(experience|work experience|employment|history|projects)\b", lower_text)),
        "has_education": bool(re.search(r"\b(education|academic|qualification|university|degree)\b", lower_text)),
        "has_summary": bool(re.search(r"\b(summary|objective|profile|about me)\b", lower_text)),
        "has_certifications": bool(re.search(r"\b(certifications|licenses|courses|accreditation)\b", lower_text)),
    }


def parse_resume_fields(raw_text: str) -> dict:
    """
    Full pipeline: clean -> NER -> structured field extraction.
    Returns a dict matching the shape the API/schema expects.
    """
    text = clean_text(raw_text)
    entities = extract_entities(text)
    skills = extract_skills(text)
    address = extract_address(text)
    location = extract_location(text, entities, skills, address=address)
    orgs = entities.get("ORG", [])[:10]
    work_exp = extract_work_experience(text, organizations=orgs)
    certs = extract_certifications(text)
    metrics = extract_metrics_and_impact(text)
    sections = check_ats_sections(text)

    return {
        "name": extract_name(text, entities),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "experience_years": extract_experience_years(text),
        "education": extract_education(text),
        "summary": extract_summary(text),
        "address": address,
        "work_experience": work_exp,
        "organizations": orgs,
        "locations": entities.get("GPE", [])[:5],
        "location": location,
        "certifications": certs,
        "metrics_and_impact": metrics,
        "ats_sections": sections,
    }

