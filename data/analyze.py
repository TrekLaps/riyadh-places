#!/usr/bin/env python3
"""Comprehensive analysis of Riyadh places data."""
import json
from collections import Counter, defaultdict

with open('/home/ubuntu/.openclaw/workspace/projects/riyadh-places/data/places.json', 'r') as f:
    data = json.load(f)

PRICE_MAP = {'مجاني': 0, 'free': 0, '$': 1, '$$': 2, '$$$': 3, '$$$$': 4}

def price_num(p):
    return PRICE_MAP.get(p.get('price_level','$$'), 2)

def value_score(p):
    """Higher rating + lower price = better value."""
    r = p.get('google_rating', 0) or 0
    pn = price_num(p)
    return r / max(pn, 0.5)  # avoid div by zero

def is_family(p):
    return 'عوائل' in p.get('audience', [])

def top_n(items, key, n=10, reverse=True):
    return sorted(items, key=key, reverse=reverse)[:n]

# ==========================================
# 1. Best 10 per category
# ==========================================
categories = defaultdict(list)
for p in data:
    categories[p['category']].append(p)

cat_analysis = {}
for cat, places in categories.items():
    cat_analysis[cat] = {
        'count': len(places),
        'top_rating': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'], 
                        'price': p['price_level'], 'neighborhood': p['neighborhood']}
                       for p in top_n(places, lambda x: x.get('google_rating', 0))],
        'top_value': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                       'price': p['price_level'], 'neighborhood': p['neighborhood'], 'value_score': round(value_score(p), 2)}
                      for p in top_n(places, value_score)],
        'top_family': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                        'price': p['price_level'], 'neighborhood': p['neighborhood']}
                       for p in top_n([x for x in places if is_family(x)], lambda x: x.get('google_rating', 0))],
        'top_new': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                     'price': p['price_level'], 'neighborhood': p['neighborhood']}
                    for p in top_n([x for x in places if x.get('is_new')], lambda x: x.get('google_rating', 0))],
    }

# ==========================================
# 2. Neighborhood analysis
# ==========================================
neighborhoods = defaultdict(list)
for p in data:
    neighborhoods[p['neighborhood']].append(p)

# Focus on neighborhoods with >= 20 places
major_hoods = {k: v for k, v in neighborhoods.items() if len(v) >= 20}

hood_analysis = {}
for hood, places in sorted(major_hoods.items(), key=lambda x: -len(x[1])):
    ratings = [p['google_rating'] for p in places if p.get('google_rating')]
    cat_counts = Counter(p['category'] for p in places)
    price_counts = Counter(p['price_level'] for p in places)
    
    hood_analysis[hood] = {
        'count': len(places),
        'avg_rating': round(sum(ratings)/len(ratings), 2) if ratings else 0,
        'top_category': cat_counts.most_common(1)[0] if cat_counts else None,
        'dominant_price': price_counts.most_common(1)[0] if price_counts else None,
        'top_5': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                   'category': p['category'], 'price': p['price_level']}
                  for p in top_n(places, lambda x: x.get('google_rating', 0), 5)],
        'category_breakdown': dict(cat_counts.most_common()),
        'price_breakdown': dict(price_counts.most_common()),
    }

# ==========================================
# 3. Price analysis
# ==========================================
# Distribution by category
price_by_cat = {}
for cat, places in categories.items():
    price_by_cat[cat] = dict(Counter(p['price_level'] for p in places).most_common())

# Most expensive
has_price = [p for p in data if p.get('price_level') == '$$$$']
most_expensive = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                   'price': p['price_level'], 'category': p['category'], 'neighborhood': p['neighborhood']}
                  for p in top_n(has_price, lambda x: x.get('google_rating', 0))]

