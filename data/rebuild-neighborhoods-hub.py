#!/usr/bin/env python3
"""Rebuild the neighborhoods.html hub page with all 166 neighborhoods."""
import json
import os
import re

# Load complete neighborhoods
neighborhoods = json.load(open('data/neighborhoods-complete.json'))

# Map page IDs for neighborhoods that have pages
# Build a dict of existing page files
existing_pages = {}
for f in os.listdir('.'):
    if f.startswith('neighborhood-') and f.endswith('.html') and f != 'neighborhoods.html':
        existing_pages[f] = True

# Map: neighborhood name_ar -> page filename
# We need to find which page file corresponds to which neighborhood
PAGE_MAP = {
    "الربيع": "neighborhood-rabee.html",
    "الندى": "neighborhood-nada.html",
    "الصحافة": "neighborhood-sahafa.html",
    "النرجس": "neighborhood-narjis.html",
    "العارض": "neighborhood-arid.html",
    "النفل": "neighborhood-nafal.html",
    "العقيق": "neighborhood-aqiq.html",
    "الوادي": "neighborhood-wadi.html",
    "الغدير": "neighborhood-ghdir.html",
    "الياسمين": "neighborhood-yasmin.html",
    "الفلاح": "neighborhood-falah.html",
    "بنبان": "neighborhood-banban.html",
    "القيروان": "neighborhood-qayrawan.html",
    "حطين": "neighborhood-hittin.html",
    "الملقا": "neighborhood-malqa.html",
    "الملك سلمان": "neighborhood-king-salman.html",
    "الريم": "neighborhood-al-reem.html",
    "الروضة": "neighborhood-rawdah.html",
    "الرمال": "neighborhood-rimal.html",
    "المونسية": "neighborhood-munsiyah.html",
    "قرطبة": "neighborhood-qurtubah.html",
    "الجنادرية": "neighborhood-janadriyah.html",
    "القادسية": "neighborhood-al-qadisiyah.html",
    "اليرموك": "neighborhood-yarmuk.html",
    "غرناطة": "neighborhood-gharnata.html",
    "إشبيلية": "neighborhood-ishbiliyah.html",
    "الحمراء": "neighborhood-hamra.html",
    "الخليج": "neighborhood-khaleej.html",
    "الملك فيصل": "neighborhood-king-faisal.html",
    "القدس": "neighborhood-quds.html",
    "النهضة": "neighborhood-nahdah.html",
    "الأندلس": "neighborhood-andalus.html",
    "العليا": "neighborhood-olaya.html",
    "السليمانية": "neighborhood-sulaymaniyah.html",
    "الورود": "neighborhood-wurud.html",
    "الملك فهد": "neighborhood-king-fahd.html",
    "المرسلات": "neighborhood-al-mursalat.html",
    "النزهة": "neighborhood-nuzha.html",
    "المغرزات": "neighborhood-mughrazat.html",
    "المروج": "neighborhood-muruj.html",
    "المصيف": "neighborhood-al-masif.html",
    "التعاون": "neighborhood-taawun.html",
    "كافد": "neighborhood-kafd.html",
    "العروبة": "neighborhood-urubah.html",
    "المعذر": "neighborhood-maathar.html",
    "المعذر الشمالي": "neighborhood-al-maathar-north.html",
    "المحمدية": "neighborhood-muhammadiyah.html",
    "الرحمانية": "neighborhood-rahmaniyah.html",
    "الرائد": "neighborhood-raid.html",
    "النخيل": "neighborhood-nakheel.html",
    "أم الحمام الشرقي": "neighborhood-umm-alhamam.html",
    "السفارات": "neighborhood-safarat.html",
    "عرقة": "neighborhood-irqah.html",
    "ظهرة لبن": "neighborhood-dhahrat-laban.html",
    "الخزامى": "neighborhood-al-khuzama.html",
    "الحي الدبلوماسي": "neighborhood-diplomasi.html",
    "النسيم الشرقي": "neighborhood-al-naseem-east.html",
    "النسيم الغربي": "neighborhood-naseem.html",
    "السلام": "neighborhood-salam.html",
    "الروابي": "neighborhood-rawabi.html",
    "النظيم": "neighborhood-nadheem.html",
    "المنار": "neighborhood-manar.html",
    "الندوة": "neighborhood-al-nadwa.html",
    "الشهداء": "neighborhood-shuhada.html",
    "الملز": "neighborhood-malz.html",
    "الربوة": "neighborhood-rabwa.html",
    "المربع": "neighborhood-murabba.html",
    "الديرة": "neighborhood-deira.html",
    "البديعة": "neighborhood-badiah.html",
    "الشميسي": "neighborhood-shumaisi.html",
    "السويدي": "neighborhood-suwaidi.html",
    "العريجاء": "neighborhood-uraija.html",
    "شبرا": "neighborhood-al-shubra.html",
    "ظهرة نمار": "neighborhood-namar.html",
    "نمار": "neighborhood-namar.html",
    "الشفاء": "neighborhood-shifa.html",
    "الشفا": "neighborhood-shifa.html",
    "بدر": "neighborhood-badr.html",
    "المنصورة": "neighborhood-mansourah.html",
    "العزيزية": "neighborhood-aziziyah.html",
    "السلي": "neighborhood-sali.html",
    "الفيحاء": "neighborhood-fayha.html",
    "الخالدية": "neighborhood-khalidiyah.html",
    "العود": "neighborhood-oud.html",
    "منفوحة": "neighborhood-manfuhah.html",
    "الدرعية": "neighborhood-diriyah.html",
    "الثمامة": "neighborhood-thumamah.html",
    "جاكس": "neighborhood-jax.html",
    "البجيري": "neighborhood-al-bujairi.html",
    "الفلاح": "neighborhood-falah.html",
}

