"""FastAPI backend — وين نروح بالرياض.

Main application with CORS, Gzip, rate limiting, and lifespan management.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

load_dotenv()

# ── Config ──────────────────────────────────────────────────────────

DATABASE_PATH = os.getenv("DATABASE_PATH", "./places.db")
DATA_JSON_PATH = os.getenv("DATA_JSON_PATH", "../data/places.json")
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://wain-nrooh.com",
).split(",")
RATE_LIMIT = os.getenv("RATE_LIMIT", "60/minute")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# ── Rate Limiter ────────────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])


# ── Lifespan ────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load data → SQLite, pre-compute caches."""
    from database import init_db, get_connection
    from cache import precompute_views

    db_path = Path(DATABASE_PATH)

    # Initialize DB (creates tables if needed)
    conn = init_db(db_path)

    # Check if data needs importing
    count = conn.execute("SELECT COUNT(*) as cnt FROM places").fetchone()["cnt"]
    if count == 0:
        print("🔄 قاعدة البيانات فاضية — جاري الاستيراد...")
        from import_data import main as import_main
        import_main(DATA_JSON_PATH, DATABASE_PATH)
        # Reconnect after import
        conn = init_db(db_path)

    count = conn.execute("SELECT COUNT(*) as cnt FROM places").fetchone()["cnt"]
    print(f"✅ قاعدة البيانات جاهزة: {count} مكان")

    # Pre-compute caches
    print("🔄 حساب الكاش...")
    precompute_views(conn)
    print("✅ الكاش جاهز!")

    yield  # App is running

    # Shutdown
    conn.close()
    print("👋 تم إيقاف السيرفر")


# ── App ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="وين نروح بالرياض API",
    description="API لاكتشاف أفضل الأماكن بالرياض 🏙️",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if DEBUG else "/docs",
    redoc_url="/redoc" if DEBUG else None,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip
app.add_middleware(GZipMiddleware, minimum_size=500)


# ── Routers ─────────────────────────────────────────────────────────

from routers.places import router as places_router
from routers.neighborhoods import router as neighborhoods_router
from routers.occasions import router as occasions_router
from routers.trending import router as trending_router
from routers.favorites import router as favorites_router
from routers.lists import router as lists_router
from routers.ai import router as ai_router

app.include_router(places_router)
app.include_router(neighborhoods_router)
app.include_router(occasions_router)
app.include_router(trending_router)
app.include_router(favorites_router)
app.include_router(lists_router)
app.include_router(ai_router)


# ── Health ──────────────────────────────────────────────────────────


@app.get("/health")
def health_check():
    from database import get_connection
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) as cnt FROM places").fetchone()["cnt"]
    return {
        "status": "ok",
        "version": "1.0.0",
        "places_count": count,
        "database": "connected",
    }


@app.get("/")
def root():
    return {
        "app": "وين نروح بالرياض",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# ── Run ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        workers=int(os.getenv("WORKERS", "4")),
        reload=DEBUG,
    )
