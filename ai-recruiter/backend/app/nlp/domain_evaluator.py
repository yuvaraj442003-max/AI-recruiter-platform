"""
domain_evaluator.py — Evaluates candidate resumes strictly against specified
technology domains / job roles. Provides explicit role identification, strict ATS scoring,
other job role match percentages, and structured improvement recommendations.
"""
from dataclasses import dataclass, field
import re

from app.nlp.domain_data import DOMAINS_KB
from app.ml.tfidf_matcher import tfidf_similarity
@dataclass
class DomainATSResult:
    target_domain: str
    domain_title: str
    domain_score: int
    skill_match_percentage: float
    matched_required_skills: list[str] = field(default_factory=list)
    missing_required_skills: list[str] = field(default_factory=list)
    matched_preferred_skills: list[str] = field(default_factory=list)
    missing_preferred_skills: list[str] = field(default_factory=list)
    keyword_match_percentage: float = 0.0
    recommendations: list[str] = field(default_factory=list)
    explicit_role: dict = field(default_factory=dict)
    other_role_matches: list[dict] = field(default_factory=list)
    top_3_roles: list[dict] = field(default_factory=list)
    categorized_recommendations: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "target_domain": self.target_domain,
            "domain_title": self.domain_title,
            "domain_score": self.domain_score,
            "skill_match_percentage": self.skill_match_percentage,
            "matched_required_skills": self.matched_required_skills,
            "missing_required_skills": self.missing_required_skills,
            "matched_preferred_skills": self.matched_preferred_skills,
            "missing_preferred_skills": self.missing_preferred_skills,
            "keyword_match_percentage": self.keyword_match_percentage,
            "recommendations": self.recommendations,
            "explicit_role": self.explicit_role,
            "other_role_matches": self.other_role_matches,
            "top_3_roles": self.top_3_roles,
            "categorized_recommendations": self.categorized_recommendations,
        }


def _calculate_keyword_density(resume_text: str, domain_keywords: list[str]) -> float:
    """Calculates percentage of domain keywords present in resume text."""
    if not resume_text or not domain_keywords:
        return 0.0

    lower_text = resume_text.lower()
    found_count = 0
    for kw in domain_keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, lower_text):
            found_count += 1

    return round((found_count / len(domain_keywords)) * 100.0, 2)


def extract_dynamic_headline_role(resume_text: str) -> str | None:
    """Scans header lines (first 500 chars) for lines that look like explicit job title headlines."""
    lines = [line.strip() for line in (resume_text or "").splitlines()[:12] if line.strip()]
    role_words = [
        "developer", "engineer", "manager", "analyst", "specialist", "accountant",
        "recruiter", "designer", "consultant", "administrator", "executive",
        "architect", "lead", "officer", "coordinator", "head", "director", "auditor",
        "representative", "associate"
    ]
    for line in lines:
        lower = line.lower()
        if any(w in lower for w in role_words) and len(line.split()) <= 6:
            if "@" not in line and not re.search(r"\d{7,}", line):
                return line.strip(" :-|•#*")
    return None


