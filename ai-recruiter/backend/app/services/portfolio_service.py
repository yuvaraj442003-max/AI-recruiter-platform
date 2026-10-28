"""
portfolio_service.py — Business logic and database operations for candidate portfolios.
Handles resume-to-portfolio pipeline, AI integration, theme configuration, slug generation,
and safe public/recruiter data exposure.
"""
import json
import logging
import os
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload, object_session

from app.ai.portfolio_ai_service import (
    extract_structured_portfolio_data,
    generate_headline_options,
    improve_about_text,
    improve_experience_item,
    improve_project_item,
    organize_skills_into_categories,
)
from app.core.exceptions import AppError, BadRequestError, NotFoundError
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.portfolio import Portfolio
from app.models.user import User
from app.nlp.resume_parser import extract_resume_text
from app.nlp.skill_extractor import parse_resume_fields, extract_email

logger = logging.getLogger("ai_recruiter.portfolio_service")

RESERVED_SLUGS = {
    "api", "admin", "me", "public", "generate", "publish", "unpublish", "theme", "customize",
    "dashboard", "login", "register", "null", "undefined", "jobs", "messages", "profile"
}

DEFAULT_SECTION_ORDER = [
    "home", "about", "skills", "experience", "projects", "education",
    "certifications", "achievements", "services", "contact"
]

DEFAULT_SECTION_VISIBILITY = {
    "home": True,
    "about": True,
    "skills": True,
    "experience": True,
    "projects": True,
    "education": True,
    "certifications": True,
    "achievements": True,
    "services": True,
    "contact": True,
}


def normalize_education_items(edu_data: Any) -> list:
    """Normalizes and cleans education items to prevent broken or corrupted degree displays."""
    if isinstance(edu_data, str):
        try:
            edu_data = json.loads(edu_data)
        except Exception:
            return []
    if not isinstance(edu_data, list):
        return []

    normalized = []
    for item in edu_data:
        if not isinstance(item, dict):
            continue
        deg = (item.get("degree") or "").strip()
        inst = (item.get("institution") or "").strip()
        field = (item.get("field_of_study") or "").strip()
        end_year = str(item.get("end_year") or item.get("year") or "").strip()
        score = (item.get("score") or item.get("details") or item.get("grade") or "").strip()

        # 1. Extract GPA / score from institution if embedded
        m_score = re.search(r"\b(?:c?gpa|grade|score|percentage)\s*[:\-–—]?\s*(\d+(?:\.\d+)?(?:\s*/\s*\d+)?(?:\s*(?:cgpa|gpa|%))?)", inst, re.I)
        if not m_score:
            m_score = re.search(r"[\s,\-|–—]+(\d+(?:\.\d+)?\s*(?:/\s*\d+)?\s*(?:%|cgpa|gpa))\b", inst, re.I)
        if m_score:
            if not score or score == "-":
                score = m_score.group(0).strip(" ,-|.")
            inst = re.sub(r"\s*[\s,\-|–—]*\b(?:c?gpa|grade|score|percentage)\s*[:\-–—]?\s*\d+(?:\.\d+)?(?:\s*/\s*\d+)?(?:\s*(?:cgpa|gpa|%))?.*$", "", inst, flags=re.I).strip(" ,-|.")
            inst = re.sub(r"[\s,\-|–—]+(?:\d+(?:\.\d+)?\s*(?:/\s*\d+)?\s*(?:%|cgpa|gpa))\b.*$", "", inst, flags=re.I).strip(" ,-|.")

        if score == "-":
            score = ""

        # 2. Check for orphan / dummy entry
        is_orphan = (not inst or inst == "-" or inst.lower() in ("n/a", "none")) and (not deg or deg.lower() in ("academic degree", "education", "-"))
        if is_orphan:
            if end_year and normalized:
                target = next((e for e in normalized if not e.get("end_year") and any(k in (e.get("degree") or "").lower() for k in ("bachelor", "degree", "b.sc", "b.tech", "academic"))), normalized[-1])
                if not target.get("end_year"):
                    target["end_year"] = end_year
            if score and normalized and not normalized[-1].get("score"):
                normalized[-1]["score"] = score
                normalized[-1]["details"] = score
            continue

        if (not inst or inst == "-") and end_year and not field and not score and normalized and not normalized[-1].get("end_year"):
            normalized[-1]["end_year"] = end_year
            continue

        # 3. Clean placeholder degrees
        if not deg or deg.lower() in ("academic degree", "education", "degree") or deg == "-":
            if "arts and science" in inst.lower() or "college of science" in inst.lower():
                deg = f"Bachelor of Science ({field.split('/')[0].strip()})" if field else "Bachelor of Science (B.Sc)"
            elif field and any(kw in field.lower() for kw in ("computer", "engineering", "tech")):
                deg = "Bachelor of Science / Engineering"
            elif field:
                deg = f"Bachelor's Degree in {field}"
            else:
                deg = "Bachelor's Degree"

        # 4. Clean HSC / SSLC
        if "HSC" in deg.upper() or "HIGHER SECONDARY" in deg.upper():
            deg = "Higher Secondary Certificate (HSC)"
            if not inst or inst == "-" or "higher secondary certificate" in inst.lower() or "hsc" in inst.lower():
                inst = "State Board / Higher Secondary School"
            field = field or "Higher Secondary (12th)"
        elif "SSLC" in deg.upper() or "SECONDARY" in deg.upper():
            deg = "Secondary School Leaving Certificate (SSLC)"
            if not inst or inst == "-" or "secondary school leaving" in inst.lower() or "sslc" in inst.lower():
                inst = "State Board / Secondary School"
            field = field or "Secondary Education (10th)"
        elif "higher secondary certificate" in inst.lower():
            inst = "State Board / Higher Secondary School"

        inst = inst.strip(" ,-|.")

        cleaned_item = dict(item)
        cleaned_item["degree"] = deg
        cleaned_item["institution"] = inst or "Institution"
        cleaned_item["field_of_study"] = field or None
        cleaned_item["end_year"] = end_year or item.get("end_year") or ""
        cleaned_item["start_year"] = item.get("start_year") or ""
        cleaned_item["score"] = score or item.get("score") or ""
        cleaned_item["details"] = score or item.get("details") or ""
        normalized.append(cleaned_item)

    return normalized


def sanitize_slug(text: str) -> str:
    """Creates a URL-safe lowercase slug."""
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "portfolio"


def generate_unique_slug(db: Session, base_text: str, exclude_portfolio_id: Optional[uuid.UUID] = None) -> str:
    """
    Generates a unique, readable URL slug based on candidate's name or role.
    Example: 'yuvaraj', 'yuvaraj-2', 'yuvaraj-ai-developer'
    """
    base_slug = sanitize_slug(base_text)
    if base_slug in RESERVED_SLUGS:
        base_slug = f"{base_slug}-dev"

    slug = base_slug
    counter = 1

    while True:
        query = db.query(Portfolio).filter(Portfolio.slug == slug)
        if exclude_portfolio_id:
            query = query.filter(Portfolio.id != exclude_portfolio_id)
        exists = query.first()

        if not exists and slug not in RESERVED_SLUGS:
            return slug

        counter += 1
        slug = f"{base_slug}-{counter}"


