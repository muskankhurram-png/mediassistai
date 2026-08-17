"""
Extracts text directly from PDF files that have a real text layer
(i.e. not scanned images) using PyMuPDF.
"""
import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> str:
    text_parts = []
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).strip()
