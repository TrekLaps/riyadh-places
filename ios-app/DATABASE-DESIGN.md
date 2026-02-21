# Database Design — وين نروح بالرياض (iOS)
**Version:** 1.0 | **Date:** 2026-02-21 | **Author:** iOS System Architect

---

## 1. Database Strategy by Phase

| Phase | Database | Location | Size |
|-------|----------|----------|------|
| MVP | SwiftData (SQLite) | On-device | ~8 MB |
| Phase 2 | Supabase PostgreSQL + SwiftData cache | Cloud + device | ~50 MB (cloud) |
| Phase 3 | + pgvector + Meilisearch | Cloud | ~200 MB |

---

## 2. MVP: SwiftData Schema (On-Device)

### 2.1 Entity Relationship Diagram

```
┌──────────────────────────────────┐
│          CachedPlace             │
│ ─────────────────────────────    │
│ @Attribute(.unique)              │
│ id: String (PK)                  │
│ nameAr: String                   │
│ nameEn: String?                  │
│ category: String                 │
│ categoryAr: String               │
│ neighborhood: String?            │
│ neighborhoodEn: String?          │
│ descriptionAr: String?           │
│ googleRating: Double             │
│ priceRange: String?              │
│ latitude: Double?                │
│ longitude: Double?               │
│ googleMapsUrl: String?           │
│ phone: String?                   │
│ website: String?                 │
│ instagram: String?               │
│ hours: String?                   │
│ address: String?                 │
│ coverImageUrl: String?           │
│ tagsJson: String?                │
│ perfectForJson: String?          │
│ audienceJson: String?            │
│ isTrending: Bool                 │
│ isNew: Bool                      │
│ isFree: Bool                     │
│ lastSyncedAt: Date               │
│ searchText: String (computed)    │
└──────────┬───────────────────────┘
           │
           │ 1:1 (optional)
           ▼
┌──────────────────────────────────┐
│          Favorite                 │
│ ─────────────────────────────    │
│ @Attribute(.unique)              │
│ id: String (PK) = UUID           │
│ placeId: String (FK)             │
│ createdAt: Date                  │
│ note: String? (user note)        │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│       DeliveryPrice              │
│ ─────────────────────────────    │
│ id: String (PK) = UUID           │
│ placeId: String (FK)             │
│ appName: String                  │
│ deliveryFee: Double              │
│ minimumOrder: Double?            │
│ estimatedTime: String?           │
│ lastUpdated: Date                │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│          SyncState               │
│ ─────────────────────────────    │
│ id: String (PK) = "main"        │
│ lastSyncDate: Date               │
│ lastETag: String?                │
│ placesCount: Int                 │
│ lastSyncDuration: TimeInterval   │
└──────────────────────────────────┘
```

### 2.2 SwiftData Models

