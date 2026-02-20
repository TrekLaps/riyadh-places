// Category.swift
// تصنيفات الأماكن — كل الفئات المتاحة في التطبيق

import Foundation
import SwiftUI

// MARK: - تصنيفات الأماكن

/// التصنيفات الرئيسية للأماكن في الرياض
enum PlaceCategory: String, Codable, CaseIterable, Identifiable, Sendable {
    // مطاعم وأكل
    case restaurant = "restaurant"
    case cafe = "cafe"
    case bakery = "bakery"
    case dessert = "dessert"
    case fastFood = "fast_food"
    case fineDining = "fine_dining"
    case streetFood = "street_food"
    case buffet = "buffet"
    
    // ترفيه
    case entertainment = "entertainment"
    case cinema = "cinema"
    case gaming = "gaming"
    case sports = "sports"
    case park = "park"
    case pool = "pool"
    
    // تسوق
    case shopping = "shopping"
    case mall = "mall"
    case market = "market"
    case perfume = "perfume"
    
    // خدمات
    case spa = "spa"
    case salon = "salon"
    case gym = "gym"
    case hotel = "hotel"
    
    // ثقافة
    case museum = "museum"
    case library = "library"
    case gallery = "gallery"
    
    // عام
    case other = "other"
    
    var id: String { rawValue }
    
    // MARK: - الاسم بالعربي
    
    /// اسم التصنيف بالعربي
    var nameAr: String {
        switch self {
        case .restaurant: return "مطاعم"
        case .cafe: return "مقاهي"
        case .bakery: return "مخابز"
        case .dessert: return "حلويات"
        case .fastFood: return "وجبات سريعة"
        case .fineDining: return "مطاعم فاخرة"
        case .streetFood: return "أكل شعبي"
        case .buffet: return "بوفيهات"
        case .entertainment: return "ترفيه"
        case .cinema: return "سينما"
        case .gaming: return "ألعاب"
        case .sports: return "رياضة"
        case .park: return "حدائق"
        case .pool: return "مسابح"
        case .shopping: return "تسوق"
        case .mall: return "مولات"
        case .market: return "أسواق"
        case .perfume: return "عطور"
        case .spa: return "سبا"
        case .salon: return "صالونات"
        case .gym: return "جيم"
        case .hotel: return "فنادق"
        case .museum: return "متاحف"
        case .library: return "مكتبات"
        case .gallery: return "معارض"
        case .other: return "أخرى"
        }
    }
    
    // MARK: - الاسم بالإنجليزي
    
    /// اسم التصنيف بالإنجليزي
    var nameEn: String {
        switch self {
        case .restaurant: return "Restaurants"
        case .cafe: return "Cafes"
        case .bakery: return "Bakeries"
        case .dessert: return "Desserts"
        case .fastFood: return "Fast Food"
        case .fineDining: return "Fine Dining"
        case .streetFood: return "Street Food"
        case .buffet: return "Buffets"
        case .entertainment: return "Entertainment"
        case .cinema: return "Cinema"
        case .gaming: return "Gaming"
        case .sports: return "Sports"
        case .park: return "Parks"
        case .pool: return "Pools"
        case .shopping: return "Shopping"
        case .mall: return "Malls"
        case .market: return "Markets"
        case .perfume: return "Perfumes"
        case .spa: return "Spa"
        case .salon: return "Salons"
        case .gym: return "Gym"
        case .hotel: return "Hotels"
        case .museum: return "Museums"
        case .library: return "Libraries"
        case .gallery: return "Galleries"
        case .other: return "Other"
        }
    }
    
    // MARK: - الأيقونة
    
    /// أيقونة SF Symbol للتصنيف
    var icon: String {
        switch self {
        case .restaurant: return "fork.knife"
        case .cafe: return "cup.and.saucer.fill"
        case .bakery: return "birthday.cake.fill"
        case .dessert: return "ice.cream.fill" // fallback
        case .fastFood: return "takeoutbag.and.cup.and.straw.fill"
        case .fineDining: return "wineglass.fill"
        case .streetFood: return "flame.fill"
        case .buffet: return "tray.fill"
        case .entertainment: return "sparkles"
        case .cinema: return "film.fill"
        case .gaming: return "gamecontroller.fill"
        case .sports: return "sportscourt.fill"
        case .park: return "leaf.fill"
        case .pool: return "figure.pool.swim"
        case .shopping: return "bag.fill"
        case .mall: return "building.2.fill"
        case .market: return "cart.fill"
        case .perfume: return "drop.fill"
        case .spa: return "sparkle"
        case .salon: return "scissors"
        case .gym: return "dumbbell.fill"
        case .hotel: return "bed.double.fill"
        case .museum: return "building.columns.fill"
        case .library: return "books.vertical.fill"
        case .gallery: return "photo.artframe"
        case .other: return "mappin.and.ellipse"
        }
    }
    
    // MARK: - الإيموجي
    
    /// إيموجي التصنيف
    var emoji: String {
        switch self {
        case .restaurant: return "🍽️"
        case .cafe: return "☕"
        case .bakery: return "🥐"
        case .dessert: return "🍰"
        case .fastFood: return "🍔"
        case .fineDining: return "🥂"
        case .streetFood: return "🔥"
        case .buffet: return "🍱"
        case .entertainment: return "🎭"
        case .cinema: return "🎬"
        case .gaming: return "🎮"
        case .sports: return "⚽"
        case .park: return "🌳"
        case .pool: return "🏊"
        case .shopping: return "🛍️"
        case .mall: return "🏬"
        case .market: return "🏪"
        case .perfume: return "🧴"
        case .spa: return "💆"
        case .salon: return "💇"
        case .gym: return "💪"
        case .hotel: return "🏨"
        case .museum: return "🏛️"
        case .library: return "📚"
        case .gallery: return "🖼️"
        case .other: return "📍"
        }
    }
    
    // MARK: - اللون
    
    /// لون التصنيف
    var color: Color {
        switch self {
        case .restaurant, .fineDining: return .orange
        case .cafe: return Color(hex: "8B4513")
        case .bakery, .dessert: return .pink
        case .fastFood, .streetFood, .buffet: return .red
        case .entertainment, .cinema, .gaming: return .purple
        case .sports, .gym: return .green
        case .park, .pool: return .teal
        case .shopping, .mall, .market: return .blue
        case .perfume: return Color(hex: "C9A84C") // ذهبي
        case .spa, .salon: return .mint
        case .hotel: return .indigo
        case .museum, .library, .gallery: return .brown
        case .other: return .gray
        }
    }
    
    // MARK: - التصنيفات الرئيسية (للعرض في الرئيسية)
    
    /// التصنيفات الأكثر شعبية — تظهر في الشاشة الرئيسية
    static var popular: [PlaceCategory] {
        [.restaurant, .cafe, .dessert, .entertainment, .shopping, .perfume, .park, .spa]
    }
    
    /// تصنيفات الأكل
    static var food: [PlaceCategory] {
        [.restaurant, .cafe, .bakery, .dessert, .fastFood, .fineDining, .streetFood, .buffet]
    }
}
