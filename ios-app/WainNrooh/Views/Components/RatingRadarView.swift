// RatingRadarView.swift
// Tabelog-style multi-dimensional rating — SVG radar chart

import SwiftUI

struct RatingRadarView: View {
    let dimensions: RatingDimensions
    let size: CGFloat
    
    init(dimensions: RatingDimensions, size: CGFloat = 80) {
        self.dimensions = dimensions
        self.size = size
    }
    
    private let labels = ["جودة", "خدمة", "أجواء", "قيمة"]
    
    var body: some View {
        ZStack {
            // Background grid
            ForEach([0.2, 0.4, 0.6, 0.8, 1.0], id: \.self) { scale in
                RadarShape(values: [scale, scale, scale, scale])
                    .stroke(Color.gray.opacity(0.15), lineWidth: 0.5)
            }
            
            // Data shape
            RadarShape(values: normalizedValues)
                .fill(Theme.primary.opacity(0.2))
            RadarShape(values: normalizedValues)
                .stroke(Theme.primary, lineWidth: 1.5)
            
            // Data points
            ForEach(0..<4) { i in
                let point = radarPoint(index: i, value: normalizedValues[i])
                Circle()
                    .fill(Theme.primary)
                    .frame(width: 4, height: 4)
                    .position(point)
            }
            
            // Labels
            ForEach(0..<4) { i in
                let point = labelPoint(index: i)
                Text(labels[i])
                    .font(.system(size: 8))
                    .foregroundStyle(.secondary)
                    .position(point)
            }
        }
        .frame(width: size, height: size)
    }
    
    private var normalizedValues: [Double] {
        [dimensions.quality / 5.0, dimensions.service / 5.0,
         dimensions.ambiance / 5.0, dimensions.value / 5.0]
    }
    
    private func radarPoint(index: Int, value: Double) -> CGPoint {
        let angle = (Double(index) / 4.0) * 2 * .pi - .pi / 2
        let radius = value * size / 2 * 0.7
        return CGPoint(
            x: size / 2 + cos(angle) * radius,
            y: size / 2 + sin(angle) * radius
        )
    }
    
    private func labelPoint(index: Int) -> CGPoint {
        let angle = (Double(index) / 4.0) * 2 * .pi - .pi / 2
        let radius = size / 2 * 0.95
        return CGPoint(
            x: size / 2 + cos(angle) * radius,
            y: size / 2 + sin(angle) * radius
        )
    }
}

struct RadarShape: Shape {
    let values: [Double]
    
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let radius = min(rect.width, rect.height) / 2 * 0.7
        
        for (i, value) in values.enumerated() {
            let angle = (Double(i) / Double(values.count)) * 2 * .pi - .pi / 2
            let point = CGPoint(
                x: center.x + cos(angle) * radius * value,
                y: center.y + sin(angle) * radius * value
            )
            if i == 0 { path.move(to: point) }
            else { path.addLine(to: point) }
        }
        path.closeSubpath()
        return path
    }
}
