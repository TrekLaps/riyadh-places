// PlaceCard.swift
// بطاقة المكان — التصميم الأساسي
// هوية ليالي الرياض — أخضر سعودي + glass

import SwiftUI

// MARK: - بطاقة كبيرة (الهوم + الترند)

struct PlaceCard: View {
    let place: Place
    var style: CardStyle = .large
    
    enum CardStyle {
        case large    // هوم — صورة كاملة
        case compact  // قوائم — صف أفقي
        case mini     // suggestions — صغيرة
    }
    
    var body: some View {
        switch style {
        case .large:
            largeCard
        case .compact:
            compactCard
        case .mini:
            miniCard
        }
    }
    
    // MARK: - بطاقة كبيرة
    
    private var largeCard: some View {
        VStack(alignment: .trailing, spacing: 0) {
            // الصورة
            ZStack(alignment: .bottom) {
                // خلفية الصورة (placeholder لين تجي الصور الحقيقية)
                ZStack {
                    Theme.green700
                    
                    // أيقونة الفئة كـ placeholder
                    Image(systemName: categoryIcon)
                        .font(.system(size: 40))
                        .foregroundStyle(Theme.green400.opacity(0.3))
                }
                .frame(height: 180)
                
                // تدرج للنص
                Theme.heroGradient
                    .frame(height: 180)
                
                // التقييم + الفئة فوق الصورة
                HStack {
                    // badge الفئة
                    if let catAr = place.categoryAr {
                        HStack(spacing: 4) {
                            Image(systemName: categoryIcon)
                                .font(.system(size: 10))
                            Text(catAr)
                        }
                        .font(Theme.badge())
                        .foregroundStyle(Theme.cream)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 5)
                        .background(.ultraThinMaterial)
                        .clipShape(Capsule())
                    }
                    
                    Spacer()
                    
                    // badge التقييم
                    if let rating = place.googleRating {
                        HStack(spacing: 3) {
                            Image(systemName: "star.fill")
                                .font(.system(size: 10))
                                .foregroundStyle(Theme.gold500)
                            Text(String(format: "%.1f", rating))
                                .font(Theme.badge(size: 12).bold())
                                .foregroundStyle(Theme.cream)
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 5)
                        .background(Color.black.opacity(0.5))
                        .clipShape(Capsule())
                    }
                }
                .padding(.horizontal, 12)
                .padding(.bottom, 12)
            }
            .clipShape(
                UnevenRoundedRectangle(
                    topLeadingRadius: Theme.radiusLarge,
                    topTrailingRadius: Theme.radiusLarge,
                    bottomLeadingRadius: 0,
                    bottomTrailingRadius: 0,
                    style: .continuous
                )
            )
            
            // المعلومات
            VStack(alignment: .trailing, spacing: Theme.spacingS) {
                // الاسم
                Text(place.nameAr)
                    .font(Theme.headline())
                    .foregroundStyle(.appTextPrimary)
                    .lineLimit(1)
                
                // الاسم الإنقليزي (لو موجود)
                if let nameEn = place.nameEn, !nameEn.isEmpty {
                    Text(nameEn)
                        .font(Theme.caption())
                        .foregroundStyle(.appTextSecondary)
                        .lineLimit(1)
                }
                
                // الحي + السعر
                HStack(spacing: Theme.spacingS) {
                    // السعر
                    if let priceLevel = place.priceLevel, !priceLevel.isEmpty {
                        Text(priceLevel)
                            .font(Theme.detail())
                            .foregroundStyle(Theme.gold500)
                    }
                    
                    Spacer()
                    
                    // الحي
                    if let hood = place.neighborhood, !hood.isEmpty {
                        HStack(spacing: 3) {
                            Image(systemName: "mappin.circle.fill")
                                .font(.system(size: 11))
                                .foregroundStyle(Theme.green400)
                            Text(hood)
                                .font(Theme.caption())
                                .foregroundStyle(.appTextSecondary)
                        }
                    }
                }
                
                // Tags
                if let tags = place.tags, !tags.isEmpty {
                    HStack(spacing: Theme.spacingXS) {
                        ForEach(Array(tags.prefix(3)), id: \.self) { tag in
                            Text(tag)
                                .font(Theme.badge())
                                .foregroundStyle(Theme.green300)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background(Theme.green400.opacity(0.1))
                                .clipShape(Capsule())
                        }
                        Spacer()
                    }
                }
            }
            .padding(Theme.spacingM)
        }
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
        .shadow(
            color: Theme.cardShadowColor,
            radius: Theme.cardShadowRadius,
            x: 0, y: Theme.cardShadowY
        )
    }
    
    // MARK: - بطاقة مضغوطة (للقوائم)
    
    private var compactCard: some View {
        HStack(spacing: Theme.spacingM) {
            // المعلومات (يمين — RTL)
            VStack(alignment: .trailing, spacing: Theme.spacingXS) {
                Text(place.nameAr)
                    .font(Theme.headline(size: 16))
                    .foregroundStyle(.appTextPrimary)
                    .lineLimit(1)
                
                if let nameEn = place.nameEn, !nameEn.isEmpty {
                    Text(nameEn)
                        .font(Theme.caption())
                        .foregroundStyle(.appTextSecondary)
                        .lineLimit(1)
                }
                
                HStack(spacing: Theme.spacingS) {
                    if let priceLevel = place.priceLevel {
                        Text(priceLevel)
                            .font(Theme.caption())
                            .foregroundStyle(Theme.gold500)
                    }
                    Spacer()
                    if let hood = place.neighborhood {
                        Text(hood)
                            .font(Theme.caption())
                            .foregroundStyle(.appTextSecondary)
                    }
                }
                
                // تقييم
                if let rating = place.googleRating {
                    HStack(spacing: 3) {
                        Image(systemName: "star.fill")
                            .font(.system(size: 10))
                            .foregroundStyle(Theme.gold500)
                        Text(String(format: "%.1f", rating))
                            .font(Theme.detail().bold())
                            .foregroundStyle(.appTextPrimary)
                    }
                }
            }
            
            // صورة مصغرة (يسار — RTL)
            ZStack {
                Theme.green700
                Image(systemName: categoryIcon)
                    .font(.system(size: 20))
                    .foregroundStyle(Theme.green400.opacity(0.4))
            }
            .frame(width: 80, height: 80)
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
        }
        .padding(Theme.spacingM)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
    }
    
    // MARK: - بطاقة صغيرة (suggestions)
    
    private var miniCard: some View {
        VStack(spacing: Theme.spacingXS) {
            ZStack {
                Theme.green700
                Image(systemName: categoryIcon)
                    .font(.system(size: 24))
                    .foregroundStyle(Theme.green400.opacity(0.3))
            }
            .frame(width: 100, height: 80)
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
            
            Text(place.nameAr)
                .font(Theme.caption().bold())
                .foregroundStyle(.appTextPrimary)
                .lineLimit(1)
            
            if let rating = place.googleRating {
                HStack(spacing: 2) {
                    Image(systemName: "star.fill")
                        .font(.system(size: 8))
                        .foregroundStyle(Theme.gold500)
                    Text(String(format: "%.1f", rating))
                        .font(Theme.badge())
                        .foregroundStyle(.appTextSecondary)
                }
            }
        }
        .frame(width: 100)
    }
    
    // MARK: - أيقونة الفئة
    
    private var categoryIcon: String {
        switch place.category {
        case "restaurants", "مطاعم": return "fork.knife"
        case "cafes", "كافيهات": return "cup.and.saucer.fill"
        case "entertainment", "ترفيه": return "sparkles"
        case "shopping", "تسوق": return "bag.fill"
        case "hotels", "فنادق": return "bed.double.fill"
        case "nature", "طبيعة": return "leaf.fill"
        case "desserts", "حلويات": return "birthday.cake.fill"
        case "chalets", "شاليهات": return "house.lodge.fill"
        case "malls", "مولات": return "building.2.fill"
        case "museums", "متاحف": return "building.columns.fill"
        case "events", "فعاليات": return "party.popper.fill"
        default: return "mappin.circle.fill"
        }
    }
}

// MARK: - Preview

#Preview("بطاقة كبيرة") {
    ScrollView {
        PlaceCard(place: .preview)
            .padding()
    }
    .background(Color.appBackground)
    .environment(\.layoutDirection, .rightToLeft)
}

#Preview("بطاقة مضغوطة") {
    PlaceCard(place: .preview, style: .compact)
        .padding()
        .background(Color.appBackground)
        .environment(\.layoutDirection, .rightToLeft)
}
