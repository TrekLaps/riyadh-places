// CachedFavorite.swift
// موديل المفضلة المحلية — SwiftData

import Foundation
import SwiftData

// MARK: - المفضلة المخزنة محلياً

/// مفضلة محفوظة محلياً في SwiftData — للعمل بدون إنترنت
@Model
final class CachedFavorite {
    @Attribute(.unique) var id: String
    var placeId: String
    var addedAt: Date
    var isSynced: Bool
    
    init(placeId: String) {
        self.id = UUID().uuidString
        self.placeId = placeId
        self.addedAt = Date()
        self.isSynced = false
    }
}
