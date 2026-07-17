"""
Inventory router — CRUD for shelves and books.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.models.db import get_db, Shelf, Book
from app.models.schemas import (
    InventoryResponse, InventoryCreate, ShelfOut, BookOut, BookCreate
)
from app.data.demo_data import DEMO_BOOKS, DEMO_SHELF_ID, DEMO_SHELF_NAME

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


def _ensure_demo_shelf(db: Session):
    """Seed demo shelf if it doesn't exist yet."""
    shelf = db.query(Shelf).filter(Shelf.id == DEMO_SHELF_ID).first()
    if not shelf:
        shelf = Shelf(id=DEMO_SHELF_ID, name=DEMO_SHELF_NAME, sort_rule="alphabetical")
        db.add(shelf)
        db.flush()
        for bdata in DEMO_BOOKS:
            book = Book(
                id=bdata["id"],
                shelf_id=DEMO_SHELF_ID,
                title=bdata["title"],
                author=bdata["author"],
                genre=bdata["genre"],
                isbn=bdata.get("isbn", ""),
                cover_url=bdata.get("cover_url", ""),
                position=bdata["position"],
                color=bdata.get("color", "#8B6E4E"),
            )
            db.add(book)
        db.commit()
    return shelf


@router.get("/{shelf_id}", response_model=InventoryResponse)
def get_inventory(shelf_id: str, db: Session = Depends(get_db)):
    """Return the expected book list and order for a shelf."""
    _ensure_demo_shelf(db)
    shelf = db.query(Shelf).filter(Shelf.id == shelf_id).first()
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")

    books = db.query(Book).filter(Book.shelf_id == shelf_id).order_by(Book.position).all()
    return InventoryResponse(
        shelf=ShelfOut.model_validate(shelf),
        books=[BookOut.model_validate(b) for b in books],
    )


@router.post("", response_model=InventoryResponse)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    """Create a new shelf with its books."""
    shelf_id = str(uuid.uuid4())
    shelf = Shelf(
        id=shelf_id,
        name=payload.shelf.name,
        sort_rule=payload.shelf.sort_rule.value,
    )
    db.add(shelf)
    db.flush()

    books = []
    for idx, bdata in enumerate(payload.books):
        book = Book(
            id=str(uuid.uuid4()),
            shelf_id=shelf_id,
            title=bdata.title,
            author=bdata.author,
            genre=bdata.genre,
            isbn=bdata.isbn,
            cover_url=bdata.cover_url,
            position=bdata.position if bdata.position is not None else idx,
            color=bdata.color,
        )
        db.add(book)
        books.append(book)

    db.commit()
    db.refresh(shelf)

    return InventoryResponse(
        shelf=ShelfOut.model_validate(shelf),
        books=[BookOut.model_validate(b) for b in books],
    )


@router.get("", response_model=List[ShelfOut])
def list_shelves(db: Session = Depends(get_db)):
    """List all shelves."""
    _ensure_demo_shelf(db)
    shelves = db.query(Shelf).all()
    return [ShelfOut.model_validate(s) for s in shelves]
