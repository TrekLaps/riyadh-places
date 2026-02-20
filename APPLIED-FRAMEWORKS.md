# Applied Frameworks — وين نروح بالرياض

*تتبع تطبيق المقالات والمعارف المسجلة*

---

## 1. XML Prompt Engineering Framework ✅
**المصدر:** مقال @kloss_xyz (Feb 4)
**الحالة:** 🔄 قيد التطبيق (xml-framework-apply agent)

| الجانب | قبل | بعد |
|--------|------|------|
| Agent prompts | Plain text | XML tags: role, mission, rules, constraints, output_format |
| Cron job prompts | عام وغامض | محدد مع anti_patterns و examples |
| Subagent tasks | نص عادي | XML structured مع method |

---

## 2. Agent Economics / Unbrowse ✅
**المصدر:** Unbrowse + x402 article (Feb 4)
**الحالة:** ✅ مطبّق جزئياً

| الجانب | قبل | بعد |
|--------|------|------|
| Data sourcing | web_search + curl فقط | OpenStreetMap API (1,279 مكان) + web_search |
| API access | يدوي | سكربت `scripts/osm-enrichment.py` |
| Daily enrichment | web search بس | OSM API + web search + social media |
| x402 marketplace | غير مثبت | TODO — ننتظر use case |

**APIs المتاحة بدون auth:**
- ✅ OpenStreetMap Overpass API — 1,279 مكان بالرياض (مطاعم، كافيهات، فنادق، مولات، متاحف)
- ✅ Nominatim — geocoding
- ❌ Google Maps — يحتاج API key
- ❌ TripAdvisor — يحتاج auth + يحجب headless
- ❌ Foursquare — يحتاج API key
- ❌ HungerStation/Jahez — يحتاج auth

---

## 3. CI/CD Review Agent Pattern ✅
**المصدر:** مقال من تركي (Feb 19)
**الحالة:** 🔄 قيد الترقية (ci-pattern-upgrade agent)

| الجانب | قبل | بعد |
|--------|------|------|
| risk-policy-gate.yml | Basic validation | SHA-locked + remediation |
| Auto-remediate | غير موجود | auto-remediate.yml جديد |
| CI Loop | غير موجود | cron كل 4 ساعات يفحص ويصلح |
| Browser evidence | غير موجود | HTTP health checks |

---

## 4. Data Licensing (Jan 31) ✅
**مطبّق:** ما استخدمنا أي API مدفوع بدون ترخيص

## 5. 24/7 Speed Directive (Feb 19) ✅
**مطبّق:** Parallel agents + daily crons

## 6. Tool Call Discipline (Feb 4) ⚠️
**مطبّق جزئياً:** محتاج مراقبة مستمرة

---

*آخر تحديث: 2026-02-20*
