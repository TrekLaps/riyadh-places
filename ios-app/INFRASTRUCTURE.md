# Infrastructure Plan — وين نروح بالرياض (iOS)
**Version:** 1.0 | **Date:** 2026-02-21 | **Author:** iOS System Architect

---

## 1. Infrastructure Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    Infrastructure by Phase                        │
│                                                                   │
│  Phase 1 (MVP):     GitHub Pages ──► iOS App (bundled data)      │
│  Phase 2 (Growth):  + Supabase + Cloudflare CDN                  │
│  Phase 3 (Scale):   + Meilisearch + Redis + APNs                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase 1: MVP Infrastructure ($0/mo)

### 2.1 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   MVP (Phase 1)                      │
│                                                      │
│  ┌────────────────┐                                  │
│  │  GitHub Repo    │──── raw.githubusercontent.com   │
│  │  data/          │    (places.json CDN)             │
│  │  places.json    │                                  │
│  └────────────────┘                                  │
│           │                                          │
│           │ Build time: bundle into app               │
│           │ Runtime: ETag-based sync                  │
│           ▼                                          │
│  ┌────────────────────────────────────────┐          │
│  │           iOS App                       │          │
│  │  ┌──────────┐  ┌───────────┐           │          │
│  │  │ App      │  │ SwiftData │           │          │
│  │  │ Bundle   │  │ (SQLite)  │           │          │
│  │  │ places   │  │ cached    │           │          │
│  │  │ .json    │  │ places    │           │          │
│  │  └──────────┘  └───────────┘           │          │
│  │  ┌──────────┐  ┌───────────┐           │          │
│  │  │ MapKit   │  │ URLCache  │           │          │
│  │  │ (free)   │  │ (images)  │           │          │
│  │  └──────────┘  └───────────┘           │          │
│  └────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

### 2.2 Data Hosting

| Component | Host | Cost | Limits |
|-----------|------|------|--------|
| places.json | GitHub (raw.githubusercontent.com) | $0 | 100 MB file limit, CDN cached |
| App binary | App Store / TestFlight | $0 (with dev account) | 200 MB OTA limit |
| Images | External URLs (Google, websites) | $0 | Depends on source |
| User data | On-device (SwiftData) | $0 | Device storage |

### 2.3 Networking

```swift
// Data sync endpoint
GET https://raw.githubusercontent.com/treklaps/riyadh-places/main/data/places.json
Headers:
  If-None-Match: "etag-from-last-request"
  Accept-Encoding: gzip

// Response scenarios:
// 304 Not Modified → 0 bytes, use local cache
// 200 OK → ~1.5 MB gzipped (4.93 MB raw)
```

**GitHub Raw CDN characteristics:**
- CDN: Fastly (global edge network)
- Cache TTL: ~5 minutes (can be longer)
- Rate limit: 60 requests/hour (unauthenticated), 5000/hour (with token)
- Availability: 99.9%+
- HTTPS only

---

## 3. Phase 2: Supabase Backend ($0→$25/mo)

### 3.1 Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Phase 2 (Growth)                         │
│                                                             │
│  ┌──────────┐    ┌─────────────┐    ┌──────────────────┐   │
│  │  iOS App │───►│ Cloudflare  │───►│    Supabase      │   │
│  │          │◄───│ CDN + WAF   │◄───│  ┌────────────┐  │   │
│  └──────────┘    └─────────────┘    │  │ PostgreSQL │  │   │
│                        │            │  │ + PostGIS  │  │   │
│                  ┌─────▼─────┐      │  │ + pg_trgm  │  │   │
│                  │Cloudflare │      │  └────────────┘  │   │
│                  │ R2 (images│      │  ┌────────────┐  │   │
│                  │ + assets) │      │  │ Auth       │  │   │
│                  └───────────┘      │  │ (GoTrue)   │  │   │
│                                     │  └────────────┘  │   │
│                                     │  ┌────────────┐  │   │
│                                     │  │ Storage    │  │   │
│                                     │  │ (S3-compat)│  │   │
│                                     │  └────────────┘  │   │
│                                     └──────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### 3.2 Supabase Setup

**Project configuration:**

| Setting | Value |
|---------|-------|
| Region | `ap-southeast-1` (Singapore) — closest to Saudi |
| Plan | Free → Pro ($25/mo) when needed |
| Database | PostgreSQL 15+ with PostGIS, pg_trgm, pgvector |
| Auth | Phone OTP (primary), Apple Sign-In (secondary) |
| Edge Functions | Deno runtime for custom logic |
| Realtime | For live price updates (Phase 3) |

