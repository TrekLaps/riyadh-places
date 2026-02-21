"""AI Chat router — وين نروح بالرياض."""

from __future__ import annotations

from fastapi import APIRouter

from database import get_connection
from models import ChatRequest, ChatResponse
from services.ai_chat import process_chat

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    """AI-powered chat for place recommendations.

    Currently rule-based with Saudi dialect responses.
    Ready for OpenAI API integration.
    """
    conn = get_connection()

    user_lat = payload.location.lat if payload.location else None
    user_lng = payload.location.lng if payload.location else None

    history = [{"role": m.role, "content": m.content} for m in payload.history]

    result = process_chat(
        conn=conn,
        message=payload.message,
        history=history,
        user_lat=user_lat,
        user_lng=user_lng,
    )

    return result
