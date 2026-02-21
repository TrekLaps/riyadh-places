# APP Features Blueprint — وين نروح بالرياض
**Version:** 1.0 | **Date:** 2026-02-21 | **Source:** تحليل 20 تطبيق عالمي ومحلي

---

## Executive Summary

حللنا 20 تطبيق (5 سعودي/خليجي، 5 شرق آسيوي، 5 كوري/ياباني، 5 غربي) واستخرجنا أفضل 3 ميزات من كل واحد مع خطة تطبيق عملية لـ "وين نروح". الميزات مرتبة حسب الأولوية (MVP / Phase 2 / Phase 3) مع تقديرات ساعات التطوير والـ dependencies.

**إجمالي الميزات المستخلصة:** 60 ميزة → تم تصفيتها إلى **28 ميزة قابلة للتطبيق**
**إجمالي ساعات التطوير التقديرية:** ~185 ساعة (MVP: 42h | Phase 2: 68h | Phase 3: 75h)

---

## 📊 Feature Priority Matrix

| الأولوية | عدد الميزات | الساعات | النسبة |
|----------|------------|---------|--------|
| 🔴 MVP (Phase 1) | 10 | ~42h | أول أسبوعين |
| 🟡 Phase 2 | 10 | ~68h | أسبوع 3-6 |
| 🟢 Phase 3 | 8 | ~75h | شهر 2-3 |

---

## 🇸🇦 Saudi/Gulf Apps (5)

---

### 1. HungerStation — Super App Pattern ⭐⭐⭐

**لماذا مهم:** أنجح super app سعودي. 14M+ تحميل. Architecture خفيف ومودولار.

#### Feature 1: Modular Tab Architecture (Lazy Loading)
- **الأولوية:** 🔴 MVP
- **ساعات:** 3h
- **الوصف:** كل tab يحمّل بشكل مستقل. المستخدم يشوف المحتوى فوراً بدون ما ينتظر كل الأقسام تحمّل.

```swift
// PATTERN: Lazy Tab Loading (HungerStation-inspired)
struct MainTabView: View {
    @State private var selectedTab: AppTab = .home
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // Each tab loads only when selected
            LazyView(HomeView())
                .tabItem { Label("الرئيسية", systemImage: "house.fill") }
                .tag(AppTab.home)
            
            LazyView(ExploreView())
                .tabItem { Label("استكشف", systemImage: "safari.fill") }
                .tag(AppTab.explore)
            
            LazyView(MapTabView())
                .tabItem { Label("الخريطة", systemImage: "map.fill") }
                .tag(AppTab.map)
            
            LazyView(FavoritesView())
                .tabItem { Label("المفضلة", systemImage: "heart.fill") }
                .tag(AppTab.favorites)
        }
        .environment(\.layoutDirection, .rightToLeft)
    }
}

// Lazy wrapper — doesn't init body until visible
struct LazyView<Content: View>: View {
    let build: () -> Content
    init(_ build: @autoclosure @escaping () -> Content) {
        self.build = build
    }
    var body: Content { build() }
}

enum AppTab: Hashable {
    case home, explore, map, favorites
}
```

- **Dependencies:** None (pure SwiftUI)

#### Feature 2: Category Cards with Quick Actions
- **الأولوية:** 🔴 MVP
- **ساعات:** 2h
- **الوصف:** Grid بطاقات للفئات (كافيهات، مطاعم، حلويات...) مع أيقونات واضحة وأرقام.

```swift
// DATA MODEL
struct PlaceCategory: Identifiable, Hashable {
    let id: String
    let nameAr: String
    let nameEn: String
    let icon: String        // SF Symbol
    let color: Color
    let count: Int
    
    static let allCategories: [PlaceCategory] = [
        .init(id: "cafe", nameAr: "كافيهات", nameEn: "Cafes", 
              icon: "cup.and.saucer.fill", color: .brown, count: 0),
        .init(id: "restaurant", nameAr: "مطاعم", nameEn: "Restaurants",
              icon: "fork.knife", color: .orange, count: 0),
        // ... 25 categories
    ]
}

// VIEW
struct CategoryGridView: View {
    let categories: [PlaceCategory]
    let columns = Array(repeating: GridItem(.flexible(), spacing: 12), count: 3)
    
    var body: some View {
        LazyVGrid(columns: columns, spacing: 12) {
            ForEach(categories) { cat in
                NavigationLink(value: cat) {
                    CategoryCard(category: cat)
                }
            }
        }
    }
}

struct CategoryCard: View {
    let category: PlaceCategory
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: category.icon)
                .font(.title2)
                .foregroundStyle(category.color)
            Text(category.nameAr)
                .font(.caption)
                .fontWeight(.medium)
            Text("\(category.count)")
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 16)
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
```

- **Dependencies:** None

#### Feature 3: Lightweight Data Loading (Progressive)
- **الأولوية:** 🔴 MVP
- **ساعات:** 4h
- **الوصف:** مثل HungerStation — يحمّل أول 20 نتيجة فوراً، وباقي الداتا بالتمرير (infinite scroll).

```swift
// VIEWMODEL: Progressive Loading
@Observable
class PlaceListViewModel {
    private let repository: PlaceRepository
    
    var places: [CachedPlace] = []
    var isLoading = false
    var hasMore = true
    private var currentPage = 0
    private let pageSize = 20
    
    func loadNextPage() async {
        guard !isLoading, hasMore else { return }
        isLoading = true
        defer { isLoading = false }
        
        let newPlaces = await repository.fetchPlaces(
            page: currentPage,
            limit: pageSize
        )
        
        if newPlaces.count < pageSize { hasMore = false }
        places.append(contentsOf: newPlaces)
        currentPage += 1
    }
    
    func loadMore(currentItem: CachedPlace) async {
        // Trigger when user reaches last 5 items
        guard let index = places.firstIndex(where: { $0.id == currentItem.id }),
              index >= places.count - 5 else { return }
        await loadNextPage()
    }
}
```

- **Dependencies:** SwiftData, Repository Protocol

---

### 2. Jahez — Fast Discovery Pattern

**لماذا مهم:** أسرع تطبيق سعودي بالـ UX. بساطة مبالغ فيها = تحويل عالي.

#### Feature 1: Instant Category Switching (Horizontal Scroll)
- **الأولوية:** 🔴 MVP
- **ساعات:** 2h
- **الوصف:** شريط أفقي فوق القائمة يتيح التبديل السريع بين الفئات بدون تحميل صفحة جديدة.

```swift
struct CategoryPillBar: View {
    @Binding var selectedCategory: String?
    let categories: [PlaceCategory]
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                PillButton(title: "الكل", isSelected: selectedCategory == nil) {
                    selectedCategory = nil
                }
                ForEach(categories) { cat in
                    PillButton(
                        title: cat.nameAr,
                        isSelected: selectedCategory == cat.id
                    ) {
                        withAnimation(.snappy) { selectedCategory = cat.id }
                    }
                }
            }
            .padding(.horizontal)
        }
    }
}

struct PillButton: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(isSelected ? .bold : .regular)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(isSelected ? Color.accentColor : Color(.systemGray6))
                .foregroundStyle(isSelected ? .white : .primary)
                .clipShape(Capsule())
        }
    }
}
```

- **Dependencies:** None

#### Feature 2: Place Preview Card (Rich Info)
- **الأولوية:** 🔴 MVP
- **ساعات:** 3h

```swift
struct PlacePreviewCard: View {
    let place: CachedPlace
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 8) {
            // Cover image with async loading
            AsyncImage(url: URL(string: place.coverImageUrl ?? "")) { phase in
                switch phase {
                case .success(let image):
                    image.resizable().aspectRatio(16/9, contentMode: .fill)
                case .failure:
                    PlaceholderImage(category: place.category)
                default:
                    ShimmerView()
                }
            }
            .frame(height: 160)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            
            VStack(alignment: .trailing, spacing: 4) {
                HStack {
                    // Tags
                    if place.isNew { TagBadge(text: "جديد", color: .green) }
                    if place.isTrending { TagBadge(text: "رائج", color: .orange) }
                    Spacer()
                    // Rating
                    HStack(spacing: 2) {
                        Text(String(format: "%.1f", place.googleRating))
                            .font(.caption).bold()
                        Image(systemName: "star.fill")
                            .font(.caption2)
                            .foregroundStyle(.yellow)
                    }
                }
                
                Text(place.nameAr)
                    .font(.headline)
                    .lineLimit(1)
                
                HStack {
                    if let price = place.priceRange {
                        Text(price).font(.caption).foregroundStyle(.secondary)
                    }
                    Spacer()
                    if let neighborhood = place.neighborhood {
                        Label(neighborhood, systemImage: "mappin")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }
            }
            .padding(.horizontal, 4)
        }
    }
}
```

