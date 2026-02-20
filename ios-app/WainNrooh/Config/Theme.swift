// Theme.swift
// نظام التصميم — الألوان والخطوط والأبعاد
// Dark/Light mode مع ألوان ذهبية سعودية

import SwiftUI

// MARK: - الثيم الرئيسي

/// نظام التصميم المركزي للتطبيق
enum Theme {
    
    // MARK: - الألوان الرئيسية
    
    /// الذهبي الأساسي — #C9A84C
    static let primary = Color(hex: "C9A84C")
    
    /// الذهبي الفاتح
    static let primaryLight = Color(hex: "DFC474")
    
    /// الذهبي الغامق
    static let primaryDark = Color(hex: "A08530")
    
    /// الأزرق المساعد — #2196F3
    static let accent = Color(hex: "2196F3")
    
    /// الأزرق الفاتح
    static let accentLight = Color(hex: "64B5F6")
    
    // MARK: - ألوان الخلفية
    
    /// خلفية داكنة — #0A1628
    static let backgroundDark = Color(hex: "0A1628")
    
    /// خلفية فاتحة — #F5F5F5
    static let backgroundLight = Color(hex: "F5F5F5")
    
    /// خلفية البطاقة (دارك)
    static let cardBackgroundDark = Color(hex: "122240")
    
    /// خلفية البطاقة (لايت)
    static let cardBackgroundLight = Color.white
    
    /// خلفية ثانوية (دارك)
    static let secondaryBackgroundDark = Color(hex: "1A2D4D")
    
    /// خلفية ثانوية (لايت)
    static let secondaryBackgroundLight = Color(hex: "EEEEEE")
    
    // MARK: - ألوان تتكيف مع الوضع (Adaptive)
    
    /// خلفية رئيسية — تتكيف مع الدارك/لايت
    static let backgroundPrimary = Color("BackgroundPrimary", bundle: nil)
        
    /// خلفية البطاقة — تتكيف
    static let cardBackground = Color("CardBackground", bundle: nil)
    
    /// النص الأساسي
    static let textPrimary = Color("TextPrimary", bundle: nil)
    
    /// النص الثانوي
    static let textSecondary = Color("TextSecondary", bundle: nil)
    
    // MARK: - ألوان دلالية
    
    /// أخضر — للنجاح والتوفر
    static let success = Color(hex: "4CAF50")
    
    /// أحمر — للأخطاء والحذف
    static let error = Color(hex: "F44336")
    
    /// برتقالي — للتحذيرات
    static let warning = Color(hex: "FF9800")
    
    /// أزرق — للمعلومات
    static let info = Color(hex: "2196F3")
    
    // MARK: - ألوان التقييم
    
    /// نجمة ذهبية
    static let starFilled = Color(hex: "FFD700")
    
    /// نجمة فارغة
    static let starEmpty = Color(hex: "3A3A3C")
    
    // MARK: - ألوان الأسعار
    
    /// سعر رخيص
    static let pricelow = Color(hex: "4CAF50")
    
    /// سعر متوسط
    static let priceMedium = Color(hex: "FF9800")
    
    /// سعر غالي
    static let priceHigh = Color(hex: "F44336")
    
    // MARK: - الخطوط
    
