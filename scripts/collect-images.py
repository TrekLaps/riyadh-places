#!/usr/bin/env python3
"""
Collect REAL images for Riyadh places from free public sources.

Sources (in priority order):
1. Wikimedia Commons - search by place name
2. Wikipedia - article main images for famous places
3. Place websites - og:image meta tags
4. Wikidata - images linked to entities

Stores image URLs only (no downloads).
Idempotent - skips places that already have image_url.

Usage:
    python3 scripts/collect-images.py                    # Full run
    python3 scripts/collect-images.py --limit 500        # Sample run
    python3 scripts/collect-images.py --source wikimedia  # Single source
    python3 scripts/collect-images.py --dry-run          # Preview only
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import ssl
import argparse
from pathlib import Path

# Disable SSL verification for some websites that have issues
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PLACES_FILE = DATA_DIR / "places.json"
RESULTS_FILE = DATA_DIR / "image-collection-results.json"

# Rate limiting
WIKIMEDIA_DELAY = 1.0  # seconds between Wikimedia API calls
WEBSITE_DELAY = 2.0    # seconds between website fetches
WIKIPEDIA_DELAY = 0.5

# Stats
stats = {
    "total": 0,
    "already_has_image": 0,
    "wikimedia_found": 0,
    "wikipedia_found": 0,
    "website_found": 0,
    "no_image_found": 0,
    "errors": 0,
    "skipped_default_coords": 0,
}

# Known Riyadh landmark mappings to Wikipedia articles
WIKIPEDIA_MAPPINGS = {
    # Landmarks & Towers
    "kingdom centre": "Kingdom_Centre",
    "kingdom tower": "Kingdom_Centre",
    "برج المملكة": "Kingdom_Centre",
    "al faisaliyah": "Al_Faisaliyah_Center",
    "الفيصلية": "Al_Faisaliyah_Center",
    "masmak fortress": "Masmak_Fortress",
    "قصر المصمك": "Masmak_Fortress",
    "masmak fort": "Masmak_Fortress",
    # Districts & Areas
    "boulevard riyadh": "Boulevard_Riyadh_City",
    "بوليفارد الرياض": "Boulevard_Riyadh_City",
    "diriyah": "Diriyah",
    "الدرعية": "Diriyah",
    "king abdullah financial district": "King_Abdullah_Financial_District",
    "kafd": "King_Abdullah_Financial_District",
    "كافد": "King_Abdullah_Financial_District",
    # Museums
    "national museum": "National_Museum_of_Saudi_Arabia",
    "المتحف الوطني": "National_Museum_of_Saudi_Arabia",
    # Malls
    "al nakheel mall": "Al_Nakheel_Mall",
    "النخيل مول": "Al_Nakheel_Mall",
    "panorama mall": "Panorama_Mall",
    "بانوراما مول": "Panorama_Mall",
    "riyadh gallery": "Riyadh_Gallery",
    "الرياض جاليري": "Riyadh_Gallery",
    "granada mall": "Granada_Centre",
    "غرناطة مول": "Granada_Centre",
    # Hotels
    "ritz carlton riyadh": "The_Ritz-Carlton,_Riyadh",
    "four seasons riyadh": "Four_Seasons_Hotel_Riyadh",
    # Parks
    "king abdullah park": "King_Abdullah_Park",
    "salam park": "Salam_Park_(Riyadh)",
    "king fahd park": "King_Fahd_Park",
    # Stadiums/venues
    "king fahd stadium": "King_Fahd_International_Stadium",
    # Universities (as landmarks)
    "king saud university": "King_Saud_University",
    "princess nourah university": "Princess_Nourah_bint_Abdulrahman_University",
}

# Categories that are more likely to have Wikimedia images
HIGH_VALUE_CATEGORIES = {"museums", "museum", "malls", "mall", "hotels", "entertainment", "nature"}


def api_request(url, timeout=15):
    """Make an HTTP request with error handling."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "RiyadhPlacesBot/1.0 (image collection for wein-nrooh.com)"
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return None


def search_wikimedia_commons(query, limit=3):
    """Search Wikimedia Commons for images matching a query."""
    encoded = urllib.parse.quote(query)
    url = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&generator=search&gsrsearch={encoded}"
        f"&gsrnamespace=6&gsrlimit={limit}"
        f"&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=800&format=json"
    )
    data = api_request(url)
    if not data or "query" not in data:
        return []

    results = []
    for page in data["query"].get("pages", {}).values():
        title = page.get("title", "")
        # Filter out non-photo files (SVGs, maps, logos, flags, icons)
        lower_title = title.lower()
        skip_patterns = [".svg", "flag ", "coat of arms", "logo", "map ", "icon",
                         "seal of", "emblem", "diagram", "chart", "signature"]
        if any(p in lower_title for p in skip_patterns):
            continue

        imageinfo = page.get("imageinfo", [{}])[0]
        thumb = imageinfo.get("thumburl", "")
        full = imageinfo.get("url", "")
        if thumb or full:
            results.append({
                "title": title,
                "thumb_url": thumb,
                "full_url": full,
                "source": "wikimedia_commons"
            })
    return results


