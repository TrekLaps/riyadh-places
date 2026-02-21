// PerfectForTags.swift
// Tags display

import SwiftUI

struct PerfectForTags: View {
    let tags: [String]
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 6) {
                ForEach(tags, id: \.self) { tag in
                    Text(tag)
                        .font(.caption2)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Theme.primary.opacity(0.1))
                        .foregroundStyle(Theme.primary)
                        .clipShape(Capsule())
                }
            }
        }
    }
}
