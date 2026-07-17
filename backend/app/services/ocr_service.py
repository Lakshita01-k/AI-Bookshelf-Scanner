"""
OCR service — wraps pytesseract to extract text from spine images.
"""
import os
import pytesseract
from PIL import Image
import io
from app.config import get_settings

settings = get_settings()

# Allow configuring Tesseract path via env var
if settings.tesseract_cmd and settings.tesseract_cmd != "tesseract":
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


def extract_text_from_bytes(image_bytes: bytes) -> str:
    """Run Tesseract OCR on raw image bytes and return extracted text."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        # Rotate spine images — spines are often rotated 90 degrees
        # Try both orientations and pick whichever gives more text
        text_normal = pytesseract.image_to_string(img, config="--psm 6")
        img_rotated = img.rotate(90, expand=True)
        text_rotated = pytesseract.image_to_string(img_rotated, config="--psm 6")

        if len(text_rotated.strip()) > len(text_normal.strip()):
            return text_rotated.strip()
        return text_normal.strip()
    except Exception as e:
        return ""


def extract_text_enhanced(image_bytes: bytes) -> str:
    """
    Enhanced OCR with preprocessing: grayscale, threshold, denoise.
    """
    from PIL import ImageFilter, ImageEnhance
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L")
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(2.0)
        text = pytesseract.image_to_string(img, config="--psm 6 --oem 3")
        return text.strip()
    except Exception:
        return ""
