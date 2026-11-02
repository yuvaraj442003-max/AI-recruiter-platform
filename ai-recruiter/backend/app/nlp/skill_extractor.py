"""
skill_extractor.py — turns raw resume text into structured fields:
name, email, phone, skills, experience_years, education, summary.

Skill matching is alias-based (see skills_data.py) rather than a
statistical classifier — this keeps it fast, deterministic, and easy
to extend, which matters more than recall here since a human recruiter
always reviews the result.
"""
import re
from typing import Optional

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


SECTION_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:"
    r"experience|work\s+experience|professional\s+experience|employment\s+history|work\s+history|internship\s+experience|internships?|employment|career\s+history|work\s+background|professional\s+background|industry\s+experience|industrial\s+experience|relevant\s+experience|"
    r"education|academic\s+background|academics|academic\s+details?|academic\s+degrees?|academic\s+qualifications?|educational\s+qualifications?|educational\s+details?|educational\s+background|academic\s+history|academic\s+profile|qualifications?|course\s+details?|"
    r"skills\s*(?:&|and)\s*competencies|skills\s*(?:&|and)\s*technologies|technical\s+skills|key\s+skills|skills\s*(?:&|and)\s*expertise|core\s+competencies|competencies|technical\s+environment|technologies|tech\s+stack|technical\s+stack|technical\s+expertise|technical\s+proficiencies|tools\s*(?:&|and)\s*technologies|tools|skills|areas\s+of\s+expertise|programming\s+languages|software\s+skills|core\s+skills|extracted\s+skills|"
    r"projects?|academic\s+projects|key\s+projects|personal\s+projects|featured\s+projects|technical\s+projects|project\s+work|major\s+projects|mini\s+projects|recent\s+projects|projects\s+undertaken|project\s+details|"
    r"certifications?|certificates?|credentials?|licenses?|courses?|certifications?\s*(?:&|and)\s*licenses?|licenses?\s*(?:&|and)\s*certifications?|training\s*(?:&|and)\s*certifications?|courses?\s*(?:&|and)\s*certifications?|professional\s+certifications?|"
    r"professional\s+summary|profile\s+summary|summary\s+of\s+qualifications|professional\s+profile|personal\s+profile|personal\s+summary|career\s+objective|summary|objective|about\s+me|about|profile|bio|biography|executive\s+summary|"
    r"declaration|personal\s+details|contact\s+information|contact\s+details|personal\s+info|languages|hobbies|interests|achievements|awards|publications|references|volunteer"
    r")\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_WORK_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:professional\s+experience|work\s+experience|employment\s+history|work\s+history|internship\s+experience|internships?|experience|employment|career\s+history|companies|company|work\s+background|professional\s+background|industry\s+experience|industrial\s+experience|relevant\s+experience)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_EDUCATION_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:education|academic\s+background|academics|academic\s+details?|academic\s+degrees?|academic\s+qualifications?|educational\s+qualifications?|educational\s+details?|educational\s+background|academic\s+history|academic\s+profile|qualifications?|course\s+details?)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_SKILLS_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:skills\s*(?:&|and)\s*competencies|skills\s*(?:&|and)\s*technologies|technical\s+skills|key\s+skills|skills\s*(?:&|and)\s*expertise|core\s+competencies|competencies|technical\s+environment|technologies|tech\s+stack|technical\s+stack|technical\s+expertise|technical\s+proficiencies|tools\s*(?:&|and)\s*technologies|tools|skills|areas\s+of\s+expertise|programming\s+languages|software\s+skills|core\s+skills|extracted\s+skills)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_PROJECTS_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:projects?|academic\s+projects|key\s+projects|personal\s+projects|featured\s+projects|technical\s+projects|project\s+work|major\s+projects|mini\s+projects|recent\s+projects|projects\s+undertaken|project\s+details|selected\s+projects|side\s+projects|open\s+source\s+projects|software\s+projects|client\s+projects|relevant\s+projects|notable\s+projects|portfolio\s+projects|capstone\s+projects|live\s+projects|freelance\s+projects)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_CERTIFICATION_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:certifications?|certificates?|credentials?|licenses?|courses?|certifications?\s*(?:&|and)\s*licenses?|licenses?\s*(?:&|and)\s*certifications?|training\s*(?:&|and)\s*certifications?|courses?\s*(?:&|and)\s*certifications?|professional\s+certifications?)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_CAREER_OBJ_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:career\s+objective|objective|professional\s+summary|profile\s+summary|summary\s+of\s+qualifications|professional\s+profile|personal\s+profile|personal\s+summary|summary|profile|about\s+me|about|bio|biography|executive\s+summary)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_ADDRESS_HEADING_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:personal\s+details|address|contact\s+information|contact\s+details|personal\s+info)\s*[*_]*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_NEXT_SECTION_RE = re.compile(
    r"^\s*(?:[#*\->\d\.]+\s*)?(?:"
    r"experience|work\s+experience|professional\s+experience|employment\s+history|work\s+history|internship\s+experience|internships?|employment|career\s+history|work\s+background|professional\s+background|industry\s+experience|industrial\s+experience|relevant\s+experience|"
    r"education|academic\s+background|academics|academic\s+details?|academic\s+degrees?|academic\s+qualifications?|educational\s+qualifications?|educational\s+details?|educational\s+background|academic\s+history|academic\s+profile|qualifications?|course\s+details?|"
    r"skills\s*(?:&|and)\s*competencies|skills\s*(?:&|and)\s*technologies|technical\s+skills|key\s+skills|skills\s*(?:&|and)\s*expertise|core\s+competencies|competencies|technical\s+environment|technologies|tech\s+stack|technical\s+stack|technical\s+expertise|technical\s+proficiencies|tools\s*(?:&|and)\s*technologies|tools|skills|areas\s+of\s+expertise|programming\s+languages|software\s+skills|core\s+skills|extracted\s+skills|"
    r"projects?|academic\s+projects|key\s+projects|personal\s+projects|featured\s+projects|technical\s+projects|project\s+work|major\s+projects|mini\s+projects|recent\s+projects|projects\s+undertaken|project\s+details|"
    r"certifications?|certificates?|credentials?|licenses?|courses?|certifications?\s*(?:&|and)\s*licenses?|licenses?\s*(?:&|and)\s*certifications?|training\s*(?:&|and)\s*certifications?|courses?\s*(?:&|and)\s*certifications?|professional\s+certifications?|"
    r"professional\s+summary|career\s+objective|summary|objective|about\s+me|profile|executive\s+summary|"
    r"declaration|personal\s+details|contact\s+information|contact\s+details|personal\s+info|languages|hobbies|interests|achievements|awards|publications|references|volunteer"
    r")\s*[*_]*:?\s*$",
    re.IGNORECASE,
)

def clean_bullets(text: str) -> str:
    """Strips bullet symbols, unicode private use bullets, and normalizes dash separators."""
    if not text:
        return ""
    text = re.sub(r"[\uf000-\uf8ff•*▪●·]\s*", "", text)
    text = text.replace("\ufffd", " - ")
    return text.strip()

