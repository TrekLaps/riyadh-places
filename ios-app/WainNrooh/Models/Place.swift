// Place.swift
// موديل المكان — يطابق places.json بالضبط
// Updated: 2026-02-21 — HS Super App Pattern

import Foundation
import SwiftData
import CoreLocation

// MARK: - Place (من places.json)

/// بيانات المكان — تطابق places.json بالضبط
struct Place: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let nameAr: String
    let nameEn: String?
    let category: String
    let categoryAr: String?
    let categoryEn: String?
    let neighborhood: String?
    let neighborhoodEn: String?
    let descriptionAr: String?
    let googleRating: Double?
    let ratingSource: String?  // "google" | "not_applicable" | "pending"
    let priceLevel: String?    // $ | $$ | $$$ | $$$$
    let priceRange: String?
    let lat: Double?
    let lng: Double?
    let googleMapsUrl: String?
    let phone: String?
    let openingHours: String?
    let address: String?
    let district: String?
    let tags: [String]?
    let perfectFor: [String]?
    let audience: [String]?
    let sources: [String]?
    let isNew: Bool?
    let trending: Bool?
    let isFree: Bool?
    
    enum CodingKeys: String, CodingKey {
        case id
        case nameAr = "name_ar"
        case nameEn = "name_en"
        case category
        case categoryAr = "category_ar"
        case categoryEn = "category_en"
        case neighborhood
        case neighborhoodEn = "neighborhood_en"
        case descriptionAr = "description_ar"
        case googleRating = "google_rating"
        case ratingSource = "rating_source"
        case priceLevel = "price_level"
        case priceRange = "price_range"
        case lat, lng
        case googleMapsUrl = "google_maps_url"
        case phone
        case openingHours = "opening_hours"
        case address
        case district
        case tags
        case perfectFor = "perfect_for"
        case audience
        case sources
        case isNew = "is_new"
        case trending
        case isFree = "is_free"
    }
    
    // MARK: - Computed Properties
    
    var displayName: String { nameAr }
    
    var coordinate: CLLocationCoordinate2D? {
        guard let lat, let lng, lng > 40 else { return nil }
        return CLLocationCoordinate2D(latitude: lat, longitude: lng)
    }
    
    var location: CLLocation? {
        guard let lat, let lng, lng > 40 else { return nil }
        return CLLocation(latitude: lat, longitude: lng)
    }
    
    func distance(from userLocation: CLLocation) -> Double? {
        guard let loc = location else { return nil }
        return loc.distance(from: userLocation) / 1000.0
    }
    
    func formattedDistance(from userLocation: CLLocation) -> String? {
        guard let km = distance(from: userLocation) else { return nil }
        return km < 1.0 ? "\(Int(km * 1000)) م" : String(format: "%.1f كم", km)
    }
    
    var hasVerifiedRating: Bool {
        ratingSource == "google" && googleRating != nil
    }
    
    /// تقييم Tabelog-style: 3.5 = ممتاز
    var ratingLabel: String? {
        guard let r = googleRating else { return nil }
        if r >= 4.5 { return "استثنائي" }
        if r >= 4.0 { return "ممتاز" }
        if r >= 3.5 { return "جيد جداً" }
        if r >= 3.0 { return "جيد" }
        return "مقبول"
    }
    
    /// Multi-dimensional rating (derived from google_rating)
    var ratingDimensions: RatingDimensions {
        let base = googleRating ?? 3.5
        return RatingDimensions(
            quality: min(5, base + 0.1),
            service: min(5, base - 0.2),
            ambiance: min(5, base + 0.05),
            value: min(5, base - 0.1)
        )
    }
    
    /// Occasion matching
    var occasions: [Occasion] {
        var result: [Occasion] = []
        let pf = Set(perfectFor ?? [])
        let t = Set(tags ?? [])
        if pf.contains("families") || t.contains("عائلي") { result.append(.family) }
        if pf.contains("couples") || t.contains("رومانسي") { result.append(.romantic) }
        if pf.contains("friends") || t.contains("شباب") { result.append(.friends) }
        if pf.contains("work") || t.contains("بزنس") { result.append(.business) }
        if pf.contains("quiet") || t.contains("هادئ") { result.append(.quiet) }
        return result
    }
    
    // MARK: - Hashable
    func hash(into hasher: inout Hasher) { hasher.combine(id) }
    static func == (lhs: Place, rhs: Place) -> Bool { lhs.id == rhs.id }
}

// MARK: - Rating Dimensions (Tabelog-style)

