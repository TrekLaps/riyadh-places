#!/usr/bin/env python3
"""
OSM Enrichment Script — سحب أماكن الرياض من OpenStreetMap
يشتغل يومياً عبر cron أو يدوي

المصدر: Overpass API (مجاني، بدون API key)
"""
import requests, json, os, sys
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PLACES_FILE = os.path.join(DATA_DIR, "places.json")

# Riyadh bounding box
RIYADH_BBOX = "24.5,46.4,25.0,47.0"

# Chains to skip (already in database)
SKIP_CHAINS = [
    "kfc", "mcdonalds", "mcdonald's", "burger king", "starbucks", "kudu", 
    "albaik", "البيك", "هرفي", "herfy", "subway", "pizza hut", "dominos", 
    "dunkin", "hardees", "بيتزا هت", "baskin", "tim hortons", "costa coffee",
    "caribou", "krispy kreme", "cinnabon", "papa john", "little caesars"
]

CATEGORY_MAP = {
    "restaurant": "مطعم", "fast_food": "مطعم", "cafe": "كافيه",
    "hotel": "فنادق", "hostel": "فنادق", "mall": "مولات",
    "department_store": "تسوق", "supermarket": "تسوق",
    "museum": "متاحف", "gallery": "متاحف", "attraction": "ترفيه",
    "park": "طبيعة", "water_park": "ترفيه", "sports_centre": "ترفيه",
}

def fetch_osm():
    """Fetch all Riyadh places from OpenStreetMap"""
    query = f"""
    [out:json][timeout:90];
    (
      node["amenity"~"restaurant|cafe|fast_food"]({RIYADH_BBOX});
      node["tourism"~"hotel|museum|attraction|gallery"]({RIYADH_BBOX});
      node["shop"="mall"]({RIYADH_BBOX});
      node["leisure"~"park|water_park|sports_centre"]({RIYADH_BBOX});
      way["shop"="mall"]({RIYADH_BBOX});
      way["tourism"~"hotel|museum"]({RIYADH_BBOX});
    );
    out tags center 5000;
    """
    r = requests.post("https://overpass-api.de/api/interpreter", 
                      data={"data": query}, timeout=120)
    r.raise_for_status()
    return r.json().get("elements", [])

def classify(tags):
    for key in ["amenity", "tourism", "shop", "leisure"]:
        val = tags.get(key, "")
        if val in CATEGORY_MAP:
            return CATEGORY_MAP[val]
    return "أخرى"

def is_chain(name):
    name_lower = name.lower()
    return any(c in name_lower for c in SKIP_CHAINS)

def main():
    # Load existing
    with open(PLACES_FILE) as f:
        places = json.load(f)
    
    existing = set()
    for p in places:
        if p.get("name_ar"): existing.add(p["name_ar"].strip().lower())
        if p.get("name_en"): existing.add(p["name_en"].strip().lower())
    
    print(f"Existing: {len(places)} places")
    
    # Fetch OSM
    elements = fetch_osm()
    print(f"OSM returned: {len(elements)} elements")
    
    new_count = 0
    today = date.today().isoformat()
    
    for e in elements:
        tags = e.get("tags", {})
        name_ar = tags.get("name:ar", "")
        name_en = tags.get("name:en", tags.get("name", ""))
        
        if not name_ar and not name_en:
            continue
        if is_chain(name_en) or is_chain(name_ar):
            continue
        if (name_ar and name_ar.strip().lower() in existing) or \
           (name_en and name_en.strip().lower() in existing):
            continue
        
        lat = e.get("lat") or e.get("center", {}).get("lat")
        lon = e.get("lon") or e.get("center", {}).get("lon")
        
        entry = {
            "name_ar": name_ar or name_en,
            "name_en": name_en or name_ar,
            "category": classify(tags),
            "neighborhood": "",
            "google_rating": None,
            "google_reviews_count": None,
            "description_ar": "",
            "google_maps_url": f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "",
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "instagram": tags.get("contact:instagram", ""),
            "tags": [t for t in (tags.get("cuisine", "").split(";") + ["openstreetmap"]) if t],
            "source": "openstreetmap",
            "added_date": today,
            "lat": lat, "lon": lon,
            "opening_hours": tags.get("opening_hours", "")
        }
        places.append(entry)
        if name_ar: existing.add(name_ar.strip().lower())
        if name_en: existing.add(name_en.strip().lower())
        new_count += 1
    
    if new_count > 0:
        with open(PLACES_FILE, "w") as f:
            json.dump(places, f, ensure_ascii=False, indent=2)
        print(f"✅ Added {new_count} new places (total: {len(places)})")
    else:
        print("✅ No new places found")
    
    return new_count

if __name__ == "__main__":
    added = main()
    sys.exit(0 if added >= 0 else 1)