def extract_section_text(text: str, heading_pattern: re.Pattern) -> str:
    """Extracts all text belonging to a section until the next section boundary."""
    match = heading_pattern.search(text)
    if not match:
        return ""
    after = text[match.end():]
    next_match = SECTION_HEADING_RE.search(after)
    return after[:next_match.start()].strip() if next_match else after.strip()


def extract_email(text: str) -> str | None:
    if not text:
        return None

    # 1. Check for explicit email labels (e.g., "Email: candidate@domain.com")
    labeled_match = re.search(
        r"(?:e-?mail|mail|contact)\s*[:\-]?\s*([A-Za-z0-9._%+-]+(?:\s*@\s*|\s*\[at\]\s*)[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
        text,
        re.IGNORECASE,
    )
    if labeled_match:
        cand_email = labeled_match.group(1).replace(" ", "").replace("[at]", "@")
        if EMAIL_RE.search(cand_email):
            return cand_email.strip()

    # 2. Check candidate header lines (top 35 lines where personal contact info standardly resides)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:35]:
        line_clean = re.sub(r"\s*@\s*", "@", line)
        m = EMAIL_RE.search(line_clean)
        if m:
            return m.group(0).strip()

    # 3. Check full text with standard EMAIL_RE
    match = EMAIL_RE.search(text)
    if match:
        return match.group(0).strip()

    # 4. Check for spacing artifacts from PDF extractors (e.g. "name @ example.com")
    spaced_match = re.search(r"\b([A-Za-z0-9._%+-]+)\s*@\s*([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b", text)
    if spaced_match:
        return f"{spaced_match.group(1)}@{spaced_match.group(2)}".strip()

    return None


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

    # 0. Check explicit labeled name: Name: ..., Full Name: ..., Candidate Name: ...
    label_re = re.compile(
        r"^\s*(?:full\s+name|candidate\s+name|applicant\s+name|name)\s*[:\-–—]\s*([a-zA-Z\s.'-]+)$",
        re.IGNORECASE,
    )
    for line in lines[:8]:
        m = label_re.match(line)
        if m:
            cand = m.group(1).strip()
            w_lower = [w.lower() for w in cand.split()]
            if 1 <= len(w_lower) <= 5 and not any(w in _INVALID_NAME_TERMS for w in w_lower):
                return cand

    gpe_terms = {g.lower() for g in entities.get("GPE", [])}
    for gpe in list(gpe_terms):
        for part in gpe.split():
            gpe_terms.add(part)

    # 1. Primary Strategy: Check the top 3 non-empty lines for the candidate full name.
    # Resumes standardly start with candidate's full name on line 1.
    for line in lines[:3]:
        clean_line = re.sub(r"^(?:full\s+name|candidate\s+name|applicant\s+name|name)\s*[:\-–—]\s*", "", line, flags=re.I)
        clean_line = re.sub(r"^[^\w]+", "", clean_line).strip()
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


_ROLE_KEYWORDS = {
    "developer", "engineer", "architect", "designer", "specialist", "analyst",
    "manager", "lead", "consultant", "scientist", "programmer", "administrator",
    "intern", "full stack", "fullstack", "frontend", "backend", "mern", "mean",
    "devops", "cloud", "data", "software", "web", "mobile", "android", "ios", "qa",
    "recruiter", "talent", "acquisition", "sourcer", "hr", "people", "coordinator",
    "strategist", "officer", "executive", "technical recruiter", "corporate recruiter"
}

def is_valid_role_headline(line: str) -> bool:
    """Validates if a line is a genuine job title and not a sentence or broken fragment."""
    if not line:
        return False
    clean = re.sub(r"^[^\w]+|[^\w)]+$", "", line).strip()
    words = clean.split()
    if len(words) < 1 or len(words) > 8:
        return False
    lower = clean.lower()
    # Reject unbalanced parenthesis or sentence fragments
    if lower.startswith(")") or lower.endswith("(") or (clean.count("(") != clean.count(")")):
        return False
    if any(frag in lower for frag in [
        "building and", "deploying", "developed", "completed", "using", "responsible for",
        "participated in", "assisted in", "gained", "exposure to", "trained with", "http", "github"
    ]):
        return False
    return any(kw in lower for kw in _ROLE_KEYWORDS)

def extract_headline_or_role(text: str) -> str | None:
    """Extract candidate professional headline or current role from resume header or first role."""
    lines = [clean_bullets(l).strip() for l in text.splitlines() if clean_bullets(l).strip()]
    
    # 1. Check top lines (lines 1 to 6) right after name for exact headline
    for line in lines[1:6]:
        if SECTION_HEADING_RE.match(line) or EMAIL_RE.search(line) or PHONE_RE.search(line):
            continue
        if re.search(r"http|www\.|github|linkedin|phone|email", line, re.I):
            continue
        line_clean = re.sub(r"^[^\w]+|[^\w)]+$", "", line).strip()
        if is_valid_role_headline(line_clean):
            return line_clean

    # 2. Check summary for aspiring/seeking role or explicit student persona
    summary_text = extract_summary(text) or ""
    if summary_text:
        m_seek = re.search(r"\b(?:seeking|aspiring|as an?|role of|position of)\s+([A-Za-z\s/-]+?(?:engineer|developer|designer|analyst|specialist|recruiter))\b", summary_text, re.I)
        if m_seek:
            cand_role = m_seek.group(1).strip()
            if is_valid_role_headline(cand_role):
                return cand_role.title()
        
        # Check student of AI/ML or CS
        m_stud = re.search(r"\b(b\.sc|b\.e|b\.tech|m\.s|m\.sc)\s+([A-Za-z\s/-]+?(?:intelligence|learning|computer|data|software))\b", summary_text, re.I)
        if m_stud:
            deg = m_stud.group(2).strip().title()
            if "Intelligence" in deg or "Learning" in deg:
                return "AI & Machine Learning Engineer"
            elif "Computer" in deg or "Software" in deg:
                return "Software Engineer"

    # 3. Fallback to role in work experience
    work_text = extract_section_text(text, _WORK_HEADING_RE)
    if work_text:
        for line in work_text.splitlines():
            line_clean = re.sub(r"^[^\w]+|[^\w)]+$", "", clean_bullets(line)).strip()
            if is_valid_role_headline(line_clean):
                if not re.search(r"\b(20\d\d|19\d\d|present|january|february|months|years)\b", line_clean.lower()):
                    t_cand, _ = _split_title_company(line_clean)
                    if is_valid_role_headline(t_cand):
                        return t_cand

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
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il+)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
    r"\s+\d{4}",
    re.IGNORECASE,
)

_YEAR_RANGE_RE = re.compile(
    r"\b(19\d\d|20\d\d)\s*[-–—to]+\s*(present|current|now|19\d\d|20\d\d)\b",
    re.IGNORECASE,
)

_FRESHER_STUDENT_RE = re.compile(
    r"\b(fresher|student|final[- ]year|entry[- ]level|graduating in 20\d\d)\b",
    re.IGNORECASE,
)


def _extract_work_section_text(text: str) -> str:
    """Isolates lines under work / internship experience headings, stopping at next section."""
    return extract_section_text(text, _WORK_HEADING_RE)


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


