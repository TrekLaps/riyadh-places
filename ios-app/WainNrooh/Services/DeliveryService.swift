// DeliveryService.swift
// خدمة التوصيل — مقارنة أسعار 8+ تطبيقات توصيل

import Foundation

// MARK: - خدمة التوصيل

/// خدمة مقارنة أسعار التوصيل — الميزة القاتلة!
final class DeliveryService: @unchecked Sendable {
    
    // MARK: - Singleton
    
    static let shared = DeliveryService()
    
    private let supabase = SupabaseService.shared
    private let decoder = JSONDecoder()
    
    private init() {
        decoder.keyDecodingStrategy = .convertFromSnakeCase
    }
    
    // MARK: - مقارنة الأسعار
    
    /// مقارنة أسعار التوصيل لمكان معين من كل التطبيقات
    func compareDeliveryPrices(
        placeId: String,
        userLatitude: Double? = nil,
        userLongitude: Double? = nil
    ) async throws -> DeliveryComparison {
        let data = try await supabase.from(
            "delivery_prices",
            select: "*",
            filters: [
                SupabaseFilter(column: "place_id", op: .eq, value: placeId)
            ],
            order: "delivery_fee",
            ascending: true
        )
        
        let prices = try decoder.decode([DeliveryPrice].self, from: data)
        
        // جلب اسم المكان
        let placeData = try await supabase.from(
            "places",
            select: "name_ar",
            filters: [SupabaseFilter(column: "id", op: .eq, value: placeId)],
            limit: 1
        )
        
        struct PlaceName: Decodable { let nameAr: String }
        let placeName = (try? decoder.decode([PlaceName].self, from: placeData))?.first?.nameAr ?? ""
        
        return DeliveryComparison(
            placeId: placeId,
            placeName: placeName,
            prices: prices,
            lastUpdated: Date()
        )
    }
    
    /// جلب أسعار التوصيل لتطبيق معين
    func fetchPrices(
        for app: DeliveryApp,
        limit: Int = 50
    ) async throws -> [DeliveryPrice] {
        let data = try await supabase.from(
            "delivery_prices",
            select: "*",
            filters: [
                SupabaseFilter(column: "app_id", op: .eq, value: app.rawValue),
                SupabaseFilter(column: "is_available", op: .eq, value: "true")
            ],
            order: "delivery_fee",
            ascending: true,
            limit: limit
        )
        
        return try decoder.decode([DeliveryPrice].self, from: data)
    }
    
    /// جلب أرخص خيارات التوصيل لعدة أماكن
    func fetchCheapestOptions(
        placeIds: [String]
    ) async throws -> [String: DeliveryPrice] {
        var results: [String: DeliveryPrice] = [:]
        
        for placeId in placeIds {
            let data = try await supabase.from(
                "delivery_prices",
                select: "*",
                filters: [
                    SupabaseFilter(column: "place_id", op: .eq, value: placeId),
                    SupabaseFilter(column: "is_available", op: .eq, value: "true")
                ],
                order: "delivery_fee",
                ascending: true,
                limit: 1
            )
            
            let prices = try decoder.decode([DeliveryPrice].self, from: data)
            if let cheapest = prices.first {
                results[placeId] = cheapest
            }
        }
        
        return results
    }
    
    /// جلب كل تطبيقات التوصيل المتاحة
    func fetchAvailableApps() async throws -> [DeliveryAppInfo] {
        let data = try await supabase.from(
            "delivery_apps",
            select: "*",
            filters: [
                SupabaseFilter(column: "is_active", op: .eq, value: "true")
            ]
        )
        
        return try decoder.decode([DeliveryAppInfo].self, from: data)
    }
    
    // MARK: - روابط التطبيقات
    
    /// فتح تطبيق التوصيل للطلب
    func openDeliveryApp(_ app: DeliveryApp, deeplink: String?) {
        guard let deeplink = deeplink,
              let url = URL(string: deeplink) else {
            // إذا ما فيه رابط مباشر — افتح التطبيق
            if let appUrl = URL(string: app.deeplinkScheme) {
                openURL(appUrl, fallback: app.appStoreUrl)
            }
            return
        }
        
        openURL(url, fallback: app.appStoreUrl)
    }
    
    /// فتح رابط مع fallback
    private func openURL(_ url: URL, fallback: String) {
        Task { @MainActor in
            if await UIApplication.shared.canOpenURL(url) {
                await UIApplication.shared.open(url)
            } else if let fallbackUrl = URL(string: fallback) {
                await UIApplication.shared.open(fallbackUrl)
            }
        }
    }
}

// MARK: - معلومات تطبيق التوصيل

/// معلومات تطبيق التوصيل من الـ API
struct DeliveryAppInfo: Codable, Identifiable {
    let id: String
    let nameAr: String
    let nameEn: String
    let logoUrl: String?
    let deeplinkScheme: String?
    let isActive: Bool
    
    enum CodingKeys: String, CodingKey {
        case id
        case nameAr = "name_ar"
        case nameEn = "name_en"
        case logoUrl = "logo_url"
        case deeplinkScheme = "deeplink_scheme"
        case isActive = "is_active"
    }
}

// MARK: - UIApplication import
import UIKit
