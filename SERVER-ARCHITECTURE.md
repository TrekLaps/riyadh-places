# 🏗️ SERVER-ARCHITECTURE.md
# وين نروح بالرياض — خطة السيرفر الكاملة

> **الحالة:** مشروع startup — الأولوية: سرعة + أمان + تكلفة منخفضة
> **التاريخ:** 2026-02-20
> **المؤلف:** Backend/Infrastructure Architect

---

## 📋 جدول المحتويات

1. [البنية التحتية (Infrastructure)](#1-البنية-التحتية-infrastructure)
2. [Tech Stack](#2-tech-stack)
3. [API Design](#3-api-design)
4. [Data Layer](#4-data-layer)
5. [ربط iOS App](#5-ربط-ios-app)
6. [ربط الموقع](#6-ربط-الموقع)
7. [AI Integration](#7-ai-integration)
8. [Scraping & Data Pipeline](#8-scraping--data-pipeline)
9. [Security](#9-security)
10. [DevOps](#10-devops)
11. [التكاليف](#11-التكاليف)
12. [Timeline](#12-timeline)

---

## الوضع الحالي

```
┌─────────────────────────────────────────────────┐
│              GitHub Pages (Static)               │
│                                                  │
│  ┌──────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ 87 HTML  │  │ places.json  │  │ CSS + JS  │  │
│  │  pages   │  │  3,202 مكان  │  │  assets   │  │
│  │          │  │    2.8MB     │  │           │  │
│  └──────────┘  └──────────────┘  └───────────┘  │
│                                                  │
│  ┌──────────────────┐  ┌──────────────────────┐  │
│  │ delivery-prices  │  │ prices-initial.json  │  │
│  │     .json        │  │ prices-batch2.json   │  │
│  │  6 تطبيقات       │  │   أسعار المنيو       │  │
│  └──────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────┘
        │
        ▼
   المستخدم يحمّل كل شي client-side
   (بطيء مع 2.8MB JSON)
```

**المشاكل الحالية:**
- المستخدم يحمّل 2.8MB+ عند كل زيارة
- لا يوجد بحث سيرفر — كل شي client-side
- لا يوجد authentication أو user accounts
- تحديث البيانات يدوي (تعديل JSON files)
- لا يوجد analytics أو tracking
- لا يمكن ربط iOS app بدون API

---

## 1. البنية التحتية (Infrastructure)

### مقارنة Cloud Providers

| المعيار | Supabase | Railway | Vercel + PlanetScale | AWS (Lightsail) | Fly.io |
|---------|----------|---------|---------------------|-----------------|--------|
| **Free tier** | ✅ سخي جداً | ✅ $5 credits | ✅ Hobby free | ❌ $3.50/mo min | ✅ 3 VMs free |
| **PostgreSQL** | ✅ مدمج + PostGIS | ✅ plugin | ❌ MySQL only | ✅ يدوي | ✅ يدوي |
| **Auth مدمج** | ✅ GoTrue | ❌ | ❌ | ❌ | ❌ |
| **Storage مدمج** | ✅ S3-compatible | ❌ | ❌ Blob storage | ✅ S3 | ❌ |
| **Edge Functions** | ✅ Deno | ❌ | ✅ Serverless | ❌ Lambda | ❌ |
| **Realtime** | ✅ WebSocket مدمج | ❌ | ❌ | ❌ | ❌ |
| **سهولة الإعداد** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **تكلفة MVP** | $0 | $5/mo | $0 | $7/mo | $0 |
| **تكلفة Growth** | $25/mo | $20/mo | $40/mo | $30/mo | $20/mo |
| **تكلفة Scale** | $75/mo | $50+/mo | $100+/mo | $50+/mo | $40+/mo |
| **منطقة الشرق الأوسط** | ❌ (أقرب: EU) | ❌ (US/EU) | ✅ Edge global | ✅ Bahrain | ❌ (أقرب: India) |
| **PDPL compliance** | ⚠️ يحتاج مراجعة | ⚠️ | ⚠️ | ✅ البحرين | ⚠️ |

### 🏆 التوصية النهائية: Supabase (Primary) + Cloudflare (Edge/CDN)

**لماذا Supabase:**

1. **Free tier سخي:** 500MB database, 1GB storage, 2GB bandwidth, 50K auth users
2. **PostgreSQL + PostGIS مدمج:** البحث الجغرافي جاهز بدون setup
3. **Auth مدمج:** JWT + OAuth + Magic Link — لا نحتاج نبني authentication
4. **Realtime مدمج:** WebSocket subscriptions بدون setup
5. **Storage مدمج:** لرفع صور الأماكن
6. **Row Level Security:** أمان على مستوى الصف — مهم جداً
7. **Auto-generated API:** REST + GraphQL تلقائي من schema
8. **Edge Functions:** لـ custom logic (Deno/TypeScript)
9. **Dashboard ممتاز:** إدارة بدون SQL
10. **Client SDKs:** JavaScript + Swift جاهزين

**لماذا Cloudflare كـ Edge Layer:**

1. **Free tier سخي:** CDN + Workers (100K requests/day)
2. **R2 Storage:** S3-compatible بدون egress fees — $0 للصور
3. **Workers:** Edge compute في كل مكان (بما فيها الشرق الأوسط)
4. **KV Storage:** Cache سريع جداً
5. **الأسعار:** أرخص من أي بديل للـ bandwidth

### خطة التدرج

```
Phase 1: MVP ($0/mo)                    Phase 2: Growth ($25-40/mo)
┌─────────────────────┐                ┌─────────────────────────┐
│ Supabase Free       │                │ Supabase Pro ($25)      │
│ ├─ PostgreSQL 500MB │    ────►       │ ├─ PostgreSQL 8GB       │
│ ├─ Auth (50K users) │                │ ├─ Auth (100K users)    │
│ ├─ Storage 1GB      │                │ ├─ Storage 100GB        │
│ ├─ Edge Functions   │                │ ├─ Daily backups        │
│ └─ Realtime         │                │ └─ Email support        │
│                     │                │                         │
│ Cloudflare Free     │                │ Cloudflare Pro ($20)    │
│ ├─ CDN              │    ────►       │ ├─ CDN + WAF            │
│ ├─ R2 (10GB free)   │                │ ├─ R2 (paid tier)       │
│ ├─ Workers (100K/d) │                │ ├─ Workers (10M/mo)     │
│ └─ KV Store         │                │ └─ Analytics            │
└─────────────────────┘                └─────────────────────────┘

Phase 3: Scale ($75-150/mo)
┌──────────────────────────────┐
│ Supabase Pro + Addons ($75+) │
│ ├─ PostgreSQL 16GB+          │
│ ├─ Read replicas             │
│ ├─ Point-in-time recovery    │
│ ├─ SOC2 compliance           │
│ └─ Priority support          │
│                              │
│ Cloudflare Business ($50+)   │
│ ├─ CDN + Advanced WAF        │
│ ├─ R2 + Durable Objects      │
│ ├─ Workers Paid              │
│ └─ Advanced Analytics        │
│                              │
│ + Meilisearch Cloud ($30)    │
│ + Upstash Redis ($10)        │
└──────────────────────────────┘
```

### البنية المستهدفة (Target Architecture)

```
                         ┌─────────────┐
                         │  Cloudflare  │
                         │     CDN      │
                         │  + WAF       │
                         └──────┬───────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
              ┌─────▼─────┐ ┌──▼──┐  ┌─────▼──────┐
              │ Cloudflare │ │ R2  │  │ Cloudflare  │
              │  Workers   │ │Store│  │    KV       │
              │ (Edge API) │ │(img)│  │  (Cache)    │
              └─────┬──────┘ └─────┘  └────────────┘
                    │
                    │ (proxy to origin)
                    │
         ┌──────────▼──────────┐
         │      Supabase       │
         │                     │
         │  ┌───────────────┐  │
         │  │  PostgreSQL   │  │
         │  │  + PostGIS    │  │
         │  └───────────────┘  │
         │                     │
         │  ┌───────────────┐  │
         │  │  Auth (JWT)   │  │
         │  └───────────────┘  │
         │                     │
         │  ┌───────────────┐  │
         │  │Edge Functions │  │
         │  │   (Deno)      │  │
         │  └───────────────┘  │
         │                     │
         │  ┌───────────────┐  │
         │  │   Realtime    │  │
         │  │  (WebSocket)  │  │
         │  └───────────────┘  │
         └─────────────────────┘
                    │
         ┌──────────▼──────────┐
         │   External Services  │
         │                     │
         │  ┌───────────────┐  │
         │  │ Meilisearch   │  │   (Phase 2+)
         │  │ Cloud         │  │
         │  └───────────────┘  │
         │                     │
         │  ┌───────────────┐  │
         │  │  Upstash      │  │   (Phase 2+)
         │  │  Redis        │  │
         │  └───────────────┘  │
         │                     │
         │  ┌───────────────┐  │
         │  │  OpenAI /     │  │   (Phase 2+)
         │  │  Embeddings   │  │
         │  └───────────────┘  │
         └─────────────────────┘

Clients:
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Website │  │ iOS App  │  │  Admin   │
│  (SSG)   │  │ (Swift)  │  │  Panel   │
└──────────┘  └──────────┘  └──────────┘
```

---

## 2. Tech Stack

### Backend Framework: Supabase Edge Functions (Deno/TypeScript)

**لماذا Edge Functions بدل backend تقليدي:**

| المعيار | Edge Functions | Node.js (Express) | FastAPI (Python) | Go (Fiber) |
|---------|---------------|-------------------|-----------------|------------|
| **Cold start** | ~50ms | ~200ms | ~500ms | ~100ms |
| **Setup** | 0 — مدمج مع Supabase | يحتاج server | يحتاج server | يحتاج server |
| **TypeScript** | ✅ native | ✅ | ❌ Python | ❌ Go |
| **Auto-scaling** | ✅ | ❌ يدوي | ❌ يدوي | ❌ يدوي |
| **التكلفة** | $0 (500K/mo) | $5-20/mo | $5-20/mo | $5-20/mo |
| **DB access** | مباشر (same infra) | network hop | network hop | network hop |

**القرار:** نستخدم **3 طبقات**:

1. **Supabase Auto API:** للـ CRUD البسيط (places, reviews, users) — $0 بدون كود
2. **Edge Functions:** للـ business logic المعقد (search, recommendations, scraping)
3. **Cloudflare Workers:** للـ edge caching + image optimization + rate limiting

```
Request Flow:
                                                     
  Client ──► Cloudflare Worker ──► Supabase API ──► PostgreSQL
                   │                    │
                   ├─ Cache hit? ◄──────┘
                   │   Return cached
                   │
                   └─ Cache miss?
                       Forward to Supabase
                       Cache response in KV
```

### قاعدة البيانات: PostgreSQL + PostGIS (via Supabase)

**لماذا PostgreSQL + PostGIS:**

1. **PostGIS:** أقوى extension للبيانات الجغرافية
   - `ST_DWithin()` — البحث ضمن نطاق
   - `ST_Distance()` — حساب المسافة
   - Spatial indexing — بحث جغرافي سريع O(log n)
2. **Full-text search بالعربي:** PostgreSQL يدعم Arabic stemming
3. **JSONB:** لتخزين بيانات مرنة (ساعات العمل، features)
4. **Row Level Security:** أمان على مستوى الصف
5. **Supabase مدمج:** لا يحتاج setup

### Cache Layer: Cloudflare KV (MVP) → Upstash Redis (Growth)

**MVP — Cloudflare KV:**
- مجاني 100K reads/day
- Edge caching — أقرب نقطة للمستخدم
- Perfect لـ read-heavy workload (وهذا بالضبط استخدامنا)
- TTL-based invalidation

**Growth — Upstash Redis:**
- $0.2/100K commands (serverless)
- لما نحتاج: session management, rate limiting, real-time leaderboards
- الاتصال عبر HTTP (لا يحتاج persistent connection)

```
Cache Strategy (MVP):

  GET /api/places?category=cafe&area=olaya
       │
       ▼
  Cloudflare Worker
       │
       ├─ Check KV cache (key: "places:cafe:olaya")
       │   ├─ HIT (TTL < 1hr) → Return cached (< 5ms)
       │   └─ MISS → Forward to Supabase
       │              │
       │              ▼
       │         Query PostgreSQL
       │              │
       │              ▼
       │         Store in KV (TTL: 1hr)
       │              │
       │              ▼
       └──────── Return response
```

### Search Engine: PostgreSQL FTS (MVP) → Meilisearch (Growth)

**MVP — PostgreSQL Full-Text Search:**
- مجاني (مدمج)
- يدعم العربي مع `arabic` dictionary
- `tsvector` + `tsquery` مع GIN index
- كافي لـ 3,202 مكان (dataset صغير)

**Growth — Meilisearch Cloud:**
- $30/mo (100K documents, 10K searches/mo)
- **أفضل دعم للعربي** من أي search engine
- Typo-tolerance: "مقهى" يلاقي "مقاهي"
- Faceted search: filter by category + area + rating
- Instant search (< 50ms)
- **لماذا Meilisearch وليس Typesense أو Algolia:**
  - Typesense: دعم العربي أضعف
  - Algolia: غالي جداً ($50+ لنفس الحجم)
  - Elasticsearch: معقد و overkill لحجمنا

```
Search Architecture:

  Phase 1 (MVP):
  Client → API → PostgreSQL FTS → Results
  
  Phase 2 (Growth):
  Client → API → Meilisearch → Results
                      ↑
              Sync from PostgreSQL
              (every 5 min via Edge Function)
```

### File Storage: Cloudflare R2

**لماذا R2 وليس Supabase Storage أو S3:**

| المعيار | Cloudflare R2 | Supabase Storage | AWS S3 |
|---------|--------------|-----------------|--------|
| **Storage** | $0.015/GB/mo | 1GB free, $0.021/GB | $0.023/GB |
| **Egress** | **$0 (مجاني!)** | $0.09/GB | $0.09/GB |
| **CDN** | مدمج (Cloudflare) | يحتاج setup | CloudFront extra |
| **Image transform** | ✅ Workers | ❌ | ❌ (Lambda@Edge) |

**$0 egress = لا ندفع على عرض الصور.** هذا critical لموقع فيه آلاف الصور.

```
Image Pipeline:

  Upload → R2 Bucket → Cloudflare CDN → Client
                │
                ▼
         Workers (on-demand)
         ├─ Resize (thumb, medium, large)
         ├─ Convert to WebP/AVIF
         ├─ Strip EXIF
         └─ Cache forever (immutable URL)
```

### CDN: Cloudflare (مدمج)

- Free tier يشمل CDN كامل
- Edge nodes في الرياض والمنطقة
- Auto-minify CSS/JS
- Brotli compression
- HTTP/3 + QUIC

### الملخص التقني الكامل

```
┌────────────────────────────────────────────────────┐
│                    TECH STACK                       │
├────────────────────────────────────────────────────┤
│                                                    │
│  Runtime:      Supabase Edge Functions (Deno/TS)   │
│  Database:     PostgreSQL 15 + PostGIS 3.4         │
│  Auth:         Supabase Auth (GoTrue)              │
│  Cache:        Cloudflare KV → Upstash Redis       │
│  Search:       PostgreSQL FTS → Meilisearch        │
│  Storage:      Cloudflare R2                       │
│  CDN:          Cloudflare                          │
│  Edge:         Cloudflare Workers                  │
│  Realtime:     Supabase Realtime (WebSocket)       │
│  Monitoring:   Supabase Dashboard + Logflare       │
│  CI/CD:        GitHub Actions                      │
│  DNS:          Cloudflare DNS                      │
│                                                    │
│  Language:     TypeScript (backend + edge)          │
│  iOS:          SwiftUI + Supabase Swift SDK         │
│  Web:          Astro SSG → Next.js (later)         │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 3. API Design

### Base URL Strategy

```
MVP:      https://api.wainnrooh.com/v1/
           └─ Cloudflare Worker → proxies to Supabase

Alt:      https://<project>.supabase.co/rest/v1/
           └─ Direct Supabase (development only)
```

### Versioning Strategy

- **URL-based:** `/v1/`, `/v2/`
- **السبب:** أبسط للـ mobile apps (لا يمكن تحديث كل المستخدمين فوراً)
- **Deprecation:** إعلان 6 أشهر قبل إزالة version
- **Header:** `X-API-Version: 2026-02-20` (للتغييرات الصغيرة)

### Authentication

```
Authentication Flow:

  ┌──────────┐     ┌───────────────┐     ┌──────────────┐
  │  Client  │────►│ Supabase Auth │────►│  PostgreSQL   │
  │ (iOS/Web)│     │   (GoTrue)    │     │  (users tbl)  │
  └──────────┘     └───────────────┘     └──────────────┘
       │                   │
       │  1. Sign up/in    │  2. Issue JWT
       │   (email/phone/   │     (access + refresh)
       │    Apple/Google)  │
       │                   │
       ▼                   ▼
  ┌──────────────────────────────┐
  │  JWT Token (1hr expiry)      │
  │  ├─ sub: user_id             │
  │  ├─ role: authenticated      │
  │  ├─ email: user@example.com  │
  │  └─ app_metadata: {}         │
  └──────────────────────────────┘
       │
       │  3. Include in requests
       │     Authorization: Bearer <jwt>
       │
       ▼
  ┌──────────────────────────────┐
  │  Supabase RLS Policy         │
  │  checks JWT automatically    │
  │  before every DB query       │
  └──────────────────────────────┘
```

**Auth Methods:**
1. **Phone + OTP:** الأساسي (سعودي — رقم جوال أسهل)
2. **Apple Sign-In:** مطلوب من Apple لـ iOS apps
3. **Google Sign-In:** اختياري
4. **Anonymous auth:** للتصفح بدون حساب (Supabase يدعمه)

### REST Endpoints الكاملة

#### 🏠 Places

```
GET    /v1/places                    قائمة الأماكن (paginated)
GET    /v1/places/:id                تفاصيل مكان
GET    /v1/places/nearby             أماكن قريبة (بالإحداثيات)
GET    /v1/places/search             بحث (نص + فلاتر)
GET    /v1/places/:id/similar        أماكن مشابهة
GET    /v1/places/trending           الأكثر شعبية
GET    /v1/places/new                أماكن جديدة
POST   /v1/places                    إضافة مكان (admin)
PATCH  /v1/places/:id                تعديل مكان (admin)
DELETE /v1/places/:id                حذف مكان (admin)
POST   /v1/places/:id/report         بلاغ عن مكان
```

**GET /v1/places — Query Parameters:**

```
?page=1                  الصفحة (default: 1)
&per_page=20             عدد النتائج (default: 20, max: 100)
&category=cafe           التصنيف
&area=olaya              الحي
&min_rating=4.0          أقل تقييم
&price_range=$$          نطاق السعر ($, $$, $$$, $$$$)
&has_delivery=true       يوفر توصيل
&has_parking=true        فيه مواقف
&has_wifi=true           فيه واي فاي
&families=true           عوائل
&open_now=true           مفتوح الحين
&sort=rating             الترتيب (rating, distance, name, newest)
&lat=24.7136             خط العرض (للترتيب بالمسافة)
&lng=46.6753             خط الطول
&radius=5000             النطاق بالمتر (default: 5km)
&lang=ar                 اللغة (ar, en)
```

**Response:**

```json
{
  "data": [
    {
      "id": "place_abc123",
      "name_ar": "كافيه المعمار",
      "name_en": "Al Mimar Cafe",
      "slug": "al-mimar-cafe",
      "description_ar": "كافيه متخصص في القهوة المختصة...",
      "category": {
        "id": "cafe",
        "name_ar": "مقاهي",
        "name_en": "Cafes"
      },
      "area": {
        "id": "olaya",
        "name_ar": "العليا",
        "name_en": "Olaya"
      },
      "location": {
        "lat": 24.7136,
        "lng": 46.6753,
        "address_ar": "طريق الملك فهد، العليا",
        "google_maps_url": "https://maps.google.com/..."
      },
      "rating": {
        "average": 4.5,
        "count": 128
      },
      "price_range": "$$",
      "images": {
        "cover": "https://cdn.wainnrooh.com/places/abc123/cover.webp",
        "gallery": [
          "https://cdn.wainnrooh.com/places/abc123/1.webp",
          "https://cdn.wainnrooh.com/places/abc123/2.webp"
        ]
      },
      "features": {
        "wifi": true,
        "parking": true,
        "families": true,
        "outdoor": true,
        "delivery": true,
        "reservations": false
      },
      "hours": {
        "sunday": { "open": "07:00", "close": "23:00" },
        "monday": { "open": "07:00", "close": "23:00" },
        "tuesday": { "open": "07:00", "close": "23:00" },
        "wednesday": { "open": "07:00", "close": "23:00" },
        "thursday": { "open": "07:00", "close": "00:00" },
        "friday": { "open": "14:00", "close": "00:00" },
        "saturday": { "open": "07:00", "close": "23:00" }
      },
      "contact": {
        "phone": "+966512345678",
        "instagram": "@almimarcafe",
        "website": "https://almimarcafe.com"
      },
      "distance_m": 1250,
      "is_open_now": true,
      "created_at": "2026-01-15T10:30:00Z",
      "updated_at": "2026-02-19T14:22:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 342,
    "total_pages": 18
  }
}
```

#### 🔍 Search

```
GET    /v1/search                    بحث شامل
GET    /v1/search/suggest            اقتراحات (autocomplete)
GET    /v1/search/popular            عمليات البحث الشائعة
```

**GET /v1/search:**

```
?q=قهوة+مختصة+العليا       نص البحث
&category=cafe              فلتر التصنيف
&area=olaya                 فلتر الحي
&lat=24.7136&lng=46.6753    الموقع
&radius=5000                النطاق
&sort=relevance             الترتيب (relevance, distance, rating)
&page=1&per_page=20         الصفحات
```

**GET /v1/search/suggest:**

```
?q=قهو                      النص الجزئي
&limit=5                    عدد الاقتراحات

Response:
{
  "suggestions": [
    { "text": "قهوة مختصة", "count": 45 },
    { "text": "قهوة عربية", "count": 32 },
    { "text": "قهوة تركية", "count": 18 }
  ]
}
```

#### 🚗 Delivery

```
GET    /v1/delivery/prices           أسعار التوصيل
GET    /v1/delivery/prices/:placeId  أسعار توصيل مكان معين
GET    /v1/delivery/apps             تطبيقات التوصيل المتاحة
GET    /v1/delivery/compare          مقارنة أسعار التوصيل
```

**GET /v1/delivery/compare:**

```
?place_id=abc123            المكان
&lat=24.7136&lng=46.6753    موقع المستخدم

Response:
{
  "place": { "id": "abc123", "name_ar": "كافيه المعمار" },
  "delivery_options": [
    {
      "app": "hungerstation",
      "app_name_ar": "هنقرستيشن",
      "delivery_fee": 9.00,
      "min_order": 25.00,
      "estimated_time_min": 30,
      "currency": "SAR",
      "deeplink": "hungerstation://place/abc123"
    },
    {
      "app": "jahez",
      "app_name_ar": "جاهز",
      "delivery_fee": 12.00,
      "min_order": 20.00,
      "estimated_time_min": 25,
      "currency": "SAR",
      "deeplink": "jahez://restaurant/abc123"
    }
  ],
  "last_updated": "2026-02-19T08:00:00Z"
}
```

#### 💰 Prices (Menu)

```
GET    /v1/prices/:placeId           أسعار منيو مكان
GET    /v1/prices/:placeId/history   تاريخ تغيير الأسعار
GET    /v1/prices/compare            مقارنة أسعار منتج بين أماكن
```

**GET /v1/prices/:placeId:**

```json
{
  "place_id": "abc123",
  "currency": "SAR",
  "menu": [
    {
      "category_ar": "قهوة",
      "items": [
        {
          "name_ar": "لاتيه",
          "name_en": "Latte",
          "sizes": [
            { "size": "S", "price": 18.00 },
            { "size": "M", "price": 22.00 },
            { "size": "L", "price": 26.00 }
          ],
          "last_updated": "2026-02-15"
        }
      ]
    }
  ],
  "price_level": "$$",
  "avg_item_price": 24.50
}
```

#### 👤 Users

```
POST   /v1/auth/signup               تسجيل (phone/email)
POST   /v1/auth/login                دخول
POST   /v1/auth/logout               خروج
POST   /v1/auth/refresh              تجديد token
POST   /v1/auth/otp                  طلب OTP
POST   /v1/auth/verify-otp           تحقق OTP
GET    /v1/users/me                  ملفي
PATCH  /v1/users/me                  تعديل ملفي
GET    /v1/users/me/favorites        المفضلة
POST   /v1/users/me/favorites        إضافة للمفضلة
DELETE /v1/users/me/favorites/:id    حذف من المفضلة
GET    /v1/users/me/reviews          تقييماتي
GET    /v1/users/me/lists            قوائمي
POST   /v1/users/me/lists            إنشاء قائمة
GET    /v1/users/me/history          سجل الزيارات
```

#### ⭐ Reviews

```
GET    /v1/places/:id/reviews        تقييمات مكان
POST   /v1/places/:id/reviews        إضافة تقييم
PATCH  /v1/reviews/:id               تعديل تقييمي
DELETE /v1/reviews/:id               حذف تقييمي
POST   /v1/reviews/:id/report        بلاغ عن تقييم
POST   /v1/reviews/:id/helpful       مفيد
```

**POST /v1/places/:id/reviews:**

```json
{
  "rating": 4.5,
  "text_ar": "مكان جميل والقهوة ممتازة",
  "aspects": {
    "food": 5,
    "service": 4,
    "ambiance": 5,
    "value": 4
  },
  "images": ["upload_id_1", "upload_id_2"],
  "visited_at": "2026-02-18"
}
```

#### 📋 Categories & Areas

```
GET    /v1/categories                التصنيفات
GET    /v1/areas                     الأحياء
GET    /v1/areas/:id/stats           إحصائيات حي
```

#### 📊 Admin

```
GET    /v1/admin/stats               إحصائيات عامة
GET    /v1/admin/reports             البلاغات
PATCH  /v1/admin/reports/:id         معالجة بلاغ
GET    /v1/admin/scraping/status     حالة الـ scraping
POST   /v1/admin/scraping/trigger    تشغيل scraping يدوي
GET    /v1/admin/users               قائمة المستخدمين
```

#### 📤 Uploads

```
POST   /v1/uploads/image             رفع صورة
POST   /v1/uploads/presigned-url     طلب رابط رفع مباشر
```

### Rate Limiting

```
Rate Limits (per IP / per user):

  Anonymous:
  ├─ GET  /v1/*           → 60 req/min
  ├─ GET  /v1/search      → 30 req/min
  └─ POST /v1/auth/*      → 5 req/min

  Authenticated:
  ├─ GET  /v1/*           → 120 req/min
  ├─ GET  /v1/search      → 60 req/min
  ├─ POST /v1/reviews     → 10 req/min
  └─ POST /v1/uploads     → 20 req/min

  Admin:
  └─ All endpoints        → 300 req/min

Implementation:
  Cloudflare Worker → check Cloudflare KV counter
  Key: "ratelimit:{ip}:{endpoint}:{minute}"
  TTL: 60 seconds
```

### OpenAPI/Swagger

الـ spec الكامل يتولد تلقائياً من:
1. **Supabase:** auto-generates OpenAPI from database schema
2. **Edge Functions:** نضيف JSDoc + zod validation → auto-generate

```typescript
// Edge Function example with Zod schema
import { z } from "zod";

const SearchParams = z.object({
  q: z.string().min(1).max(200),
  category: z.string().optional(),
  area: z.string().optional(),
  lat: z.number().min(-90).max(90).optional(),
  lng: z.number().min(-180).max(180).optional(),
  radius: z.number().min(100).max(50000).default(5000),
  sort: z.enum(["relevance", "distance", "rating"]).default("relevance"),
  page: z.number().int().min(1).default(1),
  per_page: z.number().int().min(1).max(100).default(20),
});
```

الـ spec ينشر على: `https://api.wainnrooh.com/docs`

---

## 4. Data Layer

### Database Schema (SQL)

```sql
-- ============================================================
-- وين نروح بالرياض — Database Schema
-- PostgreSQL 15 + PostGIS 3.4
-- ============================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Trigram للبحث fuzzy
CREATE EXTENSION IF NOT EXISTS "unaccent";      -- تطبيع النصوص

-- ============================================================
-- ENUM Types
-- ============================================================

CREATE TYPE price_range AS ENUM ('$', '$$', '$$$', '$$$$');
CREATE TYPE report_status AS ENUM ('pending', 'reviewed', 'resolved', 'dismissed');
CREATE TYPE user_role AS ENUM ('user', 'moderator', 'admin');
CREATE TYPE day_of_week AS ENUM (
  'sunday', 'monday', 'tuesday', 'wednesday',
  'thursday', 'friday', 'saturday'
);

-- ============================================================
-- Categories
-- ============================================================

CREATE TABLE categories (
  id          TEXT PRIMARY KEY,           -- e.g., 'cafe', 'restaurant'
  name_ar     TEXT NOT NULL,
  name_en     TEXT NOT NULL,
  icon        TEXT,                       -- emoji or icon name
  slug        TEXT UNIQUE NOT NULL,
  sort_order  INTEGER DEFAULT 0,
  parent_id   TEXT REFERENCES categories(id),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Areas (أحياء الرياض)
-- ============================================================

CREATE TABLE areas (
  id          TEXT PRIMARY KEY,           -- e.g., 'olaya', 'malaz'
  name_ar     TEXT NOT NULL,
  name_en     TEXT NOT NULL,
  slug        TEXT UNIQUE NOT NULL,
  boundary    GEOMETRY(POLYGON, 4326),   -- حدود الحي
  center      GEOMETRY(POINT, 4326),     -- مركز الحي
  city        TEXT DEFAULT 'riyadh',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_areas_boundary ON areas USING GIST(boundary);

-- ============================================================
-- Places (الأماكن)
-- ============================================================

CREATE TABLE places (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- Basic info
  name_ar         TEXT NOT NULL,
  name_en         TEXT,
  slug            TEXT UNIQUE NOT NULL,
  description_ar  TEXT,
  description_en  TEXT,
  
  -- Classification
  category_id     TEXT NOT NULL REFERENCES categories(id),
  area_id         TEXT REFERENCES areas(id),
  price_range     price_range,
  
  -- Location
  location        GEOMETRY(POINT, 4326) NOT NULL,
  address_ar      TEXT,
  address_en      TEXT,
  google_maps_url TEXT,
  google_place_id TEXT UNIQUE,
  
  -- Contact
  phone           TEXT,
  website         TEXT,
  instagram       TEXT,
  twitter         TEXT,
  
  -- Media
  cover_image_url TEXT,
  
  -- Features (JSONB for flexibility)
  features        JSONB DEFAULT '{}'::JSONB,
  -- Example: {"wifi": true, "parking": true, "families": true,
  --           "outdoor": true, "delivery": true, "valet": false,
  --           "reservations": false, "kids_area": true}
  
  -- Hours (JSONB)
  hours           JSONB DEFAULT '{}'::JSONB,
  -- Example: {"sunday": {"open": "07:00", "close": "23:00"}, ...}
  
  -- Aggregated ratings (denormalized for performance)
  rating_avg      NUMERIC(3,2) DEFAULT 0,
  rating_count    INTEGER DEFAULT 0,
  
  -- Status
  is_active       BOOLEAN DEFAULT TRUE,
  is_verified     BOOLEAN DEFAULT FALSE,
  
  -- Search (tsvector for full-text search)
  search_vector_ar TSVECTOR,
  search_vector_en TSVECTOR,
  
  -- Metadata
  source          TEXT,                   -- 'manual', 'google', 'scrape'
  source_data     JSONB,                  -- original scraped data
  
  -- Timestamps
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_places_location ON places USING GIST(location);
CREATE INDEX idx_places_category ON places(category_id);
CREATE INDEX idx_places_area ON places(area_id);
CREATE INDEX idx_places_rating ON places(rating_avg DESC);
CREATE INDEX idx_places_active ON places(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_places_search_ar ON places USING GIN(search_vector_ar);
CREATE INDEX idx_places_search_en ON places USING GIN(search_vector_en);
CREATE INDEX idx_places_features ON places USING GIN(features);
CREATE INDEX idx_places_slug ON places(slug);
CREATE INDEX idx_places_name_trgm ON places USING GIN(name_ar gin_trgm_ops);

-- Auto-update search vectors
CREATE OR REPLACE FUNCTION places_search_update() RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector_ar := 
    setweight(to_tsvector('arabic', COALESCE(NEW.name_ar, '')), 'A') ||
    setweight(to_tsvector('arabic', COALESCE(NEW.description_ar, '')), 'B') ||
    setweight(to_tsvector('arabic', COALESCE(NEW.address_ar, '')), 'C');
  
  NEW.search_vector_en := 
    setweight(to_tsvector('english', COALESCE(NEW.name_en, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.description_en, '')), 'B');
  
  NEW.updated_at := NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_places_search
  BEFORE INSERT OR UPDATE OF name_ar, name_en, description_ar, description_en, address_ar
  ON places
  FOR EACH ROW
  EXECUTE FUNCTION places_search_update();

-- ============================================================
-- Place Images
-- ============================================================

CREATE TABLE place_images (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  place_id    UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  url         TEXT NOT NULL,
  alt_ar      TEXT,
  sort_order  INTEGER DEFAULT 0,
  uploaded_by UUID REFERENCES auth.users(id),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_place_images_place ON place_images(place_id);

-- ============================================================
-- Delivery Prices
-- ============================================================

CREATE TABLE delivery_apps (
  id          TEXT PRIMARY KEY,           -- 'hungerstation', 'jahez', etc.
  name_ar     TEXT NOT NULL,
  name_en     TEXT NOT NULL,
  logo_url    TEXT,
  deeplink_scheme TEXT,                   -- 'hungerstation://'
  is_active   BOOLEAN DEFAULT TRUE
);

CREATE TABLE delivery_prices (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  place_id        UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  app_id          TEXT NOT NULL REFERENCES delivery_apps(id),
  
  delivery_fee    NUMERIC(8,2),
  min_order       NUMERIC(8,2),
  estimated_time  INTEGER,                -- minutes
  is_available    BOOLEAN DEFAULT TRUE,
  
  deeplink_url    TEXT,
  
  -- Scraping metadata
  scraped_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  scrape_source   TEXT,
  raw_data        JSONB,
  
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(place_id, app_id)
);

CREATE INDEX idx_delivery_place ON delivery_prices(place_id);
CREATE INDEX idx_delivery_app ON delivery_prices(app_id);

-- ============================================================
-- Menu Prices
-- ============================================================

CREATE TABLE menu_categories (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  place_id    UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  name_ar     TEXT NOT NULL,
  name_en     TEXT,
  sort_order  INTEGER DEFAULT 0
);

CREATE TABLE menu_items (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  place_id        UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  category_id     UUID REFERENCES menu_categories(id) ON DELETE SET NULL,
  
  name_ar         TEXT NOT NULL,
  name_en         TEXT,
  description_ar  TEXT,
  
  -- Prices by size
  prices          JSONB NOT NULL,
  -- Example: [{"size": "S", "price": 18}, {"size": "M", "price": 22}]
  -- Or simple: [{"price": 35}]
  
  image_url       TEXT,
  is_available    BOOLEAN DEFAULT TRUE,
  
  scraped_at      TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_menu_items_place ON menu_items(place_id);

-- Price history (track changes over time)
CREATE TABLE price_history (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  item_id     UUID NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
  old_prices  JSONB NOT NULL,
  new_prices  JSONB NOT NULL,
  changed_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_price_history_item ON price_history(item_id);

-- ============================================================
-- User Profiles (extends Supabase auth.users)
-- ============================================================

CREATE TABLE profiles (
  id              UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username        TEXT UNIQUE,
  display_name    TEXT,
  avatar_url      TEXT,
  bio             TEXT,
  role            user_role DEFAULT 'user',
  
  -- Preferences
  preferred_lang  TEXT DEFAULT 'ar',
  home_location   GEOMETRY(POINT, 4326),  -- للاقتراحات المخصصة
  
  -- Stats (denormalized)
  reviews_count   INTEGER DEFAULT 0,
  favorites_count INTEGER DEFAULT 0,
  
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION create_profile_on_signup()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, display_name)
  VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data->>'display_name', 'مستخدم'));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION create_profile_on_signup();

-- ============================================================
-- Favorites
-- ============================================================

CREATE TABLE favorites (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  place_id    UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id, place_id)
);

CREATE INDEX idx_favorites_user ON favorites(user_id);

-- ============================================================
-- Reviews
-- ============================================================

CREATE TABLE reviews (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  place_id    UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  
  rating      NUMERIC(2,1) NOT NULL CHECK (rating >= 1 AND rating <= 5),
  text_ar     TEXT,
  
  -- Aspect ratings
  aspects     JSONB,
  -- {"food": 5, "service": 4, "ambiance": 5, "value": 4}
  
  visited_at  DATE,
  
  -- Moderation
  is_approved BOOLEAN DEFAULT TRUE,
  is_flagged  BOOLEAN DEFAULT FALSE,
  
  helpful_count INTEGER DEFAULT 0,
  
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id, place_id)  -- تقييم واحد لكل مستخدم لكل مكان
);

CREATE INDEX idx_reviews_place ON reviews(place_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(place_id, rating DESC);

-- Auto-update place rating on review change
CREATE OR REPLACE FUNCTION update_place_rating()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE places SET
    rating_avg = (
      SELECT COALESCE(AVG(rating), 0)
      FROM reviews
      WHERE place_id = COALESCE(NEW.place_id, OLD.place_id)
        AND is_approved = TRUE
    ),
    rating_count = (
      SELECT COUNT(*)
      FROM reviews
      WHERE place_id = COALESCE(NEW.place_id, OLD.place_id)
        AND is_approved = TRUE
    )
  WHERE id = COALESCE(NEW.place_id, OLD.place_id);
  
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_rating
  AFTER INSERT OR UPDATE OR DELETE ON reviews
  FOR EACH ROW
  EXECUTE FUNCTION update_place_rating();

-- ============================================================
-- Review Images
-- ============================================================

CREATE TABLE review_images (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  review_id   UUID NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
  url         TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Review Helpful Votes
-- ============================================================

CREATE TABLE review_helpful (
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  review_id   UUID NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, review_id)
);

-- ============================================================
-- User Lists (مثل "أماكن لازم أزورها")
-- ============================================================

CREATE TABLE user_lists (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name_ar     TEXT NOT NULL,
  description TEXT,
  is_public   BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_list_items (
  list_id     UUID NOT NULL REFERENCES user_lists(id) ON DELETE CASCADE,
  place_id    UUID NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  note        TEXT,
  sort_order  INTEGER DEFAULT 0,
  added_at    TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (list_id, place_id)
);

-- ============================================================
-- Reports (بلاغات)
-- ============================================================

CREATE TABLE reports (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  reporter_id UUID NOT NULL REFERENCES auth.users(id),
  
  -- Can report place or review
  place_id    UUID REFERENCES places(id) ON DELETE CASCADE,
  review_id   UUID REFERENCES reviews(id) ON DELETE CASCADE,
  
  reason      TEXT NOT NULL,
  details     TEXT,
  status      report_status DEFAULT 'pending',
  
  resolved_by UUID REFERENCES auth.users(id),
  resolved_at TIMESTAMPTZ,
  
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  
  CHECK (place_id IS NOT NULL OR review_id IS NOT NULL)
);

-- ============================================================
-- Search Analytics (لفهم ماذا يبحث المستخدمون)
-- ============================================================

CREATE TABLE search_logs (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID REFERENCES auth.users(id),
  query       TEXT NOT NULL,
  filters     JSONB,
  results_count INTEGER,
  clicked_place_id UUID REFERENCES places(id),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_search_logs_query ON search_logs(query);
CREATE INDEX idx_search_logs_date ON search_logs(created_at);

-- Partition by month for performance
-- (implement when data grows)

-- ============================================================
-- Scraping Jobs
-- ============================================================

CREATE TABLE scrape_jobs (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  job_type    TEXT NOT NULL,          -- 'delivery_prices', 'menu_prices', 'place_info'
  status      TEXT DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
  
  target_app  TEXT,                   -- e.g., 'hungerstation'
  places_count INTEGER DEFAULT 0,
  processed   INTEGER DEFAULT 0,
  errors      INTEGER DEFAULT 0,
  
  started_at  TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  error_log   JSONB,
  
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Row Level Security (RLS)
-- ============================================================

ALTER TABLE places ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_list_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

-- Places: everyone can read active places
CREATE POLICY "Places: public read"
  ON places FOR SELECT
  USING (is_active = TRUE);

-- Places: only admins can write
CREATE POLICY "Places: admin write"
  ON places FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );

-- Profiles: public read, own write
CREATE POLICY "Profiles: public read"
  ON profiles FOR SELECT
  USING (TRUE);

CREATE POLICY "Profiles: own update"
  ON profiles FOR UPDATE
  USING (id = auth.uid());

-- Favorites: own read/write
CREATE POLICY "Favorites: own access"
  ON favorites FOR ALL
  USING (user_id = auth.uid());

-- Reviews: public read, own write
CREATE POLICY "Reviews: public read"
  ON reviews FOR SELECT
  USING (is_approved = TRUE);

CREATE POLICY "Reviews: own insert"
  ON reviews FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Reviews: own update"
  ON reviews FOR UPDATE
  USING (user_id = auth.uid());

CREATE POLICY "Reviews: own delete"
  ON reviews FOR DELETE
  USING (user_id = auth.uid());

-- User Lists: public lists readable, own write
CREATE POLICY "Lists: public read"
  ON user_lists FOR SELECT
  USING (is_public = TRUE OR user_id = auth.uid());

CREATE POLICY "Lists: own write"
  ON user_lists FOR ALL
  USING (user_id = auth.uid());

-- Reports: own insert, admin read
CREATE POLICY "Reports: own insert"
  ON reports FOR INSERT
  WITH CHECK (reporter_id = auth.uid());

CREATE POLICY "Reports: admin read"
  ON reports FOR SELECT
  USING (
    reporter_id = auth.uid() OR
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'moderator')
    )
  );
```

### نقل البيانات من JSON إلى Database

```
Migration Pipeline:

  places.json (2.8MB, 3,202 records)
       │
       ▼
  ┌─────────────────────┐
  │  1. Parse & Validate │
  │  (Zod schema)        │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │  2. Transform       │
  │  ├─ Normalize names  │
  │  ├─ Geocode missing  │
  │  ├─ Map categories   │
  │  ├─ Map areas        │
  │  ├─ Generate slugs   │
  │  └─ Extract features │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │  3. Load to DB      │
  │  ├─ categories first │
  │  ├─ areas second     │
  │  ├─ places third     │
  │  └─ verify counts    │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │  4. Post-migration  │
  │  ├─ Build indexes    │
  │  ├─ Update vectors   │
  │  ├─ Verify search    │
  │  └─ Sanity checks    │
  └─────────────────────┘
```

**Migration Script (TypeScript):**

```typescript
// scripts/migrate-places.ts
import { createClient } from '@supabase/supabase-js';
import placesData from '../data/places.json';
import deliveryData from '../data/delivery-prices.json';
import pricesInitial from '../data/prices-initial.json';
import pricesBatch2 from '../data/prices-batch2.json';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY! // service key for migration
);

async function migrate() {
  console.log(`Migrating ${placesData.length} places...`);
  
  // 1. Extract unique categories
  const categories = [...new Set(placesData.map(p => p.category))];
  await supabase.from('categories').upsert(
    categories.map(c => ({
      id: slugify(c),
      name_ar: c,
      name_en: translateCategory(c),
      slug: slugify(c),
    }))
  );
  
  // 2. Extract unique areas
  const areas = [...new Set(placesData.map(p => p.area).filter(Boolean))];
  await supabase.from('areas').upsert(
    areas.map(a => ({
      id: slugify(a),
      name_ar: a,
      name_en: translateArea(a),
      slug: slugify(a),
    }))
  );
  
  // 3. Insert places in batches of 100
  const BATCH_SIZE = 100;
  for (let i = 0; i < placesData.length; i += BATCH_SIZE) {
    const batch = placesData.slice(i, i + BATCH_SIZE).map(p => ({
      name_ar: p.name,
      name_en: p.name_en || null,
      slug: generateSlug(p.name),
      description_ar: p.description || null,
      category_id: slugify(p.category),
      area_id: p.area ? slugify(p.area) : null,
      location: `POINT(${p.lng} ${p.lat})`,
      address_ar: p.address || null,
      phone: p.phone || null,
      instagram: p.instagram || null,
      google_maps_url: p.google_maps || null,
      features: extractFeatures(p),
      hours: p.hours || {},
      cover_image_url: p.image || null,
      rating_avg: p.rating || 0,
      rating_count: p.reviews_count || 0,
      source: 'migration',
      source_data: p,
    }));
    
    const { error } = await supabase.from('places').insert(batch);
    if (error) console.error(`Batch ${i}: ${error.message}`);
    else console.log(`Migrated ${Math.min(i + BATCH_SIZE, placesData.length)}/${placesData.length}`);
  }
  
  // 4. Migrate delivery prices
  // ... similar batch insert
  
  // 5. Migrate menu prices
  // ... similar batch insert
  
  console.log('Migration complete!');
}
```

### Indexing Strategy

```sql
-- ============================================================
-- Arabic Search Indexing
-- ============================================================

-- 1. Full-text search with Arabic dictionary
--    PostgreSQL ships with 'arabic' text search config
--    Works with: stemming, stop words, normalization

-- Test Arabic FTS:
SELECT to_tsvector('arabic', 'مقهى القهوة المختصة في الرياض');
-- Result: 'رياض':5 'قهو':1,2 'مختص':3

-- 2. Trigram index for fuzzy/partial matching
--    Catches typos: "مقهي" matches "مقهى"
CREATE INDEX idx_places_name_trgm ON places USING GIN(name_ar gin_trgm_ops);

-- 3. Spatial index for geo queries
CREATE INDEX idx_places_location ON places USING GIST(location);

-- 4. Composite indexes for common queries
CREATE INDEX idx_places_cat_rating 
  ON places(category_id, rating_avg DESC) 
  WHERE is_active = TRUE;

CREATE INDEX idx_places_area_cat 
  ON places(area_id, category_id) 
  WHERE is_active = TRUE;

-- 5. Example search query (Arabic)
-- بحث: "قهوة مختصة" في حي العليا
SELECT 
  p.*,
  ST_Distance(
    p.location,
    ST_SetSRID(ST_MakePoint(46.6753, 24.7136), 4326)::geography
  ) AS distance_m,
  ts_rank(p.search_vector_ar, query) AS relevance
FROM 
  places p,
  plainto_tsquery('arabic', 'قهوة مختصة') query
WHERE 
  p.is_active = TRUE
  AND p.search_vector_ar @@ query
  AND p.area_id = 'olaya'
ORDER BY 
  relevance DESC, 
  p.rating_avg DESC
LIMIT 20;
```

---

## 5. ربط iOS App

### Architecture

```
┌──────────────────────────────────────────┐
│              iOS App (SwiftUI)            │
│                                          │
│  ┌────────────┐  ┌──────────────────┐    │
│  │   Views    │  │  ViewModels      │    │
│  │  (SwiftUI) │──│  (ObservableObj) │    │
│  └────────────┘  └────────┬─────────┘    │
│                           │              │
│  ┌────────────────────────▼──────────┐   │
│  │         Repository Layer          │   │
│  │  ├─ PlacesRepository             │   │
│  │  ├─ SearchRepository             │   │
│  │  ├─ UserRepository               │   │
│  │  └─ DeliveryRepository           │   │
│  └────────────────┬──────────────────┘   │
│                   │                      │
│       ┌───────────┼───────────┐          │
│       │           │           │          │
│  ┌────▼────┐ ┌────▼────┐ ┌───▼────┐     │
│  │ Remote  │ │  Local  │ │ Cache  │     │
│  │  (API)  │ │(SwiftDa)│ │(Memory)│     │
│  └────┬────┘ └────┬────┘ └───┬────┘     │
│       │           │          │           │
└───────┼───────────┼──────────┼───────────┘
        │           │          │
        ▼           ▼          ▼
  ┌──────────┐ ┌─────────┐ ┌──────┐
  │ Supabase │ │ SQLite  │ │ NSCa │
  │   API    │ │(SwiftDa)│ │ che  │
  └──────────┘ └─────────┘ └──────┘
```

### Supabase Swift SDK Integration

```swift
// Config/SupabaseConfig.swift
import Supabase

let supabase = SupabaseClient(
    supabaseURL: URL(string: "https://xxx.supabase.co")!,
    supabaseKey: "your-anon-key" // anon key — safe for client
)

// Models/Place.swift
struct Place: Codable, Identifiable {
    let id: UUID
    let nameAr: String
    let nameEn: String?
    let slug: String
    let descriptionAr: String?
    let categoryId: String
    let areaId: String?
    let location: PostGISPoint
    let addressAr: String?
    let phone: String?
    let instagram: String?
    let coverImageUrl: String?
    let features: PlaceFeatures
    let hours: [String: DayHours]
    let ratingAvg: Double
    let ratingCount: Int
    let isActive: Bool
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case nameAr = "name_ar"
        case nameEn = "name_en"
        case slug
        case descriptionAr = "description_ar"
        case categoryId = "category_id"
        case areaId = "area_id"
        case location
        case addressAr = "address_ar"
        case phone, instagram
        case coverImageUrl = "cover_image_url"
        case features, hours
        case ratingAvg = "rating_avg"
        case ratingCount = "rating_count"
        case isActive = "is_active"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// Repositories/PlacesRepository.swift
class PlacesRepository {
    
    func fetchPlaces(
        category: String? = nil,
        area: String? = nil,
        page: Int = 1,
        perPage: Int = 20
    ) async throws -> [Place] {
        var query = supabase
            .from("places")
            .select()
            .eq("is_active", value: true)
        
        if let category { query = query.eq("category_id", value: category) }
        if let area { query = query.eq("area_id", value: area) }
        
        let response: [Place] = try await query
            .order("rating_avg", ascending: false)
            .range(from: (page - 1) * perPage, to: page * perPage - 1)
            .execute()
            .value
        
        return response
    }
    
    func fetchNearby(
        lat: Double,
        lng: Double,
        radiusMeters: Int = 5000
    ) async throws -> [Place] {
        // Use PostGIS via RPC
        let response: [Place] = try await supabase
            .rpc("nearby_places", params: [
                "lat": lat,
                "lng": lng,
                "radius_m": radiusMeters
            ])
            .execute()
            .value
        
        return response
    }
    
    func search(query: String) async throws -> [Place] {
        let response: [Place] = try await supabase
            .rpc("search_places", params: [
                "search_query": query
            ])
            .execute()
            .value
        
        return response
    }
}
```

### Offline-First Strategy

```
Offline-First Architecture:

  ┌────────────────────────────────────┐
  │           iOS App                   │
  │                                    │
  │  ┌──────────────────────────────┐  │
  │  │     SwiftData (Local DB)     │  │
  │  │                              │  │
  │  │  ┌────────┐  ┌───────────┐  │  │
  │  │  │ Places │  │ Favorites │  │  │
  │  │  │ (cache)│  │ (offline) │  │  │
  │  │  └────────┘  └───────────┘  │  │
  │  │                              │  │
  │  │  ┌────────┐  ┌───────────┐  │  │
  │  │  │Reviews │  │  Pending  │  │  │
  │  │  │(cache) │  │  Actions  │  │  │
  │  │  └────────┘  └───────────┘  │  │
  │  └──────────────────────────────┘  │
  │           │          ▲              │
  │           │          │              │
  │  ┌────────▼──────────┴───────────┐ │
  │  │       Sync Engine             │ │
  │  │  ├─ Pull: server → local      │ │
  │  │  ├─ Push: pending → server    │ │
  │  │  ├─ Conflict resolution       │ │
  │  │  └─ Delta sync (updated_at)   │ │
  │  └──────────────┬────────────────┘ │
  │                 │                   │
  └─────────────────┼───────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │   Supabase   │
            │   Realtime   │
            │  (WebSocket) │
            └──────────────┘
```

**Sync Strategy:**

```swift
// Services/SyncEngine.swift
class SyncEngine {
    
    /// Full sync on first launch
    func initialSync() async throws {
        let places = try await supabase
            .from("places")
            .select()
            .eq("is_active", value: true)
            .execute()
            .value as [Place]
        
        // Store in SwiftData
        try modelContext.transaction {
            for place in places {
                modelContext.insert(LocalPlace(from: place))
            }
        }
        
        UserDefaults.standard.set(Date(), forKey: "lastSync")
    }
    
    /// Delta sync — only changed records
    func deltaSync() async throws {
        let lastSync = UserDefaults.standard.object(forKey: "lastSync") as? Date
            ?? Date.distantPast
        
        let updated = try await supabase
            .from("places")
            .select()
            .gte("updated_at", value: lastSync.ISO8601Format())
            .execute()
            .value as [Place]
        
        // Upsert locally
        for place in updated {
            if let existing = try modelContext.fetch(
                FetchDescriptor<LocalPlace>(predicate: #Predicate { $0.id == place.id })
            ).first {
                existing.update(from: place)
            } else {
                modelContext.insert(LocalPlace(from: place))
            }
        }
        
        UserDefaults.standard.set(Date(), forKey: "lastSync")
    }
    
    /// Push pending actions (reviews, favorites added offline)
    func pushPending() async throws {
        let pending = try modelContext.fetch(
            FetchDescriptor<PendingAction>(
                sortBy: [SortDescriptor(\.createdAt)]
            )
        )
        
        for action in pending {
            try await action.execute(supabase: supabase)
            modelContext.delete(action)
        }
    }
    
    /// Realtime subscription for live updates
    func subscribeToChanges() {
        let channel = supabase.realtime.channel("places-changes")
        
        channel.on("postgres_changes", filter: .init(
            event: .all,
            schema: "public",
            table: "places"
        )) { payload in
            Task {
                // Update local cache
                await self.handleRealtimeChange(payload)
            }
        }
        
        channel.subscribe()
    }
}
```

**حجم البيانات المحلية:**
- 3,202 مكان × ~500 bytes = ~1.6MB (SQLite)
- Images cached on demand (NSCache + disk)
- Total initial download: ~2MB (أقل من الـ JSON الحالي!)

### Push Notifications

```
Push Notification Architecture:

  ┌──────────────┐
  │  APNs        │ ◄── Supabase Edge Function
  │  (Apple)     │     triggers on:
  └──────┬───────┘     ├─ New place near you
         │             ├─ Reply to your review
         ▼             ├─ Price drop alert
  ┌──────────────┐     ├─ Weekly digest
  │   iOS App    │     └─ Admin announcement
  │  ┌────────┐  │
  │  │  UNNot │  │
  │  │ Center │  │
  │  └────────┘  │
  └──────────────┘
```

**Implementation:**

```typescript
// supabase/functions/send-notification/index.ts
import { createClient } from '@supabase/supabase-js';

Deno.serve(async (req) => {
  const { user_id, title, body, data } = await req.json();
  
  // Get user's device token
  const { data: device } = await supabase
    .from('user_devices')
    .select('apns_token')
    .eq('user_id', user_id)
    .single();
  
  if (!device?.apns_token) return new Response('No device token');
  
  // Send via APNs
  const response = await fetch(
    `https://api.push.apple.com/3/device/${device.apns_token}`,
    {
      method: 'POST',
      headers: {
        'authorization': `bearer ${generateAPNsJWT()}`,
        'apns-topic': 'com.wainnrooh.app',
        'apns-push-type': 'alert',
      },
      body: JSON.stringify({
        aps: {
          alert: { title, body },
          sound: 'default',
          badge: 1,
        },
        data,
      }),
    }
  );
  
  return new Response('Sent');
});
```

### Image CDN Pipeline

```
Image Upload & Delivery:

  iOS App uploads image
       │
       ▼
  POST /v1/uploads/presigned-url
       │
       ▼
  Upload directly to Cloudflare R2
       │
       ▼
  Cloudflare Worker processes:
  ├─ Validate (size < 10MB, type = jpg/png/heic)
  ├─ Strip EXIF metadata (privacy)
  ├─ Generate variants:
  │   ├─ thumb:  150x150  (WebP, ~5KB)
  │   ├─ small:  400x300  (WebP, ~15KB)
  │   ├─ medium: 800x600  (WebP, ~40KB)
  │   └─ large:  1200x900 (WebP, ~80KB)
  ├─ Store all variants in R2
  └─ Return CDN URLs
       │
       ▼
  CDN URL: https://cdn.wainnrooh.com/places/{id}/{variant}.webp
  ├─ Cached at edge (Cloudflare CDN)
  ├─ Cache-Control: public, max-age=31536000, immutable
  └─ Content negotiation: WebP → AVIF → JPEG
```

### API Client Generation (OpenAPI → Swift)

```
OpenAPI Spec → Swift Client:

  1. Supabase auto-generates OpenAPI from schema
  2. We enhance with custom endpoints (Edge Functions)
  3. Generate Swift client using swift-openapi-generator

  openapi.yaml
       │
       ▼
  swift-openapi-generator
       │
       ▼
  Generated/
  ├─ Types.swift      (all models)
  ├─ Client.swift     (API client)
  └─ Server.swift     (mock server for testing)
```

**openapi-generator-config.yaml:**
```yaml
generate:
  - types
  - client
accessModifier: public
```

---

## 6. ربط الموقع

### التوصية: Astro SSG (MVP) → Next.js (Growth)

**لماذا Astro أولاً:**

| المعيار | Static (حالي) | Astro SSG | Next.js SSR |
|---------|--------------|-----------|-------------|
| **التكلفة** | $0 (GitHub Pages) | $0 (Cloudflare Pages) | $20/mo (Vercel) |
| **سرعة التحميل** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **SEO** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Dynamic content** | ❌ | ⚠️ محدود | ✅ كامل |
| **Build time** | N/A | ~30s | ~60s |
| **Arabic SSR** | ❌ | ✅ (build time) | ✅ (runtime) |

**الخطة:**

```
Phase 1 (MVP): Astro SSG + Islands
┌──────────────────────────────────┐
│  Astro SSG (build time)          │
│  ├─ Static HTML pages            │
│  ├─ Pre-rendered place pages     │
│  ├─ React islands for dynamic:   │
│  │   ├─ Search bar               │
│  │   ├─ Map component            │
│  │   ├─ Reviews (lazy)           │
│  │   └─ Favorites (lazy)         │
│  └─ API calls client-side        │
│                                  │
│  Deploy: Cloudflare Pages ($0)   │
└──────────────────────────────────┘

Phase 2 (Growth): Next.js App Router
┌──────────────────────────────────┐
│  Next.js (SSR + ISR)             │
│  ├─ Server Components (Arabic)   │
│  ├─ ISR: revalidate every 1hr    │
│  ├─ Dynamic routes for places    │
│  ├─ Auth via Supabase SSR        │
│  ├─ Reviews, lists, profiles     │
│  └─ Full dynamic features        │
│                                  │
│  Deploy: Vercel ($20/mo)         │
│  or Cloudflare Pages (free)      │
└──────────────────────────────────┘
```

### API Integration Strategy

```
Website API Flow:

  Browser ──► Cloudflare CDN
                 │
                 ├─ Static assets (HTML, CSS, JS, images)
                 │   └─ Cache: 1 year (immutable hash URLs)
                 │
                 ├─ Place pages (pre-rendered HTML)
                 │   └─ Cache: 1 hour (ISR/rebuild)
                 │
                 └─ API calls (client-side)
                     │
                     ▼
               Cloudflare Worker
                     │
                     ├─ Cache check (KV)
                     │   ├─ HIT → return cached
                     │   └─ MISS → forward to Supabase
                     │
                     └─ Supabase API
                         └─ PostgreSQL
```

### Real-time Features

```
Supabase Realtime (WebSocket):

  استخدامات:
  1. عدد المتصفحين الحين ("42 شخص يتصفحون هذا المكان")
  2. تحديث التقييمات live
  3. إشعارات الردود
  
  Implementation:
  
  // Client-side (JavaScript)
  const channel = supabase
    .channel('place-viewers')
    .on('presence', { event: 'sync' }, () => {
      const viewers = channel.presenceState();
      updateViewerCount(Object.keys(viewers).length);
    })
    .subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        await channel.track({ user_id: userId });
      }
    });
```

**ملاحظة:** Real-time features تجي Phase 2+. المهم الحين الـ static site يشتغل مع API.

---

## 7. AI Integration

### Architecture Overview

```
AI Architecture:

  ┌─────────────────────────────────────────────┐
  │                 Server-Side AI               │
  │                                             │
  │  ┌───────────────────┐  ┌────────────────┐  │
  │  │  Semantic Search   │  │ Recommendations│  │
  │  │  (Embeddings)      │  │  Engine        │  │
  │  │                   │  │                │  │
  │  │  "أبي مكان هادي   │  │  Based on:     │  │
  │  │   للدراسة قريب"   │  │  ├─ History    │  │
  │  │                   │  │  ├─ Favorites  │  │
  │  │  → Embed query    │  │  ├─ Location   │  │
  │  │  → Vector search  │  │  └─ Similar    │  │
  │  │  → Return matches │  │    users       │  │
  │  └───────────────────┘  └────────────────┘  │
  │                                             │
  │  ┌───────────────────┐  ┌────────────────┐  │
  │  │  Arabic NLP       │  │ Smart Summary  │  │
  │  │  Pipeline         │  │  Generator     │  │
  │  │                   │  │                │  │
  │  │  ├─ Tokenization  │  │  "Generate a   │  │
  │  │  ├─ Stemming      │  │   summary of   │  │
  │  │  ├─ NER           │  │   this cafe    │  │
  │  │  └─ Sentiment     │  │   from reviews"│  │
  │  └───────────────────┘  └────────────────┘  │
  └─────────────────────────────────────────────┘
          │
          │ API calls
          ▼
  ┌─────────────────────────────────────────────┐
  │              Client-Side AI                  │
  │                                             │
  │  ┌───────────────────┐  ┌────────────────┐  │
  │  │  Natural Language  │  │ Personalized   │  │
  │  │  Search UI         │  │  Feed          │  │
  │  │  (query → API)     │  │  (display)     │  │
  │  └───────────────────┘  └────────────────┘  │
  └─────────────────────────────────────────────┘
```

**القرار: كل الـ AI يشتغل server-side.** الأسباب:
1. **تكلفة أقل:** API calls أرخص من on-device ML
2. **تحديث أسهل:** نحدث النموذج بدون تحديث التطبيق
3. **أداء أفضل:** GPU على السيرفر أقوى من iPhone
4. **خصوصية:** البيانات تبقى على السيرفر

### Arabic NLP Pipeline

```
Arabic NLP Pipeline:

  Raw Arabic Text
  "أبي مقهى هادي قريب من العليا فيه واي فاي"
       │
       ▼
  ┌─────────────────────┐
  │ 1. Normalization     │
  │  ├─ Remove tashkeel  │  "أبي" → "ابي"
  │  ├─ Normalize alef   │  "إ" → "ا"
  │  ├─ Normalize taa    │  "ة" → "ه"
  │  └─ Remove tatweel   │  "مقـــهى" → "مقهى"
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ 2. Tokenization      │
  │  camel-tools or      │
  │  custom tokenizer    │
  │                      │
  │  ["ابي", "مقهى",     │
  │   "هادي", "قريب",    │
  │   "من", "العليا",    │
  │   "فيه", "واي فاي"]  │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ 3. Intent Detection  │
  │  ├─ "ابي" → SEARCH   │
  │  ├─ Entity: مقهى     │
  │  │   → category:cafe  │
  │  ├─ Entity: العليا   │
  │  │   → area:olaya     │
  │  └─ Features:         │
  │      quiet=true       │
  │      wifi=true        │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ 4. Structured Query  │
  │                      │
  │  {                   │
  │    category: "cafe", │
  │    area: "olaya",    │
  │    features: {       │
  │      quiet: true,    │
  │      wifi: true      │
  │    },                │
  │    sort: "distance"  │
  │  }                   │
  └─────────────────────┘
```

**المكتبات:**
- **Tokenization:** CAMeL Tools (Python) أو regex-based (TypeScript)
- **For MVP:** Simple keyword matching + synonyms dictionary
- **For Growth:** OpenAI API for intent detection (cheapest: gpt-4o-mini)

### Embedding Model for Semantic Search

```
Semantic Search Pipeline:

  1. Index Time (offline, batch):
  ┌─────────────────────────────────────┐
  │  For each place:                     │
  │                                     │
  │  text = f"{name} {description}       │
  │          {category} {features}"      │
  │       │                             │
  │       ▼                             │
  │  OpenAI Embeddings API              │
  │  model: text-embedding-3-small      │
  │  dimensions: 256 (reduced)          │
  │  Cost: $0.02 / 1M tokens            │
  │       │                             │
  │       ▼                             │
  │  Store in PostgreSQL:               │
  │  pgvector extension                 │
  │  CREATE EXTENSION vector;           │
  │                                     │
  │  ALTER TABLE places ADD COLUMN      │
  │    embedding vector(256);           │
  │                                     │
  │  3,202 places × ~100 tokens each   │
  │  = ~320K tokens = $0.006 (!)       │
  └─────────────────────────────────────┘

  2. Query Time (real-time):
  ┌─────────────────────────────────────┐
  │  User: "مكان رومانسي لعشاء خاص"     │
  │       │                             │
  │       ▼                             │
  │  Embed query (same model)           │
  │       │                             │
  │       ▼                             │
  │  SELECT *, embedding <=> $1 AS dist │
  │  FROM places                        │
  │  WHERE is_active = TRUE             │
  │  ORDER BY dist ASC                  │
  │  LIMIT 20;                          │
  │       │                             │
  │       ▼                             │
  │  Return semantically similar places │
  └─────────────────────────────────────┘
```

**لماذا `text-embedding-3-small` من OpenAI:**
1. أفضل أداء مع العربي من البدائل المجانية
2. 256 dimensions كافية (بدل 1536 — يوفر storage)
3. تكلفة شبه مجانية: $0.006 لفهرسة كل الأماكن
4. سريع: ~200ms per request

**البديل المجاني:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- يشتغل locally بدون API
- أداء أقل مع العربي
- يحتاج server compute

### Recommendation Engine

```
Recommendation Algorithm:

  Input Signals:
  ├─ User favorites (explicit preference)
  ├─ User reviews (rated places)
  ├─ Search history (intent)
  ├─ Location (proximity)
  ├─ Time of day (breakfast vs dinner)
  └─ Similar users (collaborative filtering)
       │
       ▼
  ┌────────────────────────────────────┐
  │     Hybrid Recommendation          │
  │                                    │
  │  Score = w1 × content_similarity   │  (embedding distance)
  │        + w2 × collaborative_score  │  (similar users liked)
  │        + w3 × popularity_score     │  (rating × review_count)
  │        + w4 × recency_boost        │  (newer places)
  │        + w5 × distance_penalty     │  (closer = better)
  │        + w6 × time_relevance       │  (open now + suitable)
  │                                    │
  │  Weights (MVP):                    │
  │  w1=0.3, w2=0.2, w3=0.2,         │
  │  w4=0.1, w5=0.1, w6=0.1          │
  └────────────────────────────────────┘
       │
       ▼
  Top 20 recommendations
  (re-ranked, deduplicated, diversified)
```

**MVP Implementation:** Simple content-based (embedding similarity + popularity). No collaborative filtering until we have enough user data (1,000+ users).

---

## 8. Scraping & Data Pipeline

### Architecture

```
Scraping Pipeline Architecture:

  ┌─────────────────────────────────────────────┐
  │           Scheduler (Cron Triggers)          │
  │                                             │
  │  ┌────────┐ ┌────────┐ ┌────────────────┐  │
  │  │ Daily  │ │Weekly  │ │  On-demand     │  │
  │  │02:00 AM│ │Friday  │ │  (admin panel) │  │
  │  │delivery│ │ menu   │ │                │  │
  │  │prices  │ │prices  │ │                │  │
  │  └───┬────┘ └───┬────┘ └───────┬────────┘  │
  │      │          │              │            │
  └──────┼──────────┼──────────────┼────────────┘
         │          │              │
         ▼          ▼              ▼
  ┌──────────────────────────────────────┐
  │        Edge Function: Scraper         │
  │                                      │
  │  1. Get target list from DB          │
  │  2. For each target:                 │
  │     ├─ Rate limit (2 req/sec)        │
  │     ├─ Random delays (1-5 sec)       │
  │     ├─ Rotate User-Agent             │
  │     ├─ Fetch page/API                │
  │     ├─ Parse response                │
  │     ├─ Validate data                 │
  │     └─ Store in staging table        │
  │  3. Compare with existing data       │
  │  4. Update if changed               │
  │  5. Log results                      │
  └──────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────┐
  │        Data Validation Pipeline       │
  │                                      │
  │  ├─ Price range check (SAR 1-5000)   │
  │  ├─ Phone number format              │
  │  ├─ GPS coordinates in Riyadh bbox   │
  │  ├─ Category consistency             │
  │  ├─ Duplicate detection              │
  │  └─ Anomaly detection (±50% change)  │
  └──────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────┐
  │        Staging → Production           │
  │                                      │
  │  ├─ Auto-approve: normal changes     │
  │  ├─ Flag for review: large changes   │
  │  └─ Reject: invalid data             │
  └──────────────────────────────────────┘
```

### Cron Jobs Architecture

```typescript
// supabase/functions/cron-scrape-delivery/index.ts
// Triggered by Supabase Cron (pg_cron extension)

// Schedule: Every day at 02:00 AM AST (23:00 UTC)
// SELECT cron.schedule('scrape-delivery', '0 23 * * *', $$
//   SELECT net.http_post(
//     url := 'https://xxx.supabase.co/functions/v1/cron-scrape-delivery',
//     headers := '{"Authorization": "Bearer service_key"}'::jsonb
//   );
// $$);

import { createClient } from '@supabase/supabase-js';

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );
  
  // Create scrape job
  const { data: job } = await supabase
    .from('scrape_jobs')
    .insert({
      job_type: 'delivery_prices',
      status: 'running',
      started_at: new Date().toISOString(),
    })
    .select()
    .single();
  
  const apps = ['hungerstation', 'jahez', 'marsool', 'toyou', 'careem', 'nana'];
  let processed = 0;
  let errors = 0;
  
  for (const app of apps) {
    try {
      const prices = await scrapeDeliveryPrices(app);
      
      // Validate
      const validated = prices.filter(p => validatePrice(p));
      
      // Upsert
      await supabase
        .from('delivery_prices')
        .upsert(validated, { onConflict: 'place_id,app_id' });
      
      processed += validated.length;
    } catch (e) {
      errors++;
      console.error(`Error scraping ${app}:`, e);
    }
    
    // Rate limit between apps
    await new Promise(r => setTimeout(r, 5000));
  }
  
  // Update job status
  await supabase
    .from('scrape_jobs')
    .update({
      status: errors > 3 ? 'failed' : 'completed',
      processed,
      errors,
      completed_at: new Date().toISOString(),
    })
    .eq('id', job.id);
  
  return new Response(JSON.stringify({ processed, errors }));
});
```

### Anti-Bot Handling

```
Anti-Bot Strategy:

  1. Request Patterns:
  ├─ Rate limit: 2 requests/second max
  ├─ Random delays: 1-5 seconds between requests
  ├─ Randomize request order
  └─ Don't scrape same target more than 1x/day

  2. Headers:
  ├─ Rotate User-Agent (pool of 50+ real browsers)
  ├─ Accept-Language: ar-SA,ar;q=0.9,en;q=0.8
  ├─ Realistic Referer headers
  └─ Accept-Encoding: gzip, deflate, br

  3. IP Rotation:
  ├─ MVP: Single IP (Edge Function) — sufficient for 6 apps
  ├─ Growth: Proxy rotation service (if blocked)
  └─ Scale: Residential proxies (last resort)

  4. Fallback Strategy:
  ├─ If blocked → wait 24 hours, retry
  ├─ If API changes → alert admin, pause scraping
  ├─ Manual override: admin can trigger with different strategy
  └─ Worst case: crowdsource prices from users
```

### Data Validation Pipeline

```typescript
// lib/validation.ts

interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

function validatePlace(place: any): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Required fields
  if (!place.name_ar) errors.push('Missing Arabic name');
  if (!place.location) errors.push('Missing location');
  
  // GPS in Riyadh bounding box
  const RIYADH_BBOX = {
    minLat: 24.4,  maxLat: 25.1,
    minLng: 46.3,  maxLng: 47.1,
  };
  if (place.lat < RIYADH_BBOX.minLat || place.lat > RIYADH_BBOX.maxLat ||
      place.lng < RIYADH_BBOX.minLng || place.lng > RIYADH_BBOX.maxLng) {
    errors.push('Location outside Riyadh');
  }
  
  // Phone format (Saudi)
  if (place.phone && !/^\+966[0-9]{9}$/.test(place.phone)) {
    warnings.push('Invalid Saudi phone format');
  }
  
  // Price range check
  if (place.delivery_fee && (place.delivery_fee < 0 || place.delivery_fee > 100)) {
    errors.push('Delivery fee out of range (0-100 SAR)');
  }
  
  // Anomaly: price changed more than 50%
  if (place.old_price && place.new_price) {
    const change = Math.abs(place.new_price - place.old_price) / place.old_price;
    if (change > 0.5) {
      warnings.push(`Price changed ${(change * 100).toFixed(0)}% — needs review`);
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    warnings,
  };
}
```

---

## 9. Security

### Authentication Flow

```
Complete Auth Flow:

  ┌─────────────────────────────────────────────────┐
  │                   Registration                   │
  │                                                 │
  │  Phone OTP (Primary):                           │
  │  ┌────────┐  ┌──────────┐  ┌────────────────┐  │
  │  │ Enter  │─►│ Supabase │─►│  SMS via       │  │
  │  │ +966.. │  │ sends OTP│  │  Twilio/MessageB│ │
  │  └────────┘  └──────────┘  └───────┬────────┘  │
  │                                    │            │
  │  ┌────────┐  ┌──────────┐  ┌───────▼────────┐  │
  │  │ Enter  │─►│ Verify   │─►│  Create user   │  │
  │  │  OTP   │  │  OTP     │  │  + profile     │  │
  │  └────────┘  └──────────┘  └───────┬────────┘  │
  │                                    │            │
  │  ┌─────────────────────────────────▼─────────┐  │
  │  │  Return: access_token (JWT) + refresh     │  │
  │  └──────────────────────────────────────────┘  │
  │                                                 │
  │  Apple Sign-In (iOS):                           │
  │  ┌──────┐  ┌───────┐  ┌──────────┐  ┌───────┐ │
  │  │Apple │─►│AuthSrv│─►│Supabase  │─►│Create │ │
  │  │SignIn│  │ident  │  │verifies  │  │or link│ │
  │  └──────┘  └───────┘  └──────────┘  └───────┘ │
  └─────────────────────────────────────────────────┘

  Token Lifecycle:
  ┌──────────────────────────────────────────────┐
  │  access_token:  1 hour expiry                 │
  │  refresh_token: 30 days expiry                │
  │                                              │
  │  iOS: Stored in Keychain (encrypted)          │
  │  Web: httpOnly secure cookie                  │
  │                                              │
  │  Refresh flow:                                │
  │  Token expired → auto-refresh → new tokens    │
  │  Refresh expired → re-login required          │
  └──────────────────────────────────────────────┘
```

### API Security

```
Security Layers:

  Request
    │
    ▼
  ┌─────────────────────────────────┐
  │  1. Cloudflare WAF              │  ← DDoS protection, bot detection
  │     ├─ Rate limiting            │
  │     ├─ IP reputation            │
  │     ├─ Managed rules            │
  │     └─ Challenge mode           │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  2. Cloudflare Worker           │  ← API gateway
  │     ├─ Rate limit (per user)    │
  │     ├─ CORS enforcement         │
  │     ├─ Request validation       │
  │     ├─ API key check (if B2B)   │
  │     └─ Geo-blocking (optional)  │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  3. Supabase JWT Verification   │  ← Authentication
  │     ├─ Verify JWT signature     │
  │     ├─ Check expiry             │
  │     ├─ Extract user claims      │
  │     └─ Pass to RLS              │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  4. Row Level Security (RLS)    │  ← Authorization
  │     ├─ User can only read own   │
  │     │   favorites/reviews       │
  │     ├─ Admin can write places   │
  │     └─ Public can read places   │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  5. Input Validation (Zod)      │  ← Data integrity
  │     ├─ Type checking            │
  │     ├─ Size limits              │
  │     ├─ SQL injection prevention │
  │     └─ XSS sanitization         │
  └─────────────────────────────────┘
```

### OWASP Top 10 Protections

```
┌──────┬─────────────────────────┬────────────────────────────────┐
│  #   │  Vulnerability          │  Protection                    │
├──────┼─────────────────────────┼────────────────────────────────┤
│  1   │  Broken Access Control  │  Supabase RLS policies         │
│      │                         │  JWT verification on all       │
│      │                         │  endpoints                     │
├──────┼─────────────────────────┼────────────────────────────────┤
│  2   │  Cryptographic Failures │  TLS 1.3 everywhere            │
│      │                         │  Supabase encrypts at rest     │
│      │                         │  No secrets in code            │
├──────┼─────────────────────────┼────────────────────────────────┤
│  3   │  Injection              │  Supabase uses parameterized   │
│      │                         │  queries (no raw SQL from API) │
│      │                         │  Zod input validation          │
├──────┼─────────────────────────┼────────────────────────────────┤
│  4   │  Insecure Design        │  Threat modeling per feature   │
│      │                         │  Rate limiting everywhere      │
│      │                         │  Principle of least privilege  │
├──────┼─────────────────────────┼────────────────────────────────┤
│  5   │  Security Misconfig     │  Supabase manages server       │
│      │                         │  config. We manage RLS only.   │
│      │                         │  No default credentials        │
├──────┼─────────────────────────┼────────────────────────────────┤
│  6   │  Vulnerable Components  │  Dependabot alerts             │
│      │                         │  npm audit in CI               │
│      │                         │  Monthly dependency updates    │
├──────┼─────────────────────────┼────────────────────────────────┤
│  7   │  Auth Failures          │  Supabase Auth (battle-tested) │
│      │                         │  OTP rate limiting (5/min)     │
│      │                         │  Account lockout after 10 fail │
├──────┼─────────────────────────┼────────────────────────────────┤
│  8   │  Data Integrity         │  Input validation (Zod)        │
│      │                         │  DB constraints (CHECK, FK)    │
│      │                         │  Image scanning on upload      │
├──────┼─────────────────────────┼────────────────────────────────┤
│  9   │  Logging Failures       │  Supabase Logflare             │
│      │                         │  All auth events logged        │
│      │                         │  Anomaly alerting              │
├──────┼─────────────────────────┼────────────────────────────────┤
│ 10   │  SSRF                   │  Edge Functions isolated       │
│      │                         │  Allowlist for external calls  │
│      │                         │  No user-controlled URLs       │
└──────┴─────────────────────────┴────────────────────────────────┘
```

### Saudi Data Residency (PDPL — نظام حماية البيانات الشخصية)

```
PDPL Compliance Checklist:

  ✅  Privacy Policy (Arabic):
      ├─ What data we collect
      ├─ Why we collect it
      ├─ How we use it
      ├─ Who we share it with
      └─ User rights (access, delete, correct)

  ✅  Consent:
      ├─ Clear consent before collecting personal data
      ├─ Separate consent for marketing
      └─ Easy opt-out mechanism

  ✅  Data Minimization:
      ├─ Only collect what's needed
      ├─ Phone number + display name (minimum)
      └─ Location only when actively using

  ⚠️  Data Residency:
      ├─ PDPL requires data processing in Saudi Arabia
      │   OR in a country with adequate protection
      ├─ Supabase (AWS us-east-1) — needs review
      ├─ Options:
      │   1. Supabase on AWS me-south-1 (Bahrain) — ask Supabase
      │   2. Self-host PostgreSQL on AWS Bahrain
      │   3. Request PDPL adequacy assessment
      └─ LOW RISK for MVP: no sensitive data (just places + reviews)

  ✅  Data Breach Notification:
      ├─ Notify SDAIA within 72 hours
      └─ Notify affected users

  ✅  Right to Delete:
      ├─ User can delete their account
      ├─ All personal data removed (CASCADE)
      └─ Anonymize reviews (keep text, remove user link)

  ✅  Data Processing Agreement:
      └─ Supabase DPA available for Pro plan
```

**ملاحظة عن PDPL:** القانون ما زال في مراحل التطبيق المبكرة. للـ MVP مع بيانات غير حساسة (أماكن عامة + اسم مستعار)، المخاطر منخفضة. عند جمع بيانات حساسة (موقع دقيق، سلوك تصفح)، نحتاج مراجعة قانونية.

---

## 10. DevOps

### CI/CD Pipeline

```
CI/CD Pipeline (GitHub Actions):

  ┌─────────────────────────────────────────────┐
  │  Push to main / PR                           │
  │                                             │
  │  ┌─────────────────────────────────────┐    │
  │  │  1. Lint & Type Check               │    │
  │  │  ├─ ESLint + Prettier               │    │
  │  │  ├─ TypeScript strict mode           │    │
  │  │  └─ Fails fast on errors             │    │
  │  └─────────────┬───────────────────────┘    │
  │                │                             │
  │  ┌─────────────▼───────────────────────┐    │
  │  │  2. Tests                           │    │
  │  │  ├─ Unit tests (Vitest)             │    │
  │  │  ├─ Integration tests (Supabase local)│  │
  │  │  ├─ API tests (Hurl/Bruno)          │    │
  │  │  └─ Coverage > 80%                  │    │
  │  └─────────────┬───────────────────────┘    │
  │                │                             │
  │  ┌─────────────▼───────────────────────┐    │
  │  │  3. Security Scan                   │    │
  │  │  ├─ npm audit                       │    │
  │  │  ├─ Semgrep (SAST)                  │    │
  │  │  └─ Secret scanning                 │    │
  │  └─────────────┬───────────────────────┘    │
  │                │                             │
  │  ┌─────────────▼───────────────────────┐    │
  │  │  4. Build                           │    │
  │  │  ├─ Build Edge Functions            │    │
  │  │  ├─ Build website (Astro)           │    │
  │  │  └─ Generate OpenAPI spec           │    │
  │  └─────────────┬───────────────────────┘    │
  │                │                             │
  │                │  (only on merge to main)    │
  │                │                             │
  │  ┌─────────────▼───────────────────────┐    │
  │  │  5. Deploy                          │    │
  │  │  ├─ Supabase migrations (db push)   │    │
  │  │  ├─ Edge Functions (supabase deploy)│    │
  │  │  ├─ Cloudflare Workers (wrangler)   │    │
  │  │  ├─ Website (Cloudflare Pages)      │    │
  │  │  └─ Invalidate CDN cache            │    │
  │  └─────────────────────────────────────┘    │
  └─────────────────────────────────────────────┘
```

**GitHub Actions Workflow:**

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test -- --coverage
      - run: npx semgrep --config auto

  deploy:
    needs: lint-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Deploy DB migrations
      - uses: supabase/setup-cli@v1
      - run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
      
      # Deploy Edge Functions
      - run: supabase functions deploy
      
      # Deploy Workers
      - run: npx wrangler deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
      
      # Deploy Website
      # (Cloudflare Pages auto-deploys from GitHub)
```

### Monitoring & Alerting

```
Monitoring Stack:

  ┌────────────────────────────────────────┐
  │          Monitoring Dashboard           │
  │                                        │
  │  ┌──────────────┐  ┌───────────────┐   │
  │  │  Supabase    │  │  Cloudflare   │   │
  │  │  Dashboard   │  │  Analytics    │   │
  │  │              │  │               │   │
  │  │  ├─ DB stats │  │  ├─ Traffic   │   │
  │  │  ├─ API logs │  │  ├─ Errors    │   │
  │  │  ├─ Auth     │  │  ├─ Cache hit │   │
  │  │  └─ Realtime │  │  └─ WAF       │   │
  │  └──────────────┘  └───────────────┘   │
  │                                        │
  │  ┌──────────────┐  ┌───────────────┐   │
  │  │  Logflare    │  │  UptimeRobot  │   │
  │  │  (logs)      │  │  (free)       │   │
  │  │              │  │               │   │
  │  │  ├─ Errors   │  │  ├─ API up?   │   │
  │  │  ├─ Slow     │  │  ├─ Web up?   │   │
  │  │  └─ Search   │  │  └─ Alerts    │   │
  │  └──────────────┘  └───────────────┘   │
  └────────────────────────────────────────┘
```

**Alerts:**

| Metric | Threshold | Action |
|--------|-----------|--------|
| API response time | > 2 seconds | Warning → Telegram |
| API error rate | > 5% | Critical → Telegram + Email |
| DB connections | > 80% max | Warning → Telegram |
| DB size | > 400MB (free tier) | Warning → plan upgrade |
| Scraping failures | > 50% | Warning → pause + review |
| Auth failures | > 20/min (same IP) | Block IP via Cloudflare |
| Storage | > 800MB (free tier) | Cleanup old images |

### Logging

```
Log Levels:
├─ ERROR:  Exceptions, failed requests, data corruption
├─ WARN:   Rate limits hit, validation failures, slow queries
├─ INFO:   API requests, auth events, scraping results
└─ DEBUG:  Query details (dev only)

Log Format (structured JSON):
{
  "level": "error",
  "timestamp": "2026-02-20T10:30:00Z",
  "service": "edge-function",
  "function": "search-places",
  "request_id": "req_abc123",
  "user_id": "usr_xyz789",
  "message": "Search query failed",
  "error": "timeout after 5000ms",
  "metadata": {
    "query": "مقهى العليا",
    "duration_ms": 5001
  }
}

Storage:
├─ Supabase Logflare (free tier: 5M events/mo)
├─ Cloudflare Worker logs (real-time, 72hr retention)
└─ Long-term: export to R2 bucket (monthly)
```

### Backup Strategy

```
Backup Strategy:

  Supabase Free:
  ├─ No automatic backups 😬
  └─ Manual: pg_dump via CLI weekly

  Supabase Pro ($25/mo):
  ├─ Daily automatic backups
  ├─ 7-day retention
  └─ Point-in-time recovery

  Additional (DIY):
  ├─ GitHub Actions: weekly pg_dump → R2 bucket
  ├─ Keep last 30 days
  └─ Test restore quarterly

  R2 Storage:
  ├─ Images are immutable — no backup needed
  └─ R2 has 11 9's durability
```

**Backup Script (for free tier):**

```yaml
# .github/workflows/backup.yml
name: Database Backup
on:
  schedule:
    - cron: '0 3 * * 0'  # Weekly Sunday 03:00 UTC

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Dump database
        run: |
          pg_dump $DATABASE_URL \
            --format=custom \
            --no-owner \
            --file=backup-$(date +%Y%m%d).dump
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Upload to R2
        run: |
          aws s3 cp backup-*.dump \
            s3://wainnrooh-backups/ \
            --endpoint-url $R2_ENDPOINT
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.R2_ACCESS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.R2_SECRET_KEY }}
          R2_ENDPOINT: ${{ secrets.R2_ENDPOINT }}
```

### Disaster Recovery

```
Disaster Scenarios:

  1. Database corruption:
     ├─ Restore from latest backup
     ├─ RTO: 30 minutes (Pro), 2 hours (Free)
     └─ RPO: 24 hours (daily backup)

  2. Supabase outage:
     ├─ Website still works (static on Cloudflare)
     ├─ iOS app uses local cache (SwiftData)
     ├─ API returns cached data from Cloudflare KV
     └─ Wait for Supabase recovery (99.9% SLA on Pro)

  3. Cloudflare outage (rare, global):
     ├─ Direct access to Supabase API (fallback URL)
     ├─ iOS app has hardcoded fallback
     └─ DNS failover (secondary provider)

  4. Data loss (accidental deletion):
     ├─ Supabase Pro: point-in-time recovery
     ├─ Free tier: restore from weekly backup
     └─ Soft-delete pattern: is_active = FALSE (not DELETE)

  5. Security breach:
     ├─ Rotate all API keys immediately
     ├─ Revoke all active sessions
     ├─ Review audit logs
     ├─ Notify users if data exposed
     └─ Post-incident review
```

Recovery Priorities:
  1. Authentication (users can't login)    → P0 (15 min)
  2. Read API (places, search)             → P1 (30 min)
  3. Write API (reviews, favorites)        → P2 (2 hours)
  4. Scraping & background jobs            → P3 (24 hours)
  5. Admin panel                           → P3 (24 hours)
```

---

## 11. التكاليف

### Phase 1: MVP (أول 3 شهور)

```
┌──────────────────────────────────────────────────┐
│              MVP Monthly Cost: $0-5               │
├──────────────────────────────────────────────────┤
│                                                  │
│  Supabase Free Tier:              $0             │
│  ├─ PostgreSQL 500MB                             │
│  ├─ Auth 50K users                               │
│  ├─ Storage 1GB                                  │
│  ├─ Edge Functions 500K invocations              │
│  ├─ Realtime 200 concurrent                      │
│  └─ 2GB bandwidth                                │
│                                                  │
│  Cloudflare Free:                 $0             │
│  ├─ CDN (unlimited bandwidth)                    │
│  ├─ Workers 100K requests/day                    │
│  ├─ KV 100K reads/day                            │
│  ├─ R2 10GB storage                              │
│  └─ DNS                                          │
│                                                  │
│  Domain (wainnrooh.com):          ~$12/year      │
│  ├─ ≈ $1/month                                   │
│                                                  │
│  OpenAI Embeddings (one-time):    $0.01          │
│  ├─ 3,202 places × 100 tokens                   │
│                                                  │
│  GitHub (free):                   $0             │
│  ├─ Repo + Actions 2000 min/month               │
│                                                  │
│  UptimeRobot (free):              $0             │
│  ├─ 50 monitors, 5-min intervals                │
│                                                  │
│  ─────────────────────────────────────           │
│  Total MVP:  ~$1/month ($3 for 3 months)         │
│  ─────────────────────────────────────           │
│                                                  │
│  ⚠️ Limits to watch:                             │
│  ├─ DB: 500MB (currently 2.8MB JSON → ~50MB SQL) │
│  ├─ Storage: 1GB (images will fill fast)          │
│  ├─ Bandwidth: 2GB (R2 has $0 egress)           │
│  └─ Edge Functions: 500K/month                   │
└──────────────────────────────────────────────────┘
```

### Phase 2: Growth (شهر 4-12)

```
┌──────────────────────────────────────────────────┐
│           Growth Monthly Cost: $45-75             │
├──────────────────────────────────────────────────┤
│                                                  │
│  Supabase Pro:                    $25/month      │
│  ├─ PostgreSQL 8GB                               │
│  ├─ Auth 100K users                              │
│  ├─ Storage 100GB                                │
│  ├─ 250GB bandwidth                              │
│  ├─ Daily backups                                │
│  ├─ 7-day log retention                          │
│  └─ Email support                                │
│                                                  │
│  Cloudflare Pro:                  $20/month      │
│  ├─ WAF + advanced security                      │
│  ├─ Image optimization                           │
│  ├─ Workers 10M requests/month                   │
│  └─ Better analytics                             │
│                                                  │
│  OR Cloudflare Free (stay):       $0             │
│  ├─ If traffic is still manageable               │
│                                                  │
│  Meilisearch Cloud:               $30/month      │
│  ├─ 100K documents                               │
│  ├─ Instant Arabic search                        │
│  └─ 10K searches/month                           │
│                                                  │
│  OR stay with PostgreSQL FTS:     $0             │
│  ├─ If search quality is acceptable              │
│                                                  │
│  OpenAI API (search):             $1-5/month     │
│  ├─ Semantic search queries                      │
│  ├─ ~50K queries/month × $0.0001                 │
│                                                  │
│  Twilio SMS (OTP):                $5-10/month    │
│  ├─ $0.05/SMS × 100-200 OTPs/month             │
│                                                  │
│  Domain:                          $1/month       │
│                                                  │
│  ─────────────────────────────────────           │
│  Total Growth (min):  $31/month                  │
│  Total Growth (max):  $76/month                  │
│  Recommended:         ~$50/month                 │
│  ─────────────────────────────────────           │
└──────────────────────────────────────────────────┘
```

### Phase 3: Scale (سنة 2+)

```
┌──────────────────────────────────────────────────┐
│            Scale Monthly Cost: $100-200           │
├──────────────────────────────────────────────────┤
│                                                  │
│  Supabase Pro + Compute:          $50-75/month   │
│  ├─ Larger compute instance                      │
│  ├─ Read replicas (if needed)                    │
│  ├─ Dedicated Postgres (optional)                │
│  └─ Priority support                             │
│                                                  │
│  Cloudflare Pro/Business:         $20-50/month   │
│  ├─ Advanced WAF rules                           │
│  ├─ Workers Paid (50M req/month)                 │
│  ├─ Durable Objects (if needed)                  │
│  └─ R2 paid tier                                 │
│                                                  │
│  Meilisearch Cloud (larger):      $50/month      │
│  ├─ 500K documents                               │
│  ├─ 100K searches/month                          │
│                                                  │
│  Upstash Redis:                   $10/month      │
│  ├─ Serverless Redis                             │
│  ├─ Session management                           │
│  └─ Rate limiting                                │
│                                                  │
│  OpenAI API:                      $10-20/month   │
│  ├─ Embeddings + NLP queries                     │
│  ├─ Smart summaries                              │
│                                                  │
│  Twilio SMS:                      $20-50/month   │
│  ├─ More users = more OTPs                       │
│                                                  │
│  Apple Developer:                 $8/month       │
│  ├─ $99/year for App Store                       │
│                                                  │
│  ─────────────────────────────────────           │
│  Total Scale (min):  $120/month                  │
│  Total Scale (max):  $250/month                  │
│  Recommended:        ~$150/month                 │
│  ─────────────────────────────────────           │
└──────────────────────────────────────────────────┘
```

### مقارنة التكاليف الشاملة

```
Cost Comparison Over Time:

  Month:   1    2    3    4    5    6    7    8    9   10   11   12
  ─────────────────────────────────────────────────────────────────
  
  Our Plan (Supabase + Cloudflare):
  $        1    1    1   31   31   31   50   50   50   50   50   50
  Total Year 1: ~$396

  Alternative A (AWS full stack):
  $       30   30   30   50   50   50   80   80   80  100  100  100
  Total Year 1: ~$780

  Alternative B (Vercel + PlanetScale):
  $       20   20   20   40   40   40   60   60   60   80   80   80
  Total Year 1: ~$600

  Alternative C (Railway):
  $        5    5    5   20   20   20   50   50   50   50   50   50
  Total Year 1: ~$375 (but fewer features)

  ═══════════════════════════════════════════════════════════════════
  Winner: Our Plan — best feature/cost ratio
  ═══════════════════════════════════════════════════════════════════
```

### One-Time Costs

```
One-Time Costs:

  Domain registration:       $12
  Apple Developer Account:   $99 (when ready for App Store)
  OpenAI initial indexing:   $0.01
  SSL Certificate:           $0 (Cloudflare provides free)
  
  Total one-time: ~$111
  (Apple Developer can wait until iOS app is ready)
```

---

## 12. Timeline

### متى نحتاج السيرفر فعلاً؟

```
Decision Tree:

  هل الموقع الحالي يخدم المستخدمين؟
  ├─ نعم → لا تتحرك. حسّن الـ static site.
  └─ لا، نحتاج:
      ├─ بحث أفضل؟           → Phase 1 (API + search)
      ├─ حسابات مستخدمين؟     → Phase 1 (Auth)
      ├─ iOS app؟              → Phase 1 (API required)
      ├─ تحديث أسعار تلقائي؟  → Phase 2 (scraping)
      ├─ AI features؟          → Phase 2 (embeddings)
      └─ آلاف المستخدمين؟     → Phase 3 (scale)

  ⚡ الجواب القصير:
  نحتاج السيرفر عند بناء iOS app أو إضافة حسابات مستخدمين.
  قبل كذا، الـ static site كافي مع تحسينات.
```

### مراحل الانتقال

```
═══════════════════════════════════════════════════════════════════
                     IMPLEMENTATION ROADMAP
═══════════════════════════════════════════════════════════════════

Phase 0: تحسين الوضع الحالي (أسبوع 1-2)
──────────────────────────────────────
  لا سيرفر! فقط تحسين الـ static site.
  
  □ Split places.json → paginated chunks (places-1.json, places-2.json)
  □ Lazy loading للبيانات (load on scroll)
  □ Service Worker for offline caching
  □ Image optimization (WebP, lazy load)
  □ Performance audit (Lighthouse > 90)
  
  التكلفة: $0
  الفائدة: تجربة مستخدم أفضل بدون backend

═══════════════════════════════════════════════════════════════════

Phase 1: MVP Backend (أسبوع 3-6)
──────────────────────────────────
  الأساسيات فقط.
  
  Week 3:
  □ Setup Supabase project
  □ Create database schema (tables + indexes)
  □ Migrate places.json → PostgreSQL
  □ Migrate delivery-prices.json
  □ Migrate prices files
  □ Setup RLS policies
  □ Test data integrity
  
  Week 4:
  □ Setup Cloudflare (DNS + CDN + R2)
  □ Create Cloudflare Worker (API proxy + cache)
  □ Setup image upload pipeline (R2)
  □ Deploy first Edge Function (search)
  □ API: GET /v1/places (list, filter, paginate)
  □ API: GET /v1/places/:id (detail)
  □ API: GET /v1/places/nearby (PostGIS)
  □ API: GET /v1/search (PostgreSQL FTS)
  
  Week 5:
  □ Setup Supabase Auth
  □ API: POST /v1/auth/* (signup, login, OTP)
  □ API: GET/POST /v1/users/me/favorites
  □ API: GET/POST /v1/places/:id/reviews
  □ RLS policies for user data
  □ Rate limiting via Cloudflare Worker
  
  Week 6:
  □ API: GET /v1/delivery/* (prices, compare)
  □ API: GET /v1/prices/:placeId
  □ OpenAPI spec generation
  □ API documentation (Swagger UI)
  □ Integration tests
  □ Security review
  □ Deploy to production
  
  Deliverable: Working API at api.wainnrooh.com
  التكلفة: $0 (free tier)

═══════════════════════════════════════════════════════════════════

Phase 2: iOS App Backend (أسبوع 7-10)
──────────────────────────────────────
  كل شي يحتاجه التطبيق.
  
  Week 7:
  □ Generate Swift client from OpenAPI
  □ Setup Supabase Swift SDK
  □ Implement offline sync (SwiftData)
  □ Test iOS ↔ API integration
  
  Week 8:
  □ Push notifications setup (APNs)
  □ Image CDN pipeline (R2 + Workers)
  □ Deep linking support
  □ Anonymous auth for browse-only
  
  Week 9:
  □ User lists (create, share)
  □ Report system (places, reviews)
  □ Search analytics logging
  □ Performance optimization (caching)
  
  Week 10:
  □ Load testing (k6 or Artillery)
  □ Security audit
  □ App Store preparation
  □ Production readiness review
  
  Deliverable: API ready for iOS app submission
  التكلفة: $0 (still free tier)

═══════════════════════════════════════════════════════════════════

Phase 3: Website Migration (أسبوع 11-14)
──────────────────────────────────────────
  تحويل الموقع من static إلى Astro SSG + API.
  
  Week 11-12:
  □ Setup Astro project
  □ Migrate 87 HTML pages → Astro components
  □ Pre-render place pages from API
  □ React islands for search + map
  □ Arabic RTL layout system
  
  Week 13-14:
  □ Client-side auth (Supabase JS)
  □ Favorites + reviews on website
  □ Deploy to Cloudflare Pages
  □ Redirect old URLs (301)
  □ SEO validation (sitemap, meta tags)
  
  Deliverable: Modern website on wainnrooh.com
  التكلفة: $0

═══════════════════════════════════════════════════════════════════

Phase 4: Intelligence (أسبوع 15-20)
──────────────────────────────────────
  AI + scraping + advanced features.
  
  Week 15-16:
  □ Setup Meilisearch Cloud (or stay with PG FTS)
  □ Arabic search optimization
  □ Autocomplete / suggest
  □ Search analytics dashboard
  
  Week 17-18:
  □ Delivery price scraping (cron jobs)
  □ Menu price scraping
  □ Data validation pipeline
  □ Admin panel for data review
  
  Week 19-20:
  □ Embeddings pipeline (pgvector)
  □ Semantic search ("مكان هادي للدراسة")
  □ Basic recommendations
  □ AI-generated place summaries
  
  Deliverable: Smart search + auto-updated prices
  التكلفة: $25-50/month (Supabase Pro)

═══════════════════════════════════════════════════════════════════

Phase 5: Scale (شهر 6+)
──────────────────────────────────────
  حسب النمو والحاجة.
  
  □ Collaborative filtering (1000+ users)
  □ Personalized notifications
  □ Real-time features (viewers, live reviews)
  □ Advanced analytics
  □ Multi-city expansion (جدة، الدمام)
  □ B2B API for partners
  □ Monetization features
  
  التكلفة: $100-200/month

═══════════════════════════════════════════════════════════════════
```

### ترتيب الأولويات

```
Priority Matrix:

  ┌──────────────────────┬─────────┬───────────┬──────────────┐
  │  Feature             │ Impact  │ Effort    │ Priority     │
  ├──────────────────────┼─────────┼───────────┼──────────────┤
  │  API + Database      │ ⭐⭐⭐⭐⭐ │ 2 weeks   │ 🔴 P0 (must) │
  │  Auth system         │ ⭐⭐⭐⭐  │ 1 week    │ 🔴 P0        │
  │  Basic search        │ ⭐⭐⭐⭐⭐ │ 3 days    │ 🔴 P0        │
  │  iOS API client      │ ⭐⭐⭐⭐⭐ │ 1 week    │ 🔴 P0        │
  │  Image CDN           │ ⭐⭐⭐⭐  │ 3 days    │ 🟡 P1        │
  │  Favorites/Reviews   │ ⭐⭐⭐⭐  │ 1 week    │ 🟡 P1        │
  │  Offline sync        │ ⭐⭐⭐   │ 1 week    │ 🟡 P1        │
  │  Delivery compare    │ ⭐⭐⭐⭐  │ 3 days    │ 🟡 P1        │
  │  Website migration   │ ⭐⭐⭐   │ 2 weeks   │ 🟢 P2        │
  │  Push notifications  │ ⭐⭐⭐   │ 3 days    │ 🟢 P2        │
  │  Meilisearch         │ ⭐⭐⭐   │ 3 days    │ 🟢 P2        │
  │  Price scraping      │ ⭐⭐⭐   │ 1 week    │ 🟢 P2        │
  │  Semantic search     │ ⭐⭐     │ 1 week    │ 🔵 P3        │
  │  Recommendations     │ ⭐⭐     │ 2 weeks   │ 🔵 P3        │
  │  AI summaries        │ ⭐⭐     │ 1 week    │ 🔵 P3        │
  │  Real-time features  │ ⭐      │ 1 week    │ 🔵 P3        │
  │  Multi-city          │ ⭐⭐⭐   │ 2 weeks   │ 🔵 P3        │
  └──────────────────────┴─────────┴───────────┴──────────────┘
```

---

## ملخص القرارات النهائية

```
═══════════════════════════════════════════════════════════════
                    DECISION SUMMARY
═══════════════════════════════════════════════════════════════

  Cloud:        Supabase (primary) + Cloudflare (edge/CDN)
  Database:     PostgreSQL 15 + PostGIS 3.4 (Supabase)
  Auth:         Supabase Auth (Phone OTP + Apple Sign-In)
  API:          Supabase Auto API + Edge Functions (Deno/TS)
  Cache:        Cloudflare KV → Upstash Redis (later)
  Search:       PostgreSQL FTS → Meilisearch Cloud (later)
  Storage:      Cloudflare R2 ($0 egress!)
  CDN:          Cloudflare (free)
  Website:      Astro SSG → Next.js (later)
  iOS:          Supabase Swift SDK + SwiftData (offline)
  AI:           OpenAI embeddings + pgvector
  Scraping:     Edge Functions + pg_cron
  CI/CD:        GitHub Actions
  Monitoring:   Supabase Dashboard + UptimeRobot
  
  MVP Cost:     ~$1/month
  Year 1 Total: ~$396
  
  Start:        When iOS app development begins
  Timeline:     6 weeks to production-ready API

═══════════════════════════════════════════════════════════════
```

---

> **آخر تحديث:** 2026-02-20
> **الإصدار:** 1.0
> **الحالة:** Draft — يحتاج مراجعة من الفريق