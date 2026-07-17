# 📚 Shelfie — AI Bookshelf Scanner

> Scan your shelf. Watch the AI think. Get a satisfying fix-it plan.

Shelfie turns a photo of your bookshelf into an interactive, gamified organization assistant. Upload a photo (or use the demo), watch an animated scan sequence, then get a step-by-step reorder plan with shelf health stats.

---

## Project Structure

```
AIBOOK/
├── backend/      # FastAPI + SQLite
├── frontend/     # React + TypeScript + Vite
└── README.md
```

---

## Quick Start

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |
| Tesseract OCR | Optional (only for real pipeline) |

### 1. Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000  
API docs (Swagger): http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## Environment Variables

Copy `.env.example` to `.env` in the `backend/` directory:

```bash
cp .env.example backend/.env
```

| Variable | Default | Description |
|---|---|---|
| `USE_DEMO_DATA` | `true` | Skip real OCR, use pre-baked demo response |
| `GOOGLE_BOOKS_API_KEY` | *(empty)* | Optional — Open Library works without a key |
| `DATABASE_URL` | `sqlite:///./app/data/shelfie.db` | SQLite DB path |
| `TESSERACT_CMD` | `tesseract` | Path to Tesseract binary |

> **Note:** With `USE_DEMO_DATA=true` (the default), the app delivers the full interactive experience without needing Tesseract or any API keys. Perfect for demos!

---

## Demo Mode

The default `USE_DEMO_DATA=true` flag activates a pre-baked detection response with:
- **15 books** detected on a shelf
- **3 misplaced** (amber), **1 missing** (red ghost), **11 correct** (green)
- **82% shelf score**

This powers the full animated flow — scan line, bounding boxes, Fix My Shelf mode, and the dashboard — without any OCR running.

---

## Real Pipeline (Optional)

To enable actual spine detection + OCR:

1. Install Tesseract: https://github.com/tesseract-ocr/tesseract
2. Set `USE_DEMO_DATA=false` in your `.env`
3. Set `TESSERACT_CMD` to your Tesseract binary path if not on PATH

---

## Stretch Goals (scaffolded, not implemented)

- 🎥 Live camera feed with real-time bounding boxes
- 🎙️ Voice narration of fix steps
- 📤 Shareable shelf report as downloadable image
- 🗺️ Multi-shelf library map view

---

## Tech Stack

**Backend**: FastAPI · SQLite (SQLAlchemy) · Pydantic · OpenCV · pytesseract · httpx  
**Frontend**: React 18 · TypeScript · Vite · Framer Motion · Recharts · react-dropzone · canvas-confetti