```swift
// CachedPlace.swift — Primary data model
@Model
final class CachedPlace {
    @Attribute(.unique) var id: String
    var nameAr: String
    var nameEn: String?
    var category: String        // "cafe", "restaurant", etc.
    var categoryAr: String      // "كافيه", "مطاعم"
    var neighborhood: String?   // "حي العليا"
    var neighborhoodEn: String? // "Al Olaya"
    var descriptionAr: String?
    var googleRating: Double
    var priceRange: String?     // "$", "$$", "$$$"
    var latitude: Double?
    var longitude: Double?
    var googleMapsUrl: String?
    var phone: String?
    var website: String?
    var instagram: String?
    var hours: String?
    var address: String?
    var coverImageUrl: String?
    var tagsJson: String?       // JSON array as string
    var perfectForJson: String? // JSON array
    var audienceJson: String?   // JSON array
    var isTrending: Bool
    var isNew: Bool
    var isFree: Bool
    var lastSyncedAt: Date
    
    // Computed: concatenated search text for FTS
    var searchText: String {
        [nameAr, nameEn, categoryAr, neighborhood, 
         neighborhoodEn, descriptionAr, tagsJson]
            .compactMap { $0 }
            .joined(separator: " ")
    }
    
    // Parse tags from JSON string
    var tags: [String] {
        guard let data = tagsJson?.data(using: .utf8) else { return [] }
        return (try? JSONDecoder().decode([String].self, from: data)) ?? []
    }
    
    var perfectFor: [String] {
        guard let data = perfectForJson?.data(using: .utf8) else { return [] }
        return (try? JSONDecoder().decode([String].self, from: data)) ?? []
    }
    
    var audience: [String] {
        guard let data = audienceJson?.data(using: .utf8) else { return [] }
        return (try? JSONDecoder().decode([String].self, from: data)) ?? []
    }
    
    // Initialize from places.json entry
    init(from json: PlaceJSON) {
        self.id = json.id
        self.nameAr = json.name_ar
        self.nameEn = json.name_en
        self.category = json.category_en ?? "other"
        self.categoryAr = json.category ?? json.category_ar ?? ""
        self.neighborhood = json.neighborhood
        self.neighborhoodEn = json.neighborhood_en
        self.descriptionAr = json.description_ar
        self.googleRating = json.google_rating ?? 0
        self.priceRange = json.price_range ?? json.price_level
        self.latitude = json.lat
        self.longitude = json.lng
        self.googleMapsUrl = json.google_maps_url
        self.phone = nil  // Not in current data
        self.website = nil
        self.instagram = nil
        self.hours = nil
        self.address = nil
        self.coverImageUrl = nil
        self.tagsJson = json.tags.flatMap { try? String(data: JSONEncoder().encode($0), encoding: .utf8) }
        self.perfectForJson = json.perfect_for.flatMap { try? String(data: JSONEncoder().encode($0), encoding: .utf8) }
        self.audienceJson = json.audience.flatMap { try? String(data: JSONEncoder().encode($0), encoding: .utf8) }
        self.isTrending = json.trending ?? false
        self.isNew = json.is_new ?? false
        self.isFree = json.is_free ?? false
        self.lastSyncedAt = Date()
    }
}
```

### 2.3 JSON Mapping (places.json → SwiftData)

**Current places.json fields → CachedPlace mapping:**

| JSON Field | Type | SwiftData Field | Notes |
|------------|------|-----------------|-------|
| `id` | String | `id` | Unique identifier (slug) |
| `name_ar` | String | `nameAr` | Arabic name (primary) |
| `name_en` | String? | `nameEn` | English name |
| `category` | String | `categoryAr` | Arabic: "كافيه" |
| `category_en` | String | `category` | English: "cafe" |
| `neighborhood` | String | `neighborhood` | Arabic: "حي العليا" |
| `neighborhood_en` | String | `neighborhoodEn` | English: "Al Olaya" |
| `description_ar` | String? | `descriptionAr` | Arabic description |
| `google_rating` | Double? | `googleRating` | 0-5 scale |
| `price_level` / `price_range` | String? | `priceRange` | "$" to "$$$$" |
| `lat` | Double? | `latitude` | Decimal degrees |
| `lng` | Double? | `longitude` | Decimal degrees |
| `google_maps_url` | String? | `googleMapsUrl` | Direct link |
| `trending` | Bool? | `isTrending` | From social media |
| `is_new` | Bool? | `isNew` | Recently added |
| `is_free` | Bool? | `isFree` | Free entry |
| `tags` | [String]? | `tagsJson` | Stored as JSON string |
| `perfect_for` | [String]? | `perfectForJson` | Use case tags |
| `audience` | [String]? | `audienceJson` | Target audience |
| `sources` | [String]? | (not stored) | Data provenance |
| `district` | String? | (not stored) | Always "الرياض" |

### 2.4 SwiftData Queries (Common)

