#!/usr/bin/env python3
"""
Generate smart Popular Times data for Riyadh places.
Based on place category, type, and typical Saudi Arabian patterns.

Riyadh-specific patterns:
- Weekend = Thursday/Friday (not Saturday/Sunday)
- Late-night culture: many places busy until midnight+
- Extreme heat: outdoor places quieter in afternoon (summer)
- Prayer times cause brief dips
- Ramadan shifts everything later
"""

import json
import random
import os

# Hourly patterns (0-23) for each category
# Values 0-100 representing relative busyness

PATTERNS = {
    "cafe": {
        "weekday": [0,0,0,0,0,0,5,15,40,60,65,55,40,30,25,35,50,55,60,55,45,30,15,5],
        "weekend": [0,0,0,0,0,0,5,10,30,50,65,70,60,45,35,45,60,65,70,65,55,40,20,8],
        "peak_hours": "8:00-11:00, 16:00-18:00",
        "best_visit_ar": "صباحاً من 8-10 أو بعد العصر 4-6",
    },
    "restaurant": {
        "weekday": [0,0,0,0,0,0,0,5,10,15,20,40,70,85,70,40,25,30,50,70,85,90,75,40],
        "weekend": [0,0,0,0,0,0,0,5,10,20,30,50,75,90,75,45,30,40,60,80,95,100,85,50],
        "peak_hours": "12:00-14:00, 20:00-23:00",
        "best_visit_ar": "قبل وقت الذروة: 11:30 ص أو 7:30 م",
    },
    "activity": {
        "weekday": [0,0,0,0,0,0,0,5,10,20,30,35,30,25,20,30,45,55,65,70,65,55,35,15],
        "weekend": [0,0,0,0,0,0,0,5,15,30,45,55,60,55,50,55,65,75,85,90,85,70,50,25],
        "peak_hours": "17:00-22:00",
        "best_visit_ar": "الصباح أو بداية العصر للهدوء",
    },
    "shopping": {
        "weekday": [0,0,0,0,0,0,0,0,5,15,30,40,45,40,30,35,50,60,65,70,65,55,40,15],
        "weekend": [0,0,0,0,0,0,0,0,10,20,40,55,65,60,55,60,70,80,90,95,90,80,60,25],
        "peak_hours": "17:00-22:00",
        "best_visit_ar": "أيام الأسبوع الصباح 10-12",
    },
    "entertainment": {
        "weekday": [0,0,0,0,0,0,0,0,5,10,15,20,25,20,15,25,40,55,70,80,75,60,40,15],
        "weekend": [0,0,0,0,0,0,0,0,10,20,30,40,50,45,40,50,65,80,90,95,90,80,60,30],
        "peak_hours": "18:00-22:00",
        "best_visit_ar": "بداية الأسبوع أو الصباح",
    },
    "nature": {
        "weekday": [0,0,0,0,0,5,15,30,45,50,45,35,20,10,5,15,35,50,55,45,30,15,5,0],
        "weekend": [0,0,0,0,0,5,20,40,55,65,60,50,35,20,10,25,45,60,65,55,40,25,10,0],
        "peak_hours": "7:00-10:00, 16:00-19:00",
        "best_visit_ar": "الصباح الباكر 6-9 أو قبل المغرب",
    },
    "desserts": {
        "weekday": [0,0,0,0,0,0,0,5,10,15,20,25,30,25,20,30,45,55,65,75,80,70,50,25],
        "weekend": [0,0,0,0,0,0,0,5,10,20,30,35,40,35,30,40,55,65,80,90,95,85,65,35],
        "peak_hours": "19:00-23:00",
        "best_visit_ar": "بعد الظهر 2-5 أو الصباح",
    },
    "events": {
        "weekday": [0,0,0,0,0,0,0,0,5,10,15,20,25,20,15,25,45,65,80,90,85,70,50,20],
        "weekend": [0,0,0,0,0,0,0,0,10,20,30,40,50,45,40,50,65,80,95,100,95,85,65,30],
        "peak_hours": "18:00-22:00",
        "best_visit_ar": "بداية الفعالية أو أيام الأسبوع",
    },
}

DAYS = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]

