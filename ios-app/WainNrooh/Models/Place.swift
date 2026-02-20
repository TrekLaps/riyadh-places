// Place.swift
// موديل المكان — الموديل الأساسي في التطبيق
// يتطابق مع بيانات places.json و جدول places في Supabase

import Foundation
import SwiftData
import CoreLocation

// MARK: - موديل المكان (من الـ API)

/// بيانات المكان كاملة — من Supabase
struct Place: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let name: String
    let nameEn: String?
    let category: PlaceCategory
    let neighborhood: String?
    let neighborhoodEn: String?
    let description: String?
    let rating: Double?
    let ratingCount: Int?
    let priceRange: String?
    let latitude: Double?
    let longitude: Double?
    let googleMapsUrl: String?
    let phone: String?
    let website: String?
    let instagram: String?
    let hours: String?
    let address: String?
    let coverImageUrl: String?
    let tags: [String]?
    let perfectFor: [String]?
    let features: PlaceFeatures?
    let isVerified: Bool?
    let createdAt: String?
    let updatedAt: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case name = "name_ar"
        case nameEn = "name_en"
        case category = "category_id"
        case neighborhood = "area_id"
        case neighborhoodEn = "area_en"
        case description = "description_ar"
        case rating = "rating_avg"
        case ratingCount = "rating_count"
        case priceRange = "price_range"
        case latitude
        case longitude
        case googleMapsUrl = "google_maps_url"
        case phone
        case website
        case instagram
        case hours
        case address = "address_ar"
        case coverImageUrl = "cover_image_url"
        case tags
        case perfectFor = "perfect_for"
        case features
        case isVerified = "is_verified"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
    
    // MARK: - حسابات مساعدة
    
    /// الإحداثيات كـ CLLocationCoordinate2D
    var coordinate: CLLocationCoordinate2D? {
        guard let lat = latitude, let lng = longitude else { return nil }
        return CLLocationCoordinate2D(latitude: lat, longitude: lng)
    }
    
    /// الموقع كـ CLLocation
    var location: CLLocation? {
        guard let lat = latitude, let lng = longitude else { return nil }
        return CLLocation(latitude: lat, longitude: lng)
    }
    
    /// المسافة من موقع معين (بالكيلومتر)
    func distance(from userLocation: CLLocation) -> Double? {
        guard let placeLocation = location else { return nil }
        return placeLocation.distance(from: userLocation) / 1000.0
    }
    
    /// نص المسافة المنسق
    func formattedDistance(from userLocation: CLLocation) -> String? {
        guard let km = distance(from: userLocation) else { return nil }
        if km < 1.0 {
            return "\(Int(km * 1000)) م"
        } else {
            return String(format: "%.1f كم", km)
        }
    }
    
    /// هل المكان مفتوح الحين؟ (تبسيط — يحتاج بيانات ساعات مفصلة)
    var isOpenNow: Bool? {
        // TODO: تنفيذ حقيقي مع بيانات الساعات المفصلة
        return nil
    }
    
    /// اسم العرض (عربي أو إنجليزي)
    var displayName: String {
        return name
    }
    
    /// رمز نطاق السعر ($ إلى $$$$)
    var priceSymbol: String {
        return priceRange ?? "$$"
    }
    
    // MARK: - Hashable
    
    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
    
    static func == (lhs: Place, rhs: Place) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - ميزات المكان

/// الميزات المتاحة في المكان
struct PlaceFeatures: Codable, Hashable, Sendable {
    let wifi: Bool?
    let parking: Bool?
    let families: Bool?
    let outdoor: Bool?
    let delivery: Bool?
    let reservations: Bool?
    let valet: Bool?
    let kidsArea: Bool?
    let shisha: Bool?
    let liveMusic: Bool?
    let privateRooms: Bool?
    
    enum CodingKeys: String, CodingKey {
        case wifi, parking, families, outdoor, delivery, reservations, valet
        case kidsArea = "kids_area"
        case shisha
        case liveMusic = "live_music"
        case privateRooms = "private_rooms"
    }
    
    /// قائمة الميزات المتوفرة كنصوص
    var availableFeatures: [(icon: String, label: String)] {
        var result: [(String, String)] = []
        if wifi == true { result.append(("wifi", "واي فاي")) }
        if parking == true { result.append(("car.fill", "مواقف")) }
        if families == true { result.append(("figure.2.and.child", "عوائل")) }
        if outdoor == true { result.append(("sun.max.fill", "جلسات خارجية")) }
        if delivery == true { result.append(("bicycle", "توصيل")) }
        if reservations == true { result.append(("calendar.badge.clock", "حجز")) }
        if valet == true { result.append(("key.fill", "فاليه")) }
        if kidsArea == true { result.append(("figure.child", "منطقة أطفال")) }
        if shisha == true { result.append(("smoke.fill", "شيشة")) }
        if liveMusic == true { result.append(("music.note", "موسيقى حية")) }
        if privateRooms == true { result.append(("door.left.hand.closed", "غرف خاصة")) }
        return result
    }
}

