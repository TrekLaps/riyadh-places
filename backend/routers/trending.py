"""Trending router — وين نروح بالرياض."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response

from cache import get_precomputed, trending_cache, compute_etag
from database import get_connection, row_to_dict
from models import TrendingResponse

router = APIRouter(prefix="/api/v1/trending", tags=["trending"])


@router.get("", response_model=TrendingResponse)
def get_trending(request: Request, response: Response):
    """Get trending (hot + new) places."""
    cached = trending_cache.get("trending")
    if cached:
        etag = compute_etag(cached)
        if request.headers.get("if-none-match") == etag:
            return Response(status_code=304)
        response.headers["ETag"] = etag
        return cached

    hot = get_precomputed("trending_hot")
    new = get_precomputed("trending_new")

    if hot is not None and new is not None:
        result = {"hot": hot, "new": new}
        trending_cache.set("trending", result)
        etag = compute_etag(result)
        response.headers["ETag"] = etag
        return result

    # Fallback
    conn = get_connection()
    hot_rows = conn.execute(
        "SELECT * FROM places WHERE trending = 1 ORDER BY google_rating DESC LIMIT 30"
    ).fetchall()
    new_rows = conn.execute(
        "SELECT * FROM places WHERE is_new = 1 ORDER BY google_rating DESC LIMIT 30"
    ).fetchall()

    result = {
        "hot": [row_to_dict(r) for r in hot_rows],
        "new": [row_to_dict(r) for r in new_rows],
    }
    trending_cache.set("trending", result)
    return result