def detect_explicit_resume_role(resume_text: str, candidate_skills: list[str]) -> dict:
    """
    Identifies the job role explicitly mentioned in the candidate's resume across any profession
    (Software Developer, HR, Accountant, Marketing, Sales, Data Analyst, Project Manager, etc.)
    and calculates the ATS score specifically for that explicitly stated role.
    """
    lower_text = (resume_text or "").lower()

    role_patterns = [
        ("Software Developer", r"\b(software|systems?)\s+(developer|engineer|programmer|architect)\b"),
        ("Frontend Developer", r"\b(frontend|front-end|react|vue|angular|web)\s+(developer|engineer|programmer|specialist)\b"),
        ("Backend Developer", r"\b(backend|back-end|python|java|node\.?js|golang|go|c#|\.net|django|fastapi|spring)\s+(developer|engineer|programmer)\b"),
        ("Full Stack Developer", r"\b(full\s*stack|fullstack)\s+(developer|engineer|programmer)\b"),
        ("Data Analyst", r"\b(data|business\s+intelligence|bi)\s+(analyst|specialist)\b"),
        ("Data Scientist / AI Engineer", r"\b(data\s+scientist|ai\s+engineer|machine\s+learning\s+engineer|ml\s+engineer)\b"),
        ("DevOps / Cloud Engineer", r"\b(devops|cloud|infrastructure|site\s+reliability|sre)\s+(engineer|architect)\b"),
        ("QA / Automation Test Engineer", r"\b(qa|automation\s+test|test|quality\s+assurance)\s+(engineer|tester|specialist)\b"),
        ("UI/UX Designer", r"\b(ui\s*/?\s*ux|user\s+interface|ux|product)\s+(designer|architect)\b"),
        ("Human Resources (HR) / Recruiter", r"\b(hr|human\s+resources|recruiter|talent\s+acquisition|people\s+operations|hrbp)\b"),
        ("Accountant / Financial Analyst", r"\b(accountant|auditor|financial\s+analyst|finance\s+manager|bookkeeper|tax\s+specialist)\b"),
        ("Digital Marketing Specialist", r"\b(digital\s+marketing|marketing\s+specialist|marketing\s+manager|seo\s+specialist|content\s+strategist)\b"),
        ("Sales & Business Development", r"\b(sales|business\s+development|account\s+executive|bde|sdr|sales\s+manager)\b"),
        ("Project / Product Manager", r"\b(project\s+manager|product\s+manager|program\s+manager|scrum\s+master|product\s+owner)\b"),
        ("Business Operations Manager", r"\b(operations\s+manager|business\s+operations|process\s+manager)\b"),
        ("Customer Success / Support Specialist", r"\b(customer\s+success|customer\s+support|helpdesk\s+specialist|client\s+support)\b"),
        ("Cyber Security Specialist", r"\b(cyber\s*security|information\s+security|security\s+analyst|it\s+security)\b"),
    ]

    detected_key = None
    raw_match = None

    header_text = lower_text[:800]
    for domain_key, pattern in role_patterns:
        m = re.search(pattern, header_text)
        if m:
            detected_key = domain_key
            raw_match = m.group(0).title()
            break

    if not detected_key:
        for domain_key, pattern in role_patterns:
            m = re.search(pattern, lower_text)
            if m:
                detected_key = domain_key
                raw_match = m.group(0).title()
                break

    # Dynamic headline extraction fallback
    dynamic_headline = extract_dynamic_headline_role(resume_text)
    if dynamic_headline and not raw_match:
        raw_match = dynamic_headline

    is_explicit = bool(detected_key or dynamic_headline)

    if not detected_key:
        # Pick domain key with highest skill match
        best_score = -1
        for domain_key in DOMAINS_KB.keys():
            res = evaluate_domain_ats_score(candidate_skills, resume_text, domain_key, calculate_extras=False)
            if res.domain_score > best_score:
                best_score = res.domain_score
                detected_key = domain_key
        if not raw_match:
            raw_match = DOMAINS_KB[detected_key]["title"]

    eval_result = evaluate_domain_ats_score(candidate_skills, resume_text, detected_key, calculate_extras=False)

    return {
        "domain_key": detected_key,
        "role_title": raw_match or DOMAINS_KB[detected_key]["title"],
        "standard_role_title": DOMAINS_KB[detected_key]["title"],
        "raw_text_detected": raw_match or DOMAINS_KB[detected_key]["title"],
        "is_explicitly_mentioned": is_explicit,
        "ats_score": eval_result.domain_score,
        "description": DOMAINS_KB[detected_key].get("description", ""),
        "matched_skills": eval_result.matched_required_skills + eval_result.matched_preferred_skills,
    }


def evaluate_all_role_matches(candidate_skills: list[str], resume_text: str) -> list[dict]:
    """Calculates match scores and detailed metrics for all job roles in the knowledge base."""
    matches = []
    lower_text = (resume_text or "").lower()

    for domain_key, domain_meta in DOMAINS_KB.items():
        res = evaluate_domain_ats_score(candidate_skills, resume_text, domain_key, calculate_extras=False)
        missing_kws = [kw for kw in domain_meta.get("keywords", []) if kw not in lower_text][:6]

        matches.append({
            "key": domain_key,
            "title": domain_meta["title"],
            "description": domain_meta.get("description", ""),
            "match_score": res.domain_score,
            "matched_skills": res.matched_required_skills + res.matched_preferred_skills,
            "missing_skills": res.missing_required_skills + res.missing_preferred_skills,
            "missing_keywords": missing_kws,
            "certifications": domain_meta.get("certifications", []),
            "experience_guidance": domain_meta.get("experience_guidance", []),
            "matched_skills_count": len(res.matched_required_skills) + len(res.matched_preferred_skills),
            "missing_skills_count": len(res.missing_required_skills),
        })
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches


def get_top_3_role_matches(candidate_skills: list[str], resume_text: str, explicit_role: dict) -> list[dict]:
    """
    Dynamically selects the Top 3 best-matching job roles from the candidate's actual resume.
    Filters out 0% match roles and provides explanations for why the resume matches each role.
    """
    all_matches = evaluate_all_role_matches(candidate_skills, resume_text)

    # Filter out 0% match roles (roles with 0 score AND 0 matched skills)
    non_zero_matches = [m for m in all_matches if m["match_score"] > 0 or m["matched_skills_count"] > 0]
    if not non_zero_matches:
        non_zero_matches = all_matches[:3]

    explicit_key = explicit_role.get("domain_key")
    explicit_item = None

    for item in non_zero_matches:
        if item["key"] == explicit_key or item["title"] == explicit_role.get("role_title"):
            explicit_item = item
            break

    top_3: list[dict] = []
    if explicit_item:
        explicit_item_copy = dict(explicit_item)
        explicit_item_copy["is_primary"] = True
        explicit_item_copy["badge_label"] = "#1 Primary Role Match"
        matched_str = ", ".join(explicit_item_copy["matched_skills"][:4]) if explicit_item_copy["matched_skills"] else "core qualifications"
        explicit_item_copy["explanation"] = f"Primary role identified in resume. Strong alignment with your {matched_str}."
        top_3.append(explicit_item_copy)

    for item in non_zero_matches:
        if len(top_3) >= 3:
            break
        if explicit_item and item["key"] == explicit_item["key"]:
            continue
        item_copy = dict(item)
        item_copy["is_primary"] = False
        item_copy["badge_label"] = f"#{len(top_3)+1} Best Alternative"
        matched_str = ", ".join(item_copy["matched_skills"][:4]) if item_copy["matched_skills"] else "technical experience"
        item_copy["explanation"] = f"High compatibility based on your resume's {matched_str}."
        top_3.append(item_copy)

    # Fallback to fill up to 3 if less than 3 non-zero matches exist
    if len(top_3) < 3:
        for item in all_matches:
            if len(top_3) >= 3:
                break
            if not any(t["key"] == item["key"] for t in top_3):
                item_copy = dict(item)
                item_copy["is_primary"] = False
                item_copy["badge_label"] = f"#{len(top_3)+1} Suggested Role"
                item_copy["explanation"] = "Compatible role option based on your extracted background."
                top_3.append(item_copy)

    return top_3


def build_categorized_recommendations(
    target_domain: str,
    candidate_skills: list[str],
    resume_text: str,
    eval_result: DomainATSResult,
) -> dict:
    domain_meta = DOMAINS_KB.get(target_domain, DOMAINS_KB["Full Stack Developer"])
    title = domain_meta["title"]

    skills_kws = []
    if eval_result.missing_required_skills:
        missing_top = ", ".join(eval_result.missing_required_skills[:5])
        skills_kws.append(f"Add essential {title} core skills: {missing_top}.")
    if eval_result.missing_preferred_skills:
        pref_top = ", ".join(eval_result.missing_preferred_skills[:4])
        skills_kws.append(f"Boost ATS ranking by featuring key tools & frameworks: {pref_top}.")

    missing_kws = [kw for kw in domain_meta.get("keywords", []) if kw not in (resume_text or "").lower()][:5]
    if missing_kws:
        skills_kws.append(f"Include domain terminology in experience descriptions: {', '.join(missing_kws)}.")

    if eval_result.domain_score >= 80:
        skills_kws.append(f"Great fit! Your technical skill set strongly aligns with {title} requirements.")

    exp_improvements = list(domain_meta.get("experience_guidance", []))
    if not (resume_text and re.search(r"\d+(?:\.\d+)?%", resume_text)):
        exp_improvements.append("Add quantifiable impact metrics to bullet points (e.g. 'Improved efficiency by 25%', 'Reduced latency by 150ms').")

    certs = list(domain_meta.get("certifications", []))

    ats_formatting = []
    lower_text = (resume_text or "").lower()
    if "education" not in lower_text:
        ats_formatting.append("Add a clearly labeled 'Education' section heading for standard ATS parsers.")
    if "certifications" not in lower_text:
        ats_formatting.append("Include a 'Certifications & Credentials' section to improve ATS parser score.")
    if "summary" not in lower_text and "objective" not in lower_text:
        ats_formatting.append("Add a 2-3 sentence 'Professional Summary' at the top of your resume highlighting your target role.")
    if not candidate_skills or len(candidate_skills) < 5:
        ats_formatting.append("Use a dedicated 'Technical Skills' section with clean bulleted keywords.")
    if not ats_formatting:
        ats_formatting.append("Your resume layout follows standard ATS structural guidelines!")

    return {
        "skills_and_keywords": skills_kws,
        "experience_improvements": exp_improvements,
        "certifications": certs,
        "ats_formatting": ats_formatting,
    }