- **Dependencies:** AsyncImage (built-in iOS 15+)

#### Feature 3: One-Tap Navigation to Google Maps
- **الأولوية:** 🔴 MVP
- **ساعات:** 1h

```swift
struct NavigationButton: View {
    let place: CachedPlace
    
    var body: some View {
        Button {
            openInGoogleMaps()
        } label: {
            Label("توجّه", systemImage: "arrow.triangle.turn.up.right.diamond.fill")
                .font(.headline)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.accentColor)
                .foregroundStyle(.white)
                .clipShape(RoundedRectangle(cornerRadius: 12))
        }
    }
    
    private func openInGoogleMaps() {
        // Priority: Google Maps app → Apple Maps → Web
        if let gmURL = place.googleMapsUrl, let url = URL(string: gmURL) {
            UIApplication.shared.open(url)
        } else if let lat = place.latitude, let lng = place.longitude {
            let url = URL(string: "comgooglemaps://?daddr=\(lat),\(lng)&directionsmode=driving")!
            if UIApplication.shared.canOpenURL(url) {
                UIApplication.shared.open(url)
            } else {
                // Fallback to Apple Maps
                let appleURL = URL(string: "http://maps.apple.com/?daddr=\(lat),\(lng)")!
                UIApplication.shared.open(appleURL)
            }
        }
    }
}
```

- **Dependencies:** Google Maps URL scheme in Info.plist `LSApplicationQueriesSchemes`

---

### 3. Keeta (Meituan Saudi) — Visual-First Discovery

**لماذا مهم:** تطبيق صيني دخل السوق السعودي بتصميم visual-first يستهدف الشباب.

#### Feature 1: Visual Carousel for Trending Places
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h
- **الوصف:** كاروسيل كبير بالصفحة الرئيسية يعرض الأماكن الرائجة بصور كبيرة.

```swift
struct TrendingCarousel: View {
    let trendingPlaces: [CachedPlace]
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            LazyHStack(spacing: 16) {
                ForEach(trendingPlaces.prefix(10)) { place in
                    NavigationLink(value: place) {
                        TrendingCard(place: place)
                    }
                }
            }
            .padding(.horizontal)
            .scrollTargetLayout()
        }
        .scrollTargetBehavior(.viewAligned)
    }
}

struct TrendingCard: View {
    let place: CachedPlace
    
    var body: some View {
        ZStack(alignment: .bottomTrailing) {
            AsyncImage(url: URL(string: place.coverImageUrl ?? "")) { image in
                image.resizable().aspectRatio(3/4, contentMode: .fill)
            } placeholder: {
                ShimmerView()
            }
            .frame(width: 200, height: 280)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            
            VStack(alignment: .trailing) {
                Text(place.nameAr)
                    .font(.headline)
                    .foregroundStyle(.white)
                Text(place.neighborhood ?? "")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.8))
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .trailing)
            .background(.linearGradient(
                colors: [.clear, .black.opacity(0.7)],
                startPoint: .top, endPoint: .bottom
            ))
        }
        .frame(width: 200, height: 280)
    }
}
```

- **Dependencies:** AsyncImage, ScrollTargetBehavior (iOS 17+)

#### Feature 2: Delivery Price Comparison Badge
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h

```swift
// DATA MODEL
struct DeliveryPrice: Codable, Identifiable {
    let id: String // UUID
    let placeId: String
    let platform: DeliveryPlatform
    let deliveryFee: Double
    let minimumOrder: Double?
    let estimatedMinutes: Int?
    let lastUpdated: Date
}

enum DeliveryPlatform: String, Codable, CaseIterable {
    case hungerStation = "hunger_station"
    case jahez = "jahez"
    case keeta = "keeta"
    case toYou = "toyou"
    case careem = "careem"
    case marsool = "marsool"
    case theChefz = "thechefz"
    case mrsool = "mrsool"
    
    var displayName: String {
        switch self {
        case .hungerStation: "هنقرستيشن"
        case .jahez: "جاهز"
        case .keeta: "كيتا"
        case .toYou: "تويو"
        case .careem: "كريم"
        case .marsool: "مرسول"
        case .theChefz: "ذا شفز"
        case .mrsool: "مرسول"
        }
    }
    
    var color: Color {
        switch self {
        case .hungerStation: .purple
        case .jahez: .red
        case .keeta: .yellow
        case .toYou: .blue
        case .careem: .green
        case .marsool: .orange
        case .theChefz: .brown
        case .mrsool: .pink
        }
    }
}
```

- **Dependencies:** DeliveryPrice data (Phase 2 data collection)

#### Feature 3: Quick Filters with Visual Tags
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h

- **Dependencies:** Filter models, extended place metadata

---

### 4. Entertainer — Deals & Offers Pattern

**لماذا مهم:** 2M+ users بالخليج. نموذج العروض والخصومات (BOGOF) ناجح جداً.

#### Feature 1: "Perfect For" Smart Labels
- **الأولوية:** 🔴 MVP
- **ساعات:** 2h
- **الوصف:** labels ذكية (مثالي للعائلات، رومانسي، عمل، أطفال) من بيانات المكان.

```swift
struct PerfectForView: View {
    let tags: [String] // من place.perfectFor
    
    var body: some View {
        FlowLayout(spacing: 8) {
            ForEach(tags, id: \.self) { tag in
                HStack(spacing: 4) {
                    Image(systemName: iconFor(tag))
                        .font(.caption2)
                    Text(tag)
                        .font(.caption)
                }
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .background(Color.accentColor.opacity(0.1))
                .foregroundStyle(Color.accentColor)
                .clipShape(Capsule())
            }
        }
    }
    
    private func iconFor(_ tag: String) -> String {
        switch tag {
        case "عائلات": return "figure.2.and.child"
        case "رومانسي": return "heart.fill"
        case "عمل": return "briefcase.fill"
        case "أصدقاء": return "person.3.fill"
        case "أطفال": return "figure.and.child.holdinghands"
        case "هادي": return "leaf.fill"
        default: return "star.fill"
        }
    }
}
```

- **Dependencies:** `perfectFor` field in places.json

#### Feature 2: Nearby Places (Location-Based)
- **الأولوية:** 🔴 MVP
- **ساعات:** 3h

```swift
@Observable
class NearbyViewModel {
    private let locationService: LocationService
    private let repository: PlaceRepository
    
    var nearbyPlaces: [CachedPlace] = []
    var isLoadingLocation = false
    
    func loadNearby() async {
        isLoadingLocation = true
        defer { isLoadingLocation = false }
        
        guard let location = await locationService.getCurrentLocation() else { return }
        
        nearbyPlaces = await repository.fetchPlaces(
            near: location.coordinate,
            radiusKm: 3.0,
            limit: 20,
            sortBy: .distance
        )
    }
}
```

- **Dependencies:** CoreLocation, lat/lng in data

#### Feature 3: Share Place Card (Visual)
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h

```swift
// Generate shareable image card
struct ShareCardGenerator {
    @MainActor
    static func generateCard(for place: CachedPlace) -> UIImage {
        let renderer = ImageRenderer(content: ShareCardView(place: place))
        renderer.scale = 3.0 // Retina
        return renderer.uiImage ?? UIImage()
    }
}

struct ShareCardView: View {
    let place: CachedPlace
    var body: some View {
        VStack(spacing: 12) {
            Text(place.nameAr).font(.title2).bold()
            if let neighborhood = place.neighborhood {
                Text("📍 \(neighborhood)").font(.subheadline)
            }
            HStack {
                Text("⭐ \(String(format: "%.1f", place.googleRating))")
                if let price = place.priceRange { Text("💰 \(price)") }
            }
            Text("وين نروح بالرياض").font(.caption).foregroundStyle(.secondary)
        }
        .padding(24)
        .background(.ultraThickMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .frame(width: 350)
    }
}
```

- **Dependencies:** ImageRenderer (iOS 16+)

---

### 5. Careem — Super App Lite Navigation

**لماذا مهم:** Navigation pattern بسيط يخلي المستخدم يوصل لأي شي بأقل من 3 taps.

