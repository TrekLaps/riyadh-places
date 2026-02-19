#!/usr/bin/env python3
"""Comprehensive validation for wain-nrooh.com"""
import os
import re
import json
import glob
from pathlib import Path

BASE = Path("/home/ubuntu/.openclaw/workspace/projects/riyadh-places")
ISSUES = []
FIXES = []
STATS = {"total_html": 0, "passed": 0, "fixed": 0, "data_ok": 0, "data_issues": 0}

def log_issue(file, issue):
    ISSUES.append(f"- **{file}**: {issue}")

def log_fix(file, fix):
    FIXES.append(f"- **{file}**: {fix}")

# ============ HTML VALIDATION ============
html_files = sorted(BASE.glob("*.html"))
STATS["total_html"] = len(html_files)

# Collect all html filenames for internal link checking
all_html_names = {f.name for f in html_files}
all_html_names.add("index.html")

for hf in html_files:
    content = hf.read_text(encoding="utf-8", errors="replace")
    name = hf.name
    issues_for_file = []
    
    # 1. Check title
    if not re.search(r'<title>.+?</title>', content, re.DOTALL):
        issues_for_file.append("Missing <title>")
    
    # 2. Check meta description
    if not re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
        issues_for_file.append("Missing meta description")
    
    # 3. Check lang="ar" dir="rtl"
    if not re.search(r'lang=["\']ar["\']', content):
        issues_for_file.append("Missing lang='ar'")
    if not re.search(r'dir=["\']rtl["\']', content):
        issues_for_file.append("Missing dir='rtl'")
    
    # 4. Check viewport
    if not re.search(r'<meta\s+name=["\']viewport["\']', content, re.IGNORECASE):
        issues_for_file.append("Missing viewport meta")
    
    # 5. Check darkmode.js
    if 'darkmode.js' not in content and name != 'google-site-verification.html':
        issues_for_file.append("Missing darkmode.js")
    
    # 6. Check analytics.js
    if 'analytics.js' not in content and name != 'google-site-verification.html':
        issues_for_file.append("Missing analytics.js")
    
    # 7. Check internal links
    links = re.findall(r'href=["\']([^"\'#]+?\.html)(?:[#?][^"\']*)?["\']', content)
    for link in links:
        link_clean = link.split('?')[0].split('#')[0]
        if not link_clean.startswith('http') and link_clean not in all_html_names:
            issues_for_file.append(f"Broken internal link: {link_clean}")
    
    if issues_for_file:
        for i in issues_for_file:
            log_issue(name, i)
    else:
        STATS["passed"] += 1

# ============ DATA VALIDATION ============

# places.json
places_path = BASE / "data" / "places.json"
if places_path.exists():
    try:
        places = json.loads(places_path.read_text())
        ids = [p.get("id") for p in places if "id" in p]
        
        # Check duplicates
        seen = set()
        dupes = []
        for pid in ids:
            if pid in seen:
                dupes.append(pid)
            seen.add(pid)
        if dupes:
            log_issue("places.json", f"Duplicate IDs: {dupes[:10]}")
            STATS["data_issues"] += 1
        else:
            STATS["data_ok"] += 1
        
        # Check ratings
        bad_ratings = []
        for p in places:
            r = p.get("rating")
            if r is not None:
                try:
                    rv = float(r)
                    if rv < 0 or rv > 5:
                        bad_ratings.append(f"{p.get('id')}: {r}")
                except:
                    bad_ratings.append(f"{p.get('id')}: {r}")
        if bad_ratings:
            log_issue("places.json", f"Invalid ratings: {bad_ratings[:5]}")
            STATS["data_issues"] += 1
        else:
            STATS["data_ok"] += 1
        
        # Check coordinates (Riyadh area: lat 24.3-25.1, lng 46.3-47.1)
        bad_coords = []
        for p in places:
            lat = p.get("lat") or p.get("latitude")
            lng = p.get("lng") or p.get("longitude") or p.get("lon")
            if lat is not None and lng is not None:
                try:
                    lat_f, lng_f = float(lat), float(lng)
                    if not (24.3 <= lat_f <= 25.1 and 46.3 <= lng_f <= 47.1):
                        bad_coords.append(f"{p.get('id')}: ({lat_f},{lng_f})")
                except:
                    bad_coords.append(f"{p.get('id')}: parse error")
        if bad_coords:
            log_issue("places.json", f"Coordinates outside Riyadh: {bad_coords[:5]}")
            STATS["data_issues"] += 1
        else:
            STATS["data_ok"] += 1
        
        print(f"✅ places.json: {len(places)} places, {len(seen)} unique IDs")
    except json.JSONDecodeError as e:
        log_issue("places.json", f"Invalid JSON: {e}")
        STATS["data_issues"] += 1

# prices-initial.json
for jf in ["prices-initial.json", "delivery-prices.json"]:
    jp = BASE / "data" / jf
    if jp.exists():
        try:
            data = json.loads(jp.read_text())
            print(f"✅ {jf}: Valid JSON ({type(data).__name__})")
            STATS["data_ok"] += 1
        except json.JSONDecodeError as e:
            log_issue(jf, f"Invalid JSON: {e}")
            STATS["data_issues"] += 1

# ============ PERFORMANCE CHECKS ============
perf_issues = []

for hf in html_files:
    content = hf.read_text(encoding="utf-8", errors="replace")
    name = hf.name
    
    # Check for images without lazy loading
    imgs = re.findall(r'<img\s[^>]+>', content)
    for img in imgs:
        if 'loading=' not in img and 'data-src' not in img:
            perf_issues.append(f"{name}: img without lazy loading")
            break  # one per file is enough
    
    # Check for JS without defer/async (skip inline scripts)
    scripts = re.findall(r'<script\s+src=["\'][^"\']+["\'][^>]*>', content)
    for s in scripts:
        if 'defer' not in s and 'async' not in s:
            perf_issues.append(f"{name}: script without defer/async: {s[:60]}")

# Check CSS for font-display
for css_file in (BASE / "css").glob("*.css"):
    css_content = css_file.read_text(encoding="utf-8", errors="replace")
    if '@font-face' in css_content and 'font-display' not in css_content:
        perf_issues.append(f"css/{css_file.name}: @font-face without font-display: swap")

# ============ PRINT REPORT ============
print("\n" + "="*60)
print("VALIDATION REPORT")
print("="*60)
print(f"\nTotal HTML files: {STATS['total_html']}")
print(f"Clean (no issues): {STATS['passed']}")
print(f"Data checks OK: {STATS['data_ok']}")
print(f"Data issues: {STATS['data_issues']}")

if ISSUES:
    print(f"\n🔴 ISSUES FOUND ({len(ISSUES)}):")
    for i in ISSUES:
        print(f"  {i}")

if perf_issues:
    print(f"\n⚡ PERFORMANCE ISSUES ({len(perf_issues)}):")
    for p in perf_issues:
        print(f"  - {p}")

if not ISSUES and not perf_issues:
    print("\n🎉 All checks passed!")

# Write summary for use by fixer
with open(BASE / "scripts" / "validation-results.json", "w") as f:
    json.dump({
        "issues": ISSUES,
        "perf_issues": perf_issues,
        "fixes": FIXES,
        "stats": STATS
    }, f, ensure_ascii=False, indent=2)
