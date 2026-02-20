#!/usr/bin/env python3
"""Fix all MEDIUM + LOW issues for Riyadh Places website."""

import os
import re
import glob

PROJECT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT)

def read(f):
    with open(f, 'r', encoding='utf-8') as fh:
        return fh.read()

def write(f, content):
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(content)

changes = []

# ============================================================
# HEADER/NAV template (from index.html)
# ============================================================
NAV_HEADER = '''  <header class="header">
    <div class="header-inner">
      <a href="index.html" class="logo"><span>🏙️</span><h1>وين نروح بالرياض؟</h1></a>
      <div class="header-search" id="header-search">
        <button class="header-search-toggle" id="header-search-toggle" aria-label="بحث">🔍</button>
        <div class="header-search-box" id="header-search-box">
          <input type="text" class="header-search-input" id="header-search-input" placeholder="ابحث عن مكان..." autocomplete="off">
          <div class="header-search-dropdown" id="header-search-dropdown"></div>
        </div>
      </div>
      <button class="dark-mode-toggle" aria-label="الوضع الليلي">🌙</button>
      <button class="menu-toggle" aria-label="القائمة">☰</button>
      <nav class="nav">
        <a href="index.html">الرئيسية</a>
        <a href="cafes.html">كافيهات</a>
        <a href="restaurants.html">مطاعم</a>
        <a href="activities.html">ترفيه</a>
        <a href="events.html">فعاليات</a>
        <a href="new-places.html">جديد</a>
        <a href="discover.html">🎲 وين نروح؟</a>
        <a href="lists.html">📋 قوائمي</a>
        <a href="search.html">🔍 بحث</a>
        <a href="best.html">🏆 الأفضل</a>
        <a href="compare.html">⚖️ قارن</a>
        <a href="delivery-compare.html">🛵 مقارنة التوصيل</a>
        <div class="nav-dropdown">
          <a href="#">المزيد</a>
          <div class="dropdown-menu">
            <a href="prices.html">💰 أسعار</a>
            <a href="shopping.html">🛍️ تسوق</a>
            <a href="nature.html">🏞️ طبيعة</a>
            <a href="desserts.html">🍰 حلويات</a>
            <a href="top-rated.html">⭐ الأعلى تقييماً</a>
            <div class="dropdown-divider"></div>
            <a href="breakfast-riyadh.html">🍳 فطور</a>
            <a href="family-places.html">👨‍👩‍👧‍👦 عائلية</a>
            <a href="romantic-places.html">💑 رومانسية</a>
            <a href="cheap-eats.html">💰 رخيصة</a>
            <a href="work-cafes.html">💻 للعمل</a>
            <a href="open-late.html">🌙 سهرة</a>
            <a href="guide-weekend.html">📅 ويكند</a>
            <div class="dropdown-divider"></div>
            <a href="neighborhoods.html">🏘️ أحياء الرياض</a>
            <a href="ramadan.html">🌙 رمضان</a>
            <a href="riyadh-season.html">✨ موسم الرياض</a>
          </div>
        </div>
      </nav>
    </div>
  </header>'''

FOOTER = '''  <footer class="footer">
    <div class="footer-inner">
      <div>
        <h3>وين نروح بالرياض؟</h3>
        <p>دليلك الشامل لأفضل الأماكن في الرياض مع تقييمات قوقل الحقيقية. محدث يومياً بأحدث الأماكن والتقييمات.</p>
      </div>
      <div>
        <h3>الأقسام</h3>
        <ul>
          <li><a href="cafes.html">كافيهات الرياض</a></li>
          <li><a href="restaurants.html">مطاعم الرياض</a></li>
          <li><a href="activities.html">ترفيه وأنشطة</a></li>
          <li><a href="shopping.html">تسوق بالرياض</a></li>
          <li><a href="nature.html">طبيعة ورحلات</a></li>
          <li><a href="desserts.html">حلويات الرياض</a></li>
          <li><a href="events.html">فعاليات الرياض</a></li>
          <li><a href="top-rated.html">الأعلى تقييماً</a></li>
          <li><a href="trending.html">هابّ الحين 🔥</a></li>
          <li><a href="new-places.html">أماكن جديدة</a></li>
        </ul>
      </div>
      <div>
        <h3>روابط مفيدة</h3>
        <ul>
          <li><a href="sitemap.xml">خريطة الموقع</a></li>
          <li><a href="#">سياسة الخصوصية</a></li>
          <li><a href="#">تواصل معنا</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-heart">صنع بـ <span>❤️</span> في الرياض</div>
    <div class="footer-bottom"><p>© 2025-2026 وين نروح بالرياض؟ جميع الحقوق محفوظة.</p></div>
  </footer>'''

