// SearchView.swift
// شاشة البحث — بحث AI بالعربي مع فلاتر

import SwiftUI

// MARK: - شاشة البحث

/// شاشة البحث الذكي — بحث بالعربي السعودي مع فلاتر متقدمة
struct SearchView: View {
    
    @StateObject private var viewModel = SearchViewModel()
    @State private var showFilters = false
    @FocusState private var isSearchFocused: Bool
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // شريط البحث
                SearchBar(
                    text: $viewModel.searchText,
                    isFocused: $isSearchFocused,
                    onSubmit: {
                        Task { await viewModel.performSearch() }
                    },
                    onClear: {
                        viewModel.clearSearch()
                    }
                )
                .padding(.horizontal, Theme.paddingMedium)
                .padding(.top, Theme.paddingSmall)
                
                // شريط الفلاتر
                filtersBar
                
                // المحتوى
                ScrollView {
                    if viewModel.hasSearched {
                        // نتائج البحث
                        searchResultsContent
                    } else if !viewModel.suggestions.isEmpty {
                        // اقتراحات البحث
                        suggestionsContent
                    } else {
                        // الشاشة الافتراضية
                        defaultContent
                    }
                }
            }
            .background(Color.appBackground)
            .navigationBarHidden(true)
            .sheet(isPresented: $showFilters) {
                FilterView(viewModel: viewModel)
            }
        }
    }
    
    // MARK: - شريط الفلاتر
    
    private var filtersBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                // زر الفلاتر
                Button {
                    showFilters = true
                } label: {
                    HStack(spacing: 4) {
                        Image(systemName: "slider.horizontal.3")
                        Text("فلاتر")
                        if viewModel.activeFilterCount > 0 {
                            Text("\(viewModel.activeFilterCount)")
                                .font(.system(size: 10, weight: .bold))
                                .padding(4)
                                .background(Theme.primary)
                                .foregroundStyle(.white)
                                .clipShape(Circle())
                        }
                    }
                    .font(Theme.captionFont())
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(viewModel.hasActiveFilters ? Theme.primary.opacity(0.15) : Color.appSecondaryBackground)
                    .foregroundStyle(viewModel.hasActiveFilters ? Theme.primary : Color.appTextPrimary)
                    .clipShape(Capsule())
                }
                
                // فلاتر سريعة (التصنيفات)
                ForEach(PlaceCategory.popular) { category in
                    Button {
                        if viewModel.selectedCategory == category {
                            viewModel.selectedCategory = nil
                        } else {
                            viewModel.selectedCategory = category
                        }
                        Task { await viewModel.performSearch() }
                    } label: {
                        TagChip(
                            text: category.nameAr,
                            emoji: category.emoji,
                            color: category.color,
                            isSelected: viewModel.selectedCategory == category
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, Theme.paddingMedium)
            .padding(.vertical, Theme.paddingSmall)
        }
    }
    
    // MARK: - نتائج البحث
    
    private var searchResultsContent: some View {
        VStack(spacing: Theme.spacingMedium) {
            if viewModel.isSearching {
                // تحميل
                ForEach(0..<5, id: \.self) { _ in
                    PlaceCardPlaceholder()
                }
            } else if viewModel.searchResults.isEmpty {
                // لا توجد نتائج
                EmptyStateView(
                    icon: "magnifyingglass",
                    title: "ما لقينا نتائج",
                    message: "جرب كلمات بحث مختلفة أو غيّر الفلاتر",
                    actionTitle: "مسح الفلاتر"
                ) {
                    viewModel.clearFilters()
                }
            } else {
                // عدد النتائج
                HStack {
                    Spacer()
                    Text("\(viewModel.searchResults.count) نتيجة")
                        .font(Theme.captionFont())
                        .foregroundStyle(Color.appTextSecondary)
                }
                .padding(.horizontal, Theme.paddingMedium)
                
                // قائمة النتائج
                LazyVStack(spacing: Theme.spacingMedium) {
                    ForEach(viewModel.searchResults) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceCard(place: place)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, Theme.paddingMedium)
            }
            
            Spacer(minLength: 80)
        }
    }
    
    // MARK: - اقتراحات البحث
    
    private var suggestionsContent: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingSmall) {
            ForEach(viewModel.suggestions) { suggestion in
                Button {
                    viewModel.selectSuggestion(suggestion)
                } label: {
                    HStack {
                        Image(systemName: "chevron.left")
                            .font(.system(size: 10))
                            .foregroundStyle(Color.appTextSecondary)
                        
                        Spacer()
                        
                        Text(suggestion.text)
                            .font(Theme.bodyFont(size: 15))
                            .foregroundStyle(Color.appTextPrimary)
                        
                        Image(systemName: suggestion.icon)
                            .font(.system(size: 14))
                            .foregroundStyle(Theme.primary)
                    }
                    .padding(.horizontal, Theme.paddingMedium)
                    .padding(.vertical, Theme.paddingSmall + 4)
                }
            }
        }
        .padding(.top, Theme.paddingSmall)
    }
    
    // MARK: - المحتوى الافتراضي
    
    private var defaultContent: some View {
        VStack(spacing: Theme.spacingLarge + 8) {
            // البحث الأخير
            if !viewModel.recentSearches.isEmpty {
                VStack(alignment: .trailing, spacing: Theme.spacingSmall) {
                    HStack {
                        Button("مسح") {
                            viewModel.clearRecentSearches()
                        }
                        .font(Theme.captionFont())
                        .foregroundStyle(Theme.error)
                        
                        Spacer()
                        
                        Text("بحث سابق")
                            .font(Theme.headlineFont(size: 16))
                            .foregroundStyle(Color.appTextPrimary)
                    }
                    .padding(.horizontal, Theme.paddingMedium)
                    
                    ForEach(viewModel.recentSearches, id: \.self) { search in
                        Button {
                            viewModel.searchFromRecent(search)
                        } label: {
                            HStack {
                                Spacer()
                                Text(search)
                                    .font(Theme.bodyFont(size: 14))
                                    .foregroundStyle(Color.appTextPrimary)
                                Image(systemName: "clock.fill")
                                    .font(.system(size: 12))
                                    .foregroundStyle(Color.appTextSecondary)
                            }
                            .padding(.horizontal, Theme.paddingMedium)
                            .padding(.vertical, 6)
                        }
                    }
                }
            }
            
            // البحث الشائع
            VStack(alignment: .trailing, spacing: Theme.spacingSmall) {
                Text("الأكثر بحثاً 🔥")
                    .font(Theme.headlineFont(size: 16))
                    .foregroundStyle(Color.appTextPrimary)
                    .padding(.horizontal, Theme.paddingMedium)
                
                FlowLayout(spacing: 8) {
                    ForEach(viewModel.popularSearches, id: \.self) { search in
                        Button {
                            viewModel.searchFromRecent(search)
                        } label: {
                            TagChip(text: search, color: Theme.accent)
                        }
                    }
                }
                .padding(.horizontal, Theme.paddingMedium)
            }
            
            Spacer(minLength: 100)
        }
        .padding(.top, Theme.paddingMedium)
    }
}

// MARK: - Placeholder بطاقة التحميل

/// بطاقة placeholder أثناء التحميل
struct PlaceCardPlaceholder: View {
    var body: some View {
        HStack(spacing: Theme.spacingMedium) {
            RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall)
                .fill(Color.appSecondaryBackground)
                .frame(width: 100, height: 100)
            
            VStack(alignment: .trailing, spacing: 8) {
                RoundedRectangle(cornerRadius: 4)
                    .fill(Color.appSecondaryBackground)
                    .frame(height: 16)
                
                RoundedRectangle(cornerRadius: 4)
                    .fill(Color.appSecondaryBackground)
                    .frame(width: 120, height: 12)
                
                RoundedRectangle(cornerRadius: 4)
                    .fill(Color.appSecondaryBackground)
                    .frame(width: 80, height: 12)
            }
        }
        .padding(Theme.paddingMedium)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
        .shimmer()
        .padding(.horizontal, Theme.paddingMedium)
    }
}
