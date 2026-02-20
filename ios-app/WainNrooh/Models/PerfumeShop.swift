// PerfumeShop.swift
// موديل محلات العطور — مقارنة أسعار العطور عبر المحلات

import Foundation

// MARK: - محل عطور

/// محل عطور بالرياض
struct PerfumeShop: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let nameAr: String
    let nameEn: String
    let category: String
    let website: String?
    let priceRange: String?
    let branches: [PerfumeBranch]?
    let rating: Double?
    let logoUrl: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case nameAr = "name_ar"
        case nameEn = "name_en"
        case category
        case website
        case priceRange = "price_range"
        case branches
        case rating
        case logoUrl = "logo_url"
    }
    
    /// عدد الفروع
    var branchCount: Int {
        branches?.count ?? 0
    }
    
    /// نص عدد الفروع
    var formattedBranchCount: String {
        "\(branchCount) فرع"
    }
}

// MARK: - فرع محل عطور

/// فرع من فروع محل العطور
struct PerfumeBranch: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let neighborhood: String?
    let address: String?
    let latitude: Double?
    let longitude: Double?
    let phone: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case neighborhood
        case address
        case latitude
        case longitude
        case phone
    }
}

// MARK: - عطر

/// عطر مع أسعاره في محلات مختلفة
struct Perfume: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let name: String
    let brand: String
    let notes: [String]?
    let sizeMl: Int?
    let prices: [PerfumePrice]?
    let alternatives: [PerfumeAlternative]?
    let fragranticaRating: Double?
    let imageUrl: String?
    let category: PerfumeCategory?
    
    enum CodingKeys: String, CodingKey {
        case id, name, brand, notes
        case sizeMl = "size_ml"
        case prices, alternatives
        case fragranticaRating = "fragrantica_rating"
        case imageUrl = "image_url"
        case category
    }
    
    /// أقل سعر متاح
    var minPrice: Double? {
        prices?.map(\.price).min()
    }
    
    /// أعلى سعر
    var maxPrice: Double? {
        prices?.map(\.price).max()
    }
    
    /// نص السعر المنسق
    var formattedPrice: String {
        guard let min = minPrice else { return "غير متوفر" }
        if let max = maxPrice, min != max {
            return "\(Int(min)) - \(Int(max)) ر.س"
        }
        return "\(Int(min)) ر.س"
    }
    
    /// نص المكونات
    var formattedNotes: String {
        notes?.joined(separator: "، ") ?? ""
    }
    
    /// الحجم المنسق
    var formattedSize: String {
        guard let ml = sizeMl else { return "" }
        return "\(ml) مل"
    }
}

// MARK: - سعر العطر في محل

/// سعر عطر في محل معين
struct PerfumePrice: Codable, Identifiable, Hashable, Sendable {
    var id: String { "\(shopId)_\(price)" }
    let shopId: String
    let shopName: String
    let price: Double
    let isAvailable: Bool?
    let url: String?
    
    enum CodingKeys: String, CodingKey {
        case shopId = "shop_id"
        case shopName = "shop"
        case price
        case isAvailable = "is_available"
        case url
    }
    
    /// السعر المنسق
    var formattedPrice: String {
        "\(Int(price)) ر.س"
    }
}

// MARK: - بديل أرخص

/// عطر بديل أرخص (dupe)
struct PerfumeAlternative: Codable, Identifiable, Hashable, Sendable {
    var id: String { name }
    let name: String
    let brand: String?
    let price: Double
    let similarity: String?
    
    /// السعر المنسق
    var formattedPrice: String {
        "\(Int(price)) ر.س"
    }
    
    /// نسبة التشابه المنسقة
    var formattedSimilarity: String {
        similarity ?? "مشابه"
    }
}

// MARK: - فئة العطر

/// تصنيفات العطور
enum PerfumeCategory: String, Codable, CaseIterable, Sendable {
    case oud = "oud"
    case musk = "musk"
    case oriental = "oriental"
    case floral = "floral"
    case woody = "woody"
    case fresh = "fresh"
    case citrus = "citrus"
    case amber = "amber"
    
    /// الاسم بالعربي
    var nameAr: String {
        switch self {
        case .oud: return "عود"
        case .musk: return "مسك"
        case .oriental: return "شرقي"
        case .floral: return "زهري"
        case .woody: return "خشبي"
        case .fresh: return "منعش"
        case .citrus: return "حمضي"
        case .amber: return "عنبري"
        }
    }
}

// MARK: - المحلات الرئيسية

extension PerfumeShop {
    
    /// محلات العطور الرئيسية (بيانات ثابتة للبداية)
    static let mainShops: [PerfumeShop] = [
        PerfumeShop(id: "arabian_oud", nameAr: "العربية للعود", nameEn: "Arabian Oud",
                    category: "عطور", website: "https://arabianoud.com",
                    priceRange: "50-2000", branches: nil, rating: 4.3, logoUrl: nil),
        PerfumeShop(id: "abdul_samad", nameAr: "عبد الصمد القرشي", nameEn: "Abdul Samad Al Qurashi",
                    category: "عطور", website: "https://asgharali.com",
                    priceRange: "100-5000", branches: nil, rating: 4.5, logoUrl: nil),
        PerfumeShop(id: "almajed_oud", nameAr: "الماجد للعود", nameEn: "AlMajed Oud",
                    category: "عطور", website: "https://almajedoud.com",
                    priceRange: "30-1500", branches: nil, rating: 4.2, logoUrl: nil),
        PerfumeShop(id: "rasasi", nameAr: "رصاصي", nameEn: "Rasasi",
                    category: "عطور", website: "https://rasasi.com",
                    priceRange: "50-800", branches: nil, rating: 4.1, logoUrl: nil),
        PerfumeShop(id: "swiss_arabian", nameAr: "سويس أرابيان", nameEn: "Swiss Arabian",
                    category: "عطور", website: "https://swissarabian.com",
                    priceRange: "60-1200", branches: nil, rating: 4.0, logoUrl: nil),
        PerfumeShop(id: "paris_gallery", nameAr: "باريس غاليري", nameEn: "Paris Gallery",
                    category: "عطور", website: "https://parisgallery.com",
                    priceRange: "200-5000", branches: nil, rating: 4.4, logoUrl: nil),
        PerfumeShop(id: "faces", nameAr: "فيسز", nameEn: "Faces",
                    category: "عطور", website: "https://faces.com",
                    priceRange: "150-4000", branches: nil, rating: 4.3, logoUrl: nil),
        PerfumeShop(id: "lattafa", nameAr: "لطافة", nameEn: "Lattafa",
                    category: "عطور", website: nil,
                    priceRange: "30-300", branches: nil, rating: 4.0, logoUrl: nil),
    ]
}
