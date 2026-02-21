// LaunchScreen.swift
// شاشة الإطلاق — splash screen

import SwiftUI

struct LaunchScreen: View {
    @State private var opacity = 0.0
    @State private var scale = 0.8
    
    var body: some View {
        ZStack {
            Theme.backgroundDark
                .ignoresSafeArea()
            
            VStack(spacing: 16) {
                Text("🏙️")
                    .font(.system(size: 80))
                
                Text("وين نروح؟")
                    .font(.system(size: 36, weight: .bold))
                    .foregroundStyle(Theme.primary)
                
                Text("اكتشف الرياض")
                    .font(.title3)
                    .foregroundStyle(.secondary)
            }
            .scaleEffect(scale)
            .opacity(opacity)
        }
        .onAppear {
            withAnimation(.easeOut(duration: 0.6)) {
                opacity = 1
                scale = 1
            }
        }
    }
}
