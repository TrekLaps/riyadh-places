// Color+Theme.swift
// ألوان متكيفة مع Dark/Light + تحويل Hex
// هوية "ليالي الرياض"

import SwiftUI

// MARK: - تحويل من Hex

extension Color {
    
    /// إنشاء لون من كود Hex
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        
        let a, r, g, b: UInt64
        switch hex.count {
        case 3:
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
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
}

// MARK: - ألوان متكيفة (Dark ↔ Light)

extension Color {
    
    /// لون يتكيف مع الوضع
    static func adaptive(light: Color, dark: Color) -> Color {
        Color(UIColor { traitCollection in
            traitCollection.userInterfaceStyle == .dark
                ? UIColor(dark)
                : UIColor(light)
        })
    }
    
    // MARK: - خلفيات
    
    /// خلفية رئيسية
    static let appBackground = adaptive(
        light: Color(hex: "F5F2EB"),  // كريمي فاتح
        dark: Color(hex: "050F0B")    // أخضر-900 (ليل)
    )
    
    /// خلفية البطاقة
    static let appCardBackground = adaptive(
        light: .white,
        dark: Color(hex: "0A1F16")    // أخضر-800
    )
    
    /// خلفية ثانوية
    static let appSecondaryBackground = adaptive(
        light: Color(hex: "EBE8E0"),
        dark: Color(hex: "0D3B2E")    // أخضر-700
    )
    
    /// خلفية شريط البحث
    static let appSearchBackground = adaptive(
        light: Color(hex: "E8E5DD"),
        dark: Color(hex: "0A1F16").opacity(0.8)
    )
    
    // MARK: - نصوص
    
    /// نص رئيسي
    static let appTextPrimary = adaptive(
        light: Color(hex: "1A1A1A"),
        dark: Color(hex: "F0EDE5")    // كريمي
    )
    
    /// نص ثانوي
    static let appTextSecondary = adaptive(
        light: Color(hex: "6B6B6B"),
        dark: Color(hex: "B8A88A")    // رمل
    )
    
    /// نص على الصورة
    static let appTextOnImage = Color(hex: "F0EDE5")
    
    // MARK: - حدود وفواصل
    
    /// حدود
    static let appBorder = adaptive(
        light: Color(hex: "D4D0C8"),
        dark: Color(hex: "1A6B4A").opacity(0.3)  // أخضر-600
    )
    
    /// فاصل
    static let appDivider = adaptive(
        light: Color(hex: "D4D0C8").opacity(0.5),
        dark: Color(hex: "1A6B4A").opacity(0.2)
    )
    
    // MARK: - ألوان الأسعار
    
    /// لون مستوى السعر
    static func priceColor(for level: String) -> Color {
        switch level {
        case "٫", "$", "رخيص":
            return Theme.priceLow
        case "٫٫", "$$", "متوسط":
            return Theme.priceMedium
        case "٫٫٫", "$$$", "غالي":
            return Theme.priceHigh
        case "٫٫٫٫", "$$$$", "فخم":
            return Color(hex: "8B0000")
        default:
            return Theme.sand
        }
    }
    
    // MARK: - ألوان التقييم
    
    /// لون التقييم
    static func ratingColor(for rating: Double) -> Color {
        switch rating {
        case 4.5...: return Theme.green400      // ممتاز
        case 4.0..<4.5: return Theme.green300   // جيد جداً
        case 3.5..<4.0: return Theme.gold500    // جيد
        case 3.0..<3.5: return Theme.warning    // مقبول
        default: return Theme.error              // ضعيف
        }
    }
    
    // MARK: - ألوان الفئات
    
    /// لون الفئة
    static func categoryColor(for category: String) -> Color {
        switch category {
        case "مطاعم", "restaurants":
            return Color(hex: "E74C3C")  // أحمر دافئ
        case "كافيهات", "cafes":
            return Color(hex: "C9A84C")  // ذهبي
        case "ترفيه", "entertainment":
            return Color(hex: "9B59B6")  // بنفسجي
        case "تسوق", "shopping":
            return Color(hex: "3CC98E")  // أخضر
        case "فنادق", "hotels":
            return Color(hex: "2980B9")  // أزرق
        case "طبيعة", "nature":
            return Color(hex: "27AE60")  // أخضر طبيعي
        case "حلويات", "desserts":
            return Color(hex: "E67E22")  // برتقالي
        case "شاليهات", "chalets":
            return Color(hex: "1ABC9C")  // تركوازي
        case "مولات", "malls":
            return Color(hex: "F39C12")  // ذهبي فاتح
        case "متاحف", "museums":
            return Color(hex: "8E44AD")  // بنفسجي غامق
        case "فعاليات", "events":
            return Color(hex: "E91E63")  // وردي
        default:
            return Theme.green400
        }
    }
    
    // MARK: - حالة المكان
    
    /// مفتوح / مغلق
    static func statusColor(isOpen: Bool) -> Color {
        isOpen ? Theme.success : Theme.error
    }
}
