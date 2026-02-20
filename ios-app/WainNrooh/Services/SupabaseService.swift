// SupabaseService.swift
// خدمة Supabase — الاتصال بالسيرفر والـ API

import Foundation
import Combine

// MARK: - خدمة Supabase

/// خدمة الاتصال بـ Supabase — الطبقة الأساسية لكل استعلامات الـ API
final class SupabaseService: @unchecked Sendable {
    
    // MARK: - Singleton
    
    static let shared = SupabaseService()
    
    // MARK: - خصائص
    
    private let baseURL: String
    private let apiKey: String
    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder
    
    /// التوكن الحالي (JWT) — nil يعني مجهول
    private var accessToken: String?
    
    // MARK: - تهيئة
    
    private init() {
        self.baseURL = AppConfig.supabaseURL
        self.apiKey = AppConfig.supabaseAnonKey
        
        // إعداد URLSession مع timeout مناسب
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        config.waitsForConnectivity = true
        config.httpAdditionalHeaders = [
            "apikey": AppConfig.supabaseAnonKey,
            "Content-Type": "application/json",
            "Accept": "application/json"
        ]
        self.session = URLSession(configuration: config)
        
        // إعداد الـ decoder مع snake_case
        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder.dateDecodingStrategy = .iso8601
        
        // إعداد الـ encoder
        self.encoder = JSONEncoder()
        self.encoder.keyEncodingStrategy = .convertToSnakeCase
        self.encoder.dateEncodingStrategy = .iso8601
    }
    
    // MARK: - طلبات HTTP
    
    /// طلب GET
    func get<T: Decodable>(
        path: String,
        queryItems: [URLQueryItem] = []
    ) async throws -> T {
        let request = try buildRequest(
            method: "GET",
            path: path,
            queryItems: queryItems
        )
        return try await execute(request)
    }
    
    /// طلب POST
    func post<T: Decodable, B: Encodable>(
        path: String,
        body: B
    ) async throws -> T {
        var request = try buildRequest(method: "POST", path: path)
        request.httpBody = try encoder.encode(body)
        return try await execute(request)
    }
    
    /// طلب POST بدون جسم
    func post<T: Decodable>(path: String) async throws -> T {
        let request = try buildRequest(method: "POST", path: path)
        return try await execute(request)
    }
    
    /// طلب PATCH
    func patch<T: Decodable, B: Encodable>(
        path: String,
        body: B,
        queryItems: [URLQueryItem] = []
    ) async throws -> T {
        var request = try buildRequest(
            method: "PATCH",
            path: path,
            queryItems: queryItems
        )
        request.httpBody = try encoder.encode(body)
        return try await execute(request)
    }
    
    /// طلب DELETE
    func delete(
        path: String,
        queryItems: [URLQueryItem] = []
    ) async throws {
        let request = try buildRequest(
            method: "DELETE",
            path: path,
            queryItems: queryItems
        )
        let (_, response) = try await session.data(for: request)
        try validateResponse(response)
    }
    
    /// استدعاء RPC (دالة مخزنة في PostgreSQL)
    func rpc<T: Decodable>(
        functionName: String,
        params: [String: Any] = [:]
    ) async throws -> T {
        let path = "/rest/v1/rpc/\(functionName)"
        var request = try buildRequest(method: "POST", path: path)
        request.httpBody = try JSONSerialization.data(withJSONObject: params)
        return try await execute(request)
    }
    
    // MARK: - استعلام Supabase REST
    
    /// استعلام جدول مع فلاتر
    func from(
        _ table: String,
        select: String = "*",
        filters: [SupabaseFilter] = [],
        order: String? = nil,
        ascending: Bool = true,
        limit: Int? = nil,
        offset: Int? = nil
    ) async throws -> Data {
        var queryItems: [URLQueryItem] = [
            URLQueryItem(name: "select", value: select)
        ]
        
        // إضافة الفلاتر
        for filter in filters {
            queryItems.append(filter.toQueryItem())
        }
        
        // الترتيب
        if let order {
            queryItems.append(URLQueryItem(
                name: "order",
                value: "\(order).\(ascending ? "asc" : "desc")"
            ))
        }
        
        // الحد والإزاحة
        if let limit {
            queryItems.append(URLQueryItem(name: "limit", value: "\(limit)"))
        }
        if let offset {
            queryItems.append(URLQueryItem(name: "offset", value: "\(offset)"))
        }
        
        let request = try buildRequest(
            method: "GET",
            path: "/rest/v1/\(table)",
            queryItems: queryItems
        )
        
        let (data, response) = try await session.data(for: request)
        try validateResponse(response)
        return data
    }
    
