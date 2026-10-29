import sys, os

backend_dir = os.path.abspath('ai-recruiter/backend')
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal
from app.models.student import StudyMaterial
from app.services.book_curriculum_service import ALL_PRESCRIBED_TEXTBOOKS, build_textbook_markdown

print("\n=======================================================")
print("Targeting PostgreSQL database for textbooks")
print("=======================================================")
session = SessionLocal()
try:
    updated_count = 0
    total_chars = 0
    for idx, b in enumerate(ALL_PRESCRIBED_TEXTBOOKS):
        md_content = build_textbook_markdown(b)
        mat = session.query(StudyMaterial).filter(StudyMaterial.slug == b["slug"]).first()
        if mat:
            mat.title = b["title"]
            mat.description = b["description"]
            mat.content_markdown = md_content
            mat.content_type = "textbook"
            mat.category = "textbook"
            mat.company_tag = "Prescribed Curriculum"
            mat.order_index = idx + 1
        else:
            import json
            tags = [b["subject"], "Textbook", "Prescribed Curriculum", "Placement Exam Syllabus", "Core Guide"]
            mat = StudyMaterial(
                title=b["title"],
                slug=b["slug"],
                category="textbook",
                content_type="textbook",
                description=b["description"],
                content_markdown=md_content,
                company_tag="Prescribed Curriculum",
                tags_json=json.dumps(tags),
                estimated_read_time_minutes=b.get("pages_est", 120) * 2,
                order_index=idx + 1,
            )
            session.add(mat)
        updated_count += 1
        total_chars += len(md_content)
    session.commit()
    print(f"Successfully seeded/updated {updated_count} comprehensive textbooks in PostgreSQL! (Total chars: {total_chars:,})")
except Exception as e:
    session.rollback()
    print(f"Error seeding PostgreSQL: {e}")
finally:
    session.close()
