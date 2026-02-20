// MapView.swift
// خريطة تفاعلية — كل الأماكن على الخريطة

import SwiftUI
import MapKit

// MARK: - شاشة الخريطة

/// خريطة تفاعلية كاملة — عرض كل الأماكن مع فلاتر
struct MapView: View {
    
    @EnvironmentObject var locationService: LocationService
    @State private var cameraPosition: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(
            latitude: AppConfig.riyadhCenterLatitude,
            longitude: AppConfig.riyadhCenterLongitude
        ),
        span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
    ))
    @State private var selectedPlace: Place?
    @State private var places: [Place] = []
    @State private var selectedCategory: PlaceCategory?
    @State private var isLoading = false
    @State private var mapStyle: MapStyleOption = .standard
    
    var body: some View {
        NavigationStack {
            ZStack {
                // الخريطة
                Map(position: $cameraPosition, selection: $selectedPlace) {
                    // موقع المستخدم
                    UserAnnotation()
                    
                    // علامات الأماكن
                    ForEach(filteredPlaces) { place in
                        if let coordinate = place.coordinate {
                            Annotation(
                                place.name,
                                coordinate: coordinate,
                                anchor: .bottom
                            ) {
                                placeAnnotation(place)
                            }
                            .tag(place)
                        }
                    }
                }
                .mapStyle(mapStyle.style)
                .mapControls {
                    MapUserLocationButton()
                    MapCompass()
                    MapScaleView()
                }
                
                // طبقة الفلاتر العلوية
                VStack {
                    // فلاتر التصنيف
                    categoryFilterBar
                    
                    Spacer()
                    
                    // بطاقة المكان المختار
                    if let place = selectedPlace {
                        selectedPlaceCard(place)
                    }
                    
                    // أزرار التحكم
                    controlButtons
                }
            }
            .navigationTitle("الخريطة 🗺")
            .navigationBarTitleDisplayMode(.inline)
            .task {
                await loadPlaces()
            }
        }
    }
    
    // MARK: - علامة المكان
    
    private func placeAnnotation(_ place: Place) -> some View {
        VStack(spacing: 0) {
            ZStack {
                Circle()
                    .fill(place.category.color)
                    .frame(width: 36, height: 36)
                    .shadow(radius: 2)
                
                Text(place.category.emoji)
                    .font(.system(size: 18))
            }
            
            // المثلث السفلي
            Triangle()
                .fill(place.category.color)
                .frame(width: 12, height: 8)
        }
        .onTapGesture {
            selectedPlace = place
        }
    }
    
    // MARK: - شريط فلاتر التصنيف
    
    private var categoryFilterBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                // الكل
                Button {
                    selectedCategory = nil
                } label: {
                    Text("الكل")
                        .font(Theme.captionFont(size: 12))
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .foregroundStyle(selectedCategory == nil ? .white : Color.appTextPrimary)
                        .background(selectedCategory == nil ? Theme.primary : Color.appCardBackground)
                        .clipShape(Capsule())
                        .shadow(radius: 1)
                }
                
                ForEach(PlaceCategory.popular) { category in
                    Button {
                        selectedCategory = selectedCategory == category ? nil : category
                    } label: {
                        HStack(spacing: 4) {
                            Text(category.emoji)
                            Text(category.nameAr)
                                .font(Theme.captionFont(size: 12))
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .foregroundStyle(
                            selectedCategory == category ? .white : Color.appTextPrimary
                        )
                        .background(
                            selectedCategory == category ? category.color : Color.appCardBackground
                        )
                        .clipShape(Capsule())
                        .shadow(radius: 1)
                    }
                }
            }
            .padding(.horizontal, Theme.paddingMedium)
            .padding(.top, Theme.paddingSmall)
        }
    }
    
    // MARK: - بطاقة المكان المختار
    
    private func selectedPlaceCard(_ place: Place) -> some View {
        NavigationLink {
            PlaceDetailView(place: place)
        } label: {
            HStack(spacing: 12) {
                // صورة
                ZStack {
                    place.category.color.opacity(0.15)
                    Text(place.category.emoji)
                        .font(.system(size: 24))
                }
                .frame(width: 60, height: 60)
                .clipShape(RoundedRectangle(cornerRadius: 8))
                
                // معلومات
                VStack(alignment: .trailing, spacing: 4) {
                    Text(place.name)
                        .font(Theme.headlineFont(size: 15))
                        .foregroundStyle(Color.appTextPrimary)
                    
                    HStack(spacing: 8) {
                        if let priceRange = place.priceRange {
                            PriceTag(priceRange: priceRange, size: .small)
                        }
                        Spacer()
                        if let rating = place.rating {
                            CompactRating(rating: rating)
                        }
                    }
                }
                .frame(maxWidth: .infinity)
                
                Image(systemName: "chevron.left")
                    .foregroundStyle(Color.appTextSecondary)
            }
            .padding(Theme.paddingSmall + 4)
            .background(.regularMaterial)
            .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
            .shadow(radius: 4)
            .padding(.horizontal, Theme.paddingMedium)
        }
        .buttonStyle(.plain)
    }
    
    // MARK: - أزرار التحكم
    
    private var controlButtons: some View {
        HStack {
            // تغيير نمط الخريطة
            Button {
                mapStyle = mapStyle.next
            } label: {
                Image(systemName: mapStyle.icon)
                    .font(.system(size: 16))
                    .foregroundStyle(Color.appTextPrimary)
                    .padding(10)
                    .background(.regularMaterial)
                    .clipShape(Circle())
                    .shadow(radius: 2)
            }
            
            Spacer()
        }
        .padding(.horizontal, Theme.paddingMedium)
        .padding(.bottom, Theme.paddingSmall)
    }
    
    // MARK: - بيانات
    
    private var filteredPlaces: [Place] {
        if let category = selectedCategory {
            return places.filter { $0.category == category }
        }
        return places
    }
    
    private func loadPlaces() async {
        isLoading = true
        do {
            places = try await PlacesService.shared.fetchPlaces(page: 1, perPage: 100)
        } catch {
            AppConfig.debugLog("❌ فشل تحميل الأماكن للخريطة: \(error)")
        }
        isLoading = false
    }
}

// MARK: - مثلث (للعلامة)

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.minY))
        path.closeSubpath()
        return path
    }
}

// MARK: - أنماط الخريطة

enum MapStyleOption {
    case standard
    case satellite
    case hybrid
    
    var style: MapStyle {
        switch self {
        case .standard: return .standard
        case .satellite: return .imagery
        case .hybrid: return .hybrid
        }
    }
    
    var icon: String {
        switch self {
        case .standard: return "map"
        case .satellite: return "globe.americas"
        case .hybrid: return "square.stack.3d.up"
        }
    }
    
    var next: MapStyleOption {
        switch self {
        case .standard: return .satellite
        case .satellite: return .hybrid
        case .hybrid: return .standard
        }
    }
}
