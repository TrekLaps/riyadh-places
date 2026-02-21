#!/usr/bin/env python3
"""Bulk OSM data collection for Riyadh places via Overpass API"""

import json
import urllib.request
import urllib.parse
import time
import hashlib
import re
import sys

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
BBOX = "24.5,46.4,25.0,47.0"  # Riyadh

# Map OSM tags to our categories
QUERIES = [
    # SHOPS - huge untapped category
    {
        "query": f'[out:json][timeout:120];(node["shop"~"clothes|fashion|boutique"]({BBOX});way["shop"~"clothes|fashion|boutique"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "clothes"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"electronics|computer|mobile_phone"]({BBOX});way["shop"~"electronics|computer|mobile_phone"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "electronics"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"perfumery|cosmetics|beauty"]({BBOX});way["shop"~"perfumery|cosmetics|beauty"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "beauty"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"jewelry|watches"]({BBOX});way["shop"~"jewelry|watches"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "jewelry"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"books|stationery"]({BBOX});way["shop"~"books|stationery"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "books"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"supermarket|convenience|grocery"]({BBOX});way["shop"~"supermarket|convenience|grocery"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "grocery"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"furniture|interior_decoration|carpet"]({BBOX});way["shop"~"furniture|interior_decoration|carpet"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "furniture"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"optician|medical_supply|hearing_aids"]({BBOX});way["shop"~"optician|medical_supply|hearing_aids"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "optical"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"car|car_parts|car_repair|tyres"]({BBOX});way["shop"~"car|car_parts|car_repair|tyres"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "automotive"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"sports|outdoor"]({BBOX});way["shop"~"sports|outdoor"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "sports"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"toys|baby_goods|children"]({BBOX});way["shop"~"toys|baby_goods|children"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "toys"
    },
    {
        "query": f'[out:json][timeout:120];(node["shop"~"gift|florist|pet"]({BBOX});way["shop"~"gift|florist|pet"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "gifts"
    },
    # BAKERIES & SWEETS
    {
        "query": f'[out:json][timeout:120];(node["shop"~"bakery|pastry|confectionery|chocolate"]({BBOX});way["shop"~"bakery|pastry|confectionery|chocolate"]({BBOX}););out center;',
        "category_ar": "حلويات", "category_en": "desserts", "subcategory": "bakery"
    },
    {
        "query": f'[out:json][timeout:120];(node["amenity"="ice_cream"]({BBOX});way["amenity"="ice_cream"]({BBOX}););out center;',
        "category_ar": "حلويات", "category_en": "desserts", "subcategory": "ice_cream"
    },
    # HEALTH & MEDICAL
    {
        "query": f'[out:json][timeout:120];(node["amenity"~"pharmacy"]({BBOX});way["amenity"~"pharmacy"]({BBOX}););out center;',
        "category_ar": "صحة", "category_en": "health", "subcategory": "pharmacy"
    },
    {
        "query": f'[out:json][timeout:120];(node["amenity"~"hospital|clinic|doctors|dentist"]({BBOX});way["amenity"~"hospital|clinic|doctors|dentist"]({BBOX}););out center;',
        "category_ar": "صحة", "category_en": "health", "subcategory": "medical"
    },
    # EDUCATION
    {
        "query": f'[out:json][timeout:120];(node["amenity"~"school|university|college|kindergarten|library"]({BBOX});way["amenity"~"school|university|college|kindergarten|library"]({BBOX}););out center;',
        "category_ar": "تعليم", "category_en": "education", "subcategory": "school"
    },
    # FINANCE
    {
        "query": f'[out:json][timeout:120];(node["amenity"~"bank|atm|bureau_de_change|money_transfer"]({BBOX});way["amenity"~"bank|atm|bureau_de_change|money_transfer"]({BBOX}););out center;',
        "category_ar": "خدمات مالية", "category_en": "finance", "subcategory": "bank"
    },
    # FUEL
    {
        "query": f'[out:json][timeout:120];(node["amenity"="fuel"]({BBOX});way["amenity"="fuel"]({BBOX}););out center;',
        "category_ar": "خدمات", "category_en": "services", "subcategory": "fuel"
    },
    # FITNESS & SPORTS
    {
        "query": f'[out:json][timeout:120];(node["leisure"~"fitness_centre|sports_centre|swimming_pool|stadium"]({BBOX});way["leisure"~"fitness_centre|sports_centre|swimming_pool|stadium"]({BBOX}););out center;',
        "category_ar": "رياضة", "category_en": "sports", "subcategory": "gym"
    },
    {
        "query": f'[out:json][timeout:120];(node["sport"]({BBOX});way["sport"]({BBOX}););out center;',
        "category_ar": "رياضة", "category_en": "sports", "subcategory": "sport"
    },
    # PARKS & GARDENS
    {
        "query": f'[out:json][timeout:120];(node["leisure"~"park|garden|playground|dog_park"]({BBOX});way["leisure"~"park|garden|playground|dog_park"]({BBOX}););out center;',
        "category_ar": "طبيعة", "category_en": "nature", "subcategory": "park"
    },
    # TOURISM
    {
        "query": f'[out:json][timeout:120];(node["tourism"~"theme_park|zoo|attraction|viewpoint|museum|gallery|artwork"]({BBOX});way["tourism"~"theme_park|zoo|attraction|viewpoint|museum|gallery|artwork"]({BBOX}););out center;',
        "category_ar": "سياحة", "category_en": "tourism", "subcategory": "attraction"
    },
    {
        "query": f'[out:json][timeout:120];(node["tourism"~"hotel|motel|guest_house|hostel|apartment"]({BBOX});way["tourism"~"hotel|motel|guest_house|hostel|apartment"]({BBOX}););out center;',
        "category_ar": "فنادق", "category_en": "hotels", "subcategory": "hotel"
    },
    # MOSQUES (landmarks)
    {
        "query": f'[out:json][timeout:120];(node["amenity"="place_of_worship"]["religion"="muslim"]({BBOX});way["amenity"="place_of_worship"]["religion"="muslim"]({BBOX}););out center;',
        "category_ar": "مساجد", "category_en": "mosques", "subcategory": "mosque"
    },
    # ENTERTAINMENT
    {
        "query": f'[out:json][timeout:120];(node["amenity"~"cinema|theatre|nightclub|community_centre"]({BBOX});way["amenity"~"cinema|theatre|nightclub|community_centre"]({BBOX}););out center;',
        "category_ar": "ترفيه", "category_en": "entertainment", "subcategory": "cinema"
    },
    {
        "query": f'[out:json][timeout:120];(node["leisure"~"bowling_alley|golf_course|miniature_golf|amusement_arcade|escape_game|water_park"]({BBOX});way["leisure"~"bowling_alley|golf_course|miniature_golf|amusement_arcade|escape_game|water_park"]({BBOX}););out center;',
        "category_ar": "ترفيه", "category_en": "entertainment", "subcategory": "amusement"
    },
    # RESTAURANTS (additional - fast food, etc)
    {
        "query": f'[out:json][timeout:120];(node["amenity"="fast_food"]({BBOX});way["amenity"="fast_food"]({BBOX}););out center;',
        "category_ar": "مطعم", "category_en": "restaurant", "subcategory": "fast_food"
    },
    # CAFES
    {
        "query": f'[out:json][timeout:120];(node["amenity"="cafe"]({BBOX});way["amenity"="cafe"]({BBOX}););out center;',
        "category_ar": "كافيه", "category_en": "cafe", "subcategory": "cafe"
    },
    # RESTAURANTS
    {
        "query": f'[out:json][timeout:120];(node["amenity"="restaurant"]({BBOX});way["amenity"="restaurant"]({BBOX}););out center;',
        "category_ar": "مطعم", "category_en": "restaurant", "subcategory": "restaurant"
    },
    # BEAUTY/HAIRDRESSER
    {
        "query": f'[out:json][timeout:120];(node["shop"~"hairdresser|beauty|tattoo|massage"]({BBOX});way["shop"~"hairdresser|beauty|tattoo|massage"]({BBOX}););out center;',
        "category_ar": "جمال وعناية", "category_en": "beauty", "subcategory": "salon"
    },
    # MARKETPLACE
    {
        "query": f'[out:json][timeout:120];(node["amenity"="marketplace"]({BBOX});way["amenity"="marketplace"]({BBOX}););out center;',
        "category_ar": "تسوق", "category_en": "shopping", "subcategory": "market"
    },
]

