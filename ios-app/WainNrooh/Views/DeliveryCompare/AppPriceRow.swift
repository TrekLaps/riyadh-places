// AppPriceRow.swift
// صف سعر تطبيق التوصيل — صف واحد في المقارنة

import SwiftUI

// MARK: - صف سعر التطبيق

/// صف واحد في مقارنة أسعار التوصيل — يعرض التطبيق وسعره ووقته
struct AppPriceRow: View {
    let price: DeliveryPrice
    var isCheapest: Bool = false
    var isFastest: Bool = false
    
    var body: some View {
        HStack(spacing: Theme.spacingMedium) {
            // زر الطلب
            Button {
                DeliveryService.shared.openDeliveryApp(price.app, deeplink: price.deeplinkUrl)
            } label: {
                Text("اطلب")
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 6)
                    .background(price.app.brandColor)
                    .clipShape(Capsule())
            }
            
            Spacer()
            
            // المعلومات
            VStack(alignment: .trailing, spacing: 4) {
                // السعر + الوقت
                HStack(spacing: Theme.spacingSmall) {
                    // الحد الأدنى
                    if let minOrder = price.formattedMinOrder {
                        Text(minOrder)
                            .font(Theme.footnoteFont())
                            .foregroundStyle(Color.appTextSecondary)
                    }
                    
                    // الوقت
                    if let time = price.formattedTime {
                        HStack(spacing: 2) {
                            Text(time)
                                .font(Theme.captionFont(size: 11))
                            Image(systemName: "clock")
                                .font(.system(size: 9))
                        }
                        .foregroundStyle(
                            isFastest ? Theme.accent : Color.appTextSecondary
                        )
                    }
                    
                    // سعر التوصيل
                    Text(price.formattedFee)
                        .font(.system(size: 16, weight: .bold, design: .rounded))
                        .foregroundStyle(
                            isCheapest ? Theme.success :
                            price.deliveryFee == 0 ? Theme.success :
                            Color.appTextPrimary
                        )
                }
                
                // شارات
                HStack(spacing: 4) {
                    if isCheapest {
                        badge(text: "الأرخص 🏷", color: Theme.success)
                    }
                    if isFastest {
                        badge(text: "الأسرع ⚡", color: Theme.accent)
                    }
                    if price.deliveryFee == 0 {
                        badge(text: "توصيل مجاني! 🎉", color: Theme.success)
                    }
                }
            }
            
            // شعار التطبيق
            AppLogo(app: price.app, size: .small, showName: false)
            
            // اسم التطبيق
            Text(price.app.nameAr)
                .font(Theme.bodyFont(size: 14))
                .foregroundStyle(Color.appTextPrimary)
                .frame(width: 70, alignment: .trailing)
        }
        .padding(Theme.paddingSmall + 4)
        .background(
            isCheapest
            ? Theme.success.opacity(0.05)
            : Color.appCardBackground
        )
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
        .overlay(
            RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall)
                .stroke(
                    isCheapest ? Theme.success.opacity(0.3) : Color.clear,
                    lineWidth: 1
                )
        )
    }
    
    /// شارة صغيرة
    private func badge(text: String, color: Color) -> some View {
        Text(text)
            .font(.system(size: 9, weight: .semibold))
            .foregroundStyle(color)
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(color.opacity(0.12))
            .clipShape(Capsule())
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 8) {
        AppPriceRow(
            price: DeliveryPrice(
                id: "1", placeId: "p1", app: .hungerstation,
                deliveryFee: 9, minOrder: 25, estimatedTimeMin: 30,
                isAvailable: true, deeplinkUrl: nil, scrapedAt: nil
            ),
            isCheapest: true
        )
        
        AppPriceRow(
            price: DeliveryPrice(
                id: "2", placeId: "p1", app: .jahez,
                deliveryFee: 12, minOrder: 20, estimatedTimeMin: 25,
                isAvailable: true, deeplinkUrl: nil, scrapedAt: nil
            ),
            isFastest: true
        )
        
        AppPriceRow(
            price: DeliveryPrice(
                id: "3", placeId: "p1", app: .keeta,
                deliveryFee: 0, minOrder: 30, estimatedTimeMin: 35,
                isAvailable: true, deeplinkUrl: nil, scrapedAt: nil
            )
        )
    }
    .padding()
    .background(Color.appBackground)
}
