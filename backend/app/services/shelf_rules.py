"""
Shelf rules service.
Determines the correct order for books on a shelf based on sort rules,
then computes which books are correct, misplaced, or missing.
"""
from typing import List, Dict, Optional


def compute_correct_order(books: List[Dict], sort_rule: str) -> List[Dict]:
    """
    Given a list of book dicts, return them sorted according to sort_rule.
    Each book dict should have: id, title, author, genre, position, dewey_number (optional).
    Returns a new list with updated 'position' fields.
    """
    sorted_books = list(books)

    if sort_rule == "alphabetical":
        sorted_books.sort(key=lambda b: (b.get("author", "").split()[-1] if b.get("author") else "zzz", b.get("title", "")))
    elif sort_rule == "genre":
        sorted_books.sort(key=lambda b: (b.get("genre", "Unknown"), b.get("author", ""), b.get("title", "")))
    elif sort_rule == "dewey":
        sorted_books.sort(key=lambda b: float(b.get("dewey_number", 999)))
    elif sort_rule == "custom":
        sorted_books.sort(key=lambda b: b.get("position", 9999))

    for idx, book in enumerate(sorted_books):
        book["expected_position"] = idx

    return sorted_books


def compute_book_statuses(
    detected_books: List[Dict],
    inventory: List[Dict],
    sort_rule: str = "alphabetical",
) -> List[Dict]:
    """
    For each detected book, compare its detected_position to its expected_position
    under the given sort_rule, and assign a status.

    Returns the detected_books list with 'status' and 'expected_position' filled in.
    """
    sorted_inventory = compute_correct_order(list(inventory), sort_rule)
    expected_pos_by_id = {b["id"]: b["expected_position"] for b in sorted_inventory}

    for det in detected_books:
        book_id = det.get("book_id")
        if not book_id:
            det["status"] = "unknown"
            continue

        expected = expected_pos_by_id.get(book_id, -1)
        detected = det.get("detected_position", -1)

        if expected == -1:
            det["status"] = "unknown"
        elif detected == -1:
            det["status"] = "missing"
        elif detected == expected:
            det["status"] = "correct"
        else:
            det["status"] = "misplaced"

        det["expected_position"] = expected

    return detected_books


def compute_shelf_score(detected_books: List[Dict]) -> float:
    """
    Shelf score = (correct / total_non_missing) * 100
    """
    total = [b for b in detected_books if b.get("status") != "missing"]
    if not total:
        return 0.0
    correct = [b for b in total if b.get("status") == "correct"]
    return round(len(correct) / len(total) * 100, 2)


def get_reorder_steps(detected_books: List[Dict], inventory: List[Dict], sort_rule: str = "alphabetical") -> List[Dict]:
    """
    Generate human-readable reorder instructions for misplaced books.
    Returns list of {book_id, title, from_pos, to_pos, instruction} dicts.
    """
    sorted_inventory = compute_correct_order(list(inventory), sort_rule)
    pos_to_title = {b["expected_position"]: b["title"] for b in sorted_inventory}

    steps = []
    for det in detected_books:
        if det.get("status") != "misplaced":
            continue

        from_pos = det.get("detected_position", -1)
        to_pos = det.get("expected_position", -1)
        title = det.get("matched_title", "Unknown")

        if from_pos == -1 or to_pos == -1:
            continue

        diff = to_pos - from_pos
        direction = "to the right" if diff > 0 else "to the left"
        spots = abs(diff)

        neighbor_left = pos_to_title.get(to_pos - 1)
        neighbor_right = pos_to_title.get(to_pos + 1)

        if neighbor_left and neighbor_right:
            between = f"between '{neighbor_left}' and '{neighbor_right}'"
        elif neighbor_left:
            between = f"after '{neighbor_left}'"
        elif neighbor_right:
            between = f"before '{neighbor_right}'"
        else:
            between = f"at position {to_pos + 1}"

        instruction = f"Move '{title}' {spots} spot{'s' if spots != 1 else ''} {direction} — {between}"

        steps.append({
            "book_id": det.get("book_id"),
            "title": title,
            "from_position": from_pos,
            "to_position": to_pos,
            "instruction": instruction,
            "neighbor_left": neighbor_left,
            "neighbor_right": neighbor_right,
        })

    steps.sort(key=lambda s: abs(s["to_position"] - s["from_position"]), reverse=True)
    return steps