# Zone mapping for display
ZONE_MAP = {
    "شمال الرياض": {"emoji": "🧭", "label": "شمال الرياض", "badge": "شمال", "desc": "الأحياء الشمالية تتميز بحداثتها وتخطيطها العصري ونموها السريع. تضم أفضل الكافيهات والمطاعم الجديدة."},
    "وسط الرياض": {"emoji": "🏙️", "label": "وسط الرياض", "badge": "وسط", "desc": "قلب الرياض التجاري والحيوي. يضم أشهر المعالم والأبراج والمراكز التجارية والأسواق التاريخية."},
    "شرق الرياض": {"emoji": "🌅", "label": "شرق الرياض", "badge": "شرق", "desc": "الأحياء الشرقية تتميز بالتنوع والمساحات الواسعة والأسواق الشعبية والمراكز التجارية."},
    "غرب الرياض": {"emoji": "🌿", "label": "غرب الرياض", "badge": "غرب", "desc": "أحياء راقية تضم الحي الدبلوماسي ووادي حنيفة والدرعية التاريخية."},
    "جنوب الرياض": {"emoji": "🏠", "label": "جنوب الرياض", "badge": "جنوب", "desc": "أحياء سكنية تاريخية وجديدة مع خدمات متنوعة وأسعار معقولة."},
    "جنوب غرب الرياض": {"emoji": "🏡", "label": "جنوب غرب الرياض", "badge": "جنوب غرب", "desc": "أحياء سكنية متنوعة تشهد تطوراً عمرانياً مع مرافق خدمية حديثة."},
    "جنوب شرق الرياض": {"emoji": "🏗️", "label": "جنوب شرق الرياض", "badge": "جنوب شرق", "desc": "أحياء سكنية وصناعية مع خدمات أساسية متنوعة."},
    "شمال غرب الرياض": {"emoji": "🏛️", "label": "شمال غرب الرياض (الدرعية)", "badge": "درعية", "desc": "منطقة الدرعية التاريخية - عاصمة الدولة السعودية الأولى. مشاريع سياحية ضخمة ومطاعم عالمية."},
}

# Zone display order
ZONE_ORDER = ["شمال الرياض", "وسط الرياض", "شرق الرياض", "غرب الرياض", "شمال غرب الرياض", "جنوب الرياض", "جنوب غرب الرياض", "جنوب شرق الرياض"]

