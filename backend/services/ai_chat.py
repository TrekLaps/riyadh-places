"""Rule-based AI chat بلهجة سعودية — وين نروح بالرياض.

Ready for OpenAI API integration later.
"""

from __future__ import annotations

import random
import re
import sqlite3
from typing import Optional

from database import row_to_dict
from services.search import normalize_arabic


# ── Pattern matching بالعربي السعودي ────────────────────────────────

# Category keywords
CATEGORY_PATTERNS: dict[str, list[str]] = {
    "كافيه": ["كافيه", "قهوة", "كوفي", "كابتشينو", "لاتيه", "اسبريسو", "مقهى"],
    "مطعم": ["مطعم", "اكل", "أكل", "غداء", "عشاء", "فطور", "برنش", "جوعان", "ابي اكل", "ابغى اكل"],
    "ترفيه": ["ترفيه", "مرح", "ألعاب", "العاب", "بولنق", "سينما", "كارتنق"],
    "طبيعة": ["طبيعة", "حديقة", "حدائق", "نزهة", "تنزه", "هايكنق"],
    "تسوق": ["تسوق", "شوبنق", "مول", "محلات"],
    "حلويات": ["حلويات", "حلى", "كيك", "دونات", "ايس كريم", "آيس كريم"],
    "شاليه": ["شاليه", "استراحة", "مسبح"],
    "متاحف": ["متحف", "متاحف", "تاريخ", "ثقافة", "فن"],
    "رياضة": ["رياضة", "جيم", "يوغا", "تسلق", "كروسفت"],
}

# Occasion patterns
OCCASION_PATTERNS: dict[str, list[str]] = {
    "romantic": ["رومانسي", "رومنسي", "زوجتي", "خطيبتي", "عشاء رومانسي", "مكان حلو مع"],
    "family": ["عائلة", "عائلتي", "عوائل", "اطفال", "أطفال", "اولادي", "أولادي"],
    "business": ["اجتماع", "عمل", "بزنس", "ميتنق"],
    "friends": ["ربعي", "اصدقاء", "أصدقاء", "الشباب", "سهرة", "طلعة"],
    "quiet": ["هدوء", "هادي", "ساكت", "استرخاء", "ريلاكس", "مذاكرة", "دراسة"],
}

# Neighborhood patterns (common ones)
NEIGHBORHOOD_PATTERNS: dict[str, list[str]] = {
    "حي العليا": ["العليا", "عليا", "التحلية"],
    "حي الملقا": ["الملقا", "ملقا"],
    "حي النخيل": ["النخيل", "نخيل"],
    "حي الورود": ["الورود", "ورود"],
    "حي السليمانية": ["السليمانية", "سليمانية"],
    "الدرعية": ["درعية", "الدرعية", "البجيري"],
    "حي الياسمين": ["الياسمين", "ياسمين"],
    "حي الرحمانية": ["الرحمانية", "رحمانية"],
    "حي الصحافة": ["الصحافة", "صحافة"],
    "حي الربيع": ["الربيع", "ربيع"],
}

# Price patterns
PRICE_PATTERNS: dict[str, list[str]] = {
    "$": ["رخيص", "اقتصادي", "رخيصة", "ببلاش", "مجاني"],
    "$$": ["متوسط", "معقول", "مناسب"],
    "$$$": ["فاخر", "غالي", "فخم", "راقي", "لاكشري"],
}

# Greeting patterns
GREETINGS = [
    "هلا", "السلام", "مرحبا", "هاي", "صباح", "مساء",
    "اهلا", "أهلا", "كيفك", "شخبارك",
]

# ── Response templates بلهجة سعودية ─────────────────────────────────

GREETING_RESPONSES = [
    "هلا والله! وش تبي تسوي اليوم بالرياض؟ 🏙️",
    "أهلين! قل لي وش تدور عليه وأنا أساعدك 😊",
    "يا هلا فيك! تبي مطعم، كافيه، ترفيه؟ قل لي وأنا حاضر 🎯",
    "مرحبا! أنا هنا أساعدك تلقى أحلى الأماكن بالرياض 🌟",
]

RESULT_INTROS = [
    "عندك كم خيار حلو 🔥",
    "لقيت لك أماكن تجنن ✨",
    "شف هالخيارات الحلوة 👌",
    "عندي لك اقتراحات روعة 🎯",
    "خذ هالأماكن المميزة 💎",
]

NO_RESULT_RESPONSES = [
    "ما لقيت شي بالضبط بس خلني أدور لك أكثر.. جرب تكون أوضح شوي 🤔",
    "للأسف ما طلع لي شي.. جرب تسأل بطريقة ثانية 😅",
    "ما عندي نتائج حالياً.. بس جرب تغير الكلمات شوي 🔄",
]

SUGGESTION_TEMPLATES = [
    "وش رايك بكافيه حلو؟ ☕",
    "تبي مطعم فاخر ولا شعبي؟ 🍽️",
    "ودك بمكان هادي ولا فيه حركة؟ 🎭",
    "تبي شي للعائلة؟ 👨‍👩‍👧‍👦",
    "جرب تسألني عن حي معين مثل العليا أو الملقا 📍",
]


# ── Main Chat Logic ─────────────────────────────────────────────────