def evaluate_domain_ats_score(
    candidate_skills: list[str],
    resume_text: str,
    target_domain: str,
    calculate_extras: bool = True,
) -> DomainATSResult:
    """Evaluates candidate skills & resume text strictly against a target domain."""
    domain_meta = DOMAINS_KB.get(target_domain)
    if not domain_meta:
        domain_meta = DOMAINS_KB.get("Full Stack Developer")
        target_domain = "Full Stack Developer"

    title = domain_meta["title"]
    req_skills = set(domain_meta.get("required_skills", []))
    core_langs = set(domain_meta.get("core_languages", []))
    pref_skills = set(domain_meta.get("preferred_skills", []))
    keywords = domain_meta.get("keywords", [])

    cand_skill_map = {s.strip().lower(): s.strip() for s in (candidate_skills or []) if s and s.strip()}
    all_required_target = req_skills | core_langs

    # Case-insensitive matching for required skills
    matched_required_set = set()
    missing_required_set = set()
    for skill in all_required_target:
        if skill.strip().lower() in cand_skill_map:
            matched_required_set.add(skill)
        else:
            missing_required_set.add(skill)

    matched_required = sorted(list(matched_required_set))
    missing_required = sorted(list(missing_required_set))

    # Case-insensitive matching for preferred skills
    matched_preferred_set = set()
    missing_preferred_set = set()
    for skill in pref_skills:
        if skill.strip().lower() in cand_skill_map:
            matched_preferred_set.add(skill)
        else:
            missing_preferred_set.add(skill)

    matched_preferred = sorted(list(matched_preferred_set))
    missing_preferred = sorted(list(missing_preferred_set))

    # Calculate skill match percentage
    if all_required_target:
        core_matched_count = len(matched_required_set)
        target_norm = max(len(req_skills) + 1, 3)
        skill_match_pct = round(min(1.0, core_matched_count / target_norm) * 100.0, 2)
    else:
        skill_match_pct = 100.0

    pref_match_pct = (
        round((len(matched_preferred) / len(pref_skills)) * 100.0, 2) if pref_skills else 100.0
    )

    kw_pct = _calculate_keyword_density(resume_text, keywords)
    tf_pct = tfidf_similarity(resume_text, " ".join(list(all_required_target) + keywords))

    # Weight components: Required/Core Skills (45%), Preferred Skills (20%), Keyword Density (20%), TF-IDF (15%)
    raw_score = (
        skill_match_pct * 0.45
        + pref_match_pct * 0.20
        + kw_pct * 0.20
        + tf_pct * 0.15
    )

    # Apply strict domain mismatch penalties
    if len(matched_required) == 0:
        penalty_factor = 0.20
    elif skill_match_pct < 40.0:
        penalty_factor = 0.50 + (skill_match_pct / 40.0) * 0.40
    else:
        penalty_factor = 1.0

    final_score = int(round(max(0.0, min(100.0, raw_score * penalty_factor))))

    recommendations: list[str] = []
    explicit_role_info = {}
    other_roles = []
    top_3_roles = []
    cat_recs = {}

    if calculate_extras:
        explicit_role_info = detect_explicit_resume_role(resume_text, candidate_skills)
        other_roles = evaluate_all_role_matches(candidate_skills, resume_text)
        top_3_roles = get_top_3_role_matches(candidate_skills, resume_text, explicit_role_info)

        res_temp = DomainATSResult(
            target_domain=target_domain,
            domain_title=title,
            domain_score=final_score,
            skill_match_percentage=skill_match_pct,
            matched_required_skills=matched_required,
            missing_required_skills=missing_required,
            matched_preferred_skills=matched_preferred,
            missing_preferred_skills=missing_preferred,
            keyword_match_percentage=kw_pct,
        )
        cat_recs = build_categorized_recommendations(target_domain, candidate_skills, resume_text, res_temp)

        for section_recs in cat_recs.values():
            recommendations.extend(section_recs)

    return DomainATSResult(
        target_domain=target_domain,
        domain_title=title,
        domain_score=final_score,
        skill_match_percentage=skill_match_pct,
        matched_required_skills=matched_required,
        missing_required_skills=missing_required,
        matched_preferred_skills=matched_preferred,
        missing_preferred_skills=missing_preferred,
        keyword_match_percentage=kw_pct,
        recommendations=recommendations,
        explicit_role=explicit_role_info,
        other_role_matches=other_roles,
        top_3_roles=top_3_roles,
        categorized_recommendations=cat_recs,
    )


