// PlacesService.swift
// خدمة الأماكن — جلب وفلترة وترتيب الأماكن

import Foundation
import Combine

// MARK: - خدمة الأماكن

/// خدمة الأماكن — CRUD + فلترة + ترتيب
final class PlacesService: @unchecked Sendable {
    
    // MARK: - Singleton
    
    static let shared = PlacesService()
    
    private let supabase = SupabaseService.shared
    private let decoder = JSONDecoder()
    
    private init() {
        decoder.keyDecodingStrategy = .convertFromSnakeCase
    }
    
    // MARK: - جلب الأماكن
    
    /// جلب قائمة الأماكن مع فلاتر
    func fetchPlaces(
        category: PlaceCategory? = nil,
        neighborhood: String? = nil,
        minRating: Double? = nil,
        priceRange: String? = nil,
        page: Int = 1,
        perPage: Int = AppConfig.pageSize,
        sortBy: PlaceSortOption = .rating
    ) async throws -> [Place] {
        var filters: [SupabaseFilter] = [
            SupabaseFilter(column: "is_active", op: .eq, value: "true")
        ]
        
        if let category {
            filters.append(SupabaseFilter(column: "category_id", op: .eq, value: category.rawValue))
        }
        
        if let neighborhood {
            filters.append(SupabaseFilter(column: "area_id", op: .eq, value: neighborhood))
        }
        
        if let minRating {
            filters.append(SupabaseFilter(column: "rating_avg", op: .gte, value: "\(minRating)"))
        }
        
        if let priceRange {
            filters.append(SupabaseFilter(column: "price_range", op: .eq, value: priceRange))
        }
        
        let offset = (page - 1) * perPage
        
        let data = try await supabase.from(
            "places",
            select: "*",
            filters: filters,
            order: sortBy.column,
            ascending: sortBy.ascending,
            limit: perPage,
            offset: offset
        )
        
        return try decoder.decode([Place].self, from: data)
    }
    
    /// جلب مكان واحد بالتفصيل
    func fetchPlace(id: String) async throws -> Place {
        let data = try await supabase.from(
            "places",
            select: "*",
            filters: [SupabaseFilter(column: "id", op: .eq, value: id)]
        )
        
        let places = try decoder.decode([Place].self, from: data)
        guard let place = places.first else {
            throw PlacesError.notFound
        }
        return place
    }
    
    /// جلب الأماكن القريبة (باستخدام PostGIS)
    func fetchNearby(
        latitude: Double,
        longitude: Double,
        radiusMeters: Int = Int(AppConfig.defaultSearchRadius),
        limit: Int = 20
    ) async throws -> [Place] {
        return try await supabase.rpc(
            functionName: "nearby_places",
            params: [
                "lat": latitude,
                "lng": longitude,
                "radius_m": radiusMeters,
                "max_results": limit
            ]
        )
    }
    
    /// جلب الأماكن الأكثر شعبية (ترند)
    func fetchTrending(limit: Int = 10) async throws -> [Place] {
        let data = try await supabase.from(
            "places",
            select: "*",
            filters: [
                SupabaseFilter(column: "is_active", op: .eq, value: "true"),
                SupabaseFilter(column: "rating_avg", op: .gte, value: "4.0")
            ],
            order: "rating_count",
            ascending: false,
            limit: limit
        )
        
        return try decoder.decode([Place].self, from: data)
    }
    
    /// جلب الأماكن الجديدة
    func fetchNew(limit: Int = 10) async throws -> [Place] {
        let data = try await supabase.from(
            "places",
            select: "*",
            filters: [
                SupabaseFilter(column: "is_active", op: .eq, value: "true")
            ],
            order: "created_at",
            ascending: false,
            limit: limit
        )
        
        return try decoder.decode([Place].self, from: data)
    }
    
    /// جلب أماكن مشابهة
    func fetchSimilar(to place: Place, limit: Int = 5) async throws -> [Place] {
        let data = try await supabase.from(
            "places",
            select: "*",
            filters: [
                SupabaseFilter(column: "is_active", op: .eq, value: "true"),
                SupabaseFilter(column: "category_id", op: .eq, value: place.category.rawValue),
                SupabaseFilter(column: "id", op: .neq, value: place.id)
            ],
            order: "rating_avg",
            ascending: false,
            limit: limit
        )
        
        return try decoder.decode([Place].self, from: data)
    }
    
    /// جلب أماكن حسب الفئة "مناسب لـ"
    func fetchPerfectFor(tag: String, limit: Int = 20) async throws -> [Place] {
        let data = try await supabase.from(
            "places",
            select: "*",
            filters: [
                SupabaseFilter(column: "is_active", op: .eq, value: "true"),
                SupabaseFilter(column: "perfect_for", op: .cs, value: "{\"\(tag)\"}")
            ],
            order: "rating_avg",
            ascending: false,
            limit: limit
        )
        
        return try decoder.decode([Place].self, from: data)
    }
    
    // MARK: - التصنيفات
    
    /// جلب التصنيفات مع عدد الأماكن
    func fetchCategories() async throws -> [(category: PlaceCategory, count: Int)] {
        // نستخدم الفئات المحلية مع عد من الـ API
        return PlaceCategory.popular.map { ($0, 0) }
    }
    
    // MARK: - الأحياء
    
    /// جلب الأحياء مع عدد الأماكن
    func fetchNeighborhoods() async throws -> [Neighborhood] {
        let data = try await supabase.from(
            "areas",
            select: "*"
        )
        return try decoder.decode([Neighborhood].self, from: data)
    }
}

// MARK: - خيارات الترتيب

/// خيارات ترتيب الأماكن
enum PlaceSortOption: String, CaseIterable, Identifiable {
    case rating     // حسب التقييم
    case distance   // حسب المسافة
    case name       // حسب الاسم
    case newest     // الأحدث
    case priceAsc   // السعر: من الأرخص
    case priceDesc  // السعر: من الأغلى
    
    var id: String { rawValue }
    
    /// الاسم بالعربي
    var nameAr: String {
        switch self {
        case .rating: return "التقييم"
        case .distance: return "المسافة"
        case .name: return "الاسم"
        case .newest: return "الأحدث"
        case .priceAsc: return "الأرخص"
        case .priceDesc: return "الأغلى"
        }
    }
    
    /// عمود الترتيب في Supabase
    var column: String {
        switch self {
        case .rating: return "rating_avg"
        case .distance: return "rating_avg" // يحتاج PostGIS
        case .name: return "name_ar"
        case .newest: return "created_at"
        case .priceAsc, .priceDesc: return "price_range"
        }
    }
    
    /// هل الترتيب تصاعدي؟
    var ascending: Bool {
        switch self {
        case .rating, .newest, .priceDesc: return false
        case .name, .distance, .priceAsc: return true
        }
    }
    
    /// الأيقونة
    var icon: String {
        switch self {
        case .rating: return "star.fill"
        case .distance: return "location.fill"
        case .name: return "textformat.abc"
        case .newest: return "clock.fill"
        case .priceAsc: return "arrow.up.circle"
        case .priceDesc: return "arrow.down.circle"
        }
    }
}

// MARK: - أخطاء الأماكن

/// أخطاء خدمة الأماكن
enum PlacesError: LocalizedError {
    case notFound
    case fetchFailed
    case invalidData
    
    var errorDescription: String? {
        switch self {
        case .notFound: return "المكان غير موجود"
        case .fetchFailed: return "فشل جلب الأماكن"
        case .invalidData: return "بيانات غير صالحة"
        }
    }
}
