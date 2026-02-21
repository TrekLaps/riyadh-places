// AppLogo.swift
// شعار التطبيق

import SwiftUI

struct AppLogo: View {
    let size: CGFloat
    
    init(size: CGFloat = 60) {
        self.size = size
    }
    
    var body: some View {
        ZStack {
            Circle()
                .fill(Theme.primary.gradient)
                .frame(width: size, height: size)
            
            Text("🏙️")
                .font(.system(size: size * 0.5))
        }
    }
}
