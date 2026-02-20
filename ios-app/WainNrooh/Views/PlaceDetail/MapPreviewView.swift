// MapPreviewView.swift
// خريطة مصغرة — MapKit mini map

import SwiftUI
import MapKit

// MARK: - خريطة مصغرة

/// خريطة مصغرة تعرض موقع المكان
struct MapPreviewView: View {
    let coordinate: CLLocationCoordinate2D
    let title: String
    
    @State private var cameraPosition: MapCameraPosition
    
    init(coordinate: CLLocationCoordinate2D, title: String) {
        self.coordinate = coordinate
        self.title = title
        _cameraPosition = State(initialValue: .region(MKCoordinateRegion(
            center: coordinate,
            span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
        )))
    }
    
    var body: some View {
        Map(position: $cameraPosition, interactionModes: []) {
            // علامة المكان
            Annotation(title, coordinate: coordinate) {
                ZStack {
                    Circle()
                        .fill(Theme.primary)
                        .frame(width: 32, height: 32)
                    
                    Image(systemName: "mappin.circle.fill")
                        .font(.system(size: 20))
                        .foregroundStyle(.white)
                }
                .shadow(radius: 3)
            }
        }
        .mapStyle(.standard(elevation: .realistic))
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusMedium))
        .overlay(
            // زر "افتح بالخرائط"
            VStack {
                Spacer()
                HStack {
                    Label("افتح بالخرائط", systemImage: "arrow.up.right.square")
                        .font(Theme.captionFont(size: 11))
                        .foregroundStyle(.white)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(.ultraThinMaterial)
                        .clipShape(Capsule())
                    Spacer()
                }
                .padding(8)
            }
        )
    }
}

// MARK: - Preview

#Preview {
    MapPreviewView(
        coordinate: CLLocationCoordinate2D(latitude: 24.7136, longitude: 46.6753),
        title: "كافيه المعمار"
    )
    .frame(height: 200)
    .padding()
}