_SKILL_OR_ENV_BREAK_RE = re.compile(
    r"^\s*(technical environment|environment|technical skills|key skills|skills|"
    r"tech stack|technical stack|tools & technologies|tools and technologies|core competencies|"
    r"areas of expertise|competencies|technologies)\b",
    re.IGNORECASE,
)


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
            # Stop at the next recognizable section heading or skill/environment block
            if _NEXT_SECTION_RE.match(stripped) or _SKILL_OR_ENV_BREAK_RE.match(stripped):
                break
            
            # If line has inline technical environment / skills break, keep only pre-break text
            m_inline = re.search(r"\b(technical environment|technical skills|key skills|core competencies)\b", stripped, re.IGNORECASE)
            if m_inline:
                before_part = stripped[:m_inline.start()].strip()
                if before_part:
                    edu_lines.append(before_part)
                break

            edu_lines.append(stripped)
        if edu_lines:
            res = "\n".join(edu_lines[:12])
            res = re.split(r"\b(technical environment|technical skills|key skills)\b", res, flags=re.IGNORECASE)[0]
            clean_res = res.strip(" \t\n\r,;-")
            return clean_res or None

    # --- Fallback: keyword scan (only if no EDUCATION heading found) ---
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    hits = [
        line for line in lines
        if any(keyword in line.lower() for keyword in EDUCATION_KEYWORDS)
        and not _SKILL_OR_ENV_BREAK_RE.match(line)
    ]
    return "\n".join(hits[:6]) if hits else None


_SKILLS_HEADING_RE = re.compile(
    r"^\s*(skills|technical skills|key skills|core competencies|competencies|technologies|"
    r"technical environment|environment|tech stack|technical stack|technical expertise|"
    r"technical proficiencies|tools & technologies|tools and technologies|tools|"
    r"extracted skills|skills & expertise|skills & competencies|areas of expertise)\s*:?\s*$",
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

    # 2. Section Extraction (parsing lines under SKILLS / TECHNICAL SKILLS / TECHNICAL ENVIRONMENT header)
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


def extract_address(text: str) -> str | None:
    """Extract full address block from PERSONAL DETAILS or ADDRESS section."""
    addr_sec = extract_section_text(text, _ADDRESS_HEADING_RE)
    if addr_sec:
        addr_lines = [l.strip() for l in addr_sec.splitlines() if l.strip()]
        if addr_lines:
            return "\n".join(addr_lines[:6])

    # Fallback: scan lines for door numbers, pin codes (6 digits), or commas with city names
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    hits = [line for line in lines if re.search(r"\b\d{6}\b", line) or re.search(r"\b\d+/[A-Za-z0-9-]+", line)]
    return "\n".join(hits[:3]) if hits else None


def extract_work_experience(text: str, organizations: list[str] | None = None) -> str | None:
    """Extract Work Experience / Company details block."""
    work_sec = extract_section_text(text, _WORK_HEADING_RE)
    if work_sec:
        work_lines = [l.strip() for l in work_sec.splitlines() if l.strip()]
        if work_lines:
            return "\n".join(work_lines[:25])

    # Fallback 1: Scan for lines with company/role keywords
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    comp_keywords = [
        "at", "company", "developer", "engineer", "manager", "lead", "consultant",
        "inc", "ltd", "corp", "corporation", "pvt", "llc", "technologies", "solutions", "systems"
    ]
    matched_lines = []
    for line in lines:
        lower = line.lower()
        if any(kw in lower for kw in comp_keywords) and len(line.split()) <= 12:
            if not EMAIL_RE.search(line) and not SECTION_HEADING_RE.match(line):
                matched_lines.append(line)
    if matched_lines:
        return "\n".join(matched_lines[:10])

    if organizations:
        return "Companies / Organizations:\n" + ", ".join(organizations[:8])

    return None


# Short all-uppercase lines near the top are typically name / job-title headers
_HEADER_LINE_RE = re.compile(r"^[A-Z][A-Z\s\.\-]+$")


def extract_summary(text: str, max_sentences: int = 5) -> str | None:
    """Extract a meaningful summary paragraph verbatim from the resume.
    Preserves candidate's exact phrasing without leaking adjacent sections."""
    # 1. Look for explicit summary / objective heading
    obj_match = _CAREER_OBJ_RE.search(text)
    if obj_match:
        after_obj = text[obj_match.end():]
        next_sec = SECTION_HEADING_RE.search(after_obj)
        body = after_obj[:next_sec.start()].strip() if next_sec else after_obj[:800].strip()
        clean_b = clean_bullets(body)
        if clean_b:
            return clean_b

    # 2. Text before first section heading (skip headers)
    first_sec = SECTION_HEADING_RE.search(text)
    head_text = text[:first_sec.start()] if first_sec else text[:600]
    lines = [clean_bullets(l).strip() for l in head_text.splitlines() if clean_bullets(l).strip()]
    content_lines = []
    for line in lines[1:]:  # skip candidate name line
        if EMAIL_RE.search(line) or PHONE_RE.search(line) or _LINKEDIN_RE.search(line) or _GITHUB_RE.search(line):
            continue
        if re.search(r"^(?:address|contact|phone|email|location|github|linkedin|portfolio)\b", line, re.IGNORECASE):
            continue
        if len(line.split()) <= 4 and _HEADER_LINE_RE.match(line):
            continue
        if len(line.split()) < 4:
            continue
        content_lines.append(line)
    if content_lines:
        return " ".join(content_lines[:4])

    return None


_CERTIFICATION_RE = re.compile(
    r"\b(aws certified|pmp|certified scrum master|csm|cka|ckad|cissp|comptia|gcp certified|azure certified|itil|ocpjpad|cisa|ceh)\b",
    re.IGNORECASE,
)

_METRICS_IMPACT_RE = re.compile(
    r"\b(?:\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[kKmMbB]?|\b\d+\s*\+\s*(?:users|clients|projects|systems|services|requests|microservices|servers|engineers|team members)\b|\b(?:reduced|increased|improved|scaled|optimized|decreased|accelerated)\b[^\.\n]{5,60}\b\d+)",
    re.IGNORECASE,
)


def extract_certifications(text: str) -> list[str]:
    """Extract certifications list from CERTIFICATIONS section or keyword match."""
    certs_sec = extract_section_text(text, _CERTIFICATION_HEADING_RE)
    if certs_sec:
        if re.search(r"[-*•▪]", certs_sec):
            raw_chunks = [re.sub(r"\s+", " ", c).strip() for c in re.split(r"(?:^|\n)\s*[-*•▪\d.]+\s*", certs_sec) if c.strip()]
        else:
            raw_chunks = [clean_bullets(l).strip() for l in certs_sec.splitlines() if clean_bullets(l).strip()]

        clean_certs = []
        for c in raw_chunks:
            if not c or len(c) < 3 or re.search(r"\b(cgpa|gpa|percentage|passed with|completed with|\d+%\b)", c, re.I):
                continue
            if not any(h in c.lower() for h in ["education", "experience", "skills", "projects", "languages"]):
                clean_certs.append(c)

        if clean_certs:
            return clean_certs[:20]

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
        "has_certifications": bool(re.search(r"\b(certifications|certificates|licenses|courses|accreditation)\b", lower_text)),
    }


