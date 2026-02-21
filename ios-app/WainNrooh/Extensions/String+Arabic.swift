// String+Arabic.swift
// Arabic text normalization for search

import Foundation

extension String {
    /// Normalize Arabic text: remove tashkeel, normalize hamza/alef
    var normalizedArabic: String {
        var result = self
        
        // Remove tashkeel (diacritics)
        let tashkeel = "ًٌٍَُِّْٰ"
        result = result.filter { !tashkeel.contains($0) }
        
        // Normalize alef variants → ا
        result = result.replacingOccurrences(of: "أ", with: "ا")
        result = result.replacingOccurrences(of: "إ", with: "ا")
        result = result.replacingOccurrences(of: "آ", with: "ا")
        result = result.replacingOccurrences(of: "ٱ", with: "ا")
        
        // Normalize taa marbuta → haa
        result = result.replacingOccurrences(of: "ة", with: "ه")
        
        // Normalize yaa
        result = result.replacingOccurrences(of: "ى", with: "ي")
        
        return result
    }
    
    /// Check if string contains Arabic characters
    var isArabic: Bool {
        rangeOfCharacter(from: CharacterSet(charactersIn: "\u{0600}"..."\u{06FF}")) != nil
    }
}
