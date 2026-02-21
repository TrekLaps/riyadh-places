#!/usr/bin/env python3
"""Generate neighborhood HTML pages for neighborhoods with 5+ places that don't have pages yet."""
import json
import os
import re

# Neighborhoods that need pages (from our analysis)
NEEDS_PAGES = [
    {"name_ar": "السليمانية", "name_en": "As Sulimaniyah", "id": "sulaymaniyah", "count": 132},
    {"name_ar": "الملز", "name_en": "Malaz", "id": "malaz", "count": 122},
    {"name_ar": "الربيع", "name_en": "Ar Rabi", "id": "ar-rabi", "count": 98},
    {"name_ar": "القيروان", "name_en": "Al Qirawan", "id": "qirawan", "count": 52},
    {"name_ar": "الديرة", "name_en": "Ad Dirah", "id": "dirah", "count": 44},
    {"name_ar": "الخليج", "name_en": "Al Khaleej", "id": "khaleej", "count": 40},
    {"name_ar": "الرائد", "name_en": "Ar Raid", "id": "raid", "count": 32},
    {"name_ar": "العريجاء", "name_en": "Al Uraija", "id": "uraija", "count": 32},
    {"name_ar": "الفلاح", "name_en": "Al Falah", "id": "falah", "count": 30},
    {"name_ar": "المحمدية", "name_en": "Al Muhammadiyah", "id": "muhammadiyah", "count": 30},
    {"name_ar": "الحي الدبلوماسي", "name_en": "Diplomatic Quarter", "id": "dq", "count": 30},
    {"name_ar": "البديعة", "name_en": "Al Badiah", "id": "badiah", "count": 28},
    {"name_ar": "جاكس", "name_en": "JAX District", "id": "jax", "count": 26},
    {"name_ar": "غرناطة", "name_en": "Ghirnatah", "id": "ghirnatah2", "count": 24},
    {"name_ar": "قرطبة", "name_en": "Qurtubah", "id": "qurtubah", "count": 20},
    {"name_ar": "النظيم", "name_en": "An Nadheem", "id": "nadheem", "count": 20},
    {"name_ar": "النفل", "name_en": "An Nafl", "id": "nafl", "count": 16},
    {"name_ar": "الوادي", "name_en": "Al Wadi", "id": "wadi", "count": 16},
    {"name_ar": "القدس", "name_en": "Al Quds", "id": "quds", "count": 16},
    {"name_ar": "الشميسي", "name_en": "Ash Shumaisi", "id": "shumaisi", "count": 16},
    {"name_ar": "الغدير", "name_en": "Al Ghadir", "id": "ghadir", "count": 14},
    {"name_ar": "الجنادرية", "name_en": "Al Janadriyah", "id": "janadriyah", "count": 10},
    {"name_ar": "إشبيلية", "name_en": "Ishbiliyah", "id": "ishbiliyah", "count": 10},
    {"name_ar": "المغرزات", "name_en": "Al Mughrizat", "id": "mughrizat2", "count": 10},
    {"name_ar": "عرقة", "name_en": "Irqah", "id": "irqah", "count": 10},
    {"name_ar": "الروابي", "name_en": "Ar Rawabi", "id": "rawabi", "count": 10},
    {"name_ar": "المنصورة", "name_en": "Al Mansurah", "id": "mansurah", "count": 10},
    {"name_ar": "الندى", "name_en": "An Nada", "id": "nada", "count": 8},
    {"name_ar": "اليرموك", "name_en": "Al Yarmuk", "id": "yarmuk", "count": 8},
    {"name_ar": "الملك فيصل", "name_en": "King Faisal", "id": "king-faisal", "count": 8},
    {"name_ar": "النهضة", "name_en": "An Nahdah", "id": "nahdah", "count": 8},
    {"name_ar": "ظهرة لبن", "name_en": "Dhahrat Laban", "id": "dhahrat-laban", "count": 8},
    {"name_ar": "السلي", "name_en": "As Sali", "id": "sali", "count": 8},
    {"name_ar": "الخالدية", "name_en": "Al Khalidiyah", "id": "khalidiyah", "count": 8},
    {"name_ar": "الملك سلمان", "name_en": "King Salman", "id": "king-salman", "count": 6},
    {"name_ar": "الأندلس", "name_en": "Al Andalus", "id": "andalus", "count": 6},
    {"name_ar": "الملك فهد", "name_en": "King Fahd", "id": "king-fahd", "count": 6},
    {"name_ar": "العروبة", "name_en": "Al Urubah", "id": "urubah", "count": 6},
    {"name_ar": "المنار", "name_en": "Al Manar", "id": "manar", "count": 6},
    {"name_ar": "الشهداء", "name_en": "Ash Shuhada", "id": "shuhada", "count": 6},
    {"name_ar": "بدر", "name_en": "Badr", "id": "badr", "count": 6},
    {"name_ar": "الفيحاء", "name_en": "Al Fayha", "id": "fayha", "count": 6},
    {"name_ar": "العود", "name_en": "Al Oud", "id": "oud", "count": 6},
]

# Check for already-existing files and skip duplicates
existing = set()
for f in os.listdir('.'):
    if f.startswith('neighborhood-') and f.endswith('.html') and f != 'neighborhoods.html':
        existing.add(f)

