"""
Extracts text from images (or scanned PDF pages) using Tesseract OCR.
"""
from PIL import Image
import pytesseract


def extract_text_from_image(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image).strip()
