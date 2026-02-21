# MVP Plan — وين نروح بالرياض (iOS)
**Version:** 1.0 | **Date:** 2026-02-21 | **Author:** iOS System Architect

---

## Executive Summary

التطبيق الحالي (46 Swift file) فيه 6 CRITICAL bugs ما يخليه يـ compile. القرار: **إعادة بناء جزئية (Surgical Rewrite)** — نحتفظ بالـ UI views ونعيد بناء الـ data layer من الصفر. الـ MVP يشتغل offline-first مع bundled JSON من GitHub Pages.

---

## 1. MVP Strategy

### 1.1 أبسط نسخة تشتغل وتفيد

**MVP = Browse + Search + Map + Favorites (offline)**

المستخدم يقدر:
1. يتصفح 6,445+ مكان حسب الفئة أو الحي
2. يبحث بالعربي (fuzzy search محلي)
3. يشوف الأماكن على الخريطة
4. يحفظ مفضلاته محلياً
5. يفتح المكان بـ Google Maps للتنقل
6. يتصفح **بدون إنترنت** بالكامل

### 1.2 MVP vs Later

| Feature | MVP (Phase 1) | Phase 2 | Phase 3 |
|---------|:---:|:---:|:---:|
| Browse by category | ✅ | | |
| Browse by neighborhood | ✅ | | |
| Arabic search (local FTS) | ✅ | | |
| Map view (MapKit) | ✅ | | |
| Place detail page | ✅ | | |
| Local favorites | ✅ | | |
| Offline browsing | ✅ | | |
| Open in Google Maps | ✅ | | |
| Share place | ✅ | | |
| Delivery price comparison | | ✅ | |
| Filters (price, rating, features) | | ✅ | |
| Auto-sync new places | | ✅ | |
| Push notifications (trending) | | | ✅ |
| User accounts (Supabase Auth) | | | ✅ |
| Reviews & ratings | | | ✅ |
| AI recommendations | | | ✅ |
| Perfume finder | | ✅ | |
| Photos gallery | | | ✅ |
| WhatsApp sharing | | ✅ | |

### 1.3 كيف ما يأثر على الموقع الحالي

```
┌────────────────────────┐     ┌─────────────────────┐
│   GitHub Pages (Web)   │     │    iOS App (MVP)     │
│   ─────────────────    │     │   ─────────────────  │
│   87 HTML pages        │     │   Bundled places.json│
│   places.json (source) │────►│   (downloaded at     │
│   JS/CSS/images        │     │    build time or     │
│   .github/workflows    │     │    first launch)     │
│                        │     │                      │
│   ⚠️ لا نغير شي هنا   │     │   SwiftData cache    │
│   الموقع يستمر كالعادة  │     │   Local favorites    │
└────────────────────────┘     └─────────────────────┘
```

**القاعدة:** الموقع = source of truth. التطبيق = consumer فقط. أي تغيير بالبيانات يصير على الموقع، والتطبيق يسحب.

---

## 2. Architecture

### 2.1 Pattern: MVVM + Repository Pattern

**ليش MVVM مو TCA؟**
- MVVM = الأنسب لـ SwiftUI (2025/2026 consensus)
- TCA = أقوى لكن overkill لـ MVP بهالحجم
- الكود الحالي بالفعل MVVM — نحتفظ بالـ pattern
- Repository pattern يفصل الـ data source عن الـ ViewModels

```
┌─────────────────────────────────────────────────────┐
│                    MVVM + Repository                 │
│                                                      │
│  ┌──────────┐    ┌──────────────┐    ┌────────────┐ │
│  │  Views   │───►│  ViewModels  │───►│ Repository │ │
│  │ (SwiftUI)│◄───│ (@Observable)│◄───│  Protocol  │ │
│  └──────────┘    └──────────────┘    └─────┬──────┘ │
│                                            │        │
│                              ┌─────────────┼─────┐  │
│                              │             │     │  │
│                         ┌────▼───┐   ┌─────▼──┐  │  │
│                         │ Local  │   │ Remote │  │  │
│                         │(Bundle │   │(GitHub │  │  │
│                         │ JSON + │   │ raw    │  │  │
│                         │SwiftData)  │ URL)   │  │  │
│                         └────────┘   └────────┘  │  │
│                                                  │  │
│                         ┌────────┐               │  │
│                         │Supabase│ (Phase 3)     │  │
│                         └────────┘               │  │
└─────────────────────────────────────────────────────┘
```

### 2.2 Data Flow: Offline-First

```
App Launch
    │
    ├── First Launch?
    │   ├── YES → Load bundled places.json from app bundle
    │   │         Parse → Store in SwiftData
    │   │         Mark lastSync = bundleDate
    │   │
    │   └── NO → Load from SwiftData (instant, < 50ms)
    │
    ├── Background (if online):
    │   └── Check GitHub raw URL for updated places.json
    │       Compare ETag / Last-Modified header
    │       If changed → Download → Delta merge → Update SwiftData
    │
    └── User sees data immediately (never waits for network)
```

**لماذا offline-first:**
- 4.93 MB JSON = ~1.5 MB compressed = يحمّل مرة واحدة
- المستخدم يتصفح فوراً بدون ما ينتظر
- يشتغل بالمترو، بالمطار، بأي مكان بدون نت
- SwiftData production-ready بـ iOS 17+ (2025 mature)

### 2.3 Caching Strategy

| Layer | What | TTL | Size |
|-------|------|-----|------|
| App Bundle | places.json snapshot | At build time | ~5 MB |
| SwiftData | All places (CachedPlace) | Persistent | ~8 MB SQLite |
| URLCache | Images (covers) | 7 days | 50 MB max |
| UserDefaults | Favorites, settings | Permanent | < 100 KB |
| ETag header | Data freshness check | Per request | 32 bytes |

### 2.4 Best Approach for 6,445+ Places

```
Bundled JSON (5 MB) → Parse once → SwiftData (SQLite)
                                        │
                      ┌─────────────────┼───────────────┐
                      │                 │               │
                 FetchDescriptor    Predicate       SortDescriptor
                 (pagination)     (category,       (rating, name,
                  20 per page     neighborhood,     distance)
                                  rating filter)
```

**Performance targets:**
- Initial parse: < 2 seconds (background thread)
- Search query: < 50ms (SwiftData FTS)
- Category filter: < 20ms
- Scroll/pagination: 60fps

---

## 3. MVP Features (Priority Order)

### Phase 1: Core Browse + Search (أول أسبوعين)

**الهدف:** تطبيق يتصفح فيه 6,445 مكان بشكل سلس

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| 1 | Data layer rewrite | Repository + LocalDataService + bundled JSON | 4h |
| 2 | Home screen | Categories grid + trending + nearby (if location) | 3h |
| 3 | Category browse | List places by category + pagination | 2h |
| 4 | Place detail | Full info + map preview + open in maps + share | 3h |
| 5 | Arabic search | Local FTS with fuzzy matching (pg_trgm-style) | 4h |
| 6 | Map view | All places on MapKit + tap to detail | 3h |
| 7 | Favorites | Local favorites with SwiftData | 2h |
| 8 | Neighborhood browse | List by neighborhood + count | 2h |
| 9 | RTL polish | Ensure all views RTL-correct | 2h |
| 10 | App icon + launch | Saudi-themed icon + splash screen | 1h |

**Total Phase 1: ~26 hours AI agent time**

### Phase 2: Enrich + Connect (أسبوع 3-4)

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| 11 | Delivery compare | 60 restaurants × 8 apps comparison | 4h |
| 12 | Advanced filters | Price, rating, features, distance | 3h |
| 13 | Auto-sync | Background check GitHub for updates | 3h |
| 14 | Perfume finder | 100 perfumes + 23 shops + alternatives | 3h |
| 15 | Share to WhatsApp | Deep link with place card | 2h |
| 16 | Onboarding | 3-screen intro for first launch | 2h |
| 17 | Dark/Light mode | System + manual toggle | 1h |
| 18 | Settings | Theme, cache management, about | 2h |

### Phase 3: Platform Features (شهر 2)

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| 19 | Supabase backend | Migrate to real API | 8h |
| 20 | User accounts | Phone OTP via Supabase Auth | 4h |
| 21 | Cloud favorites | Sync across devices | 3h |
| 22 | Reviews & ratings | User-generated content | 6h |
| 23 | Push notifications | New places, trending alerts | 4h |
| 24 | AI search | Semantic "مكان رومانسي هادي" | 6h |
| 25 | Analytics | Mixpanel/PostHog integration | 2h |
| 26 | Widget | iOS home screen widget (nearby/trending) | 3h |

---

## 4. Fix Plan for Current Code

### 4.1 The 6 CRITICAL Bugs

| # | Bug | Root Cause | Fix |
|---|-----|-----------|-----|
| 1 | `CachedMenuPrice` missing | Model referenced in SwiftData schema but .swift file never created | Create the model file OR remove from schema |
| 2 | Supabase creds = placeholder | `"your-project.supabase.co"` and `"your-anon-key-here"` | For MVP: remove Supabase dependency entirely, use local data |
| 3 | `category_id` type mismatch | Place.category is `PlaceCategory` enum but JSON has Arabic string `"كافيه"` | Add custom decoder or mapping layer |
| 4 | Map selection binding broken | `@Binding` type mismatch in MapView | Fix binding type to `Place?` |
| 5 | No data source at all | PlacesService calls Supabase which has fake credentials | Replace with LocalDataService reading bundled JSON |
| 6 | ContentView missing | WainNroohApp references ContentView which may not navigate correctly | Already exists — verify TabView routing |

### 4.2 Fix vs Rewrite Decision Matrix

| Factor | Fix Current | Rewrite | Score |
|--------|:-----------:|:-------:|-------|
| **UI Views (30 files)** | Keep ✅ | Waste effort ❌ | Fix wins |
| **Models (7 files)** | Mostly ok, patch 2 | Rewrite 2 | Fix wins |
| **Services (5 files)** | All broken ❌ | Replace all ✅ | Rewrite wins |
| **ViewModels (5 files)** | Depend on broken services | Reconnect to new services | Rewrite wins |
| **Config (2 files)** | Needs major changes | Rewrite | Rewrite wins |
| **Time to working app** | 12-16h (patch everything) | 8-10h (clean foundation) | Rewrite wins |
| **Technical debt** | Accumulates | Clean start | Rewrite wins |
| **Familiarity with code** | Already built MVVM | Same pattern | Tie |

### 4.3 Decision: **Surgical Rewrite** 🔧

**Keep:** All UI views (30+ SwiftUI files) — they're well-built with Arabic RTL support
**Rewrite:** Data layer (Services, ViewModels, Config, 2 Models)
**Why:** The UI is 70% of the work and it's good. The data pipeline is 100% broken. Fastest path = new foundation, existing walls.

```
KEEP (as-is or minor tweaks):
├── Views/Components/ (6 files)
├── Views/Home/ (3 files)  
├── Views/Search/ (3 files)
├── Views/PlaceDetail/ (4 files)
├── Views/Map/ (1 file)
├── Views/Favorites/ (2 files)
├── Views/DeliveryCompare/ (2 files)
├── Models/Category.swift
├── Models/Neighborhood.swift
├── Extensions/ (3 files)
└── Resources/LaunchScreen.swift

REWRITE:
├── Services/LocalDataService.swift (NEW — replaces SupabaseService + PlacesService)
├── Services/SearchService.swift (NEW — local Arabic FTS)
├── Services/SyncService.swift (NEW — background GitHub sync)
├── ViewModels/ (all 5 — reconnect to new services)
├── Models/Place.swift (fix CodingKeys to match places.json)
├── Models/CachedMenuPrice.swift (create or remove)
├── Config/AppConfig.swift (remove Supabase, add GitHub URLs)
└── WainNroohApp.swift (remove Supabase container setup)

DELETE:
├── Services/SupabaseService.swift (not needed for MVP)
└── Services/DeliveryService.swift (rebuild in Phase 2)
```

---

## 5. Data Pipeline

### 5.1 places.json → التطبيق

```
GitHub Repo (data/places.json)
         │
         ├── Build Time: bundled in app (Xcode build phase)
         │   Copy places.json → App Bundle
         │
         └── Runtime: check for updates
             GET https://raw.githubusercontent.com/treklaps/riyadh-places/main/data/places.json
             Headers: If-None-Match: "previous-etag"
             │
             ├── 304 Not Modified → use local cache
             └── 200 OK → download, parse, delta merge into SwiftData
```

### 5.2 Auto-Sync Flow

```swift
// SyncService — runs on app launch + every 4 hours background
class SyncService {
    func checkForUpdates() async {
        let url = "https://raw.githubusercontent.com/treklaps/riyadh-places/main/data/places.json"
        
        // 1. HEAD request with ETag
        // 2. If changed → GET full JSON (~5 MB, ~1.5 MB gzipped)
        // 3. Parse new places
        // 4. Delta merge: insert new, update changed, keep local-only data (favorites)
        // 5. Store new ETag
        // 6. Update lastSyncDate
    }
}
```

### 5.3 Offline Support

| Scenario | Behavior |
|----------|----------|
| First launch, no internet | Use bundled JSON (ships with app) |
| First launch, has internet | Use bundled JSON + background check for newer |
| Regular launch, no internet | Use SwiftData cache (instant) |
| Regular launch, has internet | Use SwiftData cache + background sync |
| Background refresh | iOS BGAppRefreshTask every 4 hours |

### 5.4 Map: MapKit ✅

**MapKit over Google Maps because:**

| Factor | MapKit | Google Maps SDK |
|--------|--------|----------------|
| Cost | **Free** (unlimited) | $200 free credit/mo, then pay-per-use |
| Integration | **Native** SwiftUI Map {} | Requires CocoaPod + UIViewRepresentable |
| Performance | **Optimized** for iOS | Good but external framework |
| Arabic labels | **Automatic** (follows system locale) | Good Arabic support |
| Riyadh coverage | **Excellent** (Apple Maps improved significantly in Saudi) | Excellent |
| Offline maps | iOS 17+ downloadable maps | Requires separate SDK |
| Size impact | **0 MB** (built into iOS) | +20 MB framework |
| Look & feel | **Native iOS** | Google styling |
| Clustering | **Built-in** MapKit clustering | Requires extra setup |

**Decision:** MapKit for MVP. Google Maps if we need Street View or specific POI data later.

### 5.5 Search: Local FTS

**For MVP — local search is sufficient:**

```swift
// SearchService — Arabic-aware local search
class SearchService {
    func search(query: String, in places: [CachedPlace]) -> [CachedPlace] {
        // 1. Normalize Arabic (remove tashkeel, normalize hamza/alef)
        // 2. Tokenize query
        // 3. Match against: name_ar, name_en, category, neighborhood, tags, description
        // 4. Score: exact match > prefix > contains > fuzzy
        // 5. Boost: rating, trending, completeness
        // 6. Return sorted results
    }
}
```

**Performance:** ~3-5ms for 6,445 places (measured on web version)

| Option | MVP | Scale (10K+ users) |
|--------|:---:|:---:|
| Local FTS (in-app) | ✅ Perfect | ✅ Still works |
| Supabase pg_trgm | ❌ Needs backend | ✅ Good |
| Meilisearch | ❌ Overkill | ✅ Best Arabic |
| Algolia | ❌ Expensive | ✅ Premium |

---

## 6. Cost Analysis

### Month 1 (MVP): $0

| Item | Cost |
|------|------|
| Xcode + Apple tools | $0 |
| MapKit | $0 |
| GitHub (data hosting) | $0 |
| Apple Developer Program | $99/year (already have?) |
| **Total** | **$0** (+ $99/yr if needed) |

### Month 6 (Phase 2): ~$25/mo

| Item | Cost |
|------|------|
| Supabase Pro (if needed) | $25/mo |
| Cloudflare (CDN + R2) | $0 (free tier) |
| Domain (wain-nrooh.com) | $1/mo ($12/yr) |
| Apple Developer | $8.25/mo ($99/yr) |
| **Total** | **~$34/mo** |

### Month 12 (10K users): ~$50/mo

| Item | Cost |
|------|------|
| Supabase Pro | $25/mo |
| Cloudflare Pro (if needed) | $20/mo |
| Meilisearch Cloud (optional) | $0 (free tier) |
| Analytics (PostHog free) | $0 |
| Push notifications (APNs) | $0 |
| **Total** | **~$50/mo** |

### Month 24 (100K users): ~$150/mo

| Item | Cost |
|------|------|
| Supabase Pro (8GB) | $25/mo |
| Supabase bandwidth add-on | $25/mo |
| Cloudflare Pro | $20/mo |
| Cloudflare R2 (images) | $15/mo (~50GB) |
| Meilisearch Cloud | $30/mo |
| Redis (Upstash) | $10/mo |
| Monitoring (Sentry) | $26/mo |
| **Total** | **~$151/mo** |

### Cost Comparison: Us vs Competitors

| Stage | وين نروح | Typical startup |
|-------|----------|----------------|
| MVP | $0/mo | $50-200/mo |
| 10K users | $50/mo | $200-500/mo |
| 100K users | $150/mo | $500-2000/mo |

**Key advantage:** Offline-first = 90% of traffic never hits the server. Most data is served from the app bundle or local cache.

---

## 7. Technical Specifications

### 7.1 Minimum Requirements

| Requirement | Value |
|-------------|-------|
| iOS version | 17.0+ |
| Swift version | 5.9+ |
| Xcode version | 15.0+ |
| Device | iPhone (iPad later) |
| Storage | ~20 MB (app + data) |
| Network | Optional (offline-first) |

### 7.2 Dependencies (MVP)

**Zero external dependencies for MVP.** All Apple frameworks:

