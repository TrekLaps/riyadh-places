#!/usr/bin/env python3
"""Split places.json into light (listing) and detail (full) versions."""

import json
import math

LIGHT_FIELDS = [
    'id', 'name_ar', 'name_en', 'category', 'category_ar', 'category_en',
    'neighborhood', 'neighborhood_en', 'google_rating', 'review_count',
    'price_level', 'trending', 'is_new', 'image_url', 'lat', 'lng',
    'audience', 'is_free', 'perfect_for', 'district',
    'ramadan_iftar', 'ramadan_suhoor', 'ramadan_special', 'ramadan_tent',
    'review_quote_ar', 'review_quote', 'description_ar', 'google_maps_url'
]

def clean_value(v):
    """Remove empty/null values to save bytes."""
    if v is None:
        return None
    if isinstance(v, str) and v.strip() == '':
        return None
    if isinstance(v, list) and len(v) == 0:
        return None
    if isinstance(v, dict) and len(v) == 0:
        return None
    return v

def round_coord(v, decimals=4):
    """Round lat/lng to 4 decimal places (~11m precision, saves bytes)."""
    if v is None:
        return None
    return round(v, decimals)

def make_light(place):
    """Extract light fields, clean nulls, round coords."""
    light = {}
    for field in LIGHT_FIELDS:
        if field in place:
            val = clean_value(place[field])
            if val is not None:
                if field in ('lat', 'lng'):
                    val = round_coord(val)
                # Truncate description for light version (only first 150 chars needed for sharing)
                if field == 'description_ar' and isinstance(val, str) and len(val) > 150:
                    val = val[:150]
                light[field] = val
    return light

def main():
    with open('places.json', 'r', encoding='utf-8') as f:
        places = json.load(f)

    print(f"Loaded {len(places)} places from places.json")

    # Light version — for listings
    light = [make_light(p) for p in places]
    with open('places-light.json', 'w', encoding='utf-8') as f:
        json.dump(light, f, ensure_ascii=False, separators=(',', ':'))

    # Detail version — full data (for place.html)
    # Clean nulls and round coords in detail too
    detail = []
    for p in places:
        d = {}
        for k, v in p.items():
            val = clean_value(v)
            if val is not None:
                if k in ('lat', 'lng'):
                    val = round_coord(val)
                d[k] = val
        detail.append(d)
    with open('places-detail.json', 'w', encoding='utf-8') as f:
        json.dump(detail, f, ensure_ascii=False, separators=(',', ':'))

    # Report sizes
    import os
    orig = os.path.getsize('places.json')
    light_size = os.path.getsize('places-light.json')
    detail_size = os.path.getsize('places-detail.json')
    print(f"\nOriginal:  {orig/1024/1024:.2f} MB")
    print(f"Light:     {light_size/1024/1024:.2f} MB ({light_size/orig*100:.0f}%)")
    print(f"Detail:    {detail_size/1024/1024:.2f} MB ({detail_size/orig*100:.0f}%)")

if __name__ == '__main__':
    main()
