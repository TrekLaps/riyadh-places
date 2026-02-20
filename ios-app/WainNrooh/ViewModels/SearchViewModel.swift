// SearchViewModel.swift
// ViewModel البحث — بحث AI بالعربي مع فلاتر

import Foundation
import Combine

// MARK: - ViewModel البحث

/// ViewModel البحث الذكي — يدير البحث والفلاتر والاقتراحات
@MainActor
final class SearchViewModel: ObservableObject {
    
    // MARK: - خصائص منشورة
    
    /// نص البحث
    @Published var searchText: String = ""
    
    /// نتائج البحث
    @Published var searchResults: [Place] = []
    
    /// اقتراحات البحث
    @Published var suggestions: [SearchSuggestion] = []
    
    /// حالة التحميل
    @Published var isSearching: Bool = false
    
    /// هل تم البحث؟
    @Published var hasSearched: Bool = false
    
    /// رسالة الخطأ
    @Published var errorMessage: String?
    
    // MARK: - الفلاتر
    
    /// التصنيف المختار
    @Published var selectedCategory: PlaceCategory?
    
    /// الحي المختار
    @Published var selectedNeighborhood: String?
    
    /// الحد الأدنى للتقييم
    @Published var minRating: Double?
    
    /// نطاق السعر
    @Published var selectedPriceRange: String?
    
    /// خيار الترتيب
    @Published var sortOption: PlaceSortOption = .rating
    
    /// هل الفلاتر نشطة؟
    var hasActiveFilters: Bool {
        selectedCategory != nil ||
        selectedNeighborhood != nil ||
        minRating != nil ||
        selectedPriceRange != nil
    }
    
    /// عدد الفلاتر النشطة
    var activeFilterCount: Int {
        var count = 0
        if selectedCategory != nil { count += 1 }
        if selectedNeighborhood != nil { count += 1 }
        if minRating != nil { count += 1 }
        if selectedPriceRange != nil { count += 1 }
        return count
    }
    
    // MARK: - خدمات
    
    private let searchService = SearchService.shared
    private var searchTask: Task<Void, Never>?
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - تهيئة
    
    init() {
        setupSearchDebounce()
    }
    
    /// إعداد البحث التلقائي مع تأخير
    private func setupSearchDebounce() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .removeDuplicates()
            .sink { [weak self] query in
                Task {
                    if query.count >= AppConfig.minSearchLength {
                        await self?.loadSuggestions(for: query)
                    } else {
                        self?.suggestions = []
                    }
                }
            }
            .store(in: &cancellables)
    }
    
    // MARK: - البحث
    
    /// تنفيذ البحث
    func performSearch() async {
        let query = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !query.isEmpty || hasActiveFilters else { return }
        
        // إلغاء البحث السابق
        searchTask?.cancel()
        
        isSearching = true
        hasSearched = true
        errorMessage = nil
        suggestions = []
        
        searchTask = Task {
            do {
                let result = try await searchService.search(
                    query: query,
                    category: selectedCategory,
                    neighborhood: selectedNeighborhood
                )
                
                guard !Task.isCancelled else { return }
                
                searchResults = result.places
                
                // تحديث الفئة المكتشفة إذا ما تم تحديدها
                if selectedCategory == nil, let detected = result.detectedCategory {
                    selectedCategory = detected
                }
                
            } catch {
                guard !Task.isCancelled else { return }
                AppConfig.debugLog("❌ فشل البحث: \(error)")
                errorMessage = "فشل البحث — جرب مرة ثانية"
                searchResults = []
            }
            
            isSearching = false
        }
    }
    
    /// تحميل الاقتراحات
    private func loadSuggestions(for query: String) async {
        do {
            let results = try await searchService.suggest(query: query)
            suggestions = results
        } catch {
            suggestions = []
        }
    }
    
    /// اختيار اقتراح
    func selectSuggestion(_ suggestion: SearchSuggestion) {
        searchText = suggestion.text
        if let category = suggestion.category {
            selectedCategory = category
        }
        suggestions = []
        
        Task {
            await performSearch()
        }
    }
    
    // MARK: - الفلاتر
    
    /// مسح كل الفلاتر
    func clearFilters() {
        selectedCategory = nil
        selectedNeighborhood = nil
        minRating = nil
        selectedPriceRange = nil
        sortOption = .rating
    }
    
    /// مسح البحث بالكامل
    func clearSearch() {
        searchText = ""
        searchResults = []
        suggestions = []
        hasSearched = false
        errorMessage = nil
        clearFilters()
    }
    
    // MARK: - البحث الأخير
    
    /// عمليات البحث الأخيرة
    var recentSearches: [String] {
        searchService.recentSearches
    }
    
    /// البحث الشائع
    var popularSearches: [String] {
        searchService.popularSearches
    }
    
    /// مسح البحث الأخير
    func clearRecentSearches() {
        searchService.clearRecentSearches()
    }
    
    /// البحث من النص الأخير
    func searchFromRecent(_ text: String) {
        searchText = text
        Task {
            await performSearch()
        }
    }
}
