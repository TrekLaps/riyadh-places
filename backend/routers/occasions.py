"""Occasions router — وين نروح بالرياض."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from database import get_connection
from models import OccasionResponse
from services.occasions import get_occasion_places

router = APIRouter(prefix="/api/v1/occasions", tags=["occasions"])

VALID_OCCASIONS = {"romantic", "family", "business", "friends", "quiet"}


@router.get("/{occasion_type}", response_model=OccasionResponse)
def get_occasion(
    occasion_type: str,
    limit: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
):
    """Get places for a specific occasion type."""
    if occasion_type not in VALID_OCCASIONS:
        raise HTTPException(
            status_code=400,
            detail=f"نوع المناسبة غير صحيح. الخيارات: {', '.join(VALID_OCCASIONS)}",
        )

    conn = get_connection()
    offset = (page - 1) * limit
    places, total = get_occasion_places(conn, occasion_type, limit=limit, offset=offset)

    return {
        "occasion": occasion_type,
        "places": places,
        "total": total,
    }