def process_chat(
    conn: sqlite3.Connection,
    message: str,
    history: list[dict] | None = None,
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None,
) -> dict:
    """Process a chat message and return response with places.

    Returns: {reply: str, places: list[dict], suggestions: list[str]}
    """
    normalized = normalize_arabic(message.lower())

    # Check greeting
    if _is_greeting(normalized):
        return {
            "reply": random.choice(GREETING_RESPONSES),
            "places": [],
            "suggestions": random.sample(SUGGESTION_TEMPLATES, min(3, len(SUGGESTION_TEMPLATES))),
        }

    # Extract intent
    category = _extract_category(normalized)
    occasion = _extract_occasion(normalized)
    neighborhood = _extract_neighborhood(normalized)
    price = _extract_price(normalized)

    # Build query
    places = _query_places(conn, category, occasion, neighborhood, price)

    if places:
        # Limit to top 5
        top_places = places[:5]
        reply = _build_reply(top_places, category, occasion, neighborhood)
        suggestions = _build_suggestions(category, occasion, neighborhood)
        return {
            "reply": reply,
            "places": top_places,
            "suggestions": suggestions,
        }

    # No structured match — try FTS search
    from services.search import search_places
    search_results, total = search_places(conn, message, limit=5)
    if search_results:
        reply = f"{random.choice(RESULT_INTROS)}\n\nلقيت لك {total} مكان! هذي أفضلها:"
        return {
            "reply": reply,
            "places": search_results,
            "suggestions": random.sample(SUGGESTION_TEMPLATES, 2),
        }

    # No results at all
    return {
        "reply": random.choice(NO_RESULT_RESPONSES),
        "places": [],
        "suggestions": random.sample(SUGGESTION_TEMPLATES, 3),
    }


def _is_greeting(text: str) -> bool:
    words = text.split()
    return any(w in GREETINGS for w in words[:3])


def _extract_category(text: str) -> Optional[str]:
    for cat, keywords in CATEGORY_PATTERNS.items():
        if any(kw in text for kw in keywords):
            return cat
    return None


def _extract_occasion(text: str) -> Optional[str]:
    for occ, keywords in OCCASION_PATTERNS.items():
        if any(kw in text for kw in keywords):
            return occ
    return None


def _extract_neighborhood(text: str) -> Optional[str]:
    for hood, keywords in NEIGHBORHOOD_PATTERNS.items():
        if any(kw in text for kw in keywords):
            return hood
    return None


def _extract_price(text: str) -> Optional[str]:
    for price, keywords in PRICE_PATTERNS.items():
        if any(kw in text for kw in keywords):
            return price
    return None


def _query_places(
    conn: sqlite3.Connection,
    category: Optional[str],
    occasion: Optional[str],
    neighborhood: Optional[str],
    price: Optional[str],
) -> list[dict]:
    """Query places based on extracted filters."""
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

    if occasion:
        from services.occasions import OCCASION_CATEGORIES
        from cache import get_precomputed

        occasion_kws = (get_precomputed("occasion_keywords") or {}).get(occasion, [])
        occ_conditions = []
        for kw in occasion_kws:
            occ_conditions.append("perfect_for LIKE ?")
            params.append(f"%{kw}%")
            occ_conditions.append("audience LIKE ?")
            params.append(f"%{kw}%")

        cats = OCCASION_CATEGORIES.get(occasion, [])
        for cat in cats:
            occ_conditions.append("category = ?")
            params.append(cat)

        if occ_conditions:
            conditions.append(f"({' OR '.join(occ_conditions)})")

    if not conditions:
        return []

    where = " AND ".join(conditions)
    rows = conn.execute(
        f"""SELECT * FROM places WHERE {where}
        ORDER BY google_rating DESC
        LIMIT 20""",
        params,
    ).fetchall()

    return [row_to_dict(r) for r in rows]


def _build_reply(
    places: list[dict],
    category: Optional[str],
    occasion: Optional[str],
    neighborhood: Optional[str],
) -> str:
    """Build a Saudi-dialect reply."""
    intro = random.choice(RESULT_INTROS)

    parts = []
    if category:
        parts.append(f"أفضل {category}")
    if neighborhood:
        parts.append(f"بـ{neighborhood}")
    if occasion:
        occasion_ar = {
            "romantic": "لسهرة رومانسية 💕",
            "family": "للعائلة 👨‍👩‍👧‍👦",
            "business": "لاجتماع العمل 💼",
            "friends": "مع الربع 🤙",
            "quiet": "لجلسة هادية 🧘",
        }
        parts.append(occasion_ar.get(occasion, ""))

    context = " ".join(parts) if parts else ""

    lines = [f"{intro}"]
    if context:
        lines.append(context)
    lines.append("")

    for i, p in enumerate(places, 1):
        rating = f"⭐ {p.get('google_rating', 'N/A')}" if p.get('google_rating') else ""
        price = p.get('price_level', '')
        lines.append(f"{i}. **{p['name_ar']}** ({p['name_en']}) {rating} {price}")

    return "\n".join(lines)


def _build_suggestions(
    category: Optional[str],
    occasion: Optional[str],
    neighborhood: Optional[str],
) -> list[str]:
    """Build contextual follow-up suggestions."""
    suggestions = []

    if not neighborhood:
        suggestions.append("وش رايك نشوف بحي معين؟ 📍")
    if not occasion:
        suggestions.append("المناسبة وش هي؟ رومانسي، عائلي، مع الربع؟ 🎯")
    if category != "كافيه":
        suggestions.append("تبي كافيه بعد؟ ☕")
    if category != "مطعم":
        suggestions.append("ودك بمطعم؟ 🍽️")

    return suggestions[:3]
