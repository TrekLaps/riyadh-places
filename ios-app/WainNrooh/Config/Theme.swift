// Theme.swift
// نظام التصميم — هوية "ليالي الرياض"
// أخضر سعودي + ذهب صحراوي + Liquid Glass

import SwiftUI

// MARK: - الثيم الرئيسي

/// نظام التصميم المركزي — وين نروح
enum Theme {
    
    // MARK: - 🟢 الأخضر السعودي (Primary)
    
    /// أخضر-900 — خلفية رئيسية (ليل)
    static let green900 = Color(hex: "050F0B")
    
    /// أخضر-800 — خلفية البطاقات
    static let green800 = Color(hex: "0A1F16")
    
    /// أخضر-700 — headers, navigation
    static let green700 = Color(hex: "0D3B2E")
    
    /// أخضر-600 — أزرار ثانوية
    static let green600 = Color(hex: "1A6B4A")
    
    /// أخضر-500 — hover states
    static let green500 = Color(hex: "2E8B62")
    
    /// أخضر-400 — أزرار رئيسية، highlights
    static let green400 = Color(hex: "3CC98E")
    
    /// أخضر-300 — نصوص مميزة
    static let green300 = Color(hex: "6EDBA8")
    
    /// أخضر-200 — badges خفيفة
    static let green200 = Color(hex: "A8EBC8")
    
    /// أخضر-100 — light mode خلفية
    static let green100 = Color(hex: "D4F4E5")
    
    // MARK: - 🏅 الذهب الصحراوي (Accent)
    
    /// ذهب-600 — pressed state
    static let gold600 = Color(hex: "A08530")
    
    /// ذهب-500 — نجوم التقييم
    static let gold500 = Color(hex: "C9A84C")
    
    /// ذهب-400 — highlights
    static let gold400 = Color(hex: "DFC474")
    
    /// ذهب-300 — badges
    static let gold300 = Color(hex: "F0DFA0")
    
    // MARK: - 🏜 ألوان الأجواء
    
    /// رمل — نص ثانوي (dark)
    static let sand = Color(hex: "B8A88A")
    
    /// كريمي — نص رئيسي (dark)
    static let cream = Color(hex: "F0EDE5")
    
    /// سماء ليل
    static let nightSky = Color(hex: "0B1A2E")
    
    /// نخل
    static let palm = Color(hex: "1B4332")
    
    // MARK: - الألوان الرئيسية (Shortcuts)
    
    /// اللون الرئيسي — أخضر-400
    static let primary = green400
    
    /// اللون الرئيسي الغامق
    static let primaryDark = green700
    
    /// الأكسنت — ذهب
    static let accent = gold500
    
    // MARK: - ألوان دلالية
    
    /// نجاح / مفتوح
    static let success = green400
    
    /// خطأ / مغلق
    static let error = Color(hex: "E74C3C")
    
    /// تحذير
    static let warning = Color(hex: "F0AD4E")
    
    /// معلومة
    static let info = Color(hex: "5DADE2")
    
    // MARK: - التقييم
    
    /// نجمة ذهبية
    static let starFilled = gold500
    
    /// نجمة فارغة
    static let starEmpty = Color(hex: "3A3A3C")
    
    // MARK: - الأسعار
    
    /// رخيص
    static let priceLow = green400
    
    /// متوسط
    static let priceMedium = gold500
    
    /// غالي
    static let priceHigh = Color(hex: "E74C3C")
    
    // MARK: - 🔤 الخطوط
    