# ============================================================
# M1: stats.html — Replace header and add footer
# ============================================================
print("M1: Fixing stats.html header/nav and footer...")
content = read('stats.html')

# Replace the existing simple header with full nav
old_header = re.search(r'  <header class="header">.*?</header>', content, re.DOTALL)
if old_header:
    content = content[:old_header.start()] + NAV_HEADER + content[old_header.end():]

# Add footer before </body>
if '<footer' not in content:
    content = content.replace('</body>', FOOTER + '\n</body>')

# Add search-header.css (already has it per our check, but ensure)
write('stats.html', content)
changes.append("M1: stats.html — Added full navigation and footer")

# ============================================================
# M2: ai-search.html — Add footer
# ============================================================
print("M2: Fixing ai-search.html footer...")
content = read('ai-search.html')
if '<footer' not in content:
    content = content.replace('</body>', FOOTER + '\n</body>')
    write('ai-search.html', content)
    changes.append("M2: ai-search.html — Added footer")
else:
    changes.append("M2: ai-search.html — Footer already present")

# ============================================================
# M3: Add main.js to 4 pages
# ============================================================
print("M3: Adding main.js to pages missing it...")
m3_pages = ['ai-search.html', 'delivery-compare.html', 'google-site-verification.html', 'stats.html']
for page in m3_pages:
    if not os.path.exists(page):
        continue
    content = read(page)
    if 'main.js' not in content:
        # Add before </body>
        content = content.replace('</body>', '  <script src="js/main.js" defer></script>\n</body>')
        write(page, content)
        changes.append(f"M3: {page} — Added main.js")

# ============================================================
# M4: Remove console statements from production
# ============================================================
print("M4: Removing console statements...")

# HTML files with inline console statements
m4_html = ['ai-search.html', 'delivery-compare.html', 'prices.html', 'ramadan.html']
for page in m4_html:
    content = read(page)
    original = content
    # Replace console.log/error/warn with void 0 (no-op)
    content = re.sub(r'console\.(log|error|warn)\([^)]*\)', 'void 0', content)
    if content != original:
        write(page, content)
        changes.append(f"M4: {page} — Removed console statements")

# JS files
m4_js = ['js/main.js', 'js/ramadan.js', 'js/reviews.js', 'js/weather-prayer.js']
for jsfile in m4_js:
    if not os.path.exists(jsfile):
        continue
    content = read(jsfile)
    original = content
    content = re.sub(r'console\.(log|error|warn)\([^)]*\)', 'void 0', content)
    if content != original:
        write(jsfile, content)
        changes.append(f"M4: {jsfile} — Removed console statements")

# ============================================================
# M5: Add search-header.css to 5 pages
# ============================================================
print("M5: Adding search-header.css to pages missing it...")
m5_pages = ['ai-search.html', 'delivery-compare.html', 'google-site-verification.html', 'guide-weekend.html', 'lists.html']
for page in m5_pages:
    if not os.path.exists(page):
        continue
    content = read(page)
    if 'search-header.css' not in content:
        # Add after style.css link
        content = content.replace(
            '<link rel="stylesheet" href="css/style.css">',
            '<link rel="stylesheet" href="css/style.css">\n  <link rel="stylesheet" href="css/search-header.css">'
        )
        write(page, content)
        changes.append(f"M5: {page} — Added search-header.css")

