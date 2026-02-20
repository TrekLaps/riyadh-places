// PlaceCard.swift
// بطاقة المكان — مكون قابل لإعادة الاستخدام

import SwiftUI

// MARK: - بطاقة المكان

/// بطاقة عرض المكان — تستخدم في القوائم والبحث والمفضلة
struct PlaceCard: View {
    let place: Place
    var showDistance: Bool = false
    var distance: String?
    var onFavoriteToggle: (() -> Void)?
    @State private var isFavorite: Bool = false
    
    var body: some View {
        HStack(spacing: Theme.spacingMedium) {
            // صورة المكان
            placeImage
            
            // معلومات المكان
            VStack(alignment: .trailing, spacing: 6) {
                // السطر الأول: الاسم + المفضلة
                HStack {
                    // زر المفضلة
                    Button {
                        isFavorite.toggle()
                        onFavoriteToggle?()
                    } label: {
                        Image(systemName: isFavorite ? "heart.fill" : "heart")
                            .foregroundStyle(isFavorite ? .red : .gray)
                            .font(.system(size: 18))
                    }
                    .buttonStyle(.plain)
                    
                    Spacer()
                    
                    // اسم المكان
                    Text(place.name)
                        .font(Theme.headlineFont(size: 16))
                        .foregroundStyle(Color.appTextPrimary)
                        .lineLimit(1)
                }
                
                // السطر الثاني: التصنيف + الحي
                HStack(spacing: 4) {
                    if let neighborhood = place.neighborhood {
                        Text(neighborhood)
                            .font(Theme.captionFont())
                            .foregroundStyle(Color.appTextSecondary)
                    }
                    
                    Text("•")
                        .foregroundStyle(Color.appTextSecondary)
                    
                    Text(place.category.emoji)
                    Text(place.category.nameAr)
                        .font(Theme.captionFont())
                        .foregroundStyle(Color.appTextSecondary)
                }
                
                // السطر الثالث: التقييم + السعر + المسافة
                HStack(spacing: Theme.spacingSmall) {
                    // المسافة
                    if showDistance, let distance {
                        Label(distance, systemImage: "location.fill")
                            .font(Theme.footnoteFont())
                            .foregroundStyle(Theme.accent)
                    }
                    
                    Spacer()
                    
                    // نطاق السعر
                    if let priceRange = place.priceRange {
                        PriceTag(priceRange: priceRange, size: .small)
                    }
                    
                    // التقييم
                    if let rating = place.rating {
                        RatingView(rating: rating, size: .small)
                    }
                }
                
                // التاقات (Perfect For)
                if let tags = place.perfectFor, !tags.isEmpty {
                    PerfectForTags(tags: Array(tags.prefix(3)), size: .small)
                }
            }
        }
        .padding(Theme.paddingMedium)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
        .shadow(
            color: .black.opacity(0.1),
            radius: 4, x: 0, y: 2
        )
        .onAppear {
            let favorites = UserDefaults.standard.stringArray(forKey: "favorites") ?? []
            isFavorite = favorites.contains(place.id)
        }
    }
    
    // MARK: - صورة المكان
    
    private var placeImage: some View {
        Group {
            if let imageUrl = place.coverImageUrl, let url = URL(string: imageUrl) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                    case .failure:
                        placeholderImage
                    case .empty:
                        ProgressView()
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                            .background(Color.appSecondaryBackground)
                    @unknown default:
                        placeholderImage
                    }
                }
            } else {
                placeholderImage
            }
        }
        .frame(width: 100, height: 100)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
    }
    
    private var placeholderImage: some View {
        ZStack {
            Color.appSecondaryBackground
            Text(place.category.emoji)
                .font(.system(size: 32))
        }
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 12) {
        PlaceCard(
            place: Place(
                id: "1",
                name: "كافيه المعمار",
                nameEn: "Al Mimar Cafe",
                category: .cafe,
                neighborhood: "العليا",
                neighborhoodEn: "Olaya",
                description: "كافيه متخصص في القهوة المختصة",
                rating: 4.5,
                ratingCount: 128,
                priceRange: "$$",
                latitude: 24.7136,
                longitude: 46.6753,
                googleMapsUrl: nil,
                phone: "+966512345678",
                website: nil,
                instagram: "@almimarcafe",
                hours: nil,
                address: "طريق الملك فهد",
                coverImageUrl: nil,
                tags: ["قهوة مختصة", "واي فاي"],
                perfectFor: ["عمل", "دراسة", "اجتماعات"],
                features: nil,
                isVerified: true,
                createdAt: nil,
                updatedAt: nil
            ),
            showDistance: true,
            distance: "1.2 كم"
        )
    }
    .padding()
    .background(Color.appBackground)
}