    // MARK: - مصادقة
    
    /// تحديث توكن الوصول
    func setAccessToken(_ token: String?) {
        self.accessToken = token
    }
    
    // MARK: - بناء الطلب
    
    private func buildRequest(
        method: String,
        path: String,
        queryItems: [URLQueryItem] = []
    ) throws -> URLRequest {
        guard var components = URLComponents(string: baseURL + path) else {
            throw SupabaseError.invalidURL
        }
        
        if !queryItems.isEmpty {
            components.queryItems = queryItems
        }
        
        guard let url = components.url else {
            throw SupabaseError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue(apiKey, forHTTPHeaderField: "apikey")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        
        // إضافة التوكن إذا موجود
        if let token = accessToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        } else {
            request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        }
        
        return request
    }
    
    /// تنفيذ الطلب وفك التشفير
    private func execute<T: Decodable>(_ request: URLRequest) async throws -> T {
        let (data, response) = try await session.data(for: request)
        try validateResponse(response)
        
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            AppConfig.debugLog("❌ فشل فك التشفير: \(error)")
            AppConfig.debugLog("📦 البيانات: \(String(data: data, encoding: .utf8) ?? "غير قابلة للقراءة")")
            throw SupabaseError.decodingError(error)
        }
    }
    
    /// التحقق من الاستجابة
    private func validateResponse(_ response: URLResponse) throws {
        guard let httpResponse = response as? HTTPURLResponse else {
            throw SupabaseError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            return // نجاح
        case 401:
            throw SupabaseError.unauthorized
        case 403:
            throw SupabaseError.forbidden
        case 404:
            throw SupabaseError.notFound
        case 429:
            throw SupabaseError.rateLimited
        case 500...599:
            throw SupabaseError.serverError(httpResponse.statusCode)
        default:
            throw SupabaseError.httpError(httpResponse.statusCode)
        }
    }
}

// MARK: - فلتر Supabase

/// فلتر لاستعلامات Supabase REST
struct SupabaseFilter {
    let column: String
    let op: FilterOperator
    let value: String
    
    enum FilterOperator: String {
        case eq     // يساوي
        case neq    // لا يساوي
        case gt     // أكبر من
        case gte    // أكبر من أو يساوي
        case lt     // أصغر من
        case lte    // أصغر من أو يساوي
        case like   // يشبه (case sensitive)
        case ilike  // يشبه (case insensitive)
        case `in`   // ضمن قائمة
        case cs     // يحتوي (array)
        case fts    // بحث نصي كامل
    }
    
    func toQueryItem() -> URLQueryItem {
        URLQueryItem(name: column, value: "\(op.rawValue).\(value)")
    }
}

// MARK: - أخطاء Supabase

/// أنواع الأخطاء الممكنة من Supabase
enum SupabaseError: LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case forbidden
    case notFound
    case rateLimited
    case serverError(Int)
    case httpError(Int)
    case decodingError(Error)
    case networkError(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL: return "رابط غير صالح"
        case .invalidResponse: return "استجابة غير صالحة من السيرفر"
        case .unauthorized: return "غير مصرح — سجل دخولك"
        case .forbidden: return "ممنوع — ما عندك صلاحية"
        case .notFound: return "غير موجود"
        case .rateLimited: return "طلبات كثيرة — انتظر شوي"
        case .serverError(let code): return "خطأ في السيرفر (\(code))"
        case .httpError(let code): return "خطأ HTTP (\(code))"
        case .decodingError: return "خطأ في قراءة البيانات"
        case .networkError: return "مشكلة في الاتصال — تأكد من الإنترنت"
        }
    }
}
