#!/usr/bin/env python3
"""Second batch of OSM queries - retry failed + new categories"""
import json, urllib.request, urllib.parse, time, hashlib, re

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
BBOX = "24.5,46.4,25.0,47.0"

QUERIES = [
    # Failed in batch 1
    {
        "query": f'[out:json][timeout:180];node["shop"~"electronics|computer|mobile_phone"]({BBOX});out;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "electronics"
    },
    {
        "query": f'[out:json][timeout:180];node["amenity"~"bank|atm"]({BBOX});out;',
        "category_ar": "خدمات مالية", "category_en": "finance", "subcategory": "bank"
    },
    # NEW categories
    {
        "query": f'[out:json][timeout:120];node["shop"~"hardware|doityourself|paint"]({BBOX});out;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "hardware"
    },
    {
        "query": f'[out:json][timeout:120];node["shop"~"laundry|dry_cleaning"]({BBOX});out;',
        "category_ar": "خدمات", "category_en": "services", "subcategory": "laundry"
    },
    {
        "query": f'[out:json][timeout:120];node["shop"~"tailor|fabric"]({BBOX});out;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "tailor"
    },
    {
        "query": f'[out:json][timeout:120];node["amenity"~"car_rental|car_wash|parking"]({BBOX});out;',
        "category_ar": "خدمات", "category_en": "services", "subcategory": "car_services"
    },
    {
        "query": f'[out:json][timeout:120];node["amenity"~"post_office|police|fire_station|embassy|courthouse"]({BBOX});out;',
        "category_ar": "خدمات حكومية", "category_en": "government", "subcategory": "public"
    },
    {
        "query": f'[out:json][timeout:120];node["office"~"government|company|insurance|lawyer|estate_agent|travel_agent"]({BBOX});out;',
        "category_ar": "مكاتب", "category_en": "offices", "subcategory": "office"
    },
    {
        "query": f'[out:json][timeout:120];node["shop"~"travel_agency|copyshop|printing"]({BBOX});out;',
        "category_ar": "خدمات", "category_en": "services", "subcategory": "travel"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"="mall"]({BBOX});way["shop"="mall"]({BBOX});node["shop"="department_store"]({BBOX});way["shop"="department_store"]({BBOX}););out center;',
        "category_ar": "مولات", "category_en": "malls", "subcategory": "mall"
    },
    {
        "query": f'[out:json][timeout:120];node["amenity"~"veterinary"]({BBOX});out;',
        "category_ar": "خدمات", "category_en": "services", "subcategory": "vet"
    },
    {
        "query": f'[out:json][timeout:120];node["shop"~"photo|frame"]({BBOX});out;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "photo"
    },
    {
        "query": f'[out:json][timeout:120];node["craft"]({BBOX});out;',
        "category_ar": "حرف", "category_en": "crafts", "subcategory": "craft"
    },
]

def normalize_arabic(text):
    if not text: return ""
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text.strip())
    text = re.sub(r'[إأآا]', 'ا', text)
    text = text.replace('ة', 'ه').replace('ى', 'ي')
    return re.sub(r'\s+', ' ', text).strip().lower()

def query_overpass(qs, retries=3):
    for attempt in range(retries):
        try:
            data = urllib.parse.urlencode({'data': qs}).encode()
            req = urllib.request.Request(OVERPASS_URL, data=data)
            req.add_header('User-Agent', 'RiyadhPlaces/1.0')
            with urllib.request.urlopen(req, timeout=200) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1: time.sleep(15 * (attempt + 1))
    return None

with open('places.json') as f:
    existing = json.load(f)

existing_names = set()
for p in existing:
    n = normalize_arabic(p.get('name_ar', ''))
    e = (p.get('name_en') or '').lower().strip()
    if n: existing_names.add(n)
    if e: existing_names.add(e)

print(f"Starting with {len(existing)} places, {len(existing_names)} unique names")

all_new = []
seen = set()

for i, q in enumerate(QUERIES):
    print(f"\n[{i+1}/{len(QUERIES)}] {q['category_en']}/{q['subcategory']}...")
    result = query_overpass(q['query'])
    if not result or 'elements' not in result:
        print("  Failed"); continue
    
    added = 0
    for elem in result['elements']:
        tags = elem.get('tags', {})
        name_ar = tags.get('name:ar') or tags.get('name', '')
        name_en = tags.get('name:en') or tags.get('int_name', '')
        if not name_ar and not name_en: continue
        
        norm_ar = normalize_arabic(name_ar)
        norm_en = (name_en or '').lower().strip()
        if (norm_ar and norm_ar in existing_names) or (norm_en and norm_en in existing_names): continue
        if (norm_ar and norm_ar in seen) or (norm_en and norm_en in seen): continue
        
        lat = elem.get('lat') or (elem.get('center', {}).get('lat'))
        lng = elem.get('lon') or (elem.get('center', {}).get('lon'))
        if not lat or not lng: continue
        if lat < 24.4 or lat > 25.1 or lng < 46.3 or lng > 47.1: continue
        
        phone = tags.get('phone') or tags.get('contact:phone')
        website = tags.get('website') or tags.get('contact:website')
        
        place = {
            "id": re.sub(r'[\s_]+', '-', re.sub(r'[^\w\s-]', '', (name_en or name_ar).lower()))[:60] or hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
            "name_ar": name_ar or None, "name_en": name_en or None,
            "category": q['category_ar'], "category_ar": q['category_ar'], "category_en": q['category_en'],
            "subcategory": q['subcategory'],
            "neighborhood": None, "neighborhood_en": None,
            "description_ar": None, "google_rating": None, "price_level": None,
            "trending": False, "is_new": False,
            "sources": ["OpenStreetMap"],
            "google_maps_url": f"https://maps.google.com/?q={lat},{lng}",
            "lat": round(lat, 6), "lng": round(lng, 6),
            "is_free": None, "audience": [],
            "phone": phone, "website": website,
            "osm_id": elem.get('id'),
        }
        all_new.append(place)
        if norm_ar: seen.add(norm_ar); existing_names.add(norm_ar)
        if norm_en: seen.add(norm_en); existing_names.add(norm_en)
        added += 1
    print(f"  Got {len(result['elements'])} elements, added {added}")
    time.sleep(5)

print(f"\nTotal new: {len(all_new)}")
merged = existing + all_new
with open('places.json', 'w') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"Total after merge: {len(merged)}")

cats = {}
for p in all_new:
    k = f"{p['category_en']}/{p.get('subcategory','')}"
    cats[k] = cats.get(k, 0) + 1
for k,v in sorted(cats.items(), key=lambda x:-x[1]):
    print(f"  {k}: {v}")