#### Feature 1: Search with Recent + Suggestions
- **الأولوية:** 🔴 MVP
- **ساعات:** 3h

```swift
@Observable
class SearchViewModel {
    private let searchService: SearchService
    private let repository: PlaceRepository
    
    var query = ""
    var results: [CachedPlace] = []
    var recentSearches: [String] = []
    var suggestions: [String] = ["كافيه هادي", "مطعم عائلي", "حلويات", "بخاري"]
    var isSearching = false
    
    func search() async {
        guard !query.trimmingCharacters(in: .whitespaces).isEmpty else {
            results = []
            return
        }
        isSearching = true
        defer { isSearching = false }
        
        results = await searchService.search(
            query: query.normalizedArabic,
            limit: 50
        )
        
        // Save to recents
        if !query.isEmpty && !recentSearches.contains(query) {
            recentSearches.insert(query, at: 0)
            if recentSearches.count > 10 { recentSearches.removeLast() }
            UserDefaults.standard.set(recentSearches, forKey: "recentSearches")
        }
    }
}
```

- **Dependencies:** SearchService

#### Feature 2: Bottom Sheet Discovery
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h
- **الوصف:** خريطة مع bottom sheet قابل للسحب (مثل Apple Maps / Careem) يعرض تفاصيل المكان.

```swift
struct MapWithBottomSheet: View {
    @State private var selectedPlace: CachedPlace?
    @State private var detent: PresentationDetent = .fraction(0.25)
    
    var body: some View {
        Map(/* ... */)
            .sheet(item: $selectedPlace) { place in
                PlaceBottomSheet(place: place)
                    .presentationDetents([.fraction(0.25), .medium, .large])
                    .presentationDragIndicator(.visible)
                    .presentationBackgroundInteraction(.enabled(upThrough: .medium))
            }
    }
}
```

- **Dependencies:** MapKit, iOS 16.4+

#### Feature 3: Quick Action Buttons
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 2h

- **Dependencies:** URL schemes for external apps

---

### 6. Gathern — Booking & Spaces Pattern

**لماذا مهم:** تطبيق سعودي لحجز الشاليهات والاستراحات. 2M+ مستخدم.

#### Feature 1: Operating Hours Smart Display
- **الأولوية:** 🔴 MVP
- **ساعات:** 2h

```swift
struct OpenStatusView: View {
    let hours: String? // "9:00-23:00" or complex format
    
    var isOpen: Bool {
        guard let hours else { return false }
        return HoursParser.isCurrentlyOpen(hours)
    }
    
    var body: some View {
        HStack(spacing: 4) {
            Circle()
                .fill(isOpen ? .green : .red)
                .frame(width: 8, height: 8)
            Text(isOpen ? "مفتوح الآن" : "مغلق")
                .font(.caption)
                .foregroundStyle(isOpen ? .green : .red)
            if let hours {
                Text("· \(hours)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
    }
}
```

- **Dependencies:** Hours parsing logic

#### Feature 2: Photo Gallery Grid
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 5h

- **Dependencies:** Image hosting, user uploads

#### Feature 3: Save to Collection
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h

- **Dependencies:** SwiftData collections model

---

## 🇯🇵 Japanese Apps (2)

---

### 7. Tabelog — Rating Algorithm ⭐⭐⭐⭐⭐

**لماذا مهم:** أدق نظام تقييم بالعالم. التقييم مبني على مصداقية المراجع مو بس العدد. Rating 3.5+ = ممتاز (مقابل 4.5+ في Google).

#### Feature 1: Weighted Trust Rating System
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 12h
- **الوصف:** نظام Tabelog الأساسي: التقييم الخام × وزن مصداقية المراجع = تقييم نهائي موزون

```swift
// DATA MODEL: Tabelog-Inspired Rating
struct TrustRating {
    let rawAverage: Double          // المعدل الخام
    let weightedScore: Double       // التقييم الموزون
    let totalReviews: Int
    let trustedReviewers: Int       // مراجعين موثوقين
    let confidenceLevel: ConfidenceLevel
    
    enum ConfidenceLevel: String {
        case low = "قليل"       // < 5 reviews
        case medium = "متوسط"   // 5-20 reviews
        case high = "عالي"      // 20+ reviews
    }
}

// ALGORITHM
struct TabelogRatingEngine {
    /// Tabelog-style weighted rating
    /// - reviewerTrust: 0.1 (new user) to 1.0 (established reviewer)
    /// - reviewAge: Recent reviews weigh more
    /// - reviewLength: Detailed reviews weigh more
    static func calculateWeightedRating(reviews: [UserReview]) -> TrustRating {
        guard !reviews.isEmpty else {
            return TrustRating(rawAverage: 0, weightedScore: 0,
                             totalReviews: 0, trustedReviewers: 0,
                             confidenceLevel: .low)
        }
        
        var totalWeight: Double = 0
        var weightedSum: Double = 0
        var trustedCount = 0
        
        for review in reviews {
            let trust = reviewerTrustScore(review.reviewer)
            let recency = recencyWeight(review.date)
            let detail = detailWeight(review.text)
            
            let weight = trust * recency * detail
            weightedSum += review.rating * weight
            totalWeight += weight
            
            if trust > 0.5 { trustedCount += 1 }
        }
        
        let weighted = totalWeight > 0 ? weightedSum / totalWeight : 0
        let raw = reviews.map(\.rating).reduce(0, +) / Double(reviews.count)
        
        let confidence: TrustRating.ConfidenceLevel = {
            if reviews.count < 5 { return .low }
            if reviews.count < 20 { return .medium }
            return .high
        }()
        
        return TrustRating(
            rawAverage: raw,
            weightedScore: weighted,
            totalReviews: reviews.count,
            trustedReviewers: trustedCount,
            confidenceLevel: confidence
        )
    }
    
    /// Anti-Fake Measures (Tabelog approach):
    /// 1. New accounts get low trust (0.1)
    /// 2. Accounts that only give 5.0 get flagged
    /// 3. Review must have minimum text length
    /// 4. Burst reviews (5+ from same IP/time) discarded
    /// 5. Rating variance check (accounts with only extreme ratings = suspicious)
    static func reviewerTrustScore(_ reviewer: ReviewerProfile) -> Double {
        var trust: Double = 0.3 // Base
        
        // Account age bonus
        let monthsOld = Calendar.current.dateComponents(
            [.month], from: reviewer.joinDate, to: Date()
        ).month ?? 0
        trust += min(Double(monthsOld) * 0.02, 0.2) // Max +0.2 for 10+ months
        
        // Review count bonus
        trust += min(Double(reviewer.totalReviews) * 0.01, 0.2) // Max +0.2
        
        // Rating distribution penalty
        if reviewer.averageRating > 4.8 || reviewer.averageRating < 1.5 {
            trust *= 0.5 // Suspicious extremes
        }
        
        // Review diversity bonus (reviews different places, not same owner)
        trust += min(Double(reviewer.uniquePlacesReviewed) * 0.01, 0.1)
        
        return min(trust, 1.0)
    }
    
    static func recencyWeight(_ date: Date) -> Double {
        let days = Calendar.current.dateComponents([.day], from: date, to: Date()).day ?? 0
        if days < 30 { return 1.0 }
        if days < 90 { return 0.9 }
        if days < 180 { return 0.7 }
        if days < 365 { return 0.5 }
        return 0.3
    }
    
    static func detailWeight(_ text: String) -> Double {
        let length = text.count
        if length > 200 { return 1.0 }
        if length > 100 { return 0.8 }
        if length > 50 { return 0.6 }
        return 0.4 // Very short reviews get less weight
    }
}
```

- **Dependencies:** User accounts (Supabase Auth), Reviews system

#### Feature 2: Rating Distribution Visualization
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 3h

```swift
struct RatingDistributionView: View {
    let distribution: [Int: Int] // star: count (e.g., [5: 45, 4: 30, ...])
    let totalReviews: Int
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 4) {
            ForEach((1...5).reversed(), id: \.self) { star in
                HStack(spacing: 8) {
                    Text("\(star)")
                        .font(.caption)
                        .frame(width: 16)
                    
                    GeometryReader { geo in
                        let count = distribution[star] ?? 0
                        let ratio = totalReviews > 0 ? CGFloat(count) / CGFloat(totalReviews) : 0
                        
                        RoundedRectangle(cornerRadius: 2)
                            .fill(Color.yellow)
                            .frame(width: geo.size.width * ratio)
                    }
                    .frame(height: 8)
                    
                    Text("\(distribution[star] ?? 0)")
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                        .frame(width: 30, alignment: .leading)
                }
            }
        }
    }
}
```

