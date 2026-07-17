from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class BookStatus(str, Enum):
    correct = "correct"
    misplaced = "misplaced"
    missing = "missing"
    unknown = "unknown"


class SortRule(str, Enum):
    alphabetical = "alphabetical"
    genre = "genre"
    dewey = "dewey"
    custom = "custom"


# ── Shelf schemas ──────────────────────────────────────────────────────────────

class ShelfBase(BaseModel):
    name: str
    sort_rule: SortRule = SortRule.alphabetical


class ShelfCreate(ShelfBase):
    pass


class ShelfOut(ShelfBase):
    id: str

    class Config:
        from_attributes = True


# ── Book schemas ───────────────────────────────────────────────────────────────

class BookBase(BaseModel):
    title: str
    author: str = ""
    genre: str = "Unknown"
    isbn: str = ""
    cover_url: str = ""
    position: int
    color: str = "#8B6E4E"


class BookCreate(BookBase):
    shelf_id: str


class BookOut(BookBase):
    id: str
    shelf_id: str

    class Config:
        from_attributes = True


# ── Bounding box ───────────────────────────────────────────────────────────────

class BoundingBox(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0, description="Left edge, normalized 0-1")
    y: float = Field(..., ge=0.0, le=1.0, description="Top edge, normalized 0-1")
    w: float = Field(..., ge=0.0, le=1.0, description="Width, normalized 0-1")
    h: float = Field(..., ge=0.0, le=1.0, description="Height, normalized 0-1")


# ── Detected book schemas ──────────────────────────────────────────────────────

class DetectedBookOut(BaseModel):
    id: str
    ocr_text: str
    matched_title: str
    matched_author: str
    confidence: float
    status: BookStatus
    bbox: BoundingBox
    detected_position: int
    expected_position: int
    book_id: Optional[str] = None
    genre: str = "Unknown"
    cover_url: str = ""
    color: str = "#8B6E4E"

    class Config:
        from_attributes = True


# ── Scan schemas ───────────────────────────────────────────────────────────────

class ScanResponse(BaseModel):
    scan_id: str
    shelf_id: Optional[str]
    detected_books: List[DetectedBookOut]
    shelf_score: float
    message: str


# ── Inventory schemas ──────────────────────────────────────────────────────────

class InventoryResponse(BaseModel):
    shelf: ShelfOut
    books: List[BookOut]


class InventoryCreate(BaseModel):
    shelf: ShelfCreate
    books: List[BookBase]


# ── Recommendation schemas ─────────────────────────────────────────────────────

class RecommendationOut(BaseModel):
    book_id: str
    title: str
    current_position: int
    ideal_shelf_id: str
    ideal_shelf_name: str
    ideal_position: int
    instruction: str
    neighbor_left: Optional[str] = None
    neighbor_right: Optional[str] = None


# ── Shelf health schemas ───────────────────────────────────────────────────────

class GenreCount(BaseModel):
    genre: str
    count: int


class ShelfHealthOut(BaseModel):
    shelf_id: str
    shelf_name: str
    total_books: int
    correct_count: int
    misplaced_count: int
    missing_count: int
    unknown_count: int
    shelf_score: float
    genre_distribution: List[GenreCount]
    sort_rule: str
