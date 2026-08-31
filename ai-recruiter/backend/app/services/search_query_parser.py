"""
search_query_parser.py — Natural Language Search Query Parser for Smart Candidate Search.

Extracts structured filters (skills, experience range, location, ATS threshold, job role)
from recruiter natural language search strings.
"""
import re
from typing import Any, Dict, List, Optional

from app.nlp.skills_data import ALIAS_INDEX, SKILLS_KB
from app.services.ats_scoring_service import normalize_skill

KNOWN_LOCATIONS = [
    "chennai", "bangalore", "bengaluru", "mumbai", "delhi", "noida",
    "gurgaon", "hyderabad", "pune", "kolkata", "ahmedabad", "remote",
    "hybrid", "on-site", "india", "san francisco", "new york", "london"
]

KNOWN_ROLES = [
    "backend developer", "frontend developer", "fullstack developer",
    "python developer", "java developer", "data analyst", "data scientist",
    "devops engineer", "hr manager", "recruiter", "sales manager",
    "accountant", "marketing specialist", "product manager"
]


def parse_search_query(query_text: str) -> Dict[str, Any]:
    """
    Parses natural language query strings like:
    "Python + FastAPI + PostgreSQL 3+ years experience Chennai ATS > 75"
    Returns structured filters dictionary.
    """
    if not query_text or not query_text.strip():
        return {
            "skills": [],
            "minimum_experience": None,
            "maximum_experience": None,
            "location": None,
            "minimum_ats_score": None,
            "job_role": None,
        }

    q = query_text.strip()
    q_lower = q.lower()

    # 1. Experience Extraction
    min_exp = None
    max_exp = None

    range_match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*(?:years?|yrs?|yr)', q_lower)
    if range_match:
        min_exp = float(range_match.group(1))
        max_exp = float(range_match.group(2))
    else:
        plus_match = re.search(r'(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?|yr)', q_lower)
        if plus_match:
            min_exp = float(plus_match.group(1))
        else:
            min_text_match = re.search(r'(?:minimum|min|at least|over|>|>=)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?|yr)?', q_lower)
            if min_text_match:
                min_exp = float(min_text_match.group(1))
            else:
                generic_exp_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?|yr)\s*(?:of)?\s*(?:experience|exp)?', q_lower)
                if generic_exp_match:
                    min_exp = float(generic_generic_exp_match.group(1)) if 'generic_generic_exp_match' in locals() else float(generic_exp_match.group(1))

    # 2. ATS Score Extraction
    min_ats = None
    ats_match = re.search(r'(?:ats|ats score|ats match)?\s*(?:>|>=|above|over|greater than|at least)\s*(\d{1,3})%?', q_lower)
    if ats_match:
        min_ats = float(ats_match.group(1))
    else:
        ats_eq_match = re.search(r'ats\s*:\s*(\d{1,3})%?', q_lower)
        if ats_eq_match:
            min_ats = float(ats_eq_match.group(1))

    # 3. Location Extraction
    extracted_loc = None
    for loc in KNOWN_LOCATIONS:
        if re.search(r'\b' + re.escape(loc) + r'\b', q_lower):
            extracted_loc = loc.title()
            if extracted_loc.lower() == "bengaluru":
                extracted_loc = "Bangalore"
            break

    # 4. Job Role Extraction
    extracted_role = None
    for role in KNOWN_ROLES:
        if role in q_lower:
            extracted_role = role.title()
            break

    # 5. Skills Extraction
    extracted_skills = []
    seen_skills = set()

    # Split query by comma, plus, or 'and'
    tokens = re.split(r'[,+\n|]|(?:\s+and\s+)', q)
    for tok in tokens:
        cleaned = tok.strip()
        if not cleaned or len(cleaned) < 2:
            continue
        
        # Check against ALIAS_INDEX & SKILLS_KB
        norm = normalize_skill(cleaned)
        if norm and norm.lower() in ALIAS_INDEX or norm in SKILLS_KB:
            if norm.lower() not in seen_skills:
                seen_skills.add(norm.lower())
                extracted_skills.append(norm)

    # Word by word check for tech/non-tech skill names in query
    words = re.findall(r'[a-zA-Z0-9.#+]+', q)
    for word in words:
        if len(word) < 2:
            continue
        norm = normalize_skill(word)
        if norm and (norm.lower() in ALIAS_INDEX or norm in SKILLS_KB):
            if norm.lower() not in seen_skills:
                seen_skills.add(norm.lower())
                extracted_skills.append(norm)

    return {
        "skills": extracted_skills,
        "minimum_experience": min_exp,
        "maximum_experience": max_exp,
        "location": extracted_loc,
        "minimum_ats_score": min_ats,
        "job_role": extracted_role,
    }
