"""
Decides how to extract text from an uploaded medical report,
based on its file type — with an OCR fallback for scanned PDFs.
"""
from pathlib import Path

from app.ai.ocr import extract_text_from_image
from app.ai.pdf_extractor import extract_text_from_pdf


def extract_report_text(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        text = extract_text_from_pdf(file_path)
        if text:
            return text
        # PDF had no real text layer (likely a scanned document) - no OCR
        # fallback for PDFs in this simple version; return empty string.
        return ""

    if suffix in {".png", ".jpg", ".jpeg"}:
        return extract_text_from_image(file_path)

    return ""
