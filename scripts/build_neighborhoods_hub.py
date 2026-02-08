#!/usr/bin/env python3
"""Build the neighborhoods.html hub page with all neighborhoods organized by zone."""
import json

DATA_PATH = '/home/ubuntu/.openclaw/workspace/projects/riyadh-places/data/places.json'
OUTPUT_PATH = '/home/ubuntu/.openclaw/workspace/projects/riyadh-places/neighborhoods.html'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    ALL_PLACES = json.load(f)

# All neighborhoods with pages — organized by zone
# (slug, name, hood_names, zone)
ALL_NEIGHBORHOODS = [
    # شمال الرياض
    {'slug': 'malqa', 'name': 'حي الملقا', 'hood_names': ['حي الملقا'], 'zone': 'شمال'},
    {'slug': 'hittin', 'name': 'حي حطين', 'hood_names': ['حي حطين'], 'zone': 'شمال'},
    {'slug': 'yasmin', 'name': 'حي الياسمين', 'hood_names': ['حي الياسمين'], 'zone': 'شمال'},
    {'slug': 'rabee', 'name': 'حي الربيع', 'hood_names': ['حي الربيع'], 'zone': 'شمال'},
    {'slug': 'narjis', 'name': 'حي النرجس', 'hood_names': ['حي النرجس'], 'zone': 'شمال'},
    {'slug': 'sahafa', 'name': 'حي الصحافة', 'hood_names': ['حي الصحافة'], 'zone': 'شمال'},
    {'slug': 'nakheel', 'name': 'حي النخيل', 'hood_names': ['حي النخيل'], 'zone': 'شمال'},
    {'slug': 'muruj', 'name': 'حي المروج', 'hood_names': ['حي المروج'], 'zone': 'شمال'},
    {'slug': 'arid', 'name': 'حي العارض', 'hood_names': ['حي العارض'], 'zone': 'شمال'},
    {'slug': 'malik-fahd', 'name': 'حي الملك فهد', 'hood_names': ['حي الملك فهد'], 'zone': 'شمال'},
    {'slug': 'nafal', 'name': 'حي النفل', 'hood_names': ['حي النفل'], 'zone': 'شمال'},
    {'slug': 'rahmaniyah', 'name': 'حي الرحمانية', 'hood_names': ['حي الرحمانية'], 'zone': 'شمال'},
    {'slug': 'qayrawan', 'name': 'حي القيروان', 'hood_names': ['حي القيروان'], 'zone': 'شمال'},
    {'slug': 'banban', 'name': 'بنبان', 'hood_names': ['بنبان'], 'zone': 'شمال'},
    {'slug': 'thumamah', 'name': 'حي الثمامة', 'hood_names': ['حي الثمامة'], 'zone': 'شمال'},
    
    # وسط الرياض
    {'slug': 'olaya', 'name': 'حي العليا', 'hood_names': ['حي العليا'], 'zone': 'وسط'},
    {'slug': 'kafd', 'name': 'حي الملك عبدالله المالي', 'hood_names': ['حي الملك عبدالله المالي'], 'zone': 'وسط'},
    {'slug': 'wurud', 'name': 'حي الورود', 'hood_names': ['حي الورود'], 'zone': 'وسط'},
    {'slug': 'malz', 'name': 'حي الملز', 'hood_names': ['حي الملز'], 'zone': 'وسط'},
    {'slug': 'sulaymaniyah', 'name': 'حي السليمانية', 'hood_names': ['حي السليمانية'], 'zone': 'وسط'},
    {'slug': 'murabba', 'name': 'حي المربع', 'hood_names': ['حي المربع'], 'zone': 'وسط'},
    {'slug': 'hamra', 'name': 'حي الحمراء', 'hood_names': ['حي الحمراء'], 'zone': 'وسط'},
    {'slug': 'deira', 'name': 'حي الديرة', 'hood_names': ['حي الديرة'], 'zone': 'وسط'},
    {'slug': 'nuzha', 'name': 'حي النزهة', 'hood_names': ['حي النزهة'], 'zone': 'وسط'},
    {'slug': 'maathar', 'name': 'حي المعذر', 'hood_names': ['حي المعذر'], 'zone': 'وسط'},
    {'slug': 'mughrazat', 'name': 'حي المغرزات', 'hood_names': ['حي المغرزات'], 'zone': 'وسط'},
    {'slug': 'rawdah', 'name': 'حي الروضة', 'hood_names': ['حي الروضة'], 'zone': 'وسط'},
    {'slug': 'batha', 'name': 'حي البطحاء', 'hood_names': ['حي البطحاء'], 'zone': 'وسط'},
    {'slug': 'taawun', 'name': 'حي التعاون', 'hood_names': ['حي التعاون'], 'zone': 'وسط'},
    {'slug': 'muaiqiliyah', 'name': 'حي المعيقلية', 'hood_names': ['حي المعيقلية'], 'zone': 'وسط'},
    
    # غرب الرياض
    {'slug': 'diriyah', 'name': 'الدرعية', 'hood_names': ['حي الدرعية'], 'zone': 'غرب'},
    {'slug': 'aqiq', 'name': 'حي العقيق', 'hood_names': ['حي العقيق'], 'zone': 'غرب'},
    {'slug': 'safarat', 'name': 'حي السفارات', 'hood_names': ['حي السفارات'], 'zone': 'غرب'},
    {'slug': 'diplomasi', 'name': 'حي الدبلوماسي', 'hood_names': ['حي الدبلوماسي'], 'zone': 'غرب'},
    {'slug': 'umm-alhamam', 'name': 'حي أم الحمام', 'hood_names': ['حي أم الحمام'], 'zone': 'غرب'},
    
    # شرق الرياض
    {'slug': 'gharnata', 'name': 'غرناطة', 'hood_names': ['حي غرناطة'], 'zone': 'شرق'},
    {'slug': 'ghdir', 'name': 'حي الغدير', 'hood_names': ['حي الغدير'], 'zone': 'شرق'},
    {'slug': 'rimal', 'name': 'حي الرمال', 'hood_names': ['حي الرمال'], 'zone': 'شرق'},
    {'slug': 'naseem', 'name': 'حي النسيم', 'hood_names': ['حي النسيم'], 'zone': 'شرق'},
    {'slug': 'salam', 'name': 'حي السلام', 'hood_names': ['حي السلام'], 'zone': 'شرق'},
    {'slug': 'munsiyah', 'name': 'حي المونسية', 'hood_names': ['حي المونسية'], 'zone': 'شرق'},
    
    # جنوب الرياض
    {'slug': 'rabwa', 'name': 'حي الربوة', 'hood_names': ['حي الربوة'], 'zone': 'جنوب'},
    {'slug': 'suwaidi', 'name': 'حي السويدي', 'hood_names': ['حي السويدي'], 'zone': 'جنوب'},
    {'slug': 'aziziyah', 'name': 'حي العزيزية', 'hood_names': ['حي العزيزية'], 'zone': 'جنوب'},
    {'slug': 'shifa', 'name': 'حي الشفا', 'hood_names': ['حي الشفا'], 'zone': 'جنوب'},
    {'slug': 'namar', 'name': 'نمار', 'hood_names': ['نمار'], 'zone': 'جنوب'},
    {'slug': 'ammariyah', 'name': 'حي العمارية', 'hood_names': ['حي العمارية'], 'zone': 'جنوب'},
    {'slug': 'mansourah', 'name': 'حي المنصورة', 'hood_names': ['حي المنصورة'], 'zone': 'جنوب'},
]

