// HomeView.swift
// الرئيسية — هوية ليالي الرياض
// أقسام: بحث → مناسبات → ترند → أفضل ١٠ → جديد → التصنيفات

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var viewModel = HomeViewModel()
    
    var body: some View {
        NavigationStack {
            ScrollView(showsIndicators: false) {
                VStack(spacing: Theme.spacingXL) {
                    // الهيدر + البحث
                    headerSection
                    
                    // وش المناسبة؟
                    occasionSection
                    
                    // 🔥 الترند
                    if !viewModel.trendingPlaces.isEmpty {
                        trendingSection
                    }
                    
                    // 🏆 أفضل ١٠ بالحي
                    if let topPlaces = viewModel.topInNeighborhood, !topPlaces.isEmpty {
                        topNeighborhoodSection(topPlaces)
                    }
                    
                    // ✨ جديد
                    if !viewModel.newPlaces.isEmpty {
                        newSection
                    }
                    
                    // التصنيفات
                    categoriesGrid
                    
                    Spacer(minLength: 100)
                }
            }
            .background(Color.appBackground)
            .refreshable {
                await viewModel.loadData(places: appState.places)
            }
            .task {
                await viewModel.loadData(places: appState.places)
            }
            .navigationBarHidden(true)
        }
    }
    
    // MARK: - الهيدر
    
    private var headerSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingL) {
            // الشعار + الإشعارات
            HStack {
                // إشعارات
                Button {} label: {
                    Image(systemName: "bell.fill")
                        .font(.title3)
                        .foregroundStyle(Theme.sand)
                        .frame(width: 44, height: 44)
                        .background(Theme.green400.opacity(0.1))
                        .clipShape(Circle())
                }
                
                Spacer()
                
                // العنوان
                VStack(alignment: .trailing, spacing: 2) {
                    Text("وين نروح؟")
                        .font(Theme.largeTitle())
                        .foregroundStyle(.appTextPrimary)
                    
                    Text("أكثر من \(appState.places.count) مكان بالرياض")
                        .font(Theme.caption())
                        .foregroundStyle(.appTextSecondary)
                }
            }
            
            // شريط البحث
            NavigationLink {
                ExploreView()
            } label: {
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(Theme.green400)
                    Spacer()
                    Text("وش تبي تسوي اليوم؟")
                        .font(Theme.body())
                        .foregroundStyle(.appTextSecondary)
                }
                .padding(Theme.spacingL)
                .background(.ultraThinMaterial)
                .clipShape(Capsule())
                .overlay(
                    Capsule()
                        .stroke(Theme.green400.opacity(0.2), lineWidth: 1)
                )
            }
        }
        .padding(.horizontal, Theme.spacingL)
        .padding(.top, Theme.spacingL)
    }
    
    // MARK: - وش المناسبة؟
    
    private var occasionSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingM) {
            sectionHeader(title: "وش المناسبة؟", emoji: "🌙")
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingM) {
                    ForEach(Occasion.allCases) { occasion in
                        NavigationLink {
                            OccasionResultsView(occasion: occasion, places: appState.places)
                        } label: {
                            VStack(spacing: Theme.spacingS) {
                                Text(occasion.emoji)
                                    .font(.title)
                                    .frame(width: 52, height: 52)
                                    .background(Theme.green400.opacity(0.1))
                                    .clipShape(Circle())
                                
                                Text(occasion.nameAr)
                                    .font(Theme.badge(size: 12))
                                    .foregroundStyle(.appTextPrimary)
                            }
                            .frame(width: 75)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, Theme.spacingL)
            }
        }
    }
    
    // MARK: - الترند
    
    private var trendingSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingM) {
            sectionHeaderWithAction(title: "الأكثر شعبية", emoji: "🔥")
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingL) {
                    ForEach(viewModel.trendingPlaces.prefix(10)) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceCard(place: place)
                                .frame(width: 260)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, Theme.spacingL)
            }
        }
    }
    
    // MARK: - أفضل ١٠ بالحي
    
    private func topNeighborhoodSection(_ places: [Place]) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingM) {
            sectionHeaderWithAction(
                title: "أفضل ١٠ — \(viewModel.currentNeighborhood)",
                emoji: "🏆"
            )
            
            LazyVStack(spacing: Theme.spacingS) {
                ForEach(Array(places.enumerated()), id: \.element.id) { index, place in
                    NavigationLink {
                        PlaceDetailView(place: place)
                    } label: {
                        TopPlaceRow(place: place, rank: index + 1)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, Theme.spacingL)
        }
    }
    
    // MARK: - جديد بالرياض
    
    private var newSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingM) {
            sectionHeader(title: "جديد بالرياض", emoji: "✨")
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Theme.spacingM) {
                    ForEach(viewModel.newPlaces.prefix(8)) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceCard(place: place, style: .mini)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, Theme.spacingL)
            }
        }
    }
    
    // MARK: - التصنيفات
    
    private var categoriesGrid: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingM) {
            sectionHeader(title: "التصنيفات", emoji: "📂")
            
            LazyVGrid(
                columns: Array(repeating: GridItem(.flexible(), spacing: Theme.spacingM), count: 4),
                spacing: Theme.spacingM
            ) {
                ForEach(viewModel.categories, id: \.id) { cat in
                    NavigationLink {
                        CategoryPlacesView(category: cat, places: appState.places)
                    } label: {
                        VStack(spacing: Theme.spacingXS) {
                            ZStack {
                                Circle()
                                    .fill(Color.categoryColor(for: cat.nameAr).opacity(0.15))
                                    .frame(width: 48, height: 48)
                                Text(cat.emoji)
                                    .font(.title3)
                            }
                            
                            Text(cat.nameAr)
                                .font(Theme.badge(size: 11))
                                .foregroundStyle(.appTextPrimary)
                                .lineLimit(1)
                            
                            Text("\(cat.count)")
                                .font(Theme.badge(size: 10))
                                .foregroundStyle(.appTextSecondary)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, Theme.spacingM)
                        .background(Color.appCardBackground)
                        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, Theme.spacingL)
        }
    }
    
    // MARK: - عناوين الأقسام
    
    private func sectionHeader(title: String, emoji: String) -> some View {
        HStack {
            Spacer()
            Text("\(emoji) \(title)")
                .font(Theme.headline())
                .foregroundStyle(.appTextPrimary)
        }
        .padding(.horizontal, Theme.spacingL)
    }
    
    private func sectionHeaderWithAction(title: String, emoji: String) -> some View {
        HStack {
            Text("عرض الكل")
                .font(Theme.caption())
                .foregroundStyle(Theme.green400)
            
            Image(systemName: "chevron.left")
                .font(.system(size: 10))
                .foregroundStyle(Theme.green400)
            
            Spacer()
            
            Text("\(emoji) \(title)")
                .font(Theme.headline())
                .foregroundStyle(.appTextPrimary)
        }
        .padding(.horizontal, Theme.spacingL)
    }
}

