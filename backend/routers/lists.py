"""Shareable Lists router — وين نروح بالرياض."""

from __future__ import annotations

import secrets
import uuid

from fastapi import APIRouter, HTTPException

from database import get_connection, row_to_dict
from models import ShareableListCreate, ShareableListResponse

router = APIRouter(prefix="/api/v1/lists", tags=["lists"])


@router.post("", response_model=ShareableListResponse, status_code=201)
def create_list(payload: ShareableListCreate):
    """Create a shareable list of places."""
    conn = get_connection()

    # Verify all places exist
    placeholders = ",".join(["?"] * len(payload.place_ids))
    existing = conn.execute(
        f"SELECT id FROM places WHERE id IN ({placeholders})", payload.place_ids
    ).fetchall()
    existing_ids = {r["id"] for r in existing}
    missing = set(payload.place_ids) - existing_ids
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"أماكن مو موجودة: {', '.join(missing)}",
        )

    list_id = str(uuid.uuid4())
    share_code = secrets.token_urlsafe(8)

    conn.execute(
        "INSERT INTO lists (id, name, device_id, share_code) VALUES (?, ?, ?, ?)",
        (list_id, payload.name, payload.device_id, share_code),
    )

    for i, pid in enumerate(payload.place_ids):
        conn.execute(
            "INSERT INTO list_places (list_id, place_id, position) VALUES (?, ?, ?)",
            (list_id, pid, i),
        )

    conn.commit()

    # Fetch the created list with places
    return _get_list_response(conn, list_id)


@router.get("/share/{share_code}", response_model=ShareableListResponse)
def get_list_by_share_code(share_code: str):
    """Get a list by its share code."""
    conn = get_connection()
    list_row = conn.execute(
        "SELECT * FROM lists WHERE share_code = ?", (share_code,)
    ).fetchone()

    if not list_row:
        raise HTTPException(status_code=404, detail="القائمة مو موجودة")

    return _get_list_response(conn, list_row["id"])


@router.get("/{device_id}", response_model=list[ShareableListResponse])
def get_device_lists(device_id: str):
    """Get all lists for a device."""
    conn = get_connection()
    list_rows = conn.execute(
        "SELECT * FROM lists WHERE device_id = ? ORDER BY created_at DESC",
        (device_id,),
    ).fetchall()

    return [_get_list_response(conn, r["id"]) for r in list_rows]


def _get_list_response(conn, list_id: str) -> dict:
    list_row = conn.execute("SELECT * FROM lists WHERE id = ?", (list_id,)).fetchone()
    if not list_row:
        raise HTTPException(status_code=404, detail="القائمة مو موجودة")

    place_rows = conn.execute(
        """SELECT p.* FROM places p
        INNER JOIN list_places lp ON p.id = lp.place_id
        WHERE lp.list_id = ?
        ORDER BY lp.position""",
        (list_id,),
    ).fetchall()

    return {
        "id": list_row["id"],
        "name": list_row["name"],
        "device_id": list_row["device_id"],
        "places": [row_to_dict(r) for r in place_rows],
        "share_code": list_row["share_code"],
        "created_at": str(list_row["created_at"]),
    }
