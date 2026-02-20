// FilterView.swift
// شاشة الفلاتر — ميزانية / تصنيف / مسافة

import SwiftUI

// MARK: - شاشة الفلاتر

/// شاشة الفلاتر المتقدمة — تصنيف + سعر + تقييم + ترتيب
struct FilterView: View {
    @ObservedObject var viewModel: SearchViewModel
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: Theme.spacingLarge + 8) {
                    // التصنيف
                    categoryFilter
                    
                    Divider()
                    
                    // نطاق السعر
                    priceFilter
                    
                    Divider()
                    
                    // التقييم
                    ratingFilter
                    
                    Divider()
                    
                    // الحي
                    neighborhoodFilter
                    
                    Divider()
                    
                    // الترتيب
                    sortFilter
                    
                    Spacer(minLength: 100)
                }
                .padding(Theme.paddingMedium)
            }
            .background(Color.appBackground)
            .navigationTitle("الفلاتر")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("تم") {
                        dismiss()
                        Task { await viewModel.performSearch() }
                    }
                    .foregroundStyle(Theme.primary)
                    .fontWeight(.semibold)
                }
                
                ToolbarItem(placement: .topBarLeading) {
                    Button("مسح الكل") {
                        viewModel.clearFilters()
                    }
                    .foregroundStyle(Theme.error)
                    .font(Theme.captionFont())
                }
            }
        }
    }
    
    // MARK: - فلتر التصنيف
    
    private var categoryFilter: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            Text("التصنيف")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
            
            FlowLayout(spacing: 8) {
                ForEach(PlaceCategory.allCases) { category in
                    Button {
                        if viewModel.selectedCategory == category {
                            viewModel.selectedCategory = nil
                        } else {
                            viewModel.selectedCategory = category
                        }
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
        }
    }
    
    // MARK: - فلتر السعر
    
    private var priceFilter: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            Text("نطاق السعر")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
            
            HStack(spacing: 12) {
                ForEach(["$", "$$", "$$$", "$$$$"], id: \.self) { range in
                    Button {
                        if viewModel.selectedPriceRange == range {
                            viewModel.selectedPriceRange = nil
                        } else {
                            viewModel.selectedPriceRange = range
                        }
                    } label: {
                        VStack(spacing: 4) {
                            Text(range)
                                .font(.system(size: 16, weight: .bold, design: .monospaced))
                            Text(priceName(range))
                                .font(.system(size: 10))
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .foregroundStyle(
                            viewModel.selectedPriceRange == range
                            ? .white
                            : Color.priceColor(for: range)
                        )
                        .background(
                            viewModel.selectedPriceRange == range
                            ? Color.priceColor(for: range)
                            : Color.priceColor(for: range).opacity(0.12)
                        )
                        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
                    }
                    .buttonStyle(.plain)
                }
            }
        }
    }
    
    // MARK: - فلتر التقييم
    
    private var ratingFilter: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            HStack {
                if let rating = viewModel.minRating {
                    Text("\(rating, specifier: "%.1f")+ ⭐")
                        .font(Theme.captionFont())
                        .foregroundStyle(Theme.primary)
                }
                Spacer()
                Text("الحد الأدنى للتقييم")
                    .font(Theme.headlineFont(size: 16))
                    .foregroundStyle(Color.appTextPrimary)
            }
            
            HStack(spacing: 12) {
                ForEach([3.0, 3.5, 4.0, 4.5], id: \.self) { rating in
                    Button {
                        if viewModel.minRating == rating {
                            viewModel.minRating = nil
                        } else {
                            viewModel.minRating = rating
                        }
                    } label: {
                        HStack(spacing: 2) {
                            Image(systemName: "star.fill")
                                .font(.system(size: 10))
                            Text("\(rating, specifier: "%.1f")+")
                                .font(.system(size: 13, weight: .semibold))
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .foregroundStyle(
                            viewModel.minRating == rating ? .white : Color.ratingColor(for: rating)
                        )
                        .background(
                            viewModel.minRating == rating
                            ? Color.ratingColor(for: rating)
                            : Color.ratingColor(for: rating).opacity(0.12)
                        )
                        .clipShape(Capsule())
                    }
                    .buttonStyle(.plain)
                }
            }
        }
    }
    
    // MARK: - فلتر الحي
    
    private var neighborhoodFilter: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            Text("الحي")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
            
            FlowLayout(spacing: 8) {
                ForEach(Neighborhood.mainNeighborhoods) { hood in
                    Button {
                        if viewModel.selectedNeighborhood == hood.id {
                            viewModel.selectedNeighborhood = nil
                        } else {
                            viewModel.selectedNeighborhood = hood.id
                        }
                    } label: {
                        TagChip(
                            text: hood.nameAr,
                            color: Theme.accent,
                            isSelected: viewModel.selectedNeighborhood == hood.id
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
        }
    }
    
    // MARK: - فلتر الترتيب
    
    private var sortFilter: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            Text("الترتيب")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
            
            ForEach(PlaceSortOption.allCases) { option in
                Button {
                    viewModel.sortOption = option
                } label: {
                    HStack {
                        if viewModel.sortOption == option {
                            Image(systemName: "checkmark")
                                .foregroundStyle(Theme.primary)
                        }
                        
                        Spacer()
                        
                        Text(option.nameAr)
                            .font(Theme.bodyFont(size: 15))
                            .foregroundStyle(
                                viewModel.sortOption == option
                                ? Theme.primary
                                : Color.appTextPrimary
                            )
                        
                        Image(systemName: option.icon)
                            .font(.system(size: 14))
                            .foregroundStyle(Color.appTextSecondary)
                    }
                    .padding(.vertical, 8)
                }
                .buttonStyle(.plain)
            }
        }
    }
    
    // MARK: - دوال مساعدة
    
    private func priceName(_ range: String) -> String {
        switch range {
        case "$": return "رخيص"
        case "$$": return "متوسط"
        case "$$$": return "غالي"
        case "$$$$": return "فاخر"
        default: return ""
        }
    }
}
