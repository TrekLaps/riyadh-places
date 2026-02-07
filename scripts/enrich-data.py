#!/usr/bin/env python3
"""Enrich places.json with lat/lng, audience, cuisine, is_free fields."""
import json
import random

# Riyadh neighborhood approximate coordinates
NEIGHBORHOOD_COORDS = {
    'حي العليا': (24.6907, 46.6850),
    'العليا': (24.6907, 46.6850),
    'حي الملقا': (24.7820, 46.6350),
    'الملقا': (24.7820, 46.6350),
    'حي الورود': (24.7180, 46.6750),
    'الورود': (24.7180, 46.6750),
    'حي الياسمين': (24.8080, 46.6280),
    'الياسمين': (24.8080, 46.6280),
    'حي النخيل': (24.7630, 46.6450),
    'النخيل': (24.7630, 46.6450),
    'حي الربيع': (24.7950, 46.6500),
    'الربيع': (24.7950, 46.6500),
    'حي الصحافة': (24.8000, 46.6700),
    'الصحافة': (24.8000, 46.6700),
    'حي حطين': (24.7450, 46.6150),
    'حطين': (24.7450, 46.6150),
    'حي النرجس': (24.8200, 46.6200),
    'النرجس': (24.8200, 46.6200),
    'حي السليمانية': (24.6780, 46.7050),
    'السليمانية': (24.6780, 46.7050),
    'حي العارض': (24.8300, 46.6400),
    'العارض': (24.8300, 46.6400),
    'حي الملك عبدالله المالي': (24.7670, 46.6430),
    'KAFD': (24.7670, 46.6430),
    'KAFD — المركز المالي': (24.7670, 46.6430),
    'حي الرائد': (24.7200, 46.6500),
    'حي المروج': (24.7350, 46.6700),
    'المروج': (24.7350, 46.6700),
    'حي العقيق': (24.7600, 46.6300),
    'حي الغدير': (24.7500, 46.6600),
    'حي القدس': (24.7100, 46.6900),
    'حي الملز': (24.6600, 46.7200),
    'حي المربع': (24.6500, 46.7100),
    'المربع': (24.6500, 46.7100),
    'حي النسيم': (24.6600, 46.7500),
    'حي السفارات': (24.6900, 46.6200),
    'السفارات': (24.6900, 46.6200),
    'حي الملك فهد': (24.7300, 46.6600),
    'الربوة': (24.6650, 46.7350),
    'حي الربوة': (24.6650, 46.7350),
    'الحمراء': (24.6700, 46.7100),
    'غرناطة': (24.7100, 46.7300),
    'الديرة': (24.6350, 46.7150),
    'البطحاء': (24.6350, 46.7100),
    'المعيقلية': (24.6320, 46.7130),
    'السويدي': (24.6150, 46.6700),
    'الشفا': (24.5700, 46.6800),
    'العزيزية': (24.6200, 46.7200),
    'السلام': (24.6900, 46.7400),
    'بوليفارد الرياض': (24.7500, 46.6200),
    'بوليفارد سيتي': (24.7500, 46.6250),
    'الدرعية': (24.7340, 46.5730),
    'حي الدرعية': (24.7340, 46.5730),
    'الثمامة': (24.8500, 46.7200),
    'نمار': (24.5500, 46.6200),
    'وادي لبن': (24.5800, 46.5900),
    'بانبان': (24.8700, 46.7500),
    'الجنادرية': (24.7500, 46.8200),
    'أشيقر': (25.3300, 45.2100),
    'شقراء': (25.2500, 45.2500),
    'الخرج': (24.1500, 47.3100),
    'جامعة الملك سعود': (24.7200, 46.6200),
    'مسرح محمد العلي': (24.7300, 46.6350),
    'ميدان الملك عبدالعزيز': (24.6400, 46.7100),
    'العثيم مول': (24.7700, 46.6950),
    'حي السحاب': (24.6300, 46.6600),
    'حي السلي': (24.6100, 46.7300),
    'الرياض فرونت': (24.5800, 46.6000),
    'الحي الدبلوماسي': (24.6950, 46.6150),
    'طريق الملك فهد': (24.7100, 46.6750),
    'فروع متعددة': (24.7136, 46.6753),
    'متعدد': (24.7136, 46.6753),
    'مواقع متعددة': (24.7136, 46.6753),
    'شمال الرياض': (24.8100, 46.6500),
    'جنوب الرياض': (24.5800, 46.6900),
    'غرب الرياض': (24.6500, 46.5800),
    'شمال شرق الرياض': (24.8000, 46.7200),
    'شمال غرب الرياض': (24.8100, 46.5800),
    'جنوب غرب الرياض': (24.5500, 46.6000),
    'وسط الرياض': (24.6500, 46.7100),
}

# Category-based audience defaults
CATEGORY_AUDIENCE = {
    'كافيه': ['شباب', 'أزواج'],
    'مطعم': ['عوائل', 'أزواج'],
    'ترفيه': ['عوائل', 'أطفال', 'شباب'],
    'تسوق': ['عوائل', 'شباب'],
    'طبيعة': ['عوائل', 'شباب', 'أطفال'],
    'حلويات': ['عوائل', 'أطفال'],
    'فعاليات': ['عوائل', 'شباب'],
}

