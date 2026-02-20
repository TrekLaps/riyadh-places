// PlaceDetailView.swift
// صفحة تفاصيل المكان — كل المعلومات + أسعار + توصيل

import SwiftUI

// MARK: - صفحة تفاصيل المكان

/// صفحة المكان الكاملة — صور + أسعار + مقارنة توصيل + خريطة
struct PlaceDetailView: View {
    
    @StateObject private var viewModel: PlaceDetailViewModel
    @Environment(\.dismiss) private var dismiss
    
    init(place: Place) {
        _viewModel = StateObject(wrappedValue: PlaceDetailViewModel(place: place))
    }
    
    var body: some View {
        ScrollView {
            VStack(spacing: 0) {
                // الصورة الرئيسية
                heroImage
                
                // المحتوى
                VStack(spacing: Theme.spacingLarge + 4) {
                    // معلومات أساسية
                    basicInfoSection
                    
                    // الميزات
                    if let features = viewModel.place.features {
                        featuresSection(features)
                    }
                    
                    // Perfect For
                    if let tags = viewModel.place.perfectFor, !tags.isEmpty {
                        perfectForSection(tags)
                    }
                    
                    Divider().padding(.horizontal)
                    
                    // مقارنة أسعار التوصيل
                    deliverySection
                    
                    Divider().padding(.horizontal)
                    
                    // أسعار المنيو
                    menuSection
                    
                    Divider().padding(.horizontal)
                    
                    // الخريطة
                    if viewModel.place.coordinate != nil {
                        mapSection
                    }
                    
                    // معلومات التواصل
                    contactSection
                    
                    // أماكن مشابهة
                    if !viewModel.similarPlaces.isEmpty {
                        similarSection
                    }
                    
                    Spacer(minLength: 100)
                }
                .padding(.top, Theme.paddingMedium)
            }
        }
        .background(Color.appBackground)
        .ignoresSafeArea(edges: .top)
        .navigationBarBackButtonHidden(true)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                HStack(spacing: 12) {
                    Button { dismiss() } label: {
                        Image(systemName: "chevron.right")
                            .font(.system(size: 16, weight: .semibold))
                            .foregroundStyle(.white)
                            .padding(8)
                            .background(.ultraThinMaterial)
                            .clipShape(Circle())
                    }
                }
            }
            