```swift
// All places in a category
@Query(filter: #Predicate<CachedPlace> { $0.category == "cafe" },
       sort: \.googleRating, order: .reverse)
var cafes: [CachedPlace]

// Search (name contains query)
let query = "بيك"
@Query(filter: #Predicate<CachedPlace> { 
    $0.nameAr.localizedStandardContains(query) ||
    $0.nameEn?.localizedStandardContains(query) == true
})
var searchResults: [CachedPlace]

// Trending places
@Query(filter: #Predicate<CachedPlace> { $0.isTrending == true },
       sort: \.googleRating, order: .reverse)
var trending: [CachedPlace]

// Places in neighborhood
@Query(filter: #Predicate<CachedPlace> { $0.neighborhood == "حي العليا" })
var olayaPlaces: [CachedPlace]

// High-rated places (4.0+)
@Query(filter: #Predicate<CachedPlace> { $0.googleRating >= 4.0 },
       sort: \.googleRating, order: .reverse)
var topRated: [CachedPlace]
```

---

## 3. Phase 2: Supabase PostgreSQL Schema

### 3.1 Tables

```sql
-- ================================================
-- Core Tables
-- ================================================

-- Places — الجدول الرئيسي (6,445+ rows)
CREATE TABLE places (
    id TEXT PRIMARY KEY,                    -- slug: "miss-cafe"
    name_ar TEXT NOT NULL,                  -- "ميس كافيه"
    name_en TEXT,                           -- "Miss Cafe"
    category TEXT NOT NULL,                 -- "cafe"
    category_ar TEXT NOT NULL,              -- "كافيه"
    neighborhood TEXT,                      -- "حي العليا"
    neighborhood_en TEXT,                   -- "Al Olaya"
    description_ar TEXT,                    -- وصف المكان
    google_rating DECIMAL(2,1) DEFAULT 0,   -- 4.3
    rating_count INTEGER DEFAULT 0,         -- Number of Google ratings
    price_range TEXT,                        -- "$", "$$", "$$$", "$$$$"
    
    -- Location
    latitude DECIMAL(10,7),                 -- 24.7136000
    longitude DECIMAL(10,7),                -- 46.6753000
    location GEOGRAPHY(Point, 4326),        -- PostGIS point (auto-computed)
    google_maps_url TEXT,
    address_ar TEXT,
    
    -- Contact
    phone TEXT,
    website TEXT,
    instagram TEXT,
    hours JSONB,                             -- {"sat": "9-23", "sun": "9-23", ...}
    
    -- Media
    cover_image_url TEXT,
    images TEXT[],                            -- Array of image URLs
    
    -- Tags & Features
    tags TEXT[],                              -- ["هادي", "specialty coffee"]
    perfect_for TEXT[],                       -- ["استرخاء", "مناسبات"]
    audience TEXT[],                          -- ["عوائل", "شباب"]
    features JSONB,                          -- {"wifi": true, "parking": true, ...}
    
    -- Flags
    is_trending BOOLEAN DEFAULT false,
    is_new BOOLEAN DEFAULT false,
    is_free BOOLEAN DEFAULT false,
    is_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    
    -- Search
    search_vector_ar TSVECTOR,              -- Arabic full-text search vector
    search_vector_en TSVECTOR,              -- English full-text search vector
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Data quality
    completeness_score DECIMAL(3,2),         -- 0.00 to 1.00
    data_sources TEXT[]                       -- ["LiveLoveSaudi 2025", "OSM"]
);

-- Areas/Neighborhoods — الأحياء
CREATE TABLE areas (
    id TEXT PRIMARY KEY,                     -- "olaya"
    name_ar TEXT NOT NULL,                   -- "حي العليا"
    name_en TEXT,                             -- "Al Olaya"
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    location GEOGRAPHY(Point, 4326),
    places_count INTEGER DEFAULT 0,
    description_ar TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Categories — التصنيفات
CREATE TABLE categories (
    id TEXT PRIMARY KEY,                     -- "cafe"
    name_ar TEXT NOT NULL,                   -- "مقاهي"
    name_en TEXT NOT NULL,                   -- "Cafes"
    icon TEXT,                               -- SF Symbol name
    emoji TEXT,                              -- "☕"
    color TEXT,                              -- hex color
    sort_order INTEGER DEFAULT 0,
    places_count INTEGER DEFAULT 0
);

-- ================================================
-- User-Generated Content
-- ================================================

-- User Favorites
CREATE TABLE favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    place_id TEXT NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, place_id)
);

-- User Reviews
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    place_id TEXT NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    text_ar TEXT,
    visit_date DATE,
    photos TEXT[],
    is_verified BOOLEAN DEFAULT false,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, place_id)
);

-- ================================================
-- Delivery Prices — أسعار التوصيل
-- ================================================

CREATE TABLE delivery_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    place_id TEXT NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    app_name TEXT NOT NULL,                  -- "هنقرستيشن", "جاهز", etc.
    delivery_fee DECIMAL(6,2),               -- SAR
    minimum_order DECIMAL(6,2),
    estimated_minutes INTEGER,
    rating DECIMAL(2,1),
    is_available BOOLEAN DEFAULT true,
    last_checked TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(place_id, app_name)
);

-- ================================================
-- Menu Prices — أسعار الأصناف
-- ================================================

CREATE TABLE menu_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    place_id TEXT NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    item_name_ar TEXT NOT NULL,
    item_name_en TEXT,
    price DECIMAL(8,2) NOT NULL,            -- SAR
    category TEXT,                            -- "مشروبات", "أطباق رئيسية"
    size TEXT,                               -- "صغير", "وسط", "كبير"
    is_available BOOLEAN DEFAULT true,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- ================================================
-- Perfumes — العطور
-- ================================================

CREATE TABLE perfumes (
    id TEXT PRIMARY KEY,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    brand TEXT,
    type TEXT,                               -- "عود", "مسك", "فرنسي"
    price_range TEXT,
    notes JSONB,                             -- {"top": [...], "heart": [...], "base": [...]}
    alternatives TEXT[],                      -- Array of similar perfume IDs
    shops TEXT[]                              -- Array of shop IDs that carry this
);
```