# Cuisine mapping based on description keywords
CUISINE_KEYWORDS = {
    'تركي': 'تركي',
    'فرنسي': 'فرنسي',
    'إيطالي': 'إيطالي',
    'ياباني': 'ياباني',
    'صيني': 'صيني',
    'هندي': 'هندي',
    'مكسيكي': 'مكسيكي',
    'لبناني': 'لبناني',
    'أرمني': 'أرمني',
    'يمني': 'يمني',
    'سعودي': 'سعودي',
    'شعبي': 'سعودي',
    'شاورما': 'سعودي',
    'بيتزا': 'إيطالي',
    'باستا': 'إيطالي',
    'سوشي': 'ياباني',
    'كوري': 'كوري',
    'تايلندي': 'تايلندي',
    'بيروفي': 'لاتيني',
    'برازيلي': 'لاتيني',
    'مغربي': 'مغربي',
    'بحري': 'بحري',
    'أمريكي': 'أمريكي',
    'برجر': 'أمريكي',
    'ستيك': 'ستيك هاوس',
    'لحوم': 'ستيك هاوس',
    'مختصة': 'قهوة مختصة',
    'شوكولاتة': 'حلويات',
    'كيك': 'حلويات',
    'آيسكريم': 'حلويات',
    'دونات': 'حلويات',
    'بوظة': 'حلويات',
}

def get_coords(neighborhood):
    if neighborhood in NEIGHBORHOOD_COORDS:
        lat, lng = NEIGHBORHOOD_COORDS[neighborhood]
    else:
        # Default to Riyadh center with jitter
        lat, lng = 24.7136, 46.6753
    # Add small random offset to avoid overlapping markers
    lat += random.uniform(-0.005, 0.005)
    lng += random.uniform(-0.005, 0.005)
    return round(lat, 6), round(lng, 6)

def get_cuisine(place):
    if place['category'] != 'مطعم':
        return None
    desc = place.get('description_ar', '')
    name = place.get('name_ar', '')
    text = f"{desc} {name}"
    for keyword, cuisine in CUISINE_KEYWORDS.items():
        if keyword in text:
            return cuisine
    return 'عالمي'

def get_audience(place):
    base = CATEGORY_AUDIENCE.get(place['category'], ['عوائل', 'شباب'])
    desc = place.get('description_ar', '').lower()
    name = place.get('name_ar', '')
    audience = list(base)
    
    if 'عائل' in desc or 'أطفال' in desc or 'عوائل' in desc:
        if 'عوائل' not in audience: audience.append('عوائل')
        if 'أطفال' not in audience: audience.append('أطفال')
    if 'شباب' in desc or 'شبابي' in desc:
        if 'شباب' not in audience: audience.append('شباب')
    if 'أزواج' in desc or 'رومانس' in desc or 'فاخر' in desc:
        if 'أزواج' not in audience: audience.append('أزواج')
    if 'أطفال' in desc or 'ألعاب' in desc or 'عائلي' in desc:
        if 'أطفال' not in audience: audience.append('أطفال')
    
    return audience

def is_free(place):
    price = place.get('price_level', '')
    desc = place.get('description_ar', '').lower()
    cat = place.get('category', '')
    
    if cat in ['طبيعة', 'فعاليات']:
        if 'مجان' in desc or 'free' in desc.lower() or price == '$' or 'حديقة' in desc or 'منتزه' in desc:
            return True
    if 'مجان' in desc:
        return True
    return False

def main():
    with open('data/places.json', 'r', encoding='utf-8') as f:
        places = json.load(f)
    
    random.seed(42)  # Reproducible
    
    for place in places:
        lat, lng = get_coords(place.get('neighborhood', ''))
        place['lat'] = lat
        place['lng'] = lng
        place['audience'] = get_audience(place)
        place['is_free'] = is_free(place)
        cuisine = get_cuisine(place)
        if cuisine:
            place['cuisine'] = cuisine
    
    with open('data/places.json', 'w', encoding='utf-8') as f:
        json.dump(places, f, ensure_ascii=False, indent=2)
    
    # Stats
    with_coords = sum(1 for p in places if p.get('lat'))
    with_cuisine = sum(1 for p in places if p.get('cuisine'))
    free_count = sum(1 for p in places if p.get('is_free'))
    print(f"Enriched {len(places)} places")
    print(f"  With coordinates: {with_coords}")
    print(f"  With cuisine: {with_cuisine}")
    print(f"  Free: {free_count}")
    
    audiences = {}
    for p in places:
        for a in p.get('audience', []):
            audiences[a] = audiences.get(a, 0) + 1
    print(f"  Audiences: {audiences}")
    
    cuisines = {}
    for p in places:
        c = p.get('cuisine')
        if c:
            cuisines[c] = cuisines.get(c, 0) + 1
    print(f"  Cuisines: {cuisines}")

if __name__ == '__main__':
    main()