# Cheapest with high rating
cheap_good = [p for p in data if p.get('google_rating', 0) > 4.0 and p.get('price_level') in ('$', 'مجاني', 'free')]
cheapest_highrated = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                       'price': p['price_level'], 'category': p['category'], 'neighborhood': p['neighborhood']}
                      for p in top_n(cheap_good, lambda x: x.get('google_rating', 0))]

# Best value overall
best_value_all = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                   'price': p['price_level'], 'category': p['category'], 'neighborhood': p['neighborhood'],
                   'value_score': round(value_score(p), 2)}
                  for p in top_n(data, value_score)]

# ==========================================
# 4. Comparisons
# ==========================================
comparisons = []

# 4.1 Best cafe: العليا vs الملقا vs حطين
def best_in_hood_cat(hood_names, cat):
    results = {}
    for hood in hood_names:
        # match partial - some have حي prefix
        matches = [p for p in data if cat in p['category'] and hood in p['neighborhood']]
        if matches:
            best = max(matches, key=lambda x: x.get('google_rating', 0))
            results[hood] = {'name_ar': best['name_ar'], 'name_en': best['name_en'], 
                            'rating': best['google_rating'], 'price': best['price_level'],
                            'neighborhood': best['neighborhood']}
    return results

comp_cafe_hoods = best_in_hood_cat(['العليا', 'الملقا', 'حطين'], 'كافيه')
comparisons.append({
    'title': 'أفضل كافيه: العليا vs الملقا vs حطين',
    'data': comp_cafe_hoods
})

# 4.2 Best Japanese restaurants
japanese = [p for p in data if 'ياباني' in p.get('description_ar', '').lower() or 'japanese' in p.get('name_en', '').lower() 
            or 'sushi' in p.get('name_en', '').lower() or 'سوشي' in p.get('name_ar', '') or 'ياباني' in p.get('name_ar', '')]
comp_japanese = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                  'price': p['price_level'], 'neighborhood': p['neighborhood']}
                 for p in top_n(japanese, lambda x: x.get('google_rating', 0), 5)]
comparisons.append({
    'title': 'أفضل المطاعم اليابانية',
    'data': comp_japanese
})

# 4.3 Best breakfast places
breakfast = [p for p in data if 'فطور' in p.get('description_ar', '') or 'فطور' in str(p.get('perfect_for', []))
             or 'breakfast' in p.get('name_en', '').lower() or 'فطور' in p.get('name_ar', '')]
comp_breakfast = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                   'price': p['price_level'], 'neighborhood': p['neighborhood'], 'category': p['category']}
                  for p in top_n(breakfast, lambda x: x.get('google_rating', 0), 10)]
comparisons.append({
    'title': 'أفضل أماكن الفطور',
    'data': comp_breakfast
})

# 4.4 Best romantic places
romantic = [p for p in data if 'رومانسي' in p.get('description_ar', '') or 'أزواج' in str(p.get('audience', []))
            or 'رومانسية' in p.get('description_ar', '')]
comp_romantic = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                  'price': p['price_level'], 'neighborhood': p['neighborhood'], 'category': p['category']}
                 for p in top_n(romantic, lambda x: x.get('google_rating', 0), 10)]
comparisons.append({
    'title': 'أفضل الأماكن الرومانسية',
    'data': comp_romantic
})

# 4.5 Best places for kids
kids = [p for p in data if 'أطفال' in p.get('description_ar', '') or 'أطفال' in str(p.get('perfect_for', []))
        or 'kids' in p.get('name_en', '').lower() or 'أطفال' in str(p.get('audience', []))]
comp_kids = [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
              'price': p['price_level'], 'neighborhood': p['neighborhood'], 'category': p['category']}
             for p in top_n(kids, lambda x: x.get('google_rating', 0), 10)]
comparisons.append({
    'title': 'أفضل الأماكن للأطفال',
    'data': comp_kids
})