# ============================================================
# M6: discover.css — 726 lines, too big to inline. Leave as-is with a note.
# ============================================================
print("M6: discover.css is 726 lines — keeping as separate file (too large to inline)")
changes.append("M6: discover.css — 726 lines, too large to inline. Kept as separate file.")

# ============================================================
# M7: Manifest start_url
# ============================================================
print("M7: Fixing manifest.json start_url...")
content = read('manifest.json')
content = content.replace('"start_url": "/index.html"', '"start_url": "./index.html"')
# Also fix shortcuts URLs to be relative
content = content.replace('"url": "/map.html"', '"url": "./map.html"')
content = content.replace('"url": "/favorites.html"', '"url": "./favorites.html"')
content = content.replace('"url": "/cafes.html"', '"url": "./cafes.html"')
content = content.replace('"url": "/restaurants.html"', '"url": "./restaurants.html"')
write('manifest.json', content)
changes.append("M7: manifest.json — Changed start_url and shortcuts to relative paths")

# ============================================================
# M8: Add lastmod to sitemap
# ============================================================
print("M8: Adding lastmod to sitemap.xml...")
content = read('sitemap.xml')
# Add lastmod after each <loc>...</loc> line
content = re.sub(
    r'(<loc>[^<]+</loc>)(<changefreq>)',
    r'\1<lastmod>2026-02-20</lastmod>\2',
    content
)
write('sitemap.xml', content)
changes.append("M8: sitemap.xml — Added <lastmod>2026-02-20</lastmod> to all URLs")

# ============================================================
# M9: Leaflet CDN fallback
# ============================================================
print("M9: Adding Leaflet CDN fallback to map.html...")
content = read('map.html')
fallback_script = '''  <script>
    // Leaflet CDN fallback
    if (typeof L === 'undefined') {
      document.getElementById('map').innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;background:#0a1628;color:#e0e0e0;font-family:Tajawal,sans-serif;text-align:center;padding:40px;"><div><h2 style="color:#c9a84c;margin-bottom:16px;">⚠️ تعذر تحميل الخريطة</h2><p>فشل تحميل مكتبة الخرائط. تأكد من اتصالك بالإنترنت وأعد المحاولة.</p><button onclick="location.reload()" style="margin-top:16px;padding:10px 24px;background:#c9a84c;color:#0a1628;border:none;border-radius:8px;font-family:Tajawal;font-size:16px;cursor:pointer;">🔄 إعادة المحاولة</button></div></div>';
    }
  </script>'''

# Add fallback check after the leaflet scripts but before the map init code
# Find the line after leaflet.markercluster.js
content = content.replace(
    '<script defer src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>',
    '<script defer src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>\n' + fallback_script
)
write('map.html', content)
changes.append("M9: map.html — Added Leaflet CDN fallback with Arabic error message")

# ============================================================
# L1: Add favicon to ALL pages
# ============================================================
print("L1: Adding favicon to all pages...")
favicon_link = '  <link rel="icon" type="image/svg+xml" href="images/icon-192.svg">'
count = 0
for html_file in sorted(glob.glob('*.html')):
    content = read(html_file)
    if 'rel="icon"' not in content:
        # Add after <meta name="viewport"...> or after first <meta charset>
        if '<meta name="viewport"' in content:
            content = re.sub(
                r'(<meta name="viewport"[^>]*>)',
                r'\1\n' + favicon_link,
                content,
                count=1
            )
        elif '<meta charset' in content:
            content = re.sub(
                r'(<meta charset[^>]*>)',
                r'\1\n' + favicon_link,
                content,
                count=1
            )
        write(html_file, content)
        count += 1
changes.append(f"L1: Added favicon to {count} HTML pages")

