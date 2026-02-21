# iOS Ready Checklist — وين نروح بالرياض
**Version:** 1.0 | **Date:** 2026-02-21 | **Status:** Pre-Development Audit

---

## Executive Summary

هذا الـ checklist يغطي **كل شي** لازم يكون جاهز قبل ما نبدأ بناء iOS app. مقسم إلى 12 قسم رئيسي مع نسب اكتمال ومسؤوليات واضحة.

**الجاهزية الحالية: ~62%** — MVP ممكن يبدأ فوراً، لكن فيه gaps لازم تُسد.

---

## 📊 Overall Readiness Dashboard

| القسم | الجاهزية | الحالة | مطلوب قبل MVP |
|--------|----------|--------|:---:|
| 1. Data Readiness | 🟡 68% | أغلب الحقول موجودة، بعض الفجوات | ✅ |
| 2. Backend API | 🟢 85% | MVP = no backend needed (offline-first) | ❌ |
| 3. Design System | 🟡 55% | محتاج تأسيس | ✅ |
| 4. Assets | 🟡 50% | أيقونات + launch screen | ✅ |
| 5. Third-Party SDKs | 🟢 95% | MVP = zero dependencies | ❌ |
| 6. AI Integration | 🔴 20% | Phase 3 | ❌ |
| 7. Caching Strategy | 🟢 90% | مصمم بالتفصيل | ✅ |
| 8. Offline Support | 🟢 90% | Core architecture decision | ✅ |
| 9. Push Notifications | 🔴 10% | Phase 3 | ❌ |
| 10. Analytics | 🟡 40% | محتاج خطة | ❌ |
| 11. App Store | 🟡 45% | screenshots + description + privacy | ✅ |
| 12. Testing | 🟡 50% | محتاج test plan | ✅ |

---

## 1. 📦 Data Readiness

### 1.1 Field Completeness Audit

**المصدر:** `places.json` (6,445 مكان)

| الحقل | موجود | % مكتمل | الأهمية | ملاحظات |
|-------|:------:|--------:|---------|---------|
| `id` | ✅ | 100% | Critical | unique identifier |
| `name_ar` (الاسم بالعربي) | ✅ | 100% | Critical | — |
| `name_en` (الاسم بالإنجليزي) | ✅ | ~75% | High | بعض الأماكن عربي فقط |
| `category` | ✅ | 100% | Critical | 25 فئة |
| `category_ar` | ✅ | 100% | Critical | — |
| `neighborhood` | ✅ | ~90% | High | بعض الأماكن بدون حي |
| `neighborhood_en` | ✅ | ~70% | Medium | — |
| `description_ar` | ✅ | ~60% | Medium | فيه أماكن بدون وصف |
| `google_rating` | ✅ | ~85% | High | بعض الأماكن بدون تقييم |
| `review_count` | ⚠️ | ~50% | Medium | مو كل الأماكن |
| `price_range` | ⚠️ | ~40% | Medium | محتاج enrichment |
| `latitude` | ✅ | ~80% | Critical | بعض الأماكن بدون إحداثيات |
| `longitude` | ✅ | ~80% | Critical | نفس الملاحظة |
| `google_maps_url` | ✅ | ~85% | High | — |
| `phone` | ⚠️ | ~45% | Medium | كثير ناقص |
| `website` | ⚠️ | ~35% | Low | — |
| `instagram` | ⚠️ | ~40% | Medium | مهم بالسعودية |
| `hours` (ساعات العمل) | ⚠️ | ~30% | High | ⚠️ فجوة كبيرة |
| `address` | ⚠️ | ~50% | Medium | — |
| `cover_image_url` | ⚠️ | ~25% | High | ⚠️ محتاج صور |
| `tags` | ✅ | ~70% | Medium | — |
| `perfect_for` | ⚠️ | ~35% | Medium | — |
| `audience` | ⚠️ | ~30% | Low | — |
| `is_trending` | ✅ | 100% | Low | computed field |
| `is_new` | ✅ | 100% | Low | computed field |
| `is_free` | ⚠️ | ~20% | Low | — |

### 1.2 Data Quality Score

```
Data Quality Score: 62/100
═════════════════════════

Critical Fields (must be 95%+):
  ✅ id:           100%  ████████████████████ 
  ✅ name_ar:      100%  ████████████████████
  ✅ category:     100%  ████████████████████
  ⚠️ latitude:      80%  ████████████████░░░░
  ⚠️ longitude:     80%  ████████████████░░░░

High Priority Fields (should be 70%+):
  ✅ google_rating:  85%  █████████████████░░░
  ✅ google_maps_url:85%  █████████████████░░░
  ⚠️ neighborhood:   90%  ██████████████████░░
  ⚠️ name_en:        75%  ███████████████░░░░░
  ⚠️ description_ar: 60%  ████████████░░░░░░░░
  ⚠️ hours:          30%  ██████░░░░░░░░░░░░░░ ← Priority fix
  ⚠️ cover_image:    25%  █████░░░░░░░░░░░░░░░ ← Priority fix

Medium Priority:
  ⚠️ phone:          45%  █████████░░░░░░░░░░░
  ⚠️ instagram:      40%  ████████░░░░░░░░░░░░
  ⚠️ price_range:    40%  ████████░░░░░░░░░░░░
```

### 1.3 Data Gaps — Action Plan

