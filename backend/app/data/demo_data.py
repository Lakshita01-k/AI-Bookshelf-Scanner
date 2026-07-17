"""
Demo scan response — pre-baked detection data for USE_DEMO_DATA=true.

15 books on a single shelf:
- 11 correct (green)
- 3 misplaced (amber)
- 1 missing (red ghost)
Shelf score: 82%

Bounding boxes are normalized (0-1) for a landscape image.
The demo image should be ~1200×600px of a horizontal bookshelf.
"""

DEMO_SHELF_ID = "demo-shelf-001"
DEMO_SCAN_ID = "demo-scan-001"

DEMO_BOOKS = [
    {
        "id": "b001", "title": "The Name of the Wind",
        "author": "Patrick Rothfuss", "genre": "Fantasy",
        "position": 0, "color": "#6B3A2A",
        "cover_url": "https://covers.openlibrary.org/b/id/8739161-M.jpg",
        "isbn": "9780756404741"
    },
    {
        "id": "b002", "title": "Dune",
        "author": "Frank Herbert", "genre": "Sci-Fi",
        "position": 1, "color": "#C4914B",
        "cover_url": "https://covers.openlibrary.org/b/id/8225277-M.jpg",
        "isbn": "9780441013593"
    },
    {
        "id": "b003", "title": "Educated",
        "author": "Tara Westover", "genre": "Memoir",
        "position": 2, "color": "#3D6B8C",
        "cover_url": "https://covers.openlibrary.org/b/id/8739045-M.jpg",
        "isbn": "9780399590504"
    },
    {
        "id": "b004", "title": "Circe",
        "author": "Madeline Miller", "genre": "Fantasy",
        "position": 3, "color": "#8B4513",
        "cover_url": "https://covers.openlibrary.org/b/id/8739098-M.jpg",
        "isbn": "9780316556347"
    },
    {
        "id": "b005", "title": "The Midnight Library",
        "author": "Matt Haig", "genre": "Fiction",
        "position": 4, "color": "#2C5F8A",
        "cover_url": "https://covers.openlibrary.org/b/id/10520305-M.jpg",
        "isbn": "9780525559474"
    },
    {
        "id": "b006", "title": "Project Hail Mary",
        "author": "Andy Weir", "genre": "Sci-Fi",
        "position": 5, "color": "#1A5C3A",
        "cover_url": "https://covers.openlibrary.org/b/id/11061960-M.jpg",
        "isbn": "9780593135204"
    },
    {
        "id": "b007", "title": "Normal People",
        "author": "Sally Rooney", "genre": "Fiction",
        "position": 6, "color": "#C4A35A",
        "cover_url": "https://covers.openlibrary.org/b/id/8954978-M.jpg",
        "isbn": "9781984822185"
    },
    {
        "id": "b008", "title": "The Alchemist",
        "author": "Paulo Coelho", "genre": "Fiction",
        "position": 7, "color": "#8B7355",
        "cover_url": "https://covers.openlibrary.org/b/id/8739009-M.jpg",
        "isbn": "9780062315007"
    },
    {
        "id": "b009", "title": "Sapiens",
        "author": "Yuval Noah Harari", "genre": "Non-Fiction",
        "position": 8, "color": "#4A4A4A",
        "cover_url": "https://covers.openlibrary.org/b/id/8406786-M.jpg",
        "isbn": "9780062316097"
    },
    {
        "id": "b010", "title": "The Hitchhiker's Guide",
        "author": "Douglas Adams", "genre": "Sci-Fi",
        "position": 9, "color": "#2E4A7A",
        "cover_url": "https://covers.openlibrary.org/b/id/8138516-M.jpg",
        "isbn": "9780345391803"
    },
    {
        "id": "b011", "title": "Atomic Habits",
        "author": "James Clear", "genre": "Self-Help",
        "position": 10, "color": "#CC6633",
        "cover_url": "https://covers.openlibrary.org/b/id/9257770-M.jpg",
        "isbn": "9780735211292"
    },
    {
        "id": "b012", "title": "1984",
        "author": "George Orwell", "genre": "Dystopian",
        "position": 11, "color": "#333333",
        "cover_url": "https://covers.openlibrary.org/b/id/7222246-M.jpg",
        "isbn": "9780451524935"
    },
    {
        "id": "b013", "title": "Where the Crawdads Sing",
        "author": "Delia Owens", "genre": "Fiction",
        "position": 12, "color": "#5C8A3A",
        "cover_url": "https://covers.openlibrary.org/b/id/8954623-M.jpg",
        "isbn": "9780735224292"
    },
    {
        "id": "b014", "title": "The Silent Patient",
        "author": "Alex Michaelides", "genre": "Thriller",
        "position": 13, "color": "#7A2C2C",
        "cover_url": "https://covers.openlibrary.org/b/id/8750272-M.jpg",
        "isbn": "9781250301697"
    },
    {
        "id": "b015", "title": "Klara and the Sun",
        "author": "Kazuo Ishiguro", "genre": "Sci-Fi",
        "position": 14, "color": "#E8D5A0",
        "cover_url": "https://covers.openlibrary.org/b/id/11076773-M.jpg",
        "isbn": "9780593318171"
    },
]

