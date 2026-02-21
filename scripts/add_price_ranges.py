#!/usr/bin/env python3
"""
Add price_range to restaurants, cafes, and sweets shops in Riyadh places data.
Strategy:
1. Use Google price_level where available (direct mapping)
2. Use known chain/brand name matching
3. Use category-based heuristics for remaining
"""

import json
import re
import os

DATA_PATH = os.path.expanduser("~/workspace/projects/riyadh-places/data/places.json")

# Known chains and brands with their price ranges
# "$" = cheap (<30 SAR/person), "$$" = mid (30-100), "$$$" = expensive (100-300), "$$$$" = luxury (300+)

KNOWN_CHAINS = {
    # === FAST FOOD / CHEAP ($) ===
    "$": [
        # International fast food
        "ماكدونالدز", "McDonald", "ماكدونلدز",
        "برجر كنج", "Burger King", "برغر كنغ",
        "كنتاكي", "KFC",
        "هارديز", "Hardee",
        "صب واي", "Subway", "صبواي",
        "دومينوز", "Domino", "دومنوز",
        "بيتزا هت", "Pizza Hut",
        "ليتل سيزرز", "Little Caesar",
        "باباجونز", "Papa John", "بابا جونز",
        "بوبايز", "Popeye",
        "تشيكن فيل أيه",
        "ونديز", "Wendy",
        "دجاج تكساس", "Texas Chicken",
        "شاورمر", "Shawarmer",
        "جاد", # Jaad
        "كودو", "Kudu",
        "هرفي", "Herfy",
        "الطازج", "Tazaj", "Al Tazaj",
        "البيك", "Al Baik", "Albaik",
        "بروست",  # Various broasted chicken
        "الرومانسية", "Al Romansiah",
        "مندي",  # Generic mandi restaurants are usually cheap
        "شاورما", # Most shawarma places
        "فلافل",
        "فول", # Foul/falafel
        "تميس",
        "معصوب",
        "مطبق",
        "كشري",
        "الركن الذهبي",
        "ماما نورة", "Mama Noura",
        "بيت الشاورما",
        "شاورما الريم",
        "مشاوي الخليج",
        "الفلاح",
        "بيتزا",  # Most pizza places
        "كريب",  # Crepe shops usually cheap
        "وافل",  # Waffle shops
        "آيس كريم", "ايس كريم", # Ice cream
        "باسكن روبنز", "Baskin Robbins",
        "سينابون", "Cinnabon",
        "دانكن", "Dunkin",
        "تيم هورتنز", "Tim Horton",
        "الشعلة",
        "مطاعم ومطابخ",
        "مطابخ",
        "بخاري",  # Bukhari restaurants usually cheap-mid
        "مظبي",
        "حنيذ",
        "مندي ومظبي",
        "كباب",
        "مشويات",
        "مطعم زاد",
        "الريف",
        "ديري كوين", "Dairy Queen",
        "صبحي كابر", # Sobhy Kaber
        "فطور", # Breakfast places usually cheap
        "تمور",
        "سمبوسة",
        "معجنات",
        "فطائر",
        "المعجنات",
        "بليلة",
        "جريش",
        "مرقوق",
        "قرصان",
        "الأسرة", # Al Usra family restaurants
        "المجلس",
        "الضيافة",
        "ركن",
        "الناضج",
        "أبو زيد",
        "أمريكانا", "Americana",
        "الساعة",
        "المذاق",
        "النافذة",
        "كبدة",
        "بسطة",
        "شيك آت", "Chic-A", "شيكات",
        "فايف غايز", "Five Guys",  # Actually $$ but border
        "تشيليز",  # Actually $$ 
    ],
    
    # === MID-RANGE ($$) ===
    "$$": [
        # Casual dining international
        "آبل بيز", "Applebee",
        "تشيليز", "Chili",
        "فرايديز", "TGI Friday", "Friday",
        "بافلو وايلد وينغز", "Buffalo Wild Wings",
        "ذا تشيز كيك فاكتوري", "Cheesecake Factory",
        "شيك شاك", "Shake Shack",
        "فايف غايز", "Five Guys",
        "نودلز", "Noodle",
        "واقامام", "Wagamama",
        "بي إف تشانغز", "P.F. Chang",
        "ذا كاونتر", "The Counter",
        "جوني روكتز", "Johnny Rocket",
        "فودكس", # Foodics restaurants
        
        # Saudi/Arab mid-range
        "بيت المشويات",
        "لبناني",  # Lebanese restaurants
        "المشوى العربي",
        "تركي",  # Turkish restaurants
        "مطعم تركي",
        "كباب تركي",
        "الأرجوان",
        "القصر",
        "نارنج", "Narenj",
        "أوبريشن فلافل", "Operation Falafel",
        "مادو", "Mado",
        "سلطان ديلايت", "Sultan Delight",
        "الفنر",
        "ليمونة", "Lemonah",
        "ابن حمديس",
        "المحمدية",
        "النخيل",
        "الوطنية",
        "التنور",
        "النافورة",
        "سيزلر", "Sizzler",
        "بحري",  # Seafood usually $$
        "سمك",  # Fish restaurants
        "مأكولات بحرية",
        "سوشي",  # Most sushi places $$-$$$
        "وجبات هندية",
        "هندي",  # Indian restaurants
        "باكستاني",  # Pakistani restaurants
        "إيطالي",  # Italian restaurants
        "كازا", "Casa",
        "لا بيتشرا",
        "سويت",  # Sweet shops mid-range
        "تيبستي",
        "الأندلس",
        "قرية",
        "العثيم",
        "كافيه", # Most cafes
        "لاونج", "Lounge",
        "بريستو", "Presto",
        "كوستا", "Costa",
        "ستاربكس", "Starbucks",
        "كاريبو", "Caribou",
        "بارنز", "Barn",
        "دوز كافيه", "Dose Cafe",
        "كافيين", "Caffeine",
        "إلبا", "Elba",
        "فليب", "Flip",
        "رصيف", # Raseef
        "كوفي", "Coffee",
        "قهوة",
        "بيكري", "Bakery",
        "مخبز",
        "حلويات",  # Most sweets shops
        "بول", "Paul",
        "لا دوري", "La Duree", "Laduree",
        "باتشي", "Patchi",
        "سعد الدين", "Saadeddin",
        "هولز", # Holz
        "روتانا",
        "ماكارون",
        "شوكولا",
        "جوديفا", "Godiva",
        "كنافة",
        "بقلاوة",
        "كيك",
        "حلا",
        "ميلك شيك",
        "بابل تي", "Bubble Tea",
        "شاي", "Tea",
        "عصير", "Juice",
        "سموذي", "Smoothie",
    ],
    
    # === EXPENSIVE ($$$) ===
    "$$$": [
        # Upscale dining
        "ذا غريل", "The Grill",
        "سالت", "SALT",  # SALT Riyadh
        "ناين تو فايف",
        "أنتركوت", "Entrecote", "إنتركوت",
        "لاكوتش", "La Cucina",
        "هاكاسان", "Hakkasan",
        "نوبو", "Nobu",
        "زوما", "Zuma",
        "ستيك هاوس", "Steak House", "ستيك",
        "قطعة لحم", "Cut",
        "ذا بوتشر", "The Butcher",
        "مامبو",
        "كاتسبي",
        "لمسة", 
        "ليالي",
        "بريمو",
        "كارلوتشيو", "Carluccio",
        "إيل بانيتو",
        "فندق",  # Hotel restaurants usually $$$
        "هيلتون", "Hilton",
        "ماريوت", "Marriott",
        "شيراتون", "Sheraton",
        "انتركونتننتال", "Intercontinental",
        "كراون بلازا", "Crowne Plaza",
        "رامادا", "Ramada",
        "موفنبيك", "Movenpick", "موفنبك",
        "لو ميريديان", "Le Meridien",
        "بارك حياة", "Park Hyatt",
        "سفير", "Safir",
        "فور سيزونز", "Four Seasons",
        "فيرمونت", "Fairmont",
        "روكو", "Rocco",
        "أوليفو", "Olivo",
        "كازا بيانكا",
        "لا فينا", "La Vina",
        "ريو", "Rio",
        "كابري", "Capri",
        "بياتو", "Piato",
        "بريجو", "Prego",
        "ناغازاكي",
        "واقيو", "Wagyu",
        "ساكورا", "Sakura",
        "تيبانياكي", "Teppanyaki",
        "LPM", "إل بي إم",
        "روبيرتوز", "Roberto",
        "فيا رياض", "Via Riyadh",
        "تاو", "Tao",
        "سبايسز", "Spice",
        "كونتينينتال",
        "بيسترو", "Bistro",
        "بوتيك",
        "تراتوريا", "Trattoria",
    ],
    
    # === LUXURY ($$$$) ===
    "$$$$": [
        "نوزومي", "Nozomi",
        "لوسين", "Lucin",
        "هوسكي", "Husky",
        "سومو سوشي", "Sumo Sushi",
        "غلوريا", "Gloria",
        "بيير", "Pierre",
        "لو سينك", "Le Cinq",
        "ميراس", "Myras",
        "ناو", "Nusr-Et", "نصرت",
        "طلال",
        "عالم البحار الفاخر",
    ],
}

