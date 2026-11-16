"""
portfolio_prompt_service.py — Prompt-Driven Portfolio Generation with Gemini AI.
Transforms natural language prompts into complete, aesthetically tuned,
production-ready candidate portfolios with custom themes, content, and styling.
"""
import json
import logging
import re
from typing import Any, Dict, List, Optional

from app.ai.llm_service import generate
from app.ai.portfolio_ai_service import (
    clean_markdown_code_block,
    organize_skills_into_categories,
    generate_value_services,
    generate_impact_metrics,
)
from app.core.config import settings

logger = logging.getLogger("ai_recruiter.portfolio_prompt")


# Curated Theme & Style mapping suggestions based on prompt keywords
THEME_PRESETS_BY_KEYWORD = {
    # Hand-Crafted & Bespoke Designer Layout Archetypes (Artisanal, High-Aesthetic Studio Quality)
    "handcrafted": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "hand-crafted": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "hand crafted": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "experienced web designer": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "experienced designer": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "web designer": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "manually designed": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "not a template": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "not like a template": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "unique layout": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "unique design": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "unique modern creative": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "visually appealing": {"theme_id": "handcrafted", "layout": "handcrafted", "font": "Plus Jakarta Sans", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "creative studio": {"theme_id": "creative_editorial_art", "layout": "creative", "font": "Outfit", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "creative neo-studio": {"theme_id": "creative_editorial_art", "layout": "creative", "font": "Outfit", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "neo-studio": {"theme_id": "creative_editorial_art", "layout": "creative", "font": "Outfit", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": True, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "creative": {"theme_id": "creative_editorial_art", "layout": "creative", "font": "Outfit", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": False, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "split screen": {"theme_id": "saas_prism", "layout": "split_screen", "font": "Plus Jakarta Sans", "primary_color": "#f43f5e", "secondary_color": "#7c3aed", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "split-screen": {"theme_id": "saas_prism", "layout": "split_screen", "font": "Plus Jakarta Sans", "primary_color": "#f43f5e", "secondary_color": "#7c3aed", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "split": {"theme_id": "saas_prism", "layout": "split_screen", "font": "Plus Jakarta Sans", "primary_color": "#f43f5e", "secondary_color": "#7c3aed", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},

    # Modern & Clean SaaS Bento Archetypes
    "bento": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#10b981", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "modern bento": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#10b981", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "linear": {"theme_id": "linear_noir", "layout": "modern", "font": "Inter", "primary_color": "#5e6ad2", "secondary_color": "#a5b4fc", "dark_mode": True, "bg": "dots", "mask": "mask-studio-bento"},
    "stripe": {"theme_id": "saas_stripe", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#635bff", "secondary_color": "#00d4ff", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "clean": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "neat": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "well-organized": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "well organized": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "polished": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "modern": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},
    "professional": {"theme_id": "modern", "layout": "modern", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-studio-bento"},

    # Specialized Archetypes
    "developer workstation": {"theme_id": "developer", "layout": "developer", "font": "Fira Code", "primary_color": "#10b981", "secondary_color": "#06b6d4", "dark_mode": True, "bg": "grid", "mask": "mask-studio-bento"},
    "terminal ide": {"theme_id": "terminal", "layout": "developer", "font": "Fira Code", "primary_color": "#22c55e", "secondary_color": "#38bdf8", "dark_mode": True, "bg": "grid", "mask": "mask-studio-bento"},
    "developer": {"theme_id": "developer", "layout": "developer", "font": "Fira Code", "primary_color": "#10b981", "secondary_color": "#06b6d4", "dark_mode": True, "bg": "grid", "mask": "mask-studio-bento"},
    "terminal": {"theme_id": "terminal", "layout": "developer", "font": "Fira Code", "primary_color": "#22c55e", "secondary_color": "#38bdf8", "dark_mode": True, "bg": "grid", "mask": "mask-studio-bento"},
    "hacker": {"theme_id": "developer", "layout": "developer", "font": "Fira Code", "primary_color": "#10b981", "secondary_color": "#06b6d4", "dark_mode": True, "bg": "grid", "mask": "mask-studio-bento"},
    "cyberpunk": {"theme_id": "cyberpunk", "layout": "ai_tech", "font": "Fira Code", "primary_color": "#06b6d4", "secondary_color": "#ec4899", "dark_mode": True, "bg": "dots", "mask": "mask-corner-curve"},
    "neural hud": {"theme_id": "ai_tech", "layout": "ai_tech", "font": "Plus Jakarta Sans", "primary_color": "#00E5FF", "secondary_color": "#6366f1", "dark_mode": True, "bg": "mesh", "mask": "mask-corner-curve"},
    "ai tech": {"theme_id": "ai_tech", "layout": "ai_tech", "font": "Plus Jakarta Sans", "primary_color": "#00E5FF", "secondary_color": "#6366f1", "dark_mode": True, "bg": "mesh", "mask": "mask-corner-curve"},
    "neural": {"theme_id": "ai_tech", "layout": "ai_tech", "font": "Plus Jakarta Sans", "primary_color": "#00E5FF", "secondary_color": "#6366f1", "dark_mode": True, "bg": "mesh", "mask": "mask-corner-curve"},
    "ai": {"theme_id": "ai_tech", "layout": "ai_tech", "font": "Plus Jakarta Sans", "primary_color": "#00E5FF", "secondary_color": "#6366f1", "dark_mode": True, "bg": "mesh", "mask": "mask-corner-curve"},
    "swiss": {"theme_id": "zurich_grid", "layout": "minimal", "font": "Inter", "primary_color": "#0f172a", "secondary_color": "#e11d48", "dark_mode": False, "bg": "clean", "mask": "mask-arch"},
    "minimalist": {"theme_id": "minimal", "layout": "minimal", "font": "Inter", "primary_color": "#18181b", "secondary_color": "#71717a", "dark_mode": False, "bg": "clean", "mask": "mask-arch"},
    "minimal": {"theme_id": "minimal", "layout": "minimal", "font": "Inter", "primary_color": "#18181b", "secondary_color": "#71717a", "dark_mode": False, "bg": "clean", "mask": "mask-arch"},
    "creative studio": {"theme_id": "creative", "layout": "creative", "font": "Outfit", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": False, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "split screen": {"theme_id": "split_screen", "layout": "split_screen", "font": "Outfit", "primary_color": "#4f46e5", "secondary_color": "#f43f5e", "dark_mode": False, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "split": {"theme_id": "split_screen", "layout": "split_screen", "font": "Outfit", "primary_color": "#4f46e5", "secondary_color": "#f43f5e", "dark_mode": False, "bg": "mesh", "mask": "mask-asymmetric-pill"},
    "corporate": {"theme_id": "corporate", "layout": "corporate", "font": "Plus Jakarta Sans", "primary_color": "#2563EB", "secondary_color": "#0f172a", "dark_mode": False, "bg": "clean", "mask": "mask-arch"},
    "executive": {"theme_id": "executive_briefing", "layout": "corporate", "font": "Plus Jakarta Sans", "primary_color": "#2563EB", "secondary_color": "#d97706", "dark_mode": False, "bg": "clean", "mask": "mask-arch"},
    "briefing": {"theme_id": "corporate", "layout": "corporate", "font": "Plus Jakarta Sans", "primary_color": "#2563EB", "secondary_color": "#0f172a", "dark_mode": False, "bg": "clean", "mask": "mask-arch"},
    "dark luxury": {"theme_id": "dark", "layout": "dark", "font": "Inter", "primary_color": "#818cf8", "secondary_color": "#38bdf8", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "dark": {"theme_id": "dark", "layout": "dark", "font": "Inter", "primary_color": "#818cf8", "secondary_color": "#38bdf8", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "oled": {"theme_id": "dark", "layout": "dark", "font": "Inter", "primary_color": "#818cf8", "secondary_color": "#38bdf8", "dark_mode": True, "bg": "mesh", "mask": "mask-studio-bento"},
    "notion": {"theme_id": "notion", "layout": "notion", "font": "Inter", "primary_color": "#27272a", "secondary_color": "#64748b", "dark_mode": False, "bg": "clean", "mask": "mask-pebble"},
    "timeline": {"theme_id": "timeline", "layout": "timeline", "font": "Plus Jakarta Sans", "primary_color": "#4f46e5", "secondary_color": "#06b6d4", "dark_mode": False, "bg": "mesh", "mask": "mask-pebble"},
    "dashboard": {"theme_id": "dashboard", "layout": "dashboard", "font": "Plus Jakarta Sans", "primary_color": "#0284c7", "secondary_color": "#10b981", "dark_mode": True, "bg": "grid", "mask": "mask-studio-bento"},
    "nova": {"theme_id": "editorial", "layout": "nova", "font": "Plus Jakarta Sans", "primary_color": "#0D9488", "secondary_color": "#BA855E", "dark_mode": False, "bg": "mesh", "mask": "mask-pebble"},
    "editorial": {"theme_id": "editorial", "layout": "nova", "font": "Plus Jakarta Sans", "primary_color": "#0D9488", "secondary_color": "#BA855E", "dark_mode": False, "bg": "mesh", "mask": "mask-pebble"},
    "agency": {"theme_id": "editorial", "layout": "nova", "font": "Plus Jakarta Sans", "primary_color": "#0D9488", "secondary_color": "#BA855E", "dark_mode": False, "bg": "mesh", "mask": "mask-pebble"},
    "creative": {"theme_id": "creative", "layout": "creative", "font": "Outfit", "primary_color": "#F97316", "secondary_color": "#8b5cf6", "dark_mode": False, "bg": "mesh", "mask": "mask-asymmetric-pill"},
}


def _extract_json_from_llm_response(text: str) -> Optional[dict]:
    """Robustly extracts JSON from an LLM response string with multi-stage sanitization."""
    if not text:
        return None

    cleaned = clean_markdown_code_block(text).strip()

    # 1. Direct parse
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # 2. Outermost boundary extraction
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        candidate = cleaned[start_idx : end_idx + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

        # 3. Clean trailing commas
        try:
            fixed = re.sub(r",\s*([\]}])", r"\1", candidate)
            return json.loads(fixed)
        except Exception:
            pass

        # 4. Clean unescaped control chars
        try:
            fixed_ctrl = re.sub(r'[\x00-\x1f\x7f-\x9f]', lambda m: ' ' if m.group(0) in '\n\r\t' else '', candidate)
            fixed_ctrl = re.sub(r",\s*([\]}])", r"\1", fixed_ctrl)
            return json.loads(fixed_ctrl)
        except Exception:
            pass

    # 5. Regex rescue for truncated responses
    if start_idx != -1:
        partial = cleaned[start_idx:]
        open_braces = partial.count("{") - partial.count("}")
        open_brackets = partial.count("[") - partial.count("]")
        closed_partial = partial + ("]" * max(0, open_brackets)) + ("}" * max(0, open_braces))
        try:
            fixed_closed = re.sub(r",\s*([\]}])", r"\1", closed_partial)
            return json.loads(fixed_closed)
        except Exception:
            pass

    return None


def analyze_resume_with_gemini(
    candidate_name: str,
    candidate_context: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    MODEL 1: Resume Analysis Specialist.
    Analyzes candidate's raw resume text, career history, verified projects,
    and academic credentials using GEMINI_RESUME_MODEL.
    Extracts deep, structured, authentic career facts without hallucinations.
    """
    model_name = getattr(settings, "GEMINI_RESUME_MODEL", "gemini-3-flash-preview")
    logger.info("[Model 1: Resume Analysis (%s)] Analyzing authentic candidate credentials for '%s'...", model_name, candidate_name)

    ctx_parts = [f"Candidate Name: {candidate_name}"]
    if candidate_context:
        if candidate_context.get("headline"):
            ctx_parts.append(f"Authentic Headline: {candidate_context['headline']}")
        if candidate_context.get("summary"):
            ctx_parts.append(f"Authentic Career Summary: {candidate_context['summary'][:800]}")
        if candidate_context.get("skills"):
            s_list = candidate_context["skills"]
            if isinstance(s_list, list):
                ctx_parts.append(f"Verified Skills: {', '.join(str(s) for s in s_list[:40])}")
            elif isinstance(s_list, dict):
                ctx_parts.append(f"Verified Skills: {json.dumps(s_list)}")
        if candidate_context.get("experience"):
            ctx_parts.append(f"AUTHENTIC WORK HISTORY (MUST PRESERVE REAL COMPANIES & TITLES): {json.dumps(candidate_context['experience'][:6])}")
        if candidate_context.get("projects"):
            ctx_parts.append(f"AUTHENTIC PROJECTS: {json.dumps(candidate_context['projects'][:6])}")
        if candidate_context.get("education"):
            ctx_parts.append(f"AUTHENTIC ACADEMIC DEGREES: {json.dumps(candidate_context['education'][:4])}")
        if candidate_context.get("resume_text"):
            ctx_parts.append(f"RAW RESUME TEXT EXTRACT:\n{candidate_context['resume_text'][:3000]}")

    context_prompt = "\n".join(ctx_parts)

    system_instruction_resume = (
        "You are an Elite Technical Resume Intelligence Analyst.\n"
        "Your objective is to deeply analyze the candidate's authentic resume and career history to extract verified facts.\n"
        "CRITICAL FACTUAL INTEGRITY RULES:\n"
        "1. Preserve 100% of authentic employer/company names, genuine job titles, authentic degrees, and educational institutions.\n"
        "2. NEVER invent fake companies or fictional jobs.\n"
        "3. Group skills into 3-4 clean competencies.\n"
        "4. Extract real projects from the resume with their actual technologies and deliverables.\n"
        "5. Extract or calculate 4 high-impact, quantified metrics from their real accomplishments.\n"
        "6. Formulate 3 core value proposition services/pillars representing the candidate's professional offering.\n"
        "7. For every project, extract all authentic project links, live demo URLs (e.g. .app, .vercel.app, .netlify.app, custom domains), and GitHub repository URLs. Set 'live_demo_url' and 'github_url' accurately. NEVER invent fake URLs. If a real URL exists in the resume, you MUST preserve it.\n"
        "8. Output ONLY a valid JSON object. No markdown fencings, no other text.\n\n"
        "JSON SCHEMA:\n"
        "{\n"
        '  "candidate_name": "string",\n'
        '  "domain": "string (e.g. AI / Machine Learning, Full Stack Engineering, Cloud Architecture, Data Science, Talent Operations)",\n'
        '  "career_persona": "string (e.g. Senior Machine Learning Engineer | Intelligent Systems Developer)",\n'
        '  "headline": "string",\n'
        '  "about_summary": "string",\n'
        '  "skills": {"Category Name": ["Skill1", "Skill2"]},\n'
        '  "experience": [{"title": "string", "company": "string", "location": "string", "start_date": "string", "end_date": "string", "is_current": boolean, "description": "string", "highlights": ["string"], "technologies": ["string"]}],\n'
        '  "projects": [{"name": "string", "description": "string", "key_features": ["string"], "technologies": ["string"], "live_demo_url": "string", "github_url": "string"}],\n'
        '  "education": [{"degree": "string", "institution": "string", "end_year": "string", "grade": "string"}],\n'
        '  "impact_metrics": [{"value": "string", "label": "string", "icon": "string"}],\n'
        '  "services": [{"title": "string", "description": "string", "icon": "string"}],\n'
        '  "social_links": {"email": "string", "location": "string", "github": "string", "linkedin": "string"}\n'
        "}"
    )

    raw_response = generate(
        system_prompt=system_instruction_resume,
        user_prompt=context_prompt,
        max_tokens=3000,
        model=model_name,
    )
    parsed = _extract_json_from_llm_response(raw_response) if raw_response else None

    if parsed and isinstance(parsed, dict) and (parsed.get("skills") or parsed.get("experience") or parsed.get("career_persona")):
        logger.info("[Model 1: Resume Analysis (%s)] Successfully extracted structured career intelligence!", model_name)
        return parsed

    logger.warning("[Model 1: Resume Analysis (%s)] Gemini call did not return complete JSON, applying deterministic resume extraction fallback.", model_name)
    # Deterministic resume fallback
    fallback_skills = candidate_context.get("skills", []) if candidate_context else []
    if isinstance(fallback_skills, list):
        skills_dict = organize_skills_into_categories(fallback_skills)
    elif isinstance(fallback_skills, dict):
        skills_dict = fallback_skills
    else:
        skills_dict = {"Core Technologies": ["Software Development", "System Architecture"]}

    fallback_role = candidate_context.get("headline", "Software Engineer") if candidate_context else "Software Engineer"
    exp_years = float(candidate_context.get("experience_years", 0.0)) if candidate_context and candidate_context.get("experience_years") else 0.0
    projs = candidate_context.get("projects", []) if candidate_context else []
    flat_skills = fallback_skills if isinstance(fallback_skills, list) else list(skills_dict.values())
    flat_skills_list = [str(s) for sub in (flat_skills if any(isinstance(i, list) for i in flat_skills) else [flat_skills]) for s in (sub if isinstance(sub, list) else [sub])]

    derived_metrics = generate_impact_metrics(
        role=fallback_role,
        skills=flat_skills_list,
        experience_years=exp_years,
        project_count=len(projs),
        verified_metrics=candidate_context.get("metrics_and_impact") if candidate_context else None,
    )
    derived_services = generate_value_services(
        role=fallback_role,
        skills=flat_skills_list,
        experience_years=exp_years,
    )

    return {
        "candidate_name": candidate_name,
        "domain": candidate_context.get("headline", "Technology") if candidate_context else "Technology",
        "career_persona": candidate_context.get("headline", f"{candidate_name} — Professional Portfolio") if candidate_context else "Software Engineer",
        "headline": fallback_role,
        "about_summary": candidate_context.get("summary", "") if candidate_context else "",
        "skills": skills_dict,
        "experience": candidate_context.get("experience", []) if candidate_context else [],
        "projects": projs,
        "education": candidate_context.get("education", []) if candidate_context else [],
        "impact_metrics": derived_metrics,
        "services": derived_services,
        "social_links": {
            "email": candidate_context.get("email", "") if candidate_context else "",
            "location": candidate_context.get("location", "") if candidate_context else "",
            "github": candidate_context.get("github_url", "") if candidate_context else "",
            "linkedin": candidate_context.get("linkedin_url", "") if candidate_context else "",
        }
    }


def analyze_prompt_with_gemini(
    prompt: str,
    candidate_context: Optional[Dict[str, Any]] = None,
    previous_portfolio: Optional[Dict[str, Any]] = None,
    is_refinement: bool = False,
) -> Dict[str, Any]:
    """
    MODEL 2: Prompt & Design Intent Specialist.
    Analyzes the user's natural language creation prompt using GEMINI_PROMPT_MODEL.
    Extracts layout architecture, theme archetype, color palette, background image,
    portrait mask shape, font, card style, button style, and dark mode.
    """
    model_name = getattr(settings, "GEMINI_PROMPT_MODEL", "gemini-3.5-flash-lite")
    logger.info("[Model 2: Prompt Analysis (%s)] Analyzing user prompt & design directives: '%s'...", model_name, prompt[:80])

    system_instruction_prompt = (
        "You are a Creative UI/UX Design Director and Prompt Intent Specialist.\n"
        "Your objective is to analyze the user's natural language creation prompt and extract their exact visual, architectural, and styling design preferences.\n"
        "STYLING EXTRACTION RULES:\n"
        "1. Layout Architecture: Choose the exact matching archetype:\n"
        "   - 'handcrafted': if hand-crafted, handcrafted, experienced web designer, bespoke, manually designed, not a typical template, unique modern creative layout, award-winning artisan studio\n"
        "   - 'modern': if modern website, professional, bento, clean, responsive, modular, high-impact, SaaS cards\n"
        "   - 'developer': if terminal, IDE, code, matrix, hacker, CLI, engineer\n"
        "   - 'ai_tech': if AI, machine learning, neural, HUD, cyberpunk, futuristic, cyber\n"
        "   - 'minimal': if minimal, swiss, monochrome, simple, clean, hairline\n"
        "   - 'corporate': if executive, corporate, leadership, 2-column, management\n"
        "   - 'creative': only if explicitly requesting creative studio, pop art, vibrant illustrator showcase\n"
        "   - 'dark': if dark luxury, obsidian, neon, carbon\n"
        "   - 'split_screen': if split, two panels, side by side\n"
        "   - 'nova': default editorial agency magazine layout\n"
        "2. Colors: Extract primary and secondary hex colors based on user prompt (e.g. #10b981 for emerald, #06b6d4 for cyan, #8b5cf6 for violet, #F97316 for orange, #4f46e5 for indigo).\n"
        "3. Background Image: Extract whether user requested a custom image URL, a specific domain backdrop, or 'none' for clean solid background.\n"
        "4. Portrait Mask: Choose mask shape: 'mask-pebble' | 'mask-arch' | 'mask-corner-curve' | 'mask-studio-bento' | 'mask-asymmetric-pill'.\n"
        "5. Card Style: 'glass' | 'flat' | 'elevated' | 'bordered'.\n"
        "6. Button Style: 'rounded' | 'pill' | 'sharp' | 'glow'.\n"
        "7. Dark Mode: boolean true/false.\n"
        "8. Typography: 'Plus Jakarta Sans' | 'Inter' | 'Outfit' | 'Fira Code' | 'Playfair Display' | 'Poppins'.\n"
        "9. Ambient Pattern: 'mesh' | 'clean' | 'dots' | 'grid'.\n"
        "10. Output ONLY a valid JSON object matching the schema below. No markdown fencings, no other text.\n\n"
        "JSON SCHEMA:\n"
        "{\n"
        '  "layout": "handcrafted" | "developer" | "modern" | "ai_tech" | "minimal" | "corporate" | "creative" | "dark" | "split_screen" | "nova",\n'
        '  "theme_id": "string",\n'
        '  "primary_color": "#hex",\n'
        '  "secondary_color": "#hex",\n'
        '  "font": "string",\n'
        '  "background_style": "mesh" | "clean" | "dots" | "grid",\n'
        '  "background_image": "URL string or \'none\'",\n'
        '  "portrait_mask": "mask-pebble" | "mask-arch" | "mask-corner-curve" | "mask-studio-bento" | "mask-asymmetric-pill",\n'
        '  "card_style": "glass" | "flat" | "elevated" | "bordered",\n'
        '  "button_style": "rounded" | "pill" | "sharp" | "glow",\n'
        '  "dark_mode": boolean,\n'
        '  "tone": "string (e.g. authoritative, technical, executive, creative, ambitious)",\n'
        '  "creative_directives": ["string"],\n'
        '  "suggested_slug": "string"\n'
        "}"
    )

    user_prompt_text = f"User Creation Prompt: {prompt}\n"
    if is_refinement and previous_portfolio:
        user_prompt_text += f"Previous Portfolio Design: {json.dumps({'layout': previous_portfolio.get('layout'), 'theme_id': previous_portfolio.get('theme_id'), 'primary_color': previous_portfolio.get('primary_color'), 'dark_mode': previous_portfolio.get('dark_mode')})}\n"

    raw_response = generate(
        system_prompt=system_instruction_prompt,
        user_prompt=user_prompt_text,
        max_tokens=1500,
        model=model_name,
    )
    parsed = _extract_json_from_llm_response(raw_response) if raw_response else None

    if parsed and isinstance(parsed, dict) and ("layout" in parsed or "primary_color" in parsed or "theme_id" in parsed):
        logger.info("[Model 2: Prompt Analysis (%s)] Successfully extracted design directives: layout=%s, theme=%s, primary=%s",
                    model_name, parsed.get("layout"), parsed.get("theme_id"), parsed.get("primary_color"))
        return parsed

    logger.warning("[Model 2: Prompt Analysis (%s)] Gemini call did not return complete JSON, applying deterministic design extraction fallback.", model_name)
    # Deterministic prompt extraction fallback using keywords
    lower_p = prompt.lower()
    matched_preset = None
    for kw, preset in THEME_PRESETS_BY_KEYWORD.items():
        if kw in lower_p:
            matched_preset = preset
            break
    if not matched_preset:
        matched_preset = THEME_PRESETS_BY_KEYWORD["modern"]

    # Colors
    hex_matches = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", prompt)
    primary = hex_matches[0] if hex_matches else matched_preset["primary_color"]
    secondary = hex_matches[1] if len(hex_matches) > 1 else matched_preset["secondary_color"]

    # Dark mode
    dark_mode = True if any(k in lower_p for k in ("dark", "terminal", "cyberpunk", "hacker", "night", "oled", "carbon")) else (False if any(k in lower_p for k in ("light", "white", "clean", "nordic", "swiss")) else matched_preset.get("dark_mode", False))

    # Background image
    url_m = re.search(r"https?://[^\s'\"\)]+", prompt)
    bg_image = url_m.group(0) if url_m else ""

    return {
        "layout": matched_preset.get("layout", "modern"),
        "theme_id": matched_preset.get("theme_id", "modern"),
        "primary_color": primary,
        "secondary_color": secondary,
        "font": matched_preset.get("font", "Plus Jakarta Sans"),
        "background_style": matched_preset.get("bg", "mesh"),
        "background_image": bg_image or "none",
        "portrait_mask": matched_preset.get("mask", "mask-pebble"),
        "card_style": "glass",
        "button_style": "rounded",
        "dark_mode": dark_mode,
        "tone": "authoritative and modern",
        "creative_directives": [prompt],
        "suggested_slug": "",
    }


def synthesize_portfolio_with_gemini(
    candidate_name: str,
    prompt: str,
    resume_intelligence: Dict[str, Any],
    design_directive: Dict[str, Any],
    is_refinement: bool = False,
    previous_portfolio: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    MODEL 3: Portfolio Generation & Synthesis Architect.
    Combines the verified career intelligence from Model 1 and the custom design
    directives from Model 2 using GEMINI_PORTFOLIO_MODEL to produce the complete,
    award-winning portfolio website JSON.
    """
    model_name = getattr(settings, "GEMINI_PORTFOLIO_MODEL", "gemini-flash-lite-latest")
    logger.info("[Model 3: Portfolio Synthesis (%s)] Synthesizing bespoke portfolio specification...", model_name)

    system_instruction_synth = (
        "You are the Master Portfolio Synthesizer & Web Architect.\n"
        "You receive two authoritative specifications:\n"
        "1. RESUME INTELLIGENCE (produced by Model 1): Verified career facts, genuine employers, real projects, categorized skills, degrees, and impact metrics.\n"
        "2. DESIGN DIRECTIVE (produced by Model 2): The user's layout archetype, theme, colors, background image, portrait mask, typography, card style, button style, and dark mode.\n\n"
        "YOUR MISSION:\n"
        "Synthesize both inputs into a complete, award-winning candidate portfolio JSON website.\n"
        "1. Strictly apply the layout, theme, colors, background image, portrait mask, font, card style, button style, and dark mode from the DESIGN DIRECTIVE.\n"
        "2. Strictly preserve 100% of authentic companies, roles, genuine projects, real degrees, and facts from the RESUME INTELLIGENCE. NEVER fabricate fake employers.\n"
        "3. Strictly preserve all verified project URLs ('live_demo_url' and 'github_url') from the resume intelligence so visitors can launch live project websites in a new tab.\n"
        "4. Craft compelling executive headline options and an engaging 2-3 paragraph About narrative that embodies the tone from the DESIGN DIRECTIVE.\n"
        "5. BESPOKE HAND-CRAFTED QUALITY: The generated content must feel and read like a custom website manually designed by an experienced principal web designer and software engineer (Awwwards / Linear / Stripe caliber), never like a generic template. Descriptions must emphasize real engineering decisions, system performance, and measurable user impact.\n"
        "6. Output ONLY a valid JSON object matching the full portfolio schema. No markdown fencings, no other text.\n\n"
        "JSON SCHEMA:\n"
        "{\n"
        '  "full_name": "string",\n'
        '  "professional_headline": "string",\n'
        '  "headline_options": ["string", "string", "string"],\n'
        '  "about": "string",\n'
        '  "domain": "string",\n'
        '  "layout": "string",\n'
        '  "theme_id": "string",\n'
        '  "primary_color": "#hex",\n'
        '  "secondary_color": "#hex",\n'
        '  "font": "string",\n'
        '  "background_style": "string",\n'
        '  "background_image": "string",\n'
        '  "portrait_mask": "string",\n'
        '  "card_style": "string",\n'
        '  "button_style": "string",\n'
        '  "dark_mode": boolean,\n'
        '  "impact_metrics": [{"value": "string", "label": "string", "icon": "string"}],\n'
        '  "skills": {"Category Name": ["Skill1", "Skill2"]},\n'
        '  "services": [{"title": "string", "description": "string", "icon": "string"}],\n'
        '  "projects": [{"name": "string", "description": "string", "key_features": ["string"], "technologies": ["string"], "live_demo_url": "string", "github_url": "string"}],\n'
        '  "experience": [{"title": "string", "company": "string", "location": "string", "start_date": "string", "end_date": "string", "is_current": boolean, "description": "string", "highlights": ["string"], "technologies": ["string"]}],\n'
        '  "education": [{"degree": "string", "institution": "string", "end_year": "string", "grade": "string"}],\n'
        '  "certifications": [{"name": "string", "organization": "string", "year": "string"}],\n'
        '  "social_links": {"email": "string", "location": "string", "github": "string", "linkedin": "string"},\n'
        '  "suggested_slug": "string"\n'
        "}"
    )

    synthesis_payload = (
        f"Candidate Name: {candidate_name}\n"
        f"User Prompt Instruction: {prompt}\n\n"
        f"=== INPUT 1: VERIFIED RESUME INTELLIGENCE (Model 1) ===\n"
        f"{json.dumps(resume_intelligence, indent=2)}\n\n"
        f"=== INPUT 2: DESIGN & UI/UX DIRECTIVE (Model 2) ===\n"
        f"{json.dumps(design_directive, indent=2)}\n\n"
        "Synthesize both into the complete, production-ready portfolio JSON now."
    )

    raw_response = generate(
        system_prompt=system_instruction_synth,
        user_prompt=synthesis_payload,
        max_tokens=4000,
        model=model_name,
    )
    parsed = _extract_json_from_llm_response(raw_response) if raw_response else None

    if parsed and isinstance(parsed, dict) and "professional_headline" in parsed:
        logger.info("[Model 3: Portfolio Synthesis (%s)] Successfully generated unified portfolio JSON!", model_name)
        parsed["layout"] = parsed.get("layout") or design_directive.get("layout", "modern")
        parsed["theme_id"] = parsed.get("theme_id") or design_directive.get("theme_id", "modern")
        parsed["primary_color"] = parsed.get("primary_color") or design_directive.get("primary_color", "#4f46e5")
        parsed["secondary_color"] = parsed.get("secondary_color") or design_directive.get("secondary_color", "#06b6d4")
        parsed["font"] = parsed.get("font") or design_directive.get("font", "Plus Jakarta Sans")
        parsed["background_style"] = parsed.get("background_style") or design_directive.get("background_style", "mesh")
        if "background_image" in design_directive and design_directive["background_image"] is not None:
            parsed["background_image"] = design_directive["background_image"]
        if "portrait_mask" in design_directive and design_directive["portrait_mask"]:
            parsed["portrait_mask"] = design_directive["portrait_mask"]
        parsed["card_style"] = parsed.get("card_style") or design_directive.get("card_style", "glass")
        parsed["button_style"] = parsed.get("button_style") or design_directive.get("button_style", "rounded")
        if "dark_mode" in design_directive:
            parsed["dark_mode"] = design_directive["dark_mode"]
        return parsed

    logger.warning("[Model 3: Portfolio Synthesis (%s)] Synthesis call incomplete, performing direct synthesis merger.", model_name)
    # Direct synthesis merger fallback
    full_name = resume_intelligence.get("candidate_name") or candidate_name
    headline = resume_intelligence.get("headline") or resume_intelligence.get("career_persona") or f"{full_name} — Professional Portfolio"
    about = resume_intelligence.get("about_summary") or (
        f"Hi, I'm {full_name}. I design and engineer high-scale digital platforms, with a focus on engineering excellence, intuitive user experiences, and measurable organizational impact."
    )

    merged = {
        "full_name": full_name,
        "professional_headline": headline,
        "headline_options": [
            headline,
            f"{headline} | High-Impact Solutions",
            f"Strategic Technologist | {resume_intelligence.get('domain', 'Engineering')}",
        ],
        "about": about,
        "domain": resume_intelligence.get("domain", "Technology"),
        "layout": design_directive.get("layout", "modern"),
        "theme_id": design_directive.get("theme_id", "modern"),
        "primary_color": design_directive.get("primary_color", "#4f46e5"),
        "secondary_color": design_directive.get("secondary_color", "#06b6d4"),
        "font": design_directive.get("font", "Plus Jakarta Sans"),
        "background_style": design_directive.get("background_style", "mesh"),
        "background_image": design_directive.get("background_image", "none"),
        "portrait_mask": design_directive.get("portrait_mask", "mask-pebble"),
        "card_style": design_directive.get("card_style", "glass"),
        "button_style": design_directive.get("button_style", "rounded"),
        "dark_mode": design_directive.get("dark_mode", False),
        "profile_image": resume_intelligence.get("profile_image") or (previous_portfolio.get("profile_image") if previous_portfolio else None),
        "impact_metrics": resume_intelligence.get("impact_metrics", []),
        "skills": resume_intelligence.get("skills", {}),
        "services": resume_intelligence.get("services", []),
        "projects": resume_intelligence.get("projects", []),
        "experience": resume_intelligence.get("experience", []),
        "education": resume_intelligence.get("education", []),
        "certifications": resume_intelligence.get("certifications", []),
        "social_links": resume_intelligence.get("social_links", {}),
        "suggested_slug": design_directive.get("suggested_slug") or re.sub(r"[^a-z0-9]+", "-", f"{full_name}-{resume_intelligence.get('domain', 'portfolio')}".lower()).strip("-"),
    }
    return merged


def generate_single_prompt_portfolio_with_gemini(
    prompt: str,
    candidate_name: str = "Candidate",
    candidate_context: Optional[Dict[str, Any]] = None,
    previous_portfolio: Optional[Dict[str, Any]] = None,
    is_refinement: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    SINGLE-PROMPT MASTER GEMINI ENGINE:
    Takes the user's natural language creation prompt as the PRIMARY creative driver.
    Gemini deeply analyzes the prompt requirements (role, aesthetic, tone, colors, layout archetype,
    card style, button style, background, and features) and synthesizes a unique, bespoke modern
    portfolio specification in one unified master LLM pass.
    Strictly grounds factual employment and education credentials from candidate_context (Rule 21).
    """
    model_name = getattr(settings, "GEMINI_MODEL", "gemini-3-flash-preview")
    logger.info("[Single-Prompt Gemini Master Engine (%s)] Analyzing user prompt & synthesizing portfolio: '%s'...", model_name, prompt[:100])

    # Build factual candidate context grounding
    ctx_parts = []
    if candidate_context:
        if candidate_context.get("name"):
            ctx_parts.append(f"Candidate Real Name: {candidate_context['name']}")
        if candidate_context.get("headline"):
            ctx_parts.append(f"Current Headline / Role: {candidate_context['headline']}")
        if candidate_context.get("skills"):
            ctx_parts.append(f"Verified Candidate Skills: {json.dumps(candidate_context['skills'])}")
        if candidate_context.get("experience"):
            ctx_parts.append(f"AUTHENTIC WORK EXPERIENCE (Keep real employer names & titles): {json.dumps(candidate_context['experience'][:6])}")
        if candidate_context.get("projects"):
            ctx_parts.append(f"AUTHENTIC PROJECTS & REPOSITORIES (Keep real deliverables & URLs): {json.dumps(candidate_context['projects'][:6])}")
        if candidate_context.get("education"):
            ctx_parts.append(f"AUTHENTIC EDUCATION (Keep real degrees & universities): {json.dumps(candidate_context['education'][:4])}")
        if candidate_context.get("certifications"):
            ctx_parts.append(f"CERTIFICATIONS: {json.dumps(candidate_context['certifications'][:4])}")
        if candidate_context.get("resume_text"):
            ctx_parts.append(f"RESUME EXCERPT: {candidate_context['resume_text'][:2000]}")

    resume_grounding_str = "\n".join(ctx_parts) if ctx_parts else f"Candidate Name: {candidate_name}"

    system_instruction = (
        "You are Gemini AI, the world's most elite AI Portfolio Architect and Principal Creative Director.\n"
        "Your mission is to deeply analyze the user's natural language creation prompt and synthesize a stunning, modern, bespoke portfolio website specification.\n\n"
        "=== HAND-CRAFTED DESIGNER EXCELLENCE & BESPOKE QUALITY ===\n"
        "1. Every portfolio generated MUST feel and look like a professionally hand-crafted website, as if manually designed and developed by an experienced principal web designer (Awwwards / Linear / Stripe caliber).\n"
        "2. STRICTLY AVOID generic, cookie-cutter AI templates. Each portfolio MUST have a unique, modern, creative, and visually appealing layout tailored to the candidate's engineering persona.\n"
        "3. DO NOT default every portfolio to 'modern' with indigo/cyan! Choose the archetype and palette that best expresses the candidate's authentic persona:\n"
        "    * 'creative': for creative technologists, frontend engineers, UI/UX designers, or when requested 'handcrafted', 'web designer', 'creative layout', 'unique layout'. Pair with warm sunset terracotta (#f97316) / amethyst (#8b5cf6) or duotone rose (#f43f5e) / violet (#7c3aed), Outfit font, and asymmetric pill masks.\n"
        "    * 'split_screen': 50/50 dual-panel layout with sticky hero on left and scrolling case studies on right. Ideal for full-stack product engineers. Pair with vivid accents like rose (#f43f5e) / purple (#7c3aed) or indigo / cyan.\n"
        "    * 'developer': terminal/IDE code window, dark matrix carbon aesthetic, monospace Fira Code, live git commit telemetry. Ideal for backend, systems, and DevOps engineers.\n"
        "    * 'ai_tech': cyberpunk neural HUD, glowing neon cyan (#00e5ff) and hyper-violet (#a855f7) accents, futuristic data telemetry.\n"
        "    * 'dark': dark luxury obsidian titanium, deep OLED black with subtle ultraviolet/sky micro-borders.\n"
        "    * 'minimal': Swiss typographic monograph with high contrast, monochrome and vivid vermilion (#e11d48) accent.\n"
        "    * 'corporate': executive two-column briefing, enterprise prestige in deep navy (#0f172a) and champagne gold (#f59e0b).\n"
        "    * 'modern': high-impact SaaS bento grid with kinetic glass cards.\n"
        "    * 'nova': boutique editorial agency magazine aesthetic with warm sand and teal accents.\n"
        "- Visual Mood & Colors: extract exact hex colors matching prompt or role mood. Ensure strong visual identity.\n"
        "- Typography: Plus Jakarta Sans | Inter | Outfit | Fira Code | Poppins\n"
        "- Card & Button Styling: card_style: 'glass' | 'flat' | 'elevated' | 'bordered'; button_style: 'rounded' | 'pill' | 'sharp' | 'glow'\n"
        "- Portrait Mask: 'mask-studio-bento' | 'mask-arch' | 'mask-corner-curve' | 'mask-pebble' | 'mask-asymmetric-pill'\n"
        "- Background Style: 'mesh' | 'grid' | 'dots' | 'clean'\n"
        "- Dark Mode: boolean true/false based on prompt intent\n"
        "- Narrative Tone & About Section: craft an authentic, human-authored 2-3 paragraph professional story that emphasizes real engineering decisions, architectural trade-offs, and measurable outcomes. BAN generic buzzwords ('passionate problem solver', 'leveraging synergies').\n"
        "- 4 High-Impact Quantified Metrics: derived from authentic accomplishments with concrete units (e.g. '99.99% Uptime', '14M+ Daily Events', '45ms P99 Latency', '12k+ GitHub Stars').\n"
        "- 3 Core Value Proposition Services / Pillars: demonstrating technical offering\n\n"
        "=== FACTUAL GROUNDING RULES (Rule 21) ===\n"
        "1. Strictly preserve all authentic employer names, genuine job titles, genuine university degrees, and genuine projects from the candidate context.\n"
        "2. NEVER invent fake companies or fictitious academic credentials.\n"
        "3. Preserve all real project URLs (live demos, GitHub links) without fabricating fictional links.\n"
        "4. Seamlessly blend the user's prompt desires with the candidate's authentic career history.\n\n"
        "OUTPUT REQUIREMENT: Return ONLY a valid JSON object matching the exact schema below. No markdown backticks, no markdown code block, no preamble.\n\n"
        "JSON SCHEMA:\n"
        "{\n"
        '  "full_name": "string",\n'
        '  "professional_headline": "string (e.g. Senior Full Stack Engineer & Cloud Architect)",\n'
        '  "headline_options": ["Option 1", "Option 2", "Option 3"],\n'
        '  "about": "string (2-3 paragraphs of compelling, prompt-aligned professional narrative)",\n'
        '  "domain": "string",\n'
        '  "layout": "modern" | "developer" | "ai_tech" | "minimal" | "corporate" | "creative" | "dark" | "split_screen" | "nova",\n'
        '  "theme_id": "string",\n'
        '  "primary_color": "#hex",\n'
        '  "secondary_color": "#hex",\n'
        '  "font": "string",\n'
        '  "background_style": "mesh" | "grid" | "dots" | "clean",\n'
        '  "background_image": "URL string or \'none\'",\n'
        '  "portrait_mask": "mask-studio-bento" | "mask-arch" | "mask-corner-curve" | "mask-pebble" | "mask-asymmetric-pill",\n'
        '  "card_style": "glass" | "flat" | "elevated" | "bordered",\n'
        '  "button_style": "rounded" | "pill" | "sharp" | "glow",\n'
        '  "dark_mode": boolean,\n'
        '  "impact_metrics": [{"value": "string", "label": "string", "icon": "string"}],\n'
        '  "skills": {"Category Name": ["Skill1", "Skill2", "Skill3"]},\n'
        '  "services": [{"title": "string", "description": "string", "icon": "string"}],\n'
        '  "projects": [{"name": "string", "description": "string", "key_features": ["string"], "technologies": ["string"], "live_demo_url": "string", "github_url": "string"}],\n'
        '  "experience": [{"title": "string", "company": "string", "location": "string", "start_date": "string", "end_date": "string", "is_current": boolean, "description": "string", "highlights": ["string"], "technologies": ["string"]}],\n'
        '  "education": [{"degree": "string", "institution": "string", "end_year": "string", "grade": "string"}],\n'
        '  "certifications": [{"name": "string", "organization": "string", "year": "string"}],\n'
        '  "social_links": {"email": "string", "location": "string", "github": "string", "linkedin": "string"},\n'
        '  "suggested_slug": "string"\n'
        "}"
    )

    user_prompt_content = (
        f"=== USER CREATION PROMPT (PRIMARY DIRECTIVE) ===\n"
        f"{prompt}\n\n"
        f"=== CANDIDATE FACTUAL BACKGROUND (GROUNDING CONTEXT) ===\n"
        f"{resume_grounding_str}\n"
    )
    if is_refinement and previous_portfolio:
        user_prompt_content += (
            f"\n=== PREVIOUS PORTFOLIO STATE ===\n"
            f"Layout: {previous_portfolio.get('layout')}, Theme: {previous_portfolio.get('theme_id')}, "
            f"Headline: {previous_portfolio.get('professional_headline')}, Colors: {previous_portfolio.get('primary_color')}\n"
        )

    raw_response = generate(
        system_prompt=system_instruction,
        user_prompt=user_prompt_content,
        max_tokens=4000,
        model=model_name,
    )

    parsed = _extract_json_from_llm_response(raw_response) if raw_response else None
    if parsed and isinstance(parsed, dict) and parsed.get("professional_headline"):
        logger.info("[Single-Prompt Gemini Master Engine (%s)] Generation succeeded! Layout=%s, Theme=%s, Primary=%s",
                    model_name, parsed.get("layout"), parsed.get("theme_id"), parsed.get("primary_color"))
        return parsed

    logger.warning("[Single-Prompt Gemini Master Engine (%s)] LLM output did not yield complete portfolio JSON.", model_name)
    return None


def generate_portfolio_from_prompt(
    prompt: str,
    candidate_name: str = "Candidate",
    candidate_context: Optional[Dict[str, Any]] = None,
    previous_portfolio: Optional[Dict[str, Any]] = None,
    is_refinement: bool = False,
) -> Dict[str, Any]:
    """
    Main entry point: Generates a complete portfolio specification driven by the user's creation prompt.
    1. Single-Prompt Master Pass: Gemini AI directly analyzes user prompt requirements and synthesizes
       a bespoke modern portfolio with factual candidate grounding.
    2. Multi-Model Fallback: If single pass requires enrichment, invokes the 3-stage pipeline.
    3. Deterministic Safety Fallback: Always guarantees production-ready result with zero downtime.
    """
    prompt = (prompt or "").strip()
    if not prompt:
        prompt = "Create a modern, professional website with a unique design and layout. Visually attractive, creative, impressive, with a clean and responsive user interface."

    # Stage 1: Single-Prompt Master Gemini Generation (Primary Engine)
    single_prompt_result = generate_single_prompt_portfolio_with_gemini(
        prompt=prompt,
        candidate_name=candidate_name,
        candidate_context=candidate_context,
        previous_portfolio=previous_portfolio,
        is_refinement=is_refinement,
    )
    if single_prompt_result and isinstance(single_prompt_result, dict) and single_prompt_result.get("professional_headline"):
        logger.info("Single-Prompt Gemini Portfolio Generation completed successfully!")
        return _normalize_generated_portfolio(
            single_prompt_result,
            candidate_name,
            prompt,
            candidate_context=candidate_context,
            previous_portfolio=previous_portfolio,
        )

    # Stage 2: 3-Stage Pipeline Fallback
    logger.info("Invoking 3-model Gemini pipeline fallback...")
    resume_intel = analyze_resume_with_gemini(candidate_name, candidate_context)
    design_dir = analyze_prompt_with_gemini(prompt, candidate_context, previous_portfolio, is_refinement)
    final_portfolio = synthesize_portfolio_with_gemini(
        candidate_name=candidate_name,
        prompt=prompt,
        resume_intelligence=resume_intel,
        design_directive=design_dir,
        is_refinement=is_refinement,
        previous_portfolio=previous_portfolio,
    )

    if final_portfolio and isinstance(final_portfolio, dict) and "professional_headline" in final_portfolio:
        logger.info("3-Model Gemini Portfolio Generation Pipeline completed successfully!")
        return _normalize_generated_portfolio(
            final_portfolio,
            candidate_name,
            prompt,
            candidate_context=candidate_context,
            previous_portfolio=previous_portfolio,
        )

    logger.warning("Synthesis stage incomplete, merging Model 1 & Model 2 via deterministic synthesis fallback.")
    return _generate_deterministic_portfolio(prompt, candidate_name, candidate_context, previous_portfolio)


def _normalize_generated_portfolio(
    data: Dict[str, Any],
    candidate_name: str,
    prompt: str,
    candidate_context: Optional[Dict[str, Any]] = None,
    previous_portfolio: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Ensures all expected keys and structured formats conform to Portfolio standards."""
    full_name = data.get("full_name") or candidate_name or "Candidate"
    headline = data.get("professional_headline") or "Senior Software Engineer"
    headline_options = data.get("headline_options") or [
        headline,
        f"{headline} | Scalable Systems & Architecture",
        f"Principal Innovator | {data.get('domain', 'Technology')}",
    ]

    about = data.get("about") or (
        f"Hi, I'm {full_name}. I am a results-oriented technology professional specializing in building high-scale, reliable digital products."
    )

    theme_id = data.get("theme_id") or "modern"
    layout = data.get("layout") or "modern"
    theme_id = data.get("theme_id")
    if not theme_id or (theme_id == "modern" and layout != "modern"):
        layout_to_theme = {
            "creative": "saas_craft",
            "split_screen": "saas_prism",
            "developer": "tech_matrix",
            "ai_tech": "ai_tech",
            "dark": "dark_obsidian",
            "minimal": "swiss_zurich",
            "corporate": "exec_enterprise_cto",
            "nova": "editorial",
            "timeline": "timeline_journey",
            "dashboard": "dashboard",
        }
        theme_id = layout_to_theme.get(layout, "modern")

    primary_color = data.get("primary_color") or "#4f46e5"
    secondary_color = data.get("secondary_color") or "#06b6d4"
    font = data.get("font") or "Plus Jakarta Sans"
    dark_mode = bool(data.get("dark_mode", False))

    # Metrics — strictly from authentic candidate resume data, NEVER inject fake numbers
    raw_metrics = data.get("impact_metrics") or []
    impact_metrics = []
    if isinstance(raw_metrics, list):
        for m in raw_metrics:
            if isinstance(m, dict) and m.get("value") and m.get("label"):
                impact_metrics.append({
                    "value": str(m["value"]),
                    "label": str(m["label"]),
                    "icon": m.get("icon") or "⚡",
                })
    if not impact_metrics and candidate_context:
        try:
            cand_role = candidate_context.get("headline") or candidate_context.get("professional_headline") or "Software Engineer"
            cand_skills = candidate_context.get("skills") or []
            flat_sk = []
            if isinstance(cand_skills, dict):
                for sub in cand_skills.values():
                    flat_sk.extend(sub if isinstance(sub, list) else [sub])
            elif isinstance(cand_skills, list):
                flat_sk = cand_skills
            exp_yrs = float(candidate_context.get("experience_years", 0.0)) if candidate_context.get("experience_years") else 0.0
            cand_projs = candidate_context.get("projects") or []
            impact_metrics = generate_impact_metrics(
                role=cand_role,
                skills=flat_sk,
                experience_years=exp_yrs,
                project_count=len(cand_projs) if isinstance(cand_projs, list) else 0,
                verified_metrics=candidate_context.get("metrics_and_impact"),
            )
        except Exception:
            impact_metrics = []

    # Skills
    raw_skills = data.get("skills") or {}
    skills_dict = {}
    if isinstance(raw_skills, dict):
        for cat, items in raw_skills.items():
            if isinstance(items, list):
                skills_dict[cat] = [str(i).strip() for i in items if i]
    elif isinstance(raw_skills, list):
        skills_dict = organize_skills_into_categories([str(i).strip() for i in raw_skills if i])

    # Leave skills empty if not present in resume — do NOT fabricate skills

    # Projects
    raw_projects = data.get("projects") or []
    projects = []
    if isinstance(raw_projects, list):
        for p in raw_projects:
            if isinstance(p, dict) and (p.get("name") or p.get("title")):
                name = p.get("name") or p.get("title") or "Engineering Project"
                desc = p.get("description") or "Engineered scalable architecture with modern best practices."
                feats = p.get("key_features") or p.get("highlights") or []
                if isinstance(feats, str):
                    feats = [feats]
                techs = p.get("technologies") or []
                if isinstance(techs, str):
                    techs = [t.strip() for t in techs.split(",") if t.strip()]
                projects.append({
                    "name": name,
                    "description": desc,
                    "key_features": feats,
                    "technologies": techs,
                    "live_demo_url": p.get("live_demo_url") or "",
                    "github_url": p.get("github_url") or "",
                })

    # Work Experience
    raw_exp = data.get("experience") or []
    experience = []
    if isinstance(raw_exp, list):
        for e in raw_exp:
            if isinstance(e, dict) and (e.get("title") or e.get("company")):
                highlights = e.get("highlights") or []
                if isinstance(highlights, str):
                    highlights = [highlights]
                techs = e.get("technologies") or []
                if isinstance(techs, str):
                    techs = [t.strip() for t in techs.split(",") if t.strip()]
                experience.append({
                    "title": e.get("title") or "",
                    "company": e.get("company") or "",
                    "location": e.get("location") or "Remote",
                    "start_date": str(e.get("start_date") or "2022"),
                    "end_date": str(e.get("end_date") or "Present"),
                    "is_current": bool(e.get("is_current", True)),
                    "description": e.get("description") or "",
                    "highlights": highlights,
                    "technologies": techs,
                })

    # Services / Value proposition — strictly from resume, NEVER inject fake services
    raw_serv = data.get("services") or []
    services = []
    if isinstance(raw_serv, list):
        for s in raw_serv:
            if isinstance(s, dict) and s.get("title"):
                services.append({
                    "title": s["title"],
                    "description": s.get("description") or "",
                    "icon": s.get("icon") or "💡",
                })
    if not services and candidate_context:
        try:
            cand_role = candidate_context.get("headline") or candidate_context.get("professional_headline") or "Software Engineer"
            cand_skills = candidate_context.get("skills") or []
            flat_sk = []
            if isinstance(cand_skills, dict):
                for sub in cand_skills.values():
                    flat_sk.extend(sub if isinstance(sub, list) else [sub])
            elif isinstance(cand_skills, list):
                flat_sk = cand_skills
            exp_yrs = float(candidate_context.get("experience_years", 0.0)) if candidate_context.get("experience_years") else 0.0
            services = generate_value_services(
                role=cand_role,
                skills=flat_sk,
                experience_years=exp_yrs,
            )
        except Exception:
            services = []

    # Education — strictly from resume, NEVER inject fake universities
    raw_edu = data.get("education") or []
    education = []
    if isinstance(raw_edu, list):
        for ed in raw_edu:
            if isinstance(ed, dict) and (ed.get("degree") or ed.get("institution")):
                education.append(ed)

    # Certifications
    certifications = data.get("certifications") or []

    # Social links
    social_links = data.get("social_links") or {}
    if not isinstance(social_links, dict):
        social_links = {}

    # Portrait mask & background image
    portrait_mask = data.get("portrait_mask") or "mask-pebble"
    custom_css = data.get("custom_css") or json.dumps({"portrait_mask": portrait_mask})
    bg_img = data.get("background_image")
    if bg_img is None:
        from app.services.portfolio_service import DOMAIN_BACKGROUND_PRESETS
        t = theme_id.lower()
        if "ai" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["ai_tech"]["url"]
        elif "dev" in t or "terminal" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["developer"]["url"]
        elif "creative" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["creative"]["url"]
        elif "corp" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["corporate"]["url"]
        elif "data" in t or "analytics" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["data_analytics"]["url"]
        elif "recruiter" in t or "hr" in t or "talent" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["hr_recruiting"]["url"]
        elif "minimal" in t or "swiss" in t:
            bg_img = DOMAIN_BACKGROUND_PRESETS["minimal"]["url"]
        else:
            bg_img = DOMAIN_BACKGROUND_PRESETS["developer"]["url"]

    # Slug
    slug = data.get("suggested_slug") or re.sub(r"[^a-z0-9\-]+", "-", full_name.lower().replace(" ", "-")).strip("-")
    if not slug:
        slug = "candidate-portfolio"

    return {
        "full_name": full_name,
        "profile_image": data.get("profile_image") or (candidate_context.get("profile_image") if candidate_context else None) or (previous_portfolio.get("profile_image") if previous_portfolio else None),
        "professional_headline": headline,
        "headline_options": headline_options,
        "about": about,
        "domain": data.get("domain") or "Engineering",
        "theme_id": theme_id,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "font": font,
        "background_style": data.get("background_style") or "mesh",
        "background_image": bg_img,
        "portrait_mask": portrait_mask,
        "custom_css": custom_css,
        "card_style": data.get("card_style") or "glass",
        "button_style": data.get("button_style") or "rounded",
        "dark_mode": dark_mode,
        "layout": layout,
        "impact_metrics": impact_metrics,
        "skills": skills_dict,
        "services": services,
        "projects": projects,
        "experience": experience,
        "education": education,
        "certifications": certifications,
        "social_links": social_links,
        "suggested_slug": slug,
        "generation_prompt": prompt,
    }


def _generate_deterministic_portfolio(
    prompt: str,
    candidate_name: str,
    candidate_context: Optional[Dict[str, Any]],
    previous_portfolio: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Fallback engine: Analyzes prompt keywords to deterministically construct
    a complete, highly stylized portfolio matching user preferences for layout,
    theme, colors, background images, and UI/UX design.
    """
    from app.services.portfolio_service import DOMAIN_BACKGROUND_PRESETS

    p_lower = prompt.lower()

    # Detect style intent from keywords
    matched_preset = None
    for kw, preset in THEME_PRESETS_BY_KEYWORD.items():
        if kw in p_lower:
            matched_preset = preset
            break
    if not matched_preset:
        matched_preset = THEME_PRESETS_BY_KEYWORD["modern"]

    # 1. Specialized layout archetypes (Checked first to prevent generic "clean"/"modern" over-matching)
    if any(k in p_lower for k in ["split screen", "split-screen", "split", "dual panel", "two panel", "two-column hero"]):
        layout = "split_screen"
    elif any(k in p_lower for k in ["terminal", "ide", "hacker", "developer workstation", "cli", "code aesthetic", "monospace", "github"]):
        layout = "developer"
    elif any(k in p_lower for k in ["neural hud", "ai tech", "cyber telemetry", "futuristic", "hud", "telemetry", "cyberpunk", "holographic"]):
        layout = "ai_tech"
    elif any(k in p_lower for k in ["creative studio", "neo-display", "neo-studio", "pop art", "avant-garde", "creative", "artistic", "terracotta"]):
        layout = "creative"
    elif any(k in p_lower for k in ["swiss", "minimalist", "minimal monograph", "monograph", "bauhaus", "hairline"]):
        layout = "minimal"
    elif any(k in p_lower for k in ["corporate", "briefing", "2-column", "executive briefing", "dossier", "leadership", "boardroom"]):
        layout = "corporate"
    elif any(k in p_lower for k in ["dark luxury", "oled", "midnight", "obsidian", "carbon"]):
        layout = "dark"
    elif any(k in p_lower for k in ["nova", "editorial", "boutique", "magazine"]):
        layout = "nova"
    elif any(k in p_lower for k in ["timeline", "journey", "chronicle"]):
        layout = "timeline"
    elif any(k in p_lower for k in ["dashboard", "cockpit", "analytics lab"]):
        layout = "dashboard"
    elif any(k in p_lower for k in [
        "handcrafted", "hand-crafted", "hand crafted", "experienced web designer", "experienced designer",
        "web designer", "not a template", "not like a template", "unique, modern, creative", "unique layout",
        "creative and visually appealing", "manually designed"
    ]):
        # Dynamic hand-crafted layout assignment based on candidate context
        cand_text = f"{candidate_name} {candidate_context.get('headline', '') if candidate_context else ''} {candidate_context.get('skills', '') if candidate_context else ''}".lower()
        if any(w in cand_text for w in ["front", "design", "ui", "ux", "creative", "web", "react"]):
            layout = "creative"
        elif any(w in cand_text for w in ["ai", "machine learning", "data", "deep learning"]):
            layout = "ai_tech"
        elif any(w in cand_text for w in ["back", "system", "devops", "cloud", "python", "golang", "java"]):
            layout = "developer"
        elif any(w in cand_text for w in ["lead", "manager", "product", "director", "exec"]):
            layout = "corporate"
        else:
            cand_seed = abs(hash(f"{candidate_name}_{prompt}"))
            layout = ["creative", "split_screen", "dark", "modern", "nova"][cand_seed % 5]
    elif any(k in p_lower for k in ["bento", "modular", "apple", "linear", "modern bento"]):
        layout = "modern"
    else:
        layout = matched_preset.get("layout", "modern")

    # 2. Color detection
    hex_matches = re.findall(r"#[0-9a-fA-F]{6}", prompt)
    if len(hex_matches) >= 2:
        primary_color = hex_matches[0]
        secondary_color = hex_matches[1]
    elif len(hex_matches) == 1:
        primary_color = hex_matches[0]
        secondary_color = matched_preset["secondary_color"]
    else:
        if "cyan" in p_lower or "neon cyan" in p_lower:
            primary_color = "#00E5FF"
            secondary_color = "#6366f1"
        elif "emerald" in p_lower or "green" in p_lower:
            primary_color = "#10b981"
            secondary_color = "#06b6d4"
        elif "violet" in p_lower or "purple" in p_lower:
            primary_color = "#7c3aed"
            secondary_color = "#f43f5e"
        elif "indigo" in p_lower:
            primary_color = "#4f46e5"
            secondary_color = "#06b6d4"
        elif "amber" in p_lower or "gold" in p_lower:
            primary_color = "#d97706"
            secondary_color = "#1e3a8a"
        elif "orange" in p_lower or "terracotta" in p_lower:
            primary_color = "#F97316"
            secondary_color = "#8b5cf6"
        elif "teal" in p_lower:
            primary_color = "#0D9488"
            secondary_color = "#BA855E"
        elif "monochrome" in p_lower or "black" in p_lower:
            primary_color = "#18181b"
            secondary_color = "#71717a"
        else:
            primary_color = matched_preset["primary_color"]
            secondary_color = matched_preset["secondary_color"]

    # 3. Dark mode detection
    dark_mode = matched_preset["dark_mode"]
    if any(k in p_lower for k in ["dark mode", "oled", "midnight", "night", "dark theme"]):
        dark_mode = True
    elif any(k in p_lower for k in ["light mode", "clean white", "bright", "light theme"]):
        dark_mode = False

    # 4. Background styling & image detection
    url_match = re.search(r"https?://\S+\.(?:jpg|jpeg|png|webp)\S*", prompt, re.IGNORECASE) or re.search(r"https?://images\.unsplash\.com/\S+", prompt)
    if url_match:
        bg_image = url_match.group(0).rstrip(").,")
    elif any(k in p_lower for k in ["no background image", "clean background", "solid background", "no image"]):
        bg_image = ""
    elif any(k in p_lower for k in ["ai", "neural", "computing", "llm"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["ai_tech"]["url"]
    elif any(k in p_lower for k in ["developer", "code", "programming", "software"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["developer"]["url"]
    elif any(k in p_lower for k in ["cloud", "devops", "kubernetes", "aws"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["cloud_devops"]["url"]
    elif any(k in p_lower for k in ["design", "ui/ux", "product design"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["creative"]["url"]
    elif any(k in p_lower for k in ["corporate", "executive", "boardroom", "management"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["corporate"]["url"]
    elif any(k in p_lower for k in ["data", "analytics", "telemetry", "bi"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["data_analytics"]["url"]
    elif any(k in p_lower for k in ["recruiter", "talent", "hr", "people"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["hr_recruiting"]["url"]
    elif any(k in p_lower for k in ["minimal", "desk", "clean"]):
        bg_image = DOMAIN_BACKGROUND_PRESETS["minimal"]["url"]
    else:
        bg_image = DOMAIN_BACKGROUND_PRESETS["developer"]["url"]

    # 5. Portrait mask shape detection
    if any(k in p_lower for k in ["arch", "architectural"]):
        portrait_mask = "mask-arch"
    elif any(k in p_lower for k in ["corner", "cyber", "cyber corner"]):
        portrait_mask = "mask-corner-curve"
    elif any(k in p_lower for k in ["bento", "box", "rectangle", "studio bento"]):
        portrait_mask = "mask-studio-bento"
    elif any(k in p_lower for k in ["pill", "asymmetric"]):
        portrait_mask = "mask-asymmetric-pill"
    else:
        portrait_mask = matched_preset.get("mask", "mask-pebble")

    # Role & Domain detection
    if "recruiter" in p_lower or "talent" in p_lower or "hr" in p_lower or "people" in p_lower:
        role = "Senior Corporate Recruiter & Talent Strategist"
        domain = "Talent Acquisition & People Operations"
        skills = {
            "Talent Sourcing & Strategy": ["Full-Cycle Recruitment", "Executive Search", "Technical Hiring", "Candidate Pipeline"],
            "ATS & Operations": ["Greenhouse", "Lever", "Workday", "LinkedIn Recruiter", "Gem"],
            "HR Leadership": ["Workforce Planning", "Offer Negotiation", "DEI Strategy", "Onboarding"],
        }
    elif "ai" in p_lower or "machine learning" in p_lower:
        role = "Senior AI & Machine Learning Engineer"
        domain = "Artificial Intelligence"
        skills = {
            "AI & Modeling": ["PyTorch", "TensorFlow", "HuggingFace", "LangChain", "OpenAI API"],
            "Engineering & Cloud": ["Python", "FastAPI", "Docker", "Kubernetes", "AWS"],
            "Data & MLOps": ["PostgreSQL", "MLflow", "Vector DBs", "Redis"],
        }
    elif "frontend" in p_lower or "react" in p_lower or "design" in p_lower:
        role = "Lead Frontend & UI/UX Engineer"
        domain = "Frontend & Product Engineering"
        skills = {
            "Frontend Core": ["React", "Next.js", "TypeScript", "Tailwind CSS", "HTML5/CSS3"],
            "State & Tools": ["Redux Toolkit", "Zustand", "Vite", "Jest", "Storybook"],
            "Design & Workflow": ["Figma", "UI Architecture", "Accessibility (a11y)", "Design Systems"],
        }
    elif "cloud" in p_lower or "devops" in p_lower or "infrastructure" in p_lower:
        role = "Principal Cloud & DevOps Architect"
        domain = "Cloud Infrastructure & SRE"
        skills = {
            "Cloud Platforms": ["AWS", "Google Cloud", "Azure", "Terraform"],
            "Containers & Orchestration": ["Kubernetes", "Docker", "Helm", "Istio"],
            "CI/CD & Observability": ["GitHub Actions", "Prometheus", "Grafana", "Datadog"],
        }
    elif "data" in p_lower or "analytics" in p_lower:
        role = "Staff Data Engineer & Analytics Specialist"
        domain = "Data Systems & Telemetry"
        skills = {
            "Data Engineering": ["Apache Spark", "Airflow", "Kafka", "dbt", "Snowflake"],
            "Languages & Storage": ["Python", "SQL", "Scala", "PostgreSQL", "BigQuery"],
            "Analytics & BI": ["Tableau", "Data Modeling", "ETL Pipelines", "Telemetry"],
        }
    else:
        role = "Senior Full Stack Systems Engineer"
        domain = "Full Stack Engineering"
        skills = {
            "Languages": ["Python", "TypeScript", "JavaScript", "Go", "SQL"],
            "Frameworks": ["FastAPI", "React", "Node.js", "Next.js"],
            "Infrastructure & Databases": ["Docker", "PostgreSQL", "Redis", "AWS", "CI/CD"],
        }

    # CRITICAL: Preserve authentic candidate resume facts (employers, projects, education)
    # Strictly zero fabrication — if not in resume, leave empty list
    projects = []
    experience = []
    education = []
    achievements = []
    services = []
    certifications = []
    contact_email = ""
    contact_linkedin = ""
    contact_github = ""
    contact_location = ""

    if candidate_context:
        if candidate_context.get("headline"):
            role = candidate_context["headline"]
        if candidate_context.get("skills"):
            if isinstance(candidate_context["skills"], list):
                skills = organize_skills_into_categories(candidate_context["skills"])
            elif isinstance(candidate_context["skills"], dict):
                skills = candidate_context["skills"]
        if candidate_context.get("experience"):
            experience = candidate_context["experience"]
        if candidate_context.get("projects"):
            projects = candidate_context["projects"]
        if candidate_context.get("education"):
            education = candidate_context["education"]
        if candidate_context.get("metrics"):
            achievements = candidate_context["metrics"]
        if candidate_context.get("services"):
            services = candidate_context["services"]
        if candidate_context.get("certifications"):
            certifications = candidate_context["certifications"]

        contact_email = (candidate_context.get("email") or (candidate_context.get("social_links") or {}).get("email") or "").strip()
        contact_linkedin = (candidate_context.get("linkedin") or (candidate_context.get("social_links") or {}).get("linkedin") or "").strip()
        contact_github = (candidate_context.get("github") or (candidate_context.get("social_links") or {}).get("github") or "").strip()
        contact_location = (candidate_context.get("location") or (candidate_context.get("social_links") or {}).get("location") or "").strip()
    else:
        # No resume provided: leave career sections completely blank for candidate to edit
        role = ""
        skills = {}

    # Align theme_id and design tokens with chosen layout archetype
    layout_theme_defaults = {
        "creative": {"theme_id": "saas_craft", "font": "Outfit", "button_style": "pill", "card_style": "glass", "mask": "mask-asymmetric-pill"},
        "split_screen": {"theme_id": "saas_prism", "font": "Plus Jakarta Sans", "button_style": "rounded", "card_style": "glass", "mask": "mask-studio-bento"},
        "developer": {"theme_id": "tech_matrix", "font": "Fira Code", "button_style": "sharp", "card_style": "bordered", "mask": "mask-studio-bento"},
        "ai_tech": {"theme_id": "ai_tech", "font": "Plus Jakarta Sans", "button_style": "glow", "card_style": "glass", "mask": "mask-corner-curve"},
        "dark": {"theme_id": "dark_obsidian", "font": "Inter", "button_style": "rounded", "card_style": "glass", "mask": "mask-studio-bento"},
        "minimal": {"theme_id": "swiss_zurich", "font": "Inter", "button_style": "rounded", "card_style": "flat", "mask": "mask-arch"},
        "corporate": {"theme_id": "exec_enterprise_cto", "font": "Plus Jakarta Sans", "button_style": "sharp", "card_style": "elevated", "mask": "mask-arch"},
        "nova": {"theme_id": "editorial", "font": "Plus Jakarta Sans", "button_style": "rounded", "card_style": "glass", "mask": "mask-pebble"},
        "timeline": {"theme_id": "timeline_journey", "font": "Plus Jakarta Sans", "button_style": "rounded", "card_style": "glass", "mask": "mask-pebble"},
        "dashboard": {"theme_id": "dashboard", "font": "Plus Jakarta Sans", "button_style": "rounded", "card_style": "bordered", "mask": "mask-studio-bento"},
        "modern": {"theme_id": matched_preset.get("theme_id", "modern"), "font": matched_preset.get("font", "Plus Jakarta Sans"), "button_style": "rounded", "card_style": "glass", "mask": "mask-studio-bento"},
    }
    cur_layout_config = layout_theme_defaults.get(layout, layout_theme_defaults["modern"])
    chosen_theme_id = cur_layout_config["theme_id"]
    chosen_font = cur_layout_config["font"]
    chosen_btn_style = cur_layout_config["button_style"]
    chosen_card_style = cur_layout_config["card_style"]
    if portrait_mask == "mask-pebble":
        portrait_mask = cur_layout_config["mask"]

    # Auto generate metrics & services from candidate context if missing
    if not achievements and candidate_context:
        try:
            cand_role = candidate_context.get("headline") or candidate_context.get("professional_headline") or role or "Software Engineer"
            cand_skills = candidate_context.get("skills") or []
            flat_sk = []
            if isinstance(cand_skills, dict):
                for sub in cand_skills.values():
                    flat_sk.extend(sub if isinstance(sub, list) else [sub])
            elif isinstance(cand_skills, list):
                flat_sk = cand_skills
            exp_yrs = float(candidate_context.get("experience_years", 0.0)) if candidate_context.get("experience_years") else 0.0
            cand_projs = candidate_context.get("projects") or projects or []
            achievements = generate_impact_metrics(
                role=cand_role,
                skills=flat_sk,
                experience_years=exp_yrs,
                project_count=len(cand_projs) if isinstance(cand_projs, list) else 0,
                verified_metrics=candidate_context.get("metrics_and_impact"),
            )
        except Exception:
            achievements = []
    if not services and candidate_context:
        try:
            cand_role = candidate_context.get("headline") or candidate_context.get("professional_headline") or "Software Engineer"
            cand_skills = candidate_context.get("skills") or []
            flat_sk = []
            if isinstance(cand_skills, dict):
                for sub in cand_skills.values():
                    flat_sk.extend(sub if isinstance(sub, list) else [sub])
            elif isinstance(cand_skills, list):
                flat_sk = cand_skills
            exp_yrs = float(candidate_context.get("experience_years", 0.0)) if candidate_context.get("experience_years") else 0.0
            services = generate_value_services(
                role=cand_role,
                skills=flat_sk,
                experience_years=exp_yrs,
            )
        except Exception:
            services = []

    slug_base = re.sub(r"[^a-z0-9\-]+", "-", candidate_name.lower().replace(" ", "-")).strip("-") or "candidate"
    slug = f"{slug_base}-{chosen_theme_id}"

    return {
        "full_name": candidate_name,
        "profile_image": (candidate_context.get("profile_image") if candidate_context else None) or (previous_portfolio.get("profile_image") if previous_portfolio else None),
        "professional_headline": role,
        "headline_options": [
            role,
            f"{role} | High-Impact Systems & Architecture" if role else "",
            f"Senior Innovator | {domain}" if role else "",
        ] if role else [],
        "about": (
            f"Hello, I'm {candidate_name}. As a dedicated professional in {domain}, I focus on designing and executing "
            f"resilient, scalable solutions that drive measurable business outcomes. With a strong commitment to clean architecture, "
            f"seamless user experience, and continuous innovation, I thrive on solving complex engineering challenges."
        ) if role else "",
        "domain": domain,
        "theme_id": chosen_theme_id,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "font": chosen_font,
        "background_style": matched_preset["bg"],
        "background_image": bg_image,
        "portrait_mask": portrait_mask,
        "custom_css": json.dumps({"portrait_mask": portrait_mask}),
        "card_style": chosen_card_style,
        "button_style": chosen_btn_style,
        "dark_mode": dark_mode,
        "layout": layout,
        "impact_metrics": achievements if achievements else [],
        "skills": skills,
        "services": services if services else [],
        "projects": projects,
        "experience": experience,
        "education": education,
        "certifications": certifications,
        "social_links": {
            "email": contact_email,
            "linkedin": contact_linkedin,
            "github": contact_github,
            "location": contact_location,
        },
        "suggested_slug": slug,
        "generation_prompt": prompt,
    }


def refine_portfolio_section(
    section: str,
    instruction: str,
    current_data: Any,
    candidate_name: str = "Candidate",
) -> Any:
    """
    Selectively refines or rewrites a single portfolio section based on user prompt.
    """
    section = section.lower().strip()
    instruction = instruction.strip()

    system_instruction = (
        f"You are an Elite AI Portfolio Copywriter and Editor. "
        f"The candidate is refining their portfolio section: '{section}'. "
        f"Follow the user's instructions and output ONLY the updated section content in JSON format."
    )

    user_prompt = (
        f"Candidate: {candidate_name}\n"
        f"Section: {section}\n"
        f"Current Content: {json.dumps(current_data) if isinstance(current_data, (dict, list)) else str(current_data)}\n"
        f"Instruction: {instruction}\n"
        f"Return ONLY valid JSON for this section."
    )

    raw_response = generate(
        system_prompt=system_instruction,
        user_prompt=user_prompt,
        max_tokens=1500,
    )

    parsed = _extract_json_from_llm_response(raw_response) if raw_response else None
    if parsed is not None:
        return parsed

    # Simple fallback: if string section (like about or headline)
    if section in ("about", "summary") and isinstance(current_data, str):
        return f"{current_data} (Refined according to: {instruction})"
    if section == "headline" and isinstance(current_data, str):
        return f"{current_data} | {instruction.title()}"

    return current_data



def generate_portfolio_html_code_with_gemini(
    prompt: str,
    candidate_name: str = "Candidate",
    candidate_context: Optional[Dict[str, Any]] = None,
    include_placeholders: bool = True,
    existing_code: Optional[str] = None,
) -> Dict[str, Any]:
    """
    AI Code Generator: Generates bespoke production-ready HTML/CSS code from
    natural language prompts using Gemini with profile placeholder integration.
    """
    p_lower = (prompt or "").lower()
    
    # Detect layout / design archetype
    archetype = "modern_bento"
    if "terminal" in p_lower or "ide" in p_lower or "hacker" in p_lower or "cli" in p_lower or "developer" in p_lower:
        archetype = "terminal_ide"
    elif "cyber" in p_lower or "hud" in p_lower or "radar" in p_lower or "neural" in p_lower or "telemetry" in p_lower:
        archetype = "cyberpunk_hud"
    elif "swiss" in p_lower or "minimal" in p_lower or "monograph" in p_lower:
        archetype = "minimal_swiss"
    elif "executive" in p_lower or "dossier" in p_lower or "corporate" in p_lower or "leader" in p_lower:
        archetype = "executive_dossier"
    elif "creative" in p_lower or "studio" in p_lower or "asymmetric" in p_lower or "vignette" in p_lower:
        archetype = "creative_studio"

    system_instruction = (
        "You are a world-class Principal Frontend Architect and HTML/CSS/JS Engineer. "
        "Your task is to generate complete, bespoke, production-ready, beautiful HTML code "
        "with an embedded <style> block for a personal portfolio website based on the user's prompt.\n\n"
        "RULES:\n"
        "1. Output valid semantic HTML5 with an embedded <style> section containing modern CSS variables, "
        "responsive flex/grid, card hover effects, subtle glassmorphism, and elegant typography.\n"
        "2. If include_placeholders is enabled, use standard double-brace template tokens:\n"
        "   {{FULL_NAME}} - Candidate full name\n"
        "   {{HEADLINE}} - Professional headline\n"
        "   {{ABOUT}} - Bio / executive summary\n"
        "   {{PROFILE_IMAGE}} - Candidate portrait photo URL\n"
        "   {{SKILLS}} - Formatted skills tags / chips container\n"
        "   {{PROJECTS}} - Featured projects showcase cards\n"
        "   {{EXPERIENCE}} - Career experience timeline items\n"
        "   {{EDUCATION}} - Academic degrees and credentials\n"
        "   {{EMAIL}} - Contact email address\n"
        "   {{SOCIAL_LINKS}} - Social media buttons (GitHub, LinkedIn, Email)\n"
        "3. Provide rich sections: Header/Navbar, Hero with portrait & CTA, About, Skills, Projects, Experience, and Contact Footer.\n"
        "4. Return ONLY clean HTML code. Do not wrap in markdown or explanatory prose."
    )

    user_prompt = (
        f"Candidate Name: {candidate_name}\n"
        f"Desired Design & Code Directives: {prompt}\n"
        f"Detected Archetype: {archetype}\n"
        f"Include Profile Placeholders: {include_placeholders}\n"
    )
    if existing_code:
        user_prompt += f"Existing Code to Refine/Extend:\n{existing_code[:1200]}\n"

    try:
        model_name = getattr(settings, "GEMINI_SYNTHESIS_MODEL", "gemini-3-flash-preview")
        raw_response = generate(
            system_prompt=system_instruction,
            user_prompt=user_prompt,
            max_tokens=4000,
            model=model_name,
        )
        if raw_response and ("<section" in raw_response or "<div" in raw_response or "<header" in raw_response):
            cleaned_html = raw_response.strip()
            # Clean markdown code blocks if present
            if cleaned_html.startswith("```html"):
                cleaned_html = cleaned_html[7:]
            elif cleaned_html.startswith("```"):
                cleaned_html = cleaned_html[3:]
            if cleaned_html.endswith("```"):
                cleaned_html = cleaned_html[:-3]
            cleaned_html = cleaned_html.strip()
            
            return {
                "html_code": cleaned_html,
                "prompt_used": prompt,
                "detected_archetype": archetype,
            }
    except Exception as e:
        logger.warning("Gemini HTML code generation call failed: %s. Using deterministic bespoke template.", e)

    # Deterministic Bespoke Fallback Templates based on archetype
    fallback_code = _build_deterministic_archetype_code(archetype, prompt)
    return {
        "html_code": fallback_code,
        "prompt_used": prompt,
        "detected_archetype": archetype,
    }


def _build_deterministic_archetype_code(archetype: str, prompt: str) -> str:
    """
    Synthesizes rich bespoke HTML/CSS templates for each design archetype.
    """
    if archetype == "terminal_ide":
        return """<!-- Bespoke Developer Terminal IDE Portfolio Code -->
<style>
  :root {
    --term-bg: #0d1117;
    --term-card: #161b22;
    --term-border: #30363d;
    --term-green: #238636;
    --term-text: #c9d1d9;
    --term-accent: #58a6ff;
    --term-green-text: #3fb950;
  }
  .term-wrapper {
    background: var(--term-bg);
    color: var(--term-text);
    font-family: 'Fira Code', monospace, sans-serif;
    min-height: 100vh;
    padding: 2.5rem 1rem;
  }
  .term-card {
    background: var(--term-card);
    border: 1px solid var(--term-border);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .term-header {
    background: #090d12;
    border-bottom: 1px solid var(--term-border);
    padding: 10px 16px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
  }
  .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }
  .term-command { color: var(--term-green-text); }
  .term-comment { color: #8b949e; }
</style>

<div class="term-wrapper">
  <div class="container" style="max-width: 980px;">
    <!-- Terminal Window -->
    <div class="term-card mb-4">
      <div class="term-header d-flex justify-content-between align-items-center">
        <div class="d-flex gap-2">
          <span class="dot dot-red"></span>
          <span class="dot dot-yellow"></span>
          <span class="dot dot-green"></span>
        </div>
        <small class="text-secondary font-monospace">session: {{FULL_NAME}}@workstation ~ zsh</small>
        <span></span>
      </div>
      <div class="p-4 p-md-5">
        <div class="mb-4 d-flex align-items-center gap-4 flex-wrap">
          <img src="{{PROFILE_IMAGE}}" alt="{{FULL_NAME}}" class="rounded-3 border border-secondary" style="width: 100px; height: 100px; object-fit: cover;">
          <div>
            <div class="term-command fs-5 mb-1">$ whoami</div>
            <h1 class="display-6 fw-bold text-white mb-1">{{FULL_NAME}}</h1>
            <p class="text-info mb-2" style="color: var(--term-accent) !important;">{{HEADLINE}}</p>
            <div class="term-comment small">// Location: Global &bull; Status: Available for Opportunities</div>
          </div>
        </div>

        <div class="mb-4 p-3 rounded-2" style="background: rgba(0,0,0,0.3); border-left: 3px solid var(--term-green-text);">
          <div class="term-comment mb-1"># Bio & Engineering Philosophy</div>
          <p class="mb-0 small text-light" style="line-height: 1.7;">{{ABOUT}}</p>
        </div>

        <div class="d-flex gap-2 flex-wrap mb-2">
          {{SOCIAL_LINKS}}
        </div>
      </div>
    </div>

    <!-- Skills Output -->
    <div class="term-card p-4 mb-4">
      <div class="term-command mb-3">$ cat /skills/active_stack.json</div>
      <div class="p-3 rounded-2" style="background: rgba(0,0,0,0.3);">
        {{SKILLS}}
      </div>
    </div>

    <!-- Projects Section -->
    <div class="term-card p-4 mb-4">
      <div class="term-command mb-3">$ git log --featured-projects --oneline</div>
      {{PROJECTS}}
    </div>

    <!-- Experience Timeline -->
    <div class="term-card p-4 mb-4">
      <div class="term-command mb-3">$ cat /career/experience.log</div>
      {{EXPERIENCE}}
    </div>

    <!-- Footer -->
    <footer class="text-center py-4 text-secondary small">
      <p class="mb-1">&copy; 2026 {{FULL_NAME}} &bull; Built with AI Terminal Code Generator</p>
      <p class="mb-0">Contact: <a href="mailto:{{EMAIL}}" class="text-info">{{EMAIL}}</a></p>
    </footer>
  </div>
</div>"""

    elif archetype == "cyberpunk_hud":
        return """<!-- Bespoke Cyberpunk Neural HUD Portfolio Code -->
<style>
  :root {
    --cyber-bg: #090d16;
    --cyber-cyan: #00e5ff;
    --cyber-purple: #a855f7;
    --cyber-card: rgba(15, 23, 42, 0.85);
    --cyber-border: rgba(0, 229, 255, 0.25);
  }
  .cyber-wrapper {
    background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #090d16 65%);
    color: #e2e8f0;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    min-height: 100vh;
    padding: 3rem 1rem;
    position: relative;
  }
  .cyber-card {
    background: var(--cyber-card);
    border: 1px solid var(--cyber-border);
    border-radius: 16px;
    backdrop-filter: blur(16px);
    transition: all 0.3s ease;
  }
  .cyber-card:hover {
    border-color: var(--cyber-cyan);
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.2);
  }
  .cyber-glow-text {
    color: #fff;
    text-shadow: 0 0 18px rgba(0, 229, 255, 0.6);
  }
  .hud-badge {
    background: rgba(0, 229, 255, 0.1);
    color: var(--cyber-cyan);
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
</style>

<div class="cyber-wrapper">
  <div class="container" style="max-width: 1020px;">
    <!-- Neural Hero -->
    <div class="cyber-card p-4 p-md-5 mb-4 text-center text-md-start">
      <div class="row align-items-center g-4">
        <div class="col-md-4 text-center">
          <div class="position-relative d-inline-block">
            <img src="{{PROFILE_IMAGE}}" alt="{{FULL_NAME}}" class="rounded-4 border" style="width: 160px; height: 160px; object-fit: cover; border-color: var(--cyber-cyan) !important; box-shadow: 0 0 30px rgba(0,229,255,0.25);">
            <div class="position-absolute bottom-0 start-50 translate-middle-x mb-n2">
              <span class="hud-badge">ONLINE &bull; 99.9%</span>
            </div>
          </div>
        </div>
        <div class="col-md-8">
          <span class="hud-badge mb-2 d-inline-block">NEURAL HUD INTERFACE</span>
          <h1 class="display-5 fw-extrabold cyber-glow-text mb-2">{{FULL_NAME}}</h1>
          <h4 class="fw-semibold mb-3" style="color: var(--cyber-cyan);">{{HEADLINE}}</h4>
          <p class="text-secondary small mb-4" style="line-height: 1.7; font-size: 0.95rem;">{{ABOUT}}</p>
          <div class="d-flex gap-2 flex-wrap justify-content-center justify-content-md-start">
            {{SOCIAL_LINKS}}
          </div>
        </div>
      </div>
    </div>

    <!-- Telemetry Skills -->
    <div class="cyber-card p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="fw-bold mb-0 text-white">⚡ Neural Skills & Telemetry</h4>
        <span class="hud-badge">BENCHMARKED</span>
      </div>
      {{SKILLS}}
    </div>

    <!-- Projects Grid -->
    <div class="mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3 px-2">
        <h4 class="fw-bold mb-0 text-white">🚀 High-Impact Projects</h4>
        <span class="hud-badge">REPOSITORIES</span>
      </div>
      {{PROJECTS}}
    </div>

    <!-- Career Experience -->
    <div class="cyber-card p-4 mb-4">
      <h4 class="fw-bold mb-3 text-white">💼 Career Timeline & Impact</h4>
      {{EXPERIENCE}}
    </div>

    <!-- Footer -->
    <footer class="text-center py-4 text-secondary small">
      <p class="mb-1">&copy; 2026 {{FULL_NAME}} &bull; High-Throughput Cyberpunk HUD</p>
      <p class="mb-0">Secure Email: <a href="mailto:{{EMAIL}}" style="color: var(--cyber-cyan);">{{EMAIL}}</a></p>
    </footer>
  </div>
</div>"""

    # Default: Modern Modular Bento Grid
    return """<!-- Bespoke Modern Bento Grid Portfolio Code -->
<style>
  :root {
    --bento-primary: #4f46e5;
    --bento-secondary: #06b6d4;
    --bento-card-bg: rgba(255, 255, 255, 0.9);
    --bento-border: rgba(79, 70, 229, 0.12);
  }
  .bento-wrapper {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    color: #0f172a;
    min-height: 100vh;
    padding: 3rem 1rem;
  }
  .bento-card {
    background: var(--bento-card-bg);
    border: 1px solid var(--bento-border);
    border-radius: 20px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(12px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }
  .bento-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 32px -8px rgba(79, 70, 229, 0.15);
  }
  .bento-gradient-text {
    background: linear-gradient(135deg, var(--bento-primary), var(--bento-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
</style>

<div class="bento-wrapper">
  <div class="container" style="max-width: 1040px;">
    <!-- Bento Hero Card -->
    <div class="bento-card p-4 p-md-5 mb-4 border-0 shadow-sm" style="border-top: 5px solid var(--bento-primary) !important;">
      <div class="row align-items-center g-4">
        <div class="col-md-3 text-center">
          <img src="{{PROFILE_IMAGE}}" alt="{{FULL_NAME}}" class="rounded-circle shadow-lg border border-4 border-white" style="width: 140px; height: 140px; object-fit: cover;">
        </div>
        <div class="col-md-9 text-center text-md-start">
          <span class="badge bg-primary-subtle text-primary rounded-pill px-3 py-1 fw-bold small mb-2">Verified Professional</span>
          <h1 class="display-5 fw-extrabold text-dark mb-1 tracking-tight">{{FULL_NAME}}</h1>
          <p class="lead fw-bold bento-gradient-text mb-3">{{HEADLINE}}</p>
          <p class="text-secondary small mb-4" style="line-height: 1.7; font-size: 0.98rem;">{{ABOUT}}</p>
          <div class="d-flex gap-2 flex-wrap justify-content-center justify-content-md-start">
            {{SOCIAL_LINKS}}
          </div>
        </div>
      </div>
    </div>

    <!-- Skills Bento Box -->
    <div class="bento-card p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="fw-bold mb-0 text-dark">⚡ Technical Stack & Expertise</h4>
        <span class="badge bg-light text-dark border rounded-pill px-2.5 py-1 small">Proficiencies</span>
      </div>
      <div class="p-2">
        {{SKILLS}}
      </div>
    </div>

    <!-- Featured Projects Grid -->
    <div class="mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3 px-2">
        <h4 class="fw-bold mb-0 text-dark">🚀 Featured Projects</h4>
        <span class="badge bg-primary text-white rounded-pill px-3 py-1 small">Showcase</span>
      </div>
      {{PROJECTS}}
    </div>

    <!-- Experience Timeline -->
    <div class="bento-card p-4 mb-4">
      <h4 class="fw-bold mb-3 text-dark">💼 Professional Journey</h4>
      {{EXPERIENCE}}
    </div>

    <!-- Education & Credentials -->
    <div class="bento-card p-4 mb-4">
      <h4 class="fw-bold mb-3 text-dark">🎓 Education & Certifications</h4>
      {{EDUCATION}}
    </div>

    <!-- Footer -->
    <footer class="text-center py-4 border-top text-muted small">
      <p class="mb-1">&copy; 2026 {{FULL_NAME}}. All rights reserved.</p>
      <p class="mb-0">Get in touch: <a href="mailto:{{EMAIL}}" class="text-primary fw-semibold">{{EMAIL}}</a></p>
    </footer>
  </div>
</div>"""