### 3.2 Indexes

```sql
-- ================================================
-- Performance Indexes
-- ================================================

-- Primary lookup patterns
CREATE INDEX idx_places_category ON places(category);
CREATE INDEX idx_places_neighborhood ON places(neighborhood);
CREATE INDEX idx_places_rating ON places(google_rating DESC);
CREATE INDEX idx_places_trending ON places(is_trending) WHERE is_trending = true;
CREATE INDEX idx_places_new ON places(is_new) WHERE is_new = true;
CREATE INDEX idx_places_active ON places(is_active) WHERE is_active = true;

-- Composite indexes for common queries
CREATE INDEX idx_places_category_rating ON places(category, google_rating DESC) 
    WHERE is_active = true;
CREATE INDEX idx_places_neighborhood_rating ON places(neighborhood, google_rating DESC) 
    WHERE is_active = true;

-- PostGIS spatial index (for nearby queries)
CREATE INDEX idx_places_location ON places USING GIST(location);

-- Full-text search indexes
CREATE INDEX idx_places_search_ar ON places USING GIN(search_vector_ar);
CREATE INDEX idx_places_search_en ON places USING GIN(search_vector_en);

-- Trigram index for fuzzy Arabic search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_places_name_ar_trgm ON places USING GIN(name_ar gin_trgm_ops);
CREATE INDEX idx_places_name_en_trgm ON places USING GIN(name_en gin_trgm_ops);

-- Tags array index
CREATE INDEX idx_places_tags ON places USING GIN(tags);
CREATE INDEX idx_places_perfect_for ON places USING GIN(perfect_for);

-- User data indexes
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_favorites_place ON favorites(place_id);
CREATE INDEX idx_reviews_place ON reviews(place_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);

-- Delivery prices
CREATE INDEX idx_delivery_place ON delivery_prices(place_id);
CREATE INDEX idx_delivery_app ON delivery_prices(app_name);

-- Sync optimization
CREATE INDEX idx_places_updated ON places(updated_at DESC);
```

