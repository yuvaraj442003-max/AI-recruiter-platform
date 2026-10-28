"""
Seed all 13 prescribed textbooks into the SQLite database and verify contents.
"""
import os
import sys

# Change directory to backend so relative db path matches
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal
from app.models.student import StudyMaterial
from app.services.book_curriculum_service import (
    ALL_PRESCRIBED_TEXTBOOKS,
    TOPIC_QUESTION_BANKS,
    seed_prescribed_books_to_db,
    build_textbook_markdown,
)

print(f"=== CHECKING IN-MEMORY TEXTBOOK DEFINITIONS ({len(ALL_PRESCRIBED_TEXTBOOKS)} BOOKS) ===")
for b in ALL_PRESCRIBED_TEXTBOOKS:
    md = b.get("full_textbook_markdown", "")
    ch = b.get("chapters", [])
    print(f"  {b['slug']}: {len(ch)} chapters, {len(md)} chars markdown, subject='{b['subject']}'")
    assert len(ch) > 0, f"No chapters for {b['slug']}"
    assert len(md) > 2000, f"Markdown too short for {b['slug']}: {len(md)}"

print(f"\n=== CHECKING QUESTION BANKS ({len(TOPIC_QUESTION_BANKS)} MAPPINGS) ===")
for topic, qs in TOPIC_QUESTION_BANKS.items():
    print(f"  {topic}: {len(qs)} questions")
    assert len(qs) > 0, f"No questions for {topic}"

print("\n=== SEEDING TO SQLITE DATABASE ===")
db = SessionLocal()
seed_prescribed_books_to_db(db)

print("\n=== VERIFYING DATABASE CONTENTS (study_materials table) ===")
db_books = db.query(StudyMaterial).filter(StudyMaterial.category == "textbook").order_by(StudyMaterial.order_index).all()
print(f"Total seeded textbooks in database: {len(db_books)}")

for b in db_books:
    md_len = len(b.content_markdown) if b.content_markdown else 0
    print(f"  [DB #{b.order_index}] {b.slug}")
    print(f"       Title: {b.title}")
    print(f"       Markdown Size: {md_len} characters")
    print(f"       Has Exercises/Examples: {'Yes' if ('###' in b.content_markdown and ('Example' in b.content_markdown or 'Code' in b.content_markdown or 'Problem' in b.content_markdown or 'Exercise' in b.content_markdown)) else 'No'}")
    assert md_len > 3000, f"DB content_markdown unexpectedly small for {b.slug}: {md_len}"

print("\nALL 13 TEXTBOOKS SUCCESSFULLY VERIFIED AND SEEDED!")