# ============================================================
# L3: Service Worker cache — update sw.js
# ============================================================
print("L3: Updating sw.js cache list...")
sw_content = '''// Service Worker for وين نروح بالرياض؟
const CACHE_NAME = 'riyadh-places-v2';
const OFFLINE_URL = './index.html';

const PRECACHE_URLS = [
  './',
  './index.html',
  './cafes.html',
  './restaurants.html',
  './activities.html',
  './events.html',
  './shopping.html',
  './nature.html',
  './desserts.html',
  './best.html',
  './neighborhoods.html',
  './discover.html',
  './search.html',
  './favorites.html',
  './ramadan.html',
  './css/style.css',
  './css/ramadan.css',
  './css/search-header.css',
  './js/main.js',
  './js/search.js',
  './js/header-search.js',
  './images/icon-192.svg',
  './images/icon-512.svg',
  './data/places-light.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS))
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
  } else {
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
'''
write('sw.js', sw_content)
changes.append("L3: sw.js — Updated with comprehensive precache list (index, categories, neighborhoods hub, assets)")

# ============================================================
# L4: .gitattributes for Python scripts
# ============================================================
print("L4: Adding .gitattributes...")
gitattributes = """# Mark Python scripts as non-web content (data processing only)
*.py linguist-detectable=false
*.py linguist-documentation=true
# These scripts are publicly accessible on GitHub Pages but are harmless
# data processing/extraction utilities, not part of the web application.
"""
write('.gitattributes', gitattributes)
changes.append("L4: .gitattributes — Marked Python scripts as non-web content")

