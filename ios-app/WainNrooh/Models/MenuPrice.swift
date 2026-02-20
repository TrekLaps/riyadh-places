// MenuPrice.swift
// موديل أسعار المنيو — أسعار حقيقية بالريال السعودي

import Foundation
import SwiftData

// MARK: - أسعار المنيو

/// عنصر من المنيو مع أسعاره الحقيقية
struct MenuPrice: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let placeId: String
    let categoryAr: String?
    let categoryEn: String?
    let nameAr: String
    let nameEn: String?
    let descriptionAr: String?
    let sizes: [MenuItemSize]
    let imageUrl: String?
    let isAvailable: Bool?
    let lastUpdated: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case placeId = "place_id"
        case categoryAr = "category_ar"
        case categoryEn = "category_en"
        case nameAr = "name_ar"
        case nameEn = "name_en"
        case descriptionAr = "description_ar"
        case sizes = "prices"
        case imageUrl = "image_url"
        case isAvailable = "is_available"
        case lastUpdated = "last_updated"
    }
    
    /// أقل سعر متاح
    var minPrice: Double {
        sizes.map(\.price).min() ?? 0
    }
    
    /// أعلى سعر متاح
    var maxPrice: Double {
        sizes.map(\.price).max() ?? 0
    }
    
    /// نص السعر المنسق
    var formattedPrice: String {
        if sizes.count == 1 {
            return "\(Int(sizes[0].price)) ر.س"
        } else if minPrice == maxPrice {
            return "\(Int(minPrice)) ر.س"
        } else {
            return "\(Int(minPrice)) - \(Int(maxPrice)) ر.س"
        }
    }
}

// MARK: - حجم العنصر

/// حجم/مقاس العنصر مع سعره
struct MenuItemSize: Codable, Identifiable, Hashable, Sendable {
    var id: String { "\(size ?? "default")_\(price)" }
    let size: String?
    let price: Double
    
    enum CodingKeys: String, CodingKey {
        case size
        case price
    }
    
    /// اسم الحجم المنسق
    var formattedSize: String {
        guard let size = size else { return "" }
        switch size.uppercased() {
        case "S", "SMALL": return "صغير"
        case "M", "MEDIUM": return "وسط"
        case "L", "LARGE": return "كبير"
        case "XL", "EXTRA_LARGE": return "كبير جداً"
        default: return size
        }
    }
    
    /// السعر المنسق
    var formattedPrice: String {
        "\(Int(price)) ر.س"
    }
}

// MARK: - فئة المنيو

/// تجميع عناصر المنيو حسب الفئة
struct MenuCategory: Identifiable, Sendable {
    let id: String
    let nameAr: String
    let nameEn: String?
    let items: [MenuPrice]
    
    /// متوسط أسعار الفئة
    var averagePrice: Double {
        guard !items.isEmpty else { return 0 }
        return items.reduce(0) { $0 + $1.minPrice } / Double(items.count)
    }
    
    /// نص متوسط السعر
    var formattedAveragePrice: String {
        "متوسط \(Int(averagePrice)) ر.س"
    }
}

// MARK: - ملخص المنيو

/// ملخص أسعار المنيو لمكان
struct MenuSummary: Sendable {
    let placeId: String
    let categories: [MenuCategory]
    let totalItems: Int
    let averagePrice: Double
    let priceLevel: String
    let lastUpdated: Date?
    
    /// نص مستوى الأسعار
    var priceLevelText: String {
        switch priceLevel {
        case "$": return "رخيص"
        case "$$": return "متوسط"
        case "$$$": return "غالي"
        case "$$$$": return "فاخر"
        default: return "متوسط"
        }
    }
    
    /// نص متوسط السعر
    var formattedAveragePrice: String {
        "متوسط سعر العنصر: \(Int(averagePrice)) ر.س"
    }
}

// MARK: - كاش أسعار المنيو (SwiftData)

/// نسخة محلية من سعر المنيو
@Model
final class CachedMenuPrice {
    @Attribute(.unique) var id: String
    var placeId: String
    var categoryAr: String?
    var nameAr: String
    var nameEn: String?
    var sizesData: Data?
    var isAvailable: Bool
    var lastSyncedAt: Date
    
    init(from item: MenuPrice) {
        self.id = item.id
        self.placeId = item.placeId
        self.categoryAr = item.categoryAr
        self.nameAr = item.nameAr
        self.nameEn = item.nameEn
        self.sizesData = try? JSONEncoder().encode(item.sizes)
        self.isAvailable = item.isAvailable ?? true
        self.lastSyncedAt = Date()
    }
    
    /// تحويل للموديل الأصلي
    func toMenuPrice() -> MenuPrice {
        let sizes = (try? JSONDecoder().decode([MenuItemSize].self, from: sizesData ?? Data())) ?? []
        return MenuPrice(
            id: id,
            placeId: placeId,
            categoryAr: categoryAr,
            categoryEn: nil,
            nameAr: nameAr,
            nameEn: nameEn,
            descriptionAr: nil,
            sizes: sizes,
            imageUrl: nil,
            isAvailable: isAvailable,
            lastUpdated: nil
        )
    }
}
