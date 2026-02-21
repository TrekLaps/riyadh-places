// Category.swift
// تصنيفات الأماكن — يطابق places.json

import Foundation

enum PlaceCategory: String, CaseIterable, Identifiable, Codable {
    case restaurant = "restaurant"
    case cafe = "cafe"
    case desserts = "desserts"
    case entertainment = "entertainment"
    case shopping = "shopping"
    case nature = "nature"
    case hotels = "hotels"
    case chalets = "chalets"
    case malls = "malls"
    case museums = "museums"
    case events = "events"
    
    var id: String { rawValue }
    
    var nameAr: String {
        switch self {
        case .restaurant: return "مطاعم"
        case .cafe: return "كافيهات"
        case .desserts: return "حلويات"
        case .entertainment: return "ترفيه"
        case .shopping: return "تسوق"
        case .nature: return "طبيعة"
        case .hotels: return "فنادق"
        case .chalets: return "شاليهات"
        case .malls: return "مولات"
        case .museums: return "متاحف"
        case .events: return "فعاليات"
        }
    }
    
    var emoji: String {
        switch self {
        case .restaurant: return "🍽️"
        case .cafe: return "☕"
        case .desserts: return "🍰"
        case .entertainment: return "🎭"
        case .shopping: return "🛍️"
        case .nature: return "🌳"
        case .hotels: return "🏨"
        case .chalets: return "🏖️"
        case .malls: return "🏬"
        case .museums: return "🏛️"
        case .events: return "🎪"
        }
    }
    
    var icon: String {
        switch self {
        case .restaurant: return "fork.knife"
        case .cafe: return "cup.and.saucer.fill"
        case .desserts: return "birthday.cake.fill"
        case .entertainment: return "sparkles"
        case .shopping: return "bag.fill"
        case .nature: return "leaf.fill"
        case .hotels: return "building.2.fill"
        case .chalets: return "house.lodge.fill"
        case .malls: return "building.columns.fill"
        case .museums: return "building.columns"
        case .events: return "ticket.fill"
        }
    }
}
