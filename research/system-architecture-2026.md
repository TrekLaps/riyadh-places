# System Architecture — وين نروح بالرياض
**Version:** 1.0 | **Date:** 2026-02-20 | **Author:** System Architect

---

## 1. Current State

```
┌─────────────────────────────────────────────────────────┐
│                CURRENT: Static Site on GitHub Pages       │
│                                                          │
│  Browser ──► GitHub Pages CDN                            │
│                  │                                       │
│                  ▼                                       │
│  ┌──────────┐ ┌───────────────┐ ┌─────────────────────┐ │
│  │ 87 HTML  │ │ places.json   │ │ delivery-prices.json │ │
│  │ pages    │ │ 3,203 places  │ │ 150+ × 8 apps       │ │
│  │ (dir+RTL)│ │ 2.8 MB        │ │ prices-*.json       │ │
│  └──────────┘ └───────────────┘ └─────────────────────┘ │
│                                                          │
│  iOS App (46 Swift files):                               │
│  ├── SwiftUI + MVVM + SwiftData                          │
│  ├── 6 CRITICAL bugs (won't compile)                     │
│  ├── No data source (placeholder Supabase creds)         │
│  └── CachedMenuPrice undefined, map bindings broken      │
│                                                          │
│  CI/CD: 3 GitHub Actions workflows                       │
│  Analytics: none (seeyoufarm dead, localStorage only)    │
│  Domain: treklaps.github.io/riyadh-places/               │
│  Google Index: NOT indexed                               │
└─────────────────────────────────────────────────────────┘
```

**Problems:**
- Users download 2.8 MB JSON on every visit
- No server-side search — all client-side filtering
- No auth, no user accounts, no favorites persistence
- iOS app is broken — 6 critical compile errors, zero data pipeline
- No analytics, no indexing, no custom domain
- Data updates require manual JSON editing + deploy

---

## 2. Target Architecture (3 Phases)

### Phase 1 — Enhanced Static (Weeks 1–2, $0/mo)

No backend. Optimize what exists.

```
┌────────────────────────────────────────────┐
│  Browser ──► GitHub Pages / Cloudflare CDN │
│                                            │
│  Changes:                                  │
│  ├── Split places.json → chunked pages     │
│  │   (places-1.json … places-N.json)       │
│  ├── Service Worker (offline + cache)      │
│  ├── Lazy-load data on scroll              │
│  ├── Images → WebP, lazy load, <picture>   │
│  ├── Fix 4 CRITICAL site audit findings:   │
│  │   sitemap domain, SW, og:image, hrefs   │
│  ├── Register custom domain wain-nrooh.com │
│  └── Cloudflare DNS (free CDN + WAF)       │
└────────────────────────────────────────────┘
```

| Item | Detail |
|------|--------|
| **Tech** | Static HTML/CSS/JS, Service Worker, Cloudflare Free |
| **Cost** | $0/mo + $12/yr domain |
| **Deploy** | GitHub Actions → GitHub Pages + Cloudflare proxy |
| **Timeline** | 1 AI-agent sprint (2–3 days actual work) |
| **Exit criteria** | Lighthouse > 90, offline works, domain live, indexed |

### Phase 2 — Supabase Backend (Weeks 3–10, $0→$25/mo)

The real migration. Enables iOS app, auth, dynamic content.

```
                    ┌──────────────┐
                    │  Cloudflare  │
                    │  CDN + WAF   │
                    │  R2 (images) │
                    └──────┬───────┘
                           │
               ┌───────────┼───────────┐
               │           │           │
         ┌─────▼─────┐  ┌─▼────┐  ┌───▼──────┐
         │  Website   │  │ iOS  │  │  Admin   │
         │ (Astro SSG │  │ App  │  │  Scripts │
         │  + islands)│  │      │  │ (scraper)│
         └─────┬──────┘  └──┬───┘  └────┬─────┘
               │            │           │
               └────────────┼───────────┘
                            │
                  ┌─────────▼──────────┐
                  │  Cloudflare Worker │
                  │  (cache + proxy)   │
                  └─────────┬──────────┘
                            │
                  ┌─────────▼──────────┐
                  │     Supabase       │
                  │ ┌───────────────┐  │
                  │ │ PostgreSQL    │  │
                  │ │ + PostGIS     │  │
                  │ │ + pgvector    │  │
                  │ │ + pg_trgm     │  │
                  │ └───────────────┘  │
                  │ ┌───────┐┌───────┐ │
                  │ │ Auth  ││ Edge  │ │
                  │ │(GoTrue││ Funcs │ │
                  │ └───────┘└───────┘ │
                  │ ┌───────┐┌───────┐ │
                  │ │Storage││Realtime│ │
                  │ └───────┘└───────┘ │
                  └────────────────────┘
```

