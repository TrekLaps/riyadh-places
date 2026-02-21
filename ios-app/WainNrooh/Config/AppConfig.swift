// AppConfig.swift
// إعدادات التطبيق — HS Pattern (offline-first, no Supabase)

import Foundation

enum AppConfig {
    // MARK: - App Info
    static let appName = "وين نروح"
    static let appNameEn = "WainNrooh"
    static let version = "1.0.0"
    static let buildNumber = "1"
    
    // MARK: - Backend API (future)
    static let apiBaseURL = "https://api.wain-nrooh.com"
    static let apiVersion = "v1"
    
    // MARK: - Data
    static let bundledDataFile = "places"  // places.json in bundle
    static let totalPlaces = 6509
    
    // MARK: - Progressive Loading (HS Pattern)
    static let initialLoadCount = 20
    static let pageSize = 20
    static let searchDebounceMs = 300
    
    // MARK: - Cache
    static let cacheExpiryHours = 24
    static let maxCachedPlaces = 10000
    
    // MARK: - Map
    static let riyadhLat = 24.7136
    static let riyadhLng = 46.6753
    static let defaultZoomSpan = 0.15
    
    // MARK: - Riyadh Bounds (for validation)
    static let riyadhLatRange = 24.3...25.2
    static let riyadhLngRange = 46.2...47.2
    
    // MARK: - Social
    static let twitterHandle = "@RPlaces75732"
    static let websiteURL = "https://wain-nrooh.com"
    
    // MARK: - Feature Flags
    static let isAIChatEnabled = true
    static let isDeliveryCompareEnabled = false  // Phase 2
    static let isOfflineMode = true
}