| الفجوة | الأثر | الحل | الأولوية | الجهد |
|--------|-------|------|----------|-------|
| ساعات العمل 30% | المستخدم ما يعرف لو مفتوح | Google Places API batch | 🔴 عالي | 4h script |
| صور الغلاف 25% | تجربة بصرية ضعيفة | Google Places photos + Unsplash fallback | 🔴 عالي | 6h |
| إحداثيات 80% | 20% ما يظهرون بالخريطة | Google Geocoding API | 🟡 متوسط | 2h |
| هاتف 45% | ما يقدر يتصل | Google Places API | 🟡 متوسط | 2h |
| وصف عربي 60% | صفحة مكان فارغة | AI generation (GPT) | 🟡 متوسط | 4h |
| سعر 40% | ما يقدر يقارن | Manual + scraping | 🟡 متوسط | 8h |

### 1.4 Checklist — Data

- [ ] ✅ places.json validated (no broken JSON)
- [ ] ✅ All 6,445 places have unique IDs
- [ ] ✅ All categories mapped to Arabic names
- [ ] ⚠️ Fill lat/lng for remaining 20% (~1,290 places)
- [ ] ⚠️ Add operating hours for at least top 500 places
- [ ] ⚠️ Add cover images for at least top 500 places
- [ ] ⚠️ Verify phone numbers format (+966...)
- [ ] ⚠️ Normalize price ranges (consistent format)
- [ ] ✅ Bundle places.json in Xcode project
- [ ] ⚠️ Create data validation script

---

## 2. 🔌 Backend API Endpoints

### 2.1 MVP — No Backend Required ✅

```
MVP Strategy: OFFLINE-FIRST
════════════════════════════

Data Source:    Bundled places.json → SwiftData (SQLite)
Sync Source:    GitHub raw URL (ETag-based)
Auth:           None (local favorites)
Images:         External URLs (Google, Instagram)
Search:         Local FTS (in-app)
Maps:           MapKit (free, no API key)

Backend needed: ❌ NOT for MVP
Cost:           $0/month
```

### 2.2 Phase 2 — Minimal Backend

| Endpoint | Method | Purpose | Priority |
|----------|--------|---------|----------|
| `GET /api/places` | GET | Paginated places | Phase 2 |
| `GET /api/places/:id` | GET | Single place detail | Phase 2 |
| `GET /api/places/search` | GET | Server-side search | Phase 2 |
| `GET /api/places/nearby` | GET | Nearby by coordinates | Phase 2 |
| `GET /api/sync/delta` | GET | Changes since timestamp | Phase 2 |
| `GET /api/delivery/:placeId` | GET | Delivery prices | Phase 2 |
| `GET /api/rankings/:neighborhood` | GET | Top 10 by area | Phase 2 |

### 2.3 Phase 3 — Full Backend

| Endpoint | Method | Purpose | Priority |
|----------|--------|---------|----------|
| `POST /api/auth/otp/send` | POST | Send OTP (phone) | Phase 3 |
| `POST /api/auth/otp/verify` | POST | Verify OTP | Phase 3 |
| `GET /api/users/me` | GET | User profile | Phase 3 |
| `POST /api/reviews` | POST | Submit review | Phase 3 |
| `POST /api/checkins` | POST | Check-in | Phase 3 |
| `GET /api/badges` | GET | User badges | Phase 3 |
| `POST /api/favorites/sync` | POST | Sync favorites | Phase 3 |
| `POST /api/collections` | POST | Create collection | Phase 3 |
| `GET /api/ai/search` | GET | Semantic search | Phase 3 |
| `GET /api/ai/recommend` | GET | Personalized recs | Phase 3 |
| `POST /api/media/upload` | POST | Photo upload | Phase 3 |

### 2.4 Checklist — Backend

- [x] ✅ MVP works without backend
- [x] ✅ GitHub raw URL for data sync
- [x] ✅ ETag support on GitHub (automatic)
- [ ] ⚠️ Supabase project created (Phase 2)
- [ ] ⚠️ Database schema ready (see DATABASE-DESIGN.md)
- [ ] ⚠️ Row Level Security (RLS) policies defined
- [ ] ⚠️ API rate limiting configured
- [ ] ⚠️ CDN for images (Cloudflare R2)

---

## 3. 🎨 Design System

### 3.1 Colors

```swift
// Theme.swift — Saudi-inspired color palette
extension Color {
    // Primary
    static let wainPrimary = Color(hex: "#1B5E20")      // أخضر سعودي غامق
    static let wainSecondary = Color(hex: "#4CAF50")     // أخضر فاتح
    static let wainAccent = Color(hex: "#FFD600")        // ذهبي
    
    // Backgrounds
    static let wainBackground = Color(.systemBackground)
    static let wainSurface = Color(.secondarySystemBackground)
    static let wainCard = Color(.tertiarySystemBackground)
    
    // Text
    static let wainTextPrimary = Color(.label)
    static let wainTextSecondary = Color(.secondaryLabel)
    
    // Status
    static let wainOpen = Color.green
    static let wainClosed = Color.red
    static let wainTrending = Color.orange
    static let wainNew = Color.blue
    
    // Category Colors
    static let wainCafe = Color.brown
    static let wainRestaurant = Color.orange
    static let wainDessert = Color.pink
    static let wainEntertainment = Color.purple
    static let wainShopping = Color.teal
}
```

### 3.2 Typography