**Key data flow — search example:**

```
User types "مقهى هادي بالعليا"
    │
    ▼
Cloudflare Worker
    ├── Cache key: "search:مقهى+هادي+العليا"
    ├── HIT → return cached (< 5ms, edge)
    └── MISS ──► Supabase Edge Function
                    │
                    ▼
                PostgreSQL FTS:
                search_vector_ar @@ plainto_tsquery('arabic','مقهى هادي')
                AND area_id = 'olaya'
                ORDER BY ts_rank DESC, rating_avg DESC
                    │
                    ▼
                Cache result in KV (TTL 1hr)
                    │
                    ▼
                Return JSON (< 200ms total)
```

**API endpoints (core):**

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/v1/places` | GET | - | List, filter, paginate |
| `/v1/places/:id` | GET | - | Place detail |
| `/v1/places/nearby` | GET | - | PostGIS radius query |
| `/v1/search` | GET | - | Arabic FTS + filters |
| `/v1/search/suggest` | GET | - | Autocomplete |
| `/v1/delivery/compare` | GET | - | Price comparison across 8 apps |
| `/v1/prices/:placeId` | GET | - | Menu prices in SAR |
| `/v1/auth/otp` | POST | - | Phone OTP (primary) |
| `/v1/auth/verify-otp` | POST | - | Verify + issue JWT |
| `/v1/users/me/favorites` | GET/POST/DEL | JWT | Favorites CRUD |
| `/v1/places/:id/reviews` | GET/POST | JWT | Reviews |
| `/v1/admin/*` | ALL | Admin JWT | Data management |

**iOS app connection:**

```
iOS App (SwiftUI)
    │
    ├── Supabase Swift SDK ──► API (auth, CRUD)
    ├── SwiftData (local) ──► Offline cache
    │     └── Delta sync: WHERE updated_at > last_sync
    ├── MapKit + CoreLocation ──► Nearby places
    └── Keychain ──► JWT storage (encrypted)
```

| Item | Detail |
|------|--------|
| **Tech** | Supabase (PG + Auth + Edge Funcs + Realtime), Cloudflare (CDN + R2 + Workers + KV), Astro SSG, SwiftUI |
| **Cost** | $0/mo MVP → $25/mo at 1K+ users (Supabase Pro) |
| **Deploy** | GitHub Actions → Supabase CLI + Wrangler + Cloudflare Pages |
| **Timeline** | 8 weeks (2 for API, 2 for iOS integration, 2 for web migration, 2 for polish) |
| **Exit criteria** | API live, iOS compiles with real data, website uses API, auth works |

### Phase 3 — Full Platform (Months 4–6+, $50–150/mo)

AI features, automated scraping, scale.

```
Phase 2 stack
    +
    ├── Meilisearch Cloud ($30/mo)
    │   └── Arabic instant search, typo-tolerance, facets
    ├── pgvector embeddings
    │   └── text-embedding-3-small (256d, $0.006 for all places)
    │   └── Semantic: "مكان رومانسي لعشاء خاص" → vector similarity
    ├── Upstash Redis ($10/mo)
    │   └── Session management, rate limiting, leaderboards
    ├── Automated scraping pipeline
    │   └── pg_cron → Edge Function → 8 delivery apps daily
    │   └── Validation pipeline (price range, GPS bbox, anomaly detection)
    ├── Push notifications (APNs via Edge Function)
    ├── Recommendation engine
    │   └── Hybrid: content similarity + popularity + distance + time
    └── Multi-city expansion (Jeddah, Dammam)
```

| Item | Detail |
|------|--------|
| **Cost** | $50–150/mo depending on traffic |
| **Timeline** | Ongoing after Phase 2 launch |

---

## 3. Key Architecture Decisions

### Why GitHub Pages first → Supabase later

| Factor | GitHub Pages | Supabase |
|--------|-------------|----------|
| Cost | $0 | $0 free → $25 pro |
| Setup time | 0 (already live) | 2 weeks |
| SEO | Excellent (static) | Requires SSG/ISR |
| Speed | Fast (CDN) | Faster (edge cache) |
| Dynamic content | None | Full |
| iOS app | Impossible | Native SDK |

**Decision:** Don't migrate until iOS app or user accounts are needed. Improve static site first.

### Why Supabase over alternatives

| Factor | Supabase | Firebase | AWS | Railway |
|--------|----------|----------|-----|---------|
| Free tier DB | 500 MB PG | NoSQL only | Complex | $5/mo |
| PostGIS | Built-in | None | Manual | Manual |
| Arabic FTS | PG arabic dict | Weak | Manual | Manual |
| Auth | Built-in | Built-in | Cognito (complex) | None |
| Swift SDK | Official | Official | Amplify (heavy) | None |
| Real-time | WebSocket | WebSocket | AppSync ($$) | None |
| RLS | Native | Rules | IAM (complex) | None |
| $0 → production | Yes | Yes | No | No |

**Decision:** Supabase — only option with PG + PostGIS + Auth + Swift SDK + real-time at $0.

### Why SwiftUI (not React Native / Flutter)

| Factor | SwiftUI | React Native | Flutter |
|--------|---------|-------------|---------|
| Arabic RTL | Native, automatic | Manual config | Plugin |
| MapKit | Native | Wrapper (buggy) | Plugin |
| App size | ~15 MB | ~40 MB | ~30 MB |
| Liquid Glass (iOS 26) | Automatic | Never | Never |
| Offline (SwiftData) | Native | AsyncStorage (weak) | Hive/Isar |
| Performance | Native | Bridge overhead | Good |
| Code amount | Least | More | More |

**Decision:** SwiftUI — Arabic RTL is native, MapKit is native, Liquid Glass is free, single platform (iOS only for now).

### Search: Client-side → PostgreSQL FTS → Meilisearch

```
Phase 1: Client-side JS filter on places.json
    (current — works for 3K places, slow for 10K+)
         │
         ▼
Phase 2: PostgreSQL Full-Text Search
    arabic dictionary + pg_trgm (fuzzy)
    + GIN indexes + PostGIS spatial
    (free — sufficient for 5K-50K places)
         │
         ▼
Phase 3: Meilisearch Cloud ($30/mo)
    when PG FTS latency > 200ms or
    need typo-tolerance + instant facets
```

### CDN + Images: Cloudflare R2

**Critical decision:** R2 has **$0 egress**. For an image-heavy site, this saves hundreds of dollars versus S3 or Supabase Storage.

```
Image pipeline:
Upload → R2 → Cloudflare Worker (resize, WebP, strip EXIF)
    → CDN edge cache (Cache-Control: immutable)
    → User (< 50ms, nearest edge)
```

---

## 4. Security Architecture

Turki's red-team background demands security-first design.

```
Request flow through security layers:

Internet → Cloudflare WAF (DDoS, bot, IP reputation)
    → Cloudflare Worker (rate limit, CORS, API key)
    → Supabase JWT verification (auth)
    → Row Level Security (authorization per row)
    → Zod input validation (injection prevention)
    → PostgreSQL parameterized queries (no raw SQL)
```

**Key security measures:**
- **Auth:** Phone OTP (primary) + Apple Sign-In (required by Apple). JWT in Keychain (iOS) / httpOnly cookie (web).
- **RLS everywhere:** Users read only own favorites/reviews. Admins write places. Public reads active places only.
- **No secrets in code:** `.xcconfig` for iOS, env vars for Edge Functions, GitHub Secrets for CI.
- **Rate limiting:** Anonymous 60 req/min, authenticated 120, admin 300. OTP capped at 5/min.
- **PDPL (Saudi data law):** Low risk at MVP (public places + pseudonymous accounts). Review when collecting sensitive location data. Supabase on AWS — request Bahrain region for Pro tier.
- **OWASP Top 10:** Covered via Supabase managed infra (injection, auth, misconfig) + Cloudflare WAF (DDoS, SSRF) + Zod (data integrity).

---

## 5. Arabic-First Design

Arabic is not an afterthought — it drives architecture choices.

| Layer | Arabic consideration |
|-------|---------------------|
| **Database** | `name_ar` is primary, `name_en` is optional. `search_vector_ar` uses PostgreSQL `arabic` dictionary. `pg_trgm` catches "مقهي"→"مقهى". |
| **API** | `?lang=ar` default. All responses include `_ar` fields first. Error messages bilingual. |
| **Search** | Arabic stemming: "قهوة"/"قهاوي"/"مقهى" match. Tashkeel normalization. Saudi dialect synonyms dictionary. |
| **iOS** | SwiftUI RTL is automatic. SF Arabic system font. `Locale("ar_SA")` for numbers/dates. |
| **Web** | `dir="rtl"` on `<html>`. CSS `logical properties` (inline-start/end). Tajawal font for reports. |
| **Images** | Alt text in Arabic. No text in images (un-translatable). |

---

## 6. Data Migration Path

```
Current JSON files          Target PostgreSQL tables
─────────────────           ──────────────────────
places.json (3,203)    ──►  places + categories + areas
delivery-prices.json   ──►  delivery_prices + delivery_apps
prices-initial.json    ──►  menu_items + menu_categories
prices-batch2.json     ──►  menu_items (merge)
enriched-*.json        ──►  places (update features, ratings)
neighborhoods.json     ──►  areas (with PostGIS boundaries)

Migration pipeline:
1. Parse + validate (Zod schemas)
2. Transform (normalize names, geocode, generate slugs, extract features)
3. Load (categories → areas → places → delivery → menus)
4. Post-load (build FTS vectors, verify counts, sanity check)
5. Test (search queries, geo queries, RLS policies)

Estimated DB size: ~50 MB (well within 500 MB free tier)
```

---

## 7. Cost Summary

| Phase | Monthly | What you get |
|-------|---------|-------------|
| **Phase 1** (weeks 1–2) | **$0** | Optimized static site, custom domain, offline |
| **Phase 2 MVP** (weeks 3–10) | **$0** | API, auth, iOS app, Supabase free tier |
| **Phase 2 Growth** (1K+ users) | **$25** | Supabase Pro (8 GB DB, daily backups) |
| **Phase 3** (AI + scale) | **$50–150** | Meilisearch + Redis + Pro compute |
| **Year 1 total** | **~$400** | Full platform: web + iOS + API + AI |

One-time: $12 domain + $99 Apple Developer (when App Store ready) = $111.

---

## 8. Timeline (AI-augmented 1-person team)

| Week | Milestone | Agents |
|------|-----------|--------|
| 1–2 | Phase 1: static site fixes, domain, Cloudflare | 2–3 agents |
| 3–4 | Supabase setup, schema, data migration, core API | 3–4 agents |
| 5–6 | Auth, favorites, reviews, delivery compare API | 2–3 agents |
| 7–8 | iOS app: fix 6 criticals, connect to real API, offline sync | 3–4 agents |
| 9–10 | Web migration to Astro SSG + API, SEO redirect | 2–3 agents |
| 11–14 | Phase 3: Meilisearch, scraping pipeline, embeddings | 2–3 agents |
| 15–20 | Recommendations, push notifications, App Store submit | 2–3 agents |

**Critical path:** Phase 2 API must be live before iOS app can ship.

---

## 9. Scalability Checkpoints

| Users | Action needed |
|-------|--------------|
| 0–1K | Free tier. No changes. |
| 1K–10K | Supabase Pro ($25). Add Cloudflare Pro if WAF needed. |
| 10K–50K | Meilisearch Cloud ($30). Upstash Redis ($10). Read replica if DB slow. |
| 50K–100K | Dedicated Supabase compute. Cloudflare Business. Consider Bahrain region. |
| 100K+ | Evaluate self-hosted PG, microservices, dedicated search infra. |

**Key insight:** Supabase free tier handles 50K auth users and 500 MB DB. For a Riyadh-focused app, this covers the first 6–12 months easily.

---

*This document is the single source of truth for system architecture. Update it when decisions change.*
*Detailed API specs, DB schema, and iOS integration code are in SERVER-ARCHITECTURE.md and MVP-DEFINITION.md.*
