"""
Shelf health router — GET /api/shelf-health/{shelf_id}
Returns aggregate stats for the dashboard.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import Counter

from app.models.db import get_db, Shelf, Book
from app.models.schemas import ShelfHealthOut, GenreCount
from app.data.demo_data import (
    DEMO_SHELF_ID, DEMO_SHELF_NAME, DEMO_DETECTED_BOOKS, DEMO_BOOKS, DEMO_SHELF_SCORE
)

router = APIRouter(prefix="/api/shelf-health", tags=["shelf-health"])


@router.get("/{shelf_id}", response_model=ShelfHealthOut)
def get_shelf_health(shelf_id: str, db: Session = Depends(get_db)):
    """Return aggregate health stats for a shelf."""

    if shelf_id == DEMO_SHELF_ID:
        return _build_demo_health()

    shelf = db.query(Shelf).filter(Shelf.id == shelf_id).first()
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")

    books = db.query(Book).filter(Book.shelf_id == shelf_id).all()
    genre_counts = Counter(b.genre for b in books)
    genre_dist = [GenreCount(genre=g, count=c) for g, c in genre_counts.most_common()]

    return ShelfHealthOut(
        shelf_id=shelf_id,
        shelf_name=shelf.name,
        total_books=len(books),
        correct_count=len(books),  # No scan data in DB flow — assume all correct
        misplaced_count=0,
        missing_count=0,
        unknown_count=0,
        shelf_score=100.0,
        genre_distribution=genre_dist,
        sort_rule=shelf.sort_rule,
    )


def _build_demo_health() -> ShelfHealthOut:
    statuses = [d["status"] for d in DEMO_DETECTED_BOOKS]
    genre_counts = Counter(b["genre"] for b in DEMO_BOOKS)
    genre_dist = [GenreCount(genre=g, count=c) for g, c in genre_counts.most_common()]

    return ShelfHealthOut(
        shelf_id=DEMO_SHELF_ID,
        shelf_name=DEMO_SHELF_NAME,
        total_books=len(DEMO_BOOKS),
        correct_count=statuses.count("correct"),
        misplaced_count=statuses.count("misplaced"),
        missing_count=statuses.count("missing"),
        unknown_count=statuses.count("unknown"),
        shelf_score=DEMO_SHELF_SCORE,
        genre_distribution=genre_dist,
        sort_rule="alphabetical",
    )
