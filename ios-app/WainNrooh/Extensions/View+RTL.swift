// View+RTL.swift
// إضافات العرض — دعم RTL والتخطيط العربي

import SwiftUI

// MARK: - دعم RTL

extension View {
    
    /// تطبيق اتجاه RTL
    func rtl() -> some View {
        self.environment(\.layoutDirection, .rightToLeft)
    }
    
    /// محاذاة النص لليمين (عربي)
    func alignRight() -> some View {
        self.multilineTextAlignment(.trailing)
    }
    
    /// محاذاة النص لليسار (إنجليزي)
    func alignLeft() -> some View {
        self.multilineTextAlignment(.leading)
    }
    
    /// إطار كامل العرض مع محاذاة
    func fullWidth(alignment: Alignment = .trailing) -> some View {
        self.frame(maxWidth: .infinity, alignment: alignment)
    }
    
    /// إخفاء مشروط
    @ViewBuilder
    func hidden(_ isHidden: Bool) -> some View {
        if isHidden {
            self.hidden()
        } else {
            self
        }
    }
    
    /// عرض مشروط
    @ViewBuilder
    func `if`<Content: View>(_ condition: Bool, transform: (Self) -> Content) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
    
    /// تطبيق تعديل اختياري
    @ViewBuilder
    func ifLet<Value, Content: View>(_ value: Value?, transform: (Self, Value) -> Content) -> some View {
        if let value {
            transform(self, value)
        } else {
            self
        }
    }
}

// MARK: - Shimmer Effect (تأثير التحميل)

extension View {
    
    /// تأثير اللمعان أثناء التحميل
    func shimmer(isActive: Bool = true) -> some View {
        self.modifier(ShimmerModifier(isActive: isActive))
    }
    
    /// placeholder أثناء التحميل
    func loadingPlaceholder(isLoading: Bool) -> some View {
        self.modifier(LoadingPlaceholderModifier(isLoading: isLoading))
    }
}

/// معدّل تأثير اللمعان
struct ShimmerModifier: ViewModifier {
    let isActive: Bool
    @State private var phase: CGFloat = 0
    
    func body(content: Content) -> some View {
        if isActive {
            content
                .overlay(
                    LinearGradient(
                        gradient: Gradient(colors: [
                            .clear,
                            .white.opacity(0.3),
                            .clear
                        ]),
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                    .offset(x: phase)
                    .mask(content)
                )
                .onAppear {
                    withAnimation(.linear(duration: 1.5).repeatForever(autoreverses: false)) {
                        phase = 300
                    }
                }
        } else {
            content
        }
    }
}

/// معدّل placeholder التحميل
struct LoadingPlaceholderModifier: ViewModifier {
    let isLoading: Bool
    
    func body(content: Content) -> some View {
        if isLoading {
            content
                .redacted(reason: .placeholder)
                .shimmer()
        } else {
            content
        }
    }
}

// MARK: - معدّلات تنقل

extension View {
    
    /// شريط تنقل بنمط التطبيق
    func appNavigationBar(title: String) -> some View {
        self
            .navigationTitle(title)
            .navigationBarTitleDisplayMode(.large)
            .toolbarBackground(Color.appBackground, for: .navigationBar)
    }
    
    /// إخفاء شريط التنقل
    func hideNavigationBar() -> some View {
        self
            .navigationBarHidden(true)
    }
}

// MARK: - معدّلات تخطيط

extension View {
    
    /// مسافة داخلية أفقية قياسية
    func horizontalPadding(_ padding: CGFloat = Theme.paddingMedium) -> some View {
        self.padding(.horizontal, padding)
    }
    
    /// مسافة داخلية رأسية قياسية
    func verticalPadding(_ padding: CGFloat = Theme.paddingMedium) -> some View {
        self.padding(.vertical, padding)
    }
    
    /// رسالة فارغة عندما لا توجد نتائج
    func emptyState(isEmpty: Bool, message: String, icon: String = "tray.fill") -> some View {
        self.overlay {
            if isEmpty {
                ContentUnavailableView {
                    Label(message, systemImage: icon)
                } description: {
                    Text("جرب تغيير الفلاتر أو البحث بكلمات مختلفة")
                }
            }
        }
    }
}

// MARK: - معدّل التحريك عند الظهور

extension View {
    
    /// تحريك العنصر عند الظهور (تلاشي + انزلاق)
    func appearAnimation(delay: Double = 0) -> some View {
        self.modifier(AppearAnimationModifier(delay: delay))
    }
}

/// معدّل تحريك الظهور
struct AppearAnimationModifier: ViewModifier {
    let delay: Double
    @State private var isVisible = false
    
    func body(content: Content) -> some View {
        content
            .opacity(isVisible ? 1 : 0)
            .offset(y: isVisible ? 0 : 20)
            .onAppear {
                withAnimation(Theme.animationNormal.delay(delay)) {
                    isVisible = true
                }
            }
    }
}
