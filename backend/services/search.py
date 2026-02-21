"""Arabic search with normalization + FTS5 — وين نروح بالرياض."""

from __future__ import annotations

import re
import sqlite3
from typing import Optional

from database import row_to_dict


# ── Arabic Normalization ────────────────────────────────────────────

# Hamza normalization: إأآا → ا
_HAMZA_MAP = str.maketrans({
    "\u0622": "\u0627",  # آ → ا
    "\u0623": "\u0627",  # أ → ا
    "\u0625": "\u0627",  # إ → ا
    "\u0671": "\u0627",  # ٱ → ا
})

# Tashkeel (diacritics) pattern
_TASHKEEL = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7-\u06E8\u06EA-\u06ED]")

# Tatweel (kashida)
_TATWEEL = re.compile(r"\u0640")

# Final ة → ه  (optional, helps matching)
_TAA_MARBUTA = str.maketrans({"\u0629": "\u0647"})

# Remove extra whitespace
_MULTI_SPACE = re.compile(r"\s+")


def normalize_arabic(text: str) -> str:
    """Normalize Arabic text for search matching."""
    if not text:
        return ""
    text = text.translate(_HAMZA_MAP)
    text = _TASHKEEL.sub("", text)
    text = _TATWEEL.sub("", text)
    text = text.translate(_TAA_MARBUTA)
    text = _MULTI_SPACE.sub(" ", text).strip()
    return text


def build_fts_query(query: str) -> str:
    """Build FTS5 query from user input.

    Handles:
    - Arabic normalization
    - Multi-word → AND logic
    - Prefix matching with *
    """
    normalized = normalize_arabic(query)
    # Split into words, add prefix matching
    words = normalized.split()
    if not words:
        return ""

    # Each word gets prefix matching for partial search
    parts = []
    for w in words:
        # Escape special FTS5 characters
        w = w.replace('"', '""')
        parts.append(f'"{w}"*')

    return " AND ".join(parts)


def search_places(
    conn: sqlite3.Connection,
    query: str,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """Full-text search using FTS5 with Arabic normalization."""
    fts_query = build_fts_query(query)
    if not fts_query:
        return [], 0

    # Count total
    count_row = conn.execute(
        "SELECT COUNT(*) as cnt FROM places_fts WHERE places_fts MATCH ?",
        (fts_query,),
    ).fetchone()
    total = count_row["cnt"] if count_row else 0

    if total == 0:
        # Fallback: LIKE search on original text
        return _fallback_search(conn, query, limit, offset)

    # Fetch matching IDs from FTS, then join with main table
    rows = conn.execute(
        """SELECT p.* FROM places p
        INNER JOIN places_fts fts ON p.id = fts.id
        WHERE places_fts MATCH ?
        ORDER BY rank
        LIMIT ? OFFSET ?""",
        (fts_query, limit, offset),
    ).fetchall()

    results = [row_to_dict(r) for r in rows]
    return results, total


def _fallback_search(
    conn: sqlite3.Connection,
    query: str,
    limit: int,
    offset: int,
) -> tuple[list[dict], int]:
    """Fallback LIKE search when FTS doesn't match."""
    normalized = normalize_arabic(query)
    like_pattern = f"%{normalized}%"

    count_row = conn.execute(
        """SELECT COUNT(*) as cnt FROM places
        WHERE name_ar LIKE ? OR name_en LIKE ?
        OR description_ar LIKE ? OR category LIKE ?
        OR neighborhood LIKE ?""",
        (like_pattern, like_pattern, like_pattern, like_pattern, like_pattern),
    ).fetchone()
    total = count_row["cnt"] if count_row else 0

    rows = conn.execute(
        """SELECT * FROM places
        WHERE name_ar LIKE ? OR name_en LIKE ?
        OR description_ar LIKE ? OR category LIKE ?
        OR neighborhood LIKE ?
        ORDER BY google_rating DESC
        LIMIT ? OFFSET ?""",
        (like_pattern, like_pattern, like_pattern, like_pattern, like_pattern, limit, offset),
    ).fetchall()

    return [row_to_dict(r) for r in rows], total
