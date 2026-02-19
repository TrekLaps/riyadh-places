#!/usr/bin/env python3
"""Merge new places + prices + validate + generate stats for riyadh-places project."""

import json
import re
import sys
from pathlib import Path
from collections import Counter

BASE = Path("/home/ubuntu/.openclaw/workspace/projects/riyadh-places")

# Required fields with defaults
REQUIRED_FIELDS = {
    "id": "",
    "name_ar": "",
    "name_en": "",
    "category": "",
    "category_ar": "",
    "category_en": "",
    "neighborhood": "",
    "neighborhood_en": "",
    "description_ar": "",
    "google_rating": 4.0,
    "price_level": "$$",
    "trending": False,
    "is_new": True,
    "sources": [],
    "google_maps_url": "",
    "district": "الرياض",
    "perfect_for": [],
    "lat": 24.7136,
    "lng": 46.6753,
    "is_free": False,
    "audience": ["الكل"],
}

VALID_CATEGORIES_AR = {"مطعم", "كافيه", "ترفيه", "حلويات", "تسوق", "فنادق", "طبيعة", "شاليه", "فعاليات", "متاحف", "مولات"}
VALID_PRICE_LEVELS = {"$", "$$", "$$$", "$$$$", "مجاني", "free", "Free"}

# Category mapping from english/research format
CATEGORY_MAP = {
    "restaurant": ("مطعم", "مطعم", "Restaurant"),
    "cafe": ("كافيه", "كافيه", "Cafe"),
    "entertainment": ("ترفيه", "ترفيه", "Entertainment"),
    "hotel": ("فنادق", "فنادق", "Hotel"),
    "mall": ("مولات", "مولات", "Mall"),
    "shopping": ("تسوق", "تسوق", "Shopping"),
    "dessert": ("حلويات", "حلويات", "Dessert"),
    "nature": ("طبيعة", "طبيعة", "Nature"),
    "events": ("فعاليات", "فعاليات", "Events"),
    "museum": ("متاحف", "متاحف", "Museum"),
    "chalet": ("شاليه", "شاليه", "Chalet"),
}

# Neighborhood mapping
NEIGHBORHOOD_MAP = {
    "KAFD": ("حي العقيق", "KAFD"),
    "kafd": ("حي العقيق", "KAFD"),
    "Al Olaya": ("حي العليا", "Al Olaya"),
    "Diriyah": ("الدرعية", "Diriyah"),
    "الدرعية": ("الدرعية", "Diriyah"),
    "السليمانية": ("حي السليمانية", "Al Sulaimaniyah"),
    "Al Sulaimaniyah": ("حي السليمانية", "Al Sulaimaniyah"),
    "النخيل": ("حي النخيل", "Al Nakheel"),
    "Al Nakheel": ("حي النخيل", "Al Nakheel"),
    "حي الملقا": ("حي الملقا", "Al Malqa"),
    "Al Malqa": ("حي الملقا", "Al Malqa"),
    "حطين": ("حي حطين", "Hittin"),
    "Hittin": ("حي حطين", "Hittin"),
    "الياسمين": ("حي الياسمين", "Al Yasmin"),
    "Al Yasmin": ("حي الياسمين", "Al Yasmin"),
    "المروج": ("حي المروج", "Al Murooj"),
    "الورود": ("حي الورود", "Al Wurud"),
    "الرحمانية": ("حي الرحمانية", "Al Rahmaniyah"),
    "الصحافة": ("حي الصحافة", "Al Sahafah"),
    "العارض": ("حي العارض", "Al Arid"),
    "الربيع": ("حي الربيع", "Al Rabi"),
    "التعاون": ("حي التعاون", "Al Taawun"),
    "الغدير": ("حي الغدير", "Al Ghadir"),
    "المعذر": ("حي المعذر", "Al Mathar"),
    "الملز": ("حي الملز", "Al Malaz"),
}


