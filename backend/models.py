"""Pydantic models for وين نروح بالرياض API."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator
import re


# ── Input Sanitization ──────────────────────────────────────────────

_DANGEROUS_PATTERN = re.compile(r"[<>\"';\\]")


def _sanitize(v: str) -> str:
    """Strip dangerous characters from user input."""
    if v:
        v = _DANGEROUS_PATTERN.sub("", v).strip()
    return v


# ── Place Models ────────────────────────────────────────────────────


class PlaceSummary(BaseModel):
    id: str
    name_ar: str
    name_en: str
    category: str
    category_en: str
    neighborhood: str
    neighborhood_en: str
    google_rating: Optional[float] = None
    price_level: Optional[str] = None
    trending: bool = False
    is_new: bool = False
    lat: Optional[float] = None
    lng: Optional[float] = None
    is_free: bool = False
    google_maps_url: Optional[str] = None


class Place(PlaceSummary):
    description_ar: Optional[str] = None
    district: Optional[str] = None
    perfect_for: list[str] = Field(default_factory=list)
    audience: list[str] = Field(default_factory=list)
    price_range: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    opening_hours: Optional[str] = None


class PlaceList(BaseModel):
    places: list[PlaceSummary]
    total: int
    page: int
    limit: int
    has_next: bool


# ── Neighborhood ────────────────────────────────────────────────────


class NeighborhoodInfo(BaseModel):
    name: str
    name_en: str
    place_count: int


class NeighborhoodTopPlaces(BaseModel):
    neighborhood: str
    neighborhood_en: str
    places: list[PlaceSummary]


# ── Occasion ────────────────────────────────────────────────────────


class OccasionResponse(BaseModel):
    occasion: str
    places: list[PlaceSummary]
    total: int


# ── Trending ────────────────────────────────────────────────────────


class TrendingResponse(BaseModel):
    hot: list[PlaceSummary]
    new: list[PlaceSummary]


# ── Favorites & Lists ──────────────────────────────────────────────


class FavoriteAction(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=128)
    place_id: str = Field(..., min_length=1, max_length=128)

    @field_validator("device_id", "place_id", mode="before")
    @classmethod
    def sanitize_ids(cls, v: str) -> str:
        return _sanitize(v)


class FavoriteList(BaseModel):
    device_id: str
    favorites: list[PlaceSummary]
    total: int


class ShareableListCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    device_id: str = Field(..., min_length=1, max_length=128)
    place_ids: list[str] = Field(..., min_items=1, max_length=50)

    @field_validator("name", mode="before")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        return _sanitize(v)


class ShareableListResponse(BaseModel):
    id: str
    name: str
    device_id: str
    places: list[PlaceSummary]
    share_code: str
    created_at: str


# ── AI Chat ─────────────────────────────────────────────────────────


class ChatMessage(BaseModel):
    role: str = Field(..., pattern=r"^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=2000)

    @field_validator("content", mode="before")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        return _sanitize(v)


class LocationInfo(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)
    device_id: str = Field(..., min_length=1, max_length=128)
    location: Optional[LocationInfo] = None

    @field_validator("message", mode="before")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        return _sanitize(v)


class ChatResponse(BaseModel):
    reply: str
    places: list[PlaceSummary] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


# ── Health ──────────────────────────────────────────────────────────


class HealthCheck(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    places_count: int = 0
    database: str = "connected"
