"""
Scan router — POST /api/scan
Accepts an uploaded image and returns detection results.
Uses demo data when USE_DEMO_DATA=true.
"""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.db import get_db, ScanResult, DetectedBook as DetectedBookModel
from app.models.schemas import ScanResponse, DetectedBookOut, BoundingBox, BookStatus
from app.data.demo_data import (
    DEMO_SCAN_ID, DEMO_SHELF_ID, DEMO_DETECTED_BOOKS, DEMO_SHELF_SCORE
)

router = APIRouter(prefix="/api/scan", tags=["scan"])
settings = get_settings()


@router.post("", response_model=ScanResponse)
async def scan_shelf(
    file: UploadFile = File(...),
    shelf_id: str = Query(default=DEMO_SHELF_ID),
    db: Session = Depends(get_db),
):
    """
    Upload a bookshelf image. Returns detected books with bounding boxes and statuses.
    With USE_DEMO_DATA=true, returns pre-baked results immediately.
    """
    if settings.use_demo_data:
        return _build_demo_response(shelf_id)

    # Real pipeline
    image_bytes = await file.read()
    return await _run_real_pipeline(image_bytes, shelf_id, db)


def _build_demo_response(shelf_id: str) -> ScanResponse:
    """Build a ScanResponse from the pre-baked demo data."""
    detected = []
    for d in DEMO_DETECTED_BOOKS:
        detected.append(DetectedBookOut(
            id=d["id"],
            book_id=d.get("book_id"),
            ocr_text=d["ocr_text"],
            matched_title=d["matched_title"],
            matched_author=d["matched_author"],
            confidence=d["confidence"],
            status=BookStatus(d["status"]),
            bbox=BoundingBox(**d["bbox"]),
            detected_position=d["detected_position"],
            expected_position=d["expected_position"],
            genre=d["genre"],
            color=d["color"],
            cover_url=d["cover_url"],
        ))

    correct = sum(1 for d in DEMO_DETECTED_BOOKS if d["status"] == "correct")
    misplaced = sum(1 for d in DEMO_DETECTED_BOOKS if d["status"] == "misplaced")
    missing = sum(1 for d in DEMO_DETECTED_BOOKS if d["status"] == "missing")

    message = (
        f"Found {len(DEMO_DETECTED_BOOKS) - missing} book{'s' if len(DEMO_DETECTED_BOOKS) - missing != 1 else ''}. "
        f"{misplaced} seem{'s' if misplaced == 1 else ''} lost. Let's fix that. 📚"
    ) if misplaced > 0 else f"Found {len(DEMO_DETECTED_BOOKS)} books. Your shelf looks great! ✨"

    return ScanResponse(
        scan_id=DEMO_SCAN_ID,
        shelf_id=shelf_id,
        detected_books=detected,
        shelf_score=DEMO_SHELF_SCORE,
        message=message,
    )


async def _run_real_pipeline(image_bytes: bytes, shelf_id: str, db: Session) -> ScanResponse:
    """Real OCR + detection pipeline."""
    from app.services.spine_detector import detect_spines, crop_spine
    from app.services.ocr_service import extract_text_enhanced
    from app.services.book_metadata import lookup_book
    from app.services.shelf_rules import compute_shelf_score

    scan_id = str(uuid.uuid4())
    spine_boxes = detect_spines(image_bytes)

    detected = []
    for idx, box in enumerate(spine_boxes):
        cropped = crop_spine(image_bytes, box)
        ocr_text = extract_text_enhanced(cropped) if cropped else ""
        metadata = await lookup_book(ocr_text) if ocr_text else None

        det = DetectedBookOut(
            id=str(uuid.uuid4()),
            book_id=None,
            ocr_text=ocr_text,
            matched_title=metadata["title"] if metadata else ocr_text[:50],
            matched_author=metadata["author"] if metadata else "",
            confidence=metadata["confidence"] if metadata else 0.0,
            status=BookStatus.unknown,
            bbox=BoundingBox(x=box["x"], y=box["y"], w=box["w"], h=box["h"]),
            detected_position=idx,
            expected_position=-1,
            genre=metadata["genre"] if metadata else "Unknown",
            cover_url=metadata["cover_url"] if metadata else "",
            color="#8B6E4E",
        )
        detected.append(det)

    score = compute_shelf_score([d.model_dump() for d in detected])
    found = sum(1 for d in detected if d.status != BookStatus.missing)
    message = f"Found {found} books. {sum(1 for d in detected if d.status == BookStatus.unknown)} unrecognised. Confidence may vary. 🔍"

    return ScanResponse(
        scan_id=scan_id,
        shelf_id=shelf_id,
        detected_books=detected,
        shelf_score=score,
        message=message,
    )