def get_count(hood_names):
    return sum(1 for p in ALL_PLACES if p.get('neighborhood') in hood_names)

def get_avg_rating(hood_names):
    ratings = [p['google_rating'] for p in ALL_PLACES if p.get('neighborhood') in hood_names and p.get('google_rating')]
    return round(sum(ratings) / len(ratings), 1) if ratings else 4.0

def get_top_category(hood_names):
    cats = {}
    cat_icons = {
        'مطعم': '🍽️', 'كافيه': '☕', 'ترفيه': '🎭', 'تسوق': '🛍️',
        'حلويات': '🍰', 'طبيعة': '🏞️', 'فعاليات': '🎪'
    }
    for p in ALL_PLACES:
        if p.get('neighborhood') in hood_names:
            c = p.get('category', '')
            if c:
                cats[c] = cats.get(c, 0) + 1
    if not cats:
        return '📍 متنوع'
    top = max(cats, key=cats.get)
    return f'{cat_icons.get(top, "📍")} {top}'

ZONES = [
    ('🧭 شمال الرياض', 'شمال', 'الأحياء الشمالية تتميز بحداثتها وتخطيطها العصري ونموها السريع. تضم أفضل الكافيهات والمطاعم الجديدة.'),
    ('🏙️ وسط الرياض', 'وسط', 'قلب الرياض التجاري والحيوي. يضم أشهر المعالم والأبراج والمراكز التجارية والأسواق التاريخية.'),
    ('🏔️ غرب الرياض', 'غرب', 'الأحياء الغربية تتميز بقربها من وادي حنيفة والمناطق التاريخية مع مساحات خضراء واسعة.'),
    ('🌅 شرق الرياض', 'شرق', 'شرق الرياض يجمع بين الأحياء السكنية ومراكز التسوق الكبيرة بأسعار مناسبة.'),
    ('🏜️ جنوب الرياض', 'جنوب', 'جنوب الرياض يضم أحياء عائلية متكاملة مع مرافق ترفيهية وطبيعة خلابة.'),
]

