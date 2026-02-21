"""Ranking service — وين نروح بالرياض."""

from __future__ import annotations

import math
from typing import Optional


def score_place(
    place: dict,
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None,
) -> float:
    """Calculate a composite score for ranking.

    Factors:
    - Google rating (0-5) → weight 0.4
    - Trending bonus → weight 0.2
    - New bonus → weight 0.1
    - Distance penalty (if location provided) → weight 0.3
    """
    rating = place.get("google_rating") or 0.0
    rating_score = (rating / 5.0) * 0.4

    trending_score = 0.2 if place.get("trending") else 0.0
    new_score = 0.1 if place.get("is_new") else 0.0

    distance_score = 0.3  # Default full score if no location
    if user_lat and user_lng and place.get("lat") and place.get("lng"):
        dist = _haversine(user_lat, user_lng, place["lat"], place["lng"])
        # Normalize: 0 km = 1.0, 20+ km = 0.0
        distance_score = max(0, (1.0 - dist / 20.0)) * 0.3

    return rating_score + trending_score + new_score + distance_score


def _haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine distance in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def rank_places(
    places: list[dict],
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None,
) -> list[dict]:
    """Sort places by composite score (descending)."""
    scored = [(p, score_place(p, user_lat, user_lng)) for p in places]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored]
