// PriceTag.swift
// عرض مستوى السعر
// هوية ليالي الرياض

import SwiftUI

struct PriceTag: View {
    let level: String
    var style: TagStyle = .standard
    
    enum TagStyle {
        case standard  // نص ملون
        case badge     // مع خلفية
        case arabic    // ترجمة عربية
    }
    
    var body: some View {
        switch style {
        case .standard:
            Text(level)
                .font(Theme.detail().bold())
                .foregroundStyle(Color.priceColor(for: level))
        case .badge:
            Text(level)
                .font(Theme.badge())
                .foregroundStyle(Color.priceColor(for: level))
                .padding(.horizontal, 8)
                .padding(.vertical, 3)
                .background(Color.priceColor(for: level).opacity(0.1))
                .clipShape(Capsule())
        case .arabic:
            Text(arabicLabel)
                .font(Theme.badge())
                .foregroundStyle(Color.priceColor(for: level))
        }
    }
    
    private var arabicLabel: String {
        switch level {
        case "$", "٫": return "رخيص"
        case "$$", "٫٫": return "متوسط"
        case "$$$", "٫٫٫": return "غالي"
        case "$$$$", "٫٫٫٫": return "فخم"
        default: return level
        }
    }
}

#Preview {
    VStack(spacing: 12) {
        PriceTag(level: "$")
        PriceTag(level: "$$", style: .badge)
        PriceTag(level: "$$$", style: .arabic)
        PriceTag(level: "$$$$", style: .badge)
    }
    .padding()
    .background(Color.appBackground)
}