- **Dependencies:** Reviews data

#### Feature 3: Award Badges (Annual Best)
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 4h

- **Dependencies:** Rating system, enough data

---

### 8. Gurunavi — Rich Menu & Price Info

#### Feature 1: Menu Display with Prices
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 5h

```swift
struct MenuItem: Codable, Identifiable {
    let id: String
    let nameAr: String
    let nameEn: String?
    let price: Double
    let currency: String // "SAR"
    let category: String? // مشروبات، أطباق رئيسية
    let isPopular: Bool
    let imageUrl: String?
}

struct MenuView: View {
    let items: [MenuItem]
    
    var grouped: [String: [MenuItem]] {
        Dictionary(grouping: items, by: { $0.category ?? "أخرى" })
    }
    
    var body: some View {
        ForEach(Array(grouped.keys.sorted()), id: \.self) { category in
            Section(header: Text(category).font(.headline)) {
                ForEach(grouped[category] ?? []) { item in
                    MenuItemRow(item: item)
                }
            }
        }
    }
}
```

- **Dependencies:** Menu data (scraping/manual entry)

#### Feature 2: Price Range Indicator
- **الأولوية:** 🔴 MVP
- **ساعات:** 1h

```swift
struct PriceRangeView: View {
    let priceRange: String? // "$$" or "١-٥٠" or "50-150"
    
    var body: some View {
        if let price = priceRange {
            Text(price)
                .font(.caption)
                .padding(.horizontal, 8)
                .padding(.vertical, 2)
                .background(Color.green.opacity(0.1))
                .foregroundStyle(.green)
                .clipShape(Capsule())
        }
    }
}
```

- **Dependencies:** None

#### Feature 3: Cuisine Type Filters
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 2h

- **Dependencies:** Cuisine tags in data

---

## 🇨🇳 Chinese Apps (3)

---

### 9. Dianping — Hyperlocal Discovery ⭐⭐⭐⭐⭐

**لماذا مهم:** "أفضل 10 بالحي" — النموذج الأقوى للاكتشاف المحلي. 600M+ users بالصين. 

#### Feature 1: "أفضل 10 بالحي" (Neighborhood Top 10)
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 6h
- **الوصف:** لكل حي، قائمة أفضل 10 أماكن مرتبة بتقييم + شعبية. المستخدم يقدر يرى "أفضل 10 كافيهات في حي الملقا" فوراً.

```swift
// DATA MODEL
struct NeighborhoodRanking: Identifiable {
    let id: String // neighborhood_id + category
    let neighborhood: String
    let neighborhoodAr: String
    let category: String
    let categoryAr: String
    let topPlaces: [RankedPlace]
    let lastUpdated: Date
}

struct RankedPlace: Identifiable {
    let id: String
    let rank: Int
    let place: CachedPlace
    let score: Double // Composite score
    let highlights: [String] // "أجواء ممتازة", "قهوة مميزة"
}

// VIEWMODEL
@Observable
class NeighborhoodRankingViewModel {
    private let repository: PlaceRepository
    
    var rankings: [NeighborhoodRanking] = []
    
    /// Dianping Algorithm: Composite Score
    func calculateRanking(places: [CachedPlace], neighborhood: String, category: String) -> [RankedPlace] {
        let filtered = places.filter {
            $0.neighborhood == neighborhood && $0.category == category
        }
        
        return filtered
            .map { place in
                let score = compositeScore(place)
                return RankedPlace(
                    id: place.id,
                    rank: 0,
                    place: place,
                    score: score,
                    highlights: generateHighlights(place)
                )
            }
            .sorted { $0.score > $1.score }
            .prefix(10)
            .enumerated()
            .map { index, ranked in
                RankedPlace(id: ranked.id, rank: index + 1,
                           place: ranked.place, score: ranked.score,
                           highlights: ranked.highlights)
            }
    }
    
    /// Composite Score (Dianping-style):
    /// 40% rating + 25% review count + 20% completeness + 15% freshness
    private func compositeScore(_ place: CachedPlace) -> Double {
        let ratingScore = (place.googleRating / 5.0) * 40
        let reviewScore = min(Double(place.reviewCount ?? 0) / 100.0, 1.0) * 25
        let completeness = dataCompleteness(place) * 20
        let freshness = freshnessScore(place) * 15
        return ratingScore + reviewScore + completeness + freshness
    }
    
    private func dataCompleteness(_ place: CachedPlace) -> Double {
        var score = 0.0
        if place.phone != nil { score += 0.15 }
        if place.website != nil { score += 0.1 }
        if place.instagram != nil { score += 0.1 }
        if place.hours != nil { score += 0.15 }
        if place.coverImageUrl != nil { score += 0.2 }
        if place.descriptionAr != nil { score += 0.15 }
        if place.latitude != nil { score += 0.15 }
        return score
    }
}

// VIEW
struct NeighborhoodTopView: View {
    let ranking: NeighborhoodRanking
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 0) {
            // Header
            HStack {
                Image(systemName: "trophy.fill")
                    .foregroundStyle(.yellow)
                Text("أفضل 10 \(ranking.categoryAr) في \(ranking.neighborhoodAr)")
                    .font(.headline)
            }
            .padding()
            
            // List
            ForEach(ranking.topPlaces) { ranked in
                HStack(spacing: 12) {
                    // Rank badge
                    ZStack {
                        Circle()
                            .fill(rankColor(ranked.rank))
                            .frame(width: 32, height: 32)
                        Text("\(ranked.rank)")
                            .font(.callout.bold())
                            .foregroundStyle(.white)
                    }
                    
                    VStack(alignment: .trailing) {
                        Text(ranked.place.nameAr)
                            .font(.subheadline.bold())
                        HStack(spacing: 4) {
                            ForEach(ranked.highlights.prefix(2), id: \.self) { h in
                                Text(h)
                                    .font(.caption2)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.blue.opacity(0.1))
                                    .clipShape(Capsule())
                            }
                        }
                    }
                    
                    Spacer()
                    
                    Text(String(format: "%.1f", ranked.score))
                        .font(.title3.bold())
                        .foregroundStyle(.orange)
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                Divider()
            }
        }
    }
    
    func rankColor(_ rank: Int) -> Color {
        switch rank {
        case 1: .yellow
        case 2: .gray
        case 3: .brown
        default: .blue.opacity(0.7)
        }
    }
}
```

- **Dependencies:** Neighborhood + Category data, enough places per neighborhood

#### Feature 2: "أقرب لك الحين" (Real-time Nearby)
- **الأولوية:** 🔴 MVP
- **ساعات:** 3h (included in core nearby feature)

- **Dependencies:** CoreLocation

#### Feature 3: User Tips (Quick Reviews)
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 6h

- **Dependencies:** User accounts, moderation system

---

### 10. Meituan — Group Deals & Flash Sales

#### Feature 1: Time-Limited Deals Section
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 5h

```swift
struct DealCard: View {
    let deal: Deal
    @State private var timeRemaining: TimeInterval = 0
    
    var body: some View {
        VStack(alignment: .trailing) {
            // Countdown timer
            HStack {
                Image(systemName: "timer")
                Text(formatTime(timeRemaining))
                    .monospacedDigit()
                    .foregroundStyle(.red)
                Spacer()
                Text("خصم \(deal.discountPercent)%")
                    .font(.caption.bold())
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(.red)
                    .foregroundStyle(.white)
                    .clipShape(Capsule())
            }
            
            Text(deal.placeNameAr).font(.headline)
            Text(deal.description).font(.caption).foregroundStyle(.secondary)
        }
        .padding()
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
```

- **Dependencies:** Backend for deals, business partnerships

#### Feature 2: Multi-Category Search
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h

- **Dependencies:** Extended category system

#### Feature 3: User Photo Feed
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 8h

- **Dependencies:** Cloud storage, user accounts, moderation

---

### 11. Xiaohongshu (RED) — Social Discovery & UGC

**لماذا مهم:** 300M+ مستخدم. نموذج "notes" + اكتشاف = أقوى UGC platform.

#### Feature 1: Community Notes (Short Reviews + Photos)
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 10h
- **الوصف:** المستخدم يكتب "note" قصير عن تجربته + صور. يظهر كـ feed بصفحة المكان.

