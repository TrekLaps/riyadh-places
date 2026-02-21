// MapView.swift
// خريطة تفاعلية — MapKit + clustering + category filter

import SwiftUI
import MapKit

struct MapView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var locationService = LocationService.shared
    @State private var position: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: AppConfig.riyadhLat, longitude: AppConfig.riyadhLng),
        span: MKCoordinateSpan(latitudeDelta: 0.15, longitudeDelta: 0.15)
    ))
    @State private var selectedPlace: Place?
    @State private var selectedCategory: String?
    
    var visiblePlaces: [Place] {
        var places = appState.places.filter { $0.coordinate != nil }
        if let cat = selectedCategory {
            places = places.filter { ($0.categoryEn ?? $0.category) == cat }
        }
        // Limit markers for performance
        return Array(places.prefix(500))
    }
    
    var body: some View {
        NavigationStack {
            ZStack(alignment: .top) {
                Map(position: $position, selection: $selectedPlace) {
                    ForEach(visiblePlaces) { place in
                        if let coord = place.coordinate {
                            Marker(place.nameAr, systemImage: markerIcon(for: place),
                                   coordinate: coord)
                                .tint(markerColor(for: place))
                                .tag(place)
                        }
                    }
                    
                    // User location
                    UserAnnotation()
                }
                .mapControls {
                    MapUserLocationButton()
                    MapCompass()
                    MapScaleView()
                }
                
                // Category filter bar
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        PillButton(title: "الكل", isSelected: selectedCategory == nil) {
                            selectedCategory = nil
                        }
                        ForEach(["restaurant", "cafe", "entertainment", "shopping", "nature"], id: \.self) { cat in
                            let names: [String: String] = [
                                "restaurant": "🍽️ مطاعم", "cafe": "☕ كافيهات",
                                "entertainment": "🎭 ترفيه", "shopping": "🛍️ تسوق",
                                "nature": "🌳 طبيعة"
                            ]
                            PillButton(title: names[cat] ?? cat, isSelected: selectedCategory == cat) {
                                withAnimation { selectedCategory = selectedCategory == cat ? nil : cat }
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.top, 8)
                }
            }
            .navigationTitle("الخريطة")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(item: $selectedPlace) { place in
                PlaceDetailView(place: place)
                    .presentationDetents([.medium, .large])
            }
            .onAppear {
                locationService.requestPermission()
            }
        }
    }
    
    // MARK: - Marker Helpers
    
    private func markerIcon(for place: Place) -> String {
        switch place.categoryEn ?? place.category {
        case "restaurant": return "fork.knife"
        case "cafe": return "cup.and.saucer.fill"
        case "entertainment": return "sparkles"
        case "shopping": return "bag.fill"
        case "nature": return "leaf.fill"
        case "hotels": return "building.2.fill"
        case "malls": return "building.columns.fill"
        default: return "mappin"
        }
    }
    
    private func markerColor(for place: Place) -> Color {
        switch place.categoryEn ?? place.category {
        case "restaurant": return .orange
        case "cafe": return .brown
        case "entertainment": return .purple
        case "shopping": return .pink
        case "nature": return .green
        case "hotels": return .blue
        default: return Theme.primary
        }
    }
}