```swift
// Typography System
extension Font {
    // Arabic-optimized (2025-2026 best practice)
    static let wainLargeTitle = Font.system(size: 28, weight: .bold, design: .rounded)
    static let wainTitle = Font.system(size: 22, weight: .bold, design: .rounded)
    static let wainTitle2 = Font.system(size: 20, weight: .semibold, design: .rounded)
    static let wainHeadline = Font.system(size: 17, weight: .semibold)
    static let wainBody = Font.system(size: 15, weight: .regular)
    static let wainCallout = Font.system(size: 14, weight: .regular)
    static let wainCaption = Font.system(size: 12, weight: .regular)
    static let wainCaption2 = Font.system(size: 11, weight: .regular)
    
    // Note: iOS system Arabic font (SF Arabic) is excellent
    // No need for custom Arabic font in MVP
    // Phase 2: Consider "IBM Plex Arabic" or "Noto Sans Arabic" if needed
}
```

### 3.3 Components Library

| Component | Status | Description |
|-----------|--------|-------------|
| `PlaceCard` | 🟡 Design needed | بطاقة المكان (list + grid variants) |
| `CategoryCard` | 🟡 Design needed | بطاقة الفئة (icon + name + count) |
| `PillButton` | 🟡 Design needed | زر كبسولي (filter chips) |
| `RatingView` | 🟡 Design needed | عرض التقييم (stars + number) |
| `OpenStatusBadge` | 🟡 Design needed | مفتوح/مغلق badge |
| `PriceRangeBadge` | 🟡 Design needed | مستوى الأسعار |
| `TagBadge` | 🟡 Design needed | جديد، رائج، مجاني |
| `ShimmerView` | 🟡 Design needed | Loading placeholder |
| `EmptyStateView` | 🟡 Design needed | لا نتائج، لا مفضلة |
| `ErrorView` | 🟡 Design needed | خطأ بالتحميل |
| `SearchBar` | 🟡 Design needed | شريط البحث العربي |
| `MapPin` | 🟡 Design needed | دبوس الخريطة المخصص |
| `BottomSheet` | 🟡 Design needed | Sheet سفلي (iOS native) |
| `NavigationButton` | 🟡 Design needed | زر التوجيه (Google Maps) |

### 3.4 Spacing & Layout

```swift
// Spacing System (8-point grid)
enum Spacing {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 12
    static let lg: CGFloat = 16
    static let xl: CGFloat = 24
    static let xxl: CGFloat = 32
    static let xxxl: CGFloat = 48
}

// Corner Radius
enum CornerRadius {
    static let small: CGFloat = 8
    static let medium: CGFloat = 12
    static let large: CGFloat = 16
    static let pill: CGFloat = 999
}
```

### 3.5 Checklist — Design

- [ ] ⚠️ Final color palette approved
- [ ] ⚠️ Typography scale tested on device
- [ ] ⚠️ All 14 components designed (Figma/code)
- [ ] ⚠️ Dark mode variants for all colors
- [ ] ⚠️ RTL layout guidelines documented
- [ ] ⚠️ Animation guidelines (duration, easing)
- [ ] ✅ 8-point spacing grid defined
- [ ] ⚠️ Accessibility contrast ratios verified (WCAG AA)
- [x] ✅ System font decision (SF Arabic = good enough)
- [ ] ⚠️ Icon style guide (SF Symbols + custom)

---

## 4. 🖼️ Asset Requirements

### 4.1 App Icon

| Item | Size | Status | Notes |
|------|------|--------|-------|
| App Icon (1024×1024) | 1024px | ⚠️ Needed | مطلوب لـ App Store |
| Icon variants | Multiple | Auto-generated | Xcode generates from 1024 |
| Settings icon | 29pt @3x | Auto-generated | — |
| Spotlight icon | 40pt @3x | Auto-generated | — |
| Home screen | 60pt @3x | Auto-generated | — |

**Icon Design Direction:**
- 🟢 أخضر سعودي + 📍 دبوس مكان
- بسيط، يتعرف عليه بسهولة
- يشتغل على خلفيات فاتحة وغامقة

### 4.2 Launch Screen

| Item | Status | Notes |
|------|--------|-------|
| Launch storyboard OR SwiftUI | ⚠️ Needed | Logo + brand color |
| Animation (optional) | 🟡 Phase 2 | Lottie or native |

### 4.3 Images & Illustrations

| Asset | Quantity | Status | Source |
|-------|----------|--------|--------|
| Category icons (SF Symbols) | 25 | ✅ Available | SF Symbols 5+ |
| Custom category icons (optional) | 25 | 🟡 Phase 2 | Design |
| Empty state illustrations | 5 | ⚠️ Needed | undraw.co / custom |
| Onboarding screens | 3 | 🟡 Phase 2 | Design |
| Map pin variants | 25 | ⚠️ Needed | Per category |
| Error illustrations | 3 | ⚠️ Needed | Design |
| Placeholder image (place) | 1 | ⚠️ Needed | Design |

### 4.4 Animations

| Animation | Type | Priority | Status |
|-----------|------|----------|--------|
| Tab switching | SwiftUI transition | MVP | Built-in |
| Card tap | Scale + haptic | MVP | Code |
| Pull to refresh | Custom | Phase 2 | Code |
| Map pin drop | MapKit | MVP | Built-in |
| Shimmer loading | Custom | MVP | Code |
| Badge unlock | Lottie | Phase 2 | Design |
| Check-in success | Lottie | Phase 2 | Design |

### 4.5 Checklist — Assets

- [ ] ⚠️ App icon designed (1024×1024 PNG)
- [ ] ⚠️ Launch screen implemented
- [ ] ✅ SF Symbols selected for 25 categories
- [ ] ⚠️ Empty state illustrations (5)
- [ ] ⚠️ Placeholder image for places without photos
- [ ] ⚠️ Error state illustrations (3)
- [ ] ⚠️ Custom map pins per category (25)
- [ ] ✅ Assets.xcassets structure created
- [ ] ⚠️ App Store preview images (see section 11)