def is_slug_available(db: Session, requested_slug: str, exclude_portfolio_id: Optional[uuid.UUID] = None) -> bool:
    """Checks if requested slug is valid, non-reserved, and available."""
    clean = sanitize_slug(requested_slug)
    if not clean or clean in RESERVED_SLUGS:
        return False

    query = db.query(Portfolio).filter(Portfolio.slug == clean)
    if exclude_portfolio_id:
        query = query.filter(Portfolio.id != exclude_portfolio_id)
    return query.first() is None


def get_candidate_portfolio(db: Session, candidate_id: uuid.UUID) -> Optional[Portfolio]:
    """Retrieves existing portfolio for candidate if present."""
    return (
        db.query(Portfolio)
        .options(joinedload(Portfolio.candidate).joinedload(CandidateProfile.user))
        .filter(Portfolio.candidate_id == candidate_id)
        .first()
    )


THEME_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "developer": {
        "primary_color": "#58a6ff",
        "secondary_color": "#7ee787",
        "font": "Fira Code",
        "background_style": "grid",
        "card_style": "bordered",
        "dark_mode": True,
        "button_style": "sharp",
        "layout": "split_terminal",
    },
    "ai_tech": {
        "primary_color": "#06b6d4",
        "secondary_color": "#a855f7",
        "font": "Plus Jakarta Sans",
        "background_style": "mesh",
        "card_style": "glass",
        "dark_mode": True,
        "button_style": "glow",
        "layout": "ai_hud",
    },
    "creative": {
        "primary_color": "#ec4899",
        "secondary_color": "#f59e0b",
        "font": "Outfit",
        "background_style": "mesh",
        "card_style": "glass",
        "dark_mode": False,
        "button_style": "pill",
        "layout": "asymmetric_studio",
    },
    "corporate": {
        "primary_color": "#1e3a8a",
        "secondary_color": "#0284c7",
        "font": "Plus Jakarta Sans",
        "background_style": "clean",
        "card_style": "elevated",
        "dark_mode": False,
        "button_style": "sharp",
        "layout": "executive_briefing",
    },
    "minimal": {
        "primary_color": "#111827",
        "secondary_color": "#6b7280",
        "font": "Inter",
        "background_style": "clean",
        "card_style": "flat",
        "dark_mode": False,
        "button_style": "rounded",
        "layout": "swiss_minimal",
    },
    "dark": {
        "primary_color": "#6366f1",
        "secondary_color": "#38bdf8",
        "font": "Plus Jakarta Sans",
        "background_style": "dots",
        "card_style": "glass",
        "dark_mode": True,
        "button_style": "rounded",
        "layout": "dark_luxury",
    },
    "elegant": {
        "primary_color": "#92643b",
        "secondary_color": "#4a5568",
        "font": "Playfair Display",
        "background_style": "clean",
        "card_style": "elevated",
        "dark_mode": False,
        "button_style": "sharp",
        "layout": "editorial_gazette",
    },
    "modern": {
        "primary_color": "#4f46e5",
        "secondary_color": "#06b6d4",
        "font": "Plus Jakarta Sans",
        "background_style": "mesh",
        "card_style": "glass",
        "dark_mode": False,
        "button_style": "rounded",
        "layout": "bento",
    },
    "notion": {
        "primary_color": "#2563eb",
        "secondary_color": "#64748b",
        "font": "Inter",
        "background_style": "clean",
        "card_style": "bordered",
        "dark_mode": False,
        "button_style": "rounded",
        "layout": "notion",
    },
    "timeline": {
        "primary_color": "#4f46e5",
        "secondary_color": "#06b6d4",
        "font": "Plus Jakarta Sans",
        "background_style": "mesh",
        "card_style": "glass",
        "dark_mode": False,
        "button_style": "rounded",
        "layout": "timeline",
    },
    "dashboard": {
        "primary_color": "#326ce5",
        "secondary_color": "#00d2d3",
        "font": "Fira Code",
        "background_style": "grid",
        "card_style": "bordered",
        "dark_mode": True,
        "button_style": "sharp",
        "layout": "dashboard",
    },
    "split_screen": {
        "primary_color": "#18181b",
        "secondary_color": "#ef4444",
        "font": "Space Grotesk",
        "background_style": "clean",
        "card_style": "flat",
        "dark_mode": False,
        "button_style": "sharp",
        "layout": "split_screen",
    },
}

