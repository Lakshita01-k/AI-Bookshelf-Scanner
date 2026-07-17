"""
Spine detector service.
Real pipeline: OpenCV contour detection to find vertical spine regions.
Returns normalized bounding boxes (0-1 relative to image dimensions).
"""
import cv2
import numpy as np
from typing import List, Dict


def detect_spines(image_bytes: bytes) -> List[Dict]:
    """
    Detect book spines in an image using OpenCV contour detection.
    Returns list of normalized bounding boxes: [{x, y, w, h}, ...]
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        return []

    height, width = img.shape[:2]

    # Convert to grayscale and apply edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Dilate edges to connect nearby lines (book spines tend to have vertical edges)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 15))
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    spine_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = h / w if w > 0 else 0

        # Filter: spines are tall and narrow, with significant area
        if aspect_ratio > 2.0 and area > (width * height * 0.005):
            spine_boxes.append({
                "x": x / width,
                "y": y / height,
                "w": w / width,
                "h": h / height,
            })

    # Sort left to right
    spine_boxes.sort(key=lambda b: b["x"])

    # Merge overlapping boxes
    merged = _merge_overlapping_boxes(spine_boxes)
    return merged


def _merge_overlapping_boxes(boxes: List[Dict], overlap_threshold: float = 0.3) -> List[Dict]:
    """Merge bounding boxes that overlap significantly (same spine detected twice)."""
    if not boxes:
        return []

    merged = []
    used = [False] * len(boxes)

    for i, box in enumerate(boxes):
        if used[i]:
            continue
        group = [box]
        for j, other in enumerate(boxes[i + 1:], start=i + 1):
            if used[j]:
                continue
            # Check horizontal overlap
            x_overlap = min(box["x"] + box["w"], other["x"] + other["w"]) - max(box["x"], other["x"])
            if x_overlap > overlap_threshold * min(box["w"], other["w"]):
                group.append(other)
                used[j] = True
        # Merge group into one box
        xs = [b["x"] for b in group]
        ys = [b["y"] for b in group]
        x2s = [b["x"] + b["w"] for b in group]
        y2s = [b["y"] + b["h"] for b in group]
        merged.append({
            "x": min(xs), "y": min(ys),
            "w": max(x2s) - min(xs), "h": max(y2s) - min(ys)
        })
        used[i] = True

    return merged


def crop_spine(image_bytes: bytes, bbox: Dict) -> bytes:
    """Crop a spine region from the image given a normalized bounding box."""
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        return b""

    h, w = img.shape[:2]
    x = int(bbox["x"] * w)
    y = int(bbox["y"] * h)
    bw = int(bbox["w"] * w)
    bh = int(bbox["h"] * h)

    cropped = img[y:y + bh, x:x + bw]
    _, buffer = cv2.imencode(".jpg", cropped)
    return buffer.tobytes()
