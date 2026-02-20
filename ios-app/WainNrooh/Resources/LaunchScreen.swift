// LaunchScreen.swift
// شاشة الإطلاق — أول شي يشوفه المستخدم

import SwiftUI

// MARK: - شاشة الإطلاق

/// شاشة الإطلاق — شعار التطبيق مع خلفية ذهبية
struct LaunchScreen: View {
    
    @State private var isAnimating = false
    @State private var opacity = 0.0
    
    var body: some View {
        ZStack {
            // الخلفية
            LinearGradient(
                colors: [
                    Color(hex: "0A1628"),
                    Color(hex: "122240")
                ],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
            
            // المحتوى
            VStack(spacing: 24) {
                // الشعار
                ZStack {
                    // الدائرة الخلفية
                    Circle()
                        .fill(
                            RadialGradient(
                                colors: [
                                    Color(hex: "C9A84C").opacity(0.3),
                                    Color.clear
                                ],
                                center: .center,
                                startRadius: 20,
                                endRadius: 80
                            )
                        )
                        .frame(width: 160, height: 160)
                        .scaleEffect(isAnimating ? 1.1 : 0.9)
                    
                    // أيقونة الموقع
                    Image(systemName: "mappin.circle.fill")
                        .font(.system(size: 72))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [
                                    Color(hex: "C9A84C"),
                                    Color(hex: "DFC474")
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .scaleEffect(isAnimating ? 1.0 : 0.8)
                }
                
                // اسم التطبيق
                VStack(spacing: 8) {
                    Text("وين نروح")
                        .font(.system(size: 36, weight: .bold, design: .rounded))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [
                                    Color(hex: "C9A84C"),
                                    Color(hex: "DFC474")
                                ],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                    
                    Text("اكتشف أفضل الأماكن بالرياض")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(.white.opacity(0.7))
                }
                .opacity(opacity)
            }
        }
        .onAppear {
            withAnimation(.easeInOut(duration: 1.0).repeatForever(autoreverses: true)) {
                isAnimating = true
            }
            withAnimation(.easeIn(duration: 0.8)) {
                opacity = 1.0
            }
        }
    }
}

// MARK: - Preview

#Preview {
    LaunchScreen()
}
