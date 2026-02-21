// View+RTL.swift
// RTL support helpers

import SwiftUI

extension View {
    /// Apply RTL layout direction
    func rtl() -> some View {
        self.environment(\.layoutDirection, .rightToLeft)
    }
    
    /// Conditional modifier
    @ViewBuilder
    func `if`<Content: View>(_ condition: Bool, transform: (Self) -> Content) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}
