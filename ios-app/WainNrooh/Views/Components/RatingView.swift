// RatingView.swift
// عرض التقييم — نجوم ذهبية
// هوية ليالي الرياض

import SwiftUI

struct RatingView: View {
    let rating: Double
    var maxRating: Int = 5
    var size: CGFloat = 14
    
    var body: some View {
        HStack(spacing: 2) {
            ForEach(1...maxRating, id: \.self) { star in
                Image(systemName: starIcon(for: star))
                    .font(.system(size: size))
                    .foregroundStyle(starColor(for: star))
            }
        }
    }
    
    private func starIcon(for star: Int) -> String {
        let value = Double(star)
        if rating >= value {
            return "star.fill"
        } else if rating >= value - 0.5 {
            return "star.leadinghalf.filled"
        } else {
            return "star"
        }
    }
    
    private func starColor(for star: Int) -> Color {
        Double(star) <= rating + 0.5 ? Theme.starFilled : Theme.starEmpty
    }
}

// MARK: - Rating Badge (رقم + نجمة)

struct RatingBadge: View {
    let rating: Double
    var style: BadgeStyle = .standard
    
    enum BadgeStyle {
        case standard   // خلفية شفافة
        case filled     // خلفية ملونة
        case minimal    // بدون خلفية
    }
    
    var body: some View {
        HStack(spacing: 3) {
            Image(systemName: "star.fill")
                .font(.system(size: 10))
                .foregroundStyle(Theme.gold500)
            
            Text(String(format: "%.1f", rating))
                .font(Theme.detail().bold())
                .foregroundStyle(style == .filled ? .white : .appTextPrimary)
        }
        .padding(.horizontal, style == .minimal ? 0 : 8)
        .padding(.vertical, style == .minimal ? 0 : 4)
        .background(badgeBackground)
        .clipShape(Capsule())
    }
    
    @ViewBuilder
    private var badgeBackground: some View {
        switch style {
        case .standard:
            Color.appCardBackground
        case .filled:
            Color.ratingColor(for: rating)
        case .minimal:
            Color.clear
        }
    }
}

#Preview {
    VStack(spacing: 20) {
        RatingView(rating: 4.7)
        RatingView(rating: 3.5, size: 20)
        RatingBadge(rating: 4.7)
        RatingBadge(rating: 4.7, style: .filled)
        RatingBadge(rating: 4.7, style: .minimal)
    }
    .padding()
    .background(Color.appBackground)
}
