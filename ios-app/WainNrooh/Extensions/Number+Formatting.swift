// Number+Formatting.swift
// Number formatting helpers

import Foundation

extension Double {
    /// Format rating: 4.5 → "4.5", 4.0 → "4.0"
    var formattedRating: String {
        String(format: "%.1f", self)
    }
}

extension Int {
    /// Format count: 1234 → "1.2K", 150 → "150"
    var formattedCount: String {
        if self >= 1000 {
            return String(format: "%.1fK", Double(self) / 1000.0)
        }
        return "\(self)"
    }
}
