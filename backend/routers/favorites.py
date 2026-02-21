"""Favorites router — وين نروح بالرياض."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from database import get_connection, row_to_dict
from models import FavoriteAction, FavoriteList

router = APIRouter(prefix="/api/v1/favorites", tags=["favorites"])


@router.post("", status_code=201)
def add_favorite(action: FavoriteAction):
    """Add a place to favorites."""
    conn = get_connection()

    # Verify place exists
    place = conn.execute("SELECT id FROM places WHERE id = ?", (action.place_id,)).fetchone()
    if not place:
        raise HTTPException(status_code=404, detail="المكان مو موجود")

    try:
        conn.execute(
            "INSERT OR IGNORE INTO favorites (device_id, place_id) VALUES (?, ?)",
            (action.device_id, action.place_id),
        )
        conn.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="خطأ في حفظ المفضلة")

    return {"status": "ok", "message": "تمت الإضافة للمفضلة ⭐"}


@router.delete("")
def remove_favorite(action: FavoriteAction):
    """Remove a place from favorites."""
    conn = get_connection()
    conn.execute(
        "DELETE FROM favorites WHERE device_id = ? AND place_id = ?",
        (action.device_id, action.place_id),
    )
    conn.commit()
    return {"status": "ok", "message": "تم الحذف من المفضلة"}


@router.get("/{device_id}", response_model=FavoriteList)
def get_favorites(device_id: str):
    """Get all favorites for a device."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT p.* FROM places p
        INNER JOIN favorites f ON p.id = f.place_id
        WHERE f.device_id = ?
        ORDER BY f.created_at DESC""",
        (device_id,),
    ).fetchall()

    places = [row_to_dict(r) for r in rows]
    return {
        "device_id": device_id,
        "favorites": places,
        "total": len(places),
    }
