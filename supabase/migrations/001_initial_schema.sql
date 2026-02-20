-- Migration 001: Initial Schema — وين نروح بالرياض
-- PostgreSQL + PostGIS for geographic queries
-- Arabic full-text search support

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ==========================================
-- Categories
-- ==========================================
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT UNIQUE NOT NULL,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    icon TEXT,
    color TEXT,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO categories (slug, name_ar, name_en, icon, sort_order) VALUES
('restaurant', 'مطعم', 'Restaurant', '🍽️', 1),
('cafe', 'كافيه', 'Cafe', '☕', 2),
('entertainment', 'ترفيه', 'Entertainment', '🎮', 3),
('dessert', 'حلويات', 'Desserts', '🍰', 4),
('shopping', 'تسوق', 'Shopping', '🛍️', 5),
('nature', 'طبيعة', 'Nature', '🌿', 6),
('hotel', 'فنادق', 'Hotels', '🏨', 7),
('chalet', 'شاليه', 'Chalet', '🏡', 8),
('museum', 'متاحف', 'Museums', '🏛️', 9),
('event', 'فعاليات', 'Events', '🎉', 10),
('mall', 'مولات', 'Malls', '🏬', 11),
('perfume', 'عطور', 'Perfumes', '🧴', 12);

-- ==========================================
-- Neighborhoods
-- ==========================================
CREATE TABLE neighborhoods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT UNIQUE NOT NULL,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    location GEOGRAPHY(POINT, 4326),
    bounds GEOGRAPHY(POLYGON, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- Places (core table)
-- ==========================================
CREATE TABLE places (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    name_en TEXT,
    category_slug TEXT REFERENCES categories(slug),
    neighborhood_slug TEXT REFERENCES neighborhoods(slug),
    
    -- Location
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    location GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (
        ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography
    ) STORED,
    google_maps_url TEXT,
    address TEXT,
    
    -- Details
    rating DOUBLE PRECISION,
    rating_count INT,
    price_range TEXT,  -- '$', '$$', '$$$', '$$$$'
    avg_price_per_person INT,  -- SAR
    phone TEXT,
    website TEXT,
    instagram TEXT,
    hours JSONB,  -- {"mon": "9:00-23:00", ...}
    
    -- Tags & Discovery
    tags TEXT[] DEFAULT '{}',
    perfect_for TEXT[] DEFAULT '{}',  -- رومانسي، عوائل، شباب، عمل
    cuisine TEXT,  -- ياباني، إيطالي، سعودي...
    
    -- Media
    image_url TEXT,
    images TEXT[] DEFAULT '{}',
    
    -- Metadata
    source TEXT,
    verified BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Arabic full-text search index
CREATE INDEX idx_places_search ON places USING GIN (
    to_tsvector('simple', coalesce(name, '') || ' ' || coalesce(name_en, '') || ' ' || coalesce(cuisine, '') || ' ' || coalesce(address, ''))
);

-- Geographic index for "nearby" queries
CREATE INDEX idx_places_location ON places USING GIST (location);

-- Category + active index
CREATE INDEX idx_places_category ON places (category_slug) WHERE active = TRUE;

-- Rating index for "top rated"
CREATE INDEX idx_places_rating ON places (rating DESC NULLS LAST) WHERE active = TRUE;

-- ==========================================
-- Delivery Apps
-- ==========================================
CREATE TABLE delivery_apps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT UNIQUE NOT NULL,
    name_ar TEXT NOT NULL,
    name_en TEXT NOT NULL,
    website TEXT,
    logo_url TEXT,
    typical_delivery_fee TEXT,
    min_order INT,
    color TEXT,
    sort_order INT DEFAULT 0,
    active BOOLEAN DEFAULT TRUE
);

INSERT INTO delivery_apps (slug, name_ar, name_en, website, color, sort_order) VALUES
('hungerstation', 'هنقرستيشن', 'HungerStation', 'hungerstation.com', '#FF5722', 1),
('jahez', 'جاهز', 'Jahez', 'jahez.net', '#00C853', 2),
('toyou', 'تويو', 'ToYou', 'toyou.io', '#2196F3', 3),
('carriage', 'كاريدج', 'Carriage', 'trycarriage.com', '#9C27B0', 4),
('thechefz', 'ذا شفز', 'The Chefz', 'thechefz.me', '#FF9800', 5),
('keeta', 'كيتا', 'Keeta', 'keeta.com', '#E91E63', 6),
('ninja', 'نينجا', 'Ninja', 'ninja.sa', '#607D8B', 7),
('mrsool', 'مرسول', 'Mrsool', 'mrsool.co', '#4CAF50', 8);

-- ==========================================
-- Delivery Prices (the killer feature)
-- ==========================================
CREATE TABLE delivery_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id UUID REFERENCES places(id) ON DELETE CASCADE,
    app_slug TEXT REFERENCES delivery_apps(slug),
    available BOOLEAN DEFAULT TRUE,
    delivery_fee_min INT,  -- SAR
    delivery_fee_max INT,  -- SAR
    min_order INT,
    estimated_time TEXT,  -- "25-35 min"
    rating DOUBLE PRECISION,
    source_url TEXT,
    last_checked TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(place_id, app_slug)
);

CREATE INDEX idx_delivery_place ON delivery_prices (place_id);

