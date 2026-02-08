#!/usr/bin/env python3
"""
Tag places.json with Ramadan attributes intelligently.

Logic:
- Hotels/فنادق → ramadan_iftar + ramadan_tent (likely have iftar tents)
- Restaurants ($$$ / $$$$, rating ≥ 4.3) → ramadan_iftar
- Restaurants with "بوفيه" or "عربي" → ramadan_iftar
- Late-night cafes → ramadan_suhoor
- All cafes → ramadan_suhoor (most stay open late in Ramadan)
- Dessert shops → ramadan_suhoor + ramadan_special (حلويات رمضانية)
- Malls/مولات → ramadan_special (تسوق رمضاني)
- Any place with Ramadan in name/desc → appropriate tags
"""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PLACES_PATH = os.path.join(PROJECT_DIR, 'data', 'places.json')

# Keywords for detection
IFTAR_KEYWORDS = ['إفطار', 'بوفيه', 'عربي', 'مشاوي', 'مندي', 'كبسة', 'مطبق', 'قرصان',
                  'تركي', 'لبناني', 'مصري', 'هندي', 'باكستاني', 'يمني', 'شرقي',
                  'فاخر', 'فخم', 'عائلي', 'عوائل', 'بخاري', 'حنيذ', 'مظبي']

SUHOOR_KEYWORDS = ['سحور', 'ليلي', 'فطور', 'شاي', 'معسل', 'شيشة',
                   'لاونج', 'lounge', 'midnight', 'بانكيك', '24']

TENT_KEYWORDS = ['خيمة', 'خيم', 'tent', 'رمضان', 'مجلس', 'جلسة خارجية']

SWEET_KEYWORDS = ['كنافة', 'قطايف', 'لقيمات', 'حلويات', 'حلى', 'بسبوسة', 'معمول',
                  'تمر', 'شوكولاتة', 'كيك', 'آيس كريم', 'جيلاتو', 'تشيز']

# Hotel names/brands that likely have Ramadan tents
HOTEL_KEYWORDS = ['فندق', 'hotel', 'ريتز', 'ritz', 'فور سيزونز', 'four seasons',
                  'هيلتون', 'hilton', 'ماريوت', 'marriott', 'كراون', 'crown',
                  'شيراتون', 'sheraton', 'فيرمونت', 'fairmont', 'رافلز', 'raffles',
                  'نارسيس', 'narcissus', 'موفنبيك', 'movenpick', 'حياة', 'hyatt',
                  'انتركونتيننتال', 'intercontinental', 'ألوفت', 'aloft',
                  'روزوود', 'rosewood', 'ماندارين', 'mandarin']

