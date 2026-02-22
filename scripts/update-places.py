#!/usr/bin/env python3
"""
وين نروح الرياض - Daily Update Script
=======================================
Updates places data with trending status and new places.
Placeholder for Google Places API integration.

Usage:
    python3 scripts/update-places.py

Cron (daily at 6 AM):
    0 6 * * * cd /path/to/riyadh-places && python3 scripts/update-places.py
"""

import json
import os
import sys
from datetime import datetime, timezone

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PLACES_FILE = os.path.join(PROJECT_DIR, 'data', 'places.json')
LOG_FILE = os.path.join(PROJECT_DIR, 'data', 'update-log.json')

# ============================================================
# Google Places API Integration (PLACEHOLDER)
# ============================================================
# To enable, set your API key:
#   export GOOGLE_PLACES_API_KEY="your-key-here"
#
# The script will then:
# 1. Fetch latest ratings from Google Places
# 2. Check for new trending places
# 3. Update place data automatically
# ============================================================

GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', '')


def load_places():
    """Load places from JSON file."""
    with open(PLACES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_places(places):
    """Save places to JSON file."""
    with open(PLACES_FILE, 'w', encoding='utf-8') as f:
        json.dump(places, f, ensure_ascii=False, indent=2)


def load_log():
    """Load update log."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"updates": []}


def save_log(log):
    """Save update log."""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def fetch_google_places_data(place):
    """
    PLACEHOLDER: Fetch data from Google Places API.
    
    When implemented, this will:
    1. Search for the place by name + "Riyadh"
    2. Get latest rating, review count, photos
    3. Return updated data
    
    Google Places API endpoints:
    - Place Search: https://maps.googleapis.com/maps/api/place/findplacefromtext/json
    - Place Details: https://maps.googleapis.com/maps/api/place/details/json
    """
    if not GOOGLE_PLACES_API_KEY:
        return None

    # TODO: Implement actual API call
    # import requests
    # url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    # params = {
    #     "input": f"{place['name_en']} Riyadh",
    #     "inputtype": "textquery",
    #     "fields": "place_id,name,rating,user_ratings_total,photos",
    #     "key": GOOGLE_PLACES_API_KEY
    # }
    # response = requests.get(url, params=params)
    # data = response.json()
    # 
    # if data.get('candidates'):
    #     candidate = data['candidates'][0]
    #     place_id = candidate['place_id']
    #     
    #     # Get detailed info
    #     details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    #     details_params = {
    #         "place_id": place_id,
    #         "fields": "rating,user_ratings_total,opening_hours,website,formatted_phone_number",
    #         "key": GOOGLE_PLACES_API_KEY
    #     }
    #     details_response = requests.get(details_url, params=details_params)
    #     details = details_response.json().get('result', {})
    #     
    #     return {
    #         "rating": details.get('rating', place['rating']),
    #         "review_count": details.get('user_ratings_total', 0),
    #     }
    
    return None


def update_trending_status(places):
    """
    Update trending status based on criteria.
    
    A place is trending if:
    - It has a high rating (>= 4.5)
    - It's new (is_new = true)
    - Manual override (future: based on search volume data)
    """
    changes = []
    for place in places:
        old_trending = place.get('trending', False)
        
        # Simple trending algorithm
        # Support both 'rating' and 'google_rating' fields
        rating = place.get('rating') or place.get('google_rating', 0) or 0
        is_trending = (
            rating >= 4.5 or
            place.get('is_new', False)
        )
        
        if is_trending != old_trending:
            place['trending'] = is_trending
            place_id = place.get('id', place.get('name_en', 'unknown'))
            changes.append({
                "place_id": place_id,
                "name": place.get('name_en', 'unknown'),
                "change": "trending" if is_trending else "not_trending"
            })
    
    return changes


def update_ratings_from_api(places):
    """Update ratings from Google Places API (if configured)."""
    changes = []
    for place in places:
        api_data = fetch_google_places_data(place)
        if api_data and 'rating' in api_data:
            old_rating = place['rating']
            new_rating = api_data['rating']
            if abs(old_rating - new_rating) > 0.1:
                place['rating'] = new_rating
                changes.append({
                    "place_id": place['id'],
                    "name": place['name_en'],
                    "change": f"rating: {old_rating} → {new_rating}"
                })
    return changes


def main():
    """Main update routine."""
    print("🏙️ وين نروح الرياض - Daily Update")
    print("=" * 50)
    print(f"⏰ Time: {datetime.now(timezone.utc).isoformat()}")
    print()

    # Load data
    places = load_places()
    log = load_log()
    
    print(f"📊 Total places: {len(places)}")
    print(f"🆕 New places: {sum(1 for p in places if p.get('is_new'))}")
    print(f"🔥 Currently trending: {sum(1 for p in places if p.get('trending'))}")
    print()

    all_changes = []

    # Update trending status
    print("🔄 Updating trending status...")
    trending_changes = update_trending_status(places)
    all_changes.extend(trending_changes)
    if trending_changes:
        for change in trending_changes:
            print(f"  → {change['name']}: {change['change']}")
    else:
        print("  → No trending changes")

    # Update from Google Places API
    if GOOGLE_PLACES_API_KEY:
        print("\n🌐 Fetching Google Places API data...")
        api_changes = update_ratings_from_api(places)
        all_changes.extend(api_changes)
        if api_changes:
            for change in api_changes:
                print(f"  → {change['name']}: {change['change']}")
        else:
            print("  → No rating changes from API")
    else:
        print("\n⚠️  Google Places API key not set. Skipping API update.")
        print("   Set GOOGLE_PLACES_API_KEY environment variable to enable.")

    # Save updated data
    save_places(places)

    # Log the update
    update_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_places": len(places),
        "trending_count": sum(1 for p in places if p.get('trending')),
        "new_count": sum(1 for p in places if p.get('is_new')),
        "changes": all_changes,
        "api_enabled": bool(GOOGLE_PLACES_API_KEY)
    }
    log['updates'].append(update_entry)

    # Keep only last 90 days of logs
    log['updates'] = log['updates'][-90:]
    save_log(log)

    print(f"\n✅ Update complete! {len(all_changes)} changes made.")
    print(f"📝 Log saved to {LOG_FILE}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