def normalize_arabic(text):
    """Normalize Arabic text for dedup"""
    if not text:
        return ""
    text = text.strip()
    # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Normalize alef variants
    text = re.sub(r'[إأآا]', 'ا', text)
    # Normalize taa marbouta
    text = text.replace('ة', 'ه')
    # Normalize ya
    text = text.replace('ى', 'ي')
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def make_id(name):
    """Generate slug ID from name"""
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[\s_]+', '-', name.strip())
    if not name or name == '-':
        name = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    return name[:60]

def get_lat_lng(elem):
    """Extract coordinates from OSM element"""
    if elem.get('type') == 'node':
        return elem.get('lat'), elem.get('lon')
    elif 'center' in elem:
        return elem['center'].get('lat'), elem['center'].get('lon')
    return None, None

def query_overpass(query_str, retries=3):
    """Query Overpass API with retries"""
    for attempt in range(retries):
        try:
            data = urllib.parse.urlencode({'data': query_str}).encode()
            req = urllib.request.Request(OVERPASS_URL, data=data)
            req.add_header('User-Agent', 'RiyadhPlacesCollector/1.0')
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(10 * (attempt + 1))
    return None

def main():
    # Load existing places
    with open('places.json') as f:
        existing = json.load(f)
    
    # Build dedup set from existing names
    existing_names = set()
    for p in existing:
        name_ar = normalize_arabic(p.get('name_ar', ''))
        name_en = (p.get('name_en') or '').lower().strip()
        if name_ar:
            existing_names.add(name_ar)
        if name_en:
            existing_names.add(name_en)
    
    print(f"Existing places: {len(existing)}, unique names: {len(existing_names)}")
    
    all_new = []
    seen_in_batch = set()  # dedup within this batch too
    
    for i, q in enumerate(QUERIES):
        print(f"\n[{i+1}/{len(QUERIES)}] Querying: {q['category_en']}/{q['subcategory']}...")
        result = query_overpass(q['query'])
        
        if not result or 'elements' not in result:
            print(f"  No results or error")
            continue
        
        elements = result['elements']
        print(f"  Got {len(elements)} raw elements")
        
        added = 0
        for elem in elements:
            tags = elem.get('tags', {})
            
            # Get name
            name_ar = tags.get('name:ar') or tags.get('name', '')
            name_en = tags.get('name:en') or tags.get('int_name', '')
            
            if not name_ar and not name_en:
                continue
            
            # Dedup check
            norm_ar = normalize_arabic(name_ar)
            norm_en = (name_en or '').lower().strip()
            
            if norm_ar and norm_ar in existing_names:
                continue
            if norm_en and norm_en in existing_names:
                continue
            if norm_ar and norm_ar in seen_in_batch:
                continue
            if norm_en and norm_en in seen_in_batch:
                continue
            
            lat, lng = get_lat_lng(elem)
            if not lat or not lng:
                continue
            
            # Skip if outside Riyadh proper (rough check)
            if lat < 24.4 or lat > 25.1 or lng < 46.3 or lng > 47.1:
                continue
            
            # Build place object
            place_id = make_id(name_en or name_ar)
            
            # Try to get useful tags
            phone = tags.get('phone') or tags.get('contact:phone')
            website = tags.get('website') or tags.get('contact:website')
            opening_hours = tags.get('opening_hours')
            cuisine = tags.get('cuisine')
            brand = tags.get('brand')
            
            place = {
                "id": place_id,
                "name_ar": name_ar or None,
                "name_en": name_en or None,
                "category": q['category_ar'],
                "category_ar": q['category_ar'],
                "category_en": q['category_en'],
                "subcategory": q['subcategory'],
                "neighborhood": None,
                "neighborhood_en": None,
                "description_ar": None,
                "google_rating": None,
                "price_level": None,
                "trending": False,
                "is_new": False,
                "sources": ["OpenStreetMap"],
                "google_maps_url": f"https://maps.google.com/?q={lat},{lng}",
                "lat": round(lat, 6),
                "lng": round(lng, 6),
                "is_free": None,
                "audience": [],
                "phone": phone,
                "website": website,
                "opening_hours": opening_hours,
                "osm_id": elem.get('id'),
                "osm_tags": {
                    "cuisine": cuisine,
                    "brand": brand,
                }
            }
            
            all_new.append(place)
            if norm_ar:
                seen_in_batch.add(norm_ar)
                existing_names.add(norm_ar)
            if norm_en:
                seen_in_batch.add(norm_en)
                existing_names.add(norm_en)
            added += 1
        
        print(f"  Added {added} new places")
        
        # Be nice to the API
        time.sleep(3)
    
    print(f"\n{'='*50}")
    print(f"Total new places from OSM: {len(all_new)}")
    
    # Save new places separately first
    with open('osm-new-bulk.json', 'w') as f:
        json.dump(all_new, f, ensure_ascii=False, indent=2)
    
    # Merge into main places.json
    merged = existing + all_new
    with open('places.json', 'w') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    
    print(f"Total places after merge: {len(merged)}")
    
    # Category breakdown of new
    cats = {}
    for p in all_new:
        key = f"{p['category_en']}/{p.get('subcategory','')}"
        cats[key] = cats.get(key, 0) + 1
    print("\nNew places by category:")
    for k, v in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