def has_keywords(text, keywords):
    """Check if text contains any of the keywords (case-insensitive)."""
    if not text:
        return False
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def tag_place(place):
    """Determine Ramadan tags for a single place."""
    name = place.get('name_ar', '') + ' ' + place.get('name_en', '')
    desc = place.get('description_ar', '')
    category = place.get('category', '')
    cat_en = place.get('category_en', '')
    rating = place.get('google_rating', 0)
    price = place.get('price_level', '')
    full_text = f"{name} {desc}".lower()

    tags = {
        'ramadan_iftar': False,
        'ramadan_suhoor': False,
        'ramadan_tent': False,
        'ramadan_special': None
    }

    # ===== Hotels → Iftar + Tent =====
    if category == 'فنادق' or has_keywords(name, HOTEL_KEYWORDS):
        tags['ramadan_iftar'] = True
        tags['ramadan_tent'] = True
        tags['ramadan_special'] = 'بوفيه إفطار فندقي فاخر وخيمة رمضانية'

    # ===== Restaurants =====
    elif category in ['مطعم']:
        # High-end restaurants → iftar
        if price in ['$$$', '$$$$'] and rating >= 4.3:
            tags['ramadan_iftar'] = True
            tags['ramadan_special'] = 'وجهة مميزة للإفطار الرمضاني'

        # Arabic/Middle Eastern restaurants → iftar
        if has_keywords(full_text, IFTAR_KEYWORDS):
            tags['ramadan_iftar'] = True
            if not tags['ramadan_special']:
                tags['ramadan_special'] = 'مطعم مناسب للإفطار الرمضاني'

        # All decent restaurants can be iftar spots
        if rating >= 4.4 and price in ['$$', '$$$', '$$$$']:
            tags['ramadan_iftar'] = True

        # Restaurants that might also serve suhoor
        if has_keywords(full_text, SUHOOR_KEYWORDS) or '24' in full_text:
            tags['ramadan_suhoor'] = True

    # ===== Cafes → Suhoor =====
    elif category in ['كافيه']:
        tags['ramadan_suhoor'] = True
        tags['ramadan_special'] = 'مفتوح للسحور والتحلية بعد التراويح'

        # Cafes with food can also be iftar
        if has_keywords(full_text, ['فطور', 'وجبات', 'سندويش', 'برغر', 'بيتزا']):
            tags['ramadan_iftar'] = True

    # ===== Desserts → Suhoor sweets =====
    elif category in ['حلويات']:
        tags['ramadan_suhoor'] = True
        if has_keywords(full_text, ['كنافة', 'قطايف', 'لقيمات', 'بسبوسة']):
            tags['ramadan_special'] = 'حلويات رمضانية تقليدية'
        else:
            tags['ramadan_special'] = 'حلويات وتحلية بعد الإفطار'

    # ===== Malls =====
    elif category in ['تسوق', 'مولات']:
        tags['ramadan_special'] = 'تسوق رمضاني — ساعات عمل ممتدة في رمضان'

    # ===== Activities/Entertainment =====
    elif category in ['ترفيه', 'فعاليات']:
        if has_keywords(full_text, ['رمضان', 'ليل', 'مساء', 'أمسية']):
            tags['ramadan_special'] = 'فعاليات رمضانية خاصة'

    # ===== Check for tent keywords in any category =====
    if has_keywords(full_text, TENT_KEYWORDS) and not tags['ramadan_tent']:
        tags['ramadan_tent'] = True

    # ===== Nature/Parks — good for post-iftar walks =====
    if category in ['طبيعة'] and rating >= 4.3:
        tags['ramadan_special'] = 'مناسب للمشي بعد الإفطار'

    # Clean up: remove None values for non-special
    result = {}
    if tags['ramadan_iftar']:
        result['ramadan_iftar'] = True
    if tags['ramadan_suhoor']:
        result['ramadan_suhoor'] = True
    if tags['ramadan_tent']:
        result['ramadan_tent'] = True
    if tags['ramadan_special']:
        result['ramadan_special'] = tags['ramadan_special']

    return result


def main():
    print("🌙 Tagging places with Ramadan attributes...")

    with open(PLACES_PATH, 'r', encoding='utf-8') as f:
        places = json.load(f)

    stats = {'iftar': 0, 'suhoor': 0, 'tent': 0, 'special': 0, 'any': 0}

    for place in places:
        # Remove old ramadan tags first
        for key in ['ramadan_iftar', 'ramadan_suhoor', 'ramadan_tent', 'ramadan_special']:
            place.pop(key, None)

        tags = tag_place(place)

        if tags:
            place.update(tags)
            stats['any'] += 1
            if tags.get('ramadan_iftar'): stats['iftar'] += 1
            if tags.get('ramadan_suhoor'): stats['suhoor'] += 1
            if tags.get('ramadan_tent'): stats['tent'] += 1
            if tags.get('ramadan_special'): stats['special'] += 1

    # Save updated places
    with open(PLACES_PATH, 'w', encoding='utf-8') as f:
        json.dump(places, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Tagged {stats['any']}/{len(places)} places:")
    print(f"   🍽️  إفطار (iftar):  {stats['iftar']}")
    print(f"   🌙 سحور (suhoor):  {stats['suhoor']}")
    print(f"   ⛺ خيمة (tent):    {stats['tent']}")
    print(f"   ✨ خاص (special):  {stats['special']}")

    # Show sample tagged places
    print("\n📋 Sample tagged places:")
    shown = 0
    for place in places:
        if place.get('ramadan_iftar') or place.get('ramadan_tent'):
            tags = []
            if place.get('ramadan_iftar'): tags.append('إفطار')
            if place.get('ramadan_suhoor'): tags.append('سحور')
            if place.get('ramadan_tent'): tags.append('خيمة')
            print(f"   {place['name_ar']} ({place['category']}) — {', '.join(tags)}")
            shown += 1
            if shown >= 15:
                break


if __name__ == '__main__':
    main()
