"""In-memory LRU cache with TTL + pre-computed views — وين نروح بالرياض."""

from __future__ import annotations

import hashlib
import json
import time
from functools import lru_cache
from typing import Any, Optional

import sqlite3

# ── TTL Cache ───────────────────────────────────────────────────────


class TTLCache:
    """Simple in-memory cache with TTL expiration."""

    def __init__(self, ttl_seconds: int = 300, max_size: int = 1000):
        self._store: dict[str, tuple[float, Any]] = {}
        self._ttl = ttl_seconds
        self._max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            ts, value = self._store[key]
            if time.time() - ts < self._ttl:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any) -> None:
        # Evict oldest if full
        if len(self._store) >= self._max_size:
            oldest_key = min(self._store, key=lambda k: self._store[k][0])
            del self._store[oldest_key]
        self._store[key] = (time.time(), value)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()


# ── Global caches ───────────────────────────────────────────────────

query_cache = TTLCache(ttl_seconds=300, max_size=500)
neighborhood_cache = TTLCache(ttl_seconds=600, max_size=100)
occasion_cache = TTLCache(ttl_seconds=600, max_size=50)
trending_cache = TTLCache(ttl_seconds=120, max_size=10)


# ── Pre-computed views ──────────────────────────────────────────────


_precomputed: dict[str, Any] = {}


def precompute_views(conn: sqlite3.Connection) -> None:
    """Pre-compute top-10 per neighborhood, trending, and occasion data."""
    from database import row_to_dict

    # Top 10 per neighborhood
    neighborhoods = conn.execute(
        "SELECT DISTINCT neighborhood, neighborhood_en FROM places WHERE neighborhood != ''"
    ).fetchall()

    top_by_hood: dict[str, list[dict]] = {}
    for row in neighborhoods:
        hood = row["neighborhood"]
        places = conn.execute(
            """SELECT * FROM places
            WHERE neighborhood = ?
            ORDER BY google_rating DESC, trending DESC
            LIMIT 10""",
            (hood,),
        ).fetchall()
        top_by_hood[hood] = [row_to_dict(p) for p in places]

    _precomputed["top_by_neighborhood"] = top_by_hood

    # Trending: hot (trending=true) + new (is_new=true)
    hot = conn.execute(
        "SELECT * FROM places WHERE trending = 1 ORDER BY google_rating DESC LIMIT 30"
    ).fetchall()
    new = conn.execute(
        "SELECT * FROM places WHERE is_new = 1 ORDER BY google_rating DESC LIMIT 30"
    ).fetchall()
    _precomputed["trending_hot"] = [row_to_dict(p) for p in hot]
    _precomputed["trending_new"] = [row_to_dict(p) for p in new]

    # Occasion mappings
    _precomputed["occasions"] = _build_occasion_mappings(conn)

    # Neighborhood list
    hood_info = conn.execute(
        """SELECT neighborhood, neighborhood_en, COUNT(*) as cnt
        FROM places WHERE neighborhood != ''
        GROUP BY neighborhood
        ORDER BY cnt DESC"""
    ).fetchall()
    _precomputed["neighborhoods"] = [dict(r) for r in hood_info]


def _build_occasion_mappings(conn: sqlite3.Connection) -> dict[str, list[str]]:
    """Map occasion types to perfect_for keywords."""
    from database import row_to_dict

    occasion_keywords: dict[str, list[str]] = {
        "romantic": [
            "رومانسي", "أجواء رومانسية", "عشاء رومانسي",
            "سهرة رومانسية", "أزواج", "عرسان",
        ],
        "family": [
            "عوائل", "عائلات", "أطفال", "نزهة عائلية",
            "جلسات عائلية", "حفلات أطفال", "أنشطة أطفال",
            "ملاهي أطفال", "مناسبة عائلية",
        ],
        "business": [
            "أعمال", "عمل", "اجتماعات عمل", "غداء عمل",
            "مؤتمرات", "كافيه عمل", "كافيه دراسي",
        ],
        "friends": [
            "أصدقاء", "شباب", "تجمعات", "سهرة مع أصدقاء",
            "مزة مع أصدقاء", "غداء مع أصدقاء",
            "عشاء مع أصدقاء", "سهرة",
        ],
        "quiet": [
            "هادي", "هدوء", "استرخاء", "كافيه هادئ",
            "سهرة هادئة", "قراءة", "دراسة",
        ],
    }
    _precomputed["occasion_keywords"] = occasion_keywords
    return occasion_keywords


def get_precomputed(key: str) -> Any:
    return _precomputed.get(key)


# ── ETag ────────────────────────────────────────────────────────────


def compute_etag(data: Any) -> str:
    """Generate ETag from data content."""
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.md5(raw.encode()).hexdigest()
