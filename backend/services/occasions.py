"""Occasion-based filtering — وين نروح بالرياض."""

from __future__ import annotations

import json
import sqlite3
from typing import Optional

from cache import get_precomputed, occasion_cache
from database import row_to_dict


# Category hints per occasion type
OCCASION_CATEGORIES: dict[str, list[str]] = {
    "romantic": ["مطعم", "كافيه", "فنادق"],
    "family": ["ترفيه", "مطعم", "طبيعة", "حدائق", "مولات"],
    "business": ["كافيه", "مطعم", "فنادق"],
    "friends": ["مطعم", "كافيه", "ترفيه", "رياضة"],
    "quiet": ["كافيه", "طبيعة", "متاحف"],
}


def get_occasion_places(
    conn: sqlite3.Connection,
    occasion_type: str,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """Get places suitable for an occasion type."""
    cache_key = f"occasion:{occasion_type}:{limit}:{offset}"
    cached = occasion_cache.get(cache_key)
    if cached:
        return cached

    keywords = get_precomputed("occasion_keywords") or {}
    kw_list = keywords.get(occasion_type, [])
    categories = OCCASION_CATEGORIES.get(occasion_type, [])

    if not kw_list and not categories:
        return [], 0

    # Build query: match perfect_for keywords OR audience OR category
    conditions = []
    params: list = []

    for kw in kw_list:
        conditions.append("perfect_for LIKE ?")
        params.append(f"%{kw}%")
        conditions.append("audience LIKE ?")
        params.append(f"%{kw}%")

    for cat in categories:
        conditions.append("category = ?")
        params.append(cat)

    where = " OR ".join(conditions)

    count_row = conn.execute(
        f"SELECT COUNT(*) as cnt FROM places WHERE {where}", params
    ).fetchone()
    total = count_row["cnt"] if count_row else 0

    rows = conn.execute(
        f"""SELECT * FROM places WHERE {where}
        ORDER BY google_rating DESC
        LIMIT ? OFFSET ?""",
        params + [limit, offset],
    ).fetchall()

    result = [row_to_dict(r) for r in rows]
    occasion_cache.set(cache_key, (result, total))
    return result, total