struct RatingDimensions: Codable, Sendable {
    let quality: Double   // جودة الطعام/الخدمة
    let service: Double   // الخدمة
    let ambiance: Double  // الأجواء
    let value: Double     // القيمة مقابل السعر
    
    var average: Double {
        (quality + service + ambiance + value) / 4.0
    }
}

// MARK: - Occasion Types

enum Occasion: String, CaseIterable, Identifiable, Codable {
    case family = "family"
    case romantic = "romantic"
    case friends = "friends"
    case business = "business"
    case quiet = "quiet"
    
    var id: String { rawValue }
    
    var nameAr: String {
        switch self {
        case .family: return "عائلي"
        case .romantic: return "رومانسي"
        case .friends: return "سهرة شباب"
        case .business: return "بزنس"
        case .quiet: return "قعدة هادية"
        }
    }
    
    var icon: String {
        switch self {
        case .family: return "figure.2.and.child"
        case .romantic: return "heart.fill"
        case .friends: return "person.3.fill"
        case .business: return "briefcase.fill"
        case .quiet: return "leaf.fill"
        }
    }
    
    var emoji: String {
        switch self {
        case .family: return "👨‍👩‍👧‍👦"
        case .romantic: return "💑"
        case .friends: return "🌙"
        case .business: return "💼"
        case .quiet: return "☕"
        }
    }
}

// MARK: - CachedPlace (SwiftData — Offline Storage)

@Model
final class CachedPlace {
    @Attribute(.unique) var id: String
    var nameAr: String
    var nameEn: String?
    var category: String
    var categoryAr: String?
    var categoryEn: String?
    var neighborhood: String?
    var descriptionAr: String?
    var googleRating: Double
    var ratingSource: String?
    var priceLevel: String?
    var lat: Double?
    var lng: Double?
    var googleMapsUrl: String?
    var phone: String?
    var openingHours: String?
    var address: String?
    var tagsData: Data?
    var perfectForData: Data?
    var isNew: Bool
    var trending: Bool
    var lastSyncedAt: Date
    
    init(from place: Place) {
        self.id = place.id
        self.nameAr = place.nameAr
        self.nameEn = place.nameEn
        self.category = place.category
        self.categoryAr = place.categoryAr
        self.categoryEn = place.categoryEn
        self.neighborhood = place.neighborhood
        self.descriptionAr = place.descriptionAr
        self.googleRating = place.googleRating ?? 0
        self.ratingSource = place.ratingSource
        self.priceLevel = place.priceLevel
        self.lat = place.lat
        self.lng = place.lng
        self.googleMapsUrl = place.googleMapsUrl
        self.phone = place.phone
        self.openingHours = place.openingHours
        self.address = place.address
        self.tagsData = try? JSONEncoder().encode(place.tags)
        self.perfectForData = try? JSONEncoder().encode(place.perfectFor)
        self.isNew = place.isNew ?? false
        self.trending = place.trending ?? false
        self.lastSyncedAt = Date()
    }
    
    func toPlace() -> Place {
        let tags = (try? JSONDecoder().decode([String].self, from: tagsData ?? Data())) ?? []
        let perfectFor = (try? JSONDecoder().decode([String].self, from: perfectForData ?? Data())) ?? []
        
        return Place(
            id: id, nameAr: nameAr, nameEn: nameEn,
            category: category, categoryAr: categoryAr, categoryEn: categoryEn,
            neighborhood: neighborhood, neighborhoodEn: nil,
            descriptionAr: descriptionAr,
            googleRating: googleRating > 0 ? googleRating : nil,
            ratingSource: ratingSource, priceLevel: priceLevel, priceRange: priceLevel,
            lat: lat, lng: lng, googleMapsUrl: googleMapsUrl,
            phone: phone, openingHours: openingHours, address: address,
            district: nil, tags: tags, perfectFor: perfectFor,
            audience: nil, sources: nil, isNew: isNew, trending: trending, isFree: nil
        )
    }
}

// MARK: - Pending Action (Offline Queue)

@Model
final class PendingAction {
    @Attribute(.unique) var id: String
    var actionType: String
    var targetId: String
    var payload: Data?
    var createdAt: Date
    var retryCount: Int
    
    init(actionType: String, targetId: String, payload: Data? = nil) {
        self.id = UUID().uuidString
        self.actionType = actionType
        self.targetId = targetId
        self.payload = payload
        self.createdAt = Date()
        self.retryCount = 0
    }
}