**Free tier limits (sufficient for MVP+):**

| Resource | Free Tier | Pro ($25/mo) |
|----------|-----------|-------------|
| Database | 500 MB | 8 GB |
| Auth MAU | 50,000 | 100,000 |
| Storage | 1 GB | 100 GB |
| Bandwidth | 5 GB | 250 GB |
| Edge Functions | 500K invocations | 2M invocations |
| Realtime | 200 concurrent | 500 concurrent |

### 3.3 Cloudflare Setup

| Service | Tier | Cost | Purpose |
|---------|------|------|---------|
| DNS | Free | $0 | Domain management |
| CDN | Free | $0 | Global caching |
| WAF | Free (basic) | $0 | Bot protection |
| R2 Storage | Free (10 GB) | $0 | Place images |
| Workers | Free (100K/day) | $0 | API proxy + cache |
| KV | Free (100K reads) | $0 | Search cache |

---

## 4. CI/CD Pipeline

### 4.1 MVP CI/CD (GitHub Actions → TestFlight)

```yaml
# .github/workflows/ios-build.yml
name: iOS Build & Deploy

on:
  push:
    branches: [main]
    paths:
      - 'ios-app/**'
      - 'data/places.json'
  workflow_dispatch:

jobs:
  build:
    runs-on: macos-14  # M1 runner
    steps:
      - uses: actions/checkout@v4
      
      # Bundle latest places.json into app
      - name: Bundle Data
        run: |
          cp data/places.json ios-app/WainNrooh/Resources/places.json
          
      # Build
      - name: Build Archive
        run: |
          cd ios-app
          xcodebuild archive \
            -scheme WainNrooh \
            -archivePath build/WainNrooh.xcarchive \
            -sdk iphoneos \
            CODE_SIGN_IDENTITY="Apple Distribution" \
            -allowProvisioningUpdates
      
      # Export IPA
      - name: Export IPA
        run: |
          xcodebuild -exportArchive \
            -archivePath build/WainNrooh.xcarchive \
            -exportOptionsPlist ExportOptions.plist \
            -exportPath build/ipa
      
      # Upload to TestFlight
      - name: Upload to TestFlight
        run: |
          xcrun altool --upload-app \
            --file build/ipa/WainNrooh.ipa \
            --apiKey ${{ secrets.APP_STORE_KEY_ID }} \
            --apiIssuer ${{ secrets.APP_STORE_ISSUER_ID }}

  data-sync:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.modified, 'data/places.json')
    steps:
      - name: Trigger app data update notification
        run: |
          # When places.json changes, notify app to sync
          echo "Data updated — apps will auto-sync via ETag"
```

### 4.2 Data Pipeline CI

```yaml
# .github/workflows/data-pipeline.yml
name: Data Pipeline

on:
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours
  workflow_dispatch:

jobs:
  enrich:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run enrichment
        run: python scripts/osm-enrichment.py
        
      - name: Validate data
        run: python scripts/validate-places.py
        
      - name: Commit if changed
        run: |
          git add data/places.json
          git diff --cached --quiet || \
            git commit -m "chore: auto-enrich places data" && \
            git push
```

### 4.3 Required Secrets

| Secret | Purpose | Where |
|--------|---------|-------|
| `APP_STORE_KEY_ID` | App Store Connect API key | GitHub repo secrets |
| `APP_STORE_ISSUER_ID` | API issuer ID | GitHub repo secrets |
| `APPLE_CERTIFICATE` | Distribution certificate (base64) | GitHub repo secrets |
| `PROVISIONING_PROFILE` | Provisioning profile (base64) | GitHub repo secrets |
| `SUPABASE_URL` | Phase 2: Supabase project URL | GitHub repo secrets |
| `SUPABASE_ANON_KEY` | Phase 2: Supabase anon key | GitHub repo secrets |

---

## 5. Monitoring & Analytics

### 5.1 Crash Reporting

| Phase | Tool | Cost |
|-------|------|------|
| MVP | Xcode Organizer (built-in) | $0 |
| Phase 2 | Firebase Crashlytics | $0 |
| Phase 3 | Sentry | $26/mo (Team) |

### 5.2 Analytics

