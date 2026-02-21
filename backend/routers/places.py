"""Places router — وين نروح بالرياض."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request, Response
from typing import Optional

from database import get_connection, row_to_dict
from cache import query_cache, compute_etag
from models import Place, PlaceList, PlaceSummary
from services.search import search_places

router = APIRouter(prefix="/api/v1/places", tags=["places"])


@router.get("", response_model=PlaceList)
def list_places(
    request: Request,
    response: Response,
    category: Optional[str] = Query(None, max_length=50),
    neighborhood: Optional[str] = Query(None, max_length=100),
    price: Optional[str] = Query(None, pattern=r"^(\$|\$\$|\$\$\$|\$\$\$\$)$"),
    rating_min: Optional[float] = Query(None, ge=0, le=5),
    is_free: Optional[bool] = None,
    page: int = Query(1, ge=1, le=1000),
    limit: int = Query(20, ge=1, le=100),
):
    """List places with filters."""
    cache_key = f"places:{category}:{neighborhood}:{price}:{rating_min}:{is_free}:{page}:{limit}"
    cached = query_cache.get(cache_key)

    if cached:
        etag = compute_etag(cached)
        if request.headers.get("if-none-match") == etag:
            return Response(status_code=304)
        response.headers["ETag"] = etag
        return cached

    conn = get_connection()
    conditions = []
    params: list = []

    if category:
        conditions.append("category = ?")
        params.append(category)
    if neighborhood:
        conditions.append("neighborhood = ?")
        params.append(neighborhood)
    if price:
        conditions.append("price_level = ?")
        params.append(price)
    if rating_min is not None:
        conditions.append("google_rating >= ?")
        params.append(rating_min)
    if is_free is not None:
        conditions.append("is_free = ?")
        params.append(1 if is_free else 0)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    offset = (page - 1) * limit

    count_row = conn.execute(
        f"SELECT COUNT(*) as cnt FROM places {where}", params
    ).fetchone()
    total = count_row["cnt"] if count_row else 0

    rows = conn.execute(
        f"""SELECT * FROM places {where}
        ORDER BY google_rating DESC
        LIMIT ? OFFSET ?""",
        params + [limit, offset],
    ).fetchall()

    places = [row_to_dict(r) for r in rows]
    result = {
        "places": places,
        "total": total,
        "page": page,
        "limit": limit,
        "has_next": (page * limit) < total,
    }

    query_cache.set(cache_key, result)
    etag = compute_etag(result)
    response.headers["ETag"] = etag

    return result


@router.get("/search", response_model=PlaceList)
def search(
    q: str = Query(..., min_length=1, max_length=200),
    page: int = Query(1, ge=1, le=1000),
    limit: int = Query(20, ge=1, le=100),
):
    """Arabic FTS5 search."""
    conn = get_connection()
    offset = (page - 1) * limit
    places, total = search_places(conn, q, limit=limit, offset=offset)

    return {
        "places": places,
        "total": total,
        "page": page,
        "limit": limit,
        "has_next": (page * limit) < total,
    }


@router.get("/{place_id}", response_model=Place)
def get_place(place_id: str):
    """Get single place by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM places WHERE id = ?", (place_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="المكان مو موجود")
    return row_to_dict(row)
