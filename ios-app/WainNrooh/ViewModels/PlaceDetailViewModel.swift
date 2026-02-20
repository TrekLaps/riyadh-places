// PlaceDetailViewModel.swift
// ViewModel تفاصيل المكان — أسعار + توصيل + منيو

import Foundation
import Combine

// MARK: - ViewModel تفاصيل المكان

/// ViewModel صفحة المكان — يدير التفاصيل والأسعار والتوصيل
@MainActor
final class PlaceDetailViewModel: ObservableObject {
    
    // MARK: - خصائص منشورة
    
    /// بيانات المكان
    @Published var place: Place
    
    /// أسعار التوصيل (مقارنة)
    @Published var deliveryComparison: DeliveryComparison?
    
    /// أسعار المنيو
    @Published var menuPrices: [MenuPrice] = []
    
    /// فئات المنيو
    @Published var menuCategories: [MenuCategory] = []
    
    /// أماكن مشابهة
    @Published var similarPlaces: [Place] = []
    
    /// هل المكان مفضل؟
    @Published var isFavorite: Bool = false
    
    /// حالات التحميل
    @Published var isLoadingDelivery: Bool = false
    @Published var isLoadingMenu: Bool = false
    @Published var isLoadingSimilar: Bool = false
    
    /// أخطاء
    @Published var deliveryError: String?
    @Published var menuError: String?
    
    // MARK: - خدمات
    
    private let placesService = PlacesService.shared
    private let deliveryService = DeliveryService.shared
    private let supabase = SupabaseService.shared
    
    // MARK: - تهيئة
    
    init(place: Place) {
        self.place = place
        checkFavoriteStatus()
    }
    
    // MARK: - تحميل البيانات
    
    /// تحميل كل بيانات المكان
    func loadAllData() async {
        async let deliveryTask = loadDeliveryPrices()
        async let menuTask = loadMenuPrices()
        async let similarTask = loadSimilarPlaces()
        
        await deliveryTask
        await menuTask
        await similarTask
    }
    
    /// تحميل أسعار التوصيل
    func loadDeliveryPrices() async {
        isLoadingDelivery = true
        deliveryError = nil
        
        do {
            deliveryComparison = try await deliveryService.compareDeliveryPrices(
                placeId: place.id
            )
        } catch {
            AppConfig.debugLog("❌ فشل تحميل أسعار التوصيل: \(error)")
            deliveryError = "فشل تحميل أسعار التوصيل"
        }
        
        isLoadingDelivery = false
    }
    
    /// تحميل أسعار المنيو
    func loadMenuPrices() async {
        isLoadingMenu = true
        menuError = nil
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let data = try await supabase.from(
                "menu_items",
                select: "*",
                filters: [
                    SupabaseFilter(column: "place_id", op: .eq, value: place.id),
                    SupabaseFilter(column: "is_available", op: .eq, value: "true")
                ],
                order: "category_ar"
            )
            
            menuPrices = try decoder.decode([MenuPrice].self, from: data)
            
            // تجميع حسب الفئة
            let grouped = Dictionary(grouping: menuPrices) { $0.categoryAr ?? "أخرى" }
            menuCategories = grouped.map { key, items in
                MenuCategory(
                    id: key,
                    nameAr: key,
                    nameEn: nil,
                    items: items
                )
            }.sorted { $0.nameAr < $1.nameAr }
            
        } catch {
            AppConfig.debugLog("❌ فشل تحميل أسعار المنيو: \(error)")
            menuError = "فشل تحميل الأسعار"
        }
        
        isLoadingMenu = false
    }
    
    /// تحميل أماكن مشابهة
    func loadSimilarPlaces() async {
        isLoadingSimilar = true
        
        do {
            similarPlaces = try await placesService.fetchSimilar(to: place, limit: 5)
        } catch {
            AppConfig.debugLog("❌ فشل تحميل الأماكن المشابهة: \(error)")
        }
        
        isLoadingSimilar = false
    }
    
    // MARK: - المفضلة
    
    /// تبديل حالة المفضلة
    func toggleFavorite() {
        isFavorite.toggle()
        
        // حفظ محلياً
        var favorites = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
        
        if isFavorite {
            if !favorites.contains(place.id) {
                favorites.append(place.id)
            }
        } else {
            favorites.removeAll { $0 == place.id }
        }
        
        UserDefaults.standard.set(favorites, forKey: "favorites")
        
        // TODO: مزامنة مع السيرفر
    }
    
    /// التحقق من حالة المفضلة
    private func checkFavoriteStatus() {
        let favorites = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
        isFavorite = favorites.contains(place.id)
    }
    
    // MARK: - الإجراءات
    
    /// فتح Google Maps للتنقل
    func openInGoogleMaps() {
        guard let coordinate = place.coordinate else { return }
        let urlString = place.googleMapsUrl ??
            "https://www.google.com/maps/dir/?api=1&destination=\(coordinate.latitude),\(coordinate.longitude)"
        
        if let url = URL(string: urlString) {
            Task { @MainActor in
                await UIApplication.shared.open(url)
            }
        }
    }
    
    /// الاتصال بالمكان
    func callPlace() {
        guard let phone = place.phone,
              let url = URL(string: "tel:\(phone.englishDigits)") else { return }
        Task { @MainActor in
            await UIApplication.shared.open(url)
        }
    }
    
    /// مشاركة المكان
    func sharePlace() -> String {
        var text = "🏠 \(place.name)"
        if let rating = place.rating {
            text += " ⭐ \(rating.formattedRating)"
        }
        text += "\n📍 \(place.neighborhood ?? "الرياض")"
        if let address = place.address {
            text += "\n🗺 \(address)"
        }
        text += "\n\nاكتشفه على وين نروح!"
        return text
    }
    
    /// فتح تطبيق توصيل
    func openDeliveryApp(_ app: DeliveryApp, deeplink: String?) {
        deliveryService.openDeliveryApp(app, deeplink: deeplink)
    }
}

import UIKit
