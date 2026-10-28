import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.candidate import CandidateProfile
from app.models.portfolio import Portfolio
from app.services.portfolio_service import (
    build_portfolio_from_candidate_profile,
    extract_resume_text,
    parse_resume_fields,
    extract_structured_portfolio_data
)

db = SessionLocal()
try:
    candidates = db.query(CandidateProfile).all()
    print(f"Syncing portfolios for {len(candidates)} candidates...")

    for cand in candidates:
        name = cand.user.name if cand.user else "Candidate"
        print(f"\nProcessing {name}...")

        # If resume_path exists, ensure raw_text is fresh
        raw_text = cand.resume_text or ""
        if cand.resume_path and os.path.exists(cand.resume_path):
            with open(cand.resume_path, "rb") as f:
                raw_text = extract_resume_text(f.read(), os.path.basename(cand.resume_path))
                cand.resume_text = raw_text

        parsed_fields = parse_resume_fields(raw_text) if raw_text else {}
        extracted = extract_structured_portfolio_data(raw_text, parsed_fields) if raw_text else {}

        # Update candidate profile fields to match verified resume
        if extracted.get("professional_headline"):
            cand.current_role = extracted["professional_headline"]
            cand.headline = extracted["professional_headline"]
        if extracted.get("about") and not cand.summary:
            cand.summary = extracted["about"]
        if extracted.get("education_items") and not cand.education:
            cand.education = json.dumps(extracted["education_items"])
        if extracted.get("experience") and not cand.work_experience:
            cand.work_experience = json.dumps(extracted["experience"])

        db.commit()

        # Build / update portfolio record
        portfolio = build_portfolio_from_candidate_profile(db=db, candidate=cand)

        # Set specific canonical slugs matching candidate craft
        if "keira" in name.lower():
            portfolio.slug = "keira-waldemer-corporate-recruiter"
            portfolio.theme_id = "corporate"
            portfolio.layout = "corporate"
            portfolio.primary_color = "#0D9488"
            portfolio.secondary_color = "#0284C7"
            portfolio.dark_mode = False
            portfolio.achievements = json.dumps([
                {"value": "$6M+", "label": "Hiring Expenses Saved", "icon": "⚡"},
                {"value": "41%", "label": "Faster Time-to-Hire", "icon": "⏱️"},
                {"value": "470+", "label": "Top Candidates Vetted", "icon": "👥"},
                {"value": "10+", "label": "Years Talent Leadership", "icon": "🏆"}
            ])
        elif "navin" in name.lower():
            portfolio.slug = "navin-bharath-n-data-scientist-ai-engineer"
            portfolio.theme_id = "ai_tech"
            portfolio.layout = "ai_tech"
            portfolio.primary_color = "#00E5FF"
            portfolio.secondary_color = "#6366F1"
            portfolio.dark_mode = True
            portfolio.professional_headline = "AI & Machine Learning Engineer | Intelligent Systems Developer"
            portfolio.achievements = json.dumps([
                {"value": "87%", "label": "BERT Emotion Accuracy", "icon": "🤖"},
                {"value": "82%", "label": "Satellite Land-Use Parity", "icon": "🛰️"},
                {"value": "4+", "label": "Shipped AI & ML Systems", "icon": "🚀"},
                {"value": "7.9", "label": "Kongunadu AI/ML GPA", "icon": "🎓"}
            ])
        elif "srikanth" in name.lower():
            portfolio.slug = "srikanth-software-developer"
            portfolio.theme_id = "developer"
            portfolio.layout = "developer"
            portfolio.primary_color = "#10B981"
            portfolio.secondary_color = "#06B6D4"
            portfolio.dark_mode = False
            portfolio.achievements = json.dumps([
                {"value": "7+", "label": "Production Web & Mobile Apps", "icon": "📱"},
                {"value": "100%", "label": "Responsive Cross-Platform", "icon": "💻"},
                {"value": "AES", "label": "Honey Password Security", "icon": "🔒"},
                {"value": "7.32", "label": "Paavai College CGPA", "icon": "🎓"}
            ])
        elif "yokesh" in name.lower():
            portfolio.slug = "yokesh-thirumoorthi-applied-ai-architect"
            portfolio.theme_id = "ai_tech"
            portfolio.layout = "ai_tech"
            portfolio.primary_color = "#8B5CF6"
            portfolio.secondary_color = "#00E5FF"
            portfolio.dark_mode = True
            portfolio.professional_headline = "Applied AI SDLC Architect | Production GenAI & Agentic Systems"
            portfolio.achievements = json.dumps([
                {"value": "<800ms", "label": "Voice Bot Inference Latency", "icon": "⚡"},
                {"value": "95%+", "label": "Voice Accent Accuracy", "icon": "🎯"},
                {"value": "1M+", "label": "Daily Microservice Requests", "icon": "🌐"},
                {"value": "70%", "label": "MTTR Observability Reduction", "icon": "📉"}
            ])
        elif "priyanka" in name.lower():
            portfolio.slug = "priyanka-kumar-data-analyst"
            portfolio.theme_id = "modern"
            portfolio.layout = "modern"
            portfolio.primary_color = "#BA855E"
            portfolio.secondary_color = "#0F172A"
            portfolio.dark_mode = False
            portfolio.achievements = json.dumps([
                {"value": "2000+", "label": "ETL Pipelines Orchestrated", "icon": "📊"},
                {"value": "10+", "label": "Years Quantitative Analytics", "icon": "📈"},
                {"value": "800+", "label": "Executive Dashboards Shipped", "icon": "💼"},
                {"value": "100%", "label": "Enterprise Data Parity", "icon": "🛡️"}
            ])
        elif "kumaresan" in name.lower():
            portfolio.slug = "kumaresan-t-backend-developer" if "t" in name.lower() else "kumaresan-junior-software-developer"
            portfolio.theme_id = "developer"
            portfolio.layout = "developer"
            portfolio.primary_color = "#10B981"
            portfolio.secondary_color = "#06B6D4"
            portfolio.dark_mode = True

        portfolio.is_published = True
        db.commit()
        db.refresh(portfolio)
        print(f"  [OK] Saved portfolio for {name}: slug={portfolio.slug}, role={portfolio.professional_headline}")

    print("\nAll candidate portfolios synchronized successfully!")
finally:
    db.close()
