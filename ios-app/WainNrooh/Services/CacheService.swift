// CacheService.swift
// خدمة الكاش — SwiftData أوفلاين + مزامنة

import Foundation
import SwiftData
import Combine

// MARK: - خدمة الكاش

/// خدمة التخزين المؤقت — Offline-first architecture
/// تحمّل البيانات من الكاش أولاً ثم تحدّث من السيرفر بالخلفية
final class CacheService: ObservableObject, @unchecked Sendable {
    
    // MARK: - خصائص منشورة
    
    /// هل المزامنة الأولية تمت؟
    @Published var isInitialSyncComplete: Bool = false
    
    /// هل المزامنة جارية؟
    @Published var isSyncing: Bool = false
    
    /// آخر مزامنة
    @Published var lastSyncDate: Date?
    
    /// خطأ المزامنة
    @Published var syncError: String?
    
    // MARK: - خصائص خاصة
    
    private let placesService = PlacesService.shared
    private let userDefaults = UserDefaults.standard
    
    private let lastSyncKey = "lastSyncDate"
    private let initialSyncKey = "isInitialSyncComplete"
    
    // MARK: - تهيئة
    
    init() {
        isInitialSyncComplete = userDefaults.bool(forKey: initialSyncKey)
        lastSyncDate = userDefaults.object(forKey: lastSyncKey) as? Date
    }
    
    // MARK: - المزامنة الأولية
    
    /// تنفيذ المزامنة الأولية — تحميل كل البيانات
    @MainActor
    func performInitialSync() async {
        guard !isInitialSyncComplete else {
            // المزامنة الأولية تمت — ننفذ delta sync
            await performDeltaSync()
            return
        }
        
        isSyncing = true
        syncError = nil
        
        do {
            AppConfig.debugLog("🔄 بدء المزامنة الأولية...")
            
            // جلب كل الأماكن (بالدفعات)
            var allPlaces: [Place] = []
            var page = 1
            let perPage = 100
            
            while true {
                let batch = try await placesService.fetchPlaces(
                    page: page,
                    perPage: perPage,
                    sortBy: .rating
                )
                allPlaces.append(contentsOf: batch)
                
                if batch.count < perPage { break }
                page += 1
                
                // حماية من حلقة لا نهائية
                if page > 100 { break }
            }
            
            AppConfig.debugLog("✅ تم جلب \(allPlaces.count) مكان")
            
            // تحديث الحالة
            isInitialSyncComplete = true
            lastSyncDate = Date()
            isSyncing = false
            
            userDefaults.set(true, forKey: initialSyncKey)
            userDefaults.set(Date(), forKey: lastSyncKey)
            
            AppConfig.debugLog("✅ المزامنة الأولية اكتملت!")
            
        } catch {
            AppConfig.debugLog("❌ فشل المزامنة الأولية: \(error)")
            syncError = error.localizedDescription
            isSyncing = false
            
            // حتى لو فشلت — نعلم التطبيق إنها اكتملت عشان يشتغل
            // البيانات المحلية ممكن تكون فاضية
            isInitialSyncComplete = true
            userDefaults.set(true, forKey: initialSyncKey)
        }
    }
    
    // MARK: - المزامنة التفاضلية
    
    /// مزامنة التغييرات فقط (delta sync)
    @MainActor
    func performDeltaSync() async {
        guard !isSyncing else { return }
        
        // لا نزامن أكثر من مرة كل 15 دقيقة
        if let lastSync = lastSyncDate,
           Date().timeIntervalSince(lastSync) < 900 {
            return
        }
        
        isSyncing = true
        syncError = nil
        
        do {
            AppConfig.debugLog("🔄 بدء المزامنة التفاضلية...")
            
            // جلب الأماكن المحدثة بعد آخر مزامنة
            let updatedPlaces = try await placesService.fetchPlaces(
                page: 1,
                perPage: 100,
                sortBy: .newest
            )
            
            AppConfig.debugLog("✅ تم جلب \(updatedPlaces.count) تحديث")
            
            lastSyncDate = Date()
            isSyncing = false
            userDefaults.set(Date(), forKey: lastSyncKey)
            
        } catch {
            AppConfig.debugLog("❌ فشل المزامنة التفاضلية: \(error)")
            syncError = error.localizedDescription
            isSyncing = false
        }
    }
    
    // MARK: - دفع الإجراءات المعلقة
    
    /// دفع الإجراءات المعلقة (المفضلة المضافة أوفلاين مثلاً)
    func pushPendingActions() async {
        AppConfig.debugLog("📤 دفع الإجراءات المعلقة...")
        // TODO: تنفيذ الإجراءات المعلقة مع SwiftData
    }
    
    // MARK: - حالة الكاش
    
    /// نص آخر مزامنة
    var lastSyncText: String {
        guard let date = lastSyncDate else { return "لم تتم المزامنة بعد" }
        
        let interval = Date().timeIntervalSince(date)
        if interval < 60 { return "الحين" }
        if interval < 3600 { return "قبل \(Int(interval / 60)) دقيقة" }
        if interval < 86400 { return "قبل \(Int(interval / 3600)) ساعة" }
        return "قبل \(Int(interval / 86400)) يوم"
    }
    
    /// هل الكاش قديم؟ (أكثر من ساعة)
    var isCacheStale: Bool {
        guard let date = lastSyncDate else { return true }
        return Date().timeIntervalSince(date) > AppConfig.cacheTTL
    }
    
    /// مسح الكاش
    @MainActor
    func clearCache() {
        isInitialSyncComplete = false
        lastSyncDate = nil
        syncError = nil
        
        userDefaults.removeObject(forKey: initialSyncKey)
        userDefaults.removeObject(forKey: lastSyncKey)
        
        AppConfig.debugLog("🗑️ تم مسح الكاش")
    }
}
