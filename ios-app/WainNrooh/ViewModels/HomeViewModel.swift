// HomeViewModel.swift
// HS Pattern: Pre-compute + cache everything

import SwiftUI

struct CategoryInfo: Identifiable {
    let id: String
    let nameAr: String
    let nameEn: String
    let emoji: String
    let count: Int
}

@MainActor
class HomeViewModel: ObservableObject {
    @Published var trendingPlaces: [Place] = []
    @Published var newPlaces: [Place] = []
    @Published var topInNeighborhood: [Place]?
    @Published var currentNeighborhood: String = "حي العليا"
    @Published var categories: [CategoryInfo] = []
    @Published var isDataLoaded = false
    
    var greeting: String {
        let hour = Calendar.current.component(.hour, from: Date())
        if hour < 12 { return "صباح الخير ☀️" }
        if hour < 17 { return "مساء الخير 🌤️" }
        return "مساء النور 🌙"
    }
    
    func loadData(places: [Place]) async {
        guard !places.isEmpty else { return }
        
        // Trending: top rated with trending flag
        trendingPlaces = places
            .filter { $0.trending == true && $0.googleRating != nil }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(20).map { $0 }
        
        // New places
        newPlaces = places
            .filter { $0.isNew == true }
            .prefix(15).map { $0 }
        
        // Top 10 in default neighborhood
        topInNeighborhood = places
            .filter { $0.neighborhood == currentNeighborhood && $0.googleRating != nil }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(10).map { $0 }
        
        // Categories with counts
        var catCounts: [String: (ar: String, en: String, emoji: String, count: Int)] = [:]
        let emojiMap: [String: String] = [
            "restaurant": "🍽️", "cafe": "☕", "entertainment": "🎭",
            "shopping": "🛍️", "desserts": "🍰", "nature": "🌳",
            "hotels": "🏨", "chalets": "🏖️", "malls": "🏬",
            "museums": "🏛️", "events": "🎪", "perfume": "🧴",
            "mosques": "🕌", "sports": "⚽", "education": "📚",
            "health": "🏥", "services": "🔧", "offices": "🏢",
            "tourism": "✈️", "finance": "🏦"
        ]
        
        for p in places {
            let cat = p.categoryEn ?? p.category
            let catAr = p.categoryAr ?? p.category
            if catCounts[cat] == nil {
                catCounts[cat] = (catAr, cat, emojiMap[cat] ?? "📍", 0)
            }
            catCounts[cat]!.count += 1
        }
        
        categories = catCounts
            .sorted { $0.value.count > $1.value.count }
            .map { CategoryInfo(id: $0.key, nameAr: $0.value.ar, nameEn: $0.value.en, emoji: $0.value.emoji, count: $0.value.count) }
        
        isDataLoaded = true
    }
}
