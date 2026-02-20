#!/usr/bin/env python3
"""Fix all CRITICAL and HIGH SEO issues for Riyadh Places website."""

import os
import re
import glob
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://treklaps.github.io/riyadh-places"
OG_IMAGE_URL = f"{BASE_URL}/images/icon-512.svg"

html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
print(f"Found {len(html_files)} HTML files")

# Category pages (for structured data)
CATEGORY_PAGES = [
    "activities.html", "cafes.html", "restaurants.html", "desserts.html",
    "shopping.html", "nature.html", "family-places.html", "open-late.html",
    "cheap-eats.html", "top-rated.html", "trending.html", "new-places.html",
    "work-cafes.html", "romantic-places.html", "breakfast-riyadh.html",
    "best.html", "neighborhoods.html", "lists.html", "prices.html",
    "riyadh-season.html", "ramadan.html", "delivery-compare.html",
    "events.html", "discover.html"
]

# Neighborhood pages (also get ItemList)
NEIGHBORHOOD_PAGES = [f for f in os.listdir(BASE_DIR) if f.startswith("neighborhood-") and f.endswith(".html")]

stats = {
    "canonical_fixed": 0,
    "canonical_added": 0,
    "og_image_added": 0,
    "twitter_added": 0,
    "manifest_added": 0,
    "sw_registration_added": 0,
    "structured_data_added": 0,
    "noindex_added": 0,
}

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # === C1: Fix canonical URLs (wain-nrooh.com -> treklaps.github.io) ===
    if "wain-nrooh.com" in content:
        # Fix canonical href
        if filename == "index.html":
            content = re.sub(
                r'<link\s+rel="canonical"\s+href="https?://wain-nrooh\.com/?"',
                f'<link rel="canonical" href="{BASE_URL}/"',
                content
            )
        else:
            content = re.sub(
                r'<link\s+rel="canonical"\s+href="https?://wain-nrooh\.com/([^"]*)"',
                lambda m: f'<link rel="canonical" href="{BASE_URL}/{m.group(1)}"',
                content
            )
        # Fix og:url
        if filename == "index.html":
            content = re.sub(
                r'<meta\s+property="og:url"\s+content="https?://wain-nrooh\.com/?"',
                f'<meta property="og:url" content="{BASE_URL}/"',
                content
            )
        else:
            content = re.sub(
                r'<meta\s+property="og:url"\s+content="https?://wain-nrooh\.com/([^"]*)"',
                lambda m: f'<meta property="og:url" content="{BASE_URL}/{m.group(1)}"',
                content
            )
        if content != original:
            stats["canonical_fixed"] += 1
    
    # === H5: Add canonical to pages missing it ===
    if '<link rel="canonical"' not in content:
        if filename == "index.html":
            canonical_url = f"{BASE_URL}/"
        else:
            canonical_url = f"{BASE_URL}/{filename}"
        canonical_tag = f'  <link rel="canonical" href="{canonical_url}">\n'
        # Insert after <meta name="robots"> or after viewport
        if '<meta name="robots"' in content:
            content = re.sub(
                r'(<meta\s+name="robots"[^>]*>)\n',
                r'\1\n' + canonical_tag,
                content
            )
        elif '<meta name="viewport"' in content:
            content = re.sub(
                r'(<meta\s+name="viewport"[^>]*>)\n',
                r'\1\n' + canonical_tag,
                content
            )
        stats["canonical_added"] += 1
    
    # === C4: Add og:image to ALL pages ===
    if 'og:image' not in content:
        og_image_tag = f'  <meta property="og:image" content="{OG_IMAGE_URL}">\n'
        # Insert after og:site_name or og:locale or og:url or og:description
        inserted = False
        for anchor in ['og:site_name', 'og:locale', 'og:url', 'og:description', 'og:title', 'og:type']:
            pattern = f'(<meta\\s+property="{anchor}"[^>]*>)\\n'
            if re.search(pattern, content):
                content = re.sub(pattern, r'\1\n' + og_image_tag, content, count=1)
                inserted = True
                break
        if not inserted:
            # Insert before </head>
            content = content.replace('</head>', og_image_tag + '</head>')
        stats["og_image_added"] += 1
    
    # === H2: Add Twitter Card meta tags ===
    if 'twitter:card' not in content:
        # Extract title and description from existing meta
        title_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', content)
        desc_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', content)
        title = title_match.group(1) if title_match else "وين نروح بالرياض؟"
        desc = desc_match.group(1) if desc_match else "دليلك الشامل لأفضل أماكن الرياض"
        
        twitter_tags = (
            f'  <meta name="twitter:card" content="summary_large_image">\n'
            f'  <meta name="twitter:title" content="{title}">\n'
            f'  <meta name="twitter:description" content="{desc}">\n'
            f'  <meta name="twitter:image" content="{OG_IMAGE_URL}">\n'
        )
        # Insert before </head> or after og tags
        if 'og:site_name' in content:
            content = re.sub(
                r'(<meta\s+property="og:site_name"[^>]*>)\n',
                r'\1\n' + twitter_tags,
                content, count=1
            )
        elif 'og:image' in content:
            content = re.sub(
                r'(<meta\s+property="og:image"[^>]*>)\n',
                r'\1\n' + twitter_tags,
                content, count=1
            )
        else:
            content = content.replace('</head>', twitter_tags + '</head>')
        stats["twitter_added"] += 1
    else:
        # Page has twitter:card but may be missing twitter:image
        if 'twitter:image' not in content:
            twitter_image = f'  <meta name="twitter:image" content="{OG_IMAGE_URL}">\n'
            content = re.sub(
                r'(<meta\s+name="twitter:description"[^>]*>)\n',
                r'\1\n' + twitter_image,
                content, count=1
            )
    
    # === H6: Add manifest.json link ===
    if 'rel="manifest"' not in content:
        manifest_tag = '  <link rel="manifest" href="manifest.json">\n'
        if '<meta name="theme-color"' in content:
            content = re.sub(
                r'(<meta\s+name="theme-color"[^>]*>)\n',
                manifest_tag + r'\1\n',
                content, count=1
            )
        else:
            content = content.replace('</head>', manifest_tag + '</head>')
        stats["manifest_added"] += 1
    
    # === C3: Add service worker registration ===
    if 'serviceWorker' not in content and 'service-worker' not in content:
        sw_script = '''  <script>
    if('serviceWorker' in navigator){navigator.serviceWorker.register('sw.js').catch(function(){});}
  </script>
'''
        content = content.replace('</body>', sw_script + '</body>')
        stats["sw_registration_added"] += 1
    
    # === H8: noindex for google-site-verification.html ===
    if filename == "google-site-verification.html":
        if '<meta name="robots" content="noindex"' not in content:
            if '<meta name="robots"' in content:
                content = re.sub(
                    r'<meta\s+name="robots"\s+content="[^"]*"',
                    '<meta name="robots" content="noindex, nofollow"',
                    content
                )
            else:
                noindex_tag = '  <meta name="robots" content="noindex, nofollow">\n'
                content = content.replace('</head>', noindex_tag + '</head>')
            stats["noindex_added"] += 1
    
    # === H1: Add structured data ===
    if '<script type="application/ld+json">' not in content:
        schema = None
        
        if filename == "index.html":
            schema = {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "وين نروح بالرياض؟",
                "url": f"{BASE_URL}/",
                "description": "دليلك الشامل لأفضل أماكن الرياض 2025-2026",
                "inLanguage": "ar",
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{BASE_URL}/search.html?q={{search_term_string}}",
                    "query-input": "required name=search_term_string"
                }
            }
        elif filename == "place.html":
            schema = {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": "{{place_name}}",
                "description": "{{place_description}}",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "الرياض",
                    "addressCountry": "SA"
                }
            }
        elif filename in CATEGORY_PAGES or filename in NEIGHBORHOOD_PAGES:
            # Extract page title for the schema
            title_match = re.search(r'<title>([^<]*)</title>', content)
            page_title = title_match.group(1) if title_match else filename.replace('.html', '').replace('-', ' ').title()
            schema = {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": page_title,
                "url": f"{BASE_URL}/{filename}",
                "numberOfItems": 0,
                "itemListElement": []
            }
        
        if schema:
            schema_tag = f'  <script type="application/ld+json">\n  {json.dumps(schema, ensure_ascii=False, indent=2)}\n  </script>\n'
            content = content.replace('</head>', schema_tag + '</head>')
            stats["structured_data_added"] += 1
    
    # Write back if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

