#!/usr/bin/env python3
"""
Batch enrichment script for Riyadh places.
Assigns price_range, tags, and fixes data quality issues.
Sources: TripAdvisor, Google Maps, Wanderlog research.
"""
import json
import os
from datetime import datetime

DATA_PATH = os.path.expanduser("~/workspace/projects/riyadh-places/data/places.json")
LOG_PATH = os.path.expanduser("~/workspace/projects/riyadh-places/data/enrichment-log.json")

with open(DATA_PATH) as f:
    data = json.load(f)

enriched_count = 0
changes = {"price_range": 0, "tags": 0, "google_rating_fix": 0}

# ============================================================
# 1. PRICE RANGE ASSIGNMENT (based on web research)
# ============================================================
# Known chains and their price levels from TripAdvisor/Google
KNOWN_PRICES = {
    # Cheap ($) - researched
    "ماكدونالز": "$", "McDonald's": "$", "mcdonalds": "$",
    "Al-Romansiah": "$", "الرومانسية": "$", "Romansiah": "$",
    "Al Romansiah": "$",
    "Hashim": "$", "Hashim Restaurant": "$",
    "Al Baik": "$", "البيك": "$",
    "Herfy": "$", "هرفي": "$",
    "Kudu": "$", "كودو": "$",
    "Shawarmer": "$", "شاورمر": "$",
    "Al Tazaj": "$", "التازج": "$",
    "Maestro Pizza": "$",
    "Little Caesars": "$",
    "Domino's": "$",
    "Burger King": "$",
    "KFC": "$",
    "Subway": "$",
    "Al Mansaf": "$",
    "عمو حمزة": "$",
    "Darbar Restaurant": "$",
    "Indonesian": "$",
    "alkhafeeh": "$",
    "Al Naqaa": "$",
    "Mahboob": "$",
    "مطعم باب توما": "$",
    "شيخ البلد": "$",
    "بر وسمن": "$",
    "سلامة": "$",
    "Al Omda": "$",
    "Mama Mashael": "$",

    # Moderate ($$) - researched
    "Firdays": "$$", "Friday's": "$$", "TGI Friday's": "$$",
    "Tony Roma's": "$$",
    "Buffalo": "$$", "Buffalo Wings": "$$",
    "Planet Hollywood": "$$",
    "Yamal Asham": "$$", "Yamal Al Sham": "$$",
    "Roma Restaurant": "$$",
    "Shiraz Restaurant (Iranian)": "$$",
    "Al Yamamah Restaurant": "$$",
    "Shanghai Express": "$$",
    "Aladdin": "$$",
    "Kany Restaurant": "$$",
    "Reyash": "$$",
    "Al Rabe'a": "$$",
    "Makani": "$$",
    "Al Khozana - Garden BBQ": "$$",
    "Ghawar": "$$",
    "Mensa": "$$",
    "Mthaq alromansi": "$$",
    "Abdel Wahab": "$$",

    # Upper moderate ($$$)
    "Quattro": "$$$",
    "Finzione": "$$$",
    "French Corner": "$$$",

    # Cafes - mostly $$
    "Java Time": "$$",
    "Seatle's Best": "$$", "Seattle's Best": "$$",
    "Krispy Kreme": "$", "Krespe Kreme Doughnuts": "$",
    "Baskin & Robbins": "$", "Baskin-Robbins": "$",
    "Segafredo": "$$",
    "J.Co": "$$",
    "Reboot": "$$",
    "Octane": "$$",
    "Lorca": "$$",
    "د. كيف": "$$", "Dr. Cafe": "$$",
    "Coffe Day": "$$",
    "Karak Habitat": "$",

    # Sweets/desserts
    "Häagen-Dazs": "$$",
    "Paradise": "$$",
    "Al Karama pastry": "$",
    "Candy Shop": "$",
    "etna artisan gelato": "$$",
    "لقيمات بثينة": "$",
    "أفران الحطب": "$",
    "بيت الكنفاني": "$",
}

# Category-based defaults for unknown places
CAT_DEFAULTS = {
    "مطعم": "$$",
    "كافيه": "$$",
    "حلويات": "$",
    "فنادق": "$$$",
    "تسوق": "$$",
    "ترفيه": "$$",
}

# Category-based tag templates
CATEGORY_TAGS = {
    "مطعم": ["مطاعم", "أكل"],
    "كافيه": ["مقاهي", "قهوة"],
    "حلويات": ["حلويات", "تحلية"],
    "مساجد": ["مساجد", "عبادة"],
    "ترفيه": ["ترفيه", "نشاطات"],
    "تسوق": ["تسوق", "محلات"],
    "فنادق": ["فنادق", "إقامة"],
    "طبيعة": ["طبيعة", "تنزه"],
    "تعليم": ["تعليم", "ثقافة"],
    "صحة": ["صحة", "طبي"],
    "خدمات": ["خدمات"],
    "رياضة": ["رياضة", "لياقة"],
    "أعمال": ["أعمال"],
    "سياحة": ["سياحة", "معالم"],
    "حكومي": ["حكومي", "خدمات"],
}

