// UserProfile.swift
// موديل المستخدم — تسجيل + تفضيلات

import Foundation
import SwiftData

// MARK: - User Profile

@Model
final class UserProfile: Codable {
    @Attribute(.unique) var id: String
    var name: String
    var phone: String           // 05xxxxxxxx
    var email: String?
    var city: String            // default: الرياض
    var favoriteNeighborhoods: [String]
    var interests: [String]     // restaurant, cafe, entertainment, shopping, nature, family
    var createdAt: Date
    var lastLoginAt: Date
    
    init(name: String, phone: String, email: String? = nil,
         city: String = "الرياض",
         favoriteNeighborhoods: [String] = [],
         interests: [String] = []) {
        self.id = UUID().uuidString
        self.name = name
        self.phone = phone
        self.email = email
        self.city = city
        self.favoriteNeighborhoods = favoriteNeighborhoods
        self.interests = interests
        self.createdAt = Date()
        self.lastLoginAt = Date()
    }
    
    // Codable conformance for UserDefaults storage
    enum CodingKeys: String, CodingKey {
        case id, name, phone, email, city
        case favoriteNeighborhoods, interests
        case createdAt, lastLoginAt
    }
    
    required init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        id = try c.decode(String.self, forKey: .id)
        name = try c.decode(String.self, forKey: .name)
        phone = try c.decode(String.self, forKey: .phone)
        email = try c.decodeIfPresent(String.self, forKey: .email)
        city = try c.decode(String.self, forKey: .city)
        favoriteNeighborhoods = try c.decode([String].self, forKey: .favoriteNeighborhoods)
        interests = try c.decode([String].self, forKey: .interests)
        createdAt = try c.decode(Date.self, forKey: .createdAt)
        lastLoginAt = try c.decode(Date.self, forKey: .lastLoginAt)
    }
    
    func encode(to encoder: Encoder) throws {
        var c = encoder.container(keyedBy: CodingKeys.self)
        try c.encode(id, forKey: .id)
        try c.encode(name, forKey: .name)
        try c.encode(phone, forKey: .phone)
        try c.encodeIfPresent(email, forKey: .email)
        try c.encode(city, forKey: .city)
        try c.encode(favoriteNeighborhoods, forKey: .favoriteNeighborhoods)
        try c.encode(interests, forKey: .interests)
        try c.encode(createdAt, forKey: .createdAt)
        try c.encode(lastLoginAt, forKey: .lastLoginAt)
    }
}

// MARK: - Favorite (SwiftData)

@Model
final class CachedFavorite {
    @Attribute(.unique) var placeId: String
    var addedAt: Date
    var note: String?
    var listName: String?  // Optional: which list it belongs to
    
    init(placeId: String, note: String? = nil, listName: String? = nil) {
        self.placeId = placeId
        self.addedAt = Date()
        self.note = note
        self.listName = listName
    }
}

// MARK: - Shareable List

@Model
final class ShareableList: Identifiable {
    @Attribute(.unique) var id: String
    var name: String
    var descriptionText: String?
    var placeIds: [String]
    var createdAt: Date
    var isPublic: Bool
    
    init(name: String, description: String? = nil, placeIds: [String] = []) {
        self.id = UUID().uuidString
        self.name = name
        self.descriptionText = description
        self.placeIds = placeIds
        self.createdAt = Date()
        self.isPublic = false
    }
    
    /// Generate shareable URL
    var shareURL: URL? {
        let ids = placeIds.joined(separator: ",")
        return URL(string: "https://wain-nrooh.com/list?ids=\(ids)&name=\(name.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")")
    }
}
