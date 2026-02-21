// CacheService.swift
// خدمة الكاش — SwiftData offline + sync queue

import Foundation
import SwiftData

@MainActor
class CacheService: ObservableObject {
    static let shared = CacheService()
    
    private init() {}
    
    /// Cache places to SwiftData for offline access
    func cachePlaces(_ places: [Place], context: ModelContext) {
        for place in places {
            let cached = CachedPlace(from: place)
            context.insert(cached)
        }
        try? context.save()
    }
    
    /// Get cached places count
    func cachedCount(context: ModelContext) -> Int {
        let descriptor = FetchDescriptor<CachedPlace>()
        return (try? context.fetchCount(descriptor)) ?? 0
    }
    
    /// Clear all cached places
    func clearCache(context: ModelContext) {
        try? context.delete(model: CachedPlace.self)
        try? context.save()
    }
    
    /// Queue an action for later sync
    func queueAction(type: String, targetId: String, payload: Data? = nil, context: ModelContext) {
        let action = PendingAction(actionType: type, targetId: targetId, payload: payload)
        context.insert(action)
        try? context.save()
    }
    
    /// Get pending actions count
    func pendingActionsCount(context: ModelContext) -> Int {
        let descriptor = FetchDescriptor<PendingAction>()
        return (try? context.fetchCount(descriptor)) ?? 0
    }
}
