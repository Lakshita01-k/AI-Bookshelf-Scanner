"""
Recommend router — GET /api/recommend/{book_id}
Returns ideal placement for a book and a human-readable instruction.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.db import get_db, Book, Shelf
from app.models.schemas import RecommendationOut
from app.services.shelf_rules import compute_correct_order
from app.data.demo_data import DEMO_BOOKS, DEMO_SHELF_ID, DEMO_SHELF_NAME

router = APIRouter(prefix="/api/recommend", tags=["recommend"])


@router.get("/{book_id}", response_model=RecommendationOut)
def get_recommendation(
    book_id: str,
    current_position: int = Query(default=-1),
    db: Session = Depends(get_db),
):
    """
    Return the ideal shelf position for a book, plus a human-readable move instruction.
    """
    book = db.query(Book).filter(Book.id == book_id).first()

    # Fallback to demo data if not in DB
    if not book:
        demo_book = next((b for b in DEMO_BOOKS if b["id"] == book_id), None)
        if not demo_book:
            raise HTTPException(status_code=404, detail="Book not found")
        # Build recommendation from demo data
        return _build_demo_recommendation(demo_book, current_position)

    shelf = db.query(Shelf).filter(Shelf.id == book.shelf_id).first()
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")

    all_books = db.query(Book).filter(Book.shelf_id == shelf.id).all()
    books_list = [
        {"id": b.id, "title": b.title, "author": b.author, "genre": b.genre, "position": b.position}
        for b in all_books
    ]
    sorted_books = compute_correct_order(books_list, shelf.sort_rule)

    target = next((b for b in sorted_books if b["id"] == book_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Book not in sorted order")

    ideal_pos = target["expected_position"]
    neighbor_left = next((b["title"] for b in sorted_books if b["expected_position"] == ideal_pos - 1), None)
    neighbor_right = next((b["title"] for b in sorted_books if b["expected_position"] == ideal_pos + 1), None)

    if neighbor_left and neighbor_right:
        between = f"between '{neighbor_left}' and '{neighbor_right}'"
    elif neighbor_left:
        between = f"after '{neighbor_left}'"
    elif neighbor_right:
        between = f"before '{neighbor_right}'"
    else:
        between = f"at position {ideal_pos + 1}"

    from_pos = current_position if current_position >= 0 else book.position
    diff = ideal_pos - from_pos
    direction = "to the right" if diff > 0 else "to the left"
    spots = abs(diff)
    instruction = (
        f"Move '{book.title}' {spots} spot{'s' if spots != 1 else ''} {direction} — {between}"
        if diff != 0 else f"'{book.title}' is already in the correct position! ✅"
    )

    return RecommendationOut(
        book_id=book_id,
        title=book.title,
        current_position=from_pos,
        ideal_shelf_id=shelf.id,
        ideal_shelf_name=shelf.name,
        ideal_position=ideal_pos,
        instruction=instruction,
        neighbor_left=neighbor_left,
        neighbor_right=neighbor_right,
    )


def _build_demo_recommendation(demo_book: dict, current_position: int) -> RecommendationOut:
    sorted_books = compute_correct_order(
        [{"id": b["id"], "title": b["title"], "author": b["author"], "genre": b["genre"], "position": b["position"]}
         for b in DEMO_BOOKS],
        "alphabetical"
    )
    target = next((b for b in sorted_books if b["id"] == demo_book["id"]), None)
    ideal_pos = target["expected_position"] if target else demo_book["position"]

    neighbor_left = next((b["title"] for b in sorted_books if b["expected_position"] == ideal_pos - 1), None)
    neighbor_right = next((b["title"] for b in sorted_books if b["expected_position"] == ideal_pos + 1), None)

    from_pos = current_position if current_position >= 0 else demo_book["position"]
    diff = ideal_pos - from_pos
    direction = "to the right" if diff > 0 else "to the left"
    spots = abs(diff)

    if neighbor_left and neighbor_right:
        between = f"between '{neighbor_left}' and '{neighbor_right}'"
    elif neighbor_left:
        between = f"after '{neighbor_left}'"
    elif neighbor_right:
        between = f"before '{neighbor_right}'"
    else:
        between = f"at position {ideal_pos + 1}"

    instruction = (
        f"Move '{demo_book['title']}' {spots} spot{'s' if spots != 1 else ''} {direction} — {between}"
        if diff != 0 else f"'{demo_book['title']}' is already in the correct position! ✅"
    )

    return RecommendationOut(
        book_id=demo_book["id"],
        title=demo_book["title"],
        current_position=from_pos,
        ideal_shelf_id=DEMO_SHELF_ID,
        ideal_shelf_name=DEMO_SHELF_NAME,
        ideal_position=ideal_pos,
        instruction=instruction,
        neighbor_left=neighbor_left,
        neighbor_right=neighbor_right,
    )
