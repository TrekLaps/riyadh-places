// DeliveryPrice.swift
// موديل أسعار التوصيل — مقارنة 8+ تطبيقات توصيل

import Foundation
import SwiftUI
import SwiftData

// MARK: - تطبيقات التوصيل

/// تطبيقات التوصيل المدعومة (8 تطبيقات)
enum DeliveryApp: String, Codable, CaseIterable, Identifiable, Sendable {
    case hungerstation = "hungerstation"
    case jahez = "jahez"
    case toyou = "toyou"
    case carriage = "carriage"
    case theChefs = "the_chefs"
    case keeta = "keeta"
    case ninja = "ninja"
    case marsool = "marsool"
    
    var id: String { rawValue }
    
    /// الاسم بالعربي
    var nameAr: String {
        switch self {
        case .hungerstation: return "هنقرستيشن"
        case .jahez: return "جاهز"
        case .toyou: return "تويو"
        case .carriage: return "كاريدج"
        case .theChefs: return "ذا شفز"
        case .keeta: return "كيتا"
        case .ninja: return "نينجا"
        case .marsool: return "مرسول"
        }
    }
    
    /// الاسم بالإنجليزي
    var nameEn: String {
        switch self {
        case .hungerstation: return "HungerStation"
        case .jahez: return "Jahez"
        case .toyou: return "ToYou"
        case .carriage: return "Carriage"
        case .theChefs: return "The Chefs"
        case .keeta: return "Keeta"
        case .ninja: return "Ninja"
        case .marsool: return "Marsool"
        }
    }
    
    /// لون التطبيق الرسمي
    var brandColor: Color {
        switch self {
        case .hungerstation: return Color(hex: "D4145A")
        case .jahez: return Color(hex: "FF6B00")
        case .toyou: return Color(hex: "00B894")
        case .carriage: return Color(hex: "FF4757")
        case .theChefs: return Color(hex: "1E1E1E")
        case .keeta: return Color(hex: "00D4AA")
        case .ninja: return Color(hex: "2ECC71")
        case .marsool: return Color(hex: "FFD700")
        }
    }
    
    /// أيقونة التطبيق (SF Symbol كـ placeholder)
    var iconName: String {
        switch self {
        case .hungerstation: return "h.circle.fill"
        case .jahez: return "j.circle.fill"
        case .toyou: return "t.circle.fill"
        case .carriage: return "c.circle.fill"
        case .theChefs: return "frying.pan.fill"
        case .keeta: return "k.circle.fill"
        case .ninja: return "n.circle.fill"
        case .marsool: return "m.circle.fill"
        }
    }
    
    /// رابط التطبيق في App Store
    var appStoreUrl: String {
        switch self {
        case .hungerstation: return "https://apps.apple.com/sa/app/hungerstation/id482aborto"
        case .jahez: return "https://apps.apple.com/sa/app/jahez/id1445aborto"
        case .toyou: return "https://apps.apple.com/sa/app/toyou/id1234567890"
        case .carriage: return "https://apps.apple.com/sa/app/carriage/id1234567890"
        case .theChefs: return "https://apps.apple.com/sa/app/the-chefs/id1234567890"
        case .keeta: return "https://apps.apple.com/sa/app/keeta/id1234567890"
        case .ninja: return "https://apps.apple.com/sa/app/ninja/id1234567890"
        case .marsool: return "https://apps.apple.com/sa/app/marsool/id1234567890"
        }
    }
    
    /// Deep link scheme
    var deeplinkScheme: String {
        switch self {
        case .hungerstation: return "hungerstation://"
        case .jahez: return "jahez://"
        case .toyou: return "toyou://"
        case .carriage: return "carriage://"
        case .theChefs: return "thechefs://"
        case .keeta: return "keeta://"
        case .ninja: return "ninja://"
        case .marsool: return "marsool://"
        }
    }
}

// MARK: - سعر التوصيل

