// Color+Theme.swift
// إضافات الألوان — تحويل من Hex وألوان متكيفة مع الدارك/لايت

import SwiftUI

// MARK: - تحويل من Hex

extension Color {
    
    /// إنشاء لون من كود Hex
    /// - Parameter hex: كود اللون مثل "C9A84C" أو "#C9A84C"
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
    
    /// تحويل اللون إلى كود Hex
    var hexString: String {
        let components = UIColor(self).cgColor.components ?? [0, 0, 0, 1]
        let r = Int(components[0] * 255)
        let g = Int(components[1] * 255)
        let b = Int(components[2] * 255)
        return String(format: "#%02X%02X%02X", r, g, b)
    }
}

// MARK: - ألوان متكيفة

extension Color {
    
    /// إنشاء لون يتكيف مع الدارك/لايت
    static func adaptive(light: Color, dark: Color) -> Color {
        Color(UIColor { traitCollection in
            traitCollection.userInterfaceStyle == .dark
                ? UIColor(dark)
                : UIColor(light)
        })
    }
    
    // MARK: - ألوان التطبيق المتكيفة
    
    /// خلفية رئيسية
    static let appBackground = adaptive(
        light: Color(hex: "F5F5F5"),
        dark: Color(hex: "0A1628")
    )
    
    /// خلفية البطاقة
    static let appCardBackground = adaptive(
        light: .white,
        dark: Color(hex: "122240")
    )
    
    /// خلفية ثانوية
    static let appSecondaryBackground = adaptive(
        light: Color(hex: "EEEEEE"),
        dark: Color(hex: "1A2D4D")
    )
    
    /// النص الأساسي
    static let appTextPrimary = adaptive(
        light: Color(hex: "1A1A1A"),
        dark: .white
    )
    
    /// النص الثانوي
    static let appTextSecondary = adaptive(
        light: Color(hex: "6B6B6B"),
        dark: Color(hex: "9CA3AF")
    )
    
    /// الحدود
    static let appBorder = adaptive(
        light: Color(hex: "E0E0E0"),
        dark: Color(hex: "2A3F65")
    )
    
    /// الفاصل
    static let appDivider = adaptive(
        light: Color(hex: "E0E0E0").opacity(0.5),
        dark: Color(hex: "2A3F65").opacity(0.5)
    )
    
    // MARK: - ألوان نطاق السعر
    
    /// لون نطاق السعر
    static func priceColor(for range: String) -> Color {
        switch range {
        case "$": return Color(hex: "4CAF50")
        case "$$": return Color(hex: "C9A84C")
        case "$$$": return Color(hex: "FF9800")
        case "$$$$": return Color(hex: "F44336")
        default: return Color(hex: "9CA3AF")
        }
    }
    
    /// لون التقييم
    static func ratingColor(for rating: Double) -> Color {
        switch rating {
        case 4.5...: return Color(hex: "4CAF50")
        case 4.0..<4.5: return Color(hex: "8BC34A")
        case 3.5..<4.0: return Color(hex: "FFD700")
        case 3.0..<3.5: return Color(hex: "FF9800")
        default: return Color(hex: "F44336")
        }
    }
}