            ToolbarItem(placement: .topBarLeading) {
                HStack(spacing: 8) {
                    ShareLink(item: viewModel.sharePlace()) {
                        Image(systemName: "square.and.arrow.up")
                            .font(.system(size: 14))
                            .foregroundStyle(.white)
                            .padding(8)
                            .background(.ultraThinMaterial)
                            .clipShape(Circle())
                    }
                    
                    Button { viewModel.toggleFavorite() } label: {
                        Image(systemName: viewModel.isFavorite ? "heart.fill" : "heart")
                            .font(.system(size: 14))
                            .foregroundStyle(viewModel.isFavorite ? .red : .white)
                            .padding(8)
                            .background(.ultraThinMaterial)
                            .clipShape(Circle())
                    }
                }
            }
        }
        .task {
            await viewModel.loadAllData()
        }
    }
    
    // MARK: - الصورة الرئيسية
    
    private var heroImage: some View {
        ZStack(alignment: .bottomTrailing) {
            if let imageUrl = viewModel.place.coverImageUrl, let url = URL(string: imageUrl) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .success(let image):
                        image.resizable().aspectRatio(contentMode: .fill)
                    default:
                        heroPlaceholder
                    }
                }
            } else {
                heroPlaceholder
            }
        }
        .frame(height: 280)
        .clipped()
    }
    
    private var heroPlaceholder: some View {
        ZStack {
            LinearGradient(
                colors: [viewModel.place.category.color.opacity(0.4), Color.appBackground],
                startPoint: .top, endPoint: .bottom
            )
            Text(viewModel.place.category.emoji)
                .font(.system(size: 64))
        }
    }
    
    // MARK: - معلومات أساسية
    
    private var basicInfoSection: some View {
        VStack(alignment: .trailing, spacing: 8) {
            // الاسم
            Text(viewModel.place.name)
                .font(Theme.titleFont(size: 24))
                .foregroundStyle(Color.appTextPrimary)
            
            // التصنيف + الحي
            HStack(spacing: 8) {
                if let neighborhood = viewModel.place.neighborhood {
                    Label(neighborhood, systemImage: "mappin.circle.fill")
                        .font(Theme.captionFont())
                        .foregroundStyle(Color.appTextSecondary)
                }
                
                Text("•")
                    .foregroundStyle(Color.appTextSecondary)
                
                HStack(spacing: 4) {
                    Text(viewModel.place.category.nameAr)
                    Text(viewModel.place.category.emoji)
                }
                .font(Theme.captionFont())
                .foregroundStyle(viewModel.place.category.color)
            }
            
            // التقييم + السعر
            HStack(spacing: Theme.spacingMedium) {
                if let priceRange = viewModel.place.priceRange {
                    PriceTag(priceRange: priceRange, size: .medium)
                }
                
                Spacer()
                
                if let rating = viewModel.place.rating {
                    RatingView(
                        rating: rating,
                        size: .medium,
                        showCount: true,
                        count: viewModel.place.ratingCount
                    )
                }
            }
            
            // الوصف
            if let description = viewModel.place.description {
                Text(description)
                    .font(Theme.bodyFont(size: 14))
                    .foregroundStyle(Color.appTextSecondary)
                    .multilineTextAlignment(.trailing)
                    .lineLimit(3)
            }
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
    
    // MARK: - الميزات
    
    private func featuresSection(_ features: PlaceFeatures) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingSmall) {
            Text("الميزات")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
            
            FlowLayout(spacing: 8) {
                ForEach(features.availableFeatures, id: \.label) { feature in
                    Label(feature.label, systemImage: feature.icon)
                        .font(Theme.captionFont(size: 12))
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Theme.accent.opacity(0.1))
                        .foregroundStyle(Theme.accent)
                        .clipShape(Capsule())
                }
            }
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
    
    // MARK: - Perfect For
    
    private func perfectForSection(_ tags: [String]) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingSmall) {
            Text("مناسب لـ")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
            
            PerfectForTags(tags: tags, size: .medium)
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
    
    // MARK: - قسم التوصيل
    
    private var deliverySection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            SectionHeader(title: "🛵 مقارنة التوصيل", showSeeAll: false)
            
            if viewModel.isLoadingDelivery {
                ProgressView("جاري تحميل الأسعار...")
                    .padding()
            } else if let comparison = viewModel.deliveryComparison, !comparison.prices.isEmpty {
                DeliveryCompareView(comparison: comparison)
            } else {
                Text("لا توجد بيانات توصيل لهذا المكان")
                    .font(Theme.captionFont())
                    .foregroundStyle(Color.appTextSecondary)
                    .padding()
            }
        }
    }
    
    // MARK: - قسم المنيو
    
    private var menuSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            SectionHeader(title: "💰 الأسعار", showSeeAll: false)
            
            if viewModel.isLoadingMenu {
                ProgressView("جاري تحميل الأسعار...")
                    .padding()
            } else if !viewModel.menuPrices.isEmpty {
                MenuPriceView(categories: viewModel.menuCategories)
            } else {
                Text("لا توجد أسعار منيو لهذا المكان")
                    .font(Theme.captionFont())
                    .foregroundStyle(Color.appTextSecondary)
                    .padding()
            }
        }
    }
    
    // MARK: - الخريطة
    
    private var mapSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            SectionHeader(title: "📍 الموقع", showSeeAll: false)
            
            MapPreviewView(
                coordinate: viewModel.place.coordinate!,
                title: viewModel.place.name
            )
            .frame(height: 200)
            .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
            .padding(.horizontal, Theme.paddingMedium)
            .onTapGesture {
                viewModel.openInGoogleMaps()
            }
            
            if let address = viewModel.place.address {
                Text(address)
                    .font(Theme.captionFont())
                    .foregroundStyle(Color.appTextSecondary)
                    .padding(.horizontal, Theme.paddingMedium)
            }
        }
    }
    
    // MARK: - التواصل
    
    private var contactSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingSmall) {
            if viewModel.place.phone != nil || viewModel.place.instagram != nil {
                Text("التواصل")
                    .font(Theme.headlineFont(size: 16))
                    .foregroundStyle(Color.appTextPrimary)
                    .padding(.horizontal, Theme.paddingMedium)
                
                HStack(spacing: Theme.spacingMedium) {
                    // Google Maps
                    Button { viewModel.openInGoogleMaps() } label: {
                        Label("وصلني", systemImage: "map.fill")
                            .secondaryButtonStyle()
                    }
                    
                    // الاتصال
                    if viewModel.place.phone != nil {
                        Button { viewModel.callPlace() } label: {
                            Label("اتصل", systemImage: "phone.fill")
                                .secondaryButtonStyle()
                        }
                    }
                    
                    Spacer()
                }
                .padding(.horizontal, Theme.paddingMedium)
            }
        }
    }
    
    // MARK: - أماكن مشابهة
    
    private var similarSection: some View {
        VStack(spacing: Theme.spacingMedium) {
            SectionHeader(title: "أماكن مشابهة")
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingMedium) {
                    ForEach(viewModel.similarPlaces) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            TrendingCard(place: place)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, Theme.paddingMedium)
            }
        }
    }
}