_LINKEDIN_RE = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_%-]+)/?",
    re.IGNORECASE,
)
_GITHUB_RE = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_%-]+)/?",
    re.IGNORECASE,
)
_PORTFOLIO_HOSTING_RE = re.compile(
    r"\b([a-zA-Z0-9_-]+\.(?:netlify\.app|vercel\.app|github\.io|herokuapp\.com|web\.app|firebaseapp\.com|pages\.dev|surge\.sh|render\.com)(?:/[^\s,;]*)?)\b",
    re.IGNORECASE,
)
_HTTP_PORTFOLIO_RE = re.compile(
    r"(https?://(?:www\.)?[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+(?:/[^\s,;]*)?)",
    re.IGNORECASE,
)
_LABELED_PORTFOLIO_RE = re.compile(
    r"(?:portfolio|website|personal\s+site|web)\s*[:\-–—]\s*(https?://[^\s,;]+|[a-zA-Z0-9_-]+\.[a-zA-Z0-9._/-]+)",
    re.IGNORECASE,
)

_IGNORED_PORTFOLIO_DOMAINS = [
    "linkedin.com", "github.com", "gitlab.com", "example.com", "w3.org", "schema.org", "adobe.com",
    "canva.com", "medium.com", "youtube.com", "twitter.com", "x.com", "facebook.com", "instagram.com",
    "gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "icloud.com", "live.com", "proton.me", "protonmail.com",
    "leetcode.com", "hackerrank.com", "geeksforgeeks.org", "codeforces.com"
]


def extract_linkedin(text: str) -> Optional[str]:
    """Extract LinkedIn profile URL, normalizing to full https URL."""
    match = _LINKEDIN_RE.search(text)
    if match:
        return f"https://linkedin.com/in/{match.group(1)}"
    m_label = re.search(r"linkedin\s*[:\-]?\s*(?:https?://(?:www\.)?linkedin\.com/in/)?([a-zA-Z0-9_%-]+)", text, re.I)
    if m_label and len(m_label.group(1).strip()) >= 3 and not re.search(r"http|www", m_label.group(1), re.I):
        return f"https://linkedin.com/in/{m_label.group(1).strip()}"
    return None


def extract_github(text: str) -> Optional[str]:
    """Extract GitHub profile URL, normalizing to full https URL."""
    match = _GITHUB_RE.search(text)
    if match:
        return f"https://github.com/{match.group(1)}"
    m_label = re.search(r"github\s*[:\-]?\s*(?:https?://(?:www\.)?github\.com/)?([a-zA-Z0-9_%-]+)", text, re.I)
    if m_label and len(m_label.group(1).strip()) >= 3 and not re.search(r"http|www", m_label.group(1), re.I):
        return f"https://github.com/{m_label.group(1).strip()}"
    return None


def extract_portfolio(text: str) -> Optional[str]:
    """Extract personal portfolio URL or site without false positives from emails or social domains."""
    # 1. Explicit labeled portfolio: Portfolio: https://... or Website: mysite.dev
    m_lab = _LABELED_PORTFOLIO_RE.search(text)
    if m_lab:
        cand = m_lab.group(1).strip()
        cand_lower = cand.lower()
        if not any(ign in cand_lower for ign in _IGNORED_PORTFOLIO_DOMAINS) and "@" not in cand:
            if not cand.startswith("http://") and not cand.startswith("https://"):
                cand = f"https://{cand}"
            return cand

    # 2. Known portfolio hosting platforms (.github.io, .vercel.app, .netlify.app, etc.)
    m_host = _PORTFOLIO_HOSTING_RE.search(text)
    if m_host:
        cand = m_host.group(1).strip()
        if not cand.startswith("http://") and not cand.startswith("https://"):
            cand = f"https://{cand}"
        return cand

    # 3. Explicit HTTP(S) links that are not emails, social platforms, or documentation sites
    for m in _HTTP_PORTFOLIO_RE.findall(text):
        cand_lower = m.lower()
        if not any(ign in cand_lower for ign in _IGNORED_PORTFOLIO_DOMAINS) and "@" not in m:
            if not re.search(r"\.(pdf|docx?|png|jpe?g|gif)$", cand_lower):
                return m.strip()

    return None


def _split_title_company(text: str) -> tuple[str, str]:
    """Separates role title and company name from a heading line."""
    text = clean_bullets(text).strip()
    if not text:
        return "", ""

    if " at " in text.lower():
        parts = re.split(r"\s+at\s+", text, maxsplit=1, flags=re.I)
        return parts[0].strip(), parts[1].strip()

    role_keywords = [
        "developer", "engineer", "designer", "architect", "manager", "lead",
        "intern", "consultant", "analyst", "specialist", "tester", "programmer",
        "administrator", "scientist", "executive", "officer", "associate",
        "recruiter", "talent", "acquisition", "sourcer", "hr", "people", "coordinator", "strategist"
    ]

    for delim in [" – ", " - ", " | ", " — ", ", "]:
        if delim in text:
            parts = [p.strip() for p in text.split(delim) if p.strip()]
            if len(parts) >= 2:
                p0_is_role = any(kw in parts[0].lower() for kw in role_keywords)
                p_last_is_role = any(kw in parts[-1].lower() for kw in role_keywords)
                if p_last_is_role and not p0_is_role:
                    return parts[-1], delim.join(parts[:-1])
                elif p0_is_role and not p_last_is_role:
                    return parts[0], delim.join(parts[1:])
                else:
                    return parts[0], parts[1]

    return text, ""