# Count totals
total_hoods = len(ALL_NEIGHBORHOODS)
total_places = sum(get_count(n['hood_names']) for n in ALL_NEIGHBORHOODS)

# Build zone sections
zone_html = ''
for zone_title, zone_key, zone_desc in ZONES:
    hoods = [n for n in ALL_NEIGHBORHOODS if n['zone'] == zone_key]
    # Sort by place count desc
    hoods.sort(key=lambda n: get_count(n['hood_names']), reverse=True)
    
    cards = ''
    for n in hoods:
        count = get_count(n['hood_names'])
        avg = get_avg_rating(n['hood_names'])
        top_cat = get_top_category(n['hood_names'])
        cards += f'''
          <a href="neighborhood-{n['slug']}.html" class="neighborhood-card">
            <div class="hood-card-header">
              <h3>{n['name']}</h3>
              <span class="hood-zone-badge">{zone_key}</span>
            </div>
            <div class="hood-card-stats">
              <span class="hood-stat"><strong>{count}</strong> مكان</span>
              <span class="hood-stat">⭐ {avg}</span>
              <span class="hood-stat">{top_cat}</span>
            </div>
          </a>'''
    
    zone_html += f'''
    <div class="zone-section">
      <h2>{zone_title}</h2>
      <p class="zone-desc">{zone_desc}</p>
      <div class="neighborhoods-grid">{cards}
      </div>
    </div>'''

# Build full page
html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="google-site-verification" content="fsoLYFcBn1bK30V4OvI0U5U78wsZx4LcBG8ADB28QXU" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>أحياء الرياض - دليل شامل لأفضل {total_hoods} حي في الرياض 2025-2026 | وين نروح بالرياض؟</title>
  <meta name="description" content="دليل شامل لأفضل {total_hoods} حي في الرياض مع {total_places}+ مكان مميز. اكتشف أحياء شمال وجنوب وشرق وغرب ووسط الرياض مع تقييمات وتوصيات حقيقية.">
  <meta name="keywords" content="أحياء الرياض, أفضل أحياء الرياض, حي العليا, حي الملقا, حي حطين, الدرعية, KAFD, حي السفارات, أحياء شمال الرياض, 2025, 2026">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wain-nrooh.com/neighborhoods.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="أحياء الرياض - دليل شامل لأفضل {total_hoods} حي | وين نروح بالرياض؟">
  <meta property="og:description" content="دليل شامل لأفضل {total_hoods} حي في الرياض مع {total_places}+ مكان مميز. اكتشف أحياء الرياض.">
  <meta property="og:url" content="https://wain-nrooh.com/neighborhoods.html">
  <meta property="og:locale" content="ar_SA">
  <meta property="og:site_name" content="وين نروح بالرياض؟">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .neighborhoods-hub {{ max-width: var(--max-width); margin: 0 auto; padding: 20px; }}
    .zone-section {{ margin-bottom: 40px; }}
    .zone-section h2 {{ font-size: 24px; font-weight: 800; color: var(--primary); margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}
    .zone-section h2::after {{ content: ''; display: block; flex: 1; height: 2px; background: linear-gradient(90deg, var(--gold), transparent); }}
    .zone-desc {{ color: var(--text-light); font-size: 14px; margin-bottom: 18px; line-height: 1.7; }}
    .neighborhoods-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }}
    .neighborhood-card {{ background: var(--card-bg); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); border-top: 3px solid var(--gold); transition: var(--transition); cursor: pointer; text-decoration: none; color: inherit; }}
    .neighborhood-card:hover {{ transform: translateY(-5px); box-shadow: var(--shadow-gold); }}
    .hood-card-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }}
    .hood-card-header h3 {{ font-size: 18px; font-weight: 700; color: var(--primary); }}
    .hood-zone-badge {{ background: rgba(10,22,40,0.06); color: var(--text-light); padding: 3px 10px; border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; }}
    .hood-card-stats {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    .hood-stat {{ font-size: 13px; color: var(--text-light); font-weight: 500; }}
    .hood-stat strong {{ color: var(--primary); font-weight: 800; }}
    .hub-stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 18px; position: relative; }}
    .hub-stats .stat {{ display: flex; flex-direction: column; align-items: center; gap: 2px; }}
    .hub-stats .stat-number {{ font-size: 28px; font-weight: 900; color: var(--gold); }}
    .hub-stats .stat-label {{ font-size: 12px; color: rgba(255,255,255,0.6); }}
    @media (max-width: 768px) {{
      .neighborhoods-grid {{ grid-template-columns: 1fr; }}
      .hub-stats {{ gap: 16px; }}
      .hub-stats .stat-number {{ font-size: 22px; }}
    }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "أحياء الرياض",
    "description": "دليل شامل لأفضل {total_hoods} حي في الرياض مع أماكنها المميزة",
    "url": "https://wain-nrooh.com/neighborhoods.html",
    "inLanguage": "ar",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "وين نروح بالرياض؟",
      "url": "https://wain-nrooh.com/"
    }}
  }}
  </script>