    /// عنوان كبير (Arabic: Tajawal Bold, English: SF Pro Bold)
    static func titleFont(size: CGFloat = 24) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }
    
    /// عنوان متوسط
    static func headlineFont(size: CGFloat = 18) -> Font {
        .system(size: size, weight: .semibold, design: .rounded)
    }
    
    /// نص عادي
    static func bodyFont(size: CGFloat = 16) -> Font {
        .system(size: size, weight: .regular)
    }
    
    /// نص صغير
    static func captionFont(size: CGFloat = 13) -> Font {
        .system(size: size, weight: .regular)
    }
    
    /// نص صغير جداً
    static func footnoteFont(size: CGFloat = 11) -> Font {
        .system(size: size, weight: .regular)
    }
    
    /// رقم (سعر)
    static func priceFont(size: CGFloat = 20) -> Font {
        .system(size: size, weight: .bold, design: .monospaced)
    }
    
    // MARK: - الأبعاد
    
    /// زوايا مستديرة — صغيرة
    static let cornerRadiusSmall: CGFloat = 8
    
    /// زوايا مستديرة — متوسطة
    static let cornerRadiusMedium: CGFloat = 12
    
    /// زوايا مستديرة — كبيرة
    static let cornerRadiusLarge: CGFloat = 16
    
    /// زوايا مستديرة — كبيرة جداً
    static let cornerRadiusXL: CGFloat = 24
    
    /// مسافة داخلية — صغيرة
    static let paddingSmall: CGFloat = 8
    
    /// مسافة داخلية — متوسطة
    static let paddingMedium: CGFloat = 16
    
    /// مسافة داخلية — كبيرة
    static let paddingLarge: CGFloat = 24
    
    /// مسافة بين العناصر — صغيرة
    static let spacingSmall: CGFloat = 8
    
    /// مسافة بين العناصر — متوسطة
    static let spacingMedium: CGFloat = 12
    
    /// مسافة بين العناصر — كبيرة
    static let spacingLarge: CGFloat = 16
    
    /// ارتفاع البطاقة الصغيرة
    static let cardHeightSmall: CGFloat = 120
    
    /// ارتفاع البطاقة المتوسطة
    static let cardHeightMedium: CGFloat = 180
    
    /// ارتفاع البطاقة الكبيرة
    static let cardHeightLarge: CGFloat = 240
    
    // MARK: - ظلال
    
    /// ظل البطاقة
    static let cardShadow = Shadow(color: .black.opacity(0.15), radius: 8, x: 0, y: 4)
    
    /// ظل خفيف
    static let lightShadow = Shadow(color: .black.opacity(0.08), radius: 4, x: 0, y: 2)
    
    // MARK: - حركات (Animations)
    
    /// حركة سريعة
    static let animationFast: Animation = .easeInOut(duration: 0.2)
    
    /// حركة عادية
    static let animationNormal: Animation = .easeInOut(duration: 0.35)
    
    /// حركة نابضية
    static let animationSpring: Animation = .spring(response: 0.4, dampingFraction: 0.75)
}

// MARK: - بنية الظل

/// بنية مساعدة للظلال
struct Shadow {
    let color: Color
    let radius: CGFloat
    let x: CGFloat
    let y: CGFloat
}

// MARK: - معدّلات عرض مشتركة

extension View {
    
    /// تطبيق ستايل البطاقة
    func cardStyle(isDark: Bool = true) -> some View {
        self
            .background(isDark ? Theme.cardBackgroundDark : Theme.cardBackgroundLight)
            .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
            .shadow(
                color: Theme.cardShadow.color,
                radius: Theme.cardShadow.radius,
                x: Theme.cardShadow.x,
                y: Theme.cardShadow.y
            )
    }
    
    /// تطبيق ستايل الزر الذهبي
    func goldButtonStyle() -> some View {
        self
            .font(Theme.headlineFont(size: 16))
            .foregroundStyle(.white)
            .padding(.horizontal, Theme.paddingLarge)
            .padding(.vertical, Theme.paddingSmall + 4)
            .background(Theme.primary)
            .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
    }
    
    /// تطبيق ستايل الزر الثانوي
    func secondaryButtonStyle() -> some View {
        self
            .font(Theme.bodyFont(size: 14))
            .foregroundStyle(Theme.primary)
            .padding(.horizontal, Theme.paddingMedium)
            .padding(.vertical, Theme.paddingSmall)
            .background(Theme.primary.opacity(0.15))
            .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
    }
    
    /// تطبيق تأثير الضغط
    func pressEffect() -> some View {
        self.buttonStyle(PressButtonStyle())
    }
}

// MARK: - ستايل زر الضغط

/// تأثير بصري عند الضغط على الزر
struct PressButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .opacity(configuration.isPressed ? 0.85 : 1.0)
            .animation(Theme.animationFast, value: configuration.isPressed)
    }
}