def parse_work_experience_items(work_text: str, default_location: str = "", skills: list[str] = None) -> list[dict]:
    """Parses Work Experience section text into clean, structured items."""
    if not work_text or not work_text.strip():
        return []

    lines = [clean_bullets(l).strip() for l in work_text.splitlines() if clean_bullets(l).strip()]
    if not lines:
        return []

    date_range_re = re.compile(
        r"(?:(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il+)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+)?(\d{4})"
        r"\s*(?:[-–—to]+\s*(?:(present|current|now)|(?:(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il+)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+)?(\d{4})))?",
        re.IGNORECASE
    )

    heading_role_keywords = [
        "developer", "engineer", "lead", "manager", "specialist", "intern", "consultant", "analyst",
        "recruiter", "talent", "acquisition", "sourcer", "hr", "people", "coordinator", "strategist",
        "architect", "designer", "programmer", "administrator", "scientist"
    ]

    items = []
    current_entry = None
    i = 0

    while i < len(lines):
        line = lines[i]
        date_match = date_range_re.search(line)

        is_heading_candidate = False
        if date_match:
            is_heading_candidate = True
        elif any(kw in line.lower() for kw in heading_role_keywords) and len(line.split()) <= 10:
            is_heading_candidate = True

        if is_heading_candidate and (len(line.split()) <= 14 or date_match):
            title = ""
            company = ""
            location = default_location or ""
            start_date = None
            end_date = None
            is_current = False

            # Case A: 3-line format (Line 1 = Role, Line 2 = Company, Line 3 = Date + Location)
            if not date_match and i + 2 < len(lines) and date_range_re.search(lines[i + 2]) and not date_range_re.search(lines[i + 1]) and len(lines[i + 1].split()) <= 6:
                title = line
                company = lines[i + 1]
                ndm_2 = date_range_re.search(lines[i + 2])
                date_str = ndm_2.group(0) if ndm_2 else ""
                parts = [p.strip() for p in re.split(r"\s*(?:[-–—\ufffd]+|\bto\b)\s*", date_str) if p.strip()]
                start_date = parts[0].strip() if parts else None
                is_current = "present" in date_str.lower() or "current" in date_str.lower()
                if is_current:
                    end_date = "Present"
                elif len(parts) > 1 and parts[1].strip():
                    end_date = parts[1].strip()

                loc_m = re.search(r"[📍]\s*([A-Za-z0-9\s,]+)", lines[i + 2])
                if loc_m:
                    location = loc_m.group(1).strip()
                elif "remote" in lines[i + 2].lower():
                    location = "Remote"
                i += 2

            # Case B: Current line itself has the date
            elif date_match:
                dm = date_range_re.search(line)
                date_str = dm.group(0) if dm else ""
                before_date = line[:line.find(date_str)].strip(" –-|—,") if date_str in line else ""
                
                if before_date:
                    t_cand, c_cand = _split_title_company(before_date)
                    title = t_cand
                    company = c_cand
                
                if date_str:
                    parts = [p.strip() for p in re.split(r"\s*(?:[-–—\ufffd]+|\bto\b)\s*", date_str) if p.strip()]
                    start_date = parts[0].strip() if parts else None
                    is_current = "present" in date_str.lower() or "current" in date_str.lower()
                    if is_current:
                        end_date = "Present"
                    elif len(parts) > 1 and parts[1].strip():
                        end_date = parts[1].strip()

                if items and not items[-1].get("highlights") and not items[-1].get("start_date"):
                    prev = items.pop()
                    if not title:
                        title = prev.get("title")
                    elif not company:
                        company = prev.get("title")

            # Case C: Current line has title and/or company (date is on the following line)
            else:
                title, company = _split_title_company(line)
                if i + 1 < len(lines):
                    next_l = lines[i + 1]
                    ndm = date_range_re.search(next_l)
                    if ndm:
                        next_date_str = ndm.group(0)
                        parts = [p.strip() for p in re.split(r"\s*(?:[-–—\ufffd]+|\bto\b)\s*", next_date_str) if p.strip()]
                        start_date = parts[0].strip() if parts else None
                        is_current = "present" in next_date_str.lower() or "current" in next_date_str.lower()
                        if is_current:
                            end_date = "Present"
                        elif len(parts) > 1 and parts[1].strip():
                            end_date = parts[1].strip()
                        i += 1

            if not title and company:
                title = company
                company = ""

            current_entry = {
                "title": title or "",
                "role": title or "",
                "company": company or "",
                "location": location or default_location or "",
                "start_date": start_date,
                "end_date": end_date,
                "is_current": is_current,
                "description": "",
                "highlights": [],
                "technologies": [s for s in (skills or []) if s.lower() in (title + " " + company).lower()][:5]
            }
            items.append(current_entry)
        else:
            if current_entry:
                current_entry["highlights"].append(line)
                if not current_entry["description"]:
                    current_entry["description"] = line
                if skills:
                    for s in skills:
                        if s.lower() in line.lower() and s not in current_entry["technologies"]:
                            current_entry["technologies"].append(s)
            else:
                current_entry = {
                    "title": "",
                    "role": "",
                    "company": "",
                    "location": default_location or "",
                    "start_date": None,
                    "end_date": None,
                    "is_current": False,
                    "description": line,
                    "highlights": [line],
                    "technologies": []
                }
                items.append(current_entry)
        i += 1

    return items


def parse_projects_items(proj_text: str, candidate_github: Optional[str] = None, skills: Optional[list[str]] = None, **kwargs) -> list[dict]:
    """Parses Projects section into structured project records."""
    if not proj_text or not proj_text.strip():
        return []

    lines = proj_text.splitlines()
    raw_chunks = []
    current_chunk = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_chunk:
                raw_chunks.append(current_chunk)
                current_chunk = []
            continue

        clean_l = clean_bullets(stripped)
        is_title = False
        if clean_l.endswith(":") and len(clean_l.split()) <= 10 and not clean_l.lower().startswith("technologies"):
            is_title = True
        elif (" – " in clean_l or " - " in clean_l or " — " in clean_l) and len(clean_l.split()) <= 12 and not any(kw in clean_l.lower() for kw in ["developed", "built", "designed", "created", "implemented", "using", "achieved", "completed"]):
            is_title = True
        elif not current_chunk and len(clean_l.split()) <= 10 and not any(kw in clean_l.lower() for kw in ["http", "technologies:", "developed", "user can", "•", "*"]):
            is_title = True
        elif clean_l.isupper() and 1 <= len(clean_l.split()) <= 8 and not any(kw in clean_l.lower() for kw in ["technologies", "tools", "overview", "key skills", "languages"]):
            is_title = True

        if is_title and current_chunk:
            raw_chunks.append(current_chunk)
            current_chunk = [clean_l]
        else:
            current_chunk.append(clean_l)

    if current_chunk:
        raw_chunks.append(current_chunk)

    projects = []
    # Broad URL regex supporting explicit http/https and modern deployment domains/github links
    url_re = re.compile(
        r"(?:https?://[^\s()<>]+|(?<![\w@])(?:www\.[^\s()<>]+|[a-zA-Z0-9-]+\.(?:vercel\.app|netlify\.app|github\.io|herokuapp\.com|pages\.dev|onrender\.com|fly\.dev)[^\s()<>]*|github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+))",
        re.I
    )

    def _clean_and_normalize_url(u_str: str) -> str:
        u_clean = u_str.strip().rstrip(").,;:]'\"?")
        if not u_clean:
            return ""
        if not u_clean.startswith("http://") and not u_clean.startswith("https://"):
            u_clean = f"https://{u_clean}"
        return u_clean

    for chunk in raw_chunks:
        if not chunk:
            continue
        first_line = chunk[0].rstrip(":").strip()

        # Check if first_line has an embedded URL in parentheses or after separator
        title_urls = url_re.findall(first_line)
        demo_url = None
        github_url = candidate_github

        if title_urls:
            for tu in title_urls:
                norm_tu = _clean_and_normalize_url(tu)
                if "github.com" in norm_tu.lower():
                    github_url = norm_tu
                elif not demo_url:
                    demo_url = norm_tu
            # Clean first line title by removing the URL and wrapping parentheses
            first_line = re.sub(r"\(?\s*" + "|".join(re.escape(u) for u in title_urls) + r"\s*\)?", "", first_line).strip(" -—|:,")

        if len(first_line.split()) > 12:
            first_line = " ".join(first_line.split()[:7])

        techs = []
        desc_lines = []

        for l in chunk[1:]:
            urls = url_re.findall(l)
            l_no_url = l
            for u in urls:
                norm_u = _clean_and_normalize_url(u)
                if not norm_u:
                    continue
                # Check for explicit labels
                if any(kw in l.lower() for kw in ("github", "repo", "code", "source", "repository")) or "github.com" in norm_u.lower():
                    github_url = norm_u
                elif any(kw in l.lower() for kw in ("demo", "live", "app", "link", "url", "deployed", "website", "site", "preview")):
                    demo_url = norm_u
                elif "github.com" in norm_u.lower():
                    github_url = norm_u
                elif not demo_url:
                    demo_url = norm_u

                l_no_url = l_no_url.replace(u, "").strip()

            if "technologies:" in l.lower() or "tech stack:" in l.lower() or "tools:" in l.lower():
                tech_part = re.split(r"technologies:|tech stack:|tools:", l, flags=re.I)[-1].strip()
                items = [t.strip().rstrip(".,") for t in re.split(r"[,;&|·]+", tech_part) if t.strip()]
                techs.extend([it for it in items if it.lower() not in ["integration", "and", "&"]])
            elif re.search(r"^[A-Za-z0-9+#.]+\s*(?:·|\|)\s*[A-Za-z0-9+#.]+", l):
                # e.g. "IoT Concepts · Automation ·" or "NLP · Node.js · React.js · MySQL"
                items = [t.strip().rstrip(".,") for t in re.split(r"[·|;,]+", l) if t.strip()]
                techs.extend([it for it in items if it.lower() not in ["integration", "and", "&"]])
            elif l_no_url and not any(kw in l_no_url.lower() for kw in ("demo:", "github:", "live demo:", "repo:", "code:")):
                desc_lines.append(l_no_url)

        full_desc = " ".join(desc_lines).strip()
        if full_desc.lower().startswith(first_line.lower()):
            full_desc = full_desc[len(first_line):].lstrip(" ,-:")

        # Infer technologies from description and title if not explicitly declared
        if not techs and skills:
            proj_search_text = f" {first_line} {full_desc} "
            for s in skills:
                if re.search(r"(?<![\w+#.])" + re.escape(s) + r"(?![\w+#])", proj_search_text, re.I):
                    if s not in techs:
                        techs.append(s)
            techs = techs[:6]

        projects.append({
            "title": first_line or "Featured Project",
            "name": first_line or "Featured Project",
            "description": full_desc or first_line,
            "contribution": f"Designed and developed using {', '.join(techs[:3])}" if techs else "",
            "technologies": techs,
            "key_features": desc_lines[:3],
            "live_demo_url": demo_url,
            "github_url": github_url,
        })

    return projects