def search_wikipedia_image(article_title):
    """Get the main image from a Wikipedia article."""
    encoded = urllib.parse.quote(article_title)
    url = (
        f"https://en.wikipedia.org/w/api.php?"
        f"action=query&titles={encoded}"
        f"&prop=pageimages&piprop=original|thumbnail&pithumbsize=800&format=json"
    )
    data = api_request(url)
    if not data or "query" not in data:
        return None

    for page in data["query"].get("pages", {}).values():
        if "original" in page:
            return {
                "thumb_url": page.get("thumbnail", {}).get("source", ""),
                "full_url": page["original"]["source"],
                "source": "wikipedia",
                "article": article_title
            }
    return None


def fetch_og_image(website_url):
    """Fetch og:image meta tag from a website."""
    try:
        # Normalize URL
        if not website_url.startswith("http"):
            website_url = "https://" + website_url

        req = urllib.request.Request(website_url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            # Read only first 50KB to find meta tags
            html = resp.read(50000).decode("utf-8", errors="ignore")

        # Find og:image
        patterns = [
            r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
            r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\']([^"\']+)["\']',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                img_url = match.group(1)
                # Validate it looks like an image URL
                if any(ext in img_url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp", "image"]):
                    # Make absolute URL if relative
                    if img_url.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(website_url)
                        img_url = f"{parsed.scheme}://{parsed.netloc}{img_url}"
                    return {
                        "thumb_url": img_url,
                        "full_url": img_url,
                        "source": "website_og",
                        "website": website_url
                    }
        return None
    except Exception:
        return None


def get_best_image_for_place(place, dry_run=False):
    """Try all sources to find the best image for a place."""
    name_en = place.get("name_en", "")
    name_ar = place.get("name_ar", "")
    category = place.get("category_en", "").lower()

    # 1. Check Wikipedia mappings first (most reliable)
    for key, article in WIKIPEDIA_MAPPINGS.items():
        if key in name_en.lower() or key in name_ar:
            if not dry_run:
                time.sleep(WIKIPEDIA_DELAY)
                result = search_wikipedia_image(article)
                if result:
                    return result
            else:
                return {"source": "wikipedia_mapping", "article": article, "dry": True}

    # 2. Search Wikimedia Commons by English name + Riyadh
    if name_en and len(name_en) > 3:
        search_query = f"{name_en} Riyadh"
        if not dry_run:
            time.sleep(WIKIMEDIA_DELAY)
            results = search_wikimedia_commons(search_query, limit=3)
            if results:
                # Try to find one whose title mentions the place name
                name_words = set(name_en.lower().split())
                for r in results:
                    title_lower = r["title"].lower()
                    # Check if at least one significant word from the name appears in title
                    if any(w in title_lower for w in name_words if len(w) > 3):
                        return r
                # If no title match, skip — don't use random Riyadh images

    # 3. For high-value categories, try broader Wikimedia search
    if category in HIGH_VALUE_CATEGORIES and name_en:
        # Try without "Riyadh" suffix
        if not dry_run:
            time.sleep(WIKIMEDIA_DELAY)
            results = search_wikimedia_commons(name_en, limit=3)
            if results:
                name_words = set(name_en.lower().split())
                for r in results:
                    title_lower = r["title"].lower()
                    if any(w in title_lower for w in name_words if len(w) > 3):
                        return r

    # 4. Try website og:image
    website = place.get("website", "")
    if website:
        if not dry_run:
            time.sleep(WEBSITE_DELAY)
            result = fetch_og_image(website)
            if result:
                return result
        else:
            return {"source": "website_og", "website": website, "dry": True}

    return None


def main():
    parser = argparse.ArgumentParser(description="Collect images for Riyadh places")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of places to process")
    parser.add_argument("--source", choices=["wikimedia", "wikipedia", "website", "all"], default="all")
    parser.add_argument("--dry-run", action="store_true", help="Preview what would be searched")
    parser.add_argument("--force", action="store_true", help="Re-process places that already have images")
    parser.add_argument("--category", type=str, help="Only process specific category")
    parser.add_argument("--high-value-first", action="store_true", help="Process landmarks/malls/museums first")
    args = parser.parse_args()

    # Load places
    print(f"Loading places from {PLACES_FILE}...")
    with open(PLACES_FILE) as f:
        places = json.load(f)

    stats["total"] = len(places)
    print(f"Total places: {len(places)}")

    # Filter by category if specified
    if args.category:
        places_to_process = [p for p in places if p.get("category_en", "").lower() == args.category.lower()]
        print(f"Filtered to category '{args.category}': {len(places_to_process)} places")
    else:
        places_to_process = list(places)

    # Sort: high-value categories first if requested
    if args.high_value_first:
        def sort_key(p):
            cat = p.get("category_en", "").lower()
            if cat in HIGH_VALUE_CATEGORIES:
                return 0
            if p.get("website"):
                return 1
            return 2
        places_to_process.sort(key=sort_key)

    # Apply limit
    if args.limit:
        places_to_process = places_to_process[:args.limit]
        print(f"Limited to {args.limit} places")

    # Ensure all places have an id (generate from name if missing)
    for idx, p in enumerate(places):
        if "id" not in p:
            name = p.get("name_en", p.get("name_ar", f"place-{idx}"))
            p["id"] = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') or f"place-{idx}"
        # Store original index for update
        p["_idx"] = idx

    # Create lookup for fast update (by index to handle dup IDs)
    place_by_idx = {p["_idx"]: p for p in places}

    found_count = 0
    processed = 0
    errors = 0

    for i, place in enumerate(places_to_process):
        pid = place["id"]
        name = place.get("name_en", place.get("name_ar", "unknown"))

        # Skip if already has image (unless --force)
        if place.get("image_url") and not args.force:
            stats["already_has_image"] += 1
            continue

        idx = place["_idx"]

        processed += 1

        if args.dry_run:
            result = get_best_image_for_place(place, dry_run=True)
            if result:
                print(f"  [{i+1}] {name} -> would search: {result.get('source', '?')}")
            continue

        # Progress
        if processed % 50 == 0:
            print(f"  Progress: {processed} processed, {found_count} images found, {errors} errors")

        try:
            result = get_best_image_for_place(place, dry_run=False)
            if result:
                # Use thumb URL (800px wide) for display, store full URL too
                image_url = result.get("thumb_url") or result.get("full_url", "")
                if image_url:
                    # Update the place in the master list
                    place_by_idx[idx]["image_url"] = image_url
                    place_by_idx[idx]["image_source"] = result.get("source", "unknown")
                    if result.get("full_url"):
                        place_by_idx[idx]["image_url_full"] = result["full_url"]
                    found_count += 1
                    stats[f"{result['source']}_found"] = stats.get(f"{result['source']}_found", 0) + 1
                    print(f"  ✓ [{i+1}] {name} -> {result['source']}: {image_url[:80]}...")
            else:
                stats["no_image_found"] += 1
        except Exception as e:
            errors += 1
            stats["errors"] += 1
            print(f"  ✗ [{i+1}] {name} -> Error: {e}")

    # Save updated places
    if not args.dry_run and found_count > 0:
        # Rebuild places list preserving order, remove temp keys
        updated_places = []
        for p in places:
            p.pop("_idx", None)
            updated_places.append(p)

        # Backup first
        backup_path = DATA_DIR / "places-pre-images-backup.json"
        if not backup_path.exists():
            with open(backup_path, "w") as f:
                json.dump(places, f, ensure_ascii=False)
            print(f"\nBackup saved to {backup_path}")

        with open(PLACES_FILE, "w") as f:
            json.dump(updated_places, f, ensure_ascii=False, indent=2)
        print(f"\nUpdated {PLACES_FILE} with {found_count} new image URLs")

    # Save results summary
    results = {
        "run_date": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "stats": stats,
        "processed": processed,
        "found": found_count,
        "errors": errors,
        "coverage": f"{(found_count / len(places)) * 100:.1f}%" if places else "0%",
        "total_with_images": sum(1 for p in places if p.get("image_url")),
    }
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("IMAGE COLLECTION RESULTS")
    print("=" * 60)
    print(f"Total places:        {stats['total']}")
    print(f"Processed:           {processed}")
    print(f"Images found:        {found_count}")
    print(f"  - Wikimedia:       {stats.get('wikimedia_commons_found', 0)}")
    print(f"  - Wikipedia:       {stats.get('wikipedia_found', 0)}")
    print(f"  - Website og:      {stats.get('website_og_found', 0)}")
    print(f"No image found:      {stats.get('no_image_found', 0)}")
    print(f"Errors:              {errors}")
    print(f"Already had images:  {stats['already_has_image']}")
    total_with = sum(1 for p in places if p.get("image_url"))
    print(f"\nTotal coverage:      {total_with}/{stats['total']} ({total_with/stats['total']*100:.1f}%)")
    print("=" * 60)


if __name__ == "__main__":
    main()
