// WainNroohApp.swift
// وين نروح بالرياض — Super App خفيف (HS Pattern)
// iOS 17+ | SwiftUI | MVVM | Lazy Loading | Offline-First

import SwiftUI
import SwiftData

@main
struct WainNroohApp: App {
    
    @StateObject private var appState = AppState()
    @AppStorage("isDarkMode") private var isDarkMode = true
    @AppStorage("isFirstLaunch") private var isFirstLaunch = true
    
    // SwiftData Container
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            CachedPlace.self,
            CachedFavorite.self,
            UserProfile.self,
            ShareableList.self,
            PendingAction.self
        ])
        let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)
        do {
            return try ModelContainer(for: schema, configurations: [config])
        } catch {
            fatalError("❌ فشل إنشاء ModelContainer: \(error)")
        }
    }()
    
    var body: some Scene {
        WindowGroup {
            if isFirstLaunch {
                OnboardingView(isFirstLaunch: $isFirstLaunch)
                    .environmentObject(appState)
            } else if !appState.isLoggedIn {
                AuthView()
                    .environmentObject(appState)
            } else {
                MainTabView()
                    .environmentObject(appState)
                    .environment(\.layoutDirection, .rightToLeft)
                    .preferredColorScheme(isDarkMode ? .dark : .light)
            }
        }
        .modelContainer(sharedModelContainer)
    }
}

// MARK: - App State (Global)

@MainActor
class AppState: ObservableObject {
    @Published var isLoggedIn: Bool = false
    @Published var currentUser: UserProfile?
    @Published var places: [Place] = []
    @Published var isDataLoaded: Bool = false
    
    init() {
        // Check if user exists in UserDefaults
        if let userData = UserDefaults.standard.data(forKey: "currentUser"),
           let user = try? JSONDecoder().decode(UserProfile.self, from: userData) {
            self.currentUser = user
            self.isLoggedIn = true
        }
    }
    
    func loadPlaces() async {
        guard !isDataLoaded else { return }
        // Load bundled places.json (offline-first)
        if let url = Bundle.main.url(forResource: "places", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let decoded = try? JSONDecoder().decode([Place].self, from: data) {
            self.places = decoded
            self.isDataLoaded = true
        }
    }
    
    func login(user: UserProfile) {
        self.currentUser = user
        self.isLoggedIn = true
        if let data = try? JSONEncoder().encode(user) {
            UserDefaults.standard.set(data, forKey: "currentUser")
        }
    }
    
    func logout() {
        self.currentUser = nil
        self.isLoggedIn = false
        UserDefaults.standard.removeObject(forKey: "currentUser")
    }
}

// MARK: - Main Tab View (HS Pattern — Lazy Loading)

struct MainTabView: View {
    @State private var selectedTab: AppTab = .home
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // كل tab يحمّل لحاله (Lazy) — مثل HungerStation
            LazyView(HomeView())
                .tabItem { Label("الرئيسية", systemImage: "house.fill") }
                .tag(AppTab.home)
            
            LazyView(ExploreView())
                .tabItem { Label("استكشف", systemImage: "safari.fill") }
                .tag(AppTab.explore)
            
            LazyView(MapView())
                .tabItem { Label("خريطة", systemImage: "map.fill") }
                .tag(AppTab.map)
            
            LazyView(MyPlacesView())
                .tabItem { Label("أماكني", systemImage: "heart.fill") }
                .tag(AppTab.myPlaces)
            
            LazyView(ProfileView())
                .tabItem { Label("حسابي", systemImage: "person.fill") }
                .tag(AppTab.profile)
        }
        .tint(Theme.primary)
        .task {
            await appState.loadPlaces()
        }
    }
}

// MARK: - Lazy View Wrapper (HS Pattern)

/// لا يحمّل الـ view إلا لما يظهر — أسرع بكثير
struct LazyView<Content: View>: View {
    let build: () -> Content
    init(_ build: @autoclosure @escaping () -> Content) {
        self.build = build
    }
    var body: Content { build() }
}

// MARK: - Tab Enum

enum AppTab: Hashable {
    case home       // الرئيسية
    case explore    // استكشف (بحث + فلاتر + مناسبات)
    case map        // الخريطة
    case myPlaces   // أماكني (المفضلة + القوائم)
    case profile    // حسابي + AI Chat
}

// MARK: - Onboarding

struct OnboardingView: View {
    @Binding var isFirstLaunch: Bool
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        VStack(spacing: 32) {
            Spacer()
            
            Text("وين نروح؟")
                .font(.system(size: 40, weight: .bold))
                .foregroundStyle(Theme.primary)
            
            Text("اكتشف أفضل الأماكن بالرياض")
                .font(.title3)
                .foregroundStyle(.secondary)
            
            Text("6,500+ مكان • مطاعم • كافيهات • ترفيه • تسوق")
                .font(.subheadline)
                .foregroundStyle(.tertiary)
                .multilineTextAlignment(.center)
            
            Spacer()
            
            Button {
                isFirstLaunch = false
            } label: {
                Text("يلا نبدأ")
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Theme.primary)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 16))
            }
            .padding(.horizontal, 32)
            .padding(.bottom, 48)
        }
        .environment(\.layoutDirection, .rightToLeft)
    }
}