def slugify(name):
    """Generate a URL-friendly slug from name_en."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def normalize_research_place(p):
    """Convert a research-format place to standard format."""
    cat_key = p.get("category", "restaurant").lower()
    cat_info = CATEGORY_MAP.get(cat_key, ("مطعم", "مطعم", "Restaurant"))
    
    name_en = p.get("name_en", "")
    neighborhood = p.get("neighborhood", "")
    
    # Resolve neighborhood
    nb_ar = neighborhood
    nb_en = neighborhood
    if neighborhood in NEIGHBORHOOD_MAP:
        nb_ar, nb_en = NEIGHBORHOOD_MAP[neighborhood]
    elif not any(c in neighborhood for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
        nb_en = neighborhood
        nb_ar = neighborhood
    
    place = {
        "id": slugify(name_en),
        "name_ar": p.get("name_ar", ""),
        "name_en": name_en,
        "category": cat_info[0],
        "category_ar": cat_info[1],
        "category_en": cat_info[2],
        "neighborhood": nb_ar,
        "neighborhood_en": nb_en,
        "description_ar": p.get("description_ar", ""),
        "google_rating": p.get("google_rating", 4.2),
        "price_level": p.get("price_level", "$$$"),
        "trending": p.get("trending", True),
        "is_new": True,
        "sources": [p.get("source", "research")] if isinstance(p.get("source"), str) else p.get("sources", ["research"]),
        "google_maps_url": p.get("google_maps_url", f"https://maps.google.com/?q={name_en.replace(' ', '+')}+Riyadh"),
        "district": p.get("district", "الرياض"),
        "perfect_for": p.get("perfect_for", []),
        "lat": p.get("lat", 24.7136),
        "lng": p.get("lng", 46.6753),
        "is_free": p.get("is_free", False),
        "audience": p.get("audience", ["الكل"]),
    }
    return place


def ensure_fields(place):
    """Ensure all required fields exist with defaults."""
    for field, default in REQUIRED_FIELDS.items():
        if field not in place or place[field] is None:
            place[field] = default
    
    # Fix audience if string
    if isinstance(place.get("audience"), str):
        place["audience"] = [place["audience"]]
    
    # Fix sources if string
    if isinstance(place.get("sources"), str):
        place["sources"] = [place["sources"]]
    
    # Ensure id
    if not place["id"]:
        place["id"] = slugify(place.get("name_en", "unknown"))
    
    # Ensure google_maps_url
    if not place.get("google_maps_url"):
        name = place.get("name_en", "")
        place["google_maps_url"] = f"https://maps.google.com/?q={name.replace(' ', '+')}+Riyadh"
    
    return place


def validate_places(places):
    """Run comprehensive validation."""
    errors = []
    warnings = []
    
    # Check unique IDs
    ids = [p["id"] for p in places]
    id_counts = Counter(ids)
    for pid, count in id_counts.items():
        if count > 1:
            errors.append(f"Duplicate ID: '{pid}' appears {count} times")
    
    # Check unique name_en
    names = [p["name_en"].lower().strip() for p in places]
    name_counts = Counter(names)
    for name, count in name_counts.items():
        if count > 1:
            warnings.append(f"Duplicate name_en: '{name}' appears {count} times")
    
    for i, p in enumerate(places):
        prefix = f"[{p.get('id', f'index-{i}')}]"
        
        # Required fields
        if not p.get("name_ar"):
            errors.append(f"{prefix} Missing name_ar")
        if not p.get("name_en"):
            errors.append(f"{prefix} Missing name_en")
        
        # Rating 0-5
        rating = p.get("google_rating", 0)
        if not (0 <= rating <= 5):
            errors.append(f"{prefix} Invalid rating: {rating}")
        
        # Price level
        pl = p.get("price_level", "")
        if pl and pl not in VALID_PRICE_LEVELS:
            warnings.append(f"{prefix} Non-standard price_level: '{pl}'")
        
        # Category
        cat = p.get("category", "")
        if cat and cat not in VALID_CATEGORIES_AR:
            warnings.append(f"{prefix} Non-standard category: '{cat}'")
        
        # Lat/Lng bounds for Riyadh
        lat = p.get("lat", 0)
        lng = p.get("lng", 0)
        if lat and not (24.0 <= lat <= 25.5):
            warnings.append(f"{prefix} lat {lat} outside Riyadh range")
        if lng and not (46.0 <= lng <= 47.5):
            warnings.append(f"{prefix} lng {lng} outside Riyadh range")
        
        # Missing required fields
        for field in REQUIRED_FIELDS:
            if field not in p:
                warnings.append(f"{prefix} Missing field: {field}")
    
    return errors, warnings


def generate_light_version(places):
    """Generate places-light.json with essential fields only."""
    light_fields = ["id", "name_ar", "name_en", "category", "category_ar", "category_en",
                    "neighborhood", "neighborhood_en", "google_rating", "price_level",
                    "trending", "is_new", "lat", "lng", "is_free", "audience", "district"]
    light = []
    for p in places:
        lp = {k: p.get(k) for k in light_fields if k in p}
        light.append(lp)
    return light


def main():
    print("=" * 60)
    print("🔄 Riyadh Places - Merge & Validate")
    print("=" * 60)
    
    # 1. Load existing places
    with open(BASE / "data/places.json") as f:
        places = json.load(f)
    print(f"\n📦 Existing places: {len(places)}")
    
    # Build index by name_en (lowercase)
    existing_names = {p["name_en"].lower().strip() for p in places}
    existing_names_ar = {p["name_ar"].strip() for p in places}
    existing_ids = {p["id"] for p in places}
    
    # 2. Load new-places-batch.json
    with open(BASE / "data/new-places-batch.json") as f:
        batch_places = json.load(f)
    print(f"📦 New batch places: {len(batch_places)}")
    
    # 3. Load research places
    with open(BASE / "research/new-places-discovered.json") as f:
        research_data = json.load(f)
    research_places = research_data.get("places", [])
    print(f"📦 Research places: {len(research_places)}")
    
    # 4. Merge batch places (already in standard format)
    added_batch = 0
    for p in batch_places:
        p = ensure_fields(p)
        name_key = p["name_en"].lower().strip()
        if name_key not in existing_names:
            # Ensure unique ID
            if p["id"] in existing_ids:
                p["id"] = p["id"] + "-2"
            places.append(p)
            existing_names.add(name_key)
            existing_ids.add(p["id"])
            added_batch += 1
        else:
            pass  # Skip duplicate
    print(f"✅ Added from batch: {added_batch}")
    
    # 5. Merge research places (need normalization)
    added_research = 0
    for rp in research_places:
        p = normalize_research_place(rp)
        p = ensure_fields(p)
        name_key = p["name_en"].lower().strip()
        if name_key not in existing_names:
            if p["id"] in existing_ids:
                p["id"] = p["id"] + "-new"
            places.append(p)
            existing_names.add(name_key)
            existing_ids.add(p["id"])
            added_research += 1
    print(f"✅ Added from research: {added_research}")
    
    total_added = added_batch + added_research
    print(f"\n📊 Total new places added: {total_added}")
    print(f"📊 Total places now: {len(places)}")
    
    # 6. Ensure all places have required fields
    for p in places:
        ensure_fields(p)
    
    # 7. Load and index prices
    with open(BASE / "data/prices-initial.json") as f:
        prices = json.load(f)
    print(f"\n💰 Prices entries: {len(prices)}")
    
    price_index = {}
    for pr in prices:
        key = pr.get("name_en", "").lower().strip()
        price_index[key] = pr
    
    # Match prices to places
    matched_prices = 0
    for p in places:
        key = p["name_en"].lower().strip()
        if key in price_index:
            matched_prices += 1
    print(f"💰 Prices matched to places: {matched_prices}/{len(prices)}")
    
    # Unmatched prices
    place_names_lower = {p["name_en"].lower().strip() for p in places}
    unmatched = [pr["name_en"] for pr in prices if pr["name_en"].lower().strip() not in place_names_lower]
    if unmatched:
        print(f"⚠️  Unmatched price entries: {unmatched}")
    
    # 8. Validation
    print("\n" + "=" * 60)
    print("🔍 VALIDATION REPORT")
    print("=" * 60)
    
    errors, warnings = validate_places(places)
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for e in errors[:30]:
            print(f"   {e}")
        if len(errors) > 30:
            print(f"   ... and {len(errors) - 30} more")
    else:
        print("\n✅ No errors found!")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings[:30]:
            print(f"   {w}")
        if len(warnings) > 30:
            print(f"   ... and {len(warnings) - 30} more")
    else:
        print("\n✅ No warnings!")
    
    # 9. Fix duplicate IDs
    seen_ids = {}
    for p in places:
        if p["id"] in seen_ids:
            seen_ids[p["id"]] += 1
            p["id"] = f"{p['id']}-{seen_ids[p['id']]}"
        else:
            seen_ids[p["id"]] = 1
    
    # 10. Statistics
    print("\n" + "=" * 60)
    print("📊 STATISTICS")
    print("=" * 60)
    
    print(f"\n📍 Total places: {len(places)}")
    
    # By category
    cats = Counter(p.get("category", "غير مصنف") for p in places)
    print("\n📂 By Category:")
    for cat, count in cats.most_common():
        print(f"   {cat}: {count}")
    
    # By neighborhood (top 20)
    hoods = Counter(p.get("neighborhood", "غير محدد") for p in places)
    print("\n🏘️ Top 20 Neighborhoods:")
    for hood, count in hoods.most_common(20):
        print(f"   {hood}: {count}")
    
    # New places
    new_count = sum(1 for p in places if p.get("is_new"))
    print(f"\n🆕 New places (is_new=true): {new_count}")
    print(f"💰 Places with real prices: {matched_prices}")
    print(f"🔥 Trending places: {sum(1 for p in places if p.get('trending'))}")
    print(f"🆓 Free places: {sum(1 for p in places if p.get('is_free'))}")
    
    # 11. Save merged places.json
    with open(BASE / "data/places.json", "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved places.json ({len(places)} places)")
    
    # 12. Save places-light.json
    light = generate_light_version(places)
    with open(BASE / "data/places-light.json", "w", encoding="utf-8") as f:
        json.dump(light, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved places-light.json ({len(light)} places)")
    
    # 13. Save price index
    with open(BASE / "data/prices-index.json", "w", encoding="utf-8") as f:
        json.dump(price_index, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved prices-index.json ({len(price_index)} entries)")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ MERGE COMPLETE")
    print("=" * 60)
    print(f"   Total places: {len(places)}")
    print(f"   New added: {total_added}")
    print(f"   Errors: {len(errors)}")
    print(f"   Warnings: {len(warnings)}")
    
    return len(errors) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