# Detected books on the scanned image
# Positions detected left-to-right correspond to spine bounding boxes
DEMO_DETECTED_BOOKS = [
    # Position 0: correct
    {
        "id": "det001", "book_id": "b001",
        "ocr_text": "Name of the Wind Rothfuss",
        "matched_title": "The Name of the Wind", "matched_author": "Patrick Rothfuss",
        "confidence": 0.95, "status": "correct",
        "bbox": {"x": 0.02, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 0, "expected_position": 0,
        "genre": "Fantasy", "color": "#6B3A2A",
        "cover_url": "https://covers.openlibrary.org/b/id/8739161-M.jpg"
    },
    # Position 1: MISPLACED — Dune is in position 1 but should be position 2 (after Educated)
    {
        "id": "det002", "book_id": "b002",
        "ocr_text": "DUNE Herbert",
        "matched_title": "Dune", "matched_author": "Frank Herbert",
        "confidence": 0.97, "status": "misplaced",
        "bbox": {"x": 0.078, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 1, "expected_position": 5,
        "genre": "Sci-Fi", "color": "#C4914B",
        "cover_url": "https://covers.openlibrary.org/b/id/8225277-M.jpg"
    },
    # Position 2: correct
    {
        "id": "det003", "book_id": "b003",
        "ocr_text": "Educated Westover",
        "matched_title": "Educated", "matched_author": "Tara Westover",
        "confidence": 0.91, "status": "correct",
        "bbox": {"x": 0.136, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 2, "expected_position": 2,
        "genre": "Memoir", "color": "#3D6B8C",
        "cover_url": "https://covers.openlibrary.org/b/id/8739045-M.jpg"
    },
    # Position 3: correct
    {
        "id": "det004", "book_id": "b004",
        "ocr_text": "CIRCE Miller",
        "matched_title": "Circe", "matched_author": "Madeline Miller",
        "confidence": 0.98, "status": "correct",
        "bbox": {"x": 0.194, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 3, "expected_position": 3,
        "genre": "Fantasy", "color": "#8B4513",
        "cover_url": "https://covers.openlibrary.org/b/id/8739098-M.jpg"
    },
    # Position 4: correct
    {
        "id": "det005", "book_id": "b005",
        "ocr_text": "Midnight Library Haig",
        "matched_title": "The Midnight Library", "matched_author": "Matt Haig",
        "confidence": 0.89, "status": "correct",
        "bbox": {"x": 0.252, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 4, "expected_position": 4,
        "genre": "Fiction", "color": "#2C5F8A",
        "cover_url": "https://covers.openlibrary.org/b/id/10520305-M.jpg"
    },
    # Position 5: MISPLACED — Project Hail Mary should be at position 5 but is at 8
    {
        "id": "det006", "book_id": "b007",
        "ocr_text": "Normal People Rooney",
        "matched_title": "Normal People", "matched_author": "Sally Rooney",
        "confidence": 0.93, "status": "misplaced",
        "bbox": {"x": 0.310, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 5, "expected_position": 6,
        "genre": "Fiction", "color": "#C4A35A",
        "cover_url": "https://covers.openlibrary.org/b/id/8954978-M.jpg"
    },
    # Position 6: correct
    {
        "id": "det007", "book_id": "b008",
        "ocr_text": "Alchemist Coelho",
        "matched_title": "The Alchemist", "matched_author": "Paulo Coelho",
        "confidence": 0.94, "status": "correct",
        "bbox": {"x": 0.368, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 6, "expected_position": 7,
        "genre": "Fiction", "color": "#8B7355",
        "cover_url": "https://covers.openlibrary.org/b/id/8739009-M.jpg"
    },
    # Position 7: correct
    {
        "id": "det008", "book_id": "b009",
        "ocr_text": "SAPIENS Harari",
        "matched_title": "Sapiens", "matched_author": "Yuval Noah Harari",
        "confidence": 0.96, "status": "correct",
        "bbox": {"x": 0.426, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 7, "expected_position": 8,
        "genre": "Non-Fiction", "color": "#4A4A4A",
        "cover_url": "https://covers.openlibrary.org/b/id/8406786-M.jpg"
    },
    # Position 8: MISPLACED — Project Hail Mary here instead
    {
        "id": "det009", "book_id": "b006",
        "ocr_text": "Project Hail Mary Weir",
        "matched_title": "Project Hail Mary", "matched_author": "Andy Weir",
        "confidence": 0.92, "status": "misplaced",
        "bbox": {"x": 0.484, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 8, "expected_position": 5,
        "genre": "Sci-Fi", "color": "#1A5C3A",
        "cover_url": "https://covers.openlibrary.org/b/id/11061960-M.jpg"
    },
    # Position 9: correct
    {
        "id": "det010", "book_id": "b010",
        "ocr_text": "Hitchhiker Guide Adams",
        "matched_title": "The Hitchhiker's Guide", "matched_author": "Douglas Adams",
        "confidence": 0.88, "status": "correct",
        "bbox": {"x": 0.542, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 9, "expected_position": 9,
        "genre": "Sci-Fi", "color": "#2E4A7A",
        "cover_url": "https://covers.openlibrary.org/b/id/8138516-M.jpg"
    },
    # Position 10: correct
    {
        "id": "det011", "book_id": "b011",
        "ocr_text": "Atomic Habits Clear",
        "matched_title": "Atomic Habits", "matched_author": "James Clear",
        "confidence": 0.97, "status": "correct",
        "bbox": {"x": 0.600, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 10, "expected_position": 10,
        "genre": "Self-Help", "color": "#CC6633",
        "cover_url": "https://covers.openlibrary.org/b/id/9257770-M.jpg"
    },
    # Position 11: correct
    {
        "id": "det012", "book_id": "b012",
        "ocr_text": "1984 Orwell",
        "matched_title": "1984", "matched_author": "George Orwell",
        "confidence": 0.99, "status": "correct",
        "bbox": {"x": 0.658, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 11, "expected_position": 11,
        "genre": "Dystopian", "color": "#333333",
        "cover_url": "https://covers.openlibrary.org/b/id/7222246-M.jpg"
    },
    # Position 12: correct
    {
        "id": "det013", "book_id": "b013",
        "ocr_text": "Crawdads Sing Owens",
        "matched_title": "Where the Crawdads Sing", "matched_author": "Delia Owens",
        "confidence": 0.90, "status": "correct",
        "bbox": {"x": 0.716, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 12, "expected_position": 12,
        "genre": "Fiction", "color": "#5C8A3A",
        "cover_url": "https://covers.openlibrary.org/b/id/8954623-M.jpg"
    },
    # Position 13: correct
    {
        "id": "det014", "book_id": "b014",
        "ocr_text": "Silent Patient Michaelides",
        "matched_title": "The Silent Patient", "matched_author": "Alex Michaelides",
        "confidence": 0.93, "status": "correct",
        "bbox": {"x": 0.774, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 13, "expected_position": 13,
        "genre": "Thriller", "color": "#7A2C2C",
        "cover_url": "https://covers.openlibrary.org/b/id/8750272-M.jpg"
    },
    # Position 14: correct
    {
        "id": "det015", "book_id": "b015",
        "ocr_text": "Klara and the Sun Ishiguro",
        "matched_title": "Klara and the Sun", "matched_author": "Kazuo Ishiguro",
        "confidence": 0.91, "status": "correct",
        "bbox": {"x": 0.832, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": 14, "expected_position": 14,
        "genre": "Sci-Fi", "color": "#E8D5A0",
        "cover_url": "https://covers.openlibrary.org/b/id/11076773-M.jpg"
    },
    # MISSING: "The Silent Patient" ghost — actually represented above, so add a second missing
    # This represents a book expected on shelf but not found in the scan
    {
        "id": "det016", "book_id": None,
        "ocr_text": "",
        "matched_title": "The Hitchhiker's Guide to the Galaxy (Extended)", "matched_author": "Douglas Adams",
        "confidence": 0.0, "status": "missing",
        "bbox": {"x": 0.890, "y": 0.08, "w": 0.055, "h": 0.82},
        "detected_position": -1, "expected_position": 15,
        "genre": "Sci-Fi", "color": "#2E4A7A",
        "cover_url": "https://covers.openlibrary.org/b/id/8138516-M.jpg"
    },
]

DEMO_SHELF_SCORE = 81.25
DEMO_SHELF_NAME = "Main Shelf"