    /// عنوان كبير — ٢٨
    static func largeTitle(size: CGFloat = 28) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }
    
    /// عنوان — ٢٢
    static func title(size: CGFloat = 22) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }
    
    /// عنوان فرعي — ١٨
    static func headline(size: CGFloat = 18) -> Font {
        .system(size: size, weight: .semibold, design: .rounded)
    }
    
    /// نص عادي — ١٦
    static func body(size: CGFloat = 16) -> Font {
        .system(size: size, weight: .regular)
    }
    
    /// تفاصيل — ١٤
    static func detail(size: CGFloat = 14) -> Font {
        .system(size: size, weight: .regular)
    }
    
    /// توضيح — ١٢
    static func caption(size: CGFloat = 12) -> Font {
        .system(size: size, weight: .regular)
    }
    
    /// بادج — ١١
    static func badge(size: CGFloat = 11) -> Font {
        .system(size: size, weight: .medium)
    }
    
    /// أسعار — مونوسبيس
    static func price(size: CGFloat = 18) -> Font {
        .system(size: size, weight: .bold, design: .monospaced)
    }
    
    // MARK: - 📐 الأبعاد
    
    /// زوايا مستديرة
    static let radiusSmall: CGFloat = 8
    static let radiusMedium: CGFloat = 12
    static let radiusLarge: CGFloat = 16
    static let radiusXL: CGFloat = 24
    static let radiusFull: CGFloat = 50
    
    /// مسافات
    static let spacingXS: CGFloat = 4
    static let spacingS: CGFloat = 8
    static let spacingM: CGFloat = 12
    static let spacingL: CGFloat = 16
    static let spacingXL: CGFloat = 24
    static let spacingXXL: CGFloat = 32
    
    /// ارتفاعات
    static let cardSmall: CGFloat = 120
    static let cardMedium: CGFloat = 180
    static let cardLarge: CGFloat = 240
    static let heroHeight: CGFloat = 300
    
    // MARK: - 🌊 Gradients
    
    /// تدرج البطاقة — أخضر غامق
    static let cardGradient = LinearGradient(
        colors: [green900, green800],
        startPoint: .top,
        endPoint: .bottom
    )
    
    /// تدرج الصورة — للنص فوقها
    static let imageOverlay = LinearGradient(
        colors: [green900.opacity(0.8), .clear, green900.opacity(0.6)],
        startPoint: .bottom,
        endPoint: .top
    )
    
    /// تدرج الهيرو
    static let heroGradient = LinearGradient(
        colors: [green900, green700.opacity(0.3), .clear],
        startPoint: .bottom,
        endPoint: .center
    )
    
    /// تدرج رئيسي
    static let primaryGradient = LinearGradient(
        colors: [green600, green400],
        startPoint: .leading,
        endPoint: .trailing
    )
    
    // MARK: - 🎭 ظلال
    
    static let cardShadowColor = Color.black.opacity(0.3)
    static let cardShadowRadius: CGFloat = 12
    static let cardShadowY: CGFloat = 6
    
    static let lightShadowColor = Color.black.opacity(0.15)
    static let lightShadowRadius: CGFloat = 6
    static let lightShadowY: CGFloat = 3
    
    // MARK: - 🎬 حركات
    
    static let animFast: Animation = .easeInOut(duration: 0.2)
    static let animNormal: Animation = .easeInOut(duration: 0.35)
    static let animSpring: Animation = .spring(response: 0.4, dampingFraction: 0.75)
    static let animBouncy: Animation = .spring(response: 0.5, dampingFraction: 0.6)
}

// MARK: - 🃏 Card Style Modifier

extension View {
    
    /// ستايل بطاقة — أخضر غامق مع ظل
    func wainCard() -> some View {
        self
            .background(Theme.green800)
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
            .shadow(
                color: Theme.cardShadowColor,
                radius: Theme.cardShadowRadius,
                x: 0, y: Theme.cardShadowY
            )
    }
    
    /// زر رئيسي — أخضر متدرج
    func wainPrimaryButton() -> some View {
        self
            .font(Theme.headline(size: 16))
            .foregroundStyle(.white)
            .padding(.horizontal, Theme.spacingXL)
            .padding(.vertical, Theme.spacingM)
            .background(Theme.primaryGradient)
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
    }
    
    /// زر ثانوي — glass style
    func wainSecondaryButton() -> some View {
        self
            .font(Theme.body(size: 14))
            .foregroundStyle(Theme.green400)
            .padding(.horizontal, Theme.spacingL)
            .padding(.vertical, Theme.spacingS)
            .background(Theme.green400.opacity(0.12))
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
    }
    
    /// glass pill — لـ tags و occasions
    func wainGlassPill() -> some View {
        self
            .font(Theme.detail())
            .foregroundStyle(Theme.cream)
            .padding(.horizontal, Theme.spacingM)
            .padding(.vertical, Theme.spacingXS + 2)
            .background(.ultraThinMaterial)
            .clipShape(Capsule())
    }
    
    /// تأثير الضغط
    func wainPress() -> some View {
        self.buttonStyle(WainPressStyle())
    }
}

// MARK: - Press Button Style

struct WainPressStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .opacity(configuration.isPressed ? 0.85 : 1.0)
            .animation(Theme.animFast, value: configuration.isPressed)
    }
}
