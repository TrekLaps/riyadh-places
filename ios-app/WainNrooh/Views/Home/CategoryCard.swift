// CategoryCard.swift
// بطاقة التصنيف — أيقونة + اسم

import SwiftUI

// MARK: - بطاقة التصنيف

/// بطاقة تصنيف — تظهر في الشاشة الرئيسية
struct CategoryCard: View {
    let category: PlaceCategory
    var isSelected: Bool = false
    
    var body: some View {
        VStack(spacing: 8) {
            // الأيقونة
            ZStack {
                Circle()
                    .fill(
                        isSelected
                        ? category.color.gradient
                        : category.color.opacity(0.15).gradient
                    )
                    .frame(width: 60, height: 60)
                
                Text(category.emoji)
                    .font(.system(size: 28))
            }
            
            // الاسم
            Text(category.nameAr)
                .font(Theme.captionFont(size: 12))
                .foregroundStyle(
                    isSelected ? Theme.primary : Color.appTextPrimary
                )
                .lineLimit(1)
        }
        .frame(width: 76)
    }
}

// MARK: - Preview

#Preview {
    ScrollView(.horizontal) {
        HStack(spacing: 12) {
            ForEach(PlaceCategory.popular) { category in
                CategoryCard(category: category)
            }
        }
        .padding()
    }
    .background(Color.appBackground)
}