```swift
// DATA MODEL
struct PlaceNote: Codable, Identifiable {
    let id: String
    let placeId: String
    let authorId: String
    let authorName: String
    let authorAvatar: String?
    let text: String
    let images: [String] // URLs
    let rating: Double?
    let tags: [String] // "الأكل لذيذ", "الخدمة بطيئة"
    let likes: Int
    let createdAt: Date
}

// VIEW: Pinterest-style grid
struct NotesGridView: View {
    let notes: [PlaceNote]
    let columns = [GridItem(.flexible()), GridItem(.flexible())]
    
    var body: some View {
        LazyVGrid(columns: columns, spacing: 12) {
            ForEach(notes) { note in
                NoteCard(note: note)
            }
        }
    }
}
```

- **Dependencies:** User accounts, image upload, moderation, cloud storage

#### Feature 2: Interest-Based Feed Algorithm
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 8h

- **Dependencies:** User behavior tracking, recommendation engine

#### Feature 3: Save & Bookmark Collections
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h

```swift
// DATA MODEL
@Model
class PlaceCollection {
    @Attribute(.unique) var id: String
    var name: String
    var emoji: String
    var placeIds: [String]
    var isPublic: Bool
    var createdAt: Date
    
    init(name: String, emoji: String = "📌") {
        self.id = UUID().uuidString
        self.name = name
        self.emoji = emoji
        self.placeIds = []
        self.isPublic = false
        self.createdAt = Date()
    }
}

// VIEW
struct CollectionPickerView: View {
    let placeId: String
    @Query var collections: [PlaceCollection]
    @Environment(\.modelContext) var context
    
    var body: some View {
        List {
            ForEach(collections) { collection in
                Button {
                    togglePlace(in: collection)
                } label: {
                    HStack {
                        Text(collection.emoji)
                        Text(collection.name)
                        Spacer()
                        if collection.placeIds.contains(placeId) {
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundStyle(.green)
                        }
                    }
                }
            }
            
            Button("+ مجموعة جديدة") {
                let new = PlaceCollection(name: "مجموعة جديدة")
                new.placeIds.append(placeId)
                context.insert(new)
            }
        }
    }
    
    func togglePlace(in collection: PlaceCollection) {
        if let idx = collection.placeIds.firstIndex(of: placeId) {
            collection.placeIds.remove(at: idx)
        } else {
            collection.placeIds.append(placeId)
        }
    }
}
```

- **Dependencies:** SwiftData

---

## 🇰🇷 Korean Apps (3)

---

### 12. Naver Map — Smart Map UX

#### Feature 1: Map Cluster View with Place Count
- **الأولوية:** 🔴 MVP
- **ساعات:** 3h

```swift
import MapKit

struct ClusterMapView: View {
    let places: [CachedPlace]
    @State private var cameraPosition: MapCameraPosition = .region(
        MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 24.7136, longitude: 46.6753), // Riyadh
            span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
        )
    )
    
    var body: some View {
        Map(position: $cameraPosition) {
            ForEach(places.filter { $0.latitude != nil }) { place in
                Annotation(place.nameAr,
                          coordinate: CLLocationCoordinate2D(
                              latitude: place.latitude!,
                              longitude: place.longitude!
                          )) {
                    MapPin(place: place)
                }
            }
        }
        .mapStyle(.standard(pointsOfInterest: .excludingAll))
    }
}

struct MapPin: View {
    let place: CachedPlace
    
    var body: some View {
        VStack(spacing: 0) {
            ZStack {
                Circle()
                    .fill(categoryColor(place.category))
                    .frame(width: 36, height: 36)
                Image(systemName: categoryIcon(place.category))
                    .font(.caption)
                    .foregroundStyle(.white)
            }
            Triangle()
                .fill(categoryColor(place.category))
                .frame(width: 10, height: 6)
        }
    }
}
```

- **Dependencies:** MapKit

#### Feature 2: Place Info Overlay on Map
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h

- **Dependencies:** MapKit annotations

#### Feature 3: Route Planning (Multi-Stop)
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 6h

- **Dependencies:** MapKit directions

---

### 13. KakaoMap — Social + Map Integration

#### Feature 1: Share Location via Link
- **الأولوية:** 🔴 MVP
- **ساعات:** 2h

```swift
struct ShareHelper {
    static func sharePlace(_ place: CachedPlace) -> some View {
        ShareLink(
            item: placeURL(place),
            subject: Text(place.nameAr),
            message: Text("شوف هالمكان: \(place.nameAr) 📍")
        ) {
            Label("شارك", systemImage: "square.and.arrow.up")
        }
    }
    
    static func placeURL(_ place: CachedPlace) -> URL {
        // Link to web version or universal link
        URL(string: "https://wain-nrooh.com/place/\(place.id)")
            ?? URL(string: "https://wain-nrooh.com")!
    }
}
```

- **Dependencies:** Universal Links setup

#### Feature 2: "Friends Visited" Indicator
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 5h

- **Dependencies:** User accounts, social graph

#### Feature 3: AR Walking Directions
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 10h (complex)

- **Dependencies:** ARKit, CoreLocation

---

### 14. MangoPlate — Curated Lists

#### Feature 1: Curated "Best Of" Lists
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h

```swift
struct CuratedList: Codable, Identifiable {
    let id: String
    let title: String
    let subtitle: String
    let coverImageUrl: String
    let placeIds: [String]
    let author: String
    let publishDate: Date
    let tags: [String]
}

struct CuratedListCard: View {
    let list: CuratedList
    
    var body: some View {
        ZStack(alignment: .bottomTrailing) {
            AsyncImage(url: URL(string: list.coverImageUrl)) { image in
                image.resizable().aspectRatio(16/9, contentMode: .fill)
            } placeholder: {
                Color.gray.opacity(0.2)
            }
            .frame(height: 180)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            
            VStack(alignment: .trailing, spacing: 4) {
                Text(list.title)
                    .font(.headline)
                    .foregroundStyle(.white)
                Text("\(list.placeIds.count) مكان")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.8))
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .trailing)
            .background(.linearGradient(
                colors: [.clear, .black.opacity(0.8)],
                startPoint: .top, endPoint: .bottom
            ))
            .clipShape(RoundedRectangle(cornerRadius: 16))
        }
    }
}
```

- **Dependencies:** Editorial content creation

#### Feature 2: Food Type Classification
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 2h

- **Dependencies:** Cuisine/food tags in data

#### Feature 3: Verified Review Badge
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 3h

- **Dependencies:** Review verification system

---

## 🇪🇺 European Apps (2)

---

### 15. TheFork — Loyalty & Booking

#### Feature 1: Loyalty Points System ("نقاط")
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 8h
- **الوصف:** Yums-style نقاط. كل check-in = نقاط. اجمع نقاط = خصومات.

```swift
// DATA MODEL
struct LoyaltyAccount {
    let userId: String
    var points: Int
    var tier: LoyaltyTier
    var history: [PointTransaction]
    
    enum LoyaltyTier: String, Codable {
        case bronze = "برونزي"   // 0-500 points
        case silver = "فضي"     // 500-2000
        case gold = "ذهبي"      // 2000-5000
        case platinum = "بلاتيني" // 5000+
    }
}

struct PointTransaction: Codable, Identifiable {
    let id: String
    let type: TransactionType
    let points: Int
    let placeId: String?
    let date: Date
    
    enum TransactionType: String, Codable {
        case checkIn = "check_in"       // +10 points
        case review = "review"          // +25 points
        case photo = "photo"            // +15 points
        case referral = "referral"      // +100 points
        case redemption = "redemption"  // negative
    }
}
```

- **Dependencies:** User accounts, backend logic

#### Feature 2: Special Offers Section
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h

- **Dependencies:** Business partnerships

#### Feature 3: Reservation Integration
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 8h

- **Dependencies:** Restaurant API integrations

---

### 16. Mapstr — Personal Maps ⭐⭐⭐⭐

**لماذا مهم:** خريطتك الشخصية. حفظ، تنظيم، مشاركة، تصدير. 1M+ مستخدم.

#### Feature 1: Personal Map with Custom Tags
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 5h
- **الوصف:** المستخدم يحفظ أماكنه بتصنيفات خاصة ("زرته", "أبي أزوره", "موصى") مع ألوان وأيقونات.

