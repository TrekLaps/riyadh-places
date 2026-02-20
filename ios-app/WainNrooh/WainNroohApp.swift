// WainNroohApp.swift
// وين نروح بالرياض — نقطة الدخول الرئيسية للتطبيق
// iOS 17+ | SwiftUI | MVVM

import SwiftUI
import SwiftData

/// التطبيق الرئيسي — وين نروح بالرياض
/// تطبيق اكتشاف أماكن بالرياض مع مقارنة أسعار التوصيل والبحث الذكي بالعربي
@main
struct WainNroohApp: App {
    
    // MARK: - حالة التطبيق
    
    /// خدمة الموقع الجغرافي — تشتغل طول عمر التطبيق
    @StateObject private var locationService = LocationService()
    
    /// خدمة الكاش المحلي
    @StateObject private var cacheService = CacheService()
    
    /// إعدادات المظهر (دارك/لايت)
    @AppStorage("isDarkMode") private var isDarkMode = true
    
    /// أول فتح للتطبيق
    @AppStorage("isFirstLaunch") private var isFirstLaunch = true
    
    // MARK: - SwiftData Container
    
    /// حاوية SwiftData للتخزين المحلي (أوفلاين)
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            CachedPlace.self,
            CachedFavorite.self,
            CachedDeliveryPrice.self,
            CachedMenuPrice.self,
            PendingAction.self
        ])
        let modelConfiguration = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false
        )
        
        do {
            return try ModelContainer(
                for: schema,
                configurations: [modelConfiguration]
            )
        } catch {
            // في حالة فشل إنشاء الحاوية — نحاول مسح البيانات وإعادة الإنشاء
            fatalError("❌ فشل إنشاء ModelContainer: \(error)")
        }
    }()
    
    // MARK: - Body
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(locationService)
                .environmentObject(cacheService)
                .environment(\.layoutDirection, .rightToLeft)
                .preferredColorScheme(isDarkMode ? .dark : .light)
                .onAppear {
                    setupAppearance()
                    if isFirstLaunch {
                        performFirstLaunchSetup()
                    }
                }
        }
        .modelContainer(sharedModelContainer)
    }
    
    // MARK: - إعداد المظهر
    
    /// ضبط المظهر العام للتطبيق
    private func setupAppearance() {
        // ضبط اتجاه الواجهة RTL
        UIView.appearance().semanticContentAttribute = .forceRightToLeft
        
        // ضبط ألوان شريط التنقل
        let navBarAppearance = UINavigationBarAppearance()
        navBarAppearance.configureWithOpaqueBackground()
        navBarAppearance.backgroundColor = UIColor(Theme.backgroundPrimary)
        navBarAppearance.titleTextAttributes = [
            .foregroundColor: UIColor(Theme.textPrimary)
        ]
        navBarAppearance.largeTitleTextAttributes = [
            .foregroundColor: UIColor(Theme.textPrimary)
        ]
        
        UINavigationBar.appearance().standardAppearance = navBarAppearance
        UINavigationBar.appearance().scrollEdgeAppearance = navBarAppearance
        
        // ضبط ألوان شريط التبويب
        let tabBarAppearance = UITabBarAppearance()
        tabBarAppearance.configureWithOpaqueBackground()
        tabBarAppearance.backgroundColor = UIColor(Theme.backgroundPrimary)
        
        UITabBar.appearance().standardAppearance = tabBarAppearance
        UITabBar.appearance().scrollEdgeAppearance = tabBarAppearance
    }
    
    /// إعداد أول فتح — تحميل البيانات الأولية
    private func performFirstLaunchSetup() {
        Task {
            // طلب صلاحية الموقع
            locationService.requestPermission()
            
            // تحميل البيانات الأولية من السيرفر
            await cacheService.performInitialSync()
            
            isFirstLaunch = false
        }
    }
}

// MARK: - الشاشة الرئيسية مع التبويبات

/// الشاشة الرئيسية — تحتوي على التبويبات الخمسة
struct ContentView: View {
    
    @State private var selectedTab: AppTab = .home
    @EnvironmentObject var locationService: LocationService
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // الرئيسية
            HomeView()
                .tabItem {
                    Label("الرئيسية", systemImage: "house.fill")
                }
                .tag(AppTab.home)
            
            // البحث
            SearchView()
                .tabItem {
                    Label("بحث", systemImage: "magnifyingglass")
                }
                .tag(AppTab.search)
            
            // الخريطة
            MapView()
                .tabItem {
                    Label("خريطة", systemImage: "map.fill")
                }
                .tag(AppTab.map)
            
            // المفضلة
            FavoritesView()
                .tabItem {
                    Label("المفضلة", systemImage: "heart.fill")
                }
                .tag(AppTab.favorites)
            
            // مقارنة التوصيل
            DeliveryMainView()
                .tabItem {
                    Label("التوصيل", systemImage: "bicycle")
                }
                .tag(AppTab.delivery)
        }
        .tint(Theme.primary)
        .environment(\.layoutDirection, .rightToLeft)
    }
}

// MARK: - تبويبات التطبيق

/// التبويبات المتاحة في التطبيق
enum AppTab: Hashable {
    case home       // الرئيسية
    case search     // البحث
    case map        // الخريطة
    case favorites  // المفضلة
    case delivery   // التوصيل
}
