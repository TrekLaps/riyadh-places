#!/usr/bin/env python3
"""Auto-fix all validation issues for wain-nrooh.com"""
import re
import glob
from pathlib import Path

BASE = Path("/home/ubuntu/.openclaw/workspace/projects/riyadh-places")
fixes = []

html_files = sorted(BASE.glob("*.html"))

for hf in html_files:
    name = hf.name
    if name == "google-site-verification.html":
        continue  # Google verification file, skip
    
    content = hf.read_text(encoding="utf-8", errors="replace")
    original = content
    
    # 1. Fix broken foundation-day.html links → point to events.html
    content = content.replace('href="foundation-day.html"', 'href="events.html"')
    
    # 2. Add defer to all local script src tags (not inline scripts)
    # Match <script src="..."> without defer or async
    def add_defer(m):
        tag = m.group(0)
        if 'defer' in tag or 'async' in tag:
            return tag
        return tag.replace('<script ', '<script defer ')
    
    content = re.sub(r'<script\s+src=["\'][^"\']+["\'][^>]*>', add_defer, content)
    
    # 3. Add lazy loading to images (skip first image per page for LCP)
    img_count = [0]
    def add_lazy(m):
        tag = m.group(0)
        img_count[0] += 1
        if img_count[0] <= 1:  # Skip first image (likely LCP)
            return tag
        if 'loading=' in tag:
            return tag
        return tag.replace('<img ', '<img loading="lazy" ')
    
    content = re.sub(r'<img\s[^>]+>', add_lazy, content)
    
    # 4. Fix place.html missing title
    if name == "place.html" and not re.search(r'<title>.+?</title>', content, re.DOTALL):
        content = content.replace('<head>', '<head>\n  <title>تفاصيل المكان - وين نروح بالرياض؟</title>')
        fixes.append(f"{name}: Added title")
    
    # 5. Fix stats.html missing meta description
    if name == "stats.html" and not re.search(r'<meta\s+name=["\']description["\']', content):
        content = content.replace('</title>', '</title>\n  <meta name="description" content="إحصائيات وأرقام عن أماكن الرياض - وين نروح بالرياض؟">')
        fixes.append(f"{name}: Added meta description")
    
    # 6. Add analytics.js to delivery-compare.html if missing
    if name == "delivery-compare.html" and 'analytics.js' not in content:
        content = content.replace('</body>', '  <script defer src="js/analytics.js"></script>\n</body>')
        fixes.append(f"{name}: Added analytics.js")
    
    if content != original:
        hf.write_text(content, encoding="utf-8")
        if name not in [f.split(":")[0] for f in fixes]:
            fixes.append(f"{name}: Fixed links/defer/lazy")

# 7. Add font-display: swap to CSS @font-face
for css_file in (BASE / "css").glob("*.css"):
    content = css_file.read_text(encoding="utf-8", errors="replace")
    if '@font-face' in content and 'font-display' not in content:
        content = content.replace('@font-face {', '@font-face {\n  font-display: swap;')
        css_file.write_text(content, encoding="utf-8")
        fixes.append(f"css/{css_file.name}: Added font-display: swap")

print(f"✅ Applied {len(fixes)} categories of fixes across 86 HTML files")
for f in fixes:
    print(f"  - {f}")