```swift
// DATA MODEL
@Model
class PersonalPin {
    @Attribute(.unique) var id: String
    var placeId: String
    var customTag: String       // "زرته", "أبي أزوره", "موصى"
    var customEmoji: String     // "✅", "📌", "⭐"
    var customColor: String     // hex color
    var personalNote: String?
    var visitDate: Date?
    var rating: Double?         // Personal rating (separate from public)
    var photos: [String]        // Local photo references
    var createdAt: Date
    
    init(placeId: String, tag: String = "📌", emoji: String = "📌") {
        self.id = UUID().uuidString
        self.placeId = placeId
        self.customTag = tag
        self.customEmoji = emoji
        self.customColor = "#007AFF"
        self.createdAt = Date()
        self.photos = []
    }
}

// VIEW: Personal Map
struct PersonalMapView: View {
    @Query var pins: [PersonalPin]
    let allPlaces: [CachedPlace]
    @State private var selectedTag: String?
    
    var filteredPins: [PersonalPin] {
        if let tag = selectedTag {
            return pins.filter { $0.customTag == tag }
        }
        return Array(pins)
    }
    
    var uniqueTags: [String] {
        Array(Set(pins.map(\.customTag))).sorted()
    }
    
    var body: some View {
        VStack {
            // Tag filter
            ScrollView(.horizontal, showsIndicators: false) {
                HStack {
                    PillButton(title: "الكل (\(pins.count))",
                              isSelected: selectedTag == nil) {
                        selectedTag = nil
                    }
                    ForEach(uniqueTags, id: \.self) { tag in
                        let count = pins.filter { $0.customTag == tag }.count
                        PillButton(title: "\(tag) (\(count))",
                                  isSelected: selectedTag == tag) {
                            selectedTag = tag
                        }
                    }
                }
                .padding(.horizontal)
            }
            
            // Map with colored pins
            Map {
                ForEach(filteredPins) { pin in
                    if let place = allPlaces.first(where: { $0.id == pin.placeId }),
                       let lat = place.latitude, let lng = place.longitude {
                        Annotation(place.nameAr,
                                  coordinate: CLLocationCoordinate2D(latitude: lat, longitude: lng)) {
                            Text(pin.customEmoji)
                                .font(.title2)
                                .shadow(radius: 2)
                        }
                    }
                }
            }
        }
    }
}
```

- **Dependencies:** SwiftData, MapKit

#### Feature 2: Export Map (Share Collection)
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h

```swift
struct MapExporter {
    /// Export to different formats
    enum ExportFormat {
        case json    // App format
        case csv     // Spreadsheet
        case kml     // Google Earth
        case gpx     // GPS apps
    }
    
    static func export(pins: [PersonalPin], places: [CachedPlace],
                       format: ExportFormat) -> Data {
        switch format {
        case .csv:
            return exportCSV(pins: pins, places: places)
        case .kml:
            return exportKML(pins: pins, places: places)
        default:
            return exportJSON(pins: pins, places: places)
        }
    }
    
    private static func exportCSV(pins: [PersonalPin], places: [CachedPlace]) -> Data {
        var csv = "الاسم,الفئة,الحي,التقييم,ملاحظة,تاريخ الزيارة\n"
        for pin in pins {
            if let place = places.first(where: { $0.id == pin.placeId }) {
                csv += "\"\(place.nameAr)\",\"\(place.category)\","
                csv += "\"\(place.neighborhood ?? "")\","
                csv += "\(place.googleRating),"
                csv += "\"\(pin.personalNote ?? "")\","
                csv += "\(pin.visitDate?.formatted() ?? "")\n"
            }
        }
        return csv.data(using: .utf8)!
    }
    
    private static func exportKML(pins: [PersonalPin], places: [CachedPlace]) -> Data {
        var kml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
        <Document><name>أماكني - وين نروح</name>
        """
        for pin in pins {
            if let place = places.first(where: { $0.id == pin.placeId }),
               let lat = place.latitude, let lng = place.longitude {
                kml += """
                <Placemark>
                    <name>\(place.nameAr)</name>
                    <description>\(pin.personalNote ?? "")</description>
                    <Point><coordinates>\(lng),\(lat),0</coordinates></Point>
                </Placemark>
                """
            }
        }
        kml += "</Document></kml>"
        return kml.data(using: .utf8)!
    }
}
```

- **Dependencies:** PersonalPin model

#### Feature 3: Follow Friends' Maps
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 6h

- **Dependencies:** User accounts, social features, cloud sync

---

## 🇺🇸 Western Apps (4)

---

### 17. Time Out — Editorial Content Discovery

#### Feature 1: "Best Of" Editorial Cards
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h

```swift
struct EditorialCard: Codable, Identifiable {
    let id: String
    let title: String          // "أفضل 15 كافيه للعمل في الرياض"
    let subtitle: String       // "اشتغل بهدوء مع قهوة ممتازة"
    let coverImage: String
    let category: String       // "كافيهات", "مطاعم", "ترفيه"
    let placeIds: [String]
    let content: String        // Markdown content
    let author: String
    let publishDate: Date
    let readTimeMinutes: Int
}
```

- **Dependencies:** Editorial content system

#### Feature 2: Events & Seasonal Highlights
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 5h

- **Dependencies:** Events data, calendar integration

#### Feature 3: City Guide by Theme
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 3h

- **Dependencies:** Theme/occasion tags

---

### 18. Yelp — Review Ecosystem

#### Feature 1: Review Highlights (AI Summary)
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 6h

```swift
// AI-powered review summary
struct ReviewHighlights: View {
    let positives: [String]  // AI-extracted from reviews
    let negatives: [String]
    
    var body: some View {
        VStack(alignment: .trailing, spacing: 12) {
            Text("ملخص التقييمات").font(.headline)
            
            if !positives.isEmpty {
                VStack(alignment: .trailing, spacing: 4) {
                    ForEach(positives, id: \.self) { p in
                        HStack {
                            Text(p).font(.caption)
                            Image(systemName: "hand.thumbsup.fill")
                                .foregroundStyle(.green)
                                .font(.caption)
                        }
                    }
                }
            }
            
            if !negatives.isEmpty {
                VStack(alignment: .trailing, spacing: 4) {
                    ForEach(negatives, id: \.self) { n in
                        HStack {
                            Text(n).font(.caption)
                            Image(systemName: "hand.thumbsdown.fill")
                                .foregroundStyle(.red)
                                .font(.caption)
                        }
                    }
                }
            }
        }
    }
}
```

- **Dependencies:** AI backend, review data

#### Feature 2: Business Claimed Status
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 4h

- **Dependencies:** Business portal

#### Feature 3: Photo Reviews
- **الأولوية:** 🟢 Phase 3
- **ساعات:** 6h

- **Dependencies:** Image upload, CDN

---

### 19. Swarm (Foursquare) — Gamification ⭐⭐⭐⭐

**لماذا مهم:** أقوى نظام gamification لأماكن. Check-ins + Mayors + Badges = engagement مستمر.

#### Feature 1: Check-In System
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 6h
- **الوصف:** المستخدم "يسجل حضور" لما يزور مكان. يجمع نقاط + يبني تاريخ زياراته.

```swift
// DATA MODEL
@Model
class CheckIn {
    @Attribute(.unique) var id: String
    var placeId: String
    var userId: String
    var timestamp: Date
    var note: String?
    var sharedOnSocial: Bool
    var pointsEarned: Int
    
    init(placeId: String, userId: String) {
        self.id = UUID().uuidString
        self.placeId = placeId
        self.userId = userId
        self.timestamp = Date()
        self.sharedOnSocial = false
        self.pointsEarned = 10 // Base points
    }
}

// VIEWMODEL
@Observable
class CheckInViewModel {
    private let locationService: LocationService
    
    func checkIn(at place: CachedPlace) async throws -> CheckInResult {
        // 1. Verify location (must be within 200m of place)
        guard let userLocation = await locationService.getCurrentLocation() else {
            throw CheckInError.locationUnavailable
        }
        
        guard let lat = place.latitude, let lng = place.longitude else {
            throw CheckInError.placeHasNoLocation
        }
        
        let placeLocation = CLLocation(latitude: lat, longitude: lng)
        let distance = userLocation.distance(from: placeLocation)
        
        guard distance < 200 else { // 200 meters radius
            throw CheckInError.tooFar(distance: distance)
        }
        
        // 2. Check cooldown (no double check-in within 2 hours)
        // 3. Create check-in
        // 4. Calculate points (streak bonus, new place bonus, etc.)
        // 5. Check for badge unlocks
        // 6. Check for mayor status
        
        let checkIn = CheckIn(placeId: place.id, userId: "current_user")
        
        // Bonus points
        var points = 10
        if isFirstVisit(place.id) { points += 5 } // New place bonus
        if isConsecutiveDay() { points += 3 }      // Streak bonus
        
        checkIn.pointsEarned = points
        
        return CheckInResult(
            checkIn: checkIn,
            pointsEarned: points,
            newBadges: checkForBadges(),
            isMayor: checkMayorStatus(place.id)
        )
    }
}
```

