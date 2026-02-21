// SearchService.swift
// خدمة البحث — Arabic-aware FTS with debounce

import Foundation
import Combine

@MainActor
class SearchService: ObservableObject {
    @Published var query = ""
    @Published var results: [Place] = []
    @Published var isSearching = false
    @Published var recentSearches: [String] = []
    
    private var cancellables = Set<AnyCancellable>()
    private let placesService = PlacesService.shared
    
    init() {
        // Debounced search
        $query
            .debounce(for: .milliseconds(AppConfig.searchDebounceMs), scheduler: RunLoop.main)
            .removeDuplicates()
            .sink { [weak self] q in
                self?.performSearch(q)
            }
            .store(in: &cancellables)
        
        // Load recent searches
        recentSearches = UserDefaults.standard.stringArray(forKey: "recentSearches") ?? []
    }
    
    func performSearch(_ query: String) {
        guard !query.trimmingCharacters(in: .whitespaces).isEmpty else {
            results = []
            isSearching = false
            return
        }
        
        isSearching = true
        
        // Normalize Arabic (remove tashkeel, normalize hamza)
        let normalized = query.normalizedArabic
        results = placesService.search(query: normalized, maxResults: 50)
        isSearching = false
    }
    
    func addToRecent(_ query: String) {
        recentSearches.removeAll { $0 == query }
        recentSearches.insert(query, at: 0)
        if recentSearches.count > 10 { recentSearches = Array(recentSearches.prefix(10)) }
        UserDefaults.standard.set(recentSearches, forKey: "recentSearches")
    }
    
    func clearRecent() {
        recentSearches = []
        UserDefaults.standard.removeObject(forKey: "recentSearches")
    }
}
