// DeliveryCompareView.swift
// مقارنة أسعار التوصيل — 8+ تطبيقات

import SwiftUI

// MARK: - عرض مقارنة التوصيل

/// مقارنة أسعار التوصيل لمكان واحد — يعرض كل التطبيقات مرتبة بالسعر
struct DeliveryCompareView: View {
    let comparison: DeliveryComparison
    @State private var sortBy: DeliverySortOption = .price
    
    var body: some View {
        VStack(spacing: Theme.spacingMedium) {
            // ملخص المقارنة
            summaryCard
            
            // خيارات الترتيب
            sortOptions
            
            // قائمة الأسعار
            VStack(spacing: 8) {
                ForEach(sortedPrices) { price in
                    AppPriceRow(
                        price: price,
                        isCheapest: price.id == comparison.cheapest?.id,
                        isFastest: price.id == comparison.fastest?.id
                    )
                }
            }
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
    
    // MARK: - ملخص المقارنة
    
    private var summaryCard: some View {
        HStack {
            // الأسرع
            if let fastest = comparison.fastest {
                VStack(spacing: 4) {
                    Text("⚡ الأسرع")
                        .font(Theme.captionFont(size: 10))
                        .foregroundStyle(Color.appTextSecondary)
                    Text(fastest.app.nameAr)
                        .font(Theme.captionFont(size: 12))
                        .foregroundStyle(Theme.accent)
                    Text(fastest.formattedTime ?? "")
                        .font(Theme.footnoteFont())
                        .foregroundStyle(Color.appTextSecondary)
                }
                .frame(maxWidth: .infinity)
            }
            
            Divider().frame(height: 40)
            
            // التوفير
            if let savings = comparison.savingsText {
                VStack(spacing: 4) {
                    Text("💰 توفير")
                        .font(Theme.captionFont(size: 10))
                        .foregroundStyle(Color.appTextSecondary)
                    Text(savings)
                        .font(Theme.headlineFont(size: 14))
                        .foregroundStyle(Theme.success)
                }
                .frame(maxWidth: .infinity)
            }
            
            Divider().frame(height: 40)
            
            // الأرخص
            if let cheapest = comparison.cheapest {
                VStack(spacing: 4) {
                    Text("🏷 الأرخص")
                        .font(Theme.captionFont(size: 10))
                        .foregroundStyle(Color.appTextSecondary)
                    Text(cheapest.app.nameAr)
                        .font(Theme.captionFont(size: 12))
                        .foregroundStyle(Theme.success)
                    Text(cheapest.formattedFee)
                        .font(Theme.headlineFont(size: 14))
                        .foregroundStyle(Theme.success)
                }
                .frame(maxWidth: .infinity)
            }
        }
        .padding(Theme.paddingMedium)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
    }
    
    // MARK: - خيارات الترتيب
    
    private var sortOptions: some View {
        HStack(spacing: 8) {
            ForEach(DeliverySortOption.allCases) { option in
                Button {
                    withAnimation(Theme.animationFast) {
                        sortBy = option
                    }
                } label: {
                    HStack(spacing: 4) {
                        Image(systemName: option.icon)
                            .font(.system(size: 10))
                        Text(option.nameAr)
                            .font(Theme.captionFont(size: 11))
                    }
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .foregroundStyle(sortBy == option ? .white : Color.appTextPrimary)
                    .background(sortBy == option ? Theme.primary : Color.appSecondaryBackground)
                    .clipShape(Capsule())
                }
                .buttonStyle(.plain)
            }
            
            Spacer()
        }
    }
    
    // MARK: - الأسعار المرتبة
    
    private var sortedPrices: [DeliveryPrice] {
        let available = comparison.prices.filter { $0.isAvailable }
        switch sortBy {
        case .price: return available.sorted { $0.deliveryFee < $1.deliveryFee }
        case .time: return available.sorted { ($0.estimatedTimeMin ?? 999) < ($1.estimatedTimeMin ?? 999) }
        case .minOrder: return available.sorted { ($0.minOrder ?? 0) < ($1.minOrder ?? 0) }
        }
    }
}
