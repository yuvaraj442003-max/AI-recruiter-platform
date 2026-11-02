"""
resume_autofill_service.py — Service to parse uploaded resumes and extract
candidate Personal Details and Basic Professional/Academic Information
for auto-filling wizard forms.
"""
import re
import json
import logging
from typing import Optional, Dict, Any

from app.nlp.resume_parser import extract_resume_text
from app.nlp.skill_extractor import parse_resume_fields, clean_institution_name
from app.core.config import settings

logger = logging.getLogger("ai_recruiter.resume_autofill")


def extract_candidate_autofill_fields(file_bytes: bytes, filename: str, fallback_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Extracts structured fields from uploaded resume file (PDF, DOCX, TXT)
    to auto-populate candidate personal details and basic info.
    """
    filename_lower = filename.lower()
    if filename_lower.endswith(".txt"):
        raw_text = file_bytes.decode("utf-8", errors="ignore")
    else:
        raw_text = extract_resume_text(file_bytes, filename)

    if not raw_text or len(raw_text.strip()) < 10:
        return {}

    # 1. Base NLP Extraction
    nlp_fields = parse_resume_fields(raw_text)

    # 2. Extract / Refine Name
    name = nlp_fields.get("name") or ""
    if not name or len(name.split()) > 5:
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        for l in lines[:5]:
            if "@" in l or "http" in l or "resume" in l.lower() or "curriculum" in l.lower() or len(l.split()) > 4:
                continue
            cleaned = re.sub(r"[^A-Za-z\s.]", "", l).strip()
            if 2 <= len(cleaned) <= 40 and len(cleaned.split()) <= 4:
                name = cleaned
                break

    # 3. Email
    email = nlp_fields.get("email") or ""
    if not email or "@" not in email:
        m_email = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", raw_text)
        if m_email:
            email = m_email.group(1).strip()
        elif fallback_email:
            email = fallback_email

    # 4. Phone
    phone = nlp_fields.get("phone") or ""
    if not phone:
        m_phone = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}", raw_text)
        if m_phone:
            phone = m_phone.group(0).strip()

    # 5. Location
    location = nlp_fields.get("location") or ""
    if not location or location.lower() == "none":
        m_loc = re.search(r"(?:Location|Address|City)\s*[:\-–—]\s*([^\n\r|•,]+(?:,\s*[^\n\r|•,]+)?)", raw_text, re.I)
        if m_loc:
            location = m_loc.group(1).strip()
        else:
            cities = ["Chennai", "Bangalore", "Bengaluru", "Hyderabad", "Mumbai", "Pune", "Delhi", "Coimbatore", "Kolkata", "Noida", "Gurugram", "San Francisco", "New York", "Remote"]
            for c in cities:
                if re.search(rf"\b{c}\b", raw_text, re.I):
                    location = c
                    break

    # 6. URLs
    linkedin_url = nlp_fields.get("linkedin_url") or ""
    if not linkedin_url:
        m_li = re.search(r"(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)", raw_text, re.I)
        if m_li:
            linkedin_url = m_li.group(1).strip()

    github_url = nlp_fields.get("github_url") or ""
    if not github_url:
        m_gh = re.search(r"(https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+)", raw_text, re.I)
        if m_gh:
            github_url = m_gh.group(1).strip()

    portfolio_url = nlp_fields.get("portfolio_url") or ""
    if not portfolio_url:
        m_pf = re.search(r"(https?://(?:www\.)?[a-zA-Z0-9_.-]+\.(?:dev|me|io|com|app)(?:/[^\s]*)?)", raw_text, re.I)
        if m_pf:
            cand_url = m_pf.group(1).strip()
            if not any(ign in cand_url.lower() for ign in ["linkedin", "github", "gmail", "yahoo", "outlook", "hotmail"]):
                portfolio_url = cand_url

    # 7. Professional Headline & Current Role
    headline = nlp_fields.get("headline") or ""
    if not headline or len(headline.split()) > 7 or "http" in headline:
        m_head = re.search(r"\b([A-Za-z\s/-]+?(?:Developer|Engineer|Architect|Consultant|Designer|Analyst|Scientist))\b", raw_text)
        if m_head:
            cand_head = m_head.group(1).strip()
            if 1 <= len(cand_head.split()) <= 5:
                headline = cand_head
    if not headline:
        headline = "Software Engineer"
    current_role = nlp_fields.get("current_role") or headline

    # 8. Years of Work Experience
    exp_years = nlp_fields.get("experience_years")
    if exp_years is None:
        m_exp = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience", raw_text, re.I)
        if m_exp:
            try:
                exp_years = float(m_exp.group(1))
            except ValueError:
                exp_years = 0.0
        else:
            exp_years = 0.0

    # 9. Key Skills
    skills_list = nlp_fields.get("skills", [])
    if isinstance(skills_list, list) and skills_list:
        skills_str = ", ".join(sorted(list(set(skills_list))))
    else:
        known_skills = [
            "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "React", "React.js", "Node.js",
            "FastAPI", "Django", "Flask", "Spring Boot", "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "GitHub", "REST API", "GraphQL", "HTML",
            "CSS", "Tailwind CSS", "Bootstrap", "Linux", "Data Structures", "Algorithms", "Machine Learning"
        ]
        found = []
        for s in known_skills:
            if re.search(rf"\b{re.escape(s)}\b", raw_text, re.I):
                found.append(s)
        skills_str = ", ".join(sorted(list(set(found))))

    # 10. Summary
    summary = nlp_fields.get("summary") or ""
    if not summary:
        m_sum = re.search(r"(?:PROFESSIONAL\s+SUMMARY|SUMMARY|ABOUT|OBJECTIVE)\s*[:\-–—]?\s*(?:\r?\n)+([^\n]+(?:\n[^\n]+){0,4})", raw_text, re.I)
        if m_sum:
            summary = " ".join([l.strip() for l in m_sum.group(1).splitlines() if l.strip()])

    # 11. Certifications
    certs = nlp_fields.get("certifications", [])
    raw_cert_lines = []
    if isinstance(certs, list) and certs:
        raw_cert_lines = certs
    else:
        m_cert_sec = re.search(r"(?:CERTIFICATIONS?|LICENSES?)\s*[:\-–—]?\s*(?:\r?\n)+([^\n\r]+(?:\r?\n[^\n\r]+){0,8})", raw_text, re.I)
        if m_cert_sec:
            for cl in m_cert_sec.group(1).splitlines():
                cl_clean = re.sub(r"^[-*•\d.]+\s*", "", cl).strip()
                if cl_clean and len(cl_clean) > 2 and not any(h in cl_clean.lower() for h in ["education", "experience", "skills", "projects", "languages"]):
                    raw_cert_lines.append(cl_clean)

    # Merge broken multi-line certification titles and filter out academic/score noise
    merged_certs = []
    for c_line in raw_cert_lines:
        clean_c = c_line.strip(" •*▪-–—\t\r\n")
        if not clean_c or re.search(r"\b(cgpa|gpa|percentage|passed with|completed with|\d+%\b)", clean_c, re.I):
            continue
        # Join lines that continue previous certificate title
        if merged_certs and (clean_c[0].islower() or re.match(r"^(?:and|with|through|at|by|from|via)\b", clean_c, re.I)):
            merged_certs[-1] = f"{merged_certs[-1]} {clean_c}".strip()
        else:
            merged_certs.append(clean_c)

    certs_str = ", ".join(merged_certs)

    # 12. College & Academic Credentials with Dedicated 10th & 12th Separation
    edu_items = nlp_fields.get("education_items", [])
    if not isinstance(edu_items, list):
        edu_items = []

    # Target structured containers
    college = ""
    degree = ""
    branch = ""
    grad_year = ""
    cgpa = ""

    twelfth_school = ""
    twelfth_board = ""
    twelfth_year = ""
    twelfth_percentage = ""

    tenth_school = ""
    tenth_board = ""
    tenth_year = ""
    tenth_percentage = ""

    # Helper regexes
    year_re = re.compile(r"\b(19\d{2}|20\d{2})\b")
    pct_re = re.compile(r"(\d+(?:\.\d+)?)\s*%")
    cgpa_num_re = re.compile(r"\b(?:cgpa|gpa|grade|score)?\s*[:\-–—]?\s*([2-9]\.\d{1,2}|10\.0)\b", re.I)
    explicit_gpa_re = re.compile(r"\b(?:cgpa|gpa)\s*[:\-–—]?\s*([0-9]\.\d{1,2})\b", re.I)

    for item in edu_items:
        deg_str = str(item.get("degree") or "").strip()
        inst_str = str(item.get("institution") or "").strip()
        field_str = str(item.get("field_of_study") or "").strip()
        item_score = str(item.get("score") or "").strip()
        item_end_year = str(item.get("end_year") or "").strip()
        full_item_text = f"{deg_str} {inst_str} {field_str} {item_score} {item.get('details') or ''}"
        full_lower = full_item_text.lower()

        # Classify degree / level (check 12th / Senior Secondary first to avoid collision with 10th / Secondary)
        is_12th = bool(re.search(r"\b(hsc|12th(?:\s+grade|\s+std)?|class\s+xii\b|higher\s+secondary(?:\s+certificate)?|senior\s+secondary|intermediate|diploma|plus\s+two)\b", full_lower))
        is_10th = not is_12th and bool(re.search(r"\b(sslc|10th(?:\s+grade|\s+std)?|class\s+x\b|secondary\s+school\s+leaving|matriculation)\b", full_lower))

        if not is_10th and not is_12th:
            if re.search(r"\b(senior\s+secondary|higher\s+secondary|hsc|12th\b)\b", full_lower):
                is_12th = True
            elif re.search(r"\b(secondary\s+education|sslc|10th\b)\b", full_lower) and "senior" not in full_lower:
                is_10th = True
            elif re.search(r"\b(high\s+school)\b", full_lower):
                is_12th = True

        if is_10th and not is_12th:
            # 10th Grade / SSLC Record
            clean_school = clean_institution_name(inst_str)
            tenth_school = clean_school or tenth_school
            if "matric" in full_lower:
                tenth_board = "Matriculation / SSLC"
            elif "cbse" in full_lower:
                tenth_board = "CBSE"
            elif "icse" in full_lower:
                tenth_board = "ICSE"
            else:
                tenth_board = tenth_board or "State Board / SSLC"

            if item_end_year:
                tenth_year = item_end_year
            elif not tenth_year:
                y_m = year_re.findall(full_item_text)
                if y_m:
                    tenth_year = y_m[-1]

            if item_score:
                p_m = pct_re.search(item_score) or re.search(r"(\d+(?:\.\d+)?)", item_score)
                if p_m:
                    tenth_percentage = p_m.group(1)
            elif not tenth_percentage:
                p_m = pct_re.search(full_item_text) or re.search(r"\b([4-9]\d(?:\.\d+)?)\b", full_item_text)
                if p_m:
                    tenth_percentage = p_m.group(1)

        elif is_12th:
            # 12th Grade / HSC / Intermediate Record
            clean_school = clean_institution_name(inst_str)
            twelfth_school = clean_school or twelfth_school
            if "diploma" in full_lower:
                twelfth_board = "Diploma"
            elif "matric" in full_lower:
                twelfth_board = "Matriculation / HSC"
            elif "cbse" in full_lower:
                twelfth_board = "CBSE"
            elif "icse" in full_lower:
                twelfth_board = "ICSE"
            else:
                twelfth_board = twelfth_board or "State Board / HSC"

            if item_end_year:
                twelfth_year = item_end_year
            elif not twelfth_year:
                y_m = year_re.findall(full_item_text)
                if y_m:
                    twelfth_year = y_m[-1]

            if item_score:
                p_m = pct_re.search(item_score) or re.search(r"(\d+(?:\.\d+)?)", item_score)
                if p_m:
                    twelfth_percentage = p_m.group(1)
            elif not twelfth_percentage:
                p_m = pct_re.search(full_item_text) or re.search(r"\b([4-9]\d(?:\.\d+)?)\b", full_item_text)
                if p_m:
                    twelfth_percentage = p_m.group(1)

        else:
            # College / University Record
            clean_inst = clean_institution_name(inst_str)
            if clean_inst:
                college = clean_inst

            # Separate degree & branch if combined
            cand_deg = deg_str
            cand_branch = field_str
            if " in " in cand_deg:
                parts = cand_deg.split(" in ", 1)
                cand_deg = parts[0].strip()
                if not cand_branch:
                    cand_branch = parts[1].strip()
            if "(" in cand_deg and ")" in cand_deg:
                m_br = re.search(r"^(.*?)\s*\(([^)]+)\)", cand_deg)
                if m_br:
                    cand_deg = m_br.group(1).strip()
                    if not cand_branch:
                        cand_branch = m_br.group(2).strip()

            if not degree or degree.lower() in ("degree", "academic degree", "-"):
                degree = cand_deg
            if not branch:
                branch = cand_branch

            if not cgpa:
                cg_m = explicit_gpa_re.search(item_score) or explicit_gpa_re.search(full_item_text) or cgpa_num_re.search(item_score) or pct_re.search(item_score)
                if cg_m:
                    cgpa = cg_m.group(1)
            if item_end_year:
                grad_year = item_end_year
            elif not grad_year:
                y_m = year_re.findall(full_item_text)
                if y_m:
                    grad_year = y_m[-1]

    # Education section slice fallback if college fields remain incomplete
    m_edu_sec = re.search(r"(?:EDUCATION|ACADEMIC|ACADEMICS)\s*[:\-–—]?\s*(?:\r?\n)+([^\n]+(?:\n[^\n]+){0,8})", raw_text, re.I)
    edu_text = m_edu_sec.group(1) if m_edu_sec else raw_text

    if not college or college == "-" or len(college) > 120:
        for line in edu_text.splitlines():
            l_str = line.strip()
            if any(kw in l_str.lower() for kw in ["university", "college", "institute", "campus", "iit", "nit", "bits", "vit", "srm"]):
                college = clean_institution_name(l_str)
                college = re.sub(r"\s*[|•].*$", "", college).strip()
                break

    if not degree or degree.lower() in ("degree", "academic degree", "-"):
        m_deg = re.search(r"\b(B\.?E\.?|B\.?Tech|BCA|MCA|M\.?Tech|B\.?Sc|M\.?Sc|Bachelor(?:['’]s)?(?:\s+of\s+[A-Za-z\s]+)?|Master(?:['’]s)?(?:\s+of\s+[A-Za-z\s]+)?)\b", edu_text, re.I)
        if m_deg:
            deg_found = m_deg.group(1).strip()
            if " in " in deg_found:
                d_parts = deg_found.split(" in ", 1)
                degree = d_parts[0].strip()
                if not branch:
                    branch = d_parts[1].strip()
            elif deg_found.lower().startswith("bachelor"):
                degree = "Bachelor of Engineering (B.E.)"
            else:
                degree = deg_found

    if not branch:
        m_br = re.search(r"\b(Computer Science(?: & Engineering| and Engineering)?|Information Technology|Electronics & Communication|Electrical & Electronics|Mechanical Engineering|Data Science|Artificial Intelligence)\b", edu_text, re.I)
        if m_br:
            branch = m_br.group(1).strip()

    if not cgpa:
        m_cg = explicit_gpa_re.search(edu_text) or cgpa_num_re.search(edu_text) or pct_re.search(edu_text)
        if m_cg:
            cgpa = m_cg.group(1)

    # CRITICAL: Prevent using 10th or 12th year as College Graduation Year
    forbidden_years = {str(tenth_year), str(twelfth_year)} - {""}
    if grad_year in forbidden_years:
        grad_year = ""

    if not grad_year:
        # Check if there is another year in the college text that doesn't belong to 10th/12th
        all_years = [y for y in year_re.findall(edu_text) if y not in forbidden_years]
        if all_years:
            grad_year = all_years[-1]
        elif twelfth_year and twelfth_year.isdigit():
            # Infer college graduation year: 12th year + standard degree duration
            base_12 = int(twelfth_year)
            deg_upper = degree.upper()
            if any(k in deg_upper for k in ["B.E", "B.TECH", "ENGINEERING", "B.ARCH"]):
                grad_year = str(base_12 + 4)
            elif any(k in deg_upper for k in ["M.TECH", "MCA", "MBA"]):
                grad_year = str(base_12 + 6)
            else:
                grad_year = str(base_12 + 3)
        elif tenth_year and tenth_year.isdigit():
            base_10 = int(tenth_year)
            grad_year = str(base_10 + 6)
        else:
            # Check work experience start year
            m_work_yr = re.search(r"\b(?:202[0-9]|201[8-9])\b\s*(?:–|-|to)\s*(?:Present|current)", raw_text, re.I)
            if m_work_yr:
                grad_year = m_work_yr.group(0)[:4]

    result = {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin_url": linkedin_url,
        "github_url": github_url,
        "portfolio_url": portfolio_url,
        "headline": headline,
        "current_role": current_role,
        "experience_years": float(exp_years or 0.0),
        "skills": skills_str,
        "summary": summary,
        "certifications": certs_str,
        # College / Higher Education
        "college": college,
        "degree": degree,
        "branch": branch,
        "graduation_year": grad_year,
        "cgpa": cgpa,
        # 12th Grade / HSC / Intermediate
        "twelfth_school": twelfth_school,
        "twelfth_board": twelfth_board,
        "twelfth_year": twelfth_year,
        "twelfth_percentage": twelfth_percentage,
        # 10th Grade / SSLC
        "tenth_school": tenth_school,
        "tenth_board": tenth_board,
        "tenth_year": tenth_year,
        "tenth_percentage": tenth_percentage,
        "raw_text_preview": raw_text[:500],
    }

    return result