# === Create sw.js if it doesn't exist ===
sw_path = os.path.join(BASE_DIR, "sw.js")
if not os.path.exists(sw_path):
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write("""// Service Worker for وين نروح بالرياض؟
const CACHE_NAME = 'riyadh-places-v1';
const OFFLINE_URL = '/index.html';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll([OFFLINE_URL]))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(OFFLINE_URL))
    );
  }
});
""")
    print("Created sw.js")

# === Fix sitemap.xml — ensure URLs use correct base ===
sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap = f.read()
# Already using treklaps.github.io, but ensure consistency
sitemap = sitemap.replace("https://wain-nrooh.com/", f"{BASE_URL}/")
sitemap = sitemap.replace("https://wain-nrooh.com", BASE_URL)
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap)
print("Updated sitemap.xml")

# === Fix robots.txt ===
robots_path = os.path.join(BASE_DIR, "robots.txt")
with open(robots_path, "r", encoding="utf-8") as f:
    robots = f.read()
robots = robots.replace("https://wain-nrooh.com/", f"{BASE_URL}/")
with open(robots_path, "w", encoding="utf-8") as f:
    f.write(robots)
print("Updated robots.txt")

print("\n=== RESULTS ===")
for k, v in stats.items():
    print(f"  {k}: {v}")
print("Done!")
