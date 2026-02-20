# TASK-TRACKER.md — وين نروح بالرياض

*هذا الملف يُقرأ كل heartbeat. كل مهمة لازم تنتهي أو تتوثق.*

---

## 🔴 قيد التنفيذ الآن

| # | المهمة | Agent | بدأت | الحالة |
|---|--------|-------|------|--------|
| 1 | Global Benchmark vs Yelp/TripAdvisor/Zomato | global-benchmark | Feb 20 21:50 | 🔄 running |
| 2 | iOS Fix — 6 CRITICAL compilation issues | ios-fixer | Feb 20 21:50 | 🔄 running |
| 3 | System Architecture Document | system-architect | Feb 20 21:50 | 🔄 running |

---

## ⏳ الطابور (التالي)

| # | المهمة | الأولوية | ملاحظات |
|---|--------|---------|---------|
| 4 | وكيلين متخصصين: بحث + كتابة تقارير | عالي | تركي طلبهم — يُبنون كـ agent templates |
| 5 | Keeta integration بالكامل | متوسط | تحليل موجود، يحتاج دمج بـ delivery-compare |
| 6 | Places batch 3 (طبيعة، شاليهات، متاحف) | متوسط | OSM أضاف بعض، يحتاج enrichment |
| 7 | Google Search Console setup | عالي | ينتظر الدومين |
| 8 | Domain purchase (wain-nrooh.com) | عالي | ينتظر تركي |
| 9 | Mem0 install | منخفض | external memory |
| 10 | LibreTranslate install | منخفض | local offline translation |
| 11 | Fix Ollama nomic-embed-text | متوسط | memory_search معطل |

---

## ✅ مكتمل (اليوم Feb 20)

| المهمة | النتيجة |
|--------|---------|
| Site audit fixes (27 issues) | 0 remaining |
| Data enrichment (3,203→4,022) | +819 places |
| XML Framework applied | 5 cron prompts |
| CI/CD Pattern applied | 3 workflows |
| OSM API integration | scripts/osm-enrichment.py |
| Templates for future projects | templates/PROJECT-FRAMEWORKS.md |
| Daily enrichment cron | 5pm Riyadh |
| CI Loop cron | every 4h |
| MizarVision report | PDF done |
| Saudi satellite protection report | PDF done |
| Saudi role protection report | PDF done |

---

## 📏 القاعدة الجديدة: فصل المهام

**المشروع (وين نروح)** = أولوية أولى، لا يتوقف أبداً
**مهام جانبية** (تقارير، ترجمات، بحث عام) = subagent منفصل، ما يأثر على المشروع

---

*آخر تحديث: 2026-02-20 21:50 UTC*