### 3.3 Functions

```sql
-- ================================================
-- PostGIS: Nearby Places
-- ================================================

CREATE OR REPLACE FUNCTION nearby_places(
    lat DECIMAL,
    lng DECIMAL,
    radius_m INTEGER DEFAULT 5000,
    max_results INTEGER DEFAULT 20,
    cat TEXT DEFAULT NULL
)
RETURNS TABLE (
    id TEXT,
    name_ar TEXT,
    name_en TEXT,
    category TEXT,
    category_ar TEXT,
    neighborhood TEXT,
    google_rating DECIMAL,
    price_range TEXT,
    latitude DECIMAL,
    longitude DECIMAL,
    cover_image_url TEXT,
    distance_meters DECIMAL
)
LANGUAGE sql
STABLE
AS $$
    SELECT
        p.id, p.name_ar, p.name_en, p.category, p.category_ar,
        p.neighborhood, p.google_rating, p.price_range,
        p.latitude, p.longitude, p.cover_image_url,
        ST_Distance(
            p.location,
            ST_MakePoint(lng, lat)::geography
        ) as distance_meters
    FROM places p
    WHERE p.is_active = true
        AND p.location IS NOT NULL
        AND ST_DWithin(
            p.location,
            ST_MakePoint(lng, lat)::geography,
            radius_m
        )
        AND (cat IS NULL OR p.category = cat)
    ORDER BY distance_meters ASC
    LIMIT max_results;
$$;

-- ================================================
-- Arabic Full-Text Search
-- ================================================

-- Auto-update search vectors on insert/update
CREATE OR REPLACE FUNCTION update_search_vectors()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector_ar := to_tsvector('simple',
        coalesce(NEW.name_ar, '') || ' ' ||
        coalesce(NEW.category_ar, '') || ' ' ||
        coalesce(NEW.neighborhood, '') || ' ' ||
        coalesce(NEW.description_ar, '') || ' ' ||
        coalesce(array_to_string(NEW.tags, ' '), '') || ' ' ||
        coalesce(array_to_string(NEW.perfect_for, ' '), '')
    );
    NEW.search_vector_en := to_tsvector('english',
        coalesce(NEW.name_en, '') || ' ' ||
        coalesce(NEW.category, '') || ' ' ||
        coalesce(NEW.neighborhood_en, '') || ' ' ||
        coalesce(array_to_string(NEW.tags, ' '), '')
    );
    
    -- Auto-compute PostGIS point
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.location := ST_MakePoint(NEW.longitude, NEW.latitude)::geography;
    END IF;
    
    -- Auto-update timestamp
    NEW.updated_at := NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER places_search_update
    BEFORE INSERT OR UPDATE ON places
    FOR EACH ROW
    EXECUTE FUNCTION update_search_vectors();

-- ================================================
-- Combined Search (Arabic + English + Fuzzy)
-- ================================================

CREATE OR REPLACE FUNCTION search_places(
    query TEXT,
    cat TEXT DEFAULT NULL,
    area TEXT DEFAULT NULL,
    min_rating DECIMAL DEFAULT 0,
    max_results INTEGER DEFAULT 20
)
RETURNS TABLE (
    id TEXT,
    name_ar TEXT,
    name_en TEXT,
    category TEXT,
    category_ar TEXT,
    neighborhood TEXT,
    google_rating DECIMAL,
    price_range TEXT,
    latitude DECIMAL,
    longitude DECIMAL,
    cover_image_url TEXT,
    relevance DECIMAL
)
LANGUAGE sql
STABLE
AS $$
    SELECT
        p.id, p.name_ar, p.name_en, p.category, p.category_ar,
        p.neighborhood, p.google_rating, p.price_range,
        p.latitude, p.longitude, p.cover_image_url,
        GREATEST(
            ts_rank(p.search_vector_ar, plainto_tsquery('simple', query)),
            ts_rank(p.search_vector_en, plainto_tsquery('english', query)),
            similarity(p.name_ar, query),
            COALESCE(similarity(p.name_en, query), 0)
        ) * (1 + p.google_rating / 10.0) as relevance
    FROM places p
    WHERE p.is_active = true
        AND p.google_rating >= min_rating
        AND (cat IS NULL OR p.category = cat)
        AND (area IS NULL OR p.neighborhood = area)
        AND (
            p.search_vector_ar @@ plainto_tsquery('simple', query)
            OR p.search_vector_en @@ plainto_tsquery('english', query)
            OR p.name_ar % query  -- trigram similarity
            OR p.name_en % query
        )
    ORDER BY relevance DESC
    LIMIT max_results;
$$;
```

