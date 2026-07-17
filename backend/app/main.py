"""
Shelfie — AI Bookshelf Scanner
FastAPI main application entry point.
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.models.db import Base, engine, SessionLocal
from app.routers import scan, inventory, recommend, shelf_health

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all DB tables and seed demo data on startup."""
    Base.metadata.create_all(bind=engine)
    # Eagerly seed demo shelf
    db = SessionLocal()
    try:
        from app.routers.inventory import _ensure_demo_shelf
        _ensure_demo_shelf(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Shelfie API",
    description="AI-powered bookshelf scanner — turns a photo of a bookshelf into an organized library.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(scan.router)
app.include_router(inventory.router)
app.include_router(recommend.router)
app.include_router(shelf_health.router)


@app.get("/")
def root():
    return {
        "app": "Shelfie",
        "version": "1.0.0",
        "demo_mode": settings.use_demo_data,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok", "demo_mode": settings.use_demo_data}