</head>
<body>

  <header class="header">
    <div class="header-inner">
      <a href="index.html" class="logo"><span>🏙️</span><h1>وين نروح بالرياض؟</h1></a>
      <button class="menu-toggle" aria-label="القائمة">☰</button>
      <nav class="nav">
        <a href="index.html">الرئيسية</a>
        <a href="cafes.html">كافيهات</a>
        <a href="restaurants.html">مطاعم</a>
        <a href="activities.html">ترفيه</a>
        <a href="events.html">فعاليات</a>
        <a href="new-places.html">جديد</a>
        <div class="nav-dropdown">
          <a href="#">المزيد</a>
          <div class="dropdown-menu">
            <a href="shopping.html">🛍️ تسوق</a>
            <a href="nature.html">🏞️ طبيعة</a>
            <a href="desserts.html">🍰 حلويات</a>
            <a href="top-rated.html">⭐ الأعلى تقييماً</a>
            <div class="dropdown-divider"></div>
            <a href="neighborhoods.html" class="active">🏘️ أحياء الرياض</a>
            <a href="foundation-day.html">🇸🇦 يوم التأسيس</a>
            <a href="riyadh-season.html">✨ موسم الرياض</a>
          </div>
        </div>
      </nav>
    </div>
  </header>

  <section class="neighborhood-header">
    <h2>🏘️ أحياء <span>الرياض</span></h2>
    <p>دليل شامل لأفضل {total_hoods} حي في الرياض. اكتشف أماكن كل حي من كافيهات ومطاعم وترفيه وتسوق مع تقييمات قوقل الحقيقية. اختر الحي اللي يناسبك!</p>
    <div class="hub-stats">
      <div class="stat">
        <span class="stat-number">{total_hoods}</span>
        <span class="stat-label">حي</span>
      </div>
      <div class="stat">
        <span class="stat-number">{total_places}</span>
        <span class="stat-label">مكان</span>
      </div>
      <div class="stat">
        <span class="stat-number">5</span>
        <span class="stat-label">مناطق</span>
      </div>
    </div>
  </section>

  <div class="breadcrumb">
    <a href="index.html">الرئيسية</a><span>›</span><strong>أحياء الرياض</strong>
  </div>

  <div class="neighborhoods-hub">
    {zone_html}
  </div>

  <!-- مقال SEO -->
  <div class="seo-article">
    <div class="article-content">
      <h2>دليل أحياء الرياض الشامل 2025-2026</h2>
      <p>الرياض مدينة مترامية الأطراف تتكون من عشرات الأحياء المتنوعة، كل حي له طابعه وشخصيته الخاصة. من الأحياء التاريخية العريقة مثل الملز والسليمانية والديرة إلى الأحياء العصرية مثل KAFD وحي العليا، ومن المناطق التراثية مثل الدرعية إلى الأحياء السكنية الراقية في شمال الرياض — هذا الدليل يساعدك على اختيار الحي المناسب لزيارتك.</p>
      
      <h3>شمال الرياض ({len([n for n in ALL_NEIGHBORHOODS if n['zone'] == 'شمال'])} حي)</h3>
      <p>الأحياء الشمالية هي الأكثر نمواً وتطوراً في الرياض حالياً. حي الملقا وحي حطين وحي الياسمين وحي الربيع تُعد من أفضل الأحياء السكنية مع تركز كبير للكافيهات والمطاعم الحديثة. حي الصحافة يُعرف كعاصمة القهوة المختصة، بينما حي النرجس والعارض والقيروان يمثلون الجيل الجديد من الأحياء الناشئة. حي الملك فهد والنفل والرحمانية يقدمون فخامة سكنية مع خدمات متكاملة.</p>
      
      <h3>وسط الرياض ({len([n for n in ALL_NEIGHBORHOODS if n['zone'] == 'وسط'])} حي)</h3>
      <p>وسط الرياض يجمع بين التاريخ والحداثة. حي العليا هو القلب التجاري بأبراج المملكة والفيصلية. مركز الملك عبدالله المالي (KAFD) يمثل مستقبل الرياض بناطحات السحاب والمطاعم العالمية. حي المربع والديرة والبطحاء والمعيقلية تحتفظ بعبق التاريخ والأسواق الشعبية. حي الورود والسليمانية والحمراء والنزهة والمغرزات يقدمون أجواء أصيلة ومتنوعة.</p>
      
      <h3>غرب الرياض ({len([n for n in ALL_NEIGHBORHOODS if n['zone'] == 'غرب'])} حي)</h3>
      <p>الدرعية في غرب الرياض تقدم تجربة تاريخية وثقافية لا مثيل لها مع البجيري وجاكس. حي السفارات والحي الدبلوماسي يُعدان من أرقى الأحياء بمساحاتهم الخضراء ومطاعمهم الفاخرة. حي العقيق وأم الحمام يوفران خيارات متنوعة مع قرب من وادي حنيفة.</p>
      
      <h3>شرق الرياض ({len([n for n in ALL_NEIGHBORHOODS if n['zone'] == 'شرق'])} حي)</h3>
      <p>شرق الرياض يضم أحياء سكنية كبيرة مع مراكز تسوق متنوعة بأسعار مناسبة. غرناطة والغدير والرمال والنسيم والسلام والمونسية تقدم تجربة معيشية متكاملة مع خيارات تسوق ومطاعم متنوعة.</p>

      <h3>جنوب الرياض ({len([n for n in ALL_NEIGHBORHOODS if n['zone'] == 'جنوب'])} حي)</h3>
      <p>جنوب الرياض يتميز بطابعه العائلي والطبيعة الخلابة. حي الربوة وجهة ترفيهية عائلية، والسويدي يقدم قرباً من وادي حنيفة. نمار بشلالاتها الموسمية والعزيزية والشفا بأحيائهم السكنية الواسعة يوفرون خيارات متنوعة بأسعار مناسبة.</p>
    </div>
  </div>

  <footer class="footer">
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
          <li><a href="new-places.html">أماكن جديدة</a></li>
        </ul>
      </div>
      <div>
        <h3>الأحياء</h3>
        <ul>
          <li><a href="neighborhoods.html">كل أحياء الرياض</a></li>
          <li><a href="neighborhood-olaya.html">حي العليا</a></li>
          <li><a href="neighborhood-malqa.html">حي الملقا</a></li>
          <li><a href="neighborhood-hittin.html">حي حطين</a></li>
          <li><a href="neighborhood-diriyah.html">الدرعية</a></li>
          <li><a href="neighborhood-kafd.html">KAFD</a></li>
          <li><a href="neighborhood-safarat.html">حي السفارات</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-heart">صنع بـ <span>❤️</span> في الرياض</div>
    <div class="footer-bottom"><p>© 2025-2026 وين نروح بالرياض؟ جميع الحقوق محفوظة.</p></div>
  </footer>

  <button class="scroll-top" id="scrollTop" aria-label="العودة للأعلى">↑</button>

  <script src="js/main.js"></script>
  <script>
    document.querySelectorAll('.nav-dropdown > a').forEach(a => {{
      a.addEventListener('click', (e) => {{
        if (window.innerWidth <= 768) {{
          e.preventDefault();
          a.parentElement.classList.toggle('open');
        }}
      }});
    }});
  </script>
  <script src="js/analytics.js"></script>
</body>
</html>'''

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Updated neighborhoods.html with {total_hoods} neighborhoods, {total_places} total places")