---

## 5. 📱 Third-Party SDKs

### 5.1 MVP — Zero External Dependencies ✅

```
MVP Dependency Count: 0
═══════════════════════

All Apple frameworks:
✅ SwiftUI      — UI
✅ SwiftData    — Persistence
✅ MapKit       — Maps
✅ CoreLocation — GPS
✅ Foundation   — Networking, JSON

Package Manager: Swift Package Manager (SPM)
CocoaPods: NOT used
Carthage: NOT used
```

### 5.2 Phase 2 SDKs

| SDK | Purpose | Size Impact | License | Status |
|-----|---------|-------------|---------|--------|
| `Kingfisher` | Image caching & loading | +2 MB | MIT | Evaluate vs AsyncImage |
| `PostHog` (iOS SDK) | Analytics | +1 MB | MIT | Free tier: 1M events/mo |
| `Sentry` (iOS SDK) | Crash reporting | +2 MB | BSD | Free tier: 5K errors/mo |

### 5.3 Phase 3 SDKs

| SDK | Purpose | Size Impact | License | Status |
|-----|---------|-------------|---------|--------|
| `supabase-swift` | Backend (auth, db, storage) | +3 MB | MIT | Official SDK |
| `Mixpanel` OR `PostHog` | Advanced analytics | +1 MB | Varies | Choose one |
| `Lottie` | Animations (badges, etc.) | +2 MB | Apache 2.0 | Optional |
| `Firebase Messaging` | Push notifications (fallback) | +5 MB | Apache 2.0 | Consider APNs-only first |

### 5.4 SDKs We're NOT Using (and why)

| SDK | Why NOT |
|-----|---------|
| Google Maps SDK | +20 MB, MapKit is free & native |
| Alamofire | URLSession is sufficient |
| Realm | SwiftData is Apple-native |
| Firebase Auth | Supabase is cheaper |
| Google Analytics | Privacy concerns, PostHog better |
| Facebook SDK | Not needed, privacy nightmare |

### 5.5 Checklist — SDKs

- [x] ✅ MVP uses zero external dependencies
- [x] ✅ SPM chosen as package manager
- [ ] ⚠️ Evaluate Kingfisher vs built-in AsyncImage (Phase 2)
- [ ] ⚠️ PostHog account created (Phase 2)
- [ ] ⚠️ Sentry account created (Phase 2)
- [ ] ⚠️ Supabase project setup (Phase 3)
- [x] ✅ No privacy-invasive SDKs (Facebook, Google Analytics)

---

## 6. 🤖 AI Integration Plan

### 6.1 Phases

```
Phase 1 (MVP):  ❌ No AI — purely data-driven
Phase 2:        🟡 Basic AI — auto-descriptions, smart search
Phase 3:        🟢 Full AI — chatbot, recommendations, summaries
```

### 6.2 Phase 2: AI Features

| Feature | Model | Integration | Cost |
|---------|-------|-------------|------|
| Auto-generate Arabic descriptions | GPT-4 / Claude | Batch job (offline) | ~$5 one-time |
| Smart search synonyms | Embeddings | On-device or batch | ~$2 one-time |
| Tag generation | GPT-4 / Claude | Batch job | ~$3 one-time |

### 6.3 Phase 3: AI Chatbot Inside App

```
User: "وش أفضل مكان رومانسي هادي قريب مني؟"

AI → Understands: {intent: "recommend", mood: "romantic", 
                   attribute: "quiet", location: "nearby"}
   → Searches: places.filter(perfectFor: "رومانسي", tags: "هادي")
              .sort(distance from user)
   → Returns: Top 3 matches with explanation

Implementation Options (2025-2026):
├── Option A: Apple Intelligence (on-device, free, iOS 18.4+)
│   ✅ Free, private, fast
│   ❌ Limited capabilities, not all devices
│
├── Option B: Supabase Edge Functions + OpenAI
│   ✅ Powerful, flexible
│   ❌ Needs internet, cost per query
│
├── Option C: Local embeddings (ONNX Runtime)
│   ✅ Offline, fast, free
│   ❌ Complex setup, limited to semantic search
│
└── Recommended: Start with B, migrate to A when available
```

### 6.4 Checklist — AI

- [ ] 🔴 No AI in MVP (intentional)
- [ ] ⚠️ Generate descriptions for 60% missing (batch GPT)
- [ ] ⚠️ Generate tags for places missing tags
- [ ] ⚠️ Choose AI backend for Phase 3
- [ ] ⚠️ Design chatbot UI (floating button)
- [ ] ⚠️ Define semantic search queries (Arabic)
- [ ] ⚠️ Apple Intelligence integration research

---

## 7. 💾 Caching Strategy

### 7.1 Multi-Layer Cache Architecture

```
┌──────────────────────────────────────────────┐
│              Caching Layers                    │
│                                               │
│  Layer 1: App Bundle (places.json)            │
│  ├── Size: ~5 MB (compressed)                 │
│  ├── TTL: Ship-time snapshot                  │
│  ├── Used: First launch fallback              │
│  └── Update: Every app update                 │
│                                               │
│  Layer 2: SwiftData (SQLite)                  │
│  ├── Size: ~8 MB                              │
│  ├── TTL: Persistent (updated via sync)       │
│  ├── Used: Primary data source                │
│  └── Queries: FetchDescriptor + Predicate     │
│                                               │
│  Layer 3: URLCache (HTTP responses)           │
│  ├── Size: 50 MB max (configurable)           │
│  ├── TTL: HTTP Cache-Control headers          │
│  ├── Used: Image caching                      │
│  └── Policy: LRU eviction                     │
│                                               │
│  Layer 4: In-Memory (NSCache)                 │
│  ├── Size: ~20 MB max                         │
│  ├── TTL: App session                         │
│  ├── Used: Decoded images, computed results   │
│  └── Policy: Auto-evict on memory pressure    │
│                                               │
│  Layer 5: UserDefaults                        │
│  ├── Size: < 100 KB                           │
│  ├── TTL: Permanent                           │
│  ├── Used: Settings, recent searches, ETag    │
│  └── Policy: Manual cleanup                   │
└──────────────────────────────────────────────┘
```