def add_noise(values, noise_level=8):
    """Add random noise to make data look realistic."""
    return [max(0, min(100, v + random.randint(-noise_level, noise_level))) for v in values]

def generate_weekly_data(category):
    """Generate 7-day popular times data for a category."""
    pattern = PATTERNS.get(category, PATTERNS["activity"])
    weekly = {}
    
    for day in DAYS:
        if day in ("thursday", "friday"):
            # Weekend in Saudi Arabia
            base = pattern["weekend"]
        else:
            base = pattern["weekday"]
        
        # Add slight variation per day
        weekly[day] = add_noise(base)
    
    return weekly

def get_current_busyness(category):
    """Get a realistic busyness level string."""
    # This will be computed dynamically in JS, but we set a default
    return "moderate"

def get_busyness_for_hour(hourly_data, hour):
    """Determine busyness level for a given hour."""
    val = hourly_data[hour]
    if val == 0:
        return "closed"
    elif val <= 25:
        return "quiet"
    elif val <= 50:
        return "moderate" 
    elif val <= 75:
        return "busy"
    else:
        return "very_busy"

def main():
    places_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'places.json')
    
    with open(places_path, 'r', encoding='utf-8') as f:
        places = json.load(f)
    
    print(f"Processing {len(places)} places...")
    
    for place in places:
        cat = place.get("category_en", place.get("category", "activity"))
        
        # Map Arabic categories
        cat_map = {
            "كافيه": "cafe",
            "مطعم": "restaurant",
            "ترفيه": "activity",
            "تسوق": "shopping",
            "طبيعة": "nature",
            "حلويات": "desserts",
            "فعاليات": "events",
        }
        cat = cat_map.get(cat, cat)
        
        pattern = PATTERNS.get(cat, PATTERNS["activity"])
        
        # Generate weekly data
        place["popular_times"] = generate_weekly_data(cat)
        place["peak_hours"] = pattern["peak_hours"]
        place["best_visit_time"] = pattern["best_visit_ar"]
        
        # Adjust for specific place characteristics
        # Fine dining restaurants = later peak
        if cat == "restaurant" and place.get("price_level") in ("$$$", "$$$$"):
            for day in DAYS:
                # Shift dinner crowd later
                data = place["popular_times"][day]
                data[19] = min(100, data[19] + 10)
                data[20] = min(100, data[20] + 15)
                data[21] = min(100, data[21] + 15)
                data[22] = min(100, data[22] + 10)
                place["popular_times"][day] = data
            place["peak_hours"] = "20:00-23:00"
            place["best_visit_time"] = "احجز مسبقاً، أفضل وقت 7:30-8:00 م"
        
        # Budget restaurants = more lunch crowd
        elif cat == "restaurant" and place.get("price_level") in ("$",):
            for day in DAYS:
                data = place["popular_times"][day]
                data[11] = min(100, data[11] + 15)
                data[12] = min(100, data[12] + 20)
                data[13] = min(100, data[13] + 15)
                place["popular_times"][day] = data
            place["peak_hours"] = "12:00-14:00, 19:00-22:00"
        
        # Specialty coffee = morning crowd
        if cat == "cafe" and any(kw in place.get("name_ar", "") for kw in ["بن", "محمصة", "روست", "باتش"]):
            for day in DAYS:
                data = place["popular_times"][day]
                data[7] = min(100, data[7] + 15)
                data[8] = min(100, data[8] + 20)
                data[9] = min(100, data[9] + 15)
                place["popular_times"][day] = data
        
        # High review count = generally busier
        reviews = place.get("review_count", 0)
        if reviews > 5000:
            for day in DAYS:
                place["popular_times"][day] = [min(100, v + 8) for v in place["popular_times"][day]]
        
        # Trending places = busier
        if place.get("trending"):
            for day in DAYS:
                place["popular_times"][day] = [min(100, v + 5) for v in place["popular_times"][day]]
    
    # Write back
    with open(places_path, 'w', encoding='utf-8') as f:
        json.dump(places, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Added popular_times data to {len(places)} places")
    print(f"   Categories: {set(p.get('category_en', p.get('category','?')) for p in places)}")

if __name__ == "__main__":
    main()
