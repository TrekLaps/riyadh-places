"""SQLite database with FTS5 for Arabic search — وين نروح بالرياض."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

DATABASE_PATH = Path("./places.db")

_conn: Optional[sqlite3.Connection] = None


def get_connection() -> sqlite3.Connection:
    """Return the module-level synchronous connection (create if needed)."""
    global _conn
    if _conn is None:
        _conn = _create_connection(DATABASE_PATH)
    return _conn


def _create_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")  # 64 MB
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db(db_path: Path | None = None) -> sqlite3.Connection:
    """Create tables, indexes, and FTS5 virtual table."""
    global _conn, DATABASE_PATH
    if db_path:
        DATABASE_PATH = db_path
    _conn = _create_connection(DATABASE_PATH)
    conn = _conn

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS places (
            id TEXT PRIMARY KEY,
            name_ar TEXT NOT NULL,
            name_en TEXT NOT NULL,
            category TEXT NOT NULL,
            category_ar TEXT,
            category_en TEXT,
            neighborhood TEXT NOT NULL,
            neighborhood_en TEXT,
            description_ar TEXT,
            google_rating REAL,
            price_level TEXT,
            trending INTEGER DEFAULT 0,
            is_new INTEGER DEFAULT 0,
            sources TEXT,
            google_maps_url TEXT,
            district TEXT,
            perfect_for TEXT,
            lat REAL,
            lng REAL,
            is_free INTEGER DEFAULT 0,
            audience TEXT,
            price_range TEXT,
            tags TEXT,
            opening_hours TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_places_category ON places(category);
        CREATE INDEX IF NOT EXISTS idx_places_neighborhood ON places(neighborhood);
        CREATE INDEX IF NOT EXISTS idx_places_rating ON places(google_rating DESC);
        CREATE INDEX IF NOT EXISTS idx_places_trending ON places(trending);
        CREATE INDEX IF NOT EXISTS idx_places_is_new ON places(is_new);
        CREATE INDEX IF NOT EXISTS idx_places_category_rating ON places(category, google_rating DESC);
        CREATE INDEX IF NOT EXISTS idx_places_neighborhood_rating ON places(neighborhood, google_rating DESC);

        -- Favorites
        CREATE TABLE IF NOT EXISTS favorites (
            device_id TEXT NOT NULL,
            place_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (device_id, place_id),
            FOREIGN KEY (place_id) REFERENCES places(id)
        );
        CREATE INDEX IF NOT EXISTS idx_favorites_device ON favorites(device_id);

        -- Shareable lists
        CREATE TABLE IF NOT EXISTS lists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            device_id TEXT NOT NULL,
            share_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_lists_share_code ON lists(share_code);
        CREATE INDEX IF NOT EXISTS idx_lists_device ON lists(device_id);

        CREATE TABLE IF NOT EXISTS list_places (
            list_id TEXT NOT NULL,
            place_id TEXT NOT NULL,
            position INTEGER DEFAULT 0,
            PRIMARY KEY (list_id, place_id),
            FOREIGN KEY (list_id) REFERENCES lists(id),
            FOREIGN KEY (place_id) REFERENCES places(id)
        );
    """)

    # FTS5 virtual table for Arabic full-text search
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS places_fts USING fts5(
            id UNINDEXED,
            name_ar,
            name_en,
            description_ar,
            tags,
            category,
            neighborhood,
            tokenize='unicode61 remove_diacritics 2'
        )
    """)

    conn.commit()
    return conn


def insert_place(conn: sqlite3.Connection, place: dict) -> None:
    """Insert a single place into main table and FTS index."""
    conn.execute(
        """INSERT OR REPLACE INTO places
        (id, name_ar, name_en, category, category_ar, category_en,
         neighborhood, neighborhood_en, description_ar, google_rating,
         price_level, trending, is_new, sources, google_maps_url,
         district, perfect_for, lat, lng, is_free, audience,
         price_range, tags, opening_hours)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            place["id"],
            place.get("name_ar", ""),
            place.get("name_en", ""),
            place.get("category", ""),
            place.get("category_ar", ""),
            place.get("category_en", ""),
            place.get("neighborhood", ""),
            place.get("neighborhood_en", ""),
            place.get("description_ar", ""),
            place.get("google_rating"),
            place.get("price_level"),
            1 if place.get("trending") else 0,
            1 if place.get("is_new") else 0,
            json.dumps(place.get("sources", []), ensure_ascii=False),
            place.get("google_maps_url", ""),
            place.get("district", ""),
            json.dumps(place.get("perfect_for", []), ensure_ascii=False),
            place.get("lat"),
            place.get("lng"),
            1 if place.get("is_free") else 0,
            json.dumps(place.get("audience", []), ensure_ascii=False),
            place.get("price_range", ""),
            json.dumps(place.get("tags", []), ensure_ascii=False),
            place.get("opening_hours", ""),
        ),
    )


def insert_fts(conn: sqlite3.Connection, place: dict) -> None:
    """Insert into FTS5 index."""
    tags_str = " ".join(place.get("tags", []))
    conn.execute(
        """INSERT OR REPLACE INTO places_fts
        (id, name_ar, name_en, description_ar, tags, category, neighborhood)
        VALUES (?,?,?,?,?,?,?)""",
        (
            place["id"],
            place.get("name_ar", ""),
            place.get("name_en", ""),
            place.get("description_ar", ""),
            tags_str,
            place.get("category", ""),
            place.get("neighborhood", ""),
        ),
    )


def row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a plain dict with JSON fields parsed."""
    d = dict(row)
    for field in ("sources", "perfect_for", "audience", "tags"):
        if field in d and isinstance(d[field], str):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                d[field] = []
    # Convert int booleans back
    for field in ("trending", "is_new", "is_free"):
        if field in d:
            d[field] = bool(d[field])
    return d
