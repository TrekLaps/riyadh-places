#!/usr/bin/env python3
"""Add price_range to restaurants, cafes, and sweets shops in Riyadh places data."""
import json, os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "places.json")
valid_prices = {'$', '$$', '$$$', '$$$$'}

chains_sure = {
    '$': [
        'ماكدونالدز', 'ماكدونلدز', "McDonald", 'برجر كنج', 'Burger King',
        'كنتاكي', 'KFC', 'هارديز', 'Hardee', 'صب واي', 'Subway',
        'دومينوز', 'Domino', 'بيتزا هت', 'Pizza Hut', 'ليتل سيزرز', 'Little Caesar',
        'باباجونز', 'Papa John', 'بوبايز', 'Popeye', 'دجاج تكساس', 'Texas Chicken',
        'شاورمر', 'Shawarmer', 'كودو', 'Kudu', 'هرفي', 'Herfy',
        'الطازج', 'Tazaj', 'Al Tazaj', 'البيك', 'Al Baik', 'Albaik',
        'الرومانسية', 'Al Romansiah', 'ماما نورة', 'Mama Noura',
        'باسكن روبنز', 'Baskin Robbins', 'سينابون', 'Cinnabon',
        'دانكن', 'Dunkin', 'تيم هورتنز', 'Tim Horton',
        'ديري كوين', 'Dairy Queen', 'Krispy', 'كرسبي',
        'Gad ', 'جاد', 'Pizza Inn', 'Pizza Company', 'Pizza Fusion', 'Pizza Jarir',
        'Shawaya', 'شوايا',
    ],
    '$$': [
        'آبل بيز', 'Applebee', 'تشيليز', 'Chili', 'فرايديز', 'Friday',
        'شيك شاك', 'Shake Shack', 'فايف غايز', 'Five Guys',
        'بي إف تشانغز', 'P.F. Chang', 'واقامام', 'Wagamama',
        'مادو', 'Mado', 'ستاربكس', 'Starbucks', 'كاريبو', 'Caribou',
        'كوستا', 'Costa', 'بول', 'Paul', 'دوز كافيه', 'Dose',
        'سعد الدين', 'Saadeddin', 'Saadiddin', 'جوديفا', 'Godiva',
        'باتشي', 'Patchi', 'عبد الرحمن الحلاب', 'Abdul Rahman Hallab', 'حلاب',
        'Vapiano', 'فابيانو', 'Barbecue Nation', 'باربكيو نيشن',
        'د.كيف', 'Dr.Cafe', 'dr-cafe', 'Java Cafe', 'جافا كافيه',
        'Eric Kayser', 'ايريك قيصر', 'Shakespeare', 'شكسبير',
    ],
    '$$$': [
        'ذا غريل', 'The Grill', 'أنتركوت', 'Entrecote', 'إنتركوت',
        'نوبو', 'Nobu', 'زوما', 'Zuma', 'هاكاسان', 'Hakkasan',
        'LPM', 'إل بي إم', 'فيا رياض', 'Via Riyadh',
        'كارلوتشيو', 'Carluccio',
    ],
    '$$$$': [
        'نوزومي', 'Nozomi', 'نصرت', 'Nusr-Et', 'بيير', 'Pierre',
    ],
}

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

target_cats = {'مطعم', 'كافيه', 'حلويات'}
s1 = s2 = s3 = already = 0

for p in data:
    if p.get('category') not in target_cats:
        continue
    
    pr = p.get('price_range')
    if pr and pr not in valid_prices:
        p['price_range'] = None
        pr = None
    
    if pr and pr in valid_prices:
        already += 1
        continue
    
    name = f"{p.get('name_ar','')} {p.get('name_en','')}".lower()
    
    pl = p.get('price_level')
    if pl and pl in valid_prices:
        p['price_range'] = pl
        s1 += 1
        continue
    
    matched = False
    for price in ['$$$$','$$$','$$','$']:
        for kw in chains_sure.get(price, []):
            if kw.lower() in name:
                p['price_range'] = price
                s2 += 1
                matched = True
                break
        if matched:
            break
    if matched:
        continue
    
    if any(w in name for w in ['شاورما', 'shawarma', 'shawerma', 'فلافل', 'falafel',
                                'فول', 'كشري', 'koushari', 'بروست', 'broast',
                                'فطائر', 'فطيرة', 'fateera', 'سمبوسة',
                                'معجنات', 'بسطة', 'كباب', 'kebab',
                                'مندي', 'mandi', 'مظبي', 'حنيذ',
                                'بخاري', 'bukhari', 'برجر', 'burger',
                                'دونات', 'donut', 'آيس كريم', 'ice cream']):
        p['price_range'] = '$'
        s3 += 1
    elif any(w in name for w in ['لبناني', 'lebanese', 'lebanon', 'تركي', 'turkish',
                                  'هندي', 'indian', 'صيني', 'chinese',
                                  'سوشي', 'sushi', 'إيطالي', 'italian',
                                  'بحري', 'seafood', 'سمك', 'fish',
                                  'لاونج', 'lounge', 'كافيه', 'cafe',
                                  'كوفي', 'coffee', 'قهوة',
                                  'بيكري', 'bakery', 'مخبز',
                                  'حلويات', 'sweets', 'شوكولا', 'chocolate',
                                  'كنافة', 'كيك', 'cake']):
        p['price_range'] = '$$'
        s3 += 1
    elif any(w in name for w in ['ستيك', 'steak', 'واقيو', 'wagyu',
                                  'بيسترو', 'bistro', 'تراتوريا', 'trattoria',
                                  'فندق', 'hotel', 'هيلتون', 'hilton',
                                  'ماريوت', 'marriott', 'شيراتون', 'sheraton',
                                  'كراون بلازا', 'crown plaza']):
        p['price_range'] = '$$$'
        s3 += 1

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

all_targets = [p for p in data if p.get('category') in target_cats]
has_pr = sum(1 for p in all_targets if p.get('price_range') in valid_prices)
print(f"Already had: {already}")
print(f"Google price_level: {s1}")
print(f"Known chains: {s2}")
print(f"Name heuristics: {s3}")
print(f"Total with price_range: {has_pr} / {len(all_targets)} ({has_pr/len(all_targets)*100:.1f}%)")

from collections import Counter
pr = Counter(p.get('price_range') for p in all_targets if p.get('price_range') in valid_prices)
for k,v in pr.most_common():
    print(f"  {k}: {v}")
