"""
Book metadata service.
Looks up book info from Open Library API using fuzzy-matched OCR text.
No API key required for Open Library basic searches.
"""
import httpx
from rapidfuzz import fuzz
from typing import Optional, Dict, List
import asyncio

OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
OPEN_LIBRARY_COVER = "https://covers.openlibrary.org/b/id/{}-M.jpg"

# Simple in-memory cache: {ocr_text: metadata_dict}
_cache: Dict[str, Optional[Dict]] = {}


async def lookup_book(ocr_text: str) -> Optional[Dict]:
    """
    Given OCR text from a spine, search Open Library and return best match.
    Returns dict with title, author, genre, cover_url, isbn, confidence.
    """
    if not ocr_text or len(ocr_text) < 3:
        return None

    cache_key = ocr_text.lower().strip()
    if cache_key in _cache:
        return _cache[cache_key]

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(OPEN_LIBRARY_SEARCH, params={"q": ocr_text, "limit": 5})
            if resp.status_code != 200:
                _cache[cache_key] = None
                return None

            data = resp.json()
            docs = data.get("docs", [])
            if not docs:
                _cache[cache_key] = None
                return None

            # Find best fuzzy match
            best_doc = None
            best_score = 0
            for doc in docs:
                title = doc.get("title", "")
                score = fuzz.partial_ratio(ocr_text.lower(), title.lower())
                if score > best_score:
                    best_score = score
                    best_doc = doc

            if best_doc is None or best_score < 50:
                _cache[cache_key] = None
                return None

            cover_id = best_doc.get("cover_i")
            cover_url = OPEN_LIBRARY_COVER.format(cover_id) if cover_id else ""

            authors = best_doc.get("author_name", [])
            author = authors[0] if authors else ""

            subjects = best_doc.get("subject", [])
            genre = _infer_genre(subjects)

            isbn_list = best_doc.get("isbn", [])
            isbn = isbn_list[0] if isbn_list else ""

            result = {
                "title": best_doc.get("title", ""),
                "author": author,
                "genre": genre,
                "cover_url": cover_url,
                "isbn": isbn,
                "confidence": best_score / 100.0,
            }
            _cache[cache_key] = result
            return result

    except Exception:
        _cache[cache_key] = None
        return None


def _infer_genre(subjects: List[str]) -> str:
    """Map Open Library subjects to a simplified genre label."""
    genre_map = {
        "fantasy": "Fantasy",
        "science fiction": "Sci-Fi",
        "sci-fi": "Sci-Fi",
        "mystery": "Mystery",
        "thriller": "Thriller",
        "biography": "Biography",
        "memoir": "Memoir",
        "history": "History",
        "self-help": "Self-Help",
        "self help": "Self-Help",
        "non-fiction": "Non-Fiction",
        "fiction": "Fiction",
        "horror": "Horror",
        "romance": "Romance",
        "graphic novel": "Graphic Novel",
        "comics": "Comics",
        "children": "Children",
        "young adult": "Young Adult",
        "philosophy": "Philosophy",
        "poetry": "Poetry",
        "dystopian": "Dystopian",
    }

    subjects_lower = " ".join(subjects).lower()
    for keyword, genre in genre_map.items():
        if keyword in subjects_lower:
            return genre
    return "Fiction"


def fuzzy_match_against_inventory(ocr_text: str, inventory: List[Dict]) -> Optional[Dict]:
    """
    Fast fuzzy match OCR text against a known inventory list.
    Returns best matching book dict or None.
    """
    if not ocr_text or not inventory:
        return None

    best_match = None
    best_score = 0

    for book in inventory:
        title_score = fuzz.partial_ratio(ocr_text.lower(), book["title"].lower())
        author_score = fuzz.partial_ratio(ocr_text.lower(), book.get("author", "").lower())
        score = max(title_score, author_score)

        if score > best_score:
            best_score = score
            best_match = book

    if best_score >= 60:
        return {**best_match, "confidence": best_score / 100.0}
    return None
