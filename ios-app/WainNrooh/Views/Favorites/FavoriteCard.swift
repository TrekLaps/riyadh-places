// FavoriteCard.swift
// بطاقة المفضلة — مع زر الحذف

import SwiftUI

// MARK: - بطاقة المفضلة

/// بطاقة مكان مفضل — مع زر السحب للحذف
struct FavoriteCard: View {
    let place: Place
    var onRemove: (() -> Void)?
    
    var body: some View {
        HStack(spacing: Theme.spacingMedium) {
            // صورة المكان
            placeImage
            
            // المعلومات
            VStack(alignment: .trailing, spacing: 6) {
                // الاسم
                Text(place.name)
                    .font(Theme.headlineFont(size: 16))
                    .foregroundStyle(Color.appTextPrimary)
                    .lineLimit(1)
                
                // التصنيف + الحي
                HStack(spacing: 4) {
                    if let neighborhood = place.neighborhood {
                        Text(neighborhood)
                            .font(Theme.captionFont(size: 12))
                            .foregroundStyle(Color.appTextSecondary)
                    }
                    Text("•")
                        .foregroundStyle(Color.appTextSecondary)
                    Text(place.category.emoji + " " + place.category.nameAr)
                        .font(Theme.captionFont(size: 12))
                        .foregroundStyle(place.category.color)
                }
                
                // التقييم + السعر
                HStack {
                    if let priceRange = place.priceRange {
                        PriceTag(priceRange: priceRange, size: .small)
                    }
                    
                    Spacer()
                    
                    if let rating = place.rating {
                        CompactRating(rating: rating, count: place.ratingCount)
                    }
                }
            }
            .frame(maxWidth: .infinity)
        }
        .padding(Theme.paddingSmall + 4)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
        .shadow(color: .black.opacity(0.08), radius: 3, x: 0, y: 1)
        .swipeActions(edge: .leading, allowsFullSwipe: true) {
            Button(role: .destructive) {
                onRemove?()
            } label: {
                Label("حذف", systemImage: "trash")
            }
        }
        .contextMenu {
            Button {
                onRemove?()
            } label: {
                Label("إزالة من المفضلة", systemImage: "heart.slash")
            }
            
            if let phone = place.phone, let url = URL(string: "tel:\(phone)") {
                Link(destination: url) {
                    Label("اتصل", systemImage: "phone")
                }
            }
            
            if let googleUrl = place.googleMapsUrl, let url = URL(string: googleUrl) {
                Link(destination: url) {
                    Label("افتح في الخرائط", systemImage: "map")
                }
            }
        }
    }
    
    // MARK: - صورة المكان
    
    private var placeImage: some View {
        Group {
            if let imageUrl = place.coverImageUrl, let url = URL(string: imageUrl) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .success(let image):
                        image.resizable().aspectRatio(contentMode: .fill)
                    default:
                        placeholder
                    }
                }
            } else {
                placeholder
            }
        }
        .frame(width: 80, height: 80)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
    }
    
    private var placeholder: some View {
        ZStack {
            place.category.color.opacity(0.15)
            Text(place.category.emoji)
                .font(.system(size: 28))
        }
    }
}