def clean_institution_name(text: str) -> str:
    """Cleans school/college name by removing leading degree prefixes, trailing scores, years, and boards."""
    if not text:
        return ""
    # Strip leading generic headers
    text = re.sub(r"^(?:education|academics?|qualifications?|high\s+school|secondary\s+school)\s*[:\-–—|/]?\s*", "", text, flags=re.I)
    # 1. Remove leading degree / exam type prefix: e.g. "B.Tech (Information Technology), ", "HSC (12th), ", "SSLC (10th), "
    text = re.sub(
        r"^(?:[\s*•\-–—]*)(?:b\.?tech|b\.?e\.?|m\.?tech|bca|mca|b\.?sc|m\.?sc|bba|mba|ph\.?d|bachelor[^\,\(\)]*|master[^\,\(\)]*|hsc|sslc|12th(?:\s+grade|\s+std)?|10th(?:\s+grade|\s+std)?|class\s+xii|class\s+x|intermediate|secondary\s+school\s+leaving(?:\s+certificate)?|higher\s+secondary(?:\s+certificate)?)\s*(?:\([^\)]*\))?\s*[\,\:\-–—|/]\s*",
        "",
        text,
        flags=re.I,
    )
    # 2. Remove trailing score / CGPA / percentage: e.g. ", 89.2%", ", CGPA: 8.62"
    text = re.sub(
        r"[\s*•\-–—|,/]+\s*(?:cgpa|gpa|percentage|marks|grade|score)?\s*[:=]?\s*\d+(?:\.\d+)?\s*(?:/\s*\d+)?\s*%?.*$",
        "",
        text,
        flags=re.I,
    )
    # 3. Remove trailing years / graduated: e.g. ", 2024", ", Graduated: 2023"
    text = re.sub(r"[\s*•\-–—|,/]+\s*(?:graduated|passed|completed)?\s*[:=]?\s*(?:19\d{2}|20\d{2})\b.*$", "", text, flags=re.I)
    text = re.sub(r"[\s*•\-–—|,/]+\s*(?:graduated|passed|completed)\b.*$", "", text, flags=re.I)
    # 4. Remove trailing board
    text = re.sub(r"[\s*•\-–—|,/]+\s*(?:state\s+board|cbse|icse|matriculation|sslc|hsc|diploma)\b.*$", "", text, flags=re.I)
    return text.strip(" ,-|.:;•\t\r\n")


