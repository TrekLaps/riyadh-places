// FavoritesViewModel.swift
// ViewModel المفضلة — الأماكن المحفوظة

import Foundation
import Combine

// MARK: - ViewModel المفضلة

/// ViewModel المفضلة — يدير الأماكن المحفوظة
@MainActor
final class FavoritesViewModel: ObservableObject {
    
    // MARK: - خصائص منشورة
    
    /// الأماكن المفضلة
    @Published var favorites: [Place] = []
    
    /// حالة التحميل
    @Published var isLoading: Bool = false
    
    /// خطأ
    @Published var errorMessage: String?
    
    /// فلتر التصنيف
    @Published var filterCategory: PlaceCategory?
    
    /// نص البحث في المفضلة
    @Published var searchText: String = ""
    
    // MARK: - خدمات
    
    private let placesService = PlacesService.shared
    
    // MARK: - تحميل البيانات
    
    /// تحميل الأماكن المفضلة
    func loadFavorites() async {
        isLoading = true
        errorMessage = nil
        
        let favoriteIds = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
        
        guard !favoriteIds.isEmpty else {
            favorites = []
            isLoading = false
            return
        }
        
        do {
            // جلب تفاصيل كل مكان مفضل
            var loadedPlaces: [Place] = []
            for id in favoriteIds {
                if let place = try? await placesService.fetchPlace(id: id) {
                    loadedPlaces.append(place)
                }
            }
            favorites = loadedPlaces
        } catch {
            errorMessage = "فشل تحميل المفضلة"
            AppConfig.debugLog("❌ \(error)")
        }
        
        isLoading = false
    }
    
    // MARK: - المفضلة المفلترة
    
    /// الأماكن المفضلة بعد الفلترة
    var filteredFavorites: [Place] {
        var result = favorites
        
        // فلتر التصنيف
        if let category = filterCategory {
            result = result.filter { $0.category == category }
        }
        
        // فلتر البحث
        if !searchText.isEmpty {
            result = result.filter { place in
                place.name.arabicSearchMatch(searchText) ||
                (place.nameEn?.lowercased().contains(searchText.lowercased()) == true) ||
                (place.neighborhood?.arabicSearchMatch(searchText) == true)
            }
        }
        
        return result
    }
    
    /// التصنيفات الموجودة في المفضلة
    var availableCategories: [PlaceCategory] {
        let categories = Set(favorites.map(\.category))
        return Array(categories).sorted { $0.nameAr < $1.nameAr }
    }
    
    /// عدد المفضلة
    var favoritesCount: Int {
        favorites.count
    }
    
    /// هل المفضلة فارغة؟
    var isEmpty: Bool {
        favorites.isEmpty
    }
    
    // MARK: - إدارة المفضلة
    
    /// إزالة مكان من المفضلة
    func removeFavorite(_ place: Place) {
        // إزالة من القائمة المحلية
        favorites.removeAll { $0.id == place.id }
        
        // تحديث UserDefaults
        var savedIds = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
        savedIds.removeAll { $0 == place.id }
        UserDefaults.standard.set(savedIds, forKey: "favorites")
        
        // TODO: مزامنة مع السيرفر
    }
    
    /// هل المكان مفضل؟
    func isFavorite(_ placeId: String) -> Bool {
        let savedIds = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
        return savedIds.contains(placeId)
    }
    
    /// تبديل حالة المفضلة
    func toggleFavorite(_ place: Place) {
        if isFavorite(place.id) {
            removeFavorite(place)
        } else {
            addFavorite(place)
        }
    }
    
    /// إضافة مكان للمفضلة
    func addFavorite(_ place: Place) {
        guard !isFavorite(place.id) else { return }
        
        favorites.insert(place, at: 0)
        
        var savedIds = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
        savedIds.insert(place.id, at: 0)
        UserDefaults.standard.set(savedIds, forKey: "favorites")
    }
    
    /// مسح كل المفضلة
    func clearAll() {
        favorites.removeAll()
        UserDefaults.standard.removeObject(forKey: "favorites")
    }
}
