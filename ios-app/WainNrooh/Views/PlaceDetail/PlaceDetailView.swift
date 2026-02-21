// PlaceDetailView.swift
// صفحة تفاصيل المكان — هوية ليالي الرياض
// Hero image + معلومات + أزرار إجراء

import SwiftUI
import MapKit

struct PlaceDetailView: View {
    let place: Place
    @EnvironmentObject var appState: AppState
    @Environment(\.dismiss) private var dismiss
    @State private var showShareSheet = false
    
    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack(spacing: 0) {
                // الصورة الرئيسية
                heroSection
                
                // المعلومات
                VStack(alignment: .trailing, spacing: Theme.spacingXL) {
                    // الاسم + التقييم
                    nameAndRating
                    
                    // معلومات سريعة
                    quickInfo
                    
                    // الأوصاف
                    if let desc = place.descriptionAr, !desc.isEmpty {
                        descriptionSection(desc)
                    }
                    
                    // Tags
                    if let tags = place.tags, !tags.isEmpty {
                        tagsSection(tags)
                    }
                    
                    // مناسب لـ
                    if let perfectFor = place.perfectFor, !perfectFor.isEmpty {
                        perfectForSection(perfectFor)
                    }
                    
                    // الموقع على الخريطة
                    if let lat = place.lat, let lng = place.lng {
                        mapSection(lat: lat, lng: lng)
                    }
                    
                    // أزرار الإجراء
                    actionButtons
                    
                    Spacer(minLength: 100)
                }
                .padding(Theme.spacingL)
            }
        }
        .background(Color.appBackground)
        .ignoresSafeArea(edges: .top)
        .navigationBarHidden(true)
    }
    
    // MARK: - الصورة الرئيسية
    
    private var heroSection: some View {
        ZStack(alignment: .top) {
            // خلفية
            ZStack {
                Theme.green700
                
                Image(systemName: categoryIcon)
                    .font(.system(size: 60))
                    .foregroundStyle(Theme.green400.opacity(0.15))
            }
            .frame(height: Theme.heroHeight)
            
            // تدرج
            Theme.heroGradient
                .frame(height: Theme.heroHeight)
            
            // أزرار التنقل
            HStack {
                // مشاركة
                Button {
                    showShareSheet = true
                } label: {
                    Image(systemName: "square.and.arrow.up")
                        .navButtonStyle()
                }
                
                // مفضلة
                Button {
                    withAnimation(Theme.animSpring) {
                        appState.toggleFavorite(place.id)
                    }
                } label: {
                    Image(systemName: appState.isFavorite(place.id) ? "heart.fill" : "heart")
                        .navButtonStyle()
                        .foregroundStyle(appState.isFavorite(place.id) ? Theme.error : .white)
                }
                
                Spacer()
                
                // رجوع
                Button {
                    dismiss()
                } label: {
                    Image(systemName: "chevron.right")
                        .navButtonStyle()
                }
            }
            .padding(.horizontal, Theme.spacingL)
            .padding(.top, 56) // safe area
        }
    }
    
    // MARK: - الاسم + التقييم
    
    private var nameAndRating: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingS) {
            // الاسم العربي
            Text(place.nameAr)
                .font(Theme.title())
                .foregroundStyle(.appTextPrimary)
            
            // الاسم الإنقليزي
            if let nameEn = place.nameEn, !nameEn.isEmpty {
                Text(nameEn)
                    .font(Theme.detail())
                    .foregroundStyle(.appTextSecondary)
            }
            
            // سطر التقييم
            HStack(spacing: Theme.spacingM) {
                // حالة المكان
                if let hours = place.openingHours, !hours.isEmpty {
                    Text("مفتوح")
                        .font(Theme.badge())
                        .foregroundStyle(Theme.success)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(Theme.success.opacity(0.1))
                        .clipShape(Capsule())
                }
                
                Spacer()
                
                // السعر
                if let price = place.priceLevel {
                    Text(price)
                        .font(Theme.body().bold())
                        .foregroundStyle(Theme.gold500)
                }
                
                // التقييم
                if let rating = place.googleRating {
                    HStack(spacing: 4) {
                        Text(String(format: "%.1f", rating))
                            .font(Theme.headline())
                            .foregroundStyle(.appTextPrimary)
                        
                        Image(systemName: "star.fill")
                            .font(.system(size: 14))
                            .foregroundStyle(Theme.gold500)
                    }
                }
            }
        }
    }
    
    // MARK: - معلومات سريعة
    
    private var quickInfo: some View {
        VStack(spacing: Theme.spacingM) {
            // الحي
            if let hood = place.neighborhood, !hood.isEmpty {
                infoRow(icon: "mappin.circle.fill", text: hood, color: Theme.green400)
            }
            
            // العنوان
            if let address = place.address, !address.isEmpty {
                infoRow(icon: "location.fill", text: address, color: Theme.sand)
            }
            
            // ساعات العمل
            if let hours = place.openingHours, !hours.isEmpty {
                infoRow(icon: "clock.fill", text: hours, color: Theme.info)
            }
            
            // رقم الهاتف
            if let phone = place.phone, !phone.isEmpty {
                Button {
                    if let url = URL(string: "tel://\(phone)") {
                        UIApplication.shared.open(url)
                    }
                } label: {
                    infoRow(icon: "phone.fill", text: phone, color: Theme.green400)
                }
            }
        }
        .padding(Theme.spacingL)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
    }
    
    private func infoRow(icon: String, text: String, color: Color) -> some View {
        HStack(spacing: Theme.spacingM) {
            Text(text)
                .font(Theme.detail())
                .foregroundStyle(.appTextPrimary)
                .multilineTextAlignment(.trailing)
            
            Spacer()
            
            Image(systemName: icon)
                .font(.system(size: 16))
                .foregroundStyle(color)
                .frame(width: 32, height: 32)
                .background(color.opacity(0.1))
                .clipShape(Circle())
        }
    }
    
    // MARK: - الوصف
    
    private func descriptionSection(_ text: String) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingS) {
            Text("عن المكان")
                .font(Theme.headline(size: 16))
                .foregroundStyle(.appTextPrimary)
            
            Text(text)
                .font(Theme.detail())
                .foregroundStyle(.appTextSecondary)
                .multilineTextAlignment(.trailing)
                .lineSpacing(4)
        }
    }
    
    // MARK: - Tags
    
    private func tagsSection(_ tags: [String]) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingS) {
            Text("الوسوم")
                .font(Theme.headline(size: 16))
                .foregroundStyle(.appTextPrimary)
            
            FlowLayout(spacing: Theme.spacingS) {
                ForEach(tags, id: \.self) { tag in
                    Text(tag)
                        .wainGlassPill()
                }
            }
        }
    }
    
    // MARK: - مناسب لـ
    
    private func perfectForSection(_ items: [String]) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingS) {
            Text("مناسب لـ")
                .font(Theme.headline(size: 16))
                .foregroundStyle(.appTextPrimary)
            
            FlowLayout(spacing: Theme.spacingS) {
                ForEach(items, id: \.self) { item in
                    HStack(spacing: 4) {
                        Text(item)
                        Image(systemName: "checkmark.circle.fill")
                            .font(.system(size: 10))
                            .foregroundStyle(Theme.green400)
                    }
                    .font(Theme.badge(size: 12))
                    .foregroundStyle(Theme.green300)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 5)
                    .background(Theme.green400.opacity(0.08))
                    .clipShape(Capsule())
                }
            }
        }
    }
    
    // MARK: - الخريطة
    
    private func mapSection(lat: Double, lng: Double) -> some View {
        VStack(alignment: .trailing, spacing: Theme.spacingS) {
            Text("الموقع")
                .font(Theme.headline(size: 16))
                .foregroundStyle(.appTextPrimary)
            
            Map(initialPosition: .region(
                MKCoordinateRegion(
                    center: CLLocationCoordinate2D(latitude: lat, longitude: lng),
                    span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                )
            )) {
                Marker(place.nameAr, coordinate: CLLocationCoordinate2D(latitude: lat, longitude: lng))
                    .tint(Theme.green400)
            }
            .frame(height: 200)
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
            .allowsHitTesting(false)
            
            // زر فتح الخريطة
            if let mapsUrl = place.googleMapsUrl, let url = URL(string: mapsUrl) {
                Button {
                    UIApplication.shared.open(url)
                } label: {
                    HStack {
                        Text("ودّني هناك")
                            .font(Theme.headline(size: 16))
                        Image(systemName: "arrow.up.left.circle.fill")
                    }
                    .frame(maxWidth: .infinity)
                    .wainPrimaryButton()
                }
            }
        }
    }
    
    // MARK: - أزرار الإجراء
    
    private var actionButtons: some View {
        VStack(spacing: Theme.spacingM) {
            // اسأل الذكاء
            NavigationLink {
                AIChatView(initialPlace: place)
            } label: {
                HStack {
                    Text("اسأل الذكاء عن هالمكان")
                        .font(Theme.headline(size: 15))
                    Image(systemName: "sparkles")
                }
                .frame(maxWidth: .infinity)
                .wainSecondaryButton()
            }
        }
    }
    
    // MARK: - أيقونة الفئة
    
    private var categoryIcon: String {
        switch place.category {
        case "restaurants", "مطاعم": return "fork.knife"
        case "cafes", "كافيهات": return "cup.and.saucer.fill"
        case "entertainment", "ترفيه": return "sparkles"
        case "shopping", "تسوق": return "bag.fill"
        case "hotels", "فنادق": return "bed.double.fill"
        case "nature", "طبيعة": return "leaf.fill"
        case "desserts", "حلويات": return "birthday.cake.fill"
        case "chalets", "شاليهات": return "house.lodge.fill"
        case "malls", "مولات": return "building.2.fill"
        case "museums", "متاحف": return "building.columns.fill"
        case "events", "فعاليات": return "party.popper.fill"
        default: return "mappin.circle.fill"
        }
    }
}

