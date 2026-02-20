// AppConfig.swift
// إعدادات التطبيق — URLs و API keys و ثوابت

import Foundation

// MARK: - إعدادات التطبيق

/// الإعدادات المركزية للتطبيق
enum AppConfig {
    
    // MARK: - Supabase
    
    /// رابط مشروع Supabase
    static let supabaseURL = "https://your-project.supabase.co"
    
    /// مفتاح Supabase العام (anon key — آمن للعميل)
    static let supabaseAnonKey = "your-anon-key-here"
    
    // MARK: - API
    
    /// رابط الـ API الرئيسي
    static let apiBaseURL = "https://api.wainnrooh.com/v1"
    
    /// رابط الـ CDN للصور
    static let cdnBaseURL = "https://cdn.wainnrooh.com"
    
    /// الإصدار الحالي من الـ API
    static let apiVersion = "v1"
    
    // MARK: - خريطة الرياض
    
    /// مركز الرياض (إحداثيات)
    static let riyadhCenterLatitude = 24.7136
    static let riyadhCenterLongitude = 46.6753
    
    /// نطاق البحث الافتراضي (بالمتر)
    static let defaultSearchRadius: Double = 5000
    
    /// الحد الأقصى لنطاق البحث
    static let maxSearchRadius: Double = 50000
    
    /// حدود الرياض (Bounding Box)
    static let riyadhBounds = (
        minLat: 24.4, maxLat: 25.1,
        minLng: 46.3, maxLng: 47.1
    )
    
    // MARK: - تخزين مؤقت
    
    /// مدة صلاحية الكاش (بالثواني) — ساعة واحدة
    static let cacheTTL: TimeInterval = 3600
    
    /// مدة صلاحية كاش الأسعار — 6 ساعات
    static let priceCacheTTL: TimeInterval = 21600
    
    /// مدة صلاحية كاش البحث — 15 دقيقة
    static let searchCacheTTL: TimeInterval = 900
    
    // MARK: - صفحات
    
    /// عدد النتائج في الصفحة
    static let pageSize = 20
    
    /// الحد الأقصى للنتائج
    static let maxPageSize = 100
    
    // MARK: - بحث
    
    /// الحد الأدنى لأحرف البحث
    static let minSearchLength = 2
    
    /// تأخير البحث التلقائي (بالميلي ثانية)
    static let searchDebounceMs: UInt64 = 300_000_000 // 300ms بالنانو ثانية
    
    /// الحد الأقصى لعمليات البحث الأخيرة المحفوظة
    static let maxRecentSearches = 10
    
    // MARK: - صور
    
    /// الحد الأقصى لحجم الصورة (بالميقا بايت)
    static let maxImageSizeMB = 10
    
    /// أبعاد الصورة المصغرة
    static let thumbnailSize = CGSize(width: 150, height: 150)
    
    /// أبعاد الصورة المتوسطة
    static let mediumImageSize = CGSize(width: 400, height: 300)
    
    // MARK: - تطبيق
    
    /// اسم التطبيق
    static let appName = "وين نروح"
    
    /// اسم التطبيق بالإنجليزي
    static let appNameEn = "Wain Nrooh"
    
    /// إصدار التطبيق
    static var appVersion: String {
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0"
    }
    
    /// رقم البناء
    static var buildNumber: String {
        Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "1"
    }
    
    /// Bundle ID
    static let bundleId = "com.wainnrooh.app"
    
    // MARK: - روابط خارجية
    
    /// رابط الموقع
    static let websiteURL = "https://wainnrooh.com"
    
    /// رابط الخصوصية
    static let privacyPolicyURL = "https://wainnrooh.com/privacy"
    
    /// رابط الشروط والأحكام
    static let termsOfServiceURL = "https://wainnrooh.com/terms"
    
    /// رابط الدعم
    static let supportEmail = "support@wainnrooh.com"
    
    /// حساب تويتر
    static let twitterHandle = "@wainnrooh"
    
    /// حساب إنستقرام
    static let instagramHandle = "@wainnrooh"
    
    // MARK: - Debug
    
    /// هل نحن في وضع التطوير؟
    #if DEBUG
    static let isDebug = true
    #else
    static let isDebug = false
    #endif
    
    /// طباعة للتطوير فقط
    static func debugLog(_ message: String, file: String = #file, line: Int = #line) {
        #if DEBUG
        let fileName = (file as NSString).lastPathComponent
        print("🔍 [\(fileName):\(line)] \(message)")
        #endif
    }
}