- **Dependencies:** CoreLocation, User accounts, Backend

#### Feature 2: Mayor System (عمدة المكان)
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 4h
- **الوصف:** أكثر شخص يسجل حضور بمكان معين يصير "عمدة" المكان. يظهر اسمه بصفحة المكان.

```swift
struct MayorBadge: View {
    let mayorName: String
    let checkInCount: Int
    let isCurrentUser: Bool
    
    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "crown.fill")
                .foregroundStyle(.yellow)
                .font(.caption)
            
            VStack(alignment: .trailing, spacing: 2) {
                Text("👑 عمدة المكان")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                Text(mayorName)
                    .font(.caption.bold())
                    .foregroundStyle(isCurrentUser ? .orange : .primary)
                Text("\(checkInCount) زيارة")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(8)
        .background(Color.yellow.opacity(0.1))
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

// Mayor determination logic
struct MayorEngine {
    /// Mayor = person with most check-ins at this place in last 60 days
    static func determineMayor(placeId: String, checkIns: [CheckIn]) -> String? {
        let sixtyDaysAgo = Calendar.current.date(byAdding: .day, value: -60, to: Date())!
        let recentCheckIns = checkIns.filter {
            $0.placeId == placeId && $0.timestamp > sixtyDaysAgo
        }
        
        let counts = Dictionary(grouping: recentCheckIns, by: \.userId)
            .mapValues(\.count)
        
        guard let mayor = counts.max(by: { $0.value < $1.value }),
              mayor.value >= 3 else { // Minimum 3 visits to be mayor
            return nil
        }
        
        return mayor.key
    }
}
```

- **Dependencies:** Check-in system, user accounts

#### Feature 3: Achievement Badges System
- **الأولوية:** 🟡 Phase 2
- **ساعات:** 5h

```swift
// DATA MODEL
struct Badge: Codable, Identifiable {
    let id: String
    let nameAr: String
    let nameEn: String
    let description: String
    let icon: String       // SF Symbol or custom
    let requirement: BadgeRequirement
    let tier: BadgeTier
    
    enum BadgeTier: String, Codable {
        case bronze, silver, gold, legendary
    }
}

enum BadgeRequirement: Codable {
    case checkInCount(min: Int)                    // "مستكشف": 10 check-ins
    case uniquePlaces(min: Int)                    // "رحّال": 25 unique places
    case categoryExplorer(category: String, min: Int) // "عاشق القهوة": 10 cafes
    case neighborhoodExplorer(min: Int)            // "ابن الرياض": 10 neighborhoods
    case streak(days: Int)                         // "مثابر": 7 day streak
    case mayor(count: Int)                         // "شيخ الشيوخ": mayor of 3 places
    case firstCheckIn                              // "البداية": first ever check-in
    case nightOwl(checkInsAfter10PM: Int)          // "بومة الليل": 5 late check-ins
    case earlyBird(checkInsBefore8AM: Int)         // "صباح الخير": 5 early check-ins
    case reviewer(count: Int)                      // "نقّاد": 10 reviews
    case weekendWarrior(weekendCheckIns: Int)      // "محارب الويكند": 20 weekend check-ins
}

// Pre-defined badges
extension Badge {
    static let allBadges: [Badge] = [
        Badge(id: "first", nameAr: "البداية", nameEn: "First Step",
              description: "أول تسجيل حضور لك", icon: "star.fill",
              requirement: .firstCheckIn, tier: .bronze),
        Badge(id: "explorer10", nameAr: "مستكشف", nameEn: "Explorer",
              description: "سجّل حضور في 10 أماكن مختلفة", icon: "safari.fill",
              requirement: .uniquePlaces(min: 10), tier: .bronze),
        Badge(id: "explorer50", nameAr: "رحّال", nameEn: "Traveler",
              description: "سجّل حضور في 50 مكان مختلف", icon: "globe",
              requirement: .uniquePlaces(min: 50), tier: .silver),
        Badge(id: "coffee_lover", nameAr: "عاشق القهوة", nameEn: "Coffee Lover",
              description: "زر 10 كافيهات مختلفة", icon: "cup.and.saucer.fill",
              requirement: .categoryExplorer(category: "cafe", min: 10), tier: .bronze),
        Badge(id: "foodie", nameAr: "ذوّاق", nameEn: "Foodie",
              description: "زر 20 مطعم مختلف", icon: "fork.knife",
              requirement: .categoryExplorer(category: "restaurant", min: 20), tier: .silver),
        Badge(id: "mayor3", nameAr: "شيخ الشيوخ", nameEn: "Triple Mayor",
              description: "كن عمدة 3 أماكن بنفس الوقت", icon: "crown.fill",
              requirement: .mayor(count: 3), tier: .gold),
        Badge(id: "streak7", nameAr: "مثابر", nameEn: "Streak Master",
              description: "سجّل حضور 7 أيام متتالية", icon: "flame.fill",
              requirement: .streak(days: 7), tier: .silver),
        Badge(id: "night_owl", nameAr: "بومة الليل", nameEn: "Night Owl",
              description: "5 زيارات بعد الساعة 10 مساءً", icon: "moon.stars.fill",
              requirement: .nightOwl(checkInsAfter10PM: 5), tier: .bronze),
        Badge(id: "riyadh_kid", nameAr: "ابن الرياض", nameEn: "Riyadh Native",
              description: "زر أماكن في 10 أحياء مختلفة", icon: "building.2.fill",
              requirement: .neighborhoodExplorer(min: 10), tier: .gold),
    ]
}
```

- **Dependencies:** Check-in system, user accounts

---

### 20. Yelp (continued from #18) → replaced with additional patterns

---

## 📊 Complete Priority Summary

### 🔴 MVP Features (Phase 1) — ~42 hours

| # | الميزة | المصدر | الساعات |
|---|--------|--------|---------|
| 1 | Lazy Tab Architecture | HungerStation | 3h |
| 2 | Category Cards Grid | HungerStation | 2h |
| 3 | Progressive Loading (Infinite Scroll) | HungerStation | 4h |
| 4 | Category Pill Bar (Horizontal) | Jahez | 2h |
| 5 | Place Preview Card (Rich) | Jahez | 3h |
| 6 | One-Tap Navigation | Jahez | 1h |
| 7 | "Perfect For" Smart Labels | Entertainer | 2h |
| 8 | Nearby Places | Entertainer/Dianping | 3h |
| 9 | Search + Recent + Suggestions | Careem | 3h |
| 10 | Operating Hours Display | Gathern | 2h |
| 11 | Price Range Indicator | Gurunavi | 1h |
| 12 | Map Cluster View | Naver Map | 3h |
| 13 | Share Place Link | KakaoMap | 2h |
| — | **الإجمالي** | — | **~31h** + 11h from MVP-PLAN core = **~42h** |

### 🟡 Phase 2 Features — ~68 hours

| # | الميزة | المصدر | الساعات |
|---|--------|--------|---------|
| 1 | Trending Carousel | Keeta | 3h |
| 2 | Delivery Price Comparison | Keeta | 4h |
| 3 | Quick Visual Filters | Keeta | 3h |
| 4 | Share Card (Image) | Entertainer | 3h |
| 5 | Bottom Sheet Discovery | Careem | 4h |
| 6 | Quick Actions | Careem | 2h |
| 7 | Save to Collections | Xiaohongshu | 4h |
| 8 | "أفضل 10 بالحي" | Dianping | 6h |
| 9 | Menu Display | Gurunavi | 5h |
| 10 | Cuisine Filters | Gurunavi | 2h |
| 11 | Multi-Category Search | Meituan | 3h |
| 12 | Curated Lists | MangoPlate | 4h |
| 13 | Editorial Cards | Time Out | 4h |
| 14 | City Guide by Theme | Time Out | 3h |
| 15 | Personal Map + Tags | Mapstr | 5h |
| 16 | Export Map | Mapstr | 4h |
| 17 | Check-In System | Swarm | 6h |
| 18 | Mayor System | Swarm | 4h |
| 19 | Badges System | Swarm | 5h |
| 20 | Map Info Overlay | Naver Map | 3h |
| — | **الإجمالي** | — | **~77h** |

