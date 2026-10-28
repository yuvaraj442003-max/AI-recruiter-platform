import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.candidate import CandidateProfile
from app.services.portfolio_service import extract_resume_text

db = SessionLocal()
try:
    candidates = db.query(CandidateProfile).all()
    for c in candidates:
        name = c.user.name if c.user else "Unknown"
        safe_name = "".join(ch for ch in name if ch.isalnum() or ch == "_").strip()
        raw_text = c.resume_text or ""
        if not raw_text and c.resume_path and os.path.exists(c.resume_path):
            with open(c.resume_path, "rb") as f:
                raw_text = extract_resume_text(f.read(), os.path.basename(c.resume_path))
        
        out_path = os.path.join(os.path.dirname(__file__), f"raw_resume_{safe_name}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(raw_text)
        print(f"Wrote {len(raw_text)} chars for {name} to {out_path}")
finally:
    db.close()
