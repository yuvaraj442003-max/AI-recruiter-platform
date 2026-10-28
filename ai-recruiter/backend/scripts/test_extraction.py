import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.candidate import CandidateProfile
from app.services.portfolio_service import extract_resume_text, parse_resume_fields, extract_structured_portfolio_data

db = SessionLocal()
out_lines = []
try:
    candidates = db.query(CandidateProfile).all()
    for c in candidates:
        name = c.user.name if c.user else "Unknown"
        raw_text = c.resume_text or ""
        if not raw_text and c.resume_path and os.path.exists(c.resume_path):
            with open(c.resume_path, "rb") as f:
                raw_text = extract_resume_text(f.read(), os.path.basename(c.resume_path))
        
        parsed = parse_resume_fields(raw_text) if raw_text else {}
        extracted = extract_structured_portfolio_data(raw_text, parsed)
        
        out_lines.append(f"\n==========================================")
        out_lines.append(f"CANDIDATE: {name}")
        out_lines.append(f"  Headline: {extracted.get('professional_headline')}")
        out_lines.append(f"  Skills count: {len(extracted.get('skills', {}))}")
        out_lines.append(f"  Experience count: {len(extracted.get('experience', []))}")
        for exp in extracted.get("experience", []):
            role = exp.get("role") or exp.get("title") or "Unknown"
            comp = exp.get("company") or "Unknown"
            out_lines.append(f"    - [{comp}] {role} ({exp.get('start_date')} - {exp.get('end_date')})")
        out_lines.append(f"  Projects count: {len(extracted.get('projects', []))}")
        for prj in extracted.get("projects", []):
            p_title = prj.get("title") or prj.get("name") or "Unknown"
            out_lines.append(f"    - Project: {p_title}")
        out_lines.append(f"  Education count: {len(extracted.get('education', []))}")
        for edu in extracted.get("education", []):
            out_lines.append(f"    - Edu: {edu.get('degree')} at {edu.get('institution')}")

    with open("scripts/extraction_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print("Wrote extraction results successfully!")
finally:
    db.close()
