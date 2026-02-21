// WainNroohApp.swift
// وين نروح — تطبيق اكتشاف أماكن الرياض
// هوية ليالي الرياض + RTL + Lazy Loading

import SwiftUI

@main
struct WainNroohApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .environment(\.layoutDirection, .rightToLeft)
                .preferredColorScheme(.dark) // الدارك = الافتراضي
                .tint(Theme.green400) // اللون الرئيسي للتطبيق
        }
    }
}

// MARK: - الشاشة الرئيسية + التاب بار

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    @State private var selectedTab: AppTab = .home
    @State private var showOnboarding = false
    
    var body: some View {
        ZStack(alignment: .bottom) {
            // المحتوى — Lazy Loading
            TabView(selection: $selectedTab) {
                HomeView()
                    .tag(AppTab.home)
                
                ExploreView()
                    .tag(AppTab.explore)
                
                MapView()
                    .tag(AppTab.map)
                
                MyPlacesView()
                    .tag(AppTab.favorites)
                
                ProfileView()
                    .tag(AppTab.profile)
            }
            .tabViewStyle(.page(indexDisplayMode: .never))
            
            // تاب بار مخصص
            customTabBar
        }
        .ignoresSafeArea(.keyboard)
        .onAppear {
            // أول مرة = onboarding
            if !UserDefaults.standard.bool(forKey: "hasSeenOnboarding") {
                showOnboarding = true
            }
        }
        .fullScreenCover(isPresented: $showOnboarding) {
            OnboardingView {
                UserDefaults.standard.set(true, forKey: "hasSeenOnboarding")
                showOnboarding = false
            }
        }
    }
    
    // MARK: - تاب بار مخصص
    
    private var customTabBar: some View {
        HStack(spacing: 0) {
            ForEach(AppTab.allCases) { tab in
                Button {
                    withAnimation(Theme.animSpring) {
                        selectedTab = tab
                    }
                } label: {
                    VStack(spacing: 4) {
                        Image(systemName: selectedTab == tab ? tab.iconFilled : tab.icon)
                            .font(.system(size: 20))
                            .symbolEffect(.bounce, value: selectedTab == tab)
                        
                        Text(tab.title)
                            .font(Theme.badge(size: 10))
                    }
                    .foregroundStyle(selectedTab == tab ? Theme.green400 : Theme.sand)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, Theme.spacingS)
                }
            }
        }
        .padding(.horizontal, Theme.spacingS)
        .padding(.bottom, 4)
        .background(.ultraThinMaterial)
        .overlay(
            Rectangle()
                .fill(Theme.green400.opacity(0.1))
                .frame(height: 0.5),
            alignment: .top
        )
    }
}

// MARK: - تابات التطبيق

enum AppTab: String, CaseIterable, Identifiable {
    case home, explore, map, favorites, profile
    
    var id: String { rawValue }
    
    var title: String {
        switch self {
        case .home: return "الرئيسية"
        case .explore: return "استكشف"
        case .map: return "الخريطة"
        case .favorites: return "مفضلاتي"
        case .profile: return "حسابي"
        }
    }
    
    var icon: String {
        switch self {
        case .home: return "house"
        case .explore: return "magnifyingglass"
        case .map: return "map"
        case .favorites: return "heart"
        case .profile: return "person"
        }
    }
    
    var iconFilled: String {
        switch self {
        case .home: return "house.fill"
        case .explore: return "magnifyingglass"
        case .map: return "map.fill"
        case .favorites: return "heart.fill"
        case .profile: return "person.fill"
        }
    }
}

// MARK: - حالة التطبيق

class AppState: ObservableObject {
    @Published var places: [Place] = []
    @Published var isLoading = true
    @Published var favorites: Set<String> = []
    
    init() {
        loadPlaces()
        loadFavorites()
    }
    
    /// تحميل الأماكن من ملف JSON المدمج
    func loadPlaces() {
        guard let url = Bundle.main.url(forResource: "places", withExtension: "json") else {
            isLoading = false
            return
        }
        
        do {
            let data = try Data(contentsOf: url)
            let decoded = try JSONDecoder().decode([Place].self, from: data)
            DispatchQueue.main.async {
                self.places = decoded
                self.isLoading = false
            }
        } catch {
            print("❌ خطأ بتحميل الأماكن: \(error)")
            isLoading = false
        }
    }
    
    /// تحميل المفضلات من UserDefaults
    func loadFavorites() {
        if let saved = UserDefaults.standard.array(forKey: "favorites") as? [String] {
            favorites = Set(saved)
        }
    }
    
    /// إضافة/حذف من المفضلات
    func toggleFavorite(_ placeId: String) {
        if favorites.contains(placeId) {
            favorites.remove(placeId)
        } else {
            favorites.insert(placeId)
        }
        UserDefaults.standard.set(Array(favorites), forKey: "favorites")
    }
    
    /// هل المكان مفضل؟
    func isFavorite(_ placeId: String) -> Bool {
        favorites.contains(placeId)
    }
}

// MARK: - شاشة الترحيب

struct OnboardingView: View {
    let onComplete: () -> Void
    @State private var currentPage = 0
    
    private let pages: [(emoji: String, title: String, subtitle: String)] = [
        ("🏙", "وين نروح بالرياض؟", "أكثر من ٦,٥٠٠ مكان\nمطاعم · كافيهات · ترفيه · وأكثر"),
        ("📍", "اكتشف حسب موقعك", "أفضل الأماكن القريبة منك\nمع التقييمات والأسعار"),
        ("🤖", "ذكاء اصطناعي يساعدك", "قولّه وش تبي وهو يرشحلك\nالمكان المناسب")
    ]
    
    var body: some View {
        ZStack {
            Color.appBackground.ignoresSafeArea()
            
            VStack(spacing: Theme.spacingXXL) {
                Spacer()
                
                // المحتوى
                TabView(selection: $currentPage) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        VStack(spacing: Theme.spacingXL) {
                            Text(pages[index].emoji)
                                .font(.system(size: 80))
                            
                            Text(pages[index].title)
                                .font(Theme.largeTitle())
                                .foregroundStyle(.appTextPrimary)
                                .multilineTextAlignment(.center)
                            
                            Text(pages[index].subtitle)
                                .font(Theme.body())
                                .foregroundStyle(.appTextSecondary)
                                .multilineTextAlignment(.center)
                                .lineSpacing(6)
                        }
                        .tag(index)
                    }
                }
                .tabViewStyle(.page(indexDisplayMode: .always))
                
                Spacer()
                
                // زر البداية
                Button {
                    if currentPage < pages.count - 1 {
                        withAnimation {
                            currentPage += 1
                        }
                    } else {
                        onComplete()
                    }
                } label: {
                    Text(currentPage == pages.count - 1 ? "يلا نبدأ!" : "التالي")
                        .frame(maxWidth: .infinity)
                        .wainPrimaryButton()
                }
                .padding(.horizontal, Theme.spacingXL)
                .padding(.bottom, Theme.spacingXXL)
                
                // تخطي
                if currentPage < pages.count - 1 {
                    Button("تخطي") {
                        onComplete()
                    }
                    .font(Theme.detail())
                    .foregroundStyle(.appTextSecondary)
                    .padding(.bottom, Theme.spacingL)
                }
            }
        }
    }
}
