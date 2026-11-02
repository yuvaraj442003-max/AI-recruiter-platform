"""
resume_parser.py — extracts raw text from an uploaded resume file.

PDF: tries PyMuPDF first (fast, good general extraction), falls back to
pdfplumber if PyMuPDF returns suspiciously little text (common with
resumes that use text boxes / unusual layouts pdfplumber handles better).

DOCX: uses python-docx to walk paragraphs and table cells.
"""
import io

import pymupdf  # PyMuPDF
import pdfplumber
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

from app.core.exceptions import AppError


class ResumeParsingError(AppError):
    def __init__(self, message: str = "Could not extract text from this resume file"):
        super().__init__(message, "RESUME_PARSE_ERROR", 422)


def _extract_pdf_pymupdf(file_bytes: bytes) -> str:
    text_parts = []
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            try:
                # Use block-level extraction so multi-column layouts (e.g. Education left, Certifications right)
                # are preserved in natural reading flow rather than interleaving lines by vertical coordinates
                blocks = page.get_text("blocks")
                page_blocks = [b[4].strip() for b in blocks if len(b) > 4 and b[4].strip()]
                if page_blocks:
                    text_parts.append("\n\n".join(page_blocks))
                else:
                    page_text = page.get_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text.strip())
            except Exception:
                page_text = page.get_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text.strip())
    return "\n\n".join(text_parts)


def _extract_pdf_pdfplumber(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(layout=False) or page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text.strip())
    return "\n".join(text_parts)


def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        text = _extract_pdf_pymupdf(file_bytes)
    except Exception:
        text = ""

    # PyMuPDF sometimes returns suspiciously little text on unusual layouts or textboxes — fall back to pdfplumber
    if len(text.strip()) < 150:
        try:
            fallback_text = _extract_pdf_pdfplumber(file_bytes)
            if len(fallback_text.strip()) > len(text.strip()):
                text = fallback_text
        except Exception:
            pass
    elif len(text.strip()) < 600:
        # Check if pdfplumber extracts substantially more text (e.g. form fields, textboxes)
        try:
            fallback_text = _extract_pdf_pdfplumber(file_bytes)
            if len(fallback_text.strip()) > len(text.strip()) * 1.25:
                text = fallback_text
        except Exception:
            pass

    if len(text.strip()) < 10:
        raise ResumeParsingError("The PDF appears to contain no extractable text (it may be a scanned image).")

    return text.strip()


def extract_docx_text(file_bytes: bytes) -> str:
    try:
        document = Document(io.BytesIO(file_bytes))
    except Exception as exc:
        raise ResumeParsingError("This file could not be read as a .docx document.") from exc

    parts = []
    try:
        # Walk body in natural document order so tables remain directly attached to their respective section headers
        for child in document.element.body:
            if child.tag.endswith("p"):
                p = Paragraph(child, document)
                txt = p.text.strip()
                if txt:
                    parts.append(txt)
            elif child.tag.endswith("tbl"):
                t = Table(child, document)
                for row in t.rows:
                    row_cells_text = []
                    seen_in_row = set()
                    for cell in row.cells:
                        ctext = cell.text.strip()
                        # avoid duplicate text in merged cells
                        if ctext and ctext not in seen_in_row:
                            seen_in_row.add(ctext)
                            row_cells_text.append(ctext)
                    if row_cells_text:
                        parts.append(" | ".join(row_cells_text))
    except Exception:
        # Fallback to standard paragraphs and tables if custom document XML walking fails
        parts = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        for table in document.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    parts.append(" | ".join(dict.fromkeys(row_cells)))

    text = "\n".join(parts).strip()
    if len(text) < 10:
        raise ResumeParsingError("The document appears to contain no extractable text.")
    return text


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    """Dispatch to the right extractor based on file extension."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_pdf_text(file_bytes)
    if lower.endswith(".docx"):
        return extract_docx_text(file_bytes)
    if lower.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1", errors="replace").strip()
    if lower.endswith(".doc"):
        raise ResumeParsingError(
            "Legacy .doc files are not supported — please re-save the resume as .docx or .pdf."
        )
    raise ResumeParsingError("Unsupported file type.")