| Framework | Purpose |
|-----------|---------|
| SwiftUI | UI |
| SwiftData | Local persistence |
| MapKit | Maps |
| CoreLocation | User location |
| Foundation | Networking, JSON |

**Phase 2+ additions:**
- `supabase-swift` (Supabase SDK)
- `Kingfisher` or `SDWebImage` (image caching)

### 7.3 Project Structure (MVP)

```
WainNrooh/
├── App/
│   ├── WainNroohApp.swift
│   └── ContentView.swift
├── Config/
│   ├── AppConfig.swift
│   └── Theme.swift
├── Models/
│   ├── Place.swift (Codable — matches places.json)
│   ├── CachedPlace.swift (SwiftData @Model)
│   ├── Category.swift
│   ├── Neighborhood.swift
│   └── Favorite.swift (SwiftData @Model)
├── Repositories/
│   ├── PlaceRepository.swift (protocol)
│   ├── LocalPlaceRepository.swift (bundled JSON + SwiftData)
│   └── RemotePlaceRepository.swift (Phase 3: Supabase)
├── Services/
│   ├── SearchService.swift (Arabic FTS)
│   ├── LocationService.swift
│   └── SyncService.swift (GitHub → SwiftData)
├── ViewModels/
│   ├── HomeViewModel.swift
│   ├── SearchViewModel.swift
│   ├── PlaceDetailViewModel.swift
│   ├── MapViewModel.swift
│   └── FavoritesViewModel.swift
├── Views/
│   ├── Components/ (reusable)
│   ├── Home/
│   ├── Search/
│   ├── PlaceDetail/
│   ├── Map/
│   └── Favorites/
├── Extensions/
│   ├── String+Arabic.swift
│   ├── Color+Theme.swift
│   └── View+RTL.swift
└── Resources/
    ├── places.json (bundled data)
    ├── Assets.xcassets
    └── LaunchScreen.swift
```

---

## 8. Arabic RTL Best Practices

### 8.1 Layout

```swift
// ✅ Correct: Use environment-based RTL
.environment(\.layoutDirection, .rightToLeft)
.environment(\.locale, Locale(identifier: "ar"))

// ✅ Use leading/trailing (not left/right)
.padding(.leading, 16) // NOT .padding(.left, 16)
HStack { /* elements auto-flip in RTL */ }

// ✅ Force RTL at app level
UIView.appearance().semanticContentAttribute = .forceRightToLeft
```

### 8.2 Text

```swift
// ✅ Arabic text alignment
Text("مطعم البيك")
    .multilineTextAlignment(.trailing) // Right-aligned for Arabic
    .environment(\.layoutDirection, .rightToLeft)

// ✅ Number formatting
Text(rating, format: .number.precision(.fractionLength(1)))
// Shows: ٤.٥ (Arabic-Indic numerals when locale is ar)

// ✅ Arabic string normalization
extension String {
    var normalizedArabic: String {
        // Remove tashkeel (diacritics)
        // Normalize alef variants (أ إ آ → ا)
        // Normalize taa marbuta (ة → ه for search)
    }
}
```

### 8.3 Navigation

```swift
// ✅ NavigationStack (not NavigationView) for RTL
NavigationStack {
    // Back button auto-flips to right side
    // Swipe-to-go-back works from right edge
}
```

---

## 9. Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| places.json format changes | Data won't parse | Low | Version the JSON, backwards-compatible decoder |
| 6,445 places = slow on old devices | Poor UX | Medium | Pagination (20/page), lazy loading, background parsing |
| Apple rejects app (no backend = "wrapper") | Can't publish | Low | Genuine native features (search, map, favorites), not a webview |
| Arabic search quality | Bad results | Medium | Extensive normalization + fuzzy matching + testing |
| Offline data gets very stale | Wrong info | Medium | Background sync + "last updated" indicator |
| SwiftData bugs (still maturing) | Crashes | Low-Med | Fallback to in-memory array if SwiftData fails |

---

## 10. Success Metrics (MVP)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| App launches without crash | 100% | TestFlight testing |
| Search returns relevant results | >90% accuracy | Manual testing with 50 queries |
| Browse all categories | All 25 categories accessible | Automated UI test |
| Map loads with pins | <2 seconds | Performance test |
| Offline browsing works | Full functionality | Airplane mode test |
| App size | <25 MB | Xcode archive |
| Cold launch time | <1.5 seconds | Instruments |
| Memory usage | <100 MB | Instruments |

---

*Next: See INFRASTRUCTURE.md for hosting/CI/CD details and DATABASE-DESIGN.md for schema.*