### 3.4 Row Level Security (RLS)

```sql
-- ================================================
-- Row Level Security Policies
-- ================================================

-- Places: everyone can read, only admin can write
ALTER TABLE places ENABLE ROW LEVEL SECURITY;

CREATE POLICY "places_read" ON places
    FOR SELECT TO authenticated, anon
    USING (is_active = true);

CREATE POLICY "places_admin_write" ON places
    FOR ALL TO authenticated
    USING (auth.jwt() ->> 'role' = 'admin');

-- Favorites: users own their favorites
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

CREATE POLICY "favorites_own" ON favorites
    FOR ALL TO authenticated
    USING (user_id = auth.uid());

-- Reviews: anyone reads, users write own
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

CREATE POLICY "reviews_read" ON reviews
    FOR SELECT TO authenticated, anon
    USING (true);

CREATE POLICY "reviews_own_write" ON reviews
    FOR INSERT TO authenticated
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "reviews_own_update" ON reviews
    FOR UPDATE TO authenticated
    USING (user_id = auth.uid());

-- Delivery prices: read-only for all
ALTER TABLE delivery_prices ENABLE ROW LEVEL SECURITY;

CREATE POLICY "delivery_read" ON delivery_prices
    FOR SELECT TO authenticated, anon
    USING (true);
```

---

## 4. PostGIS for Geolocation

### 4.1 Why PostGIS

