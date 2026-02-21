// PlaceCard.swift
// بطاقة مكان — كبيرة ومفصلة (للهوم والسيرش)

import SwiftUI

struct PlaceCard: View {
    let place: Place
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 8) {
            // Image placeholder
            ZStack(alignment: .topLeading) {
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color(.systemGray4))
                    .frame(height: 150)
                
                // Category badge
                if let catAr = place.categoryAr {
                    Text(catAr)
                        .font(.caption2)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(.ultraThinMaterial)
                        .clipShape(Capsule())
                        .padding(8)
                }
                
                // Rating overlay
                if let r = place.googleRating {
                    VStack {
                        Spacer()
                        HStack {
                            HStack(spacing: 2) {
                                Image(systemName: "star.fill")
                                    .font(.caption2)
                                    .foregroundStyle(.yellow)
                                Text(String(format: "%.1f", r))
                                    .font(.caption.bold())
                                    .foregroundStyle(.white)
                            }
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(.black.opacity(0.6))
                            .clipShape(Capsule())
                            Spacer()
                        }
                        .padding(8)
                    }
                }
            }
            
            // Info
            VStack(alignment: .trailing, spacing: 4) {
                Text(place.nameAr)
                    .font(.subheadline.bold())
                    .lineLimit(1)
                
                HStack(spacing: 8) {
                    if let price = place.priceLevel {
                        Text(price)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    Spacer()
                    if let hood = place.neighborhood {
                        Label(hood, systemImage: "mappin")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }
            }
            .padding(.horizontal, 4)
        }
        .background(Color(.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// RatingView is in RatingView.swift
// PriceTag is in PriceTag.swift