| Phase | Tool | Cost | Features |
|-------|------|------|----------|
| MVP | None (TestFlight analytics) | $0 | Install count, crashes |
| Phase 2 | PostHog (self-hosted or cloud) | $0 (free tier) | Events, funnels, retention |
| Phase 3 | Mixpanel or PostHog Pro | $0-28/mo | Full product analytics |

**Key events to track:**

```swift
enum AnalyticsEvent {
    case appLaunch
    case search(query: String, resultCount: Int)
    case viewPlace(placeId: String, category: String)
    case addFavorite(placeId: String)
    case openInMaps(placeId: String)
    case sharePlace(placeId: String, method: String)
    case filterApplied(filters: [String])
    case categoryBrowsed(category: String)
    case neighborhoodBrowsed(neighborhood: String)
    case deliveryCompared(placeId: String)
    case syncCompleted(newPlaces: Int, duration: TimeInterval)
}
```

### 5.3 Performance Monitoring

| Metric | Target | Tool |
|--------|--------|------|
| App launch time | < 1.5s | Xcode Instruments |
| Search latency | < 50ms | Custom timer |
| Memory usage | < 100 MB | MetricKit |
| Battery impact | < 2%/hr | MetricKit |
| Network usage | < 5 MB/day | URLSession metrics |
| Crash-free rate | > 99.5% | Crashlytics |

---

## 6. Hosting Comparison

### 6.1 Backend Options

| Factor | Supabase | Firebase | AWS (Amplify) | CloudKit |
|--------|----------|----------|---------------|----------|
| **Free tier** | 500MB DB, 50K MAU | 1GB Firestore, 50K reads/day | 25K MAU, 250K syncs | 1GB asset, 10GB transfer |
| **Database** | PostgreSQL (relational) | Firestore (NoSQL) | DynamoDB (NoSQL) | CloudKit (Apple) |
| **SQL support** | ✅ Full SQL | ❌ | ❌ | ❌ |
| **PostGIS** | ✅ Native | ❌ (GeoFirestore) | ❌ | ✅ (CKLocationSortDescriptor) |
| **Arabic FTS** | ✅ pg_trgm + ts_vector | ⚠️ Limited | ⚠️ Limited | ⚠️ tokenize only |
| **Auth** | ✅ Phone OTP built-in | ✅ Best auth system | ✅ Cognito | ✅ Apple ID only |
| **Pricing model** | Predictable tiers | Pay-per-read/write | Pay-per-use | Free (with limits) |
| **Cost at 10K users** | $25/mo | $50-200/mo | $30-100/mo | $0 (if under limits) |
| **Cost at 100K users** | $75/mo | $200-1000/mo | $100-500/mo | $0-50/mo |
| **iOS SDK** | ✅ supabase-swift | ✅ Mature | ✅ Amplify Swift | ✅ Native CloudKit |
| **Offline sync** | ⚠️ Manual | ✅ Built-in | ✅ DataStore | ✅ Built-in |
| **Vendor lock-in** | Low (PostgreSQL) | High (Firestore) | High (AWS) | Very High (Apple) |
| **Open source** | ✅ | ❌ | ❌ | ❌ |
| **Self-host option** | ✅ | ❌ | ❌ | ❌ |

### 6.2 Recommendation

**MVP:** No backend needed (bundled JSON + SwiftData)

**Phase 2+:** **Supabase** is the clear winner because:
1. **PostgreSQL** = real SQL, joins, views, materialized views
2. **PostGIS** = native geospatial queries (nearby places)
3. **pg_trgm** = Arabic text search with trigram similarity
4. **Predictable pricing** = no surprise bills (vs Firebase per-read)
5. **Low lock-in** = standard PostgreSQL, can migrate anywhere
6. **Free tier** = generous enough for MVP + early growth
7. **Swift SDK** = `supabase-swift` maintained by Supabase team

**Why NOT Firebase:**
- Per-read billing can spike with 6,445+ places (each browse = reads)
- NoSQL makes aggregation queries painful
- No native PostGIS equivalent
- Arabic full-text search is limited

**Why NOT CloudKit:**
- Apple-only (no web admin, no Android future)
- Limited query capabilities
- No SQL, no PostGIS
- Debugging is painful

---

## 7. CDN Strategy

### 7.1 Image Hosting

| Phase | Strategy | Host | Cost |
|-------|----------|------|------|
| MVP | External URLs (Google, websites) | Source sites | $0 |
| Phase 2 | Cloudflare R2 + Image Resizing | Cloudflare | $0 (10GB free) |
| Phase 3 | R2 + Cloudflare Images | Cloudflare | $5/mo |