### 🟢 Phase 3 Features — ~75 hours

| # | الميزة | المصدر | الساعات |
|---|--------|--------|---------|
| 1 | Trust Rating (Tabelog) | Tabelog | 12h |
| 2 | Rating Distribution | Tabelog | 3h |
| 3 | Award Badges | Tabelog | 4h |
| 4 | User Tips | Dianping | 6h |
| 5 | Time-Limited Deals | Meituan | 5h |
| 6 | User Photo Feed | Meituan | 8h |
| 7 | Community Notes | Xiaohongshu | 10h |
| 8 | Interest Feed | Xiaohongshu | 8h |
| 9 | Loyalty Points | TheFork | 8h |
| 10 | Review Highlights (AI) | Yelp | 6h |
| 11 | Photo Reviews | Yelp | 6h |
| 12 | Follow Friends' Maps | Mapstr | 6h |
| 13 | Friends Visited | KakaoMap | 5h |
| 14 | Route Planning | Naver Map | 6h |
| 15 | Events & Seasonal | Time Out | 5h |
| — | **الإجمالي** | — | **~96h** |

---

## 🎯 Special Deep Dives

### 1. HungerStation Super App Pattern — Detailed Architecture

```
┌──────────────────────────────────────────────────────┐
│                 Super App Lite Pattern                 │
│                  (HungerStation-style)                │
│                                                       │
│  ┌─────────────────────────────────────────────┐     │
│  │              App Shell (< 5 MB)              │     │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐ │     │
│  │  │  Home  │ │Explore │ │  Map   │ │ Me   │ │     │
│  │  │ Module │ │ Module │ │ Module │ │Module│ │     │
│  │  └───┬────┘ └───┬────┘ └───┬────┘ └──┬───┘ │     │
│  │      │          │          │          │      │     │
│  │  ┌───▼──────────▼──────────▼──────────▼───┐ │     │
│  │  │        Shared Services Layer           │ │     │
│  │  │  PlaceRepository | SearchService       │ │     │
│  │  │  LocationService | CacheManager        │ │     │
│  │  └──────────────────┬─────────────────────┘ │     │
│  │                     │                        │     │
│  │  ┌──────────────────▼─────────────────────┐ │     │
│  │  │          Data Layer (SwiftData)         │ │     │
│  │  │  places.json → SQLite → In-Memory      │ │     │
│  │  └────────────────────────────────────────┘ │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  Key Principles:                                      │
│  ✅ Each module loads independently (lazy)            │
│  ✅ Shared data layer (no duplication)                │
│  ✅ Offline-first (all data local)                    │
│  ✅ < 25 MB total app size                            │
│  ✅ < 1.5s cold launch                                │
│  ✅ 60fps scroll performance                          │
└──────────────────────────────────────────────────────┘
```

### 2. Tabelog Rating — Full Algorithm Design

```
تقييم وين نروح (مستوحى من Tabelog)
═══════════════════════════════════

Google Rating (External):  ★★★★☆  4.2/5.0  (من Google Maps)
                                    ↓
Trust Score (Internal):    ████░░  67/100   (محسوب من:)
  ├── Data Completeness:   ███░░░  55%  (صور + ساعات + هاتف + وصف)
  ├── Activity Score:      ████░░  75%  (views + favorites + shares)
  ├── Information Quality: ████░░  70%  (تفصيل + حداثة)
  └── User Engagement:     ████░░  65%  (check-ins + reviews)

Anti-Fake Shield:
  ✅ Google rating = external (not manipulable by us)
  ✅ Trust Score = data quality metric (not user-submitted ratings)
  ✅ Phase 3: Full Tabelog-style weighted user ratings
  ✅ Reviewer credibility scoring
  ✅ Review length + detail weighting
  ✅ Burst detection (spam filter)
```

### 3. Dianping Hyperlocal — "أفضل 10 بالحي"

```
User Location: الملقا
═════════════════════

📍 أفضل 10 كافيهات في الملقا
─────────────────────────────
🥇 1. بارنز كافيه      ⭐ 4.6  │ 350m  │ "قهوة ممتازة + أجواء عمل"
🥈 2. % أرابيكا         ⭐ 4.5  │ 500m  │ "اسبريسو ياباني مميز"
🥉 3. كافيه بَتيل       ⭐ 4.5  │ 700m  │ "حلويات + قهوة + هدوء"
4. إل&هي              ⭐ 4.4  │ 200m  │ "تصميم جميل + خدمة سريعة"
5. ريسيس كافيه        ⭐ 4.3  │ 450m  │ "أسعار معقولة + واسع"
...

Score = Rating(40%) + Reviews(25%) + Completeness(20%) + Freshness(15%)

📍 أفضل 10 مطاعم في حي الياسمين
📍 أفضل 10 حلويات في حي النرجس
📍 أفضل 10 أماكن عائلية في حي العليا
```

### 4. Swarm Gamification — Full System

```
╔══════════════════════════════════╗
║     🏆 Gamification Dashboard    ║
╠══════════════════════════════════╣
║                                  ║
║  📊 إحصائياتك                    ║
║  ├── إجمالي الزيارات: 47         ║
║  ├── أماكن مختلفة: 23            ║
║  ├── أحياء: 8                    ║
║  ├── أيام متتالية: 5 🔥          ║
║  └── نقاط: 720                   ║
║                                  ║
║  👑 عمدة في:                     ║
║  ├── بارنز كافيه (12 زيارة)      ║
║  └── مطعم البيك العليا (8 زيارات)║
║                                  ║
║  🏅 شارات (6/15):               ║
║  ├── ✅ البداية (أول check-in)   ║
║  ├── ✅ مستكشف (10 أماكن)        ║
║  ├── ✅ عاشق القهوة (10 كافيه)   ║
║  ├── ✅ بومة الليل (5 زيارات ليل)║
║  ├── ✅ مثابر (7 أيام متتالية)   ║
║  ├── ✅ شيخ الشيوخ (3 عمادات)    ║
║  ├── 🔒 رحّال (50 مكان) [23/50]  ║
║  ├── 🔒 ذوّاق (20 مطعم) [14/20] ║
║  └── 🔒 ابن الرياض (10 أحياء)   ║
║                                  ║
║  📍 آخر الزيارات:                ║
║  ├── بارنز - الملقا (اليوم)      ║
║  ├── مطعم لمسات - العليا (أمس)   ║
║  └── حلويات سعد الدين (قبل يومين)║
╚══════════════════════════════════╝
```

### 5. Mapstr Personal Maps — UX Flow

```
My Map (خريطتي)
═══════════════

Filters: [الكل 47] [زرته ✅ 23] [أبي أزوره 📌 15] [موصى ⭐ 9]

🗺️ [Map with colored pins]
  ✅ Green pins = visited
  📌 Blue pins = want to visit
  ⭐ Gold pins = recommended

Actions per pin:
├── Add personal note 📝
├── Rate (personal, private) ⭐
├── Add photos 📸
├── Change tag/color 🎨
├── Share this pin 📤
└── Remove from map ❌

Export Options:
├── 📊 CSV (spreadsheet)
├── 🌍 KML (Google Earth)
├── 📱 Share collection link
└── 📋 Copy as text list
```

---

## 🔗 Dependency Map

```
Phase 1 (MVP) Dependencies:
  SwiftUI ←── built-in
  SwiftData ←── built-in (iOS 17+)
  MapKit ←── built-in
  CoreLocation ←── built-in
  places.json ←── bundled from GitHub

Phase 2 Dependencies:
  + Kingfisher (image caching) OR AsyncImage improvements
  + Check-in system → needs basic user identity
  + Personal maps → needs SwiftData collections
  + Delivery data → needs data collection pipeline
  + Editorial content → needs CMS or bundled markdown

Phase 3 Dependencies:
  + Supabase (backend)
  + Supabase Auth (user accounts)
  + Cloud storage (images, user content)
  + Push Notifications (APNs)
  + AI service (review summaries, semantic search)
  + Moderation system (UGC)
```

---

*Document generated: 2026-02-21 | Next: IOS-READY-CHECKLIST.md*
