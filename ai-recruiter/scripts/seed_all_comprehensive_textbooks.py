import sys, os

backend_dir = os.path.abspath('ai-recruiter/backend')
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.student import StudyMaterial
from app.services.book_curriculum_service import ALL_PRESCRIBED_TEXTBOOKS, build_textbook_markdown

db_paths = [
    os.path.join(backend_dir, 'ai_recruiter.db'),
    os.path.abspath(os.path.join(backend_dir, '..', '..', 'ai_recruiter.db')),
]

for db_path in db_paths:
    if not os.path.exists(db_path):
        continue
    print(f"\n=======================================================")
    print(f"Targeting SQLite database: {db_path}")
    print(f"=======================================================")
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    session = Session()
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
                    difficulty="intermediate",
                    estimated_read_time="60 mins",
                    tags_json=json.dumps(tags),
                    order_index=idx + 1,
                )
                session.add(mat)
            updated_count += 1
            total_chars += len(md_content)
            print(f"[OK] [{b['slug']}] -> {len(b['chapters'])} chapters | {len(md_content):,} chars")

        session.commit()
        print(f"\nSuccessfully seeded {updated_count} comprehensive textbooks ({total_chars:,} chars) in {db_path}!")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Error seeding {db_path}: {e}")
    finally:
        session.close()
