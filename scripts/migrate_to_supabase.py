#!/usr/bin/env python3
"""
Migration Script: JSON files → Supabase PostgreSQL
Converts existing places.json + delivery prices → SQL INSERT statements
Run: python3 scripts/migrate_to_supabase.py > supabase/seed.sql
"""

import json
import os
import re
import uuid

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Category mapping (Arabic → slug)
CATEGORY_MAP = {
    'مطعم': 'restaurant',
    'كافيه': 'cafe',
    'ترفيه': 'entertainment',
    'حلويات': 'dessert',
    'تسوق': 'shopping',
    'طبيعة': 'nature',
    'فنادق': 'hotel',
    'شاليه': 'chalet',
    'متاحف': 'museum',
    'فعاليات': 'event',
    'مولات': 'mall',
    'عطور': 'perfume',
}

def escape_sql(s):
    """Escape single quotes for SQL"""
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def migrate_places():
    """Convert places.json → SQL INSERT statements"""
    data = load_json('places.json')
    if not data:
        print("-- ERROR: places.json not found")
        return {}
    
    places = data if isinstance(data, list) else data.get('places', [])
    print(f"-- Migrating {len(places)} places")
    print()
    
    place_ids = {}  # name → uuid mapping for foreign keys
    
    for p in places:
        pid = str(uuid.uuid4())
        name = p.get('name', '')
        place_ids[name] = pid
        
        name_en = p.get('name_en') or p.get('nameEn')
        category = CATEGORY_MAP.get(p.get('category', ''), 'restaurant')
        neighborhood = p.get('neighborhood') or p.get('area')
        rating = p.get('rating')
        price_range = p.get('priceRange') or p.get('price_range')
        lat = p.get('latitude') or p.get('lat')
        lng = p.get('longitude') or p.get('lng') or p.get('lon')
        gmaps = p.get('googleMapsUrl') or p.get('google_maps_url') or p.get('maps_url')
        phone = p.get('phone')
        website = p.get('website')
        instagram = p.get('instagram')
        tags = p.get('tags', [])
        cuisine = p.get('cuisine') or p.get('type')
        source = p.get('source', 'migration')
        
        # Build tags array
        tags_sql = "'{" + ",".join(f'"{t}"' for t in tags if t) + "}'" if tags else "'{}'"
        
        print(f"INSERT INTO places (id, name, name_en, category_slug, rating, price_range, "
              f"latitude, longitude, google_maps_url, phone, website, instagram, tags, cuisine, source) VALUES (")
        print(f"  '{pid}', {escape_sql(name)}, {escape_sql(name_en)}, '{category}', "
              f"{rating or 'NULL'}, {escape_sql(price_range)}, "
              f"{lat or 'NULL'}, {lng or 'NULL'}, {escape_sql(gmaps)}, "
              f"{escape_sql(phone)}, {escape_sql(website)}, {escape_sql(instagram)}, "
              f"{tags_sql}, {escape_sql(cuisine)}, {escape_sql(source)}")
        print(f") ON CONFLICT DO NOTHING;")
        print()
    
    return place_ids

def migrate_delivery_prices(place_ids):
    """Convert delivery-prices*.json → SQL INSERT statements"""
    for filename in ['delivery-prices-full.json', 'delivery-prices.json']:
        data = load_json(filename)
        if not data:
            continue
        
        restaurants = data.get('restaurants', [])
        print(f"-- Migrating delivery prices from {filename}: {len(restaurants)} restaurants")
        print()
        
        for r in restaurants:
            name_ar = r.get('restaurant_ar') or r.get('restaurant', '')
            place_id = place_ids.get(name_ar)
            
            if not place_id:
                # Try English name
                name_en = r.get('restaurant') or r.get('restaurant_en', '')
                place_id = place_ids.get(name_en)
            
            if not place_id:
                print(f"-- SKIP: {name_ar} (not found in places)")
                continue
            
            apps = r.get('apps', [])
            if isinstance(apps, list):
                for app in apps:
                    app_slug = app.get('app', '')
                    available = app.get('available', False)
                    
                    print(f"INSERT INTO delivery_prices (place_id, app_slug, available) VALUES (")
                    print(f"  '{place_id}', '{app_slug}', {str(available).lower()}")
                    print(f") ON CONFLICT (place_id, app_slug) DO UPDATE SET available = {str(available).lower()};")
                    
                    # Menu items from delivery app
                    items = app.get('items', [])
                    for item in items:
                        item_name = item.get('name', '')
                        item_price = item.get('price')
                        if item_name and item_price:
                            print(f"INSERT INTO menu_items (place_id, name, price, source) VALUES (")
                            print(f"  '{place_id}', {escape_sql(item_name)}, {item_price}, '{app_slug}'")
                            print(f") ON CONFLICT DO NOTHING;")
                    print()
        break  # Only use first found file

def migrate_menu_prices(place_ids):
    """Convert prices-*.json → SQL INSERT statements"""
    for filename in ['prices-mass.json', 'prices-initial.json', 'prices-batch2.json']:
        data = load_json(filename)
        if not data:
            continue
        
        items = data if isinstance(data, list) else data.get('places', data.get('restaurants', []))
        print(f"-- Migrating menu prices from {filename}: {len(items)} places")
        print()
        
        for p in items:
            name_ar = p.get('name_ar') or p.get('name', '')
            name_en = p.get('name_en', '')
            place_id = place_ids.get(name_ar) or place_ids.get(name_en)
            
            if not place_id:
                print(f"-- SKIP menu: {name_ar} (not in places)")
                continue
            
            # Update avg price
            avg = p.get('avg_per_person')
            if avg:
                print(f"UPDATE places SET avg_price_per_person = {avg} WHERE id = '{place_id}';")
            
            # Insert menu items
            highlights = p.get('menu_highlights', [])
            source = p.get('source', 'menu_research')
            for item in highlights:
                item_name = item.get('item', '')
                item_price = item.get('price')
                if item_name and item_price:
                    print(f"INSERT INTO menu_items (place_id, name, price, source) VALUES (")
                    print(f"  '{place_id}', {escape_sql(item_name)}, {item_price}, {escape_sql(source)}")
                    print(f");")
            print()

if __name__ == '__main__':
    print("-- ==========================================")
    print("-- وين نروح بالرياض — Data Migration")
    print(f"-- Generated from JSON files in data/")
    print("-- ==========================================")
    print()
    
    place_ids = migrate_places()
    print(f"-- Total places migrated: {len(place_ids)}")
    print()
    
    migrate_delivery_prices(place_ids)
    migrate_menu_prices(place_ids)
    
    print()
    print("-- Migration complete!")
    print(f"-- Places: {len(place_ids)}")