// MARK: - صف أفضل ١٠ (ذهب/فضة/برونز)

struct TopPlaceRow: View {
    let place: Place
    let rank: Int
    
    private var medalColor: Color {
        switch rank {
        case 1: return Theme.gold500        // 🥇
        case 2: return Color(hex: "C0C0C0") // 🥈
        case 3: return Color(hex: "CD7F32") // 🥉
        default: return Theme.sand
        }
    }
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            // التقييم
            if let r = place.googleRating {
                Text(String(format: "%.1f", r))
                    .font(Theme.detail().bold())
                    .foregroundStyle(Theme.gold500)
            }
            
            Spacer()
            
            // المعلومات
            VStack(alignment: .trailing, spacing: 2) {
                Text(place.nameAr)
                    .font(Theme.body(size: 15).bold())
                    .foregroundStyle(.appTextPrimary)
                    .lineLimit(1)
                
                HStack(spacing: Theme.spacingS) {
                    if let price = place.priceLevel {
                        Text(price)
                            .font(Theme.badge())
                            .foregroundStyle(Theme.gold500)
                    }
                    if let hood = place.neighborhood {
                        Text(hood)
                            .font(Theme.badge())
                            .foregroundStyle(.appTextSecondary)
                    }
                }
            }
            
            // الميدالية
            ZStack {
                Circle()
                    .fill(rank <= 3 ? medalColor.opacity(0.15) : Theme.green800)
                    .frame(width: 36, height: 36)
                Text("\(rank)")
                    .font(Theme.detail().bold())
                    .foregroundStyle(rank <= 3 ? medalColor : .appTextSecondary)
            }
        }
        .padding(Theme.spacingM)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
    }
}
