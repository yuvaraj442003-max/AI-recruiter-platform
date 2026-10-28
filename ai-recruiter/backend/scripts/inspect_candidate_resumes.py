import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.candidate import CandidateProfile
from app.services.portfolio_service import extract_resume_text, parse_resume_fields, extract_structured_portfolio_data

db = SessionLocal()
try:
    candidates = db.query(CandidateProfile).all()
    for c in candidates:
        print(f"\n==========================================")
        print(f"CANDIDATE: {c.user.name if c.user else 'No User'} ({c.user.email if c.user else 'No Email'})")
        print(f"Resume Path: {c.resume_path}")
        print(f"Resume Original: {c.resume_original_filename}")
        
        raw_text = c.resume_text or ""
        if not raw_text and c.resume_path and os.path.exists(c.resume_path):
            with open(c.resume_path, "rb") as f:
                raw_text = extract_resume_text(f.read(), os.path.basename(c.resume_path))
        
        parsed = parse_resume_fields(raw_text) if raw_text else {}
        print("Parsed Name:", parsed.get("name"))
        print("Parsed Headline:", parsed.get("headline"))
        print("Parsed Role:", parsed.get("current_role"))
        print("Parsed Skills (count):", len(parsed.get("skills", [])))
        print("Parsed Experience items (count):", len(parsed.get("work_experience_items", [])))
        if parsed.get("work_experience_items"):
            for exp in parsed.get("work_experience_items")[:3]:
                print("  - Exp:", exp.get("role"), "at", exp.get("company"), f"({exp.get('start_date')} - {exp.get('end_date')})")
        print("Parsed Projects items (count):", len(parsed.get("projects", [])))
        if parsed.get("projects"):
            for prj in parsed.get("projects")[:3]:
                print("  - Project:", prj.get("title"))
        print("Parsed Education (count):", len(parsed.get("education_items", [])))
        if parsed.get("education_items"):
            for edu in parsed.get("education_items")[:2]:
                print("  - Edu:", edu.get("degree"), "at", edu.get("institution"))
finally:
    db.close()