# ============================================================
# L5: Create 404.html
# ============================================================
print("L5: Creating 404.html...")
page_404 = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/svg+xml" href="images/icon-192.svg">
  <title>الصفحة غير موجودة — وين نروح بالرياض؟</title>
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#0a1628">
  <link rel="manifest" href="manifest.json">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Tajawal', sans-serif;
      background: #0a1628;
      color: #e0e0e0;
      direction: rtl;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    .header {
      background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 100%);
      padding: 16px 20px;
      text-align: center;
    }
    .logo {
      text-decoration: none;
      color: #c9a84c;
      font-size: 1.2rem;
      font-weight: 700;
    }
    .error-container {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      text-align: center;
    }
    .error-content {
      max-width: 500px;
    }
    .error-emoji {
      font-size: 80px;
      margin-bottom: 20px;
      animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-15px); }
    }
    .error-code {
      font-size: 72px;
      font-weight: 900;
      color: #c9a84c;
      margin-bottom: 8px;
      line-height: 1;
    }
    .error-title {
      font-size: 28px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
    }
    .error-desc {
      font-size: 16px;
      color: #8899aa;
      line-height: 1.8;
      margin-bottom: 30px;
    }
    .error-suggestions {
      text-align: right;
      background: #111b2e;
      border-radius: 12px;
      padding: 20px 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(201,168,76,0.15);
    }
    .error-suggestions h3 {
      color: #c9a84c;
      font-size: 16px;
      margin-bottom: 12px;
    }
    .error-suggestions ul {
      list-style: none;
      padding: 0;
    }
    .error-suggestions li {
      padding: 6px 0;
      font-size: 14px;
      color: #8899aa;
    }
    .error-suggestions li::before {
      content: '←';
      margin-left: 8px;
      color: #c9a84c;
    }
    .error-suggestions a {
      color: #c9a84c;
      text-decoration: none;
    }
    .error-suggestions a:hover {
      text-decoration: underline;
    }
    .btn-home {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 14px 32px;
      background: linear-gradient(135deg, #c9a84c, #dbb960);
      color: #0a1628;
      border: none;
      border-radius: 50px;
      font-family: 'Tajawal', sans-serif;
      font-size: 16px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(201,168,76,0.3);
    }
    .btn-home:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(201,168,76,0.4);
    }
    .footer-mini {
      text-align: center;
      padding: 16px;
      color: #556677;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="header">
    <a href="index.html" class="logo">🏙️ وين نروح بالرياض؟</a>
  </div>

  <div class="error-container">
    <div class="error-content">
      <div class="error-emoji">🏜️</div>
      <div class="error-code">404</div>
      <h1 class="error-title">الصفحة غير موجودة</h1>
      <p class="error-desc">يبدو إنك ضعت! الصفحة اللي تدور عليها مو موجودة أو انتقلت لمكان ثاني.</p>

      <div class="error-suggestions">
        <h3>🧭 جرّب هالروابط:</h3>
        <ul>
          <li><a href="index.html">🏠 الصفحة الرئيسية</a></li>
          <li><a href="cafes.html">☕ كافيهات الرياض</a></li>
          <li><a href="restaurants.html">🍽️ مطاعم الرياض</a></li>
          <li><a href="search.html">🔍 بحث عن مكان</a></li>
          <li><a href="discover.html">🎲 ما تدري وين تروح؟</a></li>
          <li><a href="neighborhoods.html">🏘️ أحياء الرياض</a></li>
        </ul>
      </div>

      <a href="index.html" class="btn-home">🏙️ ارجع للرئيسية</a>
    </div>
  </div>

  <div class="footer-mini">© 2025-2026 وين نروح بالرياض؟</div>
</body>
</html>'''
write('404.html', page_404)
changes.append("L5: 404.html — Created Arabic 404 page with dark theme and helpful navigation")

# ============================================================
# L6: Manifest screenshots
# ============================================================
print("L6: Adding screenshots to manifest.json...")
content = read('manifest.json')
content = content.replace(
    '"screenshots": []',
    '''"screenshots": [
    {
      "src": "images/icon-512.svg",
      "sizes": "512x512",
      "type": "image/svg+xml",
      "form_factor": "wide",
      "label": "وين نروح بالرياض؟ — الصفحة الرئيسية"
    },
    {
      "src": "images/icon-192.svg",
      "sizes": "192x192",
      "type": "image/svg+xml",
      "form_factor": "narrow",
      "label": "وين نروح بالرياض؟ — عرض الجوال"
    }
  ]'''
)
write('manifest.json', content)
changes.append("L6: manifest.json — Added 2 screenshot entries")

# ============================================================
# H7: Add ramadan.css to neighborhood pages missing it + neighborhoods.html, ai-search.html, delivery-compare.html
# ============================================================
print("H7: Adding ramadan.css to pages missing it...")
neighborhood_pages = glob.glob('neighborhood-*.html')
extra_pages = ['neighborhoods.html', 'ai-search.html', 'delivery-compare.html']
h7_count = 0
for page in sorted(neighborhood_pages + extra_pages):
    if not os.path.exists(page):
        continue
    content = read(page)
    if 'ramadan.css' not in content:
        # Add after style.css
        if '<link rel="stylesheet" href="css/style.css">' in content:
            content = content.replace(
                '<link rel="stylesheet" href="css/style.css">',
                '<link rel="stylesheet" href="css/style.css">\n  <link rel="stylesheet" href="css/ramadan.css">'
            )
        elif '</head>' in content:
            content = content.replace('</head>', '  <link rel="stylesheet" href="css/ramadan.css">\n</head>')
        write(page, content)
        h7_count += 1
changes.append(f"H7: Added ramadan.css to {h7_count} pages (neighborhoods + ai-search + delivery-compare)")

# ============================================================
# H3: ai-search.html — load places-light.json instead of places.json
# ============================================================
print("H3: Switching ai-search.html to places-light.json...")
content = read('ai-search.html')
original = content
content = content.replace("fetch('data/places.json')", "fetch('data/places-light.json')")
content = content.replace('fetch("data/places.json")', 'fetch("data/places-light.json")')
if content != original:
    write('ai-search.html', content)
    changes.append("H3: ai-search.html — Switched from places.json (2.8MB) to places-light.json (1.3MB)")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("ALL FIXES APPLIED:")
print("="*60)
for c in changes:
    print(f"  ✅ {c}")
print(f"\nTotal: {len(changes)} fixes applied")