// MARK: - Nav Button Style

extension View {
    func navButtonStyle() -> some View {
        self
            .font(.system(size: 16, weight: .semibold))
            .foregroundStyle(.white)
            .frame(width: 40, height: 40)
            .background(.ultraThinMaterial)
            .clipShape(Circle())
    }
}

// MARK: - Flow Layout (للـ Tags)

struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = arrange(proposal: proposal, subviews: subviews)
        return result.size
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = arrange(proposal: ProposedViewSize(width: bounds.width, height: bounds.height), subviews: subviews)
        for (index, position) in result.positions.enumerated() {
            subviews[index].place(at: CGPoint(x: bounds.maxX - position.x, y: bounds.minY + position.y), anchor: .topTrailing, proposal: .unspecified)
        }
    }
    
    private func arrange(proposal: ProposedViewSize, subviews: Subviews) -> (size: CGSize, positions: [CGPoint]) {
        let maxWidth = proposal.width ?? .infinity
        var positions: [CGPoint] = []
        var currentX: CGFloat = 0
        var currentY: CGFloat = 0
        var lineHeight: CGFloat = 0
        
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if currentX + size.width > maxWidth, currentX > 0 {
                currentX = 0
                currentY += lineHeight + spacing
                lineHeight = 0
            }
            positions.append(CGPoint(x: currentX + size.width, y: currentY))
            currentX += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }
        
        return (CGSize(width: maxWidth, height: currentY + lineHeight), positions)
    }
}
