// RatingView.swift
// عرض التقييم — نجوم ذهبية

import SwiftUI

// MARK: - عرض التقييم

/// عرض التقييم بالنجوم
struct RatingView: View {
    let rating: Double
    var maxRating: Int = 5
    var size: RatingSize = .medium
    var showCount: Bool = false
    var count: Int?
    
    enum RatingSize {
        case small, medium, large
        
        var starSize: CGFloat {
            switch self {
            case .small: return 10
            case .medium: return 14
            case .large: return 20
            }
        }
        
        var fontSize: CGFloat {
            switch self {
            case .small: return 11
            case .medium: return 13
            case .large: return 16
            }
        }
        
        var spacing: CGFloat {
            switch self {
            case .small: return 1
            case .medium: return 2
            case .large: return 3
            }
        }
    }
    
    var body: some View {
        HStack(spacing: size.spacing) {
            // النجوم
            ForEach(0..<maxRating, id: \.self) { index in
                starImage(for: index)
                    .foregroundStyle(starColor(for: index))
                    .font(.system(size: size.starSize))
            }
            
            // الرقم
            Text(rating.formattedRating)
                .font(.system(size: size.fontSize, weight: .semibold))
                .foregroundStyle(Color.ratingColor(for: rating))
            
            // العدد
            if showCount, let count {
                Text("(\(count.formattedCount))")
                    .font(.system(size: size.fontSize - 2))
                    .foregroundStyle(Color.appTextSecondary)
            }
        }
    }
    
    /// أيقونة النجمة حسب الموقع
    private func starImage(for index: Int) -> Image {
        let threshold = Double(index) + 1
        if rating >= threshold {
            return Image(systemName: "star.fill")
        } else if rating >= threshold - 0.5 {
            return Image(systemName: "star.leadinghalf.filled")
        } else {
            return Image(systemName: "star")
        }
    }
    
    /// لون النجمة
    private func starColor(for index: Int) -> Color {
        let threshold = Double(index) + 1
        if rating >= threshold - 0.5 {
            return Theme.starFilled
        }
        return Theme.starEmpty
    }
}

// MARK: - عرض تقييم مصغر

/// عرض تقييم مصغر (رقم + نجمة واحدة)
struct CompactRating: View {
    let rating: Double
    var count: Int?
    
    var body: some View {
        HStack(spacing: 3) {
            Image(systemName: "star.fill")
                .font(.system(size: 11))
                .foregroundStyle(Theme.starFilled)
            
            Text(rating.formattedRating)
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(Color.appTextPrimary)
            
            if let count {
                Text("(\(count.formattedCount))")
                    .font(.system(size: 11))
                    .foregroundStyle(Color.appTextSecondary)
            }
        }
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 20) {
        RatingView(rating: 4.5, size: .large, showCount: true, count: 128)
        RatingView(rating: 3.7, size: .medium, showCount: true, count: 42)
        RatingView(rating: 2.5, size: .small)
        
        Divider()
        
        CompactRating(rating: 4.8, count: 256)
        CompactRating(rating: 3.2)
    }
    .padding()
    .background(Color.appBackground)
}
