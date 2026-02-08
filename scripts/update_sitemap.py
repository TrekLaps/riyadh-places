#!/usr/bin/env python3
"""Update sitemap.xml with all neighborhood pages."""
import glob
import os

PROJECT_DIR = '/home/ubuntu/.openclaw/workspace/projects/riyadh-places'
SITEMAP_PATH = os.path.join(PROJECT_DIR, 'sitemap.xml')

# Read existing sitemap
with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all neighborhood pages
pages = sorted(glob.glob(os.path.join(PROJECT_DIR, 'neighborhood-*.html')))
slugs = [os.path.basename(p).replace('.html', '') for p in pages]

# Check which are already in sitemap
existing = []
new = []
for slug in slugs:
    url = f'https://wain-nrooh.com/{slug}.html'
    if url in content:
        existing.append(slug)
    else:
        new.append(slug)

print(f"Already in sitemap: {len(existing)}")
print(f"New to add: {len(new)}")

# Build new entries
new_entries = ''
for slug in new:
    new_entries += f'  <url><loc>https://wain-nrooh.com/{slug}.html</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'

# Insert before closing </urlset>
content = content.replace('</urlset>', new_entries + '</urlset>')

with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Added {len(new)} new neighborhood pages to sitemap.xml")
for slug in new:
    print(f"  + {slug}")