### 7.2 Cache Invalidation Strategy

```swift
// CachePolicy.swift
enum CachePolicy {
    /// Sync check intervals
    static let minSyncInterval: TimeInterval = 4 * 60 * 60    // 4 hours
    static let backgroundRefresh: TimeInterval = 12 * 60 * 60  // 12 hours
    
    /// Image cache
    static let imageCacheSize = 50 * 1024 * 1024               // 50 MB
    static let imageTTL: TimeInterval = 7 * 24 * 60 * 60       // 7 days
    
    /// Search cache
    static let searchResultsCacheTTL: TimeInterval = 5 * 60    // 5 minutes
    static let maxCachedSearches = 20
    
    /// Data freshness
    static let staleDataThreshold: TimeInterval = 24 * 60 * 60 // 24 hours
}
```

### 7.3 Checklist — Caching

- [x] ✅ Multi-layer cache architecture designed
- [x] ✅ SwiftData as primary cache
- [x] ✅ Bundled JSON as fallback
- [x] ✅ ETag-based sync (no unnecessary downloads)
- [x] ✅ URLCache for images (50 MB)
- [ ] ⚠️ Implement cache size monitoring
- [ ] ⚠️ Add "Clear Cache" in settings
- [ ] ⚠️ Test cache behavior under memory pressure
- [x] ✅ Background refresh configured (BGAppRefreshTask)

---

## 8. 📴 Offline Support Plan

### 8.1 Offline Capabilities Matrix

| Feature | Online | Offline | Notes |
|---------|:------:|:-------:|-------|
| Browse places | ✅ | ✅ | SwiftData cache |
| Search | ✅ | ✅ | Local FTS |
| View place detail | ✅ | ✅ | Cached data |
| Map view | ✅ | ⚠️ | MapKit tiles need internet first time, then cached |
| View place photos | ✅ | ⚠️ | Only if previously loaded |
| Favorites (save/remove) | ✅ | ✅ | Local SwiftData |
| Open in Google Maps | ✅ | ❌ | Needs external app + internet |
| Share place | ✅ | ✅ | Generates local text |
| Data sync | ✅ | ❌ | Queued, syncs when online |
| Check-in (Phase 2) | ✅ | ⚠️ | Queued, verified when online |

### 8.2 Offline-First Data Flow

```
┌──────────────────────────────────────────┐
│           Offline-First Flow              │
│                                           │
│  1. App opens → Read from SwiftData       │
│     └── Instant (< 50ms)                  │
│                                           │
│  2. Check network availability            │
│     ├── Online: Background sync check     │
│     │   └── HEAD request with ETag        │
│     │       ├── 304: Data is fresh ✅      │
│     │       └── 200: Download + merge     │
│     │                                     │
│     └── Offline: Show cached data ✅       │
│         └── Show "آخر تحديث: ..." banner  │
│                                           │
│  3. User actions while offline:           │
│     ├── Favorites: Save locally           │
│     ├── Check-ins: Queue for sync         │
│     └── All reads: From local cache       │
│                                           │
│  4. When back online:                     │
│     ├── Sync queued actions               │
│     ├── Download data updates             │
│     └── Refresh expired image cache       │
└──────────────────────────────────────────┘
```

### 8.3 Network Monitor

```swift
// NetworkMonitor.swift
import Network

@Observable
class NetworkMonitor {
    private let monitor = NWPathMonitor()
    var isConnected = true
    var connectionType: ConnectionType = .unknown
    
    enum ConnectionType {
        case wifi, cellular, unknown
    }
    
    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in
                self?.isConnected = path.status == .satisfied
                if path.usesInterfaceType(.wifi) {
                    self?.connectionType = .wifi
                } else if path.usesInterfaceType(.cellular) {
                    self?.connectionType = .cellular
                }
            }
        }
        monitor.start(queue: .global())
    }
}
```

### 8.4 Checklist — Offline

- [x] ✅ Offline-first architecture chosen
- [x] ✅ Bundled JSON for zero-network first launch
- [x] ✅ SwiftData persistent storage
- [x] ✅ ETag-based delta sync
- [ ] ⚠️ Network monitor implementation
- [ ] ⚠️ "آخر تحديث" banner for stale data
- [ ] ⚠️ Queue offline actions (check-ins, etc.)
- [ ] ⚠️ MapKit tile caching behavior tested
- [ ] ⚠️ Airplane mode full test pass

---

## 9. 🔔 Push Notifications Plan

### 9.1 Phase Timeline

```
MVP:     ❌ No push notifications
Phase 2: 🟡 Local notifications only
Phase 3: 🟢 Remote push (APNs)
```

### 9.2 Local Notifications (Phase 2)

| Trigger | Content | Example |
|---------|---------|---------|
| Geofence entry | "أنت قريب من [مكان]!" | Near a saved place |
| Data update | "تمت إضافة 15 مكان جديد!" | After sync |
| Weekly digest | "اكتشف أفضل الأماكن هالأسبوع" | Every Sunday |

