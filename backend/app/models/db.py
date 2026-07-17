from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Shelf(Base):
    __tablename__ = "shelves"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    sort_rule = Column(String, default="alphabetical")  # alphabetical | genre | dewey | custom
    books = relationship("Book", back_populates="shelf", order_by="Book.position")


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    shelf_id = Column(String, ForeignKey("shelves.id"), nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, default="")
    genre = Column(String, default="Unknown")
    isbn = Column(String, default="")
    cover_url = Column(String, default="")
    position = Column(Integer, nullable=False)  # expected position on shelf (0-indexed)
    color = Column(String, default="#8B6E4E")   # spine color hint

    shelf = relationship("Shelf", back_populates="books")


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    shelf_id = Column(String, ForeignKey("shelves.id"), nullable=True)
    image_path = Column(String, default="")
    created_at = Column(String, default="")
    shelf_score = Column(Float, default=0.0)
    detected_books = relationship("DetectedBook", back_populates="scan_result")


class DetectedBook(Base):
    __tablename__ = "detected_books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_result_id = Column(String, ForeignKey("scan_results.id"), nullable=False)
    book_id = Column(String, ForeignKey("books.id"), nullable=True)
    ocr_text = Column(String, default="")
    matched_title = Column(String, default="")
    matched_author = Column(String, default="")
    confidence = Column(Float, default=0.0)
    status = Column(String, default="unknown")  # correct | misplaced | missing | unknown
    # Normalized bounding box (0.0 - 1.0)
    bbox_x = Column(Float, default=0.0)
    bbox_y = Column(Float, default=0.0)
    bbox_w = Column(Float, default=0.0)
    bbox_h = Column(Float, default=0.0)
    detected_position = Column(Integer, default=-1)
    expected_position = Column(Integer, default=-1)

    scan_result = relationship("ScanResult", back_populates="detected_books")