# Cuisine-based tags from restaurant names
CUISINE_KEYWORDS = {
    "iranian": "إيراني", "shiraz": "إيراني",
    "indian": "هندي", "darbar": "هندي", "mahboob": "هندي",
    "chinese": "صيني", "shanghai": "صيني",
    "italian": "إيطالي", "roma": "إيطالي", "finzione": "إيطالي", "quattro": "إيطالي",
    "french": "فرنسي",
    "syrian": "سوري", "yamal": "سوري", "باب توما": "سوري",
    "indonesian": "إندونيسي",
    "burger": "برجر",
    "pizza": "بيتزا",
    "shawarma": "شاورما", "شاورم": "شاورما",
    "bbq": "مشاوي", "مشوي": "مشاوي", "grill": "مشاوي",
    "sushi": "سوشي",
    "seafood": "مأكولات بحرية",
    "kabsa": "كبسة", "كبس": "كبسة",
    "mandi": "مندي", "مندي": "مندي",
    "coffee": "قهوة", "كافيه": "قهوة", "cafe": "قهوة",
    "shisha": "شيشة",
    "donuts": "دونات", "doughnut": "دونات",
    "gelato": "آيس كريم", "ice cream": "آيس كريم",
    "pastry": "معجنات", "أفران": "معجنات", "bakery": "مخبز",
    "مكسرات": "مكسرات",
}

for place in data:
    changed = False
    name_en = (place.get("name_en") or "").strip()
    name_ar = (place.get("name_ar") or "").strip()
    cat = place.get("category", "")

    # --- Fix invalid price_range ---
    if place.get("price_range") and place["price_range"] not in ("$", "$$", "$$$", "$$$$"):
        place["price_range"] = CAT_DEFAULTS.get(cat, "$$")
        changes["price_range_fix"] = changes.get("price_range_fix", 0) + 1
        changed = True

    # --- Assign price_range ---
    if not place.get("price_range") and cat in ("مطعم", "كافيه", "حلويات", "فنادق"):
        # Check known names
        price = None
        for key, val in KNOWN_PRICES.items():
            if key.lower() in name_en.lower() or key in name_ar:
                price = val
                break

        if not price:
            # Use category default
            price = CAT_DEFAULTS.get(cat, "$$")

        place["price_range"] = price
        changes["price_range"] += 1
        changed = True

    # --- Assign/enrich tags ---
    existing_tags = place.get("tags", [])
    if not existing_tags or existing_tags == ["openstreetmap"]:
        new_tags = list(existing_tags)  # keep existing

        # Add category tags
        cat_tags = CATEGORY_TAGS.get(cat, [])
        for t in cat_tags:
            if t not in new_tags:
                new_tags.append(t)

        # Add cuisine tags based on name
        combined_name = f"{name_en} {name_ar}".lower()
        for keyword, tag in CUISINE_KEYWORDS.items():
            if keyword.lower() in combined_name and tag not in new_tags:
                new_tags.append(tag)

        if set(new_tags) != set(existing_tags):
            place["tags"] = new_tags
            changes["tags"] += 1
            changed = True

    if changed:
        enriched_count += 1

# Also sync price_level with price_range
for place in data:
    if place.get("price_range") and place.get("price_level") != place.get("price_range"):
        place["price_level"] = place["price_range"]

# Save
with open(DATA_PATH, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Count remaining gaps
fields = ["price_range", "google_rating", "description_ar", "tags", "phone"]
print(f"\n=== ENRICHMENT COMPLETE ===")
print(f"Total places enriched: {enriched_count}")
for k, v in changes.items():
    print(f"  {k}: {v} updated")

print(f"\n=== REMAINING GAPS ===")
for field in fields:
    missing = sum(1 for p in data if not p.get(field))
    print(f"  {field}: {missing} missing / {len(data)} total")

# Save enrichment log
log = {"runs": []}
if os.path.exists(LOG_PATH):
    with open(LOG_PATH) as f:
        log = json.load(f)

log["runs"].append({
    "date": datetime.utcnow().isoformat() + "Z",
    "enriched": enriched_count,
    "changes": changes,
    "sources": [
        "TripAdvisor (price levels for known chains)",
        "Google Maps (ratings reference)",
        "Wanderlog (restaurant research)",
        "Category-based heuristics for tags",
        "Known Saudi restaurant chain pricing",
    ],
    "summary": f"Enriched {enriched_count} places: {changes['price_range']} price_range, {changes['tags']} tags"
})

with open(LOG_PATH, "w") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print(f"\nLog saved to {LOG_PATH}")
