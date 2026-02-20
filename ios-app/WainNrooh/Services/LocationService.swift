// LocationService.swift
// خدمة الموقع — GPS + أماكن قريبة

import Foundation
import CoreLocation
import Combine

// MARK: - خدمة الموقع

/// خدمة الموقع الجغرافي — تتبع موقع المستخدم وحساب المسافات
final class LocationService: NSObject, ObservableObject, CLLocationManagerDelegate {
    
    // MARK: - خصائص منشورة
    
    /// الموقع الحالي
    @Published var currentLocation: CLLocation?
    
    /// الإحداثيات الحالية
    @Published var currentCoordinate: CLLocationCoordinate2D?
    
    /// حالة الصلاحية
    @Published var authorizationStatus: CLAuthorizationStatus = .notDetermined
    
    /// هل الموقع متاح؟
    @Published var isLocationAvailable: Bool = false
    
    /// رسالة الخطأ
    @Published var locationError: String?
    
    /// اسم الحي الحالي
    @Published var currentNeighborhood: String?
    
    // MARK: - خصائص خاصة
    
    private let locationManager = CLLocationManager()
    private let geocoder = CLGeocoder()
    
    /// الموقع الافتراضي (مركز الرياض)
    static let defaultLocation = CLLocation(
        latitude: AppConfig.riyadhCenterLatitude,
        longitude: AppConfig.riyadhCenterLongitude
    )
    
    /// الإحداثيات الافتراضية
    static let defaultCoordinate = CLLocationCoordinate2D(
        latitude: AppConfig.riyadhCenterLatitude,
        longitude: AppConfig.riyadhCenterLongitude
    )
    
    // MARK: - تهيئة
    
    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        locationManager.distanceFilter = 100 // تحديث كل 100 متر
    }
    
    // MARK: - طلب الصلاحية
    
    /// طلب صلاحية الموقع
    func requestPermission() {
        locationManager.requestWhenInUseAuthorization()
    }
    
    /// بدء تتبع الموقع
    func startTracking() {
        guard authorizationStatus == .authorizedWhenInUse ||
              authorizationStatus == .authorizedAlways else {
            requestPermission()
            return
        }
        locationManager.startUpdatingLocation()
    }
    
    /// إيقاف تتبع الموقع
    func stopTracking() {
        locationManager.stopUpdatingLocation()
    }
    
    /// طلب تحديث موقع واحد
    func requestSingleUpdate() {
        locationManager.requestLocation()
    }
    
    // MARK: - CLLocationManagerDelegate
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        
        // التحقق أن الموقع ضمن حدود الرياض
        if isInRiyadh(location.coordinate) {
            currentLocation = location
            currentCoordinate = location.coordinate
            isLocationAvailable = true
            locationError = nil
            
            // جلب اسم الحي
            reverseGeocode(location)
        } else {
            // المستخدم خارج الرياض — نستخدم الموقع الافتراضي
            AppConfig.debugLog("⚠️ المستخدم خارج نطاق الرياض")
            currentLocation = Self.defaultLocation
            currentCoordinate = Self.defaultCoordinate
            isLocationAvailable = true
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        AppConfig.debugLog("❌ خطأ في الموقع: \(error.localizedDescription)")
        locationError = "تعذر تحديد موقعك"
        
        // استخدام الموقع الافتراضي
        if currentLocation == nil {
            currentLocation = Self.defaultLocation
            currentCoordinate = Self.defaultCoordinate
        }
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        authorizationStatus = manager.authorizationStatus
        
        switch manager.authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways:
            startTracking()
        case .denied, .restricted:
            locationError = "الموقع غير مفعل — فعّله من الإعدادات"
            currentLocation = Self.defaultLocation
            currentCoordinate = Self.defaultCoordinate
            isLocationAvailable = true
        case .notDetermined:
            break
        @unknown default:
            break
        }
    }
    
    // MARK: - حسابات المسافة
    
    /// حساب المسافة بين الموقع الحالي ومكان
    func distance(to coordinate: CLLocationCoordinate2D) -> CLLocationDistance? {
        guard let current = currentLocation else { return nil }
        let target = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
        return current.distance(from: target)
    }
    
    /// حساب المسافة بالكيلومتر
    func distanceInKm(to coordinate: CLLocationCoordinate2D) -> Double? {
        guard let meters = distance(to: coordinate) else { return nil }
        return meters / 1000.0
    }
    
    /// نص المسافة المنسق
    func formattedDistance(to coordinate: CLLocationCoordinate2D) -> String? {
        guard let km = distanceInKm(to: coordinate) else { return nil }
        if km < 1.0 {
            return "\(Int(km * 1000)) م"
        }
        return String(format: "%.1f كم", km)
    }
    
    /// ترتيب الأماكن حسب المسافة
    func sortByDistance(_ places: [Place]) -> [Place] {
        guard let current = currentLocation else { return places }
        return places.sorted { a, b in
            let distA = a.distance(from: current) ?? Double.infinity
            let distB = b.distance(from: current) ?? Double.infinity
            return distA < distB
        }
    }
    
    // MARK: - دوال مساعدة
    
    /// هل الإحداثيات ضمن حدود الرياض؟
    func isInRiyadh(_ coordinate: CLLocationCoordinate2D) -> Bool {
        let bounds = AppConfig.riyadhBounds
        return coordinate.latitude >= bounds.minLat &&
               coordinate.latitude <= bounds.maxLat &&
               coordinate.longitude >= bounds.minLng &&
               coordinate.longitude <= bounds.maxLng
    }
    
    /// تحويل الإحداثيات إلى اسم الحي
    private func reverseGeocode(_ location: CLLocation) {
        geocoder.reverseGeocodeLocation(location) { [weak self] placemarks, error in
            guard let placemark = placemarks?.first else { return }
            
            DispatchQueue.main.async {
                self?.currentNeighborhood = placemark.subLocality ?? placemark.locality ?? "الرياض"
            }
        }
    }
    
    /// الموقع الحالي أو الافتراضي
    var effectiveLocation: CLLocation {
        currentLocation ?? Self.defaultLocation
    }
    
    /// الإحداثيات الحالية أو الافتراضية
    var effectiveCoordinate: CLLocationCoordinate2D {
        currentCoordinate ?? Self.defaultCoordinate
    }
}