def parse_education_items(edu_text: str, **kwargs) -> list[dict]:
    """
    Parses Education section into structured academic items with verbatim precision.
    Extracts degree, institution, field of study, years, and grade/CGPA/details accurately.
    """
    if not edu_text or not edu_text.strip():
        return []

    year_re = re.compile(r"\b(19\d{2}|20\d{2})\b")
    degree_kw = re.compile(
        r"\b(bachelor(?:['’]s)?(?:\s+of\s+[A-Za-z\s]+)?|master(?:['’]s)?(?:\s+of\s+[A-Za-z\s]+)?|"
        r"b\.?tech|m\.?tech|b\.?sc|m\.?sc|bsc|msc|ph\.?d|mba|mca|bca|bba|diploma|"
        r"b\.?e\.?|associate|hsc|sslc|higher\s+secondary|secondary\s+school|12th|10th)\b",
        re.I
    )

    lines = [clean_bullets(l).strip() for l in edu_text.splitlines() if clean_bullets(l).strip()]
    if not lines:
        return []

    # Strip any top-level header line like "EDUCATION", "ACADEMIC DETAILS", etc.
    header_re = re.compile(
        r"^(?:education|academic|academics|academic\s+details?|academic\s+degrees?|course\s+details?|educational\s+qualifications?|education\s+details?|qualifications?)\s*:?$",
        re.I
    )
    while lines and header_re.match(lines[0]):
        lines.pop(0)

    # Strategy 1: Check for labeled format (Qualification: ... College: ... University: ...)
    qual_line = next((l for l in lines if l.lower().startswith("qualification:")), None)
    college_line = next((l for l in lines if l.lower().startswith("college:")), None)
    uni_line = next((l for l in lines if l.lower().startswith("university:")), None)

    if qual_line and (college_line or uni_line):
        deg_raw = qual_line.split(":", 1)[1].strip()
        inst_parts = []
        if college_line:
            inst_parts.append(college_line.split(":", 1)[1].strip())
        if uni_line:
            inst_parts.append(uni_line.split(":", 1)[1].strip())
        full_inst = ", ".join(inst_parts)
        years = year_re.findall(full_inst + " " + deg_raw)
        clean_inst = year_re.sub("", full_inst).replace("from", "").replace("to", "").strip(" ,-|.")
        clean_inst = header_re.sub("", clean_inst).strip(" ,-|.")
        field = deg_raw.split("(")[1].rstrip("). ") if "(" in deg_raw else None
        deg_clean = deg_raw.split("(")[0].strip() if "(" in deg_raw else deg_raw
        return [{
            "degree": deg_clean or "B.E",
            "institution": clean_inst,
            "field_of_study": field or "Engineering",
            "start_year": years[0] if len(years) >= 2 else None,
            "end_year": years[-1] if years else None,
            "details": f"{qual_line} | {clean_inst}",
            "score": None,
        }]

    # Strategy 2: Block / Paragraph splitting (by blank lines or institution/degree boundaries)
    raw_blocks = [b.strip() for b in re.split(r"\n\s*\n+", edu_text.strip()) if b.strip()]

    # If all lines were in a single block without blank lines, split by institution / degree headers
    if len(raw_blocks) <= 1 and len(lines) >= 3:
        inst_or_deg = re.compile(
            r"^(?:.*?\b(college|university|school|institute|vidhalaya|vidyalaya|academy)\b|.*?\b(bachelor|master|b\.?tech|m\.?tech|b\.?e\.?|diploma|hsc|sslc)\b)",
            re.I
        )
        curr_b = []
        custom_blocks = []
        for line in lines:
            if header_re.match(line):
                continue
            is_new = bool(inst_or_deg.search(line))
            has_details = any(re.search(r"\b(completed|cgpa|gpa|passed|scored|grade)\b|\d+%", l, re.I) for l in curr_b)
            if is_new and has_details and curr_b:
                custom_blocks.append("\n".join(curr_b))
                curr_b = [line]
            else:
                curr_b.append(line)
        if curr_b:
            custom_blocks.append("\n".join(curr_b))
        if len(custom_blocks) > 1:
            raw_blocks = custom_blocks

    items = []
    for block in raw_blocks:
        b_lines = [clean_bullets(l).strip() for l in block.splitlines() if clean_bullets(l).strip()]
        b_lines = [l for l in b_lines if not header_re.match(l)]
        if not b_lines:
            continue

        full_block = " ".join(b_lines)
        years = year_re.findall(full_block)

        # Check for score / CGPA / percentage
        score_match = re.search(r"\b(?:c?gpa|grade|score|percentage)\s*[:\-–—]?\s*(\d+(?:\.\d+)?(?:\s*/\s*\d+)?(?:\s*%)?)\b", full_block, re.I)
        if not score_match:
            score_match = re.search(r"(\d+(?:\.\d+)?\s*(?:/\s*\d+)?\s*(?:%|cgpa|gpa))\b", full_block, re.I)
        if not score_match:
            score_match = re.search(r"(\d+(?:\.\d+)?%)", full_block)
        score = score_match.group(0).strip(" ,-|.") if score_match else None

        desc_lines = []
        inst_lines = []
        deg_lines = []
        for l in b_lines:
            if header_re.match(l):
                continue
            if re.search(r"\b(completed|cgpa|gpa|percentage|passed|scored|grade|graduated|graduation\s+year)\b|\d+%", l, re.I):
                desc_lines.append(l)
            elif degree_kw.search(l) and not any(kw in l.lower() for kw in ["college", "university", "institute", "school"]):
                deg_lines.append(l)
            else:
                inst_lines.append(l)

        details = " ".join(desc_lines) if desc_lines else None
        inst_text = " ".join(inst_lines) if inst_lines else (deg_lines[0] if deg_lines else b_lines[0])

        # Extract degree and clean institution
        if deg_lines:
            deg = deg_lines[0].strip()
            inst = inst_text
        else:
            deg_suffix = re.search(r"[\s,\-–—]+(B\.?E\.?|B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|HSC|SSLC|Diploma|BBA|BCA|MCA|MBA|Ph\.?D)\b", inst_text, re.I)
            if deg_suffix:
                deg = deg_suffix.group(1).upper()
                inst = inst_text[:deg_suffix.start()].strip(" ,-|.")
            else:
                deg_m = degree_kw.search(full_block)
                deg = deg_m.group(0).upper() if deg_m else "Education"
                # If parts separated by dash / pipe
                parts = re.split(r"[-–—|]\s*", inst_text)
                if len(parts) >= 2 and any(kw in parts[1].lower() for kw in ["college", "university", "school", "institute"]):
                    inst = parts[1].strip(" ,-|.")
                else:
                    inst = inst_text

        # Clean institution name of redundant degree suffixes, GPA/score, and header prefixes
        inst = re.sub(r"^(?:education|academic|academics|qualifications?)\s*[:\-–—]?\s*", "", inst, flags=re.I).strip(" ,-|.")
        inst = clean_institution_name(inst)

        # Year determination
        start_year = years[0] if len(years) >= 2 else None
        end_year = years[-1] if years else None

        # Field of study
        field = None
        if " in " in full_block.lower():
            m_in = re.search(r"\b(?:in|of)\s+([A-Za-z\s&/]+?)(?:\s+with|\s+in\s+\d|\s+from|\s*\(|\.|$)", full_block, re.I)
            if m_in:
                cand_field = m_in.group(1).strip()
                if cand_field and len(cand_field.split()) <= 6 and not any(kw in cand_field.lower() for kw in ["college", "school", "university", "completed", "malco", "paavai"]):
                    field = cand_field
        elif "(" in inst_text and ")" in inst_text:
            m_par = re.search(r"\(([^)]+)\)", inst_text)
            if m_par:
                field = m_par.group(1).strip()

        # Check for orphan / dummy entry (e.g. institution is "-" or empty)
        is_orphan = (not inst or inst == "-" or inst.lower() in ("n/a", "none")) and (not deg or deg.lower() in ("academic degree", "education", "-"))
        if is_orphan:
            if end_year and items:
                target = next((it for it in items if not it.get("end_year") and any(k in (it.get("degree") or "").lower() for k in ("bachelor", "degree", "b.sc", "b.tech", "academic"))), items[-1])
                if not target.get("end_year"):
                    target["end_year"] = end_year
            if score and items and not items[-1].get("score"):
                items[-1]["score"] = score
                items[-1]["details"] = score
            continue

        # Clean generic placeholder degrees
        if not deg or deg.lower() in ("academic degree", "education", "degree") or deg == "-":
            if "arts and science" in inst.lower() or "college of science" in inst.lower():
                deg = f"Bachelor of Science ({field.split('/')[0].strip()})" if field else "Bachelor of Science (B.Sc)"
            elif field and any(kw in field.lower() for kw in ("computer", "engineering", "tech")):
                deg = "Bachelor of Science / Engineering"
            elif field:
                deg = f"Bachelor's Degree in {field}"
            else:
                deg = "Bachelor's Degree"

        if not field:
            if "HSC" in deg.upper() or "HIGHER SECONDARY" in deg.upper():
                field = "Higher Secondary (12th)"
                deg = "Higher Secondary Certificate (HSC)"
            elif "SSLC" in deg.upper() or "SECONDARY" in deg.upper():
                field = "Secondary Education (10th)"
                deg = "Secondary School Leaving Certificate (SSLC)"

        if "HSC" in deg.upper() or "HIGHER SECONDARY" in deg.upper():
            deg = "Higher Secondary Certificate (HSC)"
            if not inst or inst == "-" or "higher secondary certificate" in inst.lower():
                inst = "State Board / Higher Secondary School"
        elif "SSLC" in deg.upper() or "SECONDARY" in deg.upper():
            deg = "Secondary School Leaving Certificate (SSLC)"
            if not inst or inst == "-" or "secondary school leaving" in inst.lower():
                inst = "State Board / Secondary School"
        elif "higher secondary certificate" in inst.lower():
            inst = "State Board / Higher Secondary School"

        items.append({
            "degree": deg,
            "institution": inst,
            "field_of_study": field,
            "start_year": start_year,
            "end_year": end_year,
            "score": score,
            "details": details or score,
        })

    # Final filter: discard any orphaned items with no valid institution
    clean_items = []
    for it in items:
        if it.get("institution") and it["institution"] != "-" and it["institution"].lower() not in ("none", "n/a"):
            clean_items.append(it)
        elif it.get("end_year") and clean_items and not clean_items[-1].get("end_year"):
            clean_items[-1]["end_year"] = it["end_year"]
    return clean_items


