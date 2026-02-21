// MapView.swift
// الخريطة — كل الأماكن على الخريطة
// هوية ليالي الرياض

import SwiftUI
import MapKit

struct MapView: View {
    @EnvironmentObject var appState: AppState
    @State private var selectedPlace: Place?
    @State private var selectedCategory: String?
    @State private var position: MapCameraPosition = .region(
        MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 24.7136, longitude: 46.6753), // وسط الرياض
            span: MKCoordinateSpan(latitudeDelta: 0.15, longitudeDelta: 0.15)
        )
    )
    
    private var filteredPlaces: [Place] {
        let places = appState.places.filter { $0.lat != nil && $0.lng != nil }
        if let cat = selectedCategory {
            return places.filter { $0.categoryAr == cat || $0.category == cat }
        }
        return places
    }
    
    var body: some View {
        ZStack(alignment: .top) {
            // الخريطة
            Map(position: $position, selection: $selectedPlace) {
                ForEach(filteredPlaces.prefix(500)) { place in
                    if let lat = place.lat, let lng = place.lng {
                        Marker(
                            place.nameAr,
                            systemImage: markerIcon(for: place.category),
                            coordinate: CLLocationCoordinate2D(latitude: lat, longitude: lng)
                        )
                        .tint(Color.categoryColor(for: place.categoryAr ?? place.category))
                        .tag(place)
                    }
                }
            }
            .mapStyle(.standard(elevation: .realistic, pointsOfInterest: .excludingAll))
            .ignoresSafeArea()
            
            // فلتر الفئات
            VStack(spacing: 0) {
                categoryFilter
                Spacer()
            }
            
            // بطاقة المكان المحدد
            if let place = selectedPlace {
                VStack {
                    Spacer()
                    selectedPlaceCard(place)
                }
            }
        }
    }
    
    // MARK: - فلتر الفئات
    
    private var categoryFilter: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: Theme.spacingS) {
                // الكل
                Button {
                    withAnimation { selectedCategory = nil }
                } label: {
                    Text("الكل")
                        .font(Theme.badge(size: 12))
                        .foregroundStyle(selectedCategory == nil ? .white : Theme.cream)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 7)
                        .background(
                            selectedCategory == nil
                                ? AnyShapeStyle(Theme.primaryGradient)
                                : AnyShapeStyle(.ultraThinMaterial)
                        )
                        .clipShape(Capsule())
                }
                
                ForEach(mapCategories, id: \.self) { cat in
                    Button {
                        withAnimation {
                            selectedCategory = selectedCategory == cat ? nil : cat
                        }
                    } label: {
                        Text(cat)
                            .font(Theme.badge(size: 12))
                            .foregroundStyle(selectedCategory == cat ? .white : Theme.cream)
                            .padding(.horizontal, 14)
                            .padding(.vertical, 7)
                            .background(
                                selectedCategory == cat
                                    ? AnyShapeStyle(Color.categoryColor(for: cat))
                                    : AnyShapeStyle(.ultraThinMaterial)
                            )
                            .clipShape(Capsule())
                    }
                }
            }
            .padding(.horizontal, Theme.spacingL)
            .padding(.top, 60) // safe area
            .padding(.bottom, Theme.spacingS)
        }
    }
    
    // MARK: - بطاقة المكان المحدد
    
    private func selectedPlaceCard(_ place: Place) -> some View {
        NavigationLink {
            PlaceDetailView(place: place)
        } label: {
            PlaceCard(place: place, style: .compact)
                .padding(.horizontal, Theme.spacingL)
                .padding(.bottom, 120)
        }
        .buttonStyle(.plain)
        .transition(.move(edge: .bottom).combined(with: .opacity))
    }
    
    // MARK: - Helpers
    
    private var mapCategories: [String] {
        ["مطاعم", "كافيهات", "ترفيه", "تسوق", "حلويات", "فنادق", "طبيعة"]
    }
    
    private func markerIcon(for category: String) -> String {
        switch category {
        case "restaurants", "مطاعم": return "fork.knife"
        case "cafes", "كافيهات": return "cup.and.saucer.fill"
        case "entertainment", "ترفيه": return "sparkles"
        case "shopping", "تسوق": return "bag.fill"
        case "hotels", "فنادق": return "bed.double.fill"
        case "nature", "طبيعة": return "leaf.fill"
        case "desserts", "حلويات": return "birthday.cake.fill"
        default: return "mappin"
        }
    }
}
