// ExploreView.swift
// استكشف — Jahez-style pill bar + HS progressive loading + occasion filters

import SwiftUI

struct ExploreView: View {
    @EnvironmentObject var appState: AppState
    @State private var searchText = ""
    @State private var selectedCategory: String?
    @State private var selectedOccasion: Occasion?
    @State private var displayedCount = 20  // HS Progressive loading
    
    var filteredPlaces: [Place] {
        var result = appState.places
        
        if !searchText.isEmpty {
            let q = searchText.lowercased()
            result = result.filter {
                $0.nameAr.contains(searchText) ||
                ($0.nameEn?.lowercased().contains(q) ?? false) ||
                ($0.descriptionAr?.contains(searchText) ?? false) ||
                ($0.neighborhood?.contains(searchText) ?? false) ||
                ($0.tags?.contains(where: { $0.contains(searchText) }) ?? false)
            }
        }
        
        if let cat = selectedCategory {
            result = result.filter { ($0.categoryEn ?? $0.category) == cat }
        }
        
        if let occ = selectedOccasion {
            result = result.filter { $0.occasions.contains(occ) }
        }
        
        return result.sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Search bar
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(.secondary)
                    TextField("ابحث عن مكان...", text: $searchText)
                        .textFieldStyle(.plain)
                    if !searchText.isEmpty {
                        Button { searchText = "" } label: {
                            Image(systemName: "xmark.circle.fill").foregroundStyle(.secondary)
                        }
                    }
                }
                .padding(12)
                .background(Color(.secondarySystemBackground))
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .padding(.horizontal)
                
                // Category Pill Bar (Jahez Pattern)
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        PillButton(title: "الكل", isSelected: selectedCategory == nil) {
                            selectedCategory = nil
                        }
                        ForEach(["restaurant", "cafe", "desserts", "entertainment", "shopping", "nature", "hotels"], id: \.self) { cat in
                            let names: [String: String] = [
                                "restaurant": "مطاعم", "cafe": "كافيهات", "desserts": "حلويات",
                                "entertainment": "ترفيه", "shopping": "تسوق",
                                "nature": "طبيعة", "hotels": "فنادق"
                            ]
                            PillButton(title: names[cat] ?? cat, isSelected: selectedCategory == cat) {
                                withAnimation(.snappy) {
                                    selectedCategory = selectedCategory == cat ? nil : cat
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 8)
                }
                
                // Occasion Quick Filter
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(Occasion.allCases) { occ in
                            Button {
                                withAnimation { selectedOccasion = selectedOccasion == occ ? nil : occ }
                            } label: {
                                HStack(spacing: 4) {
                                    Text(occ.emoji)
                                    Text(occ.nameAr).font(.caption)
                                }
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(selectedOccasion == occ ? Theme.primary.opacity(0.2) : Color(.systemGray6))
                                .clipShape(Capsule())
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal)
                }
                
                // Results count
                HStack {
                    Spacer()
                    Text("\(filteredPlaces.count) مكان")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .padding(.horizontal)
                        .padding(.top, 4)
                }
                
                // Results — Progressive Loading (HS Pattern)
                ScrollView {
                    LazyVStack(spacing: 10) {
                        ForEach(filteredPlaces.prefix(displayedCount)) { place in
                            NavigationLink {
                                PlaceDetailView(place: place)
                            } label: {
                                PlaceListRow(place: place)
                            }
                            .buttonStyle(.plain)
                            .onAppear {
                                // Load more when near end (HS infinite scroll)
                                if place.id == filteredPlaces.prefix(displayedCount).last?.id {
                                    displayedCount += 20
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                }
            }
            .navigationTitle("استكشف")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

// MARK: - Pill Button (Jahez Pattern)

struct PillButton: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(isSelected ? .bold : .regular)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(isSelected ? Theme.primary : Color(.systemGray6))
                .foregroundStyle(isSelected ? .white : .primary)
                .clipShape(Capsule())
        }
    }
}

// MARK: - Place List Row

struct PlaceListRow: View {
    let place: Place
    
    var body: some View {
        HStack(spacing: 12) {
            // Rating + Price
            VStack(spacing: 4) {
                if let r = place.googleRating {
                    HStack(spacing: 2) {
                        Image(systemName: "star.fill").font(.caption2).foregroundStyle(.yellow)
                        Text(String(format: "%.1f", r)).font(.caption.bold())
                    }
                }
                if let p = place.priceLevel {
                    Text(p).font(.caption2).foregroundStyle(.secondary)
                }
            }
            
            Spacer()
            
            // Details
            VStack(alignment: .trailing, spacing: 4) {
                Text(place.nameAr)
                    .font(.subheadline.bold())
                    .lineLimit(1)
                
                if let desc = place.descriptionAr {
                    Text(desc)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(2)
                }
                
                HStack(spacing: 8) {
                    if let hood = place.neighborhood {
                        Label(hood, systemImage: "mappin")
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                    }
                    if let cat = place.categoryAr {
                        Text(cat)
                            .font(.caption2)
                            .foregroundStyle(Theme.primary)
                    }
                }
            }
        }
        .padding(12)
        .background(Color(.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// MARK: - Occasion Results

struct OccasionResultsView: View {
    let occasion: Occasion
    let places: [Place]
    
    var filtered: [Place] {
        places.filter { $0.occasions.contains(occasion) }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
    }
    
    var body: some View {
        List(filtered) { place in
            NavigationLink {
                PlaceDetailView(place: place)
            } label: {
                PlaceListRow(place: place)
            }
        }
        .navigationTitle("\(occasion.emoji) \(occasion.nameAr)")
    }
}

// MARK: - Category Places

struct CategoryPlacesView: View {
    let category: CategoryInfo
    let places: [Place]
    
    var filtered: [Place] {
        places.filter { ($0.categoryEn ?? $0.category) == category.id }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
    }
    
    var body: some View {
        List(filtered) { place in
            NavigationLink {
                PlaceDetailView(place: place)
            } label: {
                PlaceListRow(place: place)
            }
        }
        .navigationTitle("\(category.emoji) \(category.nameAr)")
    }
}
