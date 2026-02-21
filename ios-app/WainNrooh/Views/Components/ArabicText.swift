// ArabicText.swift
// Arabic text helpers

import SwiftUI

struct ArabicText: View {
    let text: String
    let font: Font
    let color: Color
    
    init(_ text: String, font: Font = .body, color: Color = .primary) {
        self.text = text
        self.font = font
        self.color = color
    }
    
    var body: some View {
        Text(text)
            .font(font)
            .foregroundStyle(color)
            .multilineTextAlignment(.trailing)
            .environment(\.layoutDirection, .rightToLeft)
    }
}