### 9.3 Remote Push (Phase 3)

| Type | Content | Frequency |
|------|---------|-----------|
| New trending places | "🔥 [مكان] صار ترند!" | 1-2/week |
| New places in your area | "📍 3 أماكن جديدة في [حي]" | 1/week |
| Badge earned | "🏅 حصلت على شارة [اسم]!" | On achievement |
| Mayor lost | "👑 [شخص] صار عمدة [مكان] بدالك!" | Real-time |
| Seasonal | "🎄 أفضل أماكن موسم الرياض" | Seasonal |

### 9.4 Implementation

```
APNs (Apple Push Notification service)
├── Provider: Supabase Edge Functions → APNs
├── Token: Device token stored in Supabase
├── Certificate: APNs key (.p8) in Supabase secrets
├── Topics: com.wainnrooh.app
└── Silent push: For background data refresh
```

### 9.5 Checklist — Push

- [ ] 🔴 Not needed for MVP
- [ ] ⚠️ APNs certificate generated (Apple Developer Portal)
- [ ] ⚠️ UNUserNotificationCenter permission flow
- [ ] ⚠️ Notification categories defined
- [ ] ⚠️ Geofence monitoring setup (CoreLocation)
- [ ] ⚠️ Supabase push integration (Phase 3)
- [ ] ⚠️ Rate limiting (max 3/day)
- [ ] ⚠️ User preferences (which notifications)

---

## 10. 📈 Analytics Plan

### 10.1 What to Track

```
Core Metrics (2025/2026 best practices):
═══════════════════════════════════════

Acquisition:
├── First launch date
├── Source (organic, share, QR)
└── Onboarding completion rate

Engagement:
├── DAU / WAU / MAU
├── Session length
├── Session frequency
├── Screens per session
├── Search queries (anonymized)
├── Categories browsed
├── Places viewed
├── Map interactions
└── Share actions

Retention:
├── Day 1 / Day 7 / Day 30 retention
├── Churn indicators
└── Re-engagement success

Feature Usage:
├── Search usage rate
├── Map view usage rate
├── Favorites count per user
├── Filter usage
├── Navigation (open in maps) rate
└── Check-in frequency (Phase 2)

Performance:
├── App launch time
├── Crash rate
├── Search latency
├── Memory usage peaks
└── Network request failures
```

### 10.2 Analytics Stack

```
MVP:    Privacy-first local analytics
        └── Custom logging to local file
            (aggregate, no PII)

Phase 2: PostHog (self-hosted option available)
         ├── Free tier: 1M events/month
         ├── Session replay (optional)
         ├── Feature flags
         └── A/B testing

Phase 3: PostHog + custom dashboards
         ├── Supabase analytics tables
         ├── Real-time metrics
         └── AI-powered insights
```

### 10.3 Privacy-First Approach (2025/2026 Standard)

```swift
// AnalyticsService.swift — Privacy-First
class AnalyticsService {
    /// We track WHAT happens, not WHO does it
    /// No user IDs, no device IDs, no IP addresses
    
    func trackEvent(_ event: AnalyticsEvent) {
        // Local aggregation only in MVP
        // Phase 2: Send to PostHog (anonymized)
    }
}

enum AnalyticsEvent {
    case appLaunched
    case searchPerformed(query: String) // Anonymized: just the query
    case placeViewed(category: String, neighborhood: String)
    case favoriteToggled(action: String) // "add" or "remove"
    case mapOpened
    case navigateToMaps(category: String)
    case sharePlace(method: String) // "whatsapp", "copy", "other"
    case filterApplied(type: String) // "category", "price", "rating"
    case categoryBrowsed(category: String)
}
```

### 10.4 Checklist — Analytics

- [ ] ⚠️ Analytics events defined (see above)
- [ ] ⚠️ Privacy-first tracking implemented (no PII)
- [ ] ⚠️ Local analytics for MVP
- [ ] ⚠️ PostHog account setup (Phase 2)
- [ ] ⚠️ App Store privacy labels filled
- [ ] ⚠️ ATT (App Tracking Transparency) NOT needed (no tracking)
- [ ] ⚠️ GDPR/Saudi PDPL compliance verified
- [ ] ⚠️ Analytics dashboard created

---

## 11. 🍎 App Store Requirements

### 11.1 App Store Connect Metadata

| Field | Content (Draft) | Status |
|-------|-----------------|--------|
| **App Name** | وين نروح بالرياض | ✅ |
| **Subtitle** | اكتشف أفضل الأماكن في الرياض | ⚠️ Draft |
| **Category** | Travel (Primary), Food & Drink (Secondary) | ⚠️ Verify |
| **Bundle ID** | `com.wainnrooh.app` | ⚠️ Register |
| **SKU** | `wainnrooh-ios-001` | ⚠️ Set |
| **Price** | Free | ✅ |
| **Age Rating** | 4+ | ✅ |
| **Copyright** | © 2026 وين نروح | ⚠️ Set |

### 11.2 App Description

