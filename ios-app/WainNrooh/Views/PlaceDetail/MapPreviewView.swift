// MapPreviewView.swift
// خريطة مصغرة في تفاصيل المكان

import SwiftUI
import MapKit

struct MapPreviewView: View {
    let coordinate: CLLocationCoordinate2D
    let name: String
    let height: CGFloat
    
    init(coordinate: CLLocationCoordinate2D, name: String, height: CGFloat = 150) {
        self.coordinate = coordinate
        self.name = name
        self.height = height
    }
    
    var body: some View {
        Map(position: .constant(.region(MKCoordinateRegion(
            center: coordinate,
            span: MKCoordinateSpan(latitudeDelta: 0.005, longitudeDelta: 0.005)
        )))) {
            Marker(name, coordinate: coordinate)
        }
        .frame(height: height)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .disabled(true)
        .onTapGesture {
            openInMaps()
        }
    }
    
    private func openInMaps() {
        let url = URL(string: "https://maps.google.com/?q=\(coordinate.latitude),\(coordinate.longitude)")!
        UIApplication.shared.open(url)
    }
}
