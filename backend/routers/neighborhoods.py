"""Neighborhoods router — وين نروح بالرياض."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, Request

from database import get_connection, row_to_dict
from cache import neighborhood_cache, get_precomputed, compute_etag
from models import NeighborhoodInfo, NeighborhoodTopPlaces, PlaceSummary

router = APIRouter(prefix="/api/v1/neighborhoods", tags=["neighborhoods"])


@router.get("", response_model=list[NeighborhoodInfo])
def list_neighborhoods(request: Request, response: Response):
    """List all neighborhoods with place counts."""
    cached = neighborhood_cache.get("all_neighborhoods")
    if cached:
        etag = compute_etag(cached)
        if request.headers.get("if-none-match") == etag:
            return Response(status_code=304)
        response.headers["ETag"] = etag
        return cached

    precomputed = get_precomputed("neighborhoods")
    if precomputed:
        result = [
            {"name": n["neighborhood"], "name_en": n["neighborhood_en"], "place_count": n["cnt"]}
            for n in precomputed
        ]
        neighborhood_cache.set("all_neighborhoods", result)
        etag = compute_etag(result)
        response.headers["ETag"] = etag
        return result

    conn = get_connection()
    rows = conn.execute(
        """SELECT neighborhood as name, neighborhood_en as name_en, COUNT(*) as place_count
        FROM places WHERE neighborhood != ''
        GROUP BY neighborhood
        ORDER BY place_count DESC"""
    ).fetchall()

    result = [dict(r) for r in rows]
    neighborhood_cache.set("all_neighborhoods", result)
    return result


@router.get("/{name}/top", response_model=NeighborhoodTopPlaces)
def top_places_in_neighborhood(name: str):
    """Top 10 places in a neighborhood."""
    cache_key = f"top:{name}"
    cached = neighborhood_cache.get(cache_key)
    if cached:
        return cached

    # Check precomputed
    top_by_hood = get_precomputed("top_by_neighborhood") or {}
    if name in top_by_hood:
        hood_en = ""
        if top_by_hood[name]:
            hood_en = top_by_hood[name][0].get("neighborhood_en", "")
        result = {
            "neighborhood": name,
            "neighborhood_en": hood_en,
            "places": top_by_hood[name],
        }
        neighborhood_cache.set(cache_key, result)
        return result

    # Fallback: query directly
    conn = get_connection()
    rows = conn.execute(
        """SELECT * FROM places
        WHERE neighborhood = ?
        ORDER BY google_rating DESC, trending DESC
        LIMIT 10""",
        (name,),
    ).fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="الحي مو موجود أو ما فيه أماكن")

    places = [row_to_dict(r) for r in rows]
    hood_en = places[0].get("neighborhood_en", "") if places else ""
    result = {
        "neighborhood": name,
        "neighborhood_en": hood_en,
        "places": places,
    }
    neighborhood_cache.set(cache_key, result)
    return result
