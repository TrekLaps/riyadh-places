#!/usr/bin/env python3
"""
Riyadh Places — Data Normalization, Merge & AI-Ready Feature Generation
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher

DATA_DIR = '.'

# ─── Standard Categories ───
STANDARD_CATEGORIES = {
    'مطعم', 'كافيه', 'ترفيه', 'حلويات', 'تسوق', 'طبيعة',
    'فنادق', 'شاليه', 'متاحف', 'فعاليات', 'مولات'
}

CATEGORY_MAP = {
    'أخرى': None,  # will keep as-is if no better match
    'cafe': 'كافيه',
    'restaurant': 'مطعم',
    'hotel': 'فنادق',
    'chalet': 'شاليه',
    'entertainment': 'ترفيه',
    'shopping': 'تسوق',
    'nature': 'طبيعة',
    'museum': 'متاحف',
    'mall': 'مولات',
    'events': 'فعاليات',
    'sweets': 'حلويات',
}

# ─── Neighborhood normalization ───
NEIGHBORHOOD_MERGE = {
    'العليا': 'حي العليا',
    'الملقا': 'حي الملقا',
    'حطين': 'حي حطين',
    'الياسمين': 'حي الياسمين',
    'النرجس': 'حي النرجس',
    'الصحافة': 'حي الصحافة',
    'الملز': 'حي الملز',
    'الربيع': 'حي الربيع',
    'العقيق': 'حي العقيق',
    'النخيل': 'حي النخيل',
    'السليمانية': 'حي السليمانية',
    'الورود': 'حي الورود',
    'الروضة': 'حي الروضة',
    'المروج': 'حي المروج',
    'الغدير': 'حي الغدير',
    'الشفا': 'حي الشفا',
    'المنصورة': 'حي المنصورة',
    'الخزامى': 'حي الخزامى',
    'الازدهار': 'حي الازدهار',
    'النسيم': 'حي النسيم',
    'السلي': 'حي السلي',
    'البطحاء': 'حي البطحاء',
    'العزيزية': 'حي العزيزية',
    'الدرعية': 'الدرعية',
    'KAFD': 'كافد',
}

def load_json(path):
    with open(f"{DATA_DIR}/{path}") as f:
        return json.load(f)

def save_json(path, data):
    with open(f"{DATA_DIR}/{path}", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path} ({len(data) if isinstance(data, list) else 'dict'} entries)")

def normalize_phone(phone):
    if not phone:
        return phone
    phone = re.sub(r'[\s\-\(\)]', '', str(phone))
    if phone.startswith('05') and len(phone) == 10:
        return '+966' + phone[1:]
    if phone.startswith('5') and len(phone) == 9:
        return '+966' + phone
    if phone.startswith('009665'):
        return '+966' + phone[5:]
    if phone.startswith('+966'):
        return phone
    if phone.startswith('966') and len(phone) == 12:
        return '+' + phone
    return phone

def normalize_instagram(handle):
    if not handle:
        return handle
    handle = str(handle).strip()
    handle = handle.lstrip('@')
    # Remove URL prefix
    for prefix in ['https://instagram.com/', 'https://www.instagram.com/', 'http://instagram.com/', 'instagram.com/']:
        if handle.lower().startswith(prefix):
            handle = handle[len(prefix):]
    handle = handle.rstrip('/')
    return handle

def normalize_neighborhood(name):
    if not name:
        return name
    name = name.strip()
    return NEIGHBORHOOD_MERGE.get(name, name)

def normalize_category(cat):
    if not cat:
        return cat
    cat = cat.strip()
    if cat in STANDARD_CATEGORIES:
        return cat
    mapped = CATEGORY_MAP.get(cat.lower())
    if mapped:
        return mapped
    return cat

def fuzzy_match(name, candidates, threshold=0.85):
    """Find best fuzzy match for name in candidates dict keyed by name_ar"""
    if not name:
        return None
    best_match = None
    best_score = 0
    for cand_name in candidates:
        score = SequenceMatcher(None, name, cand_name).ratio()
        if score > best_score and score >= threshold:
            best_score = score
            best_match = cand_name
    return best_match

# ─── Load all data ───
print("Loading data...")
places = load_json('places.json')
enriched_base = load_json('enriched-base.json')
enriched_rest = load_json('enriched-restaurants-1.json')
enriched_ent = load_json('enriched-entertainment.json')
enriched_hotels = load_json('enriched-hotels-chalets.json')

print(f"  places.json: {len(places)}")
print(f"  enriched-base: {len(enriched_base)}")
print(f"  enriched-restaurants-1: {len(enriched_rest)}")
print(f"  enriched-entertainment: {len(enriched_ent)}")
print(f"  enriched-hotels-chalets: {len(enriched_hotels)}")

# ─── Build enrichment lookup ───
# Index enrichment data by name (Arabic)
enrichment_by_name = {}

def add_enrichment(entries, source_name):
    for e in entries:
        name = e.get('name') or e.get('name_ar')
        if name:
            enrichment_by_name[name] = {**enrichment_by_name.get(name, {}), **e, '_source': source_name}

add_enrichment(enriched_base, 'enriched-base')
add_enrichment(enriched_rest, 'enriched-restaurants-1')
add_enrichment(enriched_ent, 'enriched-entertainment')
add_enrichment(enriched_hotels, 'enriched-hotels-chalets')

print(f"  Total enrichment entries: {len(enrichment_by_name)}")

# ─── STEP 1: Normalize ───
print("\n=== NORMALIZING ===")

# Coordinate normalization: consolidate lng/lon
lon_fixed = 0
for p in places:
    if p.get('lon') and not p.get('lng'):
        p['lng'] = p['lon']
        lon_fixed += 1
    if 'lon' in p:
        del p['lon']
print(f"  Fixed {lon_fixed} lon→lng")

# Normalize categories
cat_changes = 0
for p in places:
    old = p.get('category')
    new = normalize_category(old)
    if new != old:
        p['category'] = new
        cat_changes += 1
    p['category_ar'] = p['category']
print(f"  Category normalizations: {cat_changes}")

# Normalize neighborhoods
hood_changes = 0
for p in places:
    old = p.get('neighborhood')
    new = normalize_neighborhood(old)
    if new != old:
        p['neighborhood'] = new
        hood_changes += 1
print(f"  Neighborhood normalizations: {hood_changes}")

# Normalize phones
phone_changes = 0
for p in places:
    if p.get('phone'):
        old = p['phone']
        p['phone'] = normalize_phone(old)
        if p['phone'] != old:
            phone_changes += 1
print(f"  Phone normalizations: {phone_changes}")

# Normalize Instagram
ig_changes = 0
for p in places:
    if p.get('instagram'):
        old = p['instagram']
        p['instagram'] = normalize_instagram(old)
        if p['instagram'] != old:
            ig_changes += 1
print(f"  Instagram normalizations: {ig_changes}")

# ─── STEP 2: Merge enrichment data ───
print("\n=== MERGING ENRICHMENT DATA ===")

# Field mapping from enrichment → places
FIELD_MAP = {
    'phone': 'phone',
    'hours': 'opening_hours',
    'website': 'website',
    'instagram': 'instagram',
    'cuisine': 'cuisine',
    'description_ar': 'description_ar',
    'perfect_for': 'perfect_for',
    'address_ar': 'address_ar',
    'entry_fee': 'entry_fee',
    'kid_friendly': 'kid_friendly',
    'family_friendly': 'family_friendly',
    'amenities': 'amenities',
    'booking_url': 'booking_url',
    'check_in': 'check_in',
    'check_out': 'check_out',
    'rating_count': 'review_count',
}

matched = 0
fields_filled = Counter()
unmatched_enrichment = []

# Build places index by name_ar
places_by_name = {p.get('name_ar', ''): i for i, p in enumerate(places)}

for enrich_name, enrich_data in enrichment_by_name.items():
    # Try exact match first
    idx = places_by_name.get(enrich_name)
    
    # Try fuzzy match
    if idx is None:
        fuzzy = fuzzy_match(enrich_name, places_by_name.keys())
        if fuzzy:
            idx = places_by_name[fuzzy]
    
    if idx is not None:
        matched += 1
        p = places[idx]
        
        for src_field, dst_field in FIELD_MAP.items():
            val = enrich_data.get(src_field)
            if val and val not in [None, '', [], 0]:
                existing = p.get(dst_field)
                if not existing or existing in [None, '', [], 0]:
                    # Normalize before setting
                    if dst_field == 'phone':
                        val = normalize_phone(val)
                    elif dst_field == 'instagram':
                        val = normalize_instagram(val)
                    p[dst_field] = val
                    fields_filled[dst_field] += 1
    else:
        unmatched_enrichment.append(enrich_name)

print(f"  Matched: {matched}/{len(enrichment_by_name)}")
print(f"  Unmatched: {len(unmatched_enrichment)}")
print(f"  Fields filled:")
for field, count in fields_filled.most_common():
    print(f"    {field}: +{count}")

# ─── STEP 3: AI-Ready Features ───
print("\n=== GENERATING AI FEATURES ===")

# Completeness scoring weights
COMPLETENESS_FIELDS = {
    'google_rating': 10,
    'phone': 8,
    'website': 7,
    'instagram': 6,
    'description_ar': 15,
    'lat': 5,
    'lng': 5,
    'opening_hours': 8,
    'price_level': 5,
    'google_maps_url': 3,
    'image_url': 8,
    'tags': 7,
    'neighborhood': 5,
    'review_count': 4,
    'perfect_for': 4,
}
MAX_SCORE = sum(COMPLETENESS_FIELDS.values())

for p in places:
    # tags_combined: merge tags + perfect_for + audience + cuisine
    tags = set()
    for t in (p.get('tags') or []):
        if isinstance(t, str):
            tags.add(t)
    for t in (p.get('perfect_for') or []):
        if isinstance(t, str):
            tags.add(t)
    for t in (p.get('audience') or []):
        if isinstance(t, str):
            tags.add(t)
    if p.get('cuisine'):
        if isinstance(p['cuisine'], list):
            tags.update(p['cuisine'])
        elif isinstance(p['cuisine'], str):
            tags.add(p['cuisine'])
    if p.get('category'):
        tags.add(p['category'])
    p['tags_combined'] = sorted(tags)
    
    # search_text
    parts = []
    for field in ['name_ar', 'name_en', 'description_ar', 'neighborhood', 'category']:
        v = p.get(field)
        if v and isinstance(v, str):
            parts.append(v)
    for t in p.get('tags_combined', []):
        parts.append(t)
    p['search_text'] = ' '.join(parts)
    
    # category_score: rating × log(review_count + 1) for ranking
    rating = p.get('google_rating') or 0
    reviews = p.get('review_count') or 0
    if rating > 0:
        p['category_score'] = round(rating * math.log(reviews + 2), 2)
    else:
        p['category_score'] = 0
    
    # completeness_score
    score = 0
    for field, weight in COMPLETENESS_FIELDS.items():
        v = p.get(field)
        if v and v not in [None, '', [], 0]:
            score += weight
    p['completeness_score'] = round(score / MAX_SCORE * 100)
    
    # embedding_ready: has enough text
    text_len = len(p.get('search_text', ''))
    has_name = bool(p.get('name_ar'))
    has_desc = bool(p.get('description_ar'))
    p['embedding_ready'] = has_name and has_desc and text_len > 50

embed_ready = sum(1 for p in places if p.get('embedding_ready'))
avg_completeness = sum(p.get('completeness_score', 0) for p in places) / len(places)
print(f"  Embedding ready: {embed_ready}/{len(places)} ({round(embed_ready/len(places)*100, 1)}%)")
print(f"  Average completeness: {avg_completeness:.1f}%")

# ─── STEP 4: Statistics Report ───
print("\n=== GENERATING REPORT ===")

def has_value(p, field):
    v = p.get(field)
    return v is not None and v != '' and v != [] and v != 0

report = {
    'generated_at': '2026-02-20T22:30:00Z',
    'total_places': len(places),
    'places_by_category': {},
    'avg_rating_by_category': {},
    'top_neighborhoods': [],
    'field_completeness': {},
    'fields_most_null': [],
    'rating_distribution': {},
    'completeness_distribution': {},
    'embedding_ready_count': embed_ready,
    'ai_features_added': ['tags_combined', 'search_text', 'category_score', 'completeness_score', 'embedding_ready'],
    'enrichment_merge_stats': {
        'matched': matched,
        'unmatched': len(unmatched_enrichment),
        'fields_filled': dict(fields_filled),
    },
}

# By category
cat_ratings = defaultdict(list)
cat_counts = Counter()
for p in places:
    cat = p.get('category', 'UNKNOWN')
    cat_counts[cat] += 1
    r = p.get('google_rating')
    if r:
        cat_ratings[cat].append(r)

report['places_by_category'] = dict(cat_counts.most_common())
report['avg_rating_by_category'] = {
    cat: round(sum(rs)/len(rs), 2)
    for cat, rs in sorted(cat_ratings.items())
    if rs
}

# Top neighborhoods
hood_counts = Counter()
for p in places:
    h = p.get('neighborhood')
    if h:
        hood_counts[h] += 1
report['top_neighborhoods'] = [
    {'neighborhood': h, 'count': c}
    for h, c in hood_counts.most_common(30)
]

# Field completeness
check_fields = [
    'google_rating', 'phone', 'website', 'instagram', 'description_ar',
    'lat', 'lng', 'opening_hours', 'price_range', 'price_level',
    'google_maps_url', 'image_url', 'tags', 'review_count', 'perfect_for',
    'audience', 'neighborhood', 'name_en', 'tags_combined'
]
for field in check_fields:
    count = sum(1 for p in places if has_value(p, field))
    report['field_completeness'][field] = {
        'count': count,
        'total': len(places),
        'percentage': round(count / len(places) * 100, 1)
    }

# Fields most null (sorted by % null descending)
report['fields_most_null'] = sorted(
    [{'field': f, 'null_pct': round(100 - d['percentage'], 1)} for f, d in report['field_completeness'].items()],
    key=lambda x: -x['null_pct']
)

# Rating distribution
rating_bins = {'0-2': 0, '2-3': 0, '3-3.5': 0, '3.5-4': 0, '4-4.5': 0, '4.5-5': 0, 'no_rating': 0}
for p in places:
    r = p.get('google_rating')
    if r is None:
        rating_bins['no_rating'] += 1
    elif r < 2:
        rating_bins['0-2'] += 1
    elif r < 3:
        rating_bins['2-3'] += 1
    elif r < 3.5:
        rating_bins['3-3.5'] += 1
    elif r < 4:
        rating_bins['3.5-4'] += 1
    elif r < 4.5:
        rating_bins['4-4.5'] += 1
    else:
        rating_bins['4.5-5'] += 1
report['rating_distribution'] = rating_bins

# Completeness distribution
comp_bins = {'0-20': 0, '20-40': 0, '40-60': 0, '60-80': 0, '80-100': 0}
for p in places:
    cs = p.get('completeness_score', 0)
    if cs < 20:
        comp_bins['0-20'] += 1
    elif cs < 40:
        comp_bins['20-40'] += 1
    elif cs < 60:
        comp_bins['40-60'] += 1
    elif cs < 80:
        comp_bins['60-80'] += 1
    else:
        comp_bins['80-100'] += 1
report['completeness_distribution'] = comp_bins

# ─── STEP 5: Save ───
print("\n=== SAVING ===")
save_json('places.json', places)
save_json('analysis-report.json', report)

# Generate places-light.json (subset of fields for frontend)
LIGHT_FIELDS = [
    'id', 'name_ar', 'name_en', 'category', 'category_ar', 'category_en',
    'neighborhood', 'neighborhood_en', 'google_rating', 'price_level',
    'lat', 'lng', 'google_maps_url', 'image_url', 'trending', 'is_new',
    'tags_combined', 'completeness_score', 'embedding_ready',
    'description_ar', 'phone', 'website', 'instagram', 'opening_hours',
    'review_count', 'perfect_for', 'audience', 'category_score'
]

places_light = []
for p in places:
    light = {k: p.get(k) for k in LIGHT_FIELDS if p.get(k) is not None}
    places_light.append(light)

save_json('places-light.json', places_light)

print("\n=== SUMMARY ===")
print(f"Total places: {len(places)}")
print(f"Embedding ready: {embed_ready} ({round(embed_ready/len(places)*100,1)}%)")
print(f"Avg completeness: {avg_completeness:.1f}%")
print(f"Enrichment matched: {matched}")
print(f"Fields added per enrichment match (top):")
for f, c in fields_filled.most_common(5):
    print(f"  {f}: +{c}")
print("\nDone!")