def parse_certifications_items(cert_text: str = "", fallback_certs: Optional[str] = None, cert_list: Optional[list] = None, **kwargs) -> list[dict]:
    """Parses Certifications section into structured certification objects."""
    lines = []
    if cert_list and isinstance(cert_list, list):
        lines = [clean_bullets(str(c)).strip() for c in cert_list if clean_bullets(str(c)).strip()]
    elif fallback_certs and ("," in fallback_certs or ";" in fallback_certs):
        parts = [clean_bullets(p).strip() for p in re.split(r"[,;]+", fallback_certs) if clean_bullets(p).strip()]
        lines = parts
    
    if not lines:
        target_text = cert_text or fallback_certs or ""
        if not target_text or not target_text.strip():
            return []

        raw_lines = [clean_bullets(l).strip() for l in target_text.splitlines() if clean_bullets(l).strip()]
        for rl in raw_lines:
            if ("," in rl or ";" in rl) and len(rl.split()) > 6:
                parts = [p.strip() for p in re.split(r"[,;]+", rl) if p.strip()]
                lines.extend(parts)
            else:
                lines.append(rl)

    if not lines:
        return []

    year_re = re.compile(r"\b(19\d{2}|20\d{2})\b")
    header_re = re.compile(r"^(?:certifications?|certificates?|credentials?|licenses?|courses?)\s*:?$", re.I)
    lines = [l for l in lines if not header_re.match(l)]

    items = []
    for line in lines:
        y_match = year_re.search(line)
        clean_l = year_re.sub("", line).strip(" ,-|()[]")
        org = ""
        name = clean_l
        for delim in [" in ", " through ", " from ", " by ", " | ", " - ", " – ", " — ", ": "]:
            if delim in clean_l:
                p = clean_l.split(delim, 1)
                p0 = p[0].strip()
                p1 = p[1].strip()
                known_orgs = ["aws", "amazon", "google", "microsoft", "coursera", "udemy", "oracle", "cisco", "scrum alliance", "pmi", "edx", "ibm", "red hat", "great learning", "futureskills", "naan mudhalvan"]
                if delim in [" in ", " through ", " from ", " by "]:
                    name = p0
                    org = p1
                elif any(ko in p0.lower() for ko in known_orgs):
                    org = p0
                    name = p1
                elif any(ko in p1.lower() for ko in known_orgs):
                    name = p0
                    org = p1
                else:
                    name = p0
                    org = p1
                break

        # Clean "Completed " or "Certified " prefix from title if present
        clean_name = re.sub(r"^(?:completed|certified\s+in|certification\s+in)\s+", "", name, flags=re.I).strip()
        if clean_name:
            name = clean_name

        if name:
            items.append({
                "name": name,
                "organization": org.strip(" .,"),
                "year": y_match.group(0) if y_match else None,
            })

    return items[:10]


def parse_resume_fields(raw_text: str) -> dict:
    """
    Full pipeline: clean -> NER -> structured field extraction.
    Returns all candidate information verbatim from the resume.
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

    headline = extract_headline_or_role(text)
    summary = extract_summary(text)
    if not headline and summary:
        m_seek = re.search(r"\b(?:seeking|aspiring|as a|role of|position of)\s+([A-Za-z\s/-]+?(?:developer|engineer|designer|analyst|specialist))\b", summary, re.I)
        if m_seek:
            cand_role = m_seek.group(1).strip()
            if 1 <= len(cand_role.split()) <= 5:
                headline = cand_role.title()

    email = extract_email(text)
    phone = extract_phone(text)
    linkedin_url = extract_linkedin(text)
    github_url = extract_github(text)
    portfolio_url = extract_portfolio(text)

    # Section-based structured items
    proj_sec_text = extract_section_text(text, _PROJECTS_HEADING_RE)
    if not proj_sec_text:
        # Fallback: check if lines start with Project: or Project Name:
        p_lines = [l.strip() for l in text.splitlines() if re.match(r"^(?:project\s*\d*|project\s*name)\s*:", l, re.I)]
        if p_lines:
            proj_sec_text = "\n\n".join(p_lines)
    parsed_projects = parse_projects_items(proj_sec_text, candidate_github=github_url, skills=skills)

    work_sec_text = extract_section_text(text, _WORK_HEADING_RE) or (work_exp or "")
    parsed_work_items = parse_work_experience_items(work_sec_text, default_location=location or "", skills=skills)

    edu_sec_text = extract_section_text(text, _EDUCATION_HEADING_RE)
    if not edu_sec_text:
        edu_sec_text = extract_education(text) or ""
    parsed_edu_items = parse_education_items(edu_sec_text)
    if not parsed_edu_items and text:
        parsed_edu_items = parse_education_items(extract_education(text) or "")

    cert_sec_text = extract_section_text(text, _CERTIFICATION_HEADING_RE)
    if not cert_sec_text and certs:
        cert_sec_text = "\n".join(certs)
    parsed_cert_items = parse_certifications_items(cert_sec_text, fallback_certs=", ".join(certs) if certs else None, cert_list=certs)

    return {
        "name": extract_name(text, entities),
        "headline": headline,
        "current_role": headline,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience_years": extract_experience_years(text),
        "education": edu_sec_text or extract_education(text),
        "education_items": parsed_edu_items,
        "summary": summary,
        "address": address,
        "work_experience": work_exp,
        "work_experience_items": parsed_work_items,
        "projects": parsed_projects,
        "organizations": orgs,
        "locations": entities.get("GPE", [])[:5],
        "location": location,
        "certifications": certs,
        "certifications_items": parsed_cert_items,
        "certifications_text": cert_sec_text or (", ".join(certs) if certs else None),
        "metrics_and_impact": metrics,
        "ats_sections": sections,
        "linkedin_url": linkedin_url,
        "github_url": github_url,
        "portfolio_url": portfolio_url,
    }