```
Arabic:
════════
🔍 وين نروح بالرياض؟

اكتشف أكثر من 6,000 مكان في الرياض — كافيهات، مطاعم، حلويات، 
ترفيه، وأكثر! كل شي تحتاجه عشان تلقى المكان المثالي.

✨ المميزات:
• تصفح 6,445+ مكان حسب الفئة أو الحي
• بحث ذكي بالعربي
• خريطة تفاعلية لكل الأماكن
• حفظ المفضلات
• يشتغل بدون إنترنت!
• توجّه مباشر عبر Google Maps

📍 25 فئة تشمل:
كافيهات • مطاعم • حلويات • بخاري • مشاوي • برقر 
آيسكريم • مخابز • عطور • ترفيه • تسوق • وأكثر

🏘️ يغطي جميع أحياء الرياض

مجاني بالكامل. بدون إعلانات. بدون تسجيل.

English:
════════
🔍 Where to go in Riyadh?

Discover 6,000+ places in Riyadh — cafes, restaurants, desserts, 
entertainment, and more! Everything you need to find the perfect spot.

✨ Features:
• Browse 6,445+ places by category or neighborhood
• Smart Arabic search
• Interactive map
• Save favorites
• Works offline!
• Navigate via Google Maps

Free. No ads. No registration required.
```

### 11.3 Keywords

```
Arabic: وين نروح, الرياض, كافيهات, مطاعم, أماكن, حلويات, ترفيه, خريطة
English: riyadh, places, cafes, restaurants, explore, map, saudi, food
```

### 11.4 Screenshots Required

| Device | Required | Dimensions | Count |
|--------|----------|------------|-------|
| iPhone 6.9" (15 Pro Max) | ✅ Required | 1320 × 2868 | 6-10 |
| iPhone 6.7" (14 Pro Max) | ✅ Required | 1290 × 2796 | 6-10 |
| iPhone 6.5" (11 Pro Max) | Recommended | 1242 × 2688 | 6-10 |
| iPhone 5.5" (8 Plus) | Optional | 1242 × 2208 | 6-10 |

**Screenshot Plan (10 screens):**
1. الصفحة الرئيسية (Home with categories)
2. تصفح فئة (Category list)
3. صفحة مكان (Place detail)
4. الخريطة (Map view with pins)
5. البحث (Search with results)
6. المفضلة (Favorites)
7. الأحياء (Neighborhoods)
8. مكان بالتفصيل (Place with hours, rating)
9. التنقل (Navigation button)
10. Offline mode banner

### 11.5 Privacy Policy

```
Required: YES (all apps must have one)

What we collect:    Nothing (MVP)
What we don't:      No accounts, no tracking, no personal data
Where to host:      GitHub Pages (wain-nrooh.com/privacy)

Privacy Labels (App Store Connect):
├── Data Not Collected ✅ (MVP)
├── No tracking ✅
├── No third-party sharing ✅
└── Offline-first ✅
```

### 11.6 App Review Compliance (2026 Guidelines)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Built with Xcode 15+ | ✅ | Using Xcode 16 |
| iOS 17 SDK minimum | ✅ | Target iOS 17+ |
| Not a web wrapper | ✅ | Native SwiftUI |
| Has meaningful native features | ✅ | Search, map, favorites |
| Privacy policy URL | ⚠️ | Need to create |
| App privacy labels accurate | ⚠️ | Need to fill |
| No placeholder content | ✅ | Real data |
| No crashes | ⚠️ | Need testing |
| Appropriate age rating | ✅ | 4+ |
| Account deletion (if accounts) | N/A | No accounts in MVP |

### 11.7 Checklist — App Store

- [ ] ⚠️ Apple Developer account active ($99/yr)
- [ ] ⚠️ Bundle ID registered (com.wainnrooh.app)
- [ ] ⚠️ App Store Connect app entry created
- [ ] ⚠️ App description written (Arabic + English)
- [ ] ⚠️ Keywords optimized
- [ ] ⚠️ 10 screenshots per device size (2 sizes minimum)
- [ ] ⚠️ Privacy policy page created & hosted
- [ ] ⚠️ Privacy labels filled in App Store Connect
- [ ] ⚠️ Age rating questionnaire completed
- [ ] ⚠️ Support URL provided
- [ ] ⚠️ Marketing URL (optional)
- [ ] ⚠️ TestFlight beta test (2+ weeks before submission)
- [ ] ⚠️ App icon passes App Store guidelines (no alpha)

---

## 12. 🧪 Testing Plan

### 12.1 Testing Strategy

```
Testing Pyramid (2025/2026 iOS Best Practices)
═══════════════════════════════════════════════

        ┌──────────┐
        │ UI Tests │  ← 10% (Xcode UI Testing)
        │  (few)   │    Critical user journeys only
        ├──────────┤
        │Integration│  ← 20% (XCTest)
        │  Tests   │    Repository + Service tests
        ├──────────┤
        │  Unit    │  ← 70% (XCTest + Swift Testing)
        │  Tests   │    ViewModels, Services, Models
        └──────────┘

Target Coverage: 80%+ for business logic
```

### 12.2 Unit Tests

| Area | Test Count (Est.) | Priority |
|------|-------------------|----------|
| Place model parsing | 10 | 🔴 Critical |
| Arabic search normalization | 15 | 🔴 Critical |
| Search service (FTS) | 10 | 🔴 Critical |
| Category filtering | 8 | 🔴 Critical |
| Favorite toggle logic | 5 | 🔴 Critical |
| Sync service (ETag) | 8 | 🟡 High |
| Distance calculation | 5 | 🟡 High |
| Hours parsing | 10 | 🟡 High |
| Price range parsing | 5 | 🟡 High |
| Rating calculation (Phase 3) | 12 | 🟢 Later |

### 12.3 Integration Tests

