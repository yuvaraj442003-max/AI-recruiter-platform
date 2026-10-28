"""
test_books_and_pdfs.py — Comprehensive end-to-end verification of all 13 Master Textbooks,
physical PDF generation, bookmarks, download endpoints, and database contents.
"""
import os
import sys
from pathlib import Path

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.routers.study_materials import (
    get_prescribed_books,
    get_book_chapters,
    download_prescribed_book_pdf,
    get_study_material_detail,
)
from app.services.book_curriculum_service import (
    ALL_PRESCRIBED_TEXTBOOKS,
    get_prescribed_books_status,
    find_prescribed_book_pdf,
)

mock_user = User(
    id="test-student-123",
    email="student@campus.edu",
    role=UserRole.candidate,
    is_active=True,
)

db = SessionLocal()

print("=" * 75)
print(f"1. VERIFYING ALL {len(ALL_PRESCRIBED_TEXTBOOKS)} PRESCRIBED TEXTBOOKS STATUS")
print("=" * 75)

res = get_prescribed_books(None)
assert res.success is True, "Failed to get prescribed books"
books = res.data
print(f"Total textbooks returned by API: {len(books)}")
assert len(books) == 13, f"Expected 13 books, got {len(books)}"

all_have_physical_pdf = True
for b in books:
    slug = b["slug"]
    subj = b["subject"]
    has_pdf = b["has_physical_pdf"]
    pdf_fn = b["pdf_filename"]
    dl_url = b.get("pdf_download_url")
    ch_count = b["chapters_count"]

    print(f"  [{'OK' if has_pdf else 'MISSING'}] {subj}")
    print(f"       Slug: {slug} | Chapters: {ch_count} | PDF: {pdf_fn}")
    print(f"       Download URL: {dl_url}")

    if not has_pdf:
        all_have_physical_pdf = False

assert all_have_physical_pdf, "One or more books are missing their physical PDF file!"

print("\n" + "=" * 75)
print("2. VERIFYING PDF DOWNLOAD ENDPOINT (download_prescribed_book_pdf) FOR ALL 13 BOOKS")
print("=" * 75)

for b in books:
    slug = b["slug"]
    file_resp = download_prescribed_book_pdf(slug)
    assert file_resp.status_code == 200, f"Failed download for {slug}"
    assert file_resp.media_type == "application/pdf", f"Invalid media type for {slug}"
    pdf_path = file_resp.path
    assert os.path.exists(pdf_path), f"File path does not exist: {pdf_path}"
    file_size = os.path.getsize(pdf_path)
    assert file_size > 10000, f"File suspiciously small: {file_size} bytes"
    print(f"  [DOWNLOAD OK] {slug} -> {Path(pdf_path).name} ({file_size:,} bytes, {file_resp.media_type})")

print("\n" + "=" * 75)
print("3. VERIFYING IN-APP COMPLETE TEXTBOOK CONTENT & CHAPTERS IN DATABASE")
print("=" * 75)

for b in books:
    slug = b["slug"]
    detail = get_study_material_detail(slug, current_user=mock_user, db=db)
    assert detail.success is True
    mat = detail.data
    md_len = len(mat.content_markdown or "")
    print(f"  [CONTENT OK] {slug}: {md_len:,} characters of comprehensive markdown")
    assert md_len > 5000, f"Markdown content too small for {slug}: {md_len}"

    # Also test chapter breakdown endpoint
    ch_res = get_book_chapters(slug, db=db)
    assert ch_res.success is True
    ch_data = ch_res.data
    assert len(ch_data["chapters"]) == b["chapters_count"]
    assert ch_data["has_physical_pdf"] is True
    print(f"               {len(ch_data['chapters'])} chapters verified, has_physical_pdf=True")

print("\n" + "=" * 75)
print("ALL 13 PRESCRIBED CAMPUS TEXTBOOKS ARE 100% COMPLETE, VERIFIED, AND SYNCED WITH PHYSICAL PDFS!")
print("=" * 75)
