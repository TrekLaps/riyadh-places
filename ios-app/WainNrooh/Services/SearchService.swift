// SearchService.swift
// خدمة البحث — بحث AI بالعربي مع NLP

import Foundation
import Combine
import NaturalLanguage

// MARK: - خدمة البحث

/// خدمة البحث الذكي — بحث AI بالعربي مع فهم اللهجة السعودية
final class SearchService: ObservableObject, @unchecked Sendable {
    
    // MARK: - Singleton
    
    static let shared = SearchService()
    
    private let supabase = SupabaseService.shared
    private let decoder = JSONDecoder()
    
    // MARK: - البحث الأخير
    
    @Published var recentSearches: [String] = []
    @Published var popularSearches: [String] = [
        "قهوة مختصة",
        "مطعم ياباني",
        "حلويات",
        "مكان هادي للدراسة",
        "مطعم عوائل",
        "شيشة",
        "برنش",
        "آيسكريم"
    ]
    
    // MARK: - قاموس المرادفات السعودية
    
    /// مرادفات اللهجة السعودية → كلمات بحث قياسية
    private let saudiSynonyms: [String: [String]] = [
        "ابي": ["أريد", "أبغى", "أبي"],
        "ابغى": ["أريد", "أبغى", "أبي"],
        "وين": ["أين", "فين"],
        "هالحين": ["الآن", "الحين"],
        "زين": ["جيد", "ممتاز"],
        "حلو": ["جميل", "لذيذ", "ممتاز"],
        "رخيص": ["اقتصادي", "رخيص", "مناسب"],
        "غالي": ["فاخر", "غالي", "مرتفع"],
        "قريب": ["قريب", "بالجوار"],
        "هادي": ["هادئ", "سكيت", "ريلاكس"],
        "عائلي": ["عوائل", "عائلات", "فاميلي"],
        "شبابي": ["شباب", "أصدقاء"],
        "رومانسي": ["رومنسي", "كبلز", "ثنائي"],
        "فطور": ["إفطار", "فطور", "برنش", "breakfast"],
        "غدا": ["غداء", "لنش", "lunch"],
        "عشا": ["عشاء", "دنر", "dinner"],
        "كوفي": ["قهوة", "كافيه", "مقهى", "coffee"],
        "ريستورنت": ["مطعم", "restaurant"],
    ]
    
    /// تحويل الفئات من الكلمات
    private let categoryKeywords: [String: PlaceCategory] = [
        "مطعم": .restaurant,
        "مطاعم": .restaurant,
        "ريستورنت": .restaurant,
        "كافيه": .cafe,
        "كوفي": .cafe,
        "قهوة": .cafe,
        "مقهى": .cafe,
        "حلويات": .dessert,
        "كيك": .dessert,
        "آيسكريم": .dessert,
        "بيتزا": .fastFood,
        "برقر": .fastFood,
        "فاست فود": .fastFood,
        "فاخر": .fineDining,
        "فايندايننق": .fineDining,
        "ترفيه": .entertainment,
        "سينما": .cinema,
        "ألعاب": .gaming,
        "تسوق": .shopping,
        "مول": .mall,
        "عطور": .perfume,
        "سبا": .spa,
        "جيم": .gym,
        "فندق": .hotel,
    ]
    
    private init() {
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        loadRecentSearches()
    }
    
    // MARK: - البحث الرئيسي
    
    /// بحث ذكي بالعربي — يفهم اللهجة السعودية
    func search(
        query: String,
        category: PlaceCategory? = nil,
        neighborhood: String? = nil,
        latitude: Double? = nil,
        longitude: Double? = nil,
        radius: Double = AppConfig.defaultSearchRadius,
        sortBy: PlaceSortOption = .rating,
        page: Int = 1,
        perPage: Int = AppConfig.pageSize
    ) async throws -> SearchResult {
        // 1. تحليل النص العربي
        let parsed = parseArabicQuery(query)
        
        // 2. تحديد الفئة من الكلمات إذا ما تم تحديدها
        let effectiveCategory = category ?? parsed.detectedCategory
        
        // 3. تحديد الحي من الكلمات
        let effectiveNeighborhood = neighborhood ?? parsed.detectedNeighborhood
        
        // 4. البحث في Supabase
        let places: [Place] = try await supabase.rpc(
            functionName: "search_places",
            params: buildSearchParams(
                query: parsed.normalizedQuery,
                category: effectiveCategory,
                neighborhood: effectiveNeighborhood,
                latitude: latitude,
                longitude: longitude,
                radius: radius,
                page: page,
                perPage: perPage
            )
        )
        
        // 5. حفظ البحث الأخير
        addRecentSearch(query)
        
        return SearchResult(
            query: query,
            places: places,
            totalCount: places.count,
            detectedCategory: parsed.detectedCategory,
            detectedNeighborhood: parsed.detectedNeighborhood,
            suggestions: parsed.suggestions
        )
    }
    
    /// اقتراحات البحث التلقائي (autocomplete)
    func suggest(query: String) async throws -> [SearchSuggestion] {
        guard query.count >= AppConfig.minSearchLength else { return [] }
        
        let normalized = query.arabicNormalized
        var suggestions: [SearchSuggestion] = []
        
        // اقتراحات من البحث الشائع
        let matchingPopular = popularSearches.filter {
            $0.arabicNormalized.contains(normalized)
        }
        suggestions += matchingPopular.map {
            SearchSuggestion(text: $0, type: .popular)
        }
        
        // اقتراحات من التصنيفات
        let matchingCategories = PlaceCategory.allCases.filter {
            $0.nameAr.arabicNormalized.contains(normalized)
        }
        suggestions += matchingCategories.map {
            SearchSuggestion(text: $0.nameAr, type: .category, category: $0)
        }
        
        // اقتراحات من الأحياء
        let matchingNeighborhoods = Neighborhood.search(query: query)
        suggestions += matchingNeighborhoods.map {
            SearchSuggestion(text: $0.nameAr, type: .neighborhood)
        }
        
        return Array(suggestions.prefix(8))
    }
    