// MARK: - موديل المكان المحلي (SwiftData)

/// نسخة محلية من المكان — للتخزين في SwiftData (أوفلاين)
@Model
final class CachedPlace {
    @Attribute(.unique) var id: String
    var name: String
    var nameEn: String?
    var categoryId: String
    var neighborhood: String?
    var descriptionText: String?
    var rating: Double
    var ratingCount: Int
    var priceRange: String?
    var latitude: Double?
    var longitude: Double?
    var googleMapsUrl: String?
    var phone: String?
    var website: String?
    var instagram: String?
    var hours: String?
    var address: String?
    var coverImageUrl: String?
    var tagsData: Data?
    var perfectForData: Data?
    var featuresData: Data?
    var isVerified: Bool
    var lastSyncedAt: Date
    
    init(from place: Place) {
        self.id = place.id
        self.name = place.name
        self.nameEn = place.nameEn
        self.categoryId = place.category.rawValue
        self.neighborhood = place.neighborhood
        self.descriptionText = place.description
        self.rating = place.rating ?? 0
        self.ratingCount = place.ratingCount ?? 0
        self.priceRange = place.priceRange
        self.latitude = place.latitude
        self.longitude = place.longitude
        self.googleMapsUrl = place.googleMapsUrl
        self.phone = place.phone
        self.website = place.website
        self.instagram = place.instagram
        self.hours = place.hours
        self.address = place.address
        self.coverImageUrl = place.coverImageUrl
        self.tagsData = try? JSONEncoder().encode(place.tags)
        self.perfectForData = try? JSONEncoder().encode(place.perfectFor)
        self.featuresData = try? JSONEncoder().encode(place.features)
        self.isVerified = place.isVerified ?? false
        self.lastSyncedAt = Date()
    }
    
    /// تحويل من كاش إلى موديل Place
    func toPlace() -> Place {
        let tags = (try? JSONDecoder().decode([String].self, from: tagsData ?? Data())) ?? nil
        let perfectFor = (try? JSONDecoder().decode([String].self, from: perfectForData ?? Data())) ?? nil
        let features = try? JSONDecoder().decode(PlaceFeatures.self, from: featuresData ?? Data())
        
        return Place(
            id: id,
            name: name,
            nameEn: nameEn,
            category: PlaceCategory(rawValue: categoryId) ?? .restaurant,
            neighborhood: neighborhood,
            neighborhoodEn: nil,
            description: descriptionText,
            rating: rating,
            ratingCount: ratingCount,
            priceRange: priceRange,
            latitude: latitude,
            longitude: longitude,
            googleMapsUrl: googleMapsUrl,
            phone: phone,
            website: website,
            instagram: instagram,
            hours: hours,
            address: address,
            coverImageUrl: coverImageUrl,
            tags: tags,
            perfectFor: perfectFor,
            features: features,
            isVerified: isVerified,
            createdAt: nil,
            updatedAt: nil
        )
    }
    
    /// تحديث البيانات من Place جديد
    func update(from place: Place) {
        self.name = place.name
        self.nameEn = place.nameEn
        self.categoryId = place.category.rawValue
        self.neighborhood = place.neighborhood
        self.descriptionText = place.description
        self.rating = place.rating ?? 0
        self.ratingCount = place.ratingCount ?? 0
        self.priceRange = place.priceRange
        self.latitude = place.latitude
        self.longitude = place.longitude
        self.googleMapsUrl = place.googleMapsUrl
        self.phone = place.phone
        self.website = place.website
        self.instagram = place.instagram
        self.hours = place.hours
        self.address = place.address
        self.coverImageUrl = place.coverImageUrl
        self.tagsData = try? JSONEncoder().encode(place.tags)
        self.perfectForData = try? JSONEncoder().encode(place.perfectFor)
        self.featuresData = try? JSONEncoder().encode(place.features)
        self.isVerified = place.isVerified ?? false
        self.lastSyncedAt = Date()
    }
}

// MARK: - إجراء معلق (للأوفلاين)

/// إجراء معلق ينتظر الاتصال بالإنترنت
@Model
final class PendingAction {
    @Attribute(.unique) var id: String
    var actionType: String  // "favorite_add", "favorite_remove", "review_add"
    var targetId: String    // place_id
    var payload: Data?      // JSON data
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
