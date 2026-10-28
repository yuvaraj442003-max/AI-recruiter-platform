import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.candidate import CandidateProfile
from app.models.portfolio import Portfolio
from app.models.user import User

db = SessionLocal()
try:
    candidates = db.query(CandidateProfile).all()
    print(f"Total candidates: {len(candidates)}")
    for c in candidates:
        user_name = c.user.name if c.user else "No User"
        user_email = c.user.email if c.user else "No Email"
        port = db.query(Portfolio).filter(Portfolio.candidate_id == c.id).first()
        port_slug = port.slug if port else "None"
        port_title = port.professional_headline if port else "None"
        print(f"Candidate: ID={c.id} | Name={user_name} | Email={user_email} | Role={c.current_role} | Headline={c.headline} | Resume={c.resume_original_filename} | Slug={port_slug} | Headline={port_title}")
finally:
    db.close()
