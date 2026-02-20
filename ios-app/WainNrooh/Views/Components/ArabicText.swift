// ArabicText.swift
// مكون النص العربي — RTL helper

import SwiftUI

// MARK: - نص عربي

/// مكون نص عربي مع دعم RTL والخطوط المناسبة
struct ArabicText: View {
    let text: String
    var style: ArabicTextStyle = .body
    var color: Color?
    var lineLimit: Int?
    var alignment: TextAlignment = .trailing
    
    enum ArabicTextStyle {
        case largeTitle
        case title
        case headline
        case body
        case caption
        case footnote
        case price
        
        var font: Font {
            switch self {
            case .largeTitle: return Theme.titleFont(size: 28)
            case .title: return Theme.titleFont(size: 22)
            case .headline: return Theme.headlineFont(size: 18)
            case .body: return Theme.bodyFont(size: 16)
            case .caption: return Theme.captionFont(size: 13)
            case .footnote: return Theme.footnoteFont(size: 11)
            case .price: return Theme.priceFont(size: 20)
            }
        }
        
        var defaultColor: Color {
            switch self {
            case .largeTitle, .title, .headline, .body, .price:
                return Color.appTextPrimary
            case .caption, .footnote:
                return Color.appTextSecondary
            }
        }
    }
    
    var body: some View {
        Text(text)
            .font(style.font)
            .foregroundStyle(color ?? style.defaultColor)
            .multilineTextAlignment(alignment)
            .lineLimit(lineLimit)
            .environment(\.layoutDirection, .rightToLeft)
    }
}

// MARK: - عنوان القسم

/// عنوان قسم مع سهم "عرض الكل"
struct SectionHeader: View {
    let title: String
    var subtitle: String?
    var showSeeAll: Bool = true
    var onSeeAll: (() -> Void)?
    
    var body: some View {
        HStack {
            // زر "عرض الكل"
            if showSeeAll {
                Button {
                    onSeeAll?()
                } label: {
                    HStack(spacing: 4) {
                        Text("عرض الكل")
                            .font(Theme.captionFont())
                        Image(systemName: "chevron.left")
                            .font(.system(size: 10))
                    }
                    .foregroundStyle(Theme.primary)
                }
            }
            
            Spacer()
            
            // العنوان والعنوان الفرعي
            VStack(alignment: .trailing, spacing: 2) {
                Text(title)
                    .font(Theme.headlineFont(size: 20))
                    .foregroundStyle(Color.appTextPrimary)
                
                if let subtitle {
                    Text(subtitle)
                        .font(Theme.captionFont())
                        .foregroundStyle(Color.appTextSecondary)
                }
            }
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
}

// MARK: - نص "لا توجد نتائج"

/// رسالة عندما لا توجد نتائج
struct EmptyStateView: View {
    let icon: String
    let title: String
    let message: String
    var actionTitle: String?
    var action: (() -> Void)?
    
    var body: some View {
        VStack(spacing: Theme.spacingLarge) {
            Image(systemName: icon)
                .font(.system(size: 48))
                .foregroundStyle(Color.appTextSecondary.opacity(0.5))
            
            VStack(spacing: 8) {
                Text(title)
                    .font(Theme.headlineFont(size: 18))
                    .foregroundStyle(Color.appTextPrimary)
                
                Text(message)
                    .font(Theme.bodyFont(size: 14))
                    .foregroundStyle(Color.appTextSecondary)
                    .multilineTextAlignment(.center)
            }
            
            if let actionTitle {
                Button(actionTitle) {
                    action?()
                }
                .goldButtonStyle()
            }
        }
        .padding(Theme.paddingLarge * 2)
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 24) {
        ArabicText(text: "وين نروح بالرياض", style: .largeTitle)
        ArabicText(text: "اكتشف أفضل الأماكن", style: .headline)
        ArabicText(text: "مقاهي ومطاعم وترفيه", style: .body)
        ArabicText(text: "آخر تحديث: قبل ساعة", style: .caption)
        
        Divider()
        
        SectionHeader(title: "الأكثر شعبية", subtitle: "حسب التقييم")
        
        Divider()
        
        EmptyStateView(
            icon: "heart.slash",
            title: "ما عندك مفضلة",
            message: "أضف أماكن للمفضلة عشان تلاقيها بسرعة",
            actionTitle: "اكتشف أماكن"
        )
    }
    .padding()
    .background(Color.appBackground)
}
