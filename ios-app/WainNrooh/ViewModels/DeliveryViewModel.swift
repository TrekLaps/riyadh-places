// DeliveryViewModel.swift
// ViewModel مقارنة التوصيل — مقارنة أسعار 8+ تطبيقات

import Foundation
import Combine

// MARK: - ViewModel التوصيل

/// ViewModel مقارنة أسعار التوصيل
@MainActor
final class DeliveryViewModel: ObservableObject {
    
    // MARK: - خصائص منشورة
    
    /// التطبيقات المتاحة
    @Published var availableApps: [DeliveryApp] = DeliveryApp.allCases
    
    /// التطبيق المختار للفلترة
    @Published var selectedApp: DeliveryApp?
    
    /// أسعار التوصيل لمكان معين
    @Published var currentComparison: DeliveryComparison?
    
    /// حالة التحميل
    @Published var isLoading: Bool = false
    
    /// خطأ
    @Published var errorMessage: String?
    
    /// الترتيب
    @Published var sortOption: DeliverySortOption = .price
    
    // MARK: - خدمات
    
    private let deliveryService = DeliveryService.shared
    
    // MARK: - تحميل المقارنة
    
    /// مقارنة أسعار التوصيل لمكان
    func compareFor(placeId: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            currentComparison = try await deliveryService.compareDeliveryPrices(placeId: placeId)
        } catch {
            errorMessage = "فشل تحميل أسعار التوصيل"
            AppConfig.debugLog("❌ \(error)")
        }
        
        isLoading = false
    }
    
    // MARK: - الأسعار المرتبة
    
    /// الأسعار مرتبة حسب الخيار المختار
    var sortedPrices: [DeliveryPrice] {
        guard let comparison = currentComparison else { return [] }
        
        let available = comparison.prices.filter { $0.isAvailable }
        
        switch sortOption {
        case .price:
            return available.sorted { $0.deliveryFee < $1.deliveryFee }
        case .time:
            return available.sorted { ($0.estimatedTimeMin ?? 999) < ($1.estimatedTimeMin ?? 999) }
        case .minOrder:
            return available.sorted { ($0.minOrder ?? 0) < ($1.minOrder ?? 0) }
        }
    }
    
    /// الخيار الأرخص
    var cheapestOption: DeliveryPrice? {
        currentComparison?.cheapest
    }
    
    /// الخيار الأسرع
    var fastestOption: DeliveryPrice? {
        currentComparison?.fastest
    }
    
    /// كم ممكن توفر
    var savingsText: String? {
        currentComparison?.savingsText
    }
    
    /// فتح تطبيق التوصيل
    func openApp(_ app: DeliveryApp, deeplink: String?) {
        deliveryService.openDeliveryApp(app, deeplink: deeplink)
    }
}

// MARK: - خيارات ترتيب التوصيل

/// خيارات ترتيب أسعار التوصيل
enum DeliverySortOption: String, CaseIterable, Identifiable {
    case price = "price"
    case time = "time"
    case minOrder = "min_order"
    
    var id: String { rawValue }
    
    var nameAr: String {
        switch self {
        case .price: return "الأرخص"
        case .time: return "الأسرع"
        case .minOrder: return "أقل حد طلب"
        }
    }
    
    var icon: String {
        switch self {
        case .price: return "tag.fill"
        case .time: return "clock.fill"
        case .minOrder: return "cart.fill"
        }
    }
}