-- ==========================================
-- Menu Items (real prices in SAR)
-- ==========================================
CREATE TABLE menu_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id UUID REFERENCES places(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    name_en TEXT,
    price INT NOT NULL,  -- SAR
    size TEXT,  -- عادي، كبير، وسط
    category TEXT,  -- مقبلات، رئيسي، حلى، مشروبات
    image_url TEXT,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_menu_place ON menu_items (place_id);

-- ==========================================
-- Perfume Shops (new category!)
-- ==========================================
CREATE TABLE perfume_shops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id UUID REFERENCES places(id),
    brand TEXT NOT NULL,
    brand_en TEXT,
    website TEXT,
    price_range_min INT,
    price_range_max INT,
    speciality TEXT,  -- عود، بخور، عطور غربية...
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- Perfume Comparisons
-- ==========================================
CREATE TABLE perfumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    size_ml INT,
    notes TEXT[],  -- oud, rose, amber...
    fragrantica_rating DOUBLE PRECISION,
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE perfume_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    perfume_id UUID REFERENCES perfumes(id) ON DELETE CASCADE,
    shop_name TEXT NOT NULL,
    price INT NOT NULL,  -- SAR
    url TEXT,
    last_checked TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(perfume_id, shop_name)
);

CREATE TABLE perfume_alternatives (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_perfume_id UUID REFERENCES perfumes(id),
    alternative_name TEXT NOT NULL,
    alternative_brand TEXT,
    alternative_price INT,  -- SAR
    similarity_percent INT,  -- 1-100
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- User Favorites (local first, sync later)
-- ==========================================
CREATE TABLE favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,  -- future: Supabase Auth
    place_id UUID REFERENCES places(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id, place_id)
);

-- ==========================================
-- Functions
-- ==========================================

-- Search places (Arabic + English)
CREATE OR REPLACE FUNCTION search_places(
    query TEXT,
    category_filter TEXT DEFAULT NULL,
    max_price INT DEFAULT NULL,
    lat DOUBLE PRECISION DEFAULT NULL,
    lng DOUBLE PRECISION DEFAULT NULL,
    radius_km INT DEFAULT 10,
    limit_count INT DEFAULT 50
)
RETURNS TABLE (
    id UUID,
    name TEXT,
    category_slug TEXT,
    rating DOUBLE PRECISION,
    avg_price_per_person INT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    distance_km DOUBLE PRECISION,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.name,
        p.category_slug,
        p.rating,
        p.avg_price_per_person,
        p.latitude,
        p.longitude,
        CASE WHEN lat IS NOT NULL AND lng IS NOT NULL 
            THEN ST_Distance(p.location, ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography) / 1000
            ELSE NULL
        END as distance_km,
        ts_rank(
            to_tsvector('simple', coalesce(p.name, '') || ' ' || coalesce(p.name_en, '') || ' ' || coalesce(p.cuisine, '')),
            plainto_tsquery('simple', query)
        ) as rank
    FROM places p
    WHERE p.active = TRUE
        AND (category_filter IS NULL OR p.category_slug = category_filter)
        AND (max_price IS NULL OR p.avg_price_per_person <= max_price)
        AND (lat IS NULL OR lng IS NULL OR 
            ST_DWithin(p.location, ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography, radius_km * 1000))
        AND (query = '' OR to_tsvector('simple', coalesce(p.name, '') || ' ' || coalesce(p.name_en, '') || ' ' || coalesce(p.cuisine, ''))
            @@ plainto_tsquery('simple', query))
    ORDER BY rank DESC, p.rating DESC NULLS LAST
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Get nearby places
CREATE OR REPLACE FUNCTION nearby_places(
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    radius_km INT DEFAULT 5,
    category_filter TEXT DEFAULT NULL,
    limit_count INT DEFAULT 20
)
RETURNS TABLE (
    id UUID,
    name TEXT,
    category_slug TEXT,
    rating DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    distance_km DOUBLE PRECISION
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.name,
        p.category_slug,
        p.rating,
        p.latitude,
        p.longitude,
        ST_Distance(p.location, ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography) / 1000 as distance_km
    FROM places p
    WHERE p.active = TRUE
        AND (category_filter IS NULL OR p.category_slug = category_filter)
        AND ST_DWithin(p.location, ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography, radius_km * 1000)
    ORDER BY distance_km ASC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Compare delivery prices for a place
CREATE OR REPLACE FUNCTION compare_delivery(place_uuid UUID)
RETURNS TABLE (
    app_slug TEXT,
    app_name_ar TEXT,
    available BOOLEAN,
    delivery_fee_min INT,
    delivery_fee_max INT,
    min_order INT,
    estimated_time TEXT,
    rating DOUBLE PRECISION
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        da.slug,
        da.name_ar,
        dp.available,
        dp.delivery_fee_min,
        dp.delivery_fee_max,
        dp.min_order,
        dp.estimated_time,
        dp.rating
    FROM delivery_apps da
    LEFT JOIN delivery_prices dp ON dp.app_slug = da.slug AND dp.place_id = place_uuid
    WHERE da.active = TRUE
    ORDER BY da.sort_order;
END;
$$ LANGUAGE plpgsql;

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER places_updated_at
    BEFORE UPDATE ON places
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ==========================================
-- Row Level Security (RLS)
-- ==========================================
ALTER TABLE places ENABLE ROW LEVEL SECURITY;
ALTER TABLE delivery_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE menu_items ENABLE ROW LEVEL SECURITY;

-- Public read access (no auth needed for reading)
CREATE POLICY "Public read places" ON places FOR SELECT USING (true);
CREATE POLICY "Public read delivery" ON delivery_prices FOR SELECT USING (true);
CREATE POLICY "Public read menu" ON menu_items FOR SELECT USING (true);
CREATE POLICY "Public read perfumes" ON perfumes FOR SELECT USING (true);
CREATE POLICY "Public read perfume_prices" ON perfume_prices FOR SELECT USING (true);

-- Done!
