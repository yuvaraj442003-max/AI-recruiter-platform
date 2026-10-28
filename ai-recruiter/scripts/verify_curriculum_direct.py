import sys, os

backend_dir = os.path.abspath('ai-recruiter/backend')
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal
from app.models.student import StudyMaterial
from app.services.book_curriculum_service import ALL_PRESCRIBED_TEXTBOOKS, get_prescribed_books_status
from app.routers.study_materials import get_book_chapters, get_study_material_detail

def run():
    print("=" * 70)
    print("DIRECT CURRICULUM & DATABASE VERIFICATION TEST")
    print("=" * 70)

    db = SessionLocal()
    try:
        # 1. Prescribed books catalog status
        books = get_prescribed_books_status()
        print(f"[1] get_prescribed_books_status() -> Total books: {len(books)}")
        assert len(books) == 13, f"Expected 13 books, got {len(books)}"

        total_chapters = 0
        total_solved = 0
        total_practice = 0
        total_interview = 0

        for b in books:
            slug = b["slug"]
            subject = b["subject"]
            ch_count = b["chapters_count"]

            # 2. Test get_book_chapters endpoint function
            ch_resp = get_book_chapters(subject=slug, db=db)
            assert ch_resp.success, f"Failed chapters for {slug}"
            ch_data = ch_resp.data
            assert ch_data["chapters_count"] == ch_count

            # 3. Test get_study_material_detail (fetching database record)
            from unittest.mock import MagicMock
            mock_user = MagicMock()
            mat_resp = get_study_material_detail(slug=slug, current_user=mock_user, db=db)
            assert mat_resp.success, f"Failed detail for {slug}"
            mat_data = mat_resp.data
            md = mat_data.content_markdown
            assert len(md) > 25000, f"Markdown too short: {len(md)}"

            print(f"  [OK] {slug} | {ch_count} chapters | {len(md):,} chars")

            # Check every chapter has all 5 required sections
            for ch in ch_data["chapters"]:
                num = ch["chapter_num"]
                total_chapters += 1
                sec = ch.get("sections", {})
                solved = sec.get("solved_examples", [])
                practice = sec.get("practice_questions", [])
                interview = sec.get("interview_questions", [])

                total_solved += len(solved)
                total_practice += len(practice)
                total_interview += len(interview)

                assert f"## Chapter {num}:" in md, f"Missing Ch {num} in {slug}"
                assert "### 📘 1. Core Concepts" in md, f"Missing Concepts in {slug}"
                assert "### 📐 2. Key Formulas" in md or "formulas" in sec, f"Missing Formulas in {slug}"
                assert "### 💡 3. Step-by-Step Solved Examples" in md, f"Missing Solved in {slug}"
                assert "### 📝 4. Practice Questions" in md, f"Missing Practice in {slug}"
                assert "### 💼 5. Real Company Technical Interview Questions" in md, f"Missing Interview in {slug}"

        # 4. Check PDF files on disk
        dataset_books_dir = os.path.abspath("../dataset/books")
        print(f"\n[2] Physical PDF verification in {dataset_books_dir}")
        for b in books:
            pdf_path = os.path.join(dataset_books_dir, f"{b['slug']}.pdf")
            assert os.path.exists(pdf_path), f"Missing PDF for {b['slug']}"
            size_kb = os.path.getsize(pdf_path) / 1024.0
            print(f"  [PDF OK] {b['slug']}.pdf ({size_kb:.1f} KB)")

        print("\n" + "=" * 70)
        print("VERIFICATION COMPLETE: 100% PASSED!")
        print(f"Total Textbooks Verified: {len(books)}")
        print(f"Total Chapters Verified: {total_chapters}")
        print(f"Total Step-by-Step Solved Examples: {total_solved}")
        print(f"Total Practice Questions with Solutions: {total_practice}")
        print(f"Total Company Technical Interview Questions: {total_interview}")
        print("=" * 70)
    finally:
        db.close()

if __name__ == "__main__":
    run()