# 4.6 Best restaurant: العليا vs الملقا vs حطين
comp_rest_hoods = best_in_hood_cat(['العليا', 'الملقا', 'حطين'], 'مطعم')
comparisons.append({
    'title': 'أفضل مطعم: العليا vs الملقا vs حطين',
    'data': comp_rest_hoods
})

# 4.7 Best entertainment: indoor vs outdoor
indoor_ent = [p for p in data if p['category'] == 'ترفيه' and ('داخلي' in p.get('description_ar','') or 'مول' in p.get('neighborhood',''))]
outdoor_ent = [p for p in data if p['category'] == 'ترفيه' and ('خارجي' in p.get('description_ar','') or 'طبيعة' in p.get('description_ar','') or 'حديقة' in p.get('description_ar',''))]
comparisons.append({
    'title': 'ترفيه داخلي vs خارجي',
    'data': {
        'indoor_top5': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                         'price': p['price_level']} for p in top_n(indoor_ent, lambda x: x.get('google_rating',0), 5)],
        'outdoor_top5': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                          'price': p['price_level']} for p in top_n(outdoor_ent, lambda x: x.get('google_rating',0), 5)],
    }
})

# 4.8 Best sweets shops by neighborhood
comp_sweets = best_in_hood_cat(['العليا', 'الملقا', 'حطين', 'الياسمين'], 'حلويات')
comparisons.append({
    'title': 'أفضل حلويات حسب الحي',
    'data': comp_sweets
})

# 4.9 Free vs paid entertainment
free_ent = [p for p in data if p['category'] == 'ترفيه' and (p.get('is_free') or p.get('price_level') in ('مجاني', 'free'))]
paid_ent = [p for p in data if p['category'] == 'ترفيه' and not p.get('is_free') and p.get('price_level') not in ('مجاني', 'free')]
comparisons.append({
    'title': 'ترفيه مجاني vs مدفوع',
    'data': {
        'free_top5': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating']} 
                      for p in top_n(free_ent, lambda x: x.get('google_rating',0), 5)],
        'paid_top5': [{'name_ar': p['name_ar'], 'name_en': p['name_en'], 'rating': p['google_rating'],
                       'price': p['price_level']} for p in top_n(paid_ent, lambda x: x.get('google_rating',0), 5)],
    }
})

# 4.10 Best hotel by price tier
hotels = [p for p in data if p['category'] == 'فنادق']
hotel_by_price = {}
for tier in ['$', '$$', '$$$', '$$$$']:
    tier_hotels = [p for p in hotels if p.get('price_level') == tier]
    if tier_hotels:
        best = max(tier_hotels, key=lambda x: x.get('google_rating', 0))
        hotel_by_price[tier] = {'name_ar': best['name_ar'], 'name_en': best['name_en'],
                                'rating': best['google_rating'], 'neighborhood': best['neighborhood']}
comparisons.append({
    'title': 'أفضل فندق حسب مستوى السعر',
    'data': hotel_by_price
})

# ==========================================
# Save structured JSON
# ==========================================
results = {
    'summary': {
        'total_places': len(data),
        'total_categories': len(categories),
        'total_neighborhoods': len(neighborhoods),
        'avg_rating': round(sum(p['google_rating'] for p in data if p.get('google_rating')) / len([p for p in data if p.get('google_rating')]), 2),
        'new_places': sum(1 for p in data if p.get('is_new')),
        'free_places': sum(1 for p in data if p.get('is_free')),
    },
    'categories': cat_analysis,
    'neighborhoods': hood_analysis,
    'price_analysis': {
        'distribution_by_category': price_by_cat,
        'most_expensive_top10': most_expensive,
        'cheapest_high_rated_top10': cheapest_highrated,
        'best_value_top10': best_value_all,
    },
    'comparisons': comparisons,
}

with open('/home/ubuntu/.openclaw/workspace/projects/riyadh-places/data/analysis-results.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ analysis-results.json saved")
print(json.dumps(results['summary'], ensure_ascii=False, indent=2))