| Test | Description | Priority |
|------|-------------|----------|
| JSON → SwiftData | Parse full places.json → store | 🔴 Critical |
| SwiftData queries | Fetch, filter, sort, paginate | 🔴 Critical |
| Search end-to-end | Query → normalize → search → results | 🔴 Critical |
| Sync flow | Check ETag → download → merge | 🟡 High |
| Map data | Places with lat/lng render on map | 🟡 High |

### 12.4 UI Tests

| Journey | Steps | Priority |
|---------|-------|----------|
| Browse category | Home → tap category → see places → tap place | 🔴 Critical |
| Search | Home → search → type query → see results | 🔴 Critical |
| Favorite | Place detail → tap heart → go to favorites → see place | 🔴 Critical |
| Map view | Map tab → see pins → tap pin → see detail | 🟡 High |
| Navigation | Place detail → tap navigate → opens Maps | 🟡 High |

### 12.5 Arabic-Specific Tests

| Test | Input | Expected |
|------|-------|----------|
| Search with tashkeel | "مطعَم" | Same results as "مطعم" |
| Alef normalization | "أكل", "إكل", "آكل" | All match "اكل" |
| Ta marbuta | "قهوة" | Also matches "قهوه" |
| Mixed Arabic-English | "cafe كافيه" | Matches both |
| RTL layout | All screens | Text right-aligned, correct flow |
| Arabic numerals | "٤.٥" | Displays correctly |

### 12.6 Performance Tests

| Metric | Target | Tool |
|--------|--------|------|
| Cold launch | < 1.5s | Instruments (Time Profiler) |
| Warm launch | < 0.5s | Instruments |
| JSON parse (6,445 places) | < 2s | XCTest measure {} |
| Search query | < 50ms | XCTest measure {} |
| Category filter | < 20ms | XCTest measure {} |
| Scroll FPS | 60fps | Instruments (Core Animation) |
| Memory (browse) | < 100 MB | Instruments (Allocations) |
| Memory (map) | < 150 MB | Instruments (Allocations) |

### 12.7 Device Testing Matrix

| Device | iOS Version | Test |
|--------|-------------|------|
| iPhone 15 Pro Max | iOS 18+ | Primary |
| iPhone 14 | iOS 17 | Minimum target |
| iPhone SE 3 | iOS 17 | Small screen |
| iPhone 12 | iOS 17 | Older device perf |
| Simulator | iOS 17/18 | CI/CD |

### 12.8 Pre-Submission Checklist

- [ ] ⚠️ All unit tests passing
- [ ] ⚠️ All integration tests passing
- [ ] ⚠️ All UI tests passing
- [ ] ⚠️ Zero crashes in 48-hour soak test
- [ ] ⚠️ Airplane mode full functionality test
- [ ] ⚠️ Arabic text rendering verified on all screens
- [ ] ⚠️ RTL layout verified on all screens
- [ ] ⚠️ Dark mode verified on all screens
- [ ] ⚠️ Dynamic Type (accessibility text sizes) tested
- [ ] ⚠️ VoiceOver accessibility pass
- [ ] ⚠️ Memory leaks check (Instruments)
- [ ] ⚠️ Performance benchmarks met
- [ ] ⚠️ TestFlight 2-week beta (10+ testers)
- [ ] ⚠️ App size < 25 MB verified
- [ ] ⚠️ No force unwraps in production code
- [ ] ⚠️ No hardcoded strings (localization ready)
- [ ] ⚠️ Security review passed (no secrets in code)

---

## 📋 Master Checklist — Pre-Development Summary

### 🔴 MUST DO Before Starting MVP

- [ ] Validate places.json structure & quality
- [ ] Create Xcode project with correct settings
- [ ] Set up Design System (colors, fonts, spacing)
- [ ] Create app icon (1024×1024)
- [ ] Implement launch screen
- [ ] Create 5 empty state illustrations (or use SF Symbols placeholders)
- [ ] Register Bundle ID with Apple
- [ ] Set up Git repo with .gitignore
- [ ] Write basic unit test framework

### 🟡 SHOULD DO Before Phase 2

- [ ] Fill data gaps (hours, images, lat/lng for remaining 20%)
- [ ] Create Privacy Policy page
- [ ] Set up PostHog analytics
- [ ] Create App Store screenshots
- [ ] Write App Store description
- [ ] TestFlight distribution setup
- [ ] Supabase project created
- [ ] Design all 14 UI components

### 🟢 CAN DO Later (Phase 3)

- [ ] AI chatbot backend
- [ ] Push notification certificates
- [ ] User accounts system
- [ ] Advanced analytics dashboard
- [ ] Business portal (claim/edit listings)
- [ ] Moderation system

---

## ⏱️ Timeline to MVP Launch

```
Week 1: Setup + Data Layer (16h)
├── Day 1-2: Project setup, data validation, bundled JSON
├── Day 3-4: SwiftData models, Repository pattern
└── Day 5: Sync service, search service

Week 2: UI + Features (20h)
├── Day 1-2: Home screen, category browse
├── Day 3-4: Place detail, map view
└── Day 5: Favorites, search, sharing

Week 3: Polish + Test (12h)
├── Day 1-2: RTL polish, dark mode, empty states
├── Day 3: Unit tests, integration tests
└── Day 4-5: Bug fixes, performance optimization

Week 4: Beta + Submission (8h)
├── Day 1-2: TestFlight beta distribution
├── Day 3: App Store assets (screenshots, description)
├── Day 4: Final testing, privacy policy
└── Day 5: App Store submission

Total: ~56 hours → 4 weeks (part-time AI agent)
```

---

*Document generated: 2026-02-21 | Companion to: APP-FEATURES-BLUEPRINT.md, MVP-PLAN.md*