| Feature | PostGIS | Alternative (Haversine in app) |
|---------|---------|-------------------------------|
| Accuracy | ✅ Geodesic (accounts for Earth's shape) | ⚠️ Approximate (flat Earth) |
| Performance | ✅ Spatial index (R-tree) — O(log n) | ❌ Full scan — O(n) |
| Bounding box | ✅ ST_DWithin (index-accelerated) | ❌ Manual calculation |
| Distance sort | ✅ ST_Distance + ORDER BY | ❌ Sort after filtering |
| Polygon search | ✅ ST_Within, ST_Intersects | ❌ Not feasible |
| 6,445 places | ✅ < 5ms query | ⚠️ ~50ms in-app |
| 100K places | ✅ < 10ms query | ❌ ~500ms in-app |

**Decision:** PostGIS for Phase 2+ server. For MVP, client-side Haversine (6,445 places is fine for in-app filtering).

### 4.2 MVP Alternative: Client-Side Distance

```swift
// For MVP — simple distance calculation
extension CachedPlace {
    func distance(from location: CLLocation) -> CLLocationDistance? {
        guard let lat = latitude, let lng = longitude else { return nil }
        let placeLocation = CLLocation(latitude: lat, longitude: lng)
        return location.distance(from: placeLocation) // meters
    }
}

// Filter nearby places (< 5km)
func nearbyPlaces(from location: CLLocation, radius: Double = 5000) -> [CachedPlace] {
    allPlaces
        .filter { place in
            guard let distance = place.distance(from: location) else { return false }
            return distance <= radius
        }
        .sorted { ($0.distance(from: location) ?? .infinity) < ($1.distance(from: location) ?? .infinity) }
}
```

**Performance:** Filtering 6,445 places by distance: ~10ms on iPhone 12+. Acceptable for MVP.

---

## 5. Data Migration Pipeline

### 5.1 places.json → Supabase (One-Time)

```python
# scripts/migrate-to-supabase.py
import json
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

with open('data/places.json') as f:
    places = json.load(f)

# Batch insert (500 at a time for Supabase limits)
for i in range(0, len(places), 500):
    batch = places[i:i+500]
    transformed = [transform_place(p) for p in batch]
    supabase.table('places').upsert(transformed).execute()

def transform_place(p):
    return {
        'id': p['id'],
        'name_ar': p['name_ar'],
        'name_en': p.get('name_en'),
        'category': p.get('category_en', 'other'),
        'category_ar': p.get('category', p.get('category_ar', '')),
        'neighborhood': p.get('neighborhood'),
        'neighborhood_en': p.get('neighborhood_en'),
        'description_ar': p.get('description_ar'),
        'google_rating': p.get('google_rating', 0),
        'price_range': p.get('price_range', p.get('price_level')),
        'latitude': p.get('lat'),
        'longitude': p.get('lng'),
        'google_maps_url': p.get('google_maps_url'),
        'tags': p.get('tags', []),
        'perfect_for': p.get('perfect_for', []),
        'audience': p.get('audience', []),
        'is_trending': p.get('trending', False),
        'is_new': p.get('is_new', False),
        'is_free': p.get('is_free', False),
        'data_sources': p.get('sources', []),
    }
```

### 5.2 Ongoing Sync: GitHub → Supabase

```yaml
# .github/workflows/sync-to-supabase.yml
name: Sync Data to Supabase
on:
  push:
    paths: ['data/places.json']
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/sync-to-supabase.py
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
```

### 5.3 Delta Sync: Supabase → iOS App

```swift
// SyncService.swift — Delta sync from Supabase
func deltaSync() async throws {
    let lastSync = UserDefaults.standard.object(forKey: "lastSyncDate") as? Date 
        ?? Date.distantPast
    
    // Fetch only updated places since last sync
    let response = try await supabase
        .from("places")
        .select()
        .greaterThan("updated_at", value: lastSync.iso8601String)
        .order("updated_at")
        .execute()
    
    let updatedPlaces = try JSONDecoder().decode([PlaceDTO].self, from: response.data)
    
    // Upsert into SwiftData
    let context = ModelContext(modelContainer)
    for dto in updatedPlaces {
        let descriptor = FetchDescriptor<CachedPlace>(
            predicate: #Predicate { $0.id == dto.id }
        )
        if let existing = try context.fetch(descriptor).first {
            existing.update(from: dto)
        } else {
            context.insert(CachedPlace(from: dto))
        }
    }
    try context.save()
    
    UserDefaults.standard.set(Date(), forKey: "lastSyncDate")
}
```

---

## 6. Database Comparison Matrix

### 6.1 Full Comparison

| Criteria | Bundled JSON | SQLite (SwiftData) | Supabase (PostgreSQL) | Firebase (Firestore) | CloudKit |
|----------|:-----------:|:-------------------:|:---------------------:|:--------------------:|:--------:|
| **Cost (MVP)** | $0 | $0 | $0 | $0 | $0 |
| **Cost (100K users)** | $0 | $0 | $75/mo | $200-1000/mo | $0-50 |
| **Setup time** | 5 min | 1 hour | 2 hours | 1 hour | 2 hours |
| **Offline support** | ✅ Full | ✅ Full | ⚠️ Manual | ✅ Built-in | ✅ Built-in |
| **Arabic FTS** | ⚠️ Manual | ⚠️ Basic | ✅ pg_trgm | ⚠️ Limited | ❌ |
| **Geospatial** | ❌ | ❌ | ✅ PostGIS | ⚠️ GeoFirestore | ⚠️ Basic |
| **Relational queries** | ❌ | ⚠️ Predicates | ✅ Full SQL | ❌ NoSQL | ❌ |
| **User auth** | ❌ | ❌ | ✅ GoTrue | ✅ Firebase Auth | ✅ Apple ID |
| **Real-time** | ❌ | ❌ | ✅ Realtime | ✅ Snapshots | ✅ Subscriptions |
| **Multi-platform** | iOS only | iOS only | ✅ Any | ✅ Any | Apple only |
| **Vendor lock-in** | None | None | Low (PostgreSQL) | High | Very High |
| **Data residency** | On-device | On-device | Choose region | Google decides | Apple decides |
| **Scalability** | 6,445 OK | 100K+ OK | Millions | Millions | Millions |
| **Complexity** | Very Low | Low | Medium | Medium | Medium |

### 6.2 Recommendation by Phase

| Phase | Primary | Secondary | Why |
|-------|---------|-----------|-----|
| **MVP** | Bundled JSON + SwiftData | GitHub raw CDN | Zero cost, zero setup, offline-first |
| **Phase 2** | Supabase PostgreSQL | SwiftData (cache) | SQL + PostGIS + Auth + predictable pricing |
| **Phase 3** | Supabase + Meilisearch | SwiftData + pgvector | Arabic search + AI recommendations |

---

## 7. Data Quality & Validation

### 7.1 Constraints

```sql
-- Database-level validation
ALTER TABLE places ADD CONSTRAINT valid_rating 
    CHECK (google_rating >= 0 AND google_rating <= 5);
    
ALTER TABLE places ADD CONSTRAINT valid_coordinates
    CHECK (
        (latitude IS NULL AND longitude IS NULL) OR
        (latitude BETWEEN 24.0 AND 26.0 AND longitude BETWEEN 45.0 AND 48.0)
    );  -- Riyadh bounding box

ALTER TABLE places ADD CONSTRAINT valid_price_range
    CHECK (price_range IN ('$', '$$', '$$$', '$$$$', NULL));
    
ALTER TABLE reviews ADD CONSTRAINT valid_review_rating
    CHECK (rating BETWEEN 1 AND 5);
```

### 7.2 Data Quality Score

```sql
-- Auto-compute completeness score
CREATE OR REPLACE FUNCTION compute_completeness(p places)
RETURNS DECIMAL AS $$
    SELECT (
        (CASE WHEN p.name_ar IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN p.name_en IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN p.description_ar IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN p.google_rating > 0 THEN 1 ELSE 0 END) +
        (CASE WHEN p.latitude IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN p.price_range IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN p.google_maps_url IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN p.cover_image_url IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN array_length(p.tags, 1) > 0 THEN 1 ELSE 0 END) +
        (CASE WHEN p.neighborhood IS NOT NULL THEN 1 ELSE 0 END)
    )::DECIMAL / 10.0;
$$ LANGUAGE sql IMMUTABLE;
```

---

## 8. Performance Benchmarks (Expected)

### 8.1 SwiftData (MVP)

| Operation | Expected Time | Notes |
|-----------|--------------|-------|
| Initial JSON parse (6,445) | < 2s | Background thread |
| SwiftData insert (6,445) | < 3s | Batch insert |
| Query by category | < 20ms | Index on category |
| Full-text search | < 50ms | localizedStandardContains |
| Nearby filter (haversine) | < 30ms | All places scanned |
| Pagination (20 results) | < 10ms | FetchDescriptor limit |
| Favorites CRUD | < 5ms | Simple insert/delete |

### 8.2 Supabase (Phase 2)

| Operation | Expected Time | Notes |
|-----------|--------------|-------|
| List places (paginated) | < 100ms | REST API + CDN |
| Search (pg_trgm + FTS) | < 150ms | Combined index |
| Nearby (PostGIS) | < 50ms | Spatial index |
| Place detail | < 80ms | Primary key lookup |
| Auth (OTP verify) | < 500ms | GoTrue service |
| Delivery prices | < 100ms | Indexed by place_id |

---

*This document covers the complete database design from MVP to scale. See MVP-PLAN.md for implementation order and INFRASTRUCTURE.md for hosting details.*
