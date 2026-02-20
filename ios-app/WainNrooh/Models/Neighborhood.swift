// Neighborhood.swift
// موديل الأحياء — أحياء الرياض الرئيسية

import Foundation
import CoreLocation

// MARK: - حي

/// حي من أحياء الرياض
struct Neighborhood: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let nameAr: String
    let nameEn: String
    let latitude: Double?
    let longitude: Double?
    let placesCount: Int?
    
    enum CodingKeys: String, CodingKey {
        case id
        case nameAr = "name_ar"
        case nameEn = "name_en"
        case latitude
        case longitude
        case placesCount = "places_count"
    }
    
    /// الإحداثيات
    var coordinate: CLLocationCoordinate2D? {
        guard let lat = latitude, let lng = longitude else { return nil }
        return CLLocationCoordinate2D(latitude: lat, longitude: lng)
    }
    
    /// عدد الأماكن المنسق
    var formattedPlacesCount: String {
        guard let count = placesCount else { return "" }
        return "\(count) مكان"
    }
}

// MARK: - الأحياء الرئيسية

extension Neighborhood {
    
    /// أحياء الرياض الرئيسية (بيانات ثابتة للاستخدام الأولي)
    static let mainNeighborhoods: [Neighborhood] = [
        Neighborhood(id: "olaya", nameAr: "العليا", nameEn: "Olaya",
                     latitude: 24.6908, longitude: 46.6854, placesCount: nil),
        Neighborhood(id: "tahlia", nameAr: "التحلية", nameEn: "Tahlia",
                     latitude: 24.6882, longitude: 46.6805, placesCount: nil),
        Neighborhood(id: "malaz", nameAr: "الملز", nameEn: "Malaz",
                     latitude: 24.6603, longitude: 46.7387, placesCount: nil),
        Neighborhood(id: "hittin", nameAr: "حطين", nameEn: "Hittin",
                     latitude: 24.7571, longitude: 46.6350, placesCount: nil),
        Neighborhood(id: "nakheel", nameAr: "النخيل", nameEn: "Al Nakheel",
                     latitude: 24.7633, longitude: 46.6480, placesCount: nil),
        Neighborhood(id: "sulaimaniya", nameAr: "السليمانية", nameEn: "Sulaimaniya",
                     latitude: 24.6970, longitude: 46.7131, placesCount: nil),
        Neighborhood(id: "rabwa", nameAr: "الربوة", nameEn: "Al Rabwa",
                     latitude: 24.6546, longitude: 46.7191, placesCount: nil),
        Neighborhood(id: "diriyah", nameAr: "الدرعية", nameEn: "Diriyah",
                     latitude: 24.7342, longitude: 46.5726, placesCount: nil),
        Neighborhood(id: "yasmin", nameAr: "الياسمين", nameEn: "Al Yasmin",
                     latitude: 24.8062, longitude: 46.6271, placesCount: nil),
        Neighborhood(id: "hamra", nameAr: "الحمراء", nameEn: "Al Hamra",
                     latitude: 24.7256, longitude: 46.7168, placesCount: nil),
        Neighborhood(id: "sahafa", nameAr: "الصحافة", nameEn: "Al Sahafa",
                     latitude: 24.7879, longitude: 46.6658, placesCount: nil),
        Neighborhood(id: "muruj", nameAr: "المروج", nameEn: "Al Muruj",
                     latitude: 24.7430, longitude: 46.6567, placesCount: nil),
        Neighborhood(id: "exit", nameAr: "المخرج", nameEn: "Exit",
                     latitude: 24.6950, longitude: 46.6800, placesCount: nil),
        Neighborhood(id: "qurtuba", nameAr: "قرطبة", nameEn: "Qurtuba",
                     latitude: 24.7500, longitude: 46.7700, placesCount: nil),
        Neighborhood(id: "rawdah", nameAr: "الروضة", nameEn: "Al Rawdah",
                     latitude: 24.6670, longitude: 46.7450, placesCount: nil),
        Neighborhood(id: "naseem", nameAr: "النسيم", nameEn: "Al Naseem",
                     latitude: 24.6690, longitude: 46.7900, placesCount: nil),
        Neighborhood(id: "suwaidi", nameAr: "السويدي", nameEn: "Al Suwaidi",
                     latitude: 24.6120, longitude: 46.6570, placesCount: nil),
        Neighborhood(id: "aqiq", nameAr: "العقيق", nameEn: "Al Aqiq",
                     latitude: 24.7700, longitude: 46.6180, placesCount: nil),
    ]
    
    /// البحث في الأحياء
    static func search(query: String) -> [Neighborhood] {
        let normalizedQuery = query.arabicNormalized.lowercased()
        return mainNeighborhoods.filter { hood in
            hood.nameAr.arabicNormalized.lowercased().contains(normalizedQuery) ||
            hood.nameEn.lowercased().contains(normalizedQuery)
        }
    }
}
