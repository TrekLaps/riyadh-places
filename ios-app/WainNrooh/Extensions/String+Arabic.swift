// String+Arabic.swift
// إضافات النصوص — معالجة النصوص العربية والتطبيع

import Foundation

// MARK: - معالجة النصوص العربية

extension String {
    
    /// تطبيع النص العربي — إزالة التشكيل وتوحيد الأحرف
    var arabicNormalized: String {
        var result = self
        
        // إزالة التشكيل (حركات)
        result = result.removingDiacritics
        
        // توحيد الألف
        result = result
            .replacingOccurrences(of: "إ", with: "ا")
            .replacingOccurrences(of: "أ", with: "ا")
            .replacingOccurrences(of: "آ", with: "ا")
            .replacingOccurrences(of: "ٱ", with: "ا")
        
        // توحيد التاء المربوطة
        result = result.replacingOccurrences(of: "ة", with: "ه")
        
        // إزالة التطويل
        result = result.replacingOccurrences(of: "ـ", with: "")
        
        // توحيد الياء
        result = result.replacingOccurrences(of: "ى", with: "ي")
        
        // إزالة المسافات الزائدة
        result = result.components(separatedBy: .whitespaces)
            .filter { !$0.isEmpty }
            .joined(separator: " ")
        
        return result
    }
    
    /// إزالة التشكيل (الحركات)
    var removingDiacritics: String {
        // نطاق التشكيل العربي: U+0610 إلى U+065F
        let diacriticRange = Unicode.Scalar(0x0610)!...Unicode.Scalar(0x065F)
        return String(unicodeScalars.filter { !diacriticRange.contains($0) })
    }
    
    /// هل النص يحتوي على عربي؟
    var containsArabic: Bool {
        range(of: "\\p{Arabic}", options: .regularExpression) != nil
    }
    
    /// هل النص عربي بالكامل؟
    var isArabic: Bool {
        guard !isEmpty else { return false }
        let arabicAndSpaces = replacingOccurrences(of: " ", with: "")
        return arabicAndSpaces.range(of: "^[\\p{Arabic}\\s\\d\\p{P}]+$", options: .regularExpression) != nil
    }
    
    /// أول حرف (مفيد للأفاتار)
    var firstCharacter: String {
        guard let first = first else { return "?" }
        return String(first)
    }
    
    /// تقصير النص مع "..."
    func truncated(to length: Int) -> String {
        if count <= length { return self }
        return String(prefix(length)) + "..."
    }
    
    // MARK: - تحويلات سعودية
    
    /// تحويل الأرقام الإنجليزية إلى عربية
    var arabicDigits: String {
        let map: [Character: Character] = [
            "0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
            "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"
        ]
        return String(map { map[$0] ?? $0 })
    }
    
    /// تحويل الأرقام العربية إلى إنجليزية
    var englishDigits: String {
        let map: [Character: Character] = [
            "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
            "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9"
        ]
        return String(map { map[$0] ?? $0 })
    }
    
    /// تنسيق رقم الجوال السعودي
    var formattedSaudiPhone: String {
        let cleaned = englishDigits.replacingOccurrences(of: "[^0-9]", with: "", options: .regularExpression)
        
        if cleaned.hasPrefix("966") {
            let number = String(cleaned.dropFirst(3))
            return "+966 \(number.prefix(2)) \(number.dropFirst(2).prefix(3)) \(number.suffix(4))"
        } else if cleaned.hasPrefix("05") || cleaned.hasPrefix("5") {
            let number = cleaned.hasPrefix("0") ? String(cleaned.dropFirst()) : cleaned
            return "+966 \(number.prefix(2)) \(number.dropFirst(2).prefix(3)) \(number.suffix(4))"
        }
        
        return self
    }
    
    // MARK: - بحث ذكي
    
    /// البحث الذكي — يتعامل مع الاختلافات في الكتابة العربية
    func arabicSearchMatch(_ query: String) -> Bool {
        let normalizedSelf = self.arabicNormalized.lowercased()
        let normalizedQuery = query.arabicNormalized.lowercased()
        
        // بحث مباشر
        if normalizedSelf.contains(normalizedQuery) { return true }
        
        // بحث بالكلمات
        let queryWords = normalizedQuery.components(separatedBy: " ")
        return queryWords.allSatisfy { word in
            normalizedSelf.contains(word)
        }
    }
    
    // MARK: - تنسيق التاريخ
    
    /// تحويل من ISO 8601 إلى تاريخ عربي
    var arabicDate: String? {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: self) else { return nil }
        
        let displayFormatter = DateFormatter()
        displayFormatter.locale = Locale(identifier: "ar_SA")
        displayFormatter.dateStyle = .medium
        displayFormatter.timeStyle = .none
        return displayFormatter.string(from: date)
    }
    
    /// تحويل إلى "قبل X"
    var timeAgo: String? {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: self) else { return nil }
        
        let now = Date()
        let interval = now.timeIntervalSince(date)
        
        if interval < 60 {
            return "الحين"
        } else if interval < 3600 {
            let minutes = Int(interval / 60)
            return "قبل \(minutes) دقيقة"
        } else if interval < 86400 {
            let hours = Int(interval / 3600)
            return "قبل \(hours) ساعة"
        } else if interval < 604800 {
            let days = Int(interval / 86400)
            return "قبل \(days) يوم"
        } else if interval < 2592000 {
            let weeks = Int(interval / 604800)
            return "قبل \(weeks) أسبوع"
        } else {
            let months = Int(interval / 2592000)
            return "قبل \(months) شهر"
        }
    }
}

// MARK: - تنسيق الأرقام

extension Double {
    
    /// تنسيق كسعر بالريال
    var formattedSAR: String {
        if self == 0 { return "مجاني" }
        if self == floor(self) {
            return "\(Int(self)) ر.س"
        }
        return String(format: "%.1f ر.س", self)
    }
    
    /// تنسيق كتقييم
    var formattedRating: String {
        String(format: "%.1f", self)
    }
    
    /// تنسيق كمسافة
    var formattedDistance: String {
        if self < 1.0 {
            return "\(Int(self * 1000)) م"
        }
        return String(format: "%.1f كم", self)
    }
}

extension Int {
    
    /// تنسيق كعدد (مع تقصير للأعداد الكبيرة)
    var formattedCount: String {
        if self >= 1000000 {
            return String(format: "%.1fM", Double(self) / 1000000)
        } else if self >= 1000 {
            return String(format: "%.1fK", Double(self) / 1000)
        }
        return "\(self)"
    }
}
