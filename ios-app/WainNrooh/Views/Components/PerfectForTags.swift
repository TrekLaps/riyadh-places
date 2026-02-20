// PerfectForTags.swift
// شرائح "مناسب لـ" — رومانسي، عوائل، شباب...

import SwiftUI

// MARK: - شرائح "مناسب لـ"

/// عرض تاقات "مناسب لـ" كشرائح ملونة
struct PerfectForTags: View {
    let tags: [String]
    var size: TagSize = .medium
    
    enum TagSize {
        case small, medium, large
        
        var fontSize: CGFloat {
            switch self {
            case .small: return 10
            case .medium: return 12
            case .large: return 14
            }
        }
        
        var padding: CGFloat {
            switch self {
            case .small: return 4
            case .medium: return 6
            case .large: return 8
            }
        }
    }
    
    var body: some View {
        FlowLayout(spacing: 6) {
            ForEach(tags, id: \.self) { tag in
                TagChip(
                    text: tag,
                    emoji: emojiFor(tag),
                    color: colorFor(tag),
                    fontSize: size.fontSize,
                    padding: size.padding
                )
            }
        }
    }
    
    /// الإيموجي المناسب للتاق
    private func emojiFor(_ tag: String) -> String {
        let lowered = tag.arabicNormalized.lowercased()
        
        if lowered.contains("رومانسي") || lowered.contains("كبلز") { return "💕" }
        if lowered.contains("عوائل") || lowered.contains("عائل") { return "👨‍👩‍👧‍👦" }
        if lowered.contains("شباب") || lowered.contains("أصدقاء") { return "🔥" }
        if lowered.contains("عمل") || lowered.contains("اجتماع") { return "💼" }
        if lowered.contains("دراس") { return "📚" }
        if lowered.contains("هادي") || lowered.contains("ريلاكس") { return "😌" }
        if lowered.contains("فخم") || lowered.contains("فاخر") { return "✨" }
        if lowered.contains("سهر") || lowered.contains("ليل") { return "🌙" }
        if lowered.contains("فطور") || lowered.contains("برنش") { return "🌅" }
        if lowered.contains("قهوة") { return "☕" }
        if lowered.contains("حفل") || lowered.contains("مناسب") { return "🎉" }
        if lowered.contains("أطفال") { return "👶" }
        if lowered.contains("رياض") || lowered.contains("طبيع") { return "🌿" }
        
        return "✨"
    }
    
    /// اللون المناسب للتاق
    private func colorFor(_ tag: String) -> Color {
        let lowered = tag.arabicNormalized.lowercased()
        
        if lowered.contains("رومانسي") || lowered.contains("كبلز") { return .pink }
        if lowered.contains("عوائل") { return .blue }
        if lowered.contains("شباب") { return .orange }
        if lowered.contains("عمل") || lowered.contains("دراس") { return .indigo }
        if lowered.contains("هادي") { return .teal }
        if lowered.contains("فخم") { return Theme.primary }
        if lowered.contains("سهر") { return .purple }
        if lowered.contains("فطور") { return .yellow }
        
        return Theme.accent
    }
}

// MARK: - شريحة واحدة

/// شريحة واحدة (Tag Chip)
struct TagChip: View {
    let text: String
    var emoji: String = ""
    var color: Color = Theme.accent
    var fontSize: CGFloat = 12
    var padding: CGFloat = 6
    var isSelected: Bool = false
    
    var body: some View {
        HStack(spacing: 3) {
            if !emoji.isEmpty {
                Text(emoji)
                    .font(.system(size: fontSize))
            }
            Text(text)
                .font(.system(size: fontSize, weight: isSelected ? .semibold : .regular))
        }
        .padding(.horizontal, padding + 4)
        .padding(.vertical, padding)
        .foregroundStyle(isSelected ? .white : color)
        .background(
            isSelected ? color : color.opacity(0.12)
        )
        .clipShape(Capsule())
    }
}

// MARK: - تخطيط مرن (Flow Layout)

/// تخطيط مرن — يرتب العناصر بسطور مع التفاف تلقائي
struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = calculateLayout(proposal: proposal, subviews: subviews)
        return result.size
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = calculateLayout(proposal: proposal, subviews: subviews)
        
        for (index, position) in result.positions.enumerated() {
            guard index < subviews.count else { break }
            subviews[index].place(
                at: CGPoint(
                    x: bounds.maxX - position.x - subviews[index].sizeThatFits(.unspecified).width,
                    y: bounds.minY + position.y
                ),
                proposal: .unspecified
            )
        }
    }
    
    private func calculateLayout(proposal: ProposedViewSize, subviews: Subviews) -> (size: CGSize, positions: [CGPoint]) {
        let maxWidth = proposal.width ?? .infinity
        var positions: [CGPoint] = []
        var currentX: CGFloat = 0
        var currentY: CGFloat = 0
        var lineHeight: CGFloat = 0
        var totalHeight: CGFloat = 0
        
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            
            if currentX + size.width > maxWidth && currentX > 0 {
                currentX = 0
                currentY += lineHeight + spacing
                lineHeight = 0
            }
            
            positions.append(CGPoint(x: currentX, y: currentY))
            currentX += size.width + spacing
            lineHeight = max(lineHeight, size.height)
            totalHeight = currentY + lineHeight
        }
        
        return (CGSize(width: maxWidth, height: totalHeight), positions)
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 20) {
        PerfectForTags(
            tags: ["رومانسي", "عوائل", "شباب", "عمل", "هادي"],
            size: .medium
        )
        
        PerfectForTags(
            tags: ["فطور", "سهرة", "فاخر"],
            size: .small
        )
        
        PerfectForTags(
            tags: ["دراسة", "أطفال"],
            size: .large
        )
    }
    .padding()
    .background(Color.appBackground)
}
