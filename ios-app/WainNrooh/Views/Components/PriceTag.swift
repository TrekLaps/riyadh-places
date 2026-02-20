// PriceTag.swift
// عرض نطاق السعر بالريال — $ إلى $$$$

import SwiftUI

// MARK: - علامة السعر

/// عرض نطاق السعر ($ إلى $$$$)
struct PriceTag: View {
    let priceRange: String
    var size: TagSize = .medium
    
    enum TagSize {
        case small, medium, large
        
        var fontSize: CGFloat {
            switch self {
            case .small: return 11
            case .medium: return 13
            case .large: return 16
            }
        }
        
        var padding: CGFloat {
            switch self {
            case .small: return 4
            case .medium: return 6
            case .large: return 8
            }
        }
    }
    
    var body: some View {
        Text(priceText)
            .font(.system(size: size.fontSize, weight: .semibold, design: .monospaced))
            .foregroundStyle(priceColor)
            .padding(.horizontal, size.padding + 2)
            .padding(.vertical, size.padding)
            .background(priceColor.opacity(0.12))
            .clipShape(RoundedRectangle(cornerRadius: 6))
    }
    
    /// نص السعر المنسق
    private var priceText: String {
        switch priceRange {
        case "$": return "💰 رخيص"
        case "$$": return "💰💰 متوسط"
        case "$$$": return "💰💰💰 غالي"
        case "$$$$": return "💰💰💰💰 فاخر"
        default: return priceRange
        }
    }
    
    /// لون السعر
    private var priceColor: Color {
        Color.priceColor(for: priceRange)
    }
}

// MARK: - عرض سعر بالريال

/// عرض سعر محدد بالريال السعودي
struct SARPrice: View {
    let amount: Double
    var size: PriceTag.TagSize = .medium
    var showCurrency: Bool = true
    var strikethrough: Double?
    
    var body: some View {
        HStack(spacing: 4) {
            // السعر الأصلي (مشطوب)
            if let original = strikethrough, original > amount {
                Text("\(Int(original))")
                    .strikethrough()
                    .font(.system(size: size.fontSize - 2))
                    .foregroundStyle(Color.appTextSecondary)
            }
            
            // السعر الحالي
            Text(formattedAmount)
                .font(.system(size: size.fontSize, weight: .bold, design: .rounded))
                .foregroundStyle(Color.appTextPrimary)
            
            // العملة
            if showCurrency {
                Text("ر.س")
                    .font(.system(size: size.fontSize - 2, weight: .regular))
                    .foregroundStyle(Color.appTextSecondary)
            }
        }
    }
    
    private var formattedAmount: String {
        if amount == 0 { return "مجاني" }
        if amount == floor(amount) { return "\(Int(amount))" }
        return String(format: "%.1f", amount)
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 16) {
        HStack(spacing: 12) {
            PriceTag(priceRange: "$", size: .small)
            PriceTag(priceRange: "$$", size: .medium)
            PriceTag(priceRange: "$$$", size: .medium)
            PriceTag(priceRange: "$$$$", size: .large)
        }
        
        Divider()
        
        VStack(spacing: 8) {
            SARPrice(amount: 45, size: .large)
            SARPrice(amount: 0, size: .medium)
            SARPrice(amount: 89.5, size: .medium, strikethrough: 120)
        }
    }
    .padding()
    .background(Color.appBackground)
}