def match_chain(name_ar, name_en, price_range_map):
    """Check if a place name matches any known chain."""
    name_ar = name_ar or ""
    name_en = name_en or ""
    combined = f"{name_ar} {name_en}".lower()
    
    # Check from most expensive to cheapest (higher confidence for luxury)
    for price in ["$$$$", "$$$", "$$", "$"]:
        for keyword in price_range_map[price]:
            kw_lower = keyword.lower()
            if kw_lower in combined:
                return price
    return None

def get_description_hints(desc):
    """Extract price hints from description."""
    if not desc:
        return None
    desc_lower = desc.lower() if desc else ""
    
    luxury_words = ["فاخر", "luxury", "fine dining", "michelin", "ميشلان", "حصري", "exclusive"]
    expensive_words = ["راقي", "upscale", "premium", "بريميوم", "عالي الجودة"]
    cheap_words = ["رخيص", "cheap", "اقتصادي", "شعبي", "budget", "سريع", "fast food"]
    
    for w in luxury_words:
        if w in desc_lower:
            return "$$$$"
    for w in expensive_words:
        if w in desc_lower:
            return "$$$"
    for w in cheap_words:
        if w in desc_lower:
            return "$"
    return None

def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    target_categories = {"مطعم", "كافيه", "حلويات"}
    
    stats = {
        "already_had": 0,
        "from_google_price_level": 0,
        "from_chain_match": 0,
        "from_description": 0,
        "still_null": 0,
        "total_targets": 0,
    }
    
    for place in data:
        if place.get("category") not in target_categories:
            continue
        
        stats["total_targets"] += 1
        
        # Skip if already has price_range
        if place.get("price_range"):
            stats["already_had"] += 1
            continue
        
        name_ar = place.get("name_ar", "")
        name_en = place.get("name_en", "")
        desc = place.get("description_ar", "")
        price_level = place.get("price_level")
        category = place.get("category")
        
        new_price = None
        source = None
        
        # Strategy 1: Use Google price_level (most reliable)
        if price_level and price_level in ("$", "$$", "$$$", "$$$$"):
            new_price = price_level
            source = "from_google_price_level"
        
        # Strategy 2: Known chain matching
        if not new_price:
            chain_price = match_chain(name_ar, name_en, KNOWN_CHAINS)
            if chain_price:
                new_price = chain_price
                source = "from_chain_match"
        
        # Strategy 3: Description hints
        if not new_price:
            desc_price = get_description_hints(desc)
            if desc_price:
                new_price = desc_price
                source = "from_description"
        
        if new_price:
            place["price_range"] = new_price
            stats[source] += 1
        else:
            stats["still_null"] += 1
    
    # Save
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Report
    total_with_price = stats["already_had"] + stats["from_google_price_level"] + stats["from_chain_match"] + stats["from_description"]
    print(f"\n=== Price Range Assignment Results ===")
    print(f"Total target places: {stats['total_targets']}")
    print(f"Already had price_range: {stats['already_had']}")
    print(f"From Google price_level: {stats['from_google_price_level']}")
    print(f"From chain name match: {stats['from_chain_match']}")
    print(f"From description hints: {stats['from_description']}")
    print(f"Still null: {stats['still_null']}")
    print(f"TOTAL with price_range now: {total_with_price}")
    print(f"Coverage: {total_with_price/stats['total_targets']*100:.1f}%")

if __name__ == "__main__":
    main()