    // MARK: - تحليل النص العربي
    
    /// تحليل استعلام البحث العربي واستخراج المعلومات
    private func parseArabicQuery(_ query: String) -> ParsedQuery {
        let normalized = query.arabicNormalized.lowercased()
        let words = normalized.components(separatedBy: " ").filter { !$0.isEmpty }
        
        // استخراج الفئة
        var detectedCategory: PlaceCategory?
        for word in words {
            if let cat = categoryKeywords[word] {
                detectedCategory = cat
                break
            }
        }
        
        // استخراج الحي
        var detectedNeighborhood: String?
        let neighborhoods = Neighborhood.mainNeighborhoods
        for hood in neighborhoods {
            if normalized.contains(hood.nameAr.arabicNormalized.lowercased()) ||
               normalized.contains(hood.nameEn.lowercased()) {
                detectedNeighborhood = hood.id
                break
            }
        }
        
        // استخراج الميزات
        var features: [String] = []
        if normalized.contains("هادي") || normalized.contains("هادئ") { features.append("quiet") }
        if normalized.contains("واي فاي") || normalized.contains("wifi") { features.append("wifi") }
        if normalized.contains("عوائل") || normalized.contains("عائلي") { features.append("families") }
        if normalized.contains("خارجي") || normalized.contains("تراس") { features.append("outdoor") }
        if normalized.contains("مواقف") || normalized.contains("باركنق") { features.append("parking") }
        if normalized.contains("شيشة") { features.append("shisha") }
        
        // توسيع الاستعلام بالمرادفات
        var expandedWords: [String] = []
        for word in words {
            expandedWords.append(word)
            if let synonyms = saudiSynonyms[word] {
                expandedWords += synonyms
            }
        }
        
        // بناء الاستعلام المطبّع
        let searchableWords = expandedWords.filter { word in
            // إزالة كلمات التوقف
            !["ابي", "ابغى", "في", "من", "على", "عند", "فيه", "بـ", "ال"].contains(word)
        }
        
        return ParsedQuery(
            originalQuery: query,
            normalizedQuery: searchableWords.joined(separator: " "),
            detectedCategory: detectedCategory,
            detectedNeighborhood: detectedNeighborhood,
            features: features,
            suggestions: []
        )
    }
    
    /// بناء معاملات البحث لـ Supabase RPC
    private func buildSearchParams(
        query: String,
        category: PlaceCategory?,
        neighborhood: String?,
        latitude: Double?,
        longitude: Double?,
        radius: Double,
        page: Int,
        perPage: Int
    ) -> [String: Any] {
        var params: [String: Any] = [
            "search_query": query,
            "result_limit": perPage,
            "result_offset": (page - 1) * perPage
        ]
        
        if let category { params["cat_filter"] = category.rawValue }
        if let neighborhood { params["area_filter"] = neighborhood }
        if let lat = latitude { params["user_lat"] = lat }
        if let lng = longitude { params["user_lng"] = lng }
        if radius > 0 { params["search_radius"] = radius }
        
        return params
    }
    
    // MARK: - البحث الأخير
    
    /// إضافة بحث أخير
    private func addRecentSearch(_ query: String) {
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return }
        
        recentSearches.removeAll { $0 == trimmed }
        recentSearches.insert(trimmed, at: 0)
        
        if recentSearches.count > AppConfig.maxRecentSearches {
            recentSearches = Array(recentSearches.prefix(AppConfig.maxRecentSearches))
        }
        
        saveRecentSearches()
    }
    
    /// مسح البحث الأخير
    func clearRecentSearches() {
        recentSearches.removeAll()
        UserDefaults.standard.removeObject(forKey: "recentSearches")
    }
    
    /// تحميل البحث الأخير من التخزين
    private func loadRecentSearches() {
        recentSearches = UserDefaults.standard.stringArray(forKey: "recentSearches") ?? []
    }
    
    /// حفظ البحث الأخير
    private func saveRecentSearches() {
        UserDefaults.standard.set(recentSearches, forKey: "recentSearches")
    }
}

// MARK: - نتيجة البحث

/// نتيجة البحث
struct SearchResult: Sendable {
    let query: String
    let places: [Place]
    let totalCount: Int
    let detectedCategory: PlaceCategory?
    let detectedNeighborhood: String?
    let suggestions: [String]
}

// MARK: - اقتراح بحث

/// اقتراح بحث تلقائي
struct SearchSuggestion: Identifiable, Sendable {
    let id = UUID()
    let text: String
    let type: SuggestionType
    var category: PlaceCategory?
    
    enum SuggestionType: Sendable {
        case popular
        case category
        case neighborhood
        case recent
    }
    
    var icon: String {
        switch type {
        case .popular: return "flame.fill"
        case .category: return category?.icon ?? "tag.fill"
        case .neighborhood: return "mappin.circle.fill"
        case .recent: return "clock.fill"
        }
    }
}

// MARK: - استعلام محلل

/// نتيجة تحليل استعلام البحث
struct ParsedQuery {
    let originalQuery: String
    let normalizedQuery: String
    let detectedCategory: PlaceCategory?
    let detectedNeighborhood: String?
    let features: [String]
    let suggestions: [String]
}
