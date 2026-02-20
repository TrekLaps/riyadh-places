// HomeView.swift
// الشاشة الرئيسية — ترند + قريب + تصنيفات

import SwiftUI

// MARK: - الشاشة الرئيسية

/// الشاشة الرئيسية — اكتشف أماكن الرياض
struct HomeView: View {
    
    @StateObject private var viewModel = HomeViewModel()
    @EnvironmentObject var locationService: LocationService
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: Theme.spacingLarge + 4) {
                    // الترحيب
                    headerSection
                    
                    // التصنيفات
                    categoriesSection
                    
                    // الأكثر شعبية (ترند)
                    if !viewModel.trendingPlaces.isEmpty {
                        trendingSection
                    }
                    
                    // قريب منك
                    if !viewModel.nearbyPlaces.isEmpty {
                        nearbySection
                    }
                    
                    // الجديد
                    if !viewModel.newPlaces.isEmpty {
                        newPlacesSection
                    }
                    
                    Spacer(minLength: 80)
                }
            }
            .background(Color.appBackground)
            .refreshable {
                await viewModel.refresh()
            }
            .task {
                if !viewModel.isDataLoaded {
                    await viewModel.loadData()
                }
            }
            .navigationBarHidden(true)
        }
    }
    
    // MARK: - قسم الترحيب
    
    private var headerSection: some View {
        VStack(alignment: .trailing, spacing: 8) {
            HStack {
                // زر الإشعارات
                Button {
                    // TODO: شاشة الإشعارات
                } label: {
                    Image(systemName: "bell.fill")
                        .font(.system(size: 20))
                        .foregroundStyle(Color.appTextSecondary)
                }
                
                Spacer()
                
                VStack(alignment: .trailing, spacing: 4) {
                    Text(viewModel.greeting)
                        .font(Theme.titleFont(size: 24))
                        .foregroundStyle(Color.appTextPrimary)
                    
                    HStack(spacing: 4) {
                        Text(viewModel.currentNeighborhood)
                            .font(Theme.captionFont())
                            .foregroundStyle(Color.appTextSecondary)
                        
                        Image(systemName: "location.fill")
                            .font(.system(size: 10))
                            .foregroundStyle(Theme.primary)
                    }
                }
            }
            
            // شريط بحث سريع
            NavigationLink {
                SearchView()
            } label: {
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(Color.appTextSecondary)
                    
                    Spacer()
                    
                    Text("ابحث عن مكان...")
                        .font(Theme.bodyFont(size: 15))
                        .foregroundStyle(Color.appTextSecondary)
                }
                .padding(Theme.paddingMedium)
                .background(Color.appSecondaryBackground)
                .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
            }
        }
        .padding(.horizontal, Theme.paddingMedium)
        .padding(.top, Theme.paddingMedium)
    }
    
    // MARK: - قسم التصنيفات
    
    private var categoriesSection: some View {
        VStack(spacing: Theme.spacingMedium) {
            SectionHeader(title: "التصنيفات", showSeeAll: false)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingMedium) {
                    ForEach(viewModel.categories) { category in
                        NavigationLink {
                            // TODO: شاشة التصنيف
                            SearchView()
                        } label: {
                            CategoryCard(category: category)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, Theme.paddingMedium)
            }
        }
    }
    
    // MARK: - قسم الترند
    
    private var trendingSection: some View {
        VStack(spacing: Theme.spacingMedium) {
            SectionHeader(title: "🔥 الأكثر شعبية", subtitle: "الأعلى تقييماً بالرياض")
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingMedium) {
                    ForEach(viewModel.trendingPlaces) { place in
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
    
    // MARK: - قسم القريب
    
    private var nearbySection: some View {
        VStack(spacing: Theme.spacingMedium) {
            SectionHeader(title: "📍 قريب منك", subtitle: viewModel.currentNeighborhood)
            
            LazyVStack(spacing: Theme.spacingMedium) {
                ForEach(viewModel.nearbyPlaces) { place in
                    NavigationLink {
                        PlaceDetailView(place: place)
                    } label: {
                        PlaceCard(
                            place: place,
                            showDistance: true,
                            distance: place.formattedDistance(from: locationService.effectiveLocation)
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, Theme.paddingMedium)
        }
    }
    
    // MARK: - قسم الجديد
    
    private var newPlacesSection: some View {
        VStack(spacing: Theme.spacingMedium) {
            SectionHeader(title: "✨ جديد", subtitle: "أماكن مضافة مؤخراً")
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingMedium) {
                    ForEach(viewModel.newPlaces) { place in
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
