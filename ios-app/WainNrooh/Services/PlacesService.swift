// PlacesService.swift
// خدمة الأماكن — Offline-first (bundled JSON) + future API sync

import Foundation
import CoreLocation

@MainActor
class PlacesService: ObservableObject {
    static let shared = PlacesService()
    
    @Published var allPlaces: [Place] = []
    @Published var isLoaded = false
    
    private init() {}
    
    // MARK: - Load Bundled Data (Offline-First)
    
    func loadBundledPlaces() async {
        guard !isLoaded else { return }
        
        if let url = Bundle.main.url(forResource: AppConfig.bundledDataFile, withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                let decoder = JSONDecoder()
                allPlaces = try decoder.decode([Place].self, from: data)
                isLoaded = true
                print("✅ Loaded \(allPlaces.count) places from bundle")
            } catch {
                print("❌ Failed to load places: \(error)")
            }
        }
    }
    
    // MARK: - Search (Local)
    
    func search(query: String, category: String? = nil, neighborhood: String? = nil,
                occasion: Occasion? = nil, maxResults: Int = 50) -> [Place] {
        var results = allPlaces
        
        // Text search
        if !query.isEmpty {
            let q = query.lowercased()
            results = results.filter {
                $0.nameAr.contains(query) ||
                ($0.nameEn?.lowercased().contains(q) ?? false) ||
                ($0.descriptionAr?.contains(query) ?? false) ||
                ($0.neighborhood?.contains(query) ?? false) ||
                ($0.tags?.contains(where: { $0.contains(query) }) ?? false)
            }
        }
        
        // Category filter
        if let cat = category {
            results = results.filter { ($0.categoryEn ?? $0.category) == cat }
        }
        
        // Neighborhood filter
        if let hood = neighborhood {
            results = results.filter { $0.neighborhood == hood }
        }
        
        // Occasion filter
        if let occ = occasion {
            results = results.filter { $0.occasions.contains(occ) }
        }
        
        // Sort by rating
        return Array(results
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(maxResults))
    }
    
    // MARK: - Nearby (Location-based)
    
    func nearby(location: CLLocation, radius: Double = 5.0, limit: Int = 20) -> [Place] {
        allPlaces
            .compactMap { place -> (Place, Double)? in
                guard let dist = place.distance(from: location) else { return nil }
                return dist <= radius ? (place, dist) : nil
            }
            .sorted { $0.1 < $1.1 }
            .prefix(limit)
            .map(\.0)
    }
    
    // MARK: - Top Rated
    
    func topRated(category: String? = nil, neighborhood: String? = nil, limit: Int = 10) -> [Place] {
        var results = allPlaces.filter { $0.hasVerifiedRating }
        if let cat = category {
            results = results.filter { ($0.categoryEn ?? $0.category) == cat }
        }
        if let hood = neighborhood {
            results = results.filter { $0.neighborhood == hood }
        }
        return Array(results
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(limit))
    }
    
    // MARK: - Trending
    
    func trending(limit: Int = 20) -> [Place] {
        Array(allPlaces
            .filter { $0.trending == true }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(limit))
    }
    
    // MARK: - New Places
    
    func newPlaces(limit: Int = 15) -> [Place] {
        Array(allPlaces
            .filter { $0.isNew == true }
            .prefix(limit))
    }
    
    // MARK: - By Occasion
    
    func forOccasion(_ occasion: Occasion, limit: Int = 30) -> [Place] {
        Array(allPlaces
            .filter { $0.occasions.contains(occasion) }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(limit))
    }
    
    // MARK: - Stats
    
    var categories: [(name: String, nameAr: String, count: Int)] {
        var counts: [String: (ar: String, count: Int)] = [:]
        for p in allPlaces {
            let cat = p.categoryEn ?? p.category
            let catAr = p.categoryAr ?? p.category
            counts[cat, default: (catAr, 0)].count += 1
        }
        return counts
            .map { (name: $0.key, nameAr: $0.value.ar, count: $0.value.count) }
            .sorted { $0.count > $1.count }
    }
    
    var neighborhoods: [String] {
        Array(Set(allPlaces.compactMap(\.neighborhood))).sorted()
    }
}