TEMPLATE = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="google-site-verification" content="fsoLYFcBn1bK30V4OvI0U5U78wsZx4LcBG8ADB28QXU" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/svg+xml" href="images/icon-192.svg">
  <title>أفضل أماكن حي {name_ar} في الرياض 2025-2026 | وين نروح</title>
  <meta name="description" content="اكتشف أفضل المطاعم والكافيهات والأماكن الترفيهية في حي {name_ar} بالرياض. تقييمات حقيقية وفلتر متقدم.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://treklaps.github.io/riyadh-places/neighborhood-{page_id}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="أفضل أماكن حي {name_ar} في الرياض | وين نروح بالرياض؟">
  <meta property="og:description" content="اكتشف أفضل الأماكن في حي {name_ar}. مطاعم، كافيهات، ترفيه وأكثر.">
  <meta property="og:url" content="https://treklaps.github.io/riyadh-places/neighborhood-{page_id}.html">
  <meta property="og:locale" content="ar_SA">
  <meta property="og:image" content="https://treklaps.github.io/riyadh-places/images/icon-512.svg">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#0a1628">
  <link rel="preload" href="data/places-light.json" as="fetch" crossorigin>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:'Tajawal',sans-serif;background:#0a1628;color:#e0e0e0;direction:rtl}}
    .header{{background:linear-gradient(135deg,#0a1628 0%,#1a2a4a 100%);padding:12px 20px;position:sticky;top:0;z-index:100}}
    .header-inner{{display:flex;align-items:center;justify-content:space-between;max-width:1400px;margin:auto}}
    .logo{{text-decoration:none;color:#c9a84c;display:flex;align-items:center;gap:8px}}
    .logo h1{{font-size:1.2rem;margin:0}}
  </style>
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/filter-engine.css">
  <link rel="stylesheet" href="css/search-header.css">
</head>
<body>

  <header class="header">
    <div class="header-inner">
      <a href="index.html" class="logo"><span>🏙️</span><h1>وين نروح بالرياض؟</h1></a>
      <button class="dark-mode-toggle" aria-label="الوضع الليلي">🌙</button>
      <button class="menu-toggle" aria-label="القائمة">☰</button>
      <nav class="nav">
        <a href="index.html">الرئيسية</a>
        <a href="cafes.html">كافيهات</a>
        <a href="restaurants.html">مطاعم</a>
        <a href="activities.html">ترفيه</a>
        <a href="events.html">فعاليات</a>
        <a href="new-places.html">جديد</a>
        <a href="discover.html">🎲 اكتشف</a>
        <a href="lists.html">📋 قوائمي</a>
        <div class="nav-dropdown">
          <a href="#">المزيد</a>
          <div class="dropdown-menu">
            <a href="shopping.html">🛍️ تسوق</a>
            <a href="nature.html">🏞️ طبيعة</a>
            <a href="desserts.html">🍰 حلويات</a>
            <a href="top-rated.html">⭐ الأعلى تقييماً</a>
            <div class="dropdown-divider"></div>
            <a href="neighborhoods.html">🏘️ أحياء الرياض</a>
          </div>
        </div>
      </nav>
    </div>
  </header>

  <section class="page-header">
    <h2>🏘️ أفضل أماكن حي {name_ar}</h2>
    <p>اكتشف المطاعم والكافيهات والأماكن الترفيهية في حي {name_ar} بالرياض</p>
  </section>

  <div class="breadcrumb">
    <a href="index.html">الرئيسية</a><span>›</span><a href="neighborhoods.html">الأحياء</a><span>›</span><strong>حي {name_ar}</strong>
  </div>

  <div class="container" style="max-width:1400px;margin:0 auto;padding:0 20px 40px">
    <div id="category-summary"></div>
    <div id="filter-bar"></div>
    <div id="places-grid"></div>
  </div>

  <footer class="footer">
    <div class="footer-inner">
      <div>
        <h3>وين نروح بالرياض؟</h3>
        <p>دليلك الشامل لأفضل الأماكن في الرياض. محدث يومياً.</p>
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
        </ul>
      </div>
      <div>
        <h3>روابط مفيدة</h3>
        <ul>
          <li><a href="sitemap.xml">خريطة الموقع</a></li>
          <li><a href="about.html">عن الموقع</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-heart">صنع بـ <span>❤️</span> في الرياض</div>
    <div class="footer-bottom"><p>© 2025-2026 وين نروح بالرياض؟ جميع الحقوق محفوظة.</p></div>
  </footer>

  <button class="scroll-top" id="scrollTop" aria-label="العودة للأعلى">↑</button>
  <script defer src="js/darkmode.js"></script>
  <script defer src="js/filter-engine.js"></script>
  <script>
    document.querySelectorAll('.nav-dropdown > a').forEach(a => {{
      a.addEventListener('click', (e) => {{
        if (window.innerWidth <= 768) {{ e.preventDefault(); a.parentElement.classList.toggle('open'); }}
      }});
    }});
  </script>
  <script src="js/analytics.js" defer></script>
  <script>
    if('serviceWorker' in navigator){{navigator.serviceWorker.register('sw.js').catch(function(){{}});}}
  </script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      FilterEngine.initNeighborhoodPage({{
        neighborhood: '{filter_name}',
        containerSelector: '#places-grid',
        filterBarSelector: '#filter-bar',
        categorySummarySelector: '#category-summary'
      }});
    }});
  </script>
</body>
</html>'''

generated = 0
skipped = 0
for n in NEEDS_PAGES:
    filename = f"neighborhood-{n['id']}.html"
    
    # Skip if file already exists (like ghirnatah which already has a page)
    if filename in existing:
        print(f"  SKIP (exists): {filename}")
        skipped += 1
        continue
    
    # For the filter, the name used in places.json
    filter_name = n['name_ar']
    
    html = TEMPLATE.format(
        name_ar=n['name_ar'],
        name_en=n['name_en'],
        page_id=n['id'],
        filter_name=filter_name
    )
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    generated += 1

print(f"\nGenerated {generated} new neighborhood pages")
print(f"Skipped {skipped} existing pages")
print(f"Total neighborhood pages: {len(existing) + generated}")
