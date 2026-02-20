// HomeViewModel.swift
// ViewModel الشاشة الرئيسية — ترند + قريب + تصنيفات

import Foundation
import Combine
import CoreLocation

// MARK: - ViewModel الرئيسية

/// ViewModel الشاشة الرئيسية — يدير بيانات الترند والأماكن القريبة والتصنيفات
@MainActor
final class HomeViewModel: ObservableObject {
    
    // MARK: - خصائص منشورة
    
    /// الأماكن الأكثر شعبية (ترند)
    @Published var trendingPlaces: [Place] = []
    
    /// الأماكن القريبة
    @Published var nearbyPlaces: [Place] = []
    
    /// الأماكن الجديدة
    @Published var newPlaces: [Place] = []
    
    /// التصنيفات
    @Published var categories: [PlaceCategory] = PlaceCategory.popular
    
    /// حالة التحميل
    @Published var isLoading: Bool = false
    
    /// حالة تحميل الأماكن القريبة
    @Published var isLoadingNearby: Bool = false
    
    /// رسالة الخطأ
    @Published var errorMessage: String?
    
    /// هل البيانات محملة؟
    @Published var isDataLoaded: Bool = false
    
    // MARK: - خدمات
    
    private let placesService = PlacesService.shared
    private let locationService: LocationService
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - تهيئة
    
    init(locationService: LocationService = LocationService()) {
        self.locationService = locationService
        
        // الاستماع لتحديثات الموقع
        locationService.$currentLocation
            .compactMap { $0 }
            .removeDuplicates { old, new in
                old.distance(from: new) < 500 // تجاهل التغييرات الصغيرة
            }
            .sink { [weak self] location in
                Task {
                    await self?.loadNearbyPlaces(location: location)
                }
            }
            .store(in: &cancellables)
    }
    
    // MARK: - تحميل البيانات
    
    /// تحميل كل بيانات الشاشة الرئيسية
    func loadData() async {
        guard !isLoading else { return }
        isLoading = true
        errorMessage = nil
        
        // تحميل الترند والجديد بالتوازي
        async let trendingTask = loadTrendingPlaces()
        async let newTask = loadNewPlaces()
        
        await trendingTask
        await newTask
        
        isLoading = false
        isDataLoaded = true
    }
    
    /// إعادة تحميل البيانات (Pull to Refresh)
    func refresh() async {
        isDataLoaded = false
        await loadData()
        
        // تحديث الأماكن القريبة
        if let location = locationService.currentLocation {
            await loadNearbyPlaces(location: location)
        }
    }
    
    // MARK: - تحميل الترند
    
    /// جلب الأماكن الأكثر شعبية
    private func loadTrendingPlaces() async {
        do {
            trendingPlaces = try await placesService.fetchTrending(limit: 10)
        } catch {
            AppConfig.debugLog("❌ فشل تحميل الترند: \(error)")
            errorMessage = "فشل تحميل الأماكن الشائعة"
        }
    }
    
    // MARK: - تحميل الجديد
    
    /// جلب الأماكن الجديدة
    private func loadNewPlaces() async {
        do {
            newPlaces = try await placesService.fetchNew(limit: 10)
        } catch {
            AppConfig.debugLog("❌ فشل تحميل الأماكن الجديدة: \(error)")
        }
    }
    
    // MARK: - تحميل القريب
    
    /// جلب الأماكن القريبة من الموقع
    private func loadNearbyPlaces(location: CLLocation) async {
        guard !isLoadingNearby else { return }
        isLoadingNearby = true
        
        do {
            nearbyPlaces = try await placesService.fetchNearby(
                latitude: location.coordinate.latitude,
                longitude: location.coordinate.longitude,
                radiusMeters: 5000,
                limit: 10
            )
        } catch {
            AppConfig.debugLog("❌ فشل تحميل الأماكن القريبة: \(error)")
            // نرتب الأماكن الموجودة حسب المسافة كـ fallback
            nearbyPlaces = locationService.sortByDistance(trendingPlaces)
        }
        
        isLoadingNearby = false
    }
    
    // MARK: - دوال مساعدة
    
    /// التحية حسب الوقت
    var greeting: String {
        let hour = Calendar.current.component(.hour, from: Date())
        switch hour {
        case 5..<12: return "صباح الخير ☀️"
        case 12..<17: return "مساء الخير 🌤"
        case 17..<21: return "مساء النور 🌅"
        default: return "أهلاً 🌙"
        }
    }
    
    /// اسم الحي الحالي
    var currentNeighborhood: String {
        locationService.currentNeighborhood ?? "الرياض"
    }
    
    /// هل الموقع متاح؟
    var isLocationAvailable: Bool {
        locationService.isLocationAvailable
    }
}
