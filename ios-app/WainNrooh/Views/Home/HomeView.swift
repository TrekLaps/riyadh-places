// HomeView.swift
// الرئيسية — HS Super App Pattern
// Sections: Occasions → Trending → Top 10 → New → Categories

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var viewModel = HomeViewModel()
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Header + Search
                    headerSection
                    
                    // وش المناسبة؟ (SquareMeal)
                    occasionSection
                    
                    // 🔥 ترند (Yelp Hot & New)
                    if !viewModel.trendingPlaces.isEmpty {
                        trendingSection
                    }
                    
                    // 🏆 أفضل 10 بالحي (Dianping)
                    if let topPlaces = viewModel.topInNeighborhood, !topPlaces.isEmpty {
                        topNeighborhoodSection(topPlaces)
                    }
                    
                    // ✨ جديد
                    if !viewModel.newPlaces.isEmpty {
                        newSection
                    }
                    
                    // التصنيفات (HS Category Grid)
                    categoriesGrid
                    
                    Spacer(minLength: 80)
                }
            }
            .background(Color(.systemBackground))
            .refreshable {
                await viewModel.loadData(places: appState.places)
            }
            .task {
                await viewModel.loadData(places: appState.places)
            }
            .navigationBarHidden(true)
        }
    }
    
    // MARK: - Header
    
    private var headerSection: some View {
        VStack(alignment: .trailing, spacing: 12) {
            HStack {
                Button {} label: {
                    Image(systemName: "bell.fill")
                        .font(.title3)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                VStack(alignment: .trailing) {
                    Text("وين نروح؟ 🏙️")
                        .font(.title.bold())
                    Text("\(appState.places.count)+ مكان بالرياض")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            
            // Quick Search Bar
            NavigationLink {
                ExploreView()
            } label: {
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(.secondary)
                    Spacer()
                    Text("ابحث عن مكان، حي، أو نوع...")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                .padding(14)
                .background(Color(.secondarySystemBackground))
                .clipShape(RoundedRectangle(cornerRadius: 12))
            }
        }
        .padding(.horizontal)
        .padding(.top)
    }
    
    // MARK: - Occasions (SquareMeal)
    
    private var occasionSection: some View {
        VStack(alignment: .trailing, spacing: 8) {
            Text("وش المناسبة؟")
                .font(.headline)
                .padding(.horizontal)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 10) {
                    ForEach(Occasion.allCases) { occasion in
                        NavigationLink {
                            OccasionResultsView(occasion: occasion, places: appState.places)
                        } label: {
                            VStack(spacing: 6) {
                                Text(occasion.emoji)
                                    .font(.title)
                                Text(occasion.nameAr)
                                    .font(.caption)
                                    .fontWeight(.medium)
                            }
                            .frame(width: 80, height: 75)
                            .background(Color(.secondarySystemBackground))
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal)
            }
        }
    }
    
    // MARK: - Trending (Yelp)
    
    private var trendingSection: some View {
        VStack(alignment: .trailing, spacing: 8) {
            HStack {
                Text("عرض الكل →")
                    .font(.caption)
                    .foregroundStyle(Theme.primary)
                Spacer()
                Text("🔥 الأكثر شعبية")
                    .font(.headline)
            }
            .padding(.horizontal)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(viewModel.trendingPlaces.prefix(10)) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceCardCompact(place: place)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal)
            }
        }
    }
    
    // MARK: - Top 10 in Neighborhood (Dianping)
    
    private func topNeighborhoodSection(_ places: [Place]) -> some View {
        VStack(alignment: .trailing, spacing: 8) {
            HStack {
                Text("عرض الكل →")
                    .font(.caption)
                    .foregroundStyle(Theme.primary)
                Spacer()
                Text("🏆 أفضل 10 — \(viewModel.currentNeighborhood)")
                    .font(.headline)
            }
            .padding(.horizontal)
            
            LazyVStack(spacing: 8) {
                ForEach(Array(places.enumerated()), id: \.element.id) { index, place in
                    NavigationLink {
                        PlaceDetailView(place: place)
                    } label: {
                        TopPlaceRow(place: place, rank: index + 1)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal)
        }
    }
    
    // MARK: - New Places
    
    private var newSection: some View {
        VStack(alignment: .trailing, spacing: 8) {
            Text("✨ جديد بالرياض")
                .font(.headline)
                .padding(.horizontal)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(viewModel.newPlaces.prefix(8)) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceCardCompact(place: place)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal)
            }
        }
    }
    
    // MARK: - Categories Grid (HS Pattern)
    
    private var categoriesGrid: some View {
        VStack(alignment: .trailing, spacing: 8) {
            Text("التصنيفات")
                .font(.headline)
                .padding(.horizontal)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: 4), spacing: 10) {
                ForEach(viewModel.categories, id: \.id) { cat in
                    NavigationLink {
                        CategoryPlacesView(category: cat, places: appState.places)
                    } label: {
                        VStack(spacing: 6) {
                            Text(cat.emoji)
                                .font(.title2)
                            Text(cat.nameAr)
                                .font(.caption2)
                                .lineLimit(1)
                            Text("\(cat.count)")
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(Color(.secondarySystemBackground))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal)
        }
    }
}

// MARK: - Top Place Row (Dianping — Gold/Silver/Bronze)

struct TopPlaceRow: View {
    let place: Place
    let rank: Int
    
    var medalColor: Color {
        switch rank {
        case 1: return .yellow      // 🥇
        case 2: return .gray        // 🥈
        case 3: return Color(red: 0.8, green: 0.5, blue: 0.2) // 🥉
        default: return .clear
        }
    }
    
    var body: some View {
        HStack(spacing: 12) {
            // Rating
            if let r = place.googleRating {
                Text(String(format: "%.1f", r))
                    .font(.caption.bold())
                    .foregroundStyle(.yellow)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 2) {
                Text(place.nameAr)
                    .font(.subheadline.bold())
                    .lineLimit(1)
                HStack(spacing: 4) {
                    if let price = place.priceLevel {
                        Text(price).font(.caption2).foregroundStyle(.secondary)
                    }
                    if let hood = place.neighborhood {
                        Text(hood).font(.caption2).foregroundStyle(.secondary)
                    }
                }
            }
            
            // Rank medal
            ZStack {
                Circle()
                    .fill(rank <= 3 ? medalColor.opacity(0.2) : Color(.systemGray5))
                    .frame(width: 32, height: 32)
                Text("\(rank)")
                    .font(.caption.bold())
                    .foregroundStyle(rank <= 3 ? medalColor : .secondary)
            }
        }
        .padding(12)
        .background(Color(.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 10))
    }
}

// MARK: - Compact Place Card

struct PlaceCardCompact: View {
    let place: Place
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 6) {
            // Placeholder image
            RoundedRectangle(cornerRadius: 10)
                .fill(Color(.systemGray4))
                .frame(width: 140, height: 100)
                .overlay(
                    Text(place.categoryAr ?? place.category)
                        .font(.caption)
                        .foregroundStyle(.white)
                )
            
            Text(place.nameAr)
                .font(.caption.bold())
                .lineLimit(1)
            
            HStack(spacing: 4) {
                if let price = place.priceLevel {
                    Text(price).font(.caption2).foregroundStyle(.secondary)
                }
                Spacer()
                if let r = place.googleRating {
                    HStack(spacing: 2) {
                        Image(systemName: "star.fill").font(.system(size: 8)).foregroundStyle(.yellow)
                        Text(String(format: "%.1f", r)).font(.caption2)
                    }
                }
            }
        }
        .frame(width: 140)
    }
}