# Group neighborhoods by zone
zones = {}
for n in neighborhoods:
    d = n['district']
    if d not in zones:
        zones[d] = []
    zones[d].append(n)

# Sort each zone by place count descending
for d in zones:
    zones[d].sort(key=lambda x: -x['place_count'])

# Generate neighborhood cards HTML
def make_card(n):
    name = n['name_ar']
    page = PAGE_MAP.get(name, '')
    if not page or page not in existing_pages:
        # No page exists - make it a non-link card
        zone_info = ZONE_MAP.get(n['district'], {"badge": n['district'][:4]})
        badge = zone_info.get('badge', '')
        count = n['place_count']
        return f'''          <div class="neighborhood-card no-link">
            <div class="hood-card-header">
              <h3>حي {name}</h3>
              <span class="hood-zone-badge">{badge}</span>
            </div>
            <div class="hood-card-stats">
              <span class="hood-stat"><strong>{count}</strong> مكان</span>
              <span class="hood-stat">{n['character']}</span>
            </div>
          </div>'''
    
    zone_info = ZONE_MAP.get(n['district'], {"badge": n['district'][:4]})
    badge = zone_info.get('badge', '')
    count = n['place_count']
    
    return f'''          <a href="{page}" class="neighborhood-card">
            <div class="hood-card-header">
              <h3>حي {name}</h3>
              <span class="hood-zone-badge">{badge}</span>
            </div>
            <div class="hood-card-stats">
              <span class="hood-stat"><strong>{count}</strong> مكان</span>
              <span class="hood-stat">{n['character']}</span>
            </div>
          </a>'''

# Build the zones HTML
zones_html = ""
for zone_name in ZONE_ORDER:
    if zone_name not in zones:
        continue
    zone_info = ZONE_MAP.get(zone_name, {"emoji": "📍", "label": zone_name, "desc": ""})
    cards = "\n".join(make_card(n) for n in zones[zone_name])
    count = len(zones[zone_name])
    zones_html += f'''
    <div class="zone-section">
      <h2>{zone_info["emoji"]} {zone_info["label"]} <small>({count} حي)</small></h2>
      <p class="zone-desc">{zone_info["desc"]}</p>
      <div class="neighborhoods-grid">
{cards}
      </div>
    </div>
'''

# Read existing file
with open('neighborhoods.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the neighborhoods-hub div content
# Pattern: from <div class="neighborhoods-hub"> to its closing </div> before the footer
start_marker = '<div class="neighborhoods-hub">'
end_marker = '<!-- end neighborhoods-hub -->'

# If end marker doesn't exist, find it by the footer
if end_marker not in content:
    # Find the footer
    footer_pos = content.find('<footer class="footer">')
    if footer_pos == -1:
        print("ERROR: Cannot find footer marker")
        exit(1)
    # Find the last </div> before footer that closes neighborhoods-hub
    hub_start = content.find(start_marker)
    if hub_start == -1:
        print("ERROR: Cannot find neighborhoods-hub start")
        exit(1)
    
    # Replace everything between hub start and footer
    before = content[:hub_start]
    after = content[footer_pos:]
    
    new_content = before + f'''<div class="neighborhoods-hub">
{zones_html}
  </div>
  <!-- end neighborhoods-hub -->

  ''' + after
else:
    hub_start = content.find(start_marker)
    hub_end = content.find(end_marker) + len(end_marker)
    before = content[:hub_start]
    after = content[hub_end:]
    new_content = before + f'''<div class="neighborhoods-hub">
{zones_html}
  </div>
  <!-- end neighborhoods-hub -->''' + after

with open('neighborhoods.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

total_with_pages = sum(1 for n in neighborhoods if PAGE_MAP.get(n['name_ar'], '') in existing_pages)
print(f"Updated neighborhoods.html hub page")
print(f"Total neighborhoods displayed: {len(neighborhoods)}")
print(f"Neighborhoods with clickable pages: {total_with_pages}")
print(f"Zones: {len([z for z in ZONE_ORDER if z in zones])}")
for z in ZONE_ORDER:
    if z in zones:
        print(f"  {z}: {len(zones[z])} neighborhoods")
