// TrendingCard.swift
// بطاقة المكان الشائع — بطاقة كبيرة بصورة

import SwiftUI

// MARK: - بطاقة المكان الشائع

/// بطاقة كبيرة لعرض المكان الشائع مع صورة
struct TrendingCard: View {
    let place: Place
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 0) {
            // الصورة
            ZStack(alignment: .topTrailing) {
                imageSection
                
                // شارة التصنيف
                HStack(spacing: 4) {
                    Text(place.category.nameAr)
                        .font(.system(size: 10, weight: .semibold))
                    Text(place.category.emoji)
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(.ultraThinMaterial)
                .clipShape(Capsule())
                .padding(8)
            }
            
            // المعلومات
            VStack(alignment: .trailing, spacing: 6) {
                // الاسم
                Text(place.name)
                    .font(Theme.headlineFont(size: 15))
                    .foregroundStyle(Color.appTextPrimary)
                    .lineLimit(1)
                
                // الحي
                if let neighborhood = place.neighborhood {
                    HStack(spacing: 4) {
                        Text(neighborhood)
                            .font(Theme.captionFont(size: 12))
                            .foregroundStyle(Color.appTextSecondary)
                        Image(systemName: "mappin.circle.fill")
                            .font(.system(size: 10))
                            .foregroundStyle(Theme.accent)
                    }
                }
                
                // التقييم + السعر
                HStack {
                    // السعر
                    if let priceRange = place.priceRange {
                        PriceTag(priceRange: priceRange, size: .small)
                    }
                    
                    Spacer()
                    
                    // التقييم
                    if let rating = place.rating {
                        CompactRating(rating: rating, count: place.ratingCount)
                    }
                }
            }
            .padding(Theme.paddingSmall + 4)
        }
        .frame(width: 200)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
        .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
    }
    
    // MARK: - قسم الصورة
    
    private var imageSection: some View {
        Group {
            if let imageUrl = place.coverImageUrl, let url = URL(string: imageUrl) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                    case .failure, .empty:
                        placeholderImage
                    @unknown default:
                        placeholderImage
                    }
                }
            } else {
                placeholderImage
            }
        }
        .frame(width: 200, height: 130)
        .clipped()
    }
    
    private var placeholderImage: some View {
        ZStack {
            LinearGradient(
                colors: [place.category.color.opacity(0.3), place.category.color.opacity(0.1)],
                startPoint: .topTrailing,
                endPoint: .bottomLeading
            )
            
            Text(place.category.emoji)
                .font(.system(size: 40))
        }
    }
}

// MARK: - Preview

#Preview {
    ScrollView(.horizontal) {
        HStack(spacing: 12) {
            TrendingCard(place: Place(
                id: "1", name: "كافيه المعمار", nameEn: "Al Mimar Cafe",
                category: .cafe, neighborhood: "العليا", neighborhoodEn: nil,
                description: nil, rating: 4.5, ratingCount: 128, priceRange: "$$",
                latitude: nil, longitude: nil, googleMapsUrl: nil, phone: nil,
                website: nil, instagram: nil, hours: nil, address: nil,
                coverImageUrl: nil, tags: nil, perfectFor: nil, features: nil,
                isVerified: nil, createdAt: nil, updatedAt: nil
            ))
            
            TrendingCard(place: Place(
                id: "2", name: "مطعم ناديا", nameEn: "Nadia Restaurant",
                category: .fineDining, neighborhood: "حطين", neighborhoodEn: nil,
                description: nil, rating: 4.8, ratingCount: 256, priceRange: "$$$",
                latitude: nil, longitude: nil, googleMapsUrl: nil, phone: nil,
                website: nil, instagram: nil, hours: nil, address: nil,
                coverImageUrl: nil, tags: nil, perfectFor: nil, features: nil,
                isVerified: nil, createdAt: nil, updatedAt: nil
            ))
        }
        .padding()
    }
    .background(Color.appBackground)
}
