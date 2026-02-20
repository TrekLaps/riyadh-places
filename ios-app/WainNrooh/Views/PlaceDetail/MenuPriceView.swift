// MenuPriceView.swift
// عرض أسعار المنيو — أسعار حقيقية بالريال

import SwiftUI

// MARK: - عرض أسعار المنيو

/// عرض أسعار المنيو مجمّعة حسب الفئة
struct MenuPriceView: View {
    let categories: [MenuCategory]
    @State private var expandedCategory: String?
    
    var body: some View {
        VStack(spacing: Theme.spacingMedium) {
            ForEach(categories) { category in
                menuCategorySection(category)
            }
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
    
    // MARK: - قسم فئة المنيو
    
    private func menuCategorySection(_ category: MenuCategory) -> some View {
        VStack(spacing: 0) {
            // عنوان الفئة (قابل للطي)
            Button {
                withAnimation(Theme.animationNormal) {
                    if expandedCategory == category.id {
                        expandedCategory = nil
                    } else {
                        expandedCategory = category.id
                    }
                }
            } label: {
                HStack {
                    Image(systemName: expandedCategory == category.id ? "chevron.up" : "chevron.down")
                        .font(.system(size: 12))
                        .foregroundStyle(Color.appTextSecondary)
                    
                    Text(category.formattedAveragePrice)
                        .font(Theme.captionFont(size: 11))
                        .foregroundStyle(Color.appTextSecondary)
                    
                    Spacer()
                    
                    Text(category.nameAr)
                        .font(Theme.headlineFont(size: 15))
                        .foregroundStyle(Color.appTextPrimary)
                    
                    Text("(\(category.items.count))")
                        .font(Theme.captionFont(size: 11))
                        .foregroundStyle(Color.appTextSecondary)
                }
                .padding(.vertical, 10)
                .padding(.horizontal, Theme.paddingSmall)
            }
            .buttonStyle(.plain)
            
            // عناصر الفئة
            if expandedCategory == category.id {
                VStack(spacing: 0) {
                    ForEach(category.items) { item in
                        menuItemRow(item)
                        
                        if item.id != category.items.last?.id {
                            Divider()
                                .padding(.horizontal, Theme.paddingSmall)
                        }
                    }
                }
                .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
    }
    
    // MARK: - صف عنصر المنيو
    
    private func menuItemRow(_ item: MenuPrice) -> some View {
        HStack(alignment: .top) {
            // الأسعار
            VStack(alignment: .leading, spacing: 2) {
                if item.sizes.count == 1 {
                    SARPrice(amount: item.sizes[0].price, size: .small)
                } else {
                    ForEach(item.sizes) { size in
                        HStack(spacing: 4) {
                            Text("\(Int(size.price)) ر.س")
                                .font(.system(size: 13, weight: .semibold))
                                .foregroundStyle(Color.appTextPrimary)
                            
                            if let sizeLabel = size.size {
                                Text(size.formattedSize)
                                    .font(.system(size: 10))
                                    .foregroundStyle(Color.appTextSecondary)
                                    .padding(.horizontal, 4)
                                    .padding(.vertical, 2)
                                    .background(Color.appSecondaryBackground)
                                    .clipShape(Capsule())
                            }
                        }
                    }
                }
            }
            
            Spacer()
            
            // اسم العنصر
            VStack(alignment: .trailing, spacing: 2) {
                Text(item.nameAr)
                    .font(Theme.bodyFont(size: 14))
                    .foregroundStyle(Color.appTextPrimary)
                    .multilineTextAlignment(.trailing)
                
                if let nameEn = item.nameEn {
                    Text(nameEn)
                        .font(Theme.captionFont(size: 11))
                        .foregroundStyle(Color.appTextSecondary)
                }
            }
        }
        .padding(.horizontal, Theme.paddingSmall)
        .padding(.vertical, 8)
    }
}

// MARK: - Preview

#Preview {
    MenuPriceView(categories: [
        MenuCategory(
            id: "coffee",
            nameAr: "قهوة",
            nameEn: "Coffee",
            items: [
                MenuPrice(id: "1", placeId: "p1", categoryAr: "قهوة", categoryEn: nil,
                         nameAr: "لاتيه", nameEn: "Latte", descriptionAr: nil,
                         sizes: [
                            MenuItemSize(size: "S", price: 18),
                            MenuItemSize(size: "M", price: 22),
                            MenuItemSize(size: "L", price: 26)
                         ],
                         imageUrl: nil, isAvailable: true, lastUpdated: nil),
                MenuPrice(id: "2", placeId: "p1", categoryAr: "قهوة", categoryEn: nil,
                         nameAr: "أمريكانو", nameEn: "Americano", descriptionAr: nil,
                         sizes: [MenuItemSize(size: nil, price: 15)],
                         imageUrl: nil, isAvailable: true, lastUpdated: nil),
            ]
        )
    ])
    .padding()
    .background(Color.appBackground)
}