### 7.2 Image Pipeline (Phase 2+)

```
Original Image (from web)
    │
    ▼
Cloudflare Worker (Image Resizing)
    ├── /thumb/200x200/ → PlaceCard
    ├── /medium/400x300/ → Detail hero
    ├── /large/800x600/ → Full view
    └── /og/1200x630/ → Social share
    │
    ▼
Cloudflare R2 (persistent storage)
    │
    ▼
Cloudflare CDN (edge-cached globally)
```

### 7.3 iOS Image Caching

```swift
// MVP: Simple URLCache
let config = URLSessionConfiguration.default
config.urlCache = URLCache(
    memoryCapacity: 50_000_000,    // 50 MB memory
    diskCapacity: 200_000_000,      // 200 MB disk
    diskPath: "imageCache"
)

// Phase 2: Kingfisher or SDWebImage
// - Memory + disk cache
// - Progressive loading
// - WebP support
// - Placeholder images
```

---

## 8. Security Infrastructure

### 8.1 MVP Security

| Layer | Implementation |
|-------|---------------|
| Transport | HTTPS only (ATS enforced) |
| Data at rest | SwiftData (SQLite) — device encrypted |
| Secrets | No secrets in MVP (no API keys needed) |
| Code signing | Apple Distribution certificate |
| Privacy | No user data collected, no tracking |

### 8.2 Phase 2+ Security

| Layer | Implementation |
|-------|---------------|
| API auth | Supabase JWT (anon key in app, user JWT after login) |
| Key storage | iOS Keychain (JWT tokens) |
| RLS | Row Level Security on all Supabase tables |
| WAF | Cloudflare WAF (OWASP rules) |
| Rate limiting | Supabase built-in + Cloudflare rules |
| Input validation | Client-side (Swift) + Server-side (PostgreSQL constraints + Edge Functions) |
| Certificate pinning | Optional (prevents MITM but complicates updates) |

### 8.3 Privacy

```
MVP Privacy Manifest:
├── No user accounts
├── No location tracking (request permission, use locally only)
├── No analytics
├── No third-party SDKs
├── No data leaves device
├── App Store privacy label: "Data Not Collected"
└── Perfect for Saudi data residency requirements
```

---

## 9. Cost Summary by Phase

### Total Monthly Cost

| Phase | Timeline | Monthly Cost | Annual Cost |
|-------|----------|-------------|-------------|
| Phase 1 (MVP) | Now | $0 | $99 (dev account) |
| Phase 2 (Growth) | +2 months | $25-35 | $400 |
| Phase 3 (Scale, 10K) | +6 months | $50-75 | $750 |
| Phase 4 (100K users) | +12 months | $150-200 | $2,000 |

### Cost Breakdown Chart

```
Month    Cost/mo   Cumulative
  1      $0        $0
  2      $0        $0
  3      $25       $25
  4      $25       $50
  5      $25       $75
  6      $35       $110
  7      $35       $145
  8      $50       $195
  9      $50       $245
 10      $50       $295
 11      $75       $370
 12      $75       $445
        ─────────────────
Year 1 Total: ~$445 (+ $99 dev account = $544)
```

### What You Get per Dollar

| Investment | Return |
|------------|--------|
| $0/mo (MVP) | Working app, 6,445 places, offline, search, map |
| $25/mo (Supabase) | Real backend, auth, reviews, cloud sync |
| $50/mo (CDN + search) | Fast globally, Arabic search, images |
| $150/mo (full platform) | 100K users, AI features, analytics |

---

## 10. Disaster Recovery

### 10.1 Backup Strategy

| Data | Backup | Frequency | Retention |
|------|--------|-----------|-----------|
| places.json | Git history | Every commit | Permanent |
| Supabase DB | Supabase daily backup | Daily | 7 days (free), 30 days (pro) |
| User data (favorites) | On-device | N/A | User manages |
| Images (R2) | Cloudflare redundancy | Automatic | N/A |
| App binary | App Store Connect | Every upload | Permanent |

### 10.2 Rollback Plan

| Scenario | Action |
|----------|--------|
| Bad data in places.json | `git revert` → auto-redeploy |
| Supabase outage | App falls back to local SwiftData cache |
| App crash on launch | Previous TestFlight build available |
| CDN outage | Cloudflare has 99.99% SLA; direct to Supabase |

---

*Next: See DATABASE-DESIGN.md for schema details and MVP-PLAN.md for implementation plan.*