/// سعر التوصيل لمكان معين من تطبيق معين
struct DeliveryPrice: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let placeId: String
    let app: DeliveryApp
    let deliveryFee: Double
    let minOrder: Double?
    let estimatedTimeMin: Int?
    let isAvailable: Bool
    let deeplinkUrl: String?
    let scrapedAt: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case placeId = "place_id"
        case app = "app_id"
        case deliveryFee = "delivery_fee"
        case minOrder = "min_order"
        case estimatedTimeMin = "estimated_time"
        case isAvailable = "is_available"
        case deeplinkUrl = "deeplink_url"
        case scrapedAt = "scraped_at"
    }
    
    /// سعر التوصيل المنسق بالريال
    var formattedFee: String {
        if deliveryFee == 0 {
            return "مجاني"
        }
        return "\(Int(deliveryFee)) ر.س"
    }
    
    /// الحد الأدنى للطلب المنسق
    var formattedMinOrder: String? {
        guard let min = minOrder else { return nil }
        return "الحد الأدنى: \(Int(min)) ر.س"
    }
    
    /// وقت التوصيل المتوقع المنسق
    var formattedTime: String? {
        guard let time = estimatedTimeMin else { return nil }
        if time < 60 {
            return "\(time) دقيقة"
        } else {
            let hours = time / 60
            let mins = time % 60
            return mins > 0 ? "\(hours) ساعة و \(mins) دقيقة" : "\(hours) ساعة"
        }
    }
}

// MARK: - نتيجة المقارنة

/// نتيجة مقارنة أسعار التوصيل لمكان واحد
struct DeliveryComparison: Sendable {
    let placeId: String
    let placeName: String
    let prices: [DeliveryPrice]
    let lastUpdated: Date?
    
    /// الأرخص
    var cheapest: DeliveryPrice? {
        prices
            .filter { $0.isAvailable }
            .min(by: { $0.deliveryFee < $1.deliveryFee })
    }
    
    /// الأسرع
    var fastest: DeliveryPrice? {
        prices
            .filter { $0.isAvailable && $0.estimatedTimeMin != nil }
            .min(by: { ($0.estimatedTimeMin ?? 999) < ($1.estimatedTimeMin ?? 999) })
    }
    
    /// الأسعار مرتبة من الأرخص للأغلى
    var sortedByPrice: [DeliveryPrice] {
        prices
            .filter { $0.isAvailable }
            .sorted(by: { $0.deliveryFee < $1.deliveryFee })
    }
    
    /// الأسعار مرتبة من الأسرع
    var sortedByTime: [DeliveryPrice] {
        prices
            .filter { $0.isAvailable && $0.estimatedTimeMin != nil }
            .sorted(by: { ($0.estimatedTimeMin ?? 999) < ($1.estimatedTimeMin ?? 999) })
    }
    
    /// متوسط سعر التوصيل
    var averageFee: Double {
        let available = prices.filter { $0.isAvailable }
        guard !available.isEmpty else { return 0 }
        return available.reduce(0) { $0 + $1.deliveryFee } / Double(available.count)
    }
    
    /// الفرق بين الأرخص والأغلى
    var priceDifference: Double? {
        let available = prices.filter { $0.isAvailable }
        guard let min = available.min(by: { $0.deliveryFee < $1.deliveryFee }),
              let max = available.max(by: { $0.deliveryFee < $1.deliveryFee }) else {
            return nil
        }
        return max.deliveryFee - min.deliveryFee
    }
    
    /// كم ممكن توفر؟
    var savingsText: String? {
        guard let diff = priceDifference, diff > 0 else { return nil }
        return "وفّر \(Int(diff)) ر.س"
    }
}

// MARK: - كاش سعر التوصيل (SwiftData)

/// نسخة محلية من سعر التوصيل
@Model
final class CachedDeliveryPrice {
    @Attribute(.unique) var id: String
    var placeId: String
    var appId: String
    var deliveryFee: Double
    var minOrder: Double?
    var estimatedTimeMin: Int?
    var isAvailable: Bool
    var deeplinkUrl: String?
    var lastSyncedAt: Date
    
    init(from price: DeliveryPrice) {
        self.id = price.id
        self.placeId = price.placeId
        self.appId = price.app.rawValue
        self.deliveryFee = price.deliveryFee
        self.minOrder = price.minOrder
        self.estimatedTimeMin = price.estimatedTimeMin
        self.isAvailable = price.isAvailable
        self.deeplinkUrl = price.deeplinkUrl
        self.lastSyncedAt = Date()
    }
}
