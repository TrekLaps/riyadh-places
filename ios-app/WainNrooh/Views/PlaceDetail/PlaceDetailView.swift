// PlaceDetailView.swift
// تفاصيل المكان — مع Tabelog rating + favorite + share + navigate

import SwiftUI
import SwiftData
import MapKit

struct PlaceDetailView: View {
    let place: Place
    @Environment(\.modelContext) private var modelContext
    @Query private var favorites: [CachedFavorite]
    @State private var showShareSheet = false
    
    var isFavorite: Bool {
        favorites.contains { $0.placeId == place.id }
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .trailing, spacing: 16) {
                // Hero placeholder
                ZStack {
                    RoundedRectangle(cornerRadius: 0)
                        .fill(Color(.systemGray4))
                        .frame(height: 200)
                    
                    VStack {
                        Text(place.categoryAr ?? place.category)
                            .font(.title3)
                            .foregroundStyle(.white)
                    }
                }
                
                VStack(alignment: .trailing, spacing: 16) {
                    // Name + Actions
                    HStack {
                        // Actions
                        HStack(spacing: 12) {
                            Button { toggleFavorite() } label: {
                                Image(systemName: isFavorite ? "heart.fill" : "heart")
                                    .foregroundStyle(isFavorite ? .red : .secondary)
                                    .font(.title3)
                            }
                            
                            Button { sharePlace() } label: {
                                Image(systemName: "square.and.arrow.up")
                                    .foregroundStyle(.secondary)
                                    .font(.title3)
                            }
                            
                            if place.googleMapsUrl != nil {
                                Button { openInMaps() } label: {
                                    Image(systemName: "map.fill")
                                        .foregroundStyle(Theme.primary)
                                        .font(.title3)
                                }
                            }
                        }
                        
                        Spacer()
                        
                        VStack(alignment: .trailing) {
                            Text(place.nameAr)
                                .font(.title2.bold())
                            if let nameEn = place.nameEn {
                                Text(nameEn)
                                    .font(.subheadline)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    
                    // Rating — Tabelog Style
                    if place.hasVerifiedRating {
                        HStack(spacing: 16) {
                            // Radar Chart
                            RatingRadarView(dimensions: place.ratingDimensions, size: 80)
                            
                            Spacer()
                            
                            // Overall + Label
                            VStack(alignment: .trailing, spacing: 4) {
                                HStack(spacing: 4) {
                                    Image(systemName: "star.fill")
                                        .foregroundStyle(.yellow)
                                    Text(String(format: "%.1f", place.googleRating ?? 0))
                                        .font(.title.bold())
                                }
                                if let label = place.ratingLabel {
                                    Text(label)
                                        .font(.caption)
                                        .foregroundStyle(Theme.primary)
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 2)
                                        .background(Theme.primary.opacity(0.1))
                                        .clipShape(Capsule())
                                }
                            }
                        }
                        .padding()
                        .background(Color(.secondarySystemBackground))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    
                    // Info Cards
                    infoSection
                    
                    // Description
                    if let desc = place.descriptionAr {
                        VStack(alignment: .trailing, spacing: 4) {
                            Text("عن المكان")
                                .font(.headline)
                            Text(desc)
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                    }
                    
                    // Tags
                    if let tags = place.tags, !tags.isEmpty {
                        FlowLayout(spacing: 6) {
                            ForEach(tags, id: \.self) { tag in
                                Text(tag)
                                    .font(.caption)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 4)
                                    .background(Color(.systemGray6))
                                    .clipShape(Capsule())
                            }
                        }
                    }
                    
                    // Occasions
                    if !place.occasions.isEmpty {
                        VStack(alignment: .trailing, spacing: 4) {
                            Text("مناسب لـ")
                                .font(.headline)
                            HStack(spacing: 8) {
                                ForEach(place.occasions) { occ in
                                    HStack(spacing: 4) {
                                        Text(occ.emoji)
                                        Text(occ.nameAr).font(.caption)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Theme.primary.opacity(0.1))
                                    .clipShape(Capsule())
                                }
                            }
                        }
                    }
                    
                    // Map Preview
                    if let coord = place.coordinate {
                        Map(position: .constant(.region(MKCoordinateRegion(
                            center: coord,
                            span: MKCoordinateSpan(latitudeDelta: 0.005, longitudeDelta: 0.005)
                        )))) {
                            Marker(place.nameAr, coordinate: coord)
                        }
                        .frame(height: 150)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .disabled(true)
                    }
                }
                .padding()
            }
        }
        .navigationBarTitleDisplayMode(.inline)
    }
    
    // MARK: - Info Section
    
    private var infoSection: some View {
        VStack(spacing: 8) {
            if let hood = place.neighborhood {
                InfoRow(icon: "mappin", label: "الحي", value: hood)
            }
            if let price = place.priceLevel {
                InfoRow(icon: "banknote", label: "السعر", value: price)
            }
            if let hours = place.openingHours {
                InfoRow(icon: "clock", label: "الأوقات", value: hours)
            }
            if let phone = place.phone {
                Button {
                    if let url = URL(string: "tel://\(phone.replacingOccurrences(of: " ", with: ""))") {
                        UIApplication.shared.open(url)
                    }
                } label: {
                    InfoRow(icon: "phone", label: "اتصال", value: phone)
                }
            }
            if let address = place.address {
                InfoRow(icon: "location", label: "العنوان", value: address)
            }
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
    
    // MARK: - Actions
    
    private func toggleFavorite() {
        if let existing = favorites.first(where: { $0.placeId == place.id }) {
            modelContext.delete(existing)
        } else {
            modelContext.insert(CachedFavorite(placeId: place.id))
        }
    }
    
    private func sharePlace() {
        // TODO: UIActivityViewController
    }
    
    private func openInMaps() {
        if let urlStr = place.googleMapsUrl, let url = URL(string: urlStr) {
            UIApplication.shared.open(url)
        } else if let coord = place.coordinate {
            let url = URL(string: "https://maps.google.com/?q=\(coord.latitude),\(coord.longitude)")!
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - Info Row

struct InfoRow: View {
    let icon: String
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(value)
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Spacer()
            HStack(spacing: 4) {
                Text(label)
                    .font(.subheadline)
                Image(systemName: icon)
                    .foregroundStyle(Theme.primary)
            }
        }
    }
}

// MARK: - Flow Layout

struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = arrange(proposal: proposal, subviews: subviews)
        return result.size
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = arrange(proposal: ProposedViewSize(width: bounds.width, height: bounds.height), subviews: subviews)
        for (index, position) in result.positions.enumerated() {
            subviews[index].place(at: CGPoint(x: bounds.minX + position.x, y: bounds.minY + position.y), proposal: .unspecified)
        }
    }
    
    private func arrange(proposal: ProposedViewSize, subviews: Subviews) -> (size: CGSize, positions: [CGPoint]) {
        var positions: [CGPoint] = []
        var x: CGFloat = 0
        var y: CGFloat = 0
        var maxHeight: CGFloat = 0
        let maxWidth = proposal.width ?? .infinity
        
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > maxWidth, x > 0 {
                x = 0
                y += maxHeight + spacing
                maxHeight = 0
            }
            positions.append(CGPoint(x: x, y: y))
            maxHeight = max(maxHeight, size.height)
            x += size.width + spacing
        }
        
        return (CGSize(width: maxWidth, height: y + maxHeight), positions)
    }
}
