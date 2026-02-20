// FavoritesView.swift
// شاشة المفضلة — الأماكن المحفوظة

import SwiftUI

// MARK: - شاشة المفضلة

/// شاشة المفضلة — عرض الأماكن المحفوظة مع بحث وفلترة
struct FavoritesView: View {
    
    @StateObject private var viewModel = FavoritesViewModel()
    
    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isEmpty && !viewModel.isLoading {
                    // المفضلة فارغة
                    EmptyStateView(
                        icon: "heart.slash",
                        title: "ما عندك مفضلة",
                        message: "أضف أماكن للمفضلة عشان تلاقيها بسرعة",
                        actionTitle: "اكتشف أماكن"
                    )
                } else {
                    // قائمة المفضلة
                    favoritesContent
                }
            }
            .background(Color.appBackground)
            .navigationTitle("المفضلة ❤️")
            .navigationBarTitleDisplayMode(.large)
            .task {
                await viewModel.loadFavorites()
            }
            .refreshable {
                await viewModel.loadFavorites()
            }
        }
    }
    
    // MARK: - محتوى المفضلة
    
    private var favoritesContent: some View {
        VStack(spacing: 0) {
            // شريط البحث + الفلاتر
            VStack(spacing: Theme.spacingSmall) {
                // بحث
                HStack {
                    if !viewModel.searchText.isEmpty {
                        Button {
                            viewModel.searchText = ""
                        } label: {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundStyle(Color.appTextSecondary)
                        }
                    }
                    
                    TextField("ابحث في المفضلة...", text: $viewModel.searchText)
                        .font(Theme.bodyFont(size: 14))
                        .multilineTextAlignment(.trailing)
                    
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(Color.appTextSecondary)
                }
                .padding(Theme.paddingSmall + 2)
                .background(Color.appSecondaryBackground)
                .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
                .padding(.horizontal, Theme.paddingMedium)
                
                // فلاتر التصنيف
                if viewModel.availableCategories.count > 1 {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            // الكل
                            Button {
                                viewModel.filterCategory = nil
                            } label: {
                                TagChip(
                                    text: "الكل",
                                    color: Theme.primary,
                                    isSelected: viewModel.filterCategory == nil
                                )
                            }
                            .buttonStyle(.plain)
                            
                            ForEach(viewModel.availableCategories) { category in
                                Button {
                                    if viewModel.filterCategory == category {
                                        viewModel.filterCategory = nil
                                    } else {
                                        viewModel.filterCategory = category
                                    }
                                } label: {
                                    TagChip(
                                        text: category.nameAr,
                                        emoji: category.emoji,
                                        color: category.color,
                                        isSelected: viewModel.filterCategory == category
                                    )
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding(.horizontal, Theme.paddingMedium)
                    }
                }
            }
            .padding(.vertical, Theme.paddingSmall)
            
            // عدد النتائج
            HStack {
                Spacer()
                Text("\(viewModel.filteredFavorites.count) مكان")
                    .font(Theme.captionFont())
                    .foregroundStyle(Color.appTextSecondary)
            }
            .padding(.horizontal, Theme.paddingMedium)
            .padding(.bottom, 4)
            
            // القائمة
            if viewModel.isLoading {
                ProgressView("جاري التحميل...")
                    .padding(.top, 40)
            } else {
                ScrollView {
                    LazyVStack(spacing: Theme.spacingMedium) {
                        ForEach(viewModel.filteredFavorites) { place in
                            NavigationLink {
                                PlaceDetailView(place: place)
                            } label: {
                                FavoriteCard(
                                    place: place,
                                    onRemove: {
                                        withAnimation {
                                            viewModel.removeFavorite(place)
                                        }
                                    }
                                )
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal, Theme.paddingMedium)
                    .padding(.bottom, 80)
                }
            }
        }
    }
}