THEME_PALETTES: Dict[str, List[Dict[str, Any]]] = {
    "developer": [
        {"name": "GitHub Dark", "primary_color": "#58a6ff", "secondary_color": "#7ee787", "font": "Fira Code", "background_style": "grid", "card_style": "bordered", "dark_mode": True, "button_style": "sharp", "layout": "split_terminal"},
        {"name": "Dracula Neon", "primary_color": "#bd93f9", "secondary_color": "#50fa7b", "font": "Fira Code", "background_style": "dots", "card_style": "bordered", "dark_mode": True, "button_style": "sharp", "layout": "split_terminal"},
        {"name": "Cyber Matrix", "primary_color": "#00f2fe", "secondary_color": "#4facfe", "font": "Fira Code", "background_style": "grid", "card_style": "glass", "dark_mode": True, "button_style": "glow", "layout": "split_terminal"},
        {"name": "Monokai Pro", "primary_color": "#ffd866", "secondary_color": "#ff6188", "font": "Fira Code", "background_style": "clean", "card_style": "bordered", "dark_mode": True, "button_style": "sharp", "layout": "split_terminal"},
        {"name": "One Dark Emerald", "primary_color": "#61afef", "secondary_color": "#98c379", "font": "Fira Code", "background_style": "grid", "card_style": "bordered", "dark_mode": True, "button_style": "rounded", "layout": "split_terminal"},
        {"name": "Tokyo Night", "primary_color": "#7aa2f7", "secondary_color": "#bb9af7", "font": "Fira Code", "background_style": "dots", "card_style": "glass", "dark_mode": True, "button_style": "glow", "layout": "split_terminal"},
    ],
    "modern": [
        {"name": "Electric Indigo", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": False, "button_style": "rounded", "layout": "bento"},
        {"name": "Sunset Violet", "primary_color": "#7c3aed", "secondary_color": "#f43f5e", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": False, "button_style": "pill", "layout": "bento"},
        {"name": "Ocean Emerald", "primary_color": "#0284c7", "secondary_color": "#10b981", "font": "Plus Jakarta Sans", "background_style": "dots", "card_style": "glass", "dark_mode": False, "button_style": "rounded", "layout": "bento"},
        {"name": "Aurora Teal", "primary_color": "#0d9488", "secondary_color": "#6366f1", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "elevated", "dark_mode": False, "button_style": "pill", "layout": "bento"},
        {"name": "Midnight Rose", "primary_color": "#e11d48", "secondary_color": "#8b5cf6", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": False, "button_style": "rounded", "layout": "bento"},
    ],
    "creative": [
        {"name": "Neon Flamingo", "primary_color": "#ec4899", "secondary_color": "#f59e0b", "font": "Outfit", "background_style": "mesh", "card_style": "glass", "dark_mode": False, "button_style": "pill", "layout": "asymmetric_studio"},
        {"name": "Cosmic Candy", "primary_color": "#8b5cf6", "secondary_color": "#ec4899", "font": "Outfit", "background_style": "mesh", "card_style": "bordered", "dark_mode": False, "button_style": "pill", "layout": "asymmetric_studio"},
        {"name": "Tropic Tangerine", "primary_color": "#f97316", "secondary_color": "#06b6d4", "font": "Outfit", "background_style": "dots", "card_style": "elevated", "dark_mode": False, "button_style": "rounded", "layout": "asymmetric_studio"},
        {"name": "Electric Lime", "primary_color": "#10b981", "secondary_color": "#f43f5e", "font": "Outfit", "background_style": "mesh", "card_style": "bordered", "dark_mode": False, "button_style": "pill", "layout": "asymmetric_studio"},
        {"name": "Hyper Coral", "primary_color": "#ff4757", "secondary_color": "#ffa502", "font": "Outfit", "background_style": "mesh", "card_style": "glass", "dark_mode": False, "button_style": "pill", "layout": "asymmetric_studio"},
    ],
    "corporate": [
        {"name": "Executive Navy", "primary_color": "#1e3a8a", "secondary_color": "#0284c7", "font": "Plus Jakarta Sans", "background_style": "clean", "card_style": "elevated", "dark_mode": False, "button_style": "sharp", "layout": "executive_briefing"},
        {"name": "Slate Sapphire", "primary_color": "#0f172a", "secondary_color": "#2563eb", "font": "Plus Jakarta Sans", "background_style": "clean", "card_style": "bordered", "dark_mode": False, "button_style": "sharp", "layout": "executive_briefing"},
        {"name": "Steel Cobalt", "primary_color": "#1e293b", "secondary_color": "#0ea5e9", "font": "Plus Jakarta Sans", "background_style": "dots", "card_style": "elevated", "dark_mode": False, "button_style": "sharp", "layout": "executive_briefing"},
        {"name": "Royal Prussian", "primary_color": "#0c2340", "secondary_color": "#38bdf8", "font": "Plus Jakarta Sans", "background_style": "clean", "card_style": "elevated", "dark_mode": False, "button_style": "sharp", "layout": "executive_briefing"},
    ],
    "ai_tech": [
        {"name": "Quantum Cyan", "primary_color": "#06b6d4", "secondary_color": "#a855f7", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": True, "button_style": "glow", "layout": "ai_hud"},
        {"name": "Neon Violet", "primary_color": "#8b5cf6", "secondary_color": "#38bdf8", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": True, "button_style": "glow", "layout": "ai_hud"},
        {"name": "Cyber Emerald", "primary_color": "#10b981", "secondary_color": "#06b6d4", "font": "Plus Jakarta Sans", "background_style": "grid", "card_style": "bordered", "dark_mode": True, "button_style": "glow", "layout": "ai_hud"},
        {"name": "Hologram Magenta", "primary_color": "#d946ef", "secondary_color": "#06b6d4", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": True, "button_style": "glow", "layout": "ai_hud"},
    ],
    "dark": [
        {"name": "Titanium Indigo", "primary_color": "#6366f1", "secondary_color": "#38bdf8", "font": "Plus Jakarta Sans", "background_style": "dots", "card_style": "glass", "dark_mode": True, "button_style": "rounded", "layout": "dark_luxury"},
        {"name": "Obsidian Gold", "primary_color": "#fbbf24", "secondary_color": "#f59e0b", "font": "Plus Jakarta Sans", "background_style": "mesh", "card_style": "glass", "dark_mode": True, "button_style": "rounded", "layout": "dark_luxury"},
        {"name": "Midnight Emerald", "primary_color": "#34d399", "secondary_color": "#38bdf8", "font": "Plus Jakarta Sans", "background_style": "dots", "card_style": "glass", "dark_mode": True, "button_style": "rounded", "layout": "dark_luxury"},
        {"name": "Eclipse Violet", "primary_color": "#a855f7", "secondary_color": "#ec4899", "font": "Plus Jakarta Sans", "background_style": "dots", "card_style": "glass", "dark_mode": True, "button_style": "glow", "layout": "dark_luxury"},
    ],
    "elegant": [
        {"name": "Tuscan Bronze", "primary_color": "#92643b", "secondary_color": "#4a5568", "font": "Playfair Display", "background_style": "clean", "card_style": "elevated", "dark_mode": False, "button_style": "sharp", "layout": "editorial_gazette"},
        {"name": "Burgundy Heritage", "primary_color": "#881337", "secondary_color": "#b45309", "font": "Playfair Display", "background_style": "clean", "card_style": "elevated", "dark_mode": False, "button_style": "sharp", "layout": "editorial_gazette"},
        {"name": "Champagne Gold", "primary_color": "#b45309", "secondary_color": "#475569", "font": "Playfair Display", "background_style": "clean", "card_style": "bordered", "dark_mode": False, "button_style": "sharp", "layout": "editorial_gazette"},
        {"name": "Olive & Linen", "primary_color": "#4d7c0f", "secondary_color": "#78716c", "font": "Playfair Display", "background_style": "clean", "card_style": "elevated", "dark_mode": False, "button_style": "sharp", "layout": "editorial_gazette"},
    ],
    "minimal": [
        {"name": "Swiss Monochrome", "primary_color": "#111827", "secondary_color": "#6b7280", "font": "Inter", "background_style": "clean", "card_style": "flat", "dark_mode": False, "button_style": "rounded", "layout": "swiss_minimal"},
        {"name": "Cool Slate", "primary_color": "#1e293b", "secondary_color": "#64748b", "font": "Inter", "background_style": "clean", "card_style": "flat", "dark_mode": False, "button_style": "sharp", "layout": "swiss_minimal"},
        {"name": "Charcoal Indigo", "primary_color": "#1e1e2e", "secondary_color": "#475569", "font": "Inter", "background_style": "dots", "card_style": "bordered", "dark_mode": False, "button_style": "rounded", "layout": "swiss_minimal"},
        {"name": "Onyx Editorial", "primary_color": "#09090b", "secondary_color": "#71717a", "font": "Inter", "background_style": "clean", "card_style": "flat", "dark_mode": False, "button_style": "sharp", "layout": "swiss_minimal"},
    ],
}


def get_candidate_theme_tokens(theme_id: str, candidate_seed: int = 0) -> Dict[str, Any]:
    """
    Selects a distinctive, harmonious token palette and layout architecture for the candidate.
    Uses candidate_seed to ensure different candidates receive unique palettes and styles.
    """
    theme = (theme_id or "modern").lower()
    palette_list = THEME_PALETTES.get(theme)
    if palette_list:
        idx = candidate_seed % len(palette_list)
        return palette_list[idx]
    
    # Check category prefixes
    for prefix in ("developer", "creative", "corporate", "ai_tech", "dark", "elegant", "minimal", "notion", "timeline", "dashboard", "split_screen"):
        if prefix in theme or theme.startswith(prefix):
            prefix_palettes = THEME_PALETTES.get(prefix)
            if prefix_palettes:
                return prefix_palettes[candidate_seed % len(prefix_palettes)]
            if prefix in THEME_DEFAULTS:
                return THEME_DEFAULTS[prefix]

    return THEME_DEFAULTS.get(theme, THEME_DEFAULTS["modern"])


def determine_candidate_theme(candidate: CandidateProfile, parsed_fields: dict, raw_text: str = "") -> str:
    """
    Intelligently assigns a theme tailored to the candidate's profile, domain, and skills.
    Ensures different candidates receive distinct themes from the comprehensive 80+ theme catalog.
    """
    role = (candidate.current_role or candidate.headline or parsed_fields.get("current_role") or "").lower()
    skills = [s.lower() for s in (parsed_fields.get("skills") or [])]
    if candidate.candidate_skills:
        skills.extend([cs.skill.skill_name.lower() for cs in candidate.candidate_skills if cs.skill])
    text = f"{role} {' '.join(skills)} {raw_text[:2000]}".lower()

    cand_id_int = candidate.id.int if candidate.id else abs(hash(candidate.user_id or candidate.headline or "candidate"))

    # 1. AI & Machine Learning / Data Science
    ai_keywords = ["machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision", "llm", "data scientist", "genai", "generative ai", "pytorch", "tensorflow", "neural", "langchain"]
    if any(k in text for k in ai_keywords):
        ai_pool = ["ai_tech", "ai_deepmind", "ai_quantum", "ai_agentic_swarm", "ai_neural_synapse", "ai_cyber_sentinel", "ai_singularity", "ai_biomorphic"]
        return ai_pool[cand_id_int % len(ai_pool)]

    # 2. Cybersecurity / Cloud Infrastructure / SRE / DevOps
    security_keywords = ["cybersecurity", "infosec", "security engineer", "penetration", "soc", "sre", "site reliability", "network engineer", "devops", "cloud architect"]
    if any(k in text for k in security_keywords):
        sec_pool = ["dark", "dark_obsidian", "dark_carbon_fibre", "dark_cyber_crimson", "tech_devops", "ai_cyber_sentinel"]
        return sec_pool[cand_id_int % len(sec_pool)]

    # 3. Creative / UI/UX / Frontend / Mobile / Product Design
    creative_keywords = ["frontend", "ui/ux", "ui designer", "ux designer", "product designer", "graphic", "web design", "mobile developer", "flutter", "ios developer", "android developer", "react native", "css", "animation"]
    if any(k in text for k in creative_keywords):
        creative_pool = ["creative", "creative_memphis", "creative_pop_art", "creative_avant_garde", "creative_pastel_dream", "creative_cyberpunk", "creative_claymorphism", "creative_editorial_art", "creative_vaporwave", "creative_poster"]
        return creative_pool[cand_id_int % len(creative_pool)]

    # 4. Management / Product / Executive / Corporate
    corporate_keywords = ["product manager", "project manager", "scrum master", "operations", "business analyst", "finance", "hr manager", "human resources", "sales manager", "director", "vp"]
    if any(k in text for k in corporate_keywords):
        corp_pool = ["corporate", "exec_mckinsey", "exec_wall_street", "exec_enterprise_cto", "exec_deloitte", "exec_private_equity", "exec_global_vp", "exec_legal_counsel"]
        return corp_pool[cand_id_int % len(corp_pool)]

    # 5. Consulting / Strategy / Architecture / Leadership / Academic
    elegant_keywords = ["consultant", "strategy", "architect", "lead consultant", "advisor", "principal architect", "legal", "lawyer", "phd", "researcher", "scholar"]
    if any(k in text for k in elegant_keywords):
        elegant_pool = ["elegant", "elegant_vogue", "elegant_cambridge", "elegant_broadsheet", "elegant_renaissance", "elegant_curator", "notion_paper"]
        return elegant_pool[cand_id_int % len(elegant_pool)]

    # 6. QA / Testing / Writing / Research / Minimalist / Notes
    minimal_keywords = ["qa engineer", "quality assurance", "test automation", "technical writer", "researcher", "content writer", "analyst", "documentation"]
    if any(k in text for k in minimal_keywords):
        min_pool = ["minimal", "swiss_zurich", "minimal_monocle", "minimal_bauhaus", "minimal_hairline", "minimal_ink", "minimal_studio", "minimal_brutalist_mono", "notion_doc"]
        return min_pool[cand_id_int % len(min_pool)]

    # 7. Software Engineering / Backend / Full Stack / Systems
    developer_keywords = ["software engineer", "backend", "full stack", "fullstack", "systems engineer", "python developer", "java developer", "golang", "rust", "c++", "docker", "kubernetes"]
    if any(k in text for k in developer_keywords):
        dev_pool = ["developer", "tech_matrix", "dev_dracula", "dev_one_dark", "dev_monokai", "dev_git_craft", "tech_rust_systems", "tech_solidity_web3", "tech_api_architect", "linear_noir"]
        return dev_pool[cand_id_int % len(dev_pool)]

    # 8. Full broad distribution across the catalog
    pool = [
        "modern", "linear_noir", "saas_stripe", "saas_vercel", "saas_supabase", "saas_craft", "saas_aurora", "saas_prism", "saas_sunset", "saas_raycast",
        "developer", "tech_matrix", "dev_dracula", "dev_one_dark", "dev_monokai", "dev_git_craft", "tech_devops", "tech_rust_systems", "tech_solidity_web3", "tech_api_architect",
        "creative", "creative_memphis", "creative_pop_art", "creative_avant_garde", "creative_pastel_dream", "creative_cyberpunk", "creative_claymorphism", "creative_editorial_art", "creative_vaporwave", "creative_poster",
        "corporate", "exec_mckinsey", "exec_wall_street", "exec_enterprise_cto", "exec_deloitte", "exec_private_equity", "exec_global_vp", "exec_legal_counsel",
        "ai_tech", "ai_deepmind", "ai_quantum", "ai_agentic_swarm", "ai_neural_synapse", "ai_cyber_sentinel", "ai_singularity", "ai_biomorphic",
        "minimal", "swiss_zurich", "minimal_monocle", "minimal_bauhaus", "minimal_hairline", "minimal_ink", "minimal_studio", "minimal_brutalist_mono",
        "dark", "dark_obsidian", "dark_emerald_gold", "dark_carbon_fibre", "dark_amethyst", "dark_champagne", "dark_sapphire", "dark_cyber_crimson",
        "elegant", "elegant_vogue", "elegant_cambridge", "elegant_broadsheet", "elegant_renaissance", "elegant_curator",
        "notion_doc", "notion_craft", "notion_obsidian", "notion_linear", "notion_paper", "notion_wiki",
        "timeline_journey", "timeline_space", "timeline_expedition", "timeline_craft", "timeline_metro", "timeline_chronicle"
    ]
    return pool[cand_id_int % len(pool)]


DOMAIN_BACKGROUND_PRESETS: Dict[str, Dict[str, str]] = {
    "ai_tech": {
        "domain": "Artificial Intelligence & Computational Systems",
        "url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=2000&q=80",
        "title": "AI & Neural Computing Studio",
        "description": "Computational research architecture and production machine learning engineering",
        "overlay": "rgba(6, 12, 28, 0.88)",
        "accent": "#06b6d4",
    },
    "developer": {
        "domain": "Software Engineering & Full Stack",
        "url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=2000&q=80",
        "title": "Software Engineering Workstation",
        "description": "Clean focused dual-monitor development environment with code syntax",
        "overlay": "rgba(10, 15, 26, 0.90)",
        "accent": "#3b82f6",
    },
    "cloud_devops": {
        "domain": "Cloud Infrastructure, DevOps & SRE",
        "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=2000&q=80",
        "title": "Distributed Cloud Architecture",
        "description": "High-density global cloud topology, container orchestration, and telemetry",
        "overlay": "rgba(8, 14, 29, 0.89)",
        "accent": "#0ea5e9",
    },
    "creative": {
        "domain": "UI/UX & Product Design",
        "url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=2000&q=80",
        "title": "Product Design & Prototyping Studio",
        "description": "Modern creative workstation with design systems and responsive prototyping",
        "overlay": "rgba(24, 16, 38, 0.86)",
        "accent": "#8b5cf6",
    },
    "corporate": {
        "domain": "Executive Leadership & Product Management",
        "url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=2000&q=80",
        "title": "Metropolitan Executive Architecture",
        "description": "Sunlit corporate boardroom and modern leadership environment",
        "overlay": "rgba(15, 23, 42, 0.88)",
        "accent": "#2563eb",
    },
    "elegant": {
        "domain": "Strategy Consulting & Architecture",
        "url": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=2000&q=80",
        "title": "Curated Strategy Advisory Studio",
        "description": "High-aesthetic Scandinavian consulting studio with bespoke natural daylight",
        "overlay": "rgba(28, 25, 23, 0.88)",
        "accent": "#d97706",
    },
    "minimal": {
        "domain": "Minimalist Engineering & Research",
        "url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=2000&q=80",
        "title": "Clean Minimalist Engineering Desk",
        "description": "Focused modern tech setup with notebook, clean architecture and quiet precision",
        "overlay": "rgba(17, 24, 39, 0.86)",
        "accent": "#64748b",
    },
    "dark": {
        "domain": "Dark Luxury & Systems Engineering",
        "url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=2000&q=80",
        "title": "Precision Hardware Systems Studio",
        "description": "Moody tech workspace with clean aesthetic hardware and ambient studio lighting",
        "overlay": "rgba(9, 9, 11, 0.92)",
        "accent": "#6366f1",
    },
    "saas": {
        "domain": "Modern SaaS & Product Engineering",
        "url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=2000&q=80",
        "title": "Modern Software Engineering Desk",
        "description": "Clean focused product development workspace with high productivity optics",
        "overlay": "rgba(15, 23, 42, 0.87)",
        "accent": "#6366f1",
    },
    "data_analytics": {
        "domain": "Data Science, Telemetry & Analytics",
        "url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=2000&q=80",
        "title": "Telemetry Analytics & Data Station",
        "description": "Real-time analytics dashboards, metrics telemetry, and quantitative insights",
        "overlay": "rgba(11, 19, 43, 0.89)",
        "accent": "#10b981",
    },
    "hr_recruiting": {
        "domain": "Talent Acquisition & People Operations",
        "url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=2000&q=80",
        "title": "People & Talent Strategy Studio",
        "description": "Collaborative modern team conference and strategic people operations",
        "overlay": "rgba(24, 16, 38, 0.86)",
        "accent": "#ec4899",
    },
    "mobile": {
        "domain": "Mobile & Edge Systems Engineering",
        "url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=2000&q=80",
        "title": "Mobile Device Interface Lab",
        "description": "Touchscreen development studio and edge mobile engineering",
        "overlay": "rgba(15, 23, 42, 0.88)",
        "accent": "#06b6d4",
    },
}


def determine_candidate_domain_background(
    candidate: Optional[CandidateProfile],
    parsed_fields: Optional[dict] = None,
    raw_text: str = "",
    theme_id: str = "modern"
) -> str:
    """
    Intelligently assigns a suitable, high-resolution, professional background image
    based on the candidate's professional domain, skills, role, and theme.
    """
    parsed_fields = parsed_fields or {}
    role = ""
    skills: List[str] = []
    if candidate:
        role = (candidate.current_role or candidate.headline or parsed_fields.get("current_role") or "").lower()
        if candidate.candidate_skills:
            skills.extend([cs.skill.skill_name.lower() for cs in candidate.candidate_skills if cs.skill])
    if not role:
        role = str(parsed_fields.get("current_role") or parsed_fields.get("headline") or "").lower()
    if parsed_fields.get("skills"):
        skills.extend([s.lower() for s in parsed_fields["skills"]])

    text = f"{role} {' '.join(skills)} {raw_text[:2000]}".lower()

    # 1. AI, Data Science & Machine Learning
    ai_keys = ["machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision", "llm", "data scientist", "genai", "pytorch", "tensorflow", "neural", "langchain"]
    if any(k in text for k in ai_keys):
        return DOMAIN_BACKGROUND_PRESETS["ai_tech"]["url"]

    # 2. Data Analytics & Business Intelligence
    analytics_keys = ["data analyst", "business intelligence", "power bi", "tableau", "analytics", "sql analyst", "data visualization", "bi developer"]
    if any(k in text for k in analytics_keys):
        return DOMAIN_BACKGROUND_PRESETS["data_analytics"]["url"]

    # 3. Cloud Infrastructure, DevOps & Cybersecurity
    cloud_keys = ["cybersecurity", "infosec", "soc", "sre", "devops", "cloud architect", "aws", "azure", "docker", "kubernetes", "terraform", "network engineer", "infrastructure"]
    if any(k in text for k in cloud_keys):
        return DOMAIN_BACKGROUND_PRESETS["cloud_devops"]["url"]

    # 4. Creative, UI/UX, Graphic & Product Design
    creative_keys = ["ui/ux", "ui designer", "ux designer", "product designer", "graphic designer", "web designer", "figma", "art director", "visual designer", "motion designer"]
    if any(k in text for k in creative_keys):
        return DOMAIN_BACKGROUND_PRESETS["creative"]["url"]

    # 5. HR, Talent Acquisition & People Operations
    hr_keys = ["recruiter", "talent acquisition", "human resources", "hr manager", "people operations", "talent specialist", "recruitment", "headhunter"]
    if any(k in text for k in hr_keys):
        return DOMAIN_BACKGROUND_PRESETS["hr_recruiting"]["url"]

    # 6. Mobile App Development
    mobile_keys = ["mobile developer", "flutter", "ios developer", "android developer", "react native", "swift", "kotlin"]
    if any(k in text for k in mobile_keys):
        return DOMAIN_BACKGROUND_PRESETS["mobile"]["url"]

    # 7. Corporate, Leadership & Management
    corp_keys = ["product manager", "project manager", "scrum master", "operations", "business analyst", "finance", "director", "vp", "chief", "executive"]
    if any(k in text for k in corp_keys):
        return DOMAIN_BACKGROUND_PRESETS["corporate"]["url"]

    # 8. Consulting & Strategy
    consulting_keys = ["consultant", "strategy", "architect", "lead consultant", "advisor", "legal", "lawyer", "phd", "researcher"]
    if any(k in text for k in consulting_keys):
        return DOMAIN_BACKGROUND_PRESETS["elegant"]["url"]

    # 9. Software Engineering / Full Stack / Backend / Frontend
    dev_keys = ["software engineer", "backend", "full stack", "fullstack", "python developer", "java developer", "golang", "c++", "frontend developer", "web developer", "developer"]
    if any(k in text for k in dev_keys):
        return DOMAIN_BACKGROUND_PRESETS["developer"]["url"]

    # 10. Theme-based fallback
    t = (theme_id or "").lower()
    if any(p in t for p in ("ai_", "quantum", "singularity")):
        return DOMAIN_BACKGROUND_PRESETS["ai_tech"]["url"]
    if any(p in t for p in ("dev", "tech_", "matrix", "code", "terminal")):
        return DOMAIN_BACKGROUND_PRESETS["developer"]["url"]
    if any(p in t for p in ("creative", "pop_art", "memphis", "studio")):
        return DOMAIN_BACKGROUND_PRESETS["creative"]["url"]
    if any(p in t for p in ("exec", "corp", "deloitte", "mckinsey")):
        return DOMAIN_BACKGROUND_PRESETS["corporate"]["url"]
    if any(p in t for p in ("elegant", "vogue", "broadsheet", "renaissance")):
        return DOMAIN_BACKGROUND_PRESETS["elegant"]["url"]
    if any(p in t for p in ("dark", "obsidian", "carbon", "amethyst", "noir")):
        return DOMAIN_BACKGROUND_PRESETS["dark"]["url"]
    if any(p in t for p in ("minimal", "swiss", "bauhaus", "hairline")):
        return DOMAIN_BACKGROUND_PRESETS["minimal"]["url"]

    return DOMAIN_BACKGROUND_PRESETS["developer"]["url"]


def build_portfolio_from_candidate_profile(
    db: Session,
    candidate: CandidateProfile,
    theme_id: Optional[str] = None,
    file_bytes: Optional[bytes] = None,
    filename: Optional[str] = None
) -> Portfolio:
    """
    Creates or updates the candidate's portfolio using existing resume data or uploaded file.
    Does NOT duplicate portfolios; reuses existing record.
    """
    # 1. Obtain raw text and parsed fields
    raw_text = ""
    parsed_fields: Dict[str, Any] = {}

    if file_bytes and filename:
        raw_text = extract_resume_text(file_bytes, filename)
        parsed_fields = parse_resume_fields(raw_text)
    else:
        # Reuse existing candidate profile data and parse resume text fresh
        raw_text = candidate.resume_text or ""
        if not raw_text.strip() and candidate.resume_path and os.path.exists(candidate.resume_path):
            try:
                with open(candidate.resume_path, "rb") as f:
                    raw_text = extract_resume_text(f.read(), os.path.basename(candidate.resume_path))
            except Exception:
                pass

        if raw_text.strip():
            parsed_fields = parse_resume_fields(raw_text)
        else:
            parsed_fields = {}

        # Augment with candidate profile fields if not already populated from resume text
        if not parsed_fields.get("name") and candidate.full_name:
            parsed_fields["name"] = candidate.full_name
        if not parsed_fields.get("phone") and candidate.phone:
            parsed_fields["phone"] = candidate.phone
        if not parsed_fields.get("location") and candidate.location:
            parsed_fields["location"] = candidate.location
        if not parsed_fields.get("headline") and candidate.headline and not candidate.headline.lower().endswith("| professional"):
            parsed_fields["headline"] = candidate.headline
        if not parsed_fields.get("current_role") and candidate.current_role and candidate.current_role.lower() not in ("software professional", "professional"):
            parsed_fields["current_role"] = candidate.current_role
        if not parsed_fields.get("summary") and (candidate.summary or candidate.ai_summary):
            cand_sum = candidate.summary or candidate.ai_summary or ""
            if not cand_sum.lower().startswith("professional portfolio for"):
                parsed_fields["summary"] = cand_sum
        if not parsed_fields.get("linkedin_url") and candidate.linkedin_url:
            parsed_fields["linkedin_url"] = candidate.linkedin_url
        if not parsed_fields.get("github_url") and candidate.github_url:
            parsed_fields["github_url"] = candidate.github_url
        if not parsed_fields.get("portfolio_url") and candidate.portfolio_url:
            parsed_fields["portfolio_url"] = candidate.portfolio_url
        if not parsed_fields.get("skills"):
            parsed_skills = [cs.skill.skill_name for cs in candidate.candidate_skills] if candidate.candidate_skills else []
            parsed_fields["skills"] = parsed_skills
        if not parsed_fields.get("certifications") and candidate.certifications:
            parsed_fields["certifications"] = candidate.certifications
        if not parsed_fields.get("education") and candidate.education:
            parsed_fields["education"] = candidate.education
        if not parsed_fields.get("work_experience") and candidate.work_experience:
            parsed_fields["work_experience"] = candidate.work_experience

    # Priority for email address:
    # 1. Email explicitly extracted from raw resume text
    # 2. Email extracted from candidate.resume_text if available
    # 3. Only if NO resume email is found anywhere, fall back to candidate.user.email
    resume_email = None
    if raw_text:
        resume_email = extract_email(raw_text)
    if not resume_email and candidate.resume_text:
        resume_email = extract_email(candidate.resume_text)

    if resume_email:
        parsed_fields["email"] = resume_email
    elif not parsed_fields.get("email") and candidate.user and candidate.user.email:
        parsed_fields["email"] = candidate.user.email

    # If raw_text was empty but candidate had education/experience strings, stitch them
    if not raw_text:
        raw_text = f"{parsed_fields.get('name')}\n{parsed_fields.get('summary')}\n{parsed_fields.get('work_experience')}\n{parsed_fields.get('education')}"

    # 2. Run structured entity extraction verbatim without hallucination
    extracted = extract_structured_portfolio_data(raw_text, parsed_fields)

    # 3. Check for existing portfolio
    existing = get_candidate_portfolio(db, candidate.id)

    # Determine unique slug
    cand_name = candidate.full_name or parsed_fields.get("name") or "candidate"
    cand_role = candidate.current_role or parsed_fields.get("current_role") or ""
    slug_seed = f"{cand_name} {cand_role}".strip()

    # Determine candidate theme
    if not theme_id or theme_id in ("modern", "auto"):
        # Auto-detect personalized theme based on candidate role and skills
        chosen_theme = determine_candidate_theme(candidate, parsed_fields, raw_text)
    else:
        chosen_theme = theme_id

    cand_seed = abs(hash(f"{candidate.id}_{cand_name}_{cand_role}_{candidate.user_id}")) if candidate else 0
    tokens = get_candidate_theme_tokens(chosen_theme, cand_seed)
    domain_bg = determine_candidate_domain_background(candidate, parsed_fields, raw_text, chosen_theme)

    if existing:
        portfolio = existing
        if theme_id and theme_id != "auto":
            portfolio.theme_id = theme_id
        elif not portfolio.theme_id or portfolio.theme_id == "modern":
            portfolio.theme_id = chosen_theme
            portfolio.primary_color = tokens["primary_color"]
            portfolio.secondary_color = tokens["secondary_color"]
            portfolio.font = tokens["font"]
            portfolio.background_style = tokens["background_style"]
            portfolio.dark_mode = tokens["dark_mode"]
            portfolio.card_style = tokens["card_style"]
            portfolio.button_style = tokens["button_style"]
            portfolio.layout = tokens.get("layout", "standard")
        if not portfolio.background_image or "photo-1557683316-973673baf926" in portfolio.background_image:
            portfolio.background_image = domain_bg
    else:
        unique_slug = generate_unique_slug(db, slug_seed)
        portfolio = Portfolio(
            id=uuid.uuid4(),
            candidate_id=candidate.id,
            slug=unique_slug,
            is_published=False,
            theme_id=chosen_theme,
            background_image=domain_bg,
            primary_color=tokens["primary_color"],
            secondary_color=tokens["secondary_color"],
            font=tokens["font"],
            background_style=tokens["background_style"],
            dark_mode=tokens["dark_mode"],
            card_style=tokens["card_style"],
            button_style=tokens["button_style"],
            layout=tokens.get("layout", "standard"),
            views_count=0,
        )
        db.add(portfolio)

    # Populate portfolio content fields
    portfolio.professional_headline = extracted["professional_headline"]
    portfolio.headline_options = json.dumps(extracted["headline_options"])
    portfolio.about = extracted["about"]
    portfolio.skills = json.dumps(extracted["skills"])
    portfolio.experience = json.dumps(extracted["experience"])
    portfolio.education = json.dumps(normalize_education_items(extracted["education"]))
    portfolio.projects = json.dumps(extracted["projects"])
    portfolio.certifications = json.dumps(extracted["certifications"])
    portfolio.achievements = json.dumps(extracted["achievements"])
    portfolio.services = json.dumps(extracted["services"])
    portfolio.social_links = json.dumps(extracted["social_links"])

    # Configure defaults if not previously set
    if not portfolio.section_order:
        portfolio.section_order = json.dumps(DEFAULT_SECTION_ORDER)
    if not portfolio.section_visibility:
        initial_vis = dict(DEFAULT_SECTION_VISIBILITY)
        if not extracted.get("achievements"):
            initial_vis["achievements"] = False
        if not extracted.get("services"):
            initial_vis["services"] = False
        if not extracted.get("certifications"):
            initial_vis["certifications"] = False
        portfolio.section_visibility = json.dumps(initial_vis)
    else:
        try:
            curr_vis = json.loads(portfolio.section_visibility)
            if not extracted.get("achievements"):
                curr_vis["achievements"] = False
            if not extracted.get("services"):
                curr_vis["services"] = False
            if not extracted.get("certifications"):
                curr_vis["certifications"] = False
            portfolio.section_visibility = json.dumps(curr_vis)
        except Exception:
            pass

    if not portfolio.profile_image and candidate.profile_photo:
        portfolio.profile_image = candidate.profile_photo

    db.commit()
    db.refresh(portfolio)
    return portfolio


def update_candidate_portfolio(db: Session, portfolio: Portfolio, updates: Dict[str, Any]) -> Portfolio:
    """Applies updates to portfolio content, styling, theme, or slug."""

    if "slug" in updates and updates["slug"]:
        new_slug = sanitize_slug(updates["slug"])
        if new_slug != portfolio.slug:
            if not is_slug_available(db, new_slug, exclude_portfolio_id=portfolio.id):
                raise BadRequestError(f"Slug '{new_slug}' is already taken or reserved.")
            portfolio.slug = new_slug

    if "theme_id" in updates and updates["theme_id"]:
        portfolio.theme_id = str(updates["theme_id"]).strip().lower()

    # Visual custom tokens
    for attr in ["primary_color", "secondary_color", "font", "background_style", "button_style", "card_style", "layout"]:
        if attr in updates and updates[attr] is not None:
            setattr(portfolio, attr, str(updates[attr]).strip())

    if "dark_mode" in updates and updates["dark_mode"] is not None:
        portfolio.dark_mode = bool(updates["dark_mode"])

    # Content attributes
    if "candidate_name" in updates and updates["candidate_name"]:
        cand = portfolio.candidate
        if cand and cand.user:
            cand.user.name = str(updates["candidate_name"]).strip()
    if "profile_image" in updates:
        portfolio.profile_image = updates["profile_image"]
    if "background_image" in updates:
        portfolio.background_image = updates["background_image"]
    if "professional_headline" in updates:
        portfolio.professional_headline = updates["professional_headline"]
    if "about" in updates:
        portfolio.about = updates["about"]
    if "custom_css" in updates:
        portfolio.custom_css = updates["custom_css"]

    # JSON fields
    json_fields = [
        "skills", "experience", "education", "projects", "certifications",
        "achievements", "services", "social_links", "section_order",
        "section_visibility", "headline_options"
    ]
    for jf in json_fields:
        if jf in updates and updates[jf] is not None:
            val = updates[jf]
            if jf == "education":
                val = normalize_education_items(val)
            if isinstance(val, (dict, list)):
                setattr(portfolio, jf, json.dumps(val))
            elif isinstance(val, str):
                setattr(portfolio, jf, val)

    db.commit()
    db.refresh(portfolio)
    return portfolio


def publish_candidate_portfolio(db: Session, portfolio: Portfolio) -> Portfolio:
    """Publishes candidate portfolio making public URL active."""
    portfolio.is_published = True
    db.commit()
    db.refresh(portfolio)
    return portfolio


def unpublish_candidate_portfolio(db: Session, portfolio: Portfolio) -> Portfolio:
    """Unpublishes candidate portfolio making public URL inaccessible."""
    portfolio.is_published = False
    db.commit()
    db.refresh(portfolio)
    return portfolio


def get_public_portfolio(db: Session, slug: str) -> Tuple[Portfolio, str]:
    """
    Retrieves published portfolio by slug.
    Raises NotFoundError if unpublished or non-existent.
    Increments view count.
    """
    clean_slug = sanitize_slug(slug)
    portfolio = (
        db.query(Portfolio)
        .options(joinedload(Portfolio.candidate).joinedload(CandidateProfile.user))
        .filter(Portfolio.slug == clean_slug)
        .first()
    )

    if not portfolio:
        # Fallback by candidate name prefix (e.g. keira-waldemer-*) so old/alternate slugs resolve seamlessly
        parts = clean_slug.split("-")
        if len(parts) >= 2:
            prefix = f"{parts[0]}-{parts[1]}"
            portfolio = (
                db.query(Portfolio)
                .options(joinedload(Portfolio.candidate).joinedload(CandidateProfile.user))
                .filter(Portfolio.slug.like(f"{prefix}%"))
                .first()
            )

    if not portfolio or not portfolio.is_published:
        raise NotFoundError("Portfolio not found or has not been published yet.")

    portfolio.views_count += 1
    db.commit()

    cand_name = portfolio.candidate.full_name if portfolio.candidate else "Professional Portfolio"
    return portfolio, cand_name


def format_portfolio_dict(portfolio: Portfolio, public_only: bool = False, db: Optional[Session] = None) -> Dict[str, Any]:
    """Serializes portfolio model to dictionary with deserialized JSON structures."""
    if db is None:
        try:
            db = object_session(portfolio)
        except Exception:
            db = None

    cand = portfolio.candidate
    cand_user = cand.user if cand else None
    cand_name = cand.full_name if cand else "Candidate"

    def safe_json_load(text_val: Optional[str], default_val: Any) -> Any:
        if not text_val:
            return default_val
        try:
            return json.loads(text_val)
        except Exception:
            return default_val

    skills_data = safe_json_load(portfolio.skills, {})
    exp_data = safe_json_load(portfolio.experience, [])
    edu_data = safe_json_load(portfolio.education, [])
    proj_data = safe_json_load(portfolio.projects, [])
    cert_data = safe_json_load(portfolio.certifications, [])
    ach_data = safe_json_load(portfolio.achievements, [])
    srv_data = safe_json_load(portfolio.services, [])
    soc_data = safe_json_load(portfolio.social_links, {})
    if not isinstance(soc_data, dict):
        soc_data = {}

    # Strict Guarantee: Accurately synchronize education details with candidate resume
    raw_edu = safe_json_load(portfolio.education, [])
    edu_data = normalize_education_items(raw_edu)

    if cand and cand.resume_text:
        from app.nlp.skill_extractor import parse_education_items, extract_section_text, _EDUCATION_HEADING_RE
        edu_sec = extract_section_text(cand.resume_text, _EDUCATION_HEADING_RE)
        if edu_sec:
            fresh_edu = parse_education_items(edu_sec)
            has_corrupted = any(
                e.get("institution") in ("SCHOOL, HSC", "HSC", "SSLC", "-") or
                e.get("degree") in ("Academic Degree", "Education", "-") or
                "gpa:" in (e.get("institution") or "").lower() or
                "cgpa:" in (e.get("institution") or "").lower()
                for e in edu_data
            ) if isinstance(edu_data, list) else True
            if fresh_edu and (not edu_data or len(edu_data) < len(fresh_edu) or has_corrupted):
                edu_data = normalize_education_items(fresh_edu)
                portfolio.education = json.dumps(edu_data)
                if db:
                    try:
                        db.commit()
                    except Exception:
                        try:
                            db.rollback()
                        except Exception:
                            pass

    if isinstance(edu_data, list) and json.dumps(edu_data) != json.dumps(raw_edu):
        portfolio.education = json.dumps(edu_data)
        if db:
            try:
                db.commit()
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass

    # Strict Guarantee: Accurately synchronize project details and links with candidate resume
    raw_proj = safe_json_load(portfolio.projects, [])
    proj_data = raw_proj if isinstance(raw_proj, list) else []

    if cand and cand.resume_text:
        from app.nlp.skill_extractor import parse_projects_items, extract_section_text, _PROJECTS_HEADING_RE
        proj_sec = extract_section_text(cand.resume_text, _PROJECTS_HEADING_RE)
        if proj_sec:
            cand_skills_list = []
            if isinstance(skills_data, dict):
                for sk_group in skills_data.values():
                    if isinstance(sk_group, list):
                        cand_skills_list.extend(sk_group)
            elif isinstance(skills_data, list):
                cand_skills_list = skills_data

            fresh_projects = parse_projects_items(
                proj_sec,
                candidate_github=cand.github_url or (soc_data.get("github") if isinstance(soc_data, dict) else None),
                skills=cand_skills_list
            )
            if fresh_projects:
                if not proj_data:
                    proj_data = fresh_projects
                    portfolio.projects = json.dumps(proj_data)
                else:
                    # Enrich existing project records with live_demo_url and github_url if missing
                    updated_proj = False
                    for i, p in enumerate(proj_data):
                        # Match by index or title
                        match_fp = None
                        p_name = (p.get("name") or p.get("title") or "").strip().lower()
                        for fp in fresh_projects:
                            fp_name = (fp.get("name") or fp.get("title") or "").strip().lower()
                            if p_name and fp_name and (p_name in fp_name or fp_name in p_name):
                                match_fp = fp
                                break
                        if not match_fp and i < len(fresh_projects):
                            match_fp = fresh_projects[i]

                        if match_fp:
                            if not p.get("live_demo_url") and match_fp.get("live_demo_url"):
                                p["live_demo_url"] = match_fp["live_demo_url"]
                                updated_proj = True
                            if not p.get("github_url") and match_fp.get("github_url"):
                                p["github_url"] = match_fp["github_url"]
                                updated_proj = True

                    if updated_proj:
                        portfolio.projects = json.dumps(proj_data)

                if db:
                    try:
                        db.commit()
                    except Exception:
                        try:
                            db.rollback()
                        except Exception:
                            pass

    # Strict Guarantee: Use the email address mentioned in candidate's resume
    resume_email = None
    if cand and cand.resume_text:
        resume_email = extract_email(cand.resume_text)

    if resume_email:
        current_soc_email = (soc_data.get("email") or "").strip()
        # If social_links email is missing or was set to user account email instead of resume email:
        if not current_soc_email or (cand_user and current_soc_email.lower() == cand_user.email.lower() and resume_email.lower() != cand_user.email.lower()):
            soc_data["email"] = resume_email
            portfolio.social_links = json.dumps(soc_data)

    cand_email = resume_email or (cand_user.email if (cand_user and not public_only) else None)

    # Automatically assign and persist domain background image if not yet set (None)
    effective_bg = portfolio.background_image
    if effective_bg is None:
        effective_bg = determine_candidate_domain_background(cand, {"skills": skills_data}, "", portfolio.theme_id or "modern")
        portfolio.background_image = effective_bg
        if db:
            try:
                db.commit()
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
    elif effective_bg == "none":
        effective_bg = ""

    order_data = safe_json_load(portfolio.section_order, DEFAULT_SECTION_ORDER)
    vis_data = safe_json_load(portfolio.section_visibility, DEFAULT_SECTION_VISIBILITY)
    headline_options = safe_json_load(portfolio.headline_options, [])

    custom_css_val = portfolio.custom_css
    portrait_mask_val = None
    if custom_css_val:
        if custom_css_val.startswith("{") and "portrait_mask" in custom_css_val:
            try:
                css_json = json.loads(custom_css_val)
                portrait_mask_val = css_json.get("portrait_mask")
            except Exception:
                pass
        elif custom_css_val.startswith("mask-"):
            portrait_mask_val = custom_css_val

    # If public view, strip private contacts if needed
    if public_only:
        return {
            "candidate_name": cand_name,
            "professional_headline": portfolio.professional_headline,
            "about": portfolio.about,
            "skills": skills_data,
            "experience": exp_data,
            "education": edu_data,
            "projects": proj_data,
            "certifications": cert_data,
            "achievements": ach_data,
            "services": srv_data,
            "social_links": soc_data,
            "profile_image": portfolio.profile_image or (cand.profile_photo if cand else None),
            "background_image": effective_bg,
            "theme_id": portfolio.theme_id,
            "primary_color": portfolio.primary_color,
            "secondary_color": portfolio.secondary_color,
            "font": portfolio.font,
            "background_style": portfolio.background_style,
            "dark_mode": portfolio.dark_mode,
            "button_style": portfolio.button_style,
            "card_style": portfolio.card_style,
            "layout": portfolio.layout,
            "custom_css": custom_css_val,
            "portrait_mask": portrait_mask_val,
            "section_order": order_data,
            "section_visibility": vis_data,
            "slug": portfolio.slug,
            "is_published": portfolio.is_published,
            "views_count": portfolio.views_count,
            "updated_at": portfolio.updated_at,
        }

    return {
        "id": portfolio.id,
        "candidate_id": portfolio.candidate_id,
        "candidate_name": cand_name,
        "candidate_email": cand_email,
        "slug": portfolio.slug,
        "is_published": portfolio.is_published,
        "views_count": portfolio.views_count,
        "theme_id": portfolio.theme_id,
        "primary_color": portfolio.primary_color,
        "secondary_color": portfolio.secondary_color,
        "font": portfolio.font,
        "background_style": portfolio.background_style,
        "dark_mode": portfolio.dark_mode,
        "button_style": portfolio.button_style,
        "card_style": portfolio.card_style,
        "layout": portfolio.layout,
        "custom_css": custom_css_val,
        "portrait_mask": portrait_mask_val,
        "profile_image": portfolio.profile_image or (cand.profile_photo if cand else None),
        "background_image": effective_bg,
        "professional_headline": portfolio.professional_headline,
        "headline_options": headline_options,
        "about": portfolio.about,
        "skills": skills_data,
        "experience": exp_data,
        "education": edu_data,
        "projects": proj_data,
        "certifications": cert_data,
        "achievements": ach_data,
        "services": srv_data,
        "social_links": soc_data,
        "section_order": order_data,
        "section_visibility": vis_data,
        "public_url": f"/portfolio/{portfolio.slug}",
        "created_at": portfolio.created_at,
        "updated_at": portfolio.updated_at,
    }
