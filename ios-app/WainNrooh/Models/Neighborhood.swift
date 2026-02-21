// Neighborhood.swift
// أحياء الرياض

import Foundation
import CoreLocation

struct Neighborhood: Identifiable, Hashable {
    let id: String
    let nameAr: String
    let nameEn: String
    let lat: Double
    let lng: Double
    
    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: lat, longitude: lng)
    }
    
    // Top neighborhoods by place count
    static let popular: [Neighborhood] = [
        Neighborhood(id: "olaya", nameAr: "العليا", nameEn: "Al Olaya", lat: 24.6980, lng: 46.6850),
        Neighborhood(id: "narjis", nameAr: "النرجس", nameEn: "An Narjis", lat: 24.8200, lng: 46.6300),
        Neighborhood(id: "malqa", nameAr: "الملقا", nameEn: "Al Malqa", lat: 24.8100, lng: 46.6100),
        Neighborhood(id: "yasmin", nameAr: "الياسمين", nameEn: "Al Yasmin", lat: 24.8250, lng: 46.6600),
        Neighborhood(id: "sulaimaniyah", nameAr: "السليمانية", nameEn: "As Sulaimaniyah", lat: 24.6900, lng: 46.7100),
        Neighborhood(id: "hittin", nameAr: "حطين", nameEn: "Hittin", lat: 24.7600, lng: 46.6300),
        Neighborhood(id: "rabee", nameAr: "الربيع", nameEn: "Ar Rabee", lat: 24.7800, lng: 46.6400),
        Neighborhood(id: "aqiq", nameAr: "العقيق", nameEn: "Al Aqiq", lat: 24.7700, lng: 46.6200),
        Neighborhood(id: "sahafa", nameAr: "الصحافة", nameEn: "As Sahafah", lat: 24.7900, lng: 46.6700),
        Neighborhood(id: "wurud", nameAr: "الورود", nameEn: "Al Wurud", lat: 24.6950, lng: 46.6750),
    ]
}
