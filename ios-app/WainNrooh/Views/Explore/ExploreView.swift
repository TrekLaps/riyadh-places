// ExploreView.swift
// استكشف — بحث + فلترة + Pill Bar
// هوية ليالي الرياض

import SwiftUI

struct ExploreView: View {
    @EnvironmentObject var appState: AppState
    @State private var searchText = ""
    @State private var selectedCategory: String? = nil
    @State private var selectedOccasion: String? = nil
    @State private var sortBy: SortOption = .rating
    
    enum SortOption: String, CaseIterable {
        case rating = "الأعلى تقييم"
        case nearest = "الأقرب"
        case newest = "الأحدث"
        case cheapest = "الأرخص"
    }
    
    private var filteredPlaces: [Place] {
        var results = appState.places
        
        // بحث
        if !searchText.isEmpty {
            results = results.filter { place in
                place.nameAr.localizedCaseInsensitiveContains(searchText) ||
                (place.nameEn?.localizedCaseInsensitiveContains(searchText) ?? false) ||
                (place.neighborhood?.localizedCaseInsensitiveContains(searchText) ?? false) ||
                (place.descriptionAr?.localizedCaseInsensitiveContains(searchText) ?? false)
            }
        }
        
        // فلترة بالفئة
        if let cat = selectedCategory {
            results = results.filter { $0.categoryAr == cat || $0.category == cat }
        }
        
        // فلترة بالمناسبة
        if let occ = selectedOccasion {
            results = results.filter { $0.perfectFor?.contains(occ) ?? false }
        }
        
        // ترتيب
        switch sortBy {
        case .rating:
            results.sort { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
        case .newest:
            results.sort { ($0.isNew ?? false) && !($1.isNew ?? false) }
        case .cheapest:
            results.sort { ($0.priceLevel ?? "$$$$").count < ($1.priceLevel ?? "$$$$").count }
        case .nearest:
            break // يحتاج موقع المستخدم
        }
        
        return results
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // البحث
                searchBar
                
                // Pill Bar — الفلاتر
                filterPills
                
                // النتائج
                ScrollView(showsIndicators: false) {
                    LazyVStack(spacing: Theme.spacingM) {
                        // عدد النتائج
                        HStack {
                            Spacer()
                            Text("\(filteredPlaces.count) مكان")
                                .font(Theme.caption())
                                .foregroundStyle(.appTextSecondary)
                        }
                        .padding(.horizontal, Theme.spacingL)
                        
                        ForEach(filteredPlaces.prefix(50)) { place in
                            NavigationLink {
                                PlaceDetailView(place: place)
                            } label: {
                                PlaceCard(place: place, style: .compact)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal, Theme.spacingL)
                    .padding(.bottom, 100)
                }
            }
            .background(Color.appBackground)
            .navigationBarHidden(true)
        }
    }
    
    // MARK: - شريط البحث
    
    private var searchBar: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: "magnifyingglass")
                .foregroundStyle(Theme.green400)
            
            TextField("ابحث عن مكان، حي، أو نوع...", text: $searchText)
                .font(Theme.body())
                .foregroundStyle(.appTextPrimary)
                .multilineTextAlignment(.trailing)
            
            if !searchText.isEmpty {
                Button {
                    searchText = ""
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(.appTextSecondary)
                }
            }
        }
        .padding(Theme.spacingL)
        .background(Color.appCardBackground)
        .clipShape(Capsule())
        .padding(.horizontal, Theme.spacingL)
        .padding(.top, Theme.spacingM)
    }
    
    // MARK: - Pill Bar
    
    private var filterPills: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: Theme.spacingS) {
                // ترتيب
                Menu {
                    ForEach(SortOption.allCases, id: \.self) { option in
                        Button(option.rawValue) {
                            sortBy = option
                        }
                    }
                } label: {
                    HStack(spacing: 4) {
                        Image(systemName: "arrow.up.arrow.down")
                            .font(.system(size: 11))
                        Text(sortBy.rawValue)
                    }
                    .wainGlassPill()
                }
                
                Divider()
                    .frame(height: 20)
                    .background(.appDivider)
                
                // الفئات
                ForEach(categoryPills, id: \.self) { cat in
                    Button {
                        withAnimation(Theme.animFast) {
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
                                    ? AnyShapeStyle(Theme.primaryGradient)
                                    : AnyShapeStyle(.ultraThinMaterial)
                            )
                            .clipShape(Capsule())
                    }
                }
            }
            .padding(.horizontal, Theme.spacingL)
            .padding(.vertical, Theme.spacingM)
        }
    }
    
    private var categoryPills: [String] {
        ["مطاعم", "كافيهات", "ترفيه", "تسوق", "حلويات", "فنادق", "طبيعة", "شاليهات", "مولات", "متاحف"]
    }
}
