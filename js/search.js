// ===== وين نروح بالرياض — Enhanced Search Engine =====
(function() {
  'use strict';

  // Arabic normalization map
  const ARABIC_NORMALIZE = {
    'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا',
    'ة': 'ه',
    'ى': 'ي',
    'ؤ': 'و',
    'ئ': 'ي',
    // Diacritics removal
    '\u064B': '', '\u064C': '', '\u064D': '', '\u064E': '',
    '\u064F': '', '\u0650': '', '\u0651': '', '\u0652': '',
  };

  // Normalize Arabic text for search
  function normalizeArabic(text) {
    if (!text) return '';
    let result = text.toLowerCase();
    for (const [from, to] of Object.entries(ARABIC_NORMALIZE)) {
      result = result.split(from).join(to);
    }
    // Remove tatweel
    result = result.replace(/\u0640/g, '');
    // Normalize whitespace
    result = result.replace(/\s+/g, ' ').trim();
    return result;
  }

  // Build search index from places data
  function buildSearchIndex(places) {
    return places.map(place => {
      // Create a combined searchable text
      const fields = [
        place.name_ar,
        place.name_en,
        place.description_ar,
        place.neighborhood,
        place.neighborhood_en,
        place.category,
        place.category_ar,
        place.category_en,
        place.cuisine,
        place.review_quote_ar || place.review_quote,
        ...(place.audience || []),
        ...(place.perfect_for || []),
        place.district,
      ].filter(Boolean);

      const normalizedText = normalizeArabic(fields.join(' '));
      const normalizedName = normalizeArabic(place.name_ar + ' ' + (place.name_en || ''));

      return {
        place: place,
        text: normalizedText,
        name: normalizedName,
        neighborhood: normalizeArabic(place.neighborhood || ''),
        category: normalizeArabic(place.category || ''),
      };
    });
  }

  // Search with scoring
  function searchPlaces(index, query, filters) {
    if (!query && !filters) return index.map(i => ({ place: i.place, score: 0 }));

    const normalizedQuery = normalizeArabic(query || '');
    const queryTokens = normalizedQuery.split(/\s+/).filter(t => t.length > 0);

    let results = index.map(item => {
      let score = 0;

      if (queryTokens.length > 0) {
        // Exact name match — highest score
        if (item.name.includes(normalizedQuery)) {
          score += 100;
        }

        // Token matching
        for (const token of queryTokens) {
          // Name contains token
          if (item.name.includes(token)) score += 30;
          // Neighborhood match
          if (item.neighborhood.includes(token)) score += 15;
          // Category match
          if (item.category.includes(token)) score += 15;
          // General text match
          if (item.text.includes(token)) score += 5;
        }

        // Bonus for matching all tokens
        if (queryTokens.every(t => item.text.includes(t))) {
          score += 20;
        }
      } else {
        score = 1; // No query = show all
      }

      return { place: item.place, score: score };
    });

    // Apply filters
    if (filters) {
      if (filters.category) {
        const cat = normalizeArabic(filters.category);
        results = results.filter(r => normalizeArabic(r.place.category) === cat || normalizeArabic(r.place.category_ar) === cat);
      }
      if (filters.neighborhood) {
        const hood = normalizeArabic(filters.neighborhood);
        results = results.filter(r => normalizeArabic(r.place.neighborhood).includes(hood));
      }
      if (filters.price) {
        results = results.filter(r => r.place.price_level === filters.price);
      }
      if (filters.audience) {
        const aud = normalizeArabic(filters.audience);
        results = results.filter(r => (r.place.audience || []).some(a => normalizeArabic(a).includes(aud)));
      }
      if (filters.perfect_for) {
        const pf = normalizeArabic(filters.perfect_for);
        results = results.filter(r => (r.place.perfect_for || []).some(p => normalizeArabic(p).includes(pf)));
      }
      if (filters.isFree) {
        results = results.filter(r => r.place.is_free);
      }
      if (filters.minRating) {
        results = results.filter(r => r.place.google_rating >= filters.minRating);
      }
    }

    // Filter out zero-score when query present
    if (queryTokens.length > 0) {
      results = results.filter(r => r.score > 0);
    }

    return results;
  }

  // Sort results
  function sortResults(results, sortBy) {
    const sorted = [...results];
    switch (sortBy) {
      case 'relevance':
        sorted.sort((a, b) => b.score - a.score);
        break;
      case 'rating-desc':
        sorted.sort((a, b) => b.place.google_rating - a.place.google_rating || b.place.review_count - a.place.review_count);
        break;
      case 'reviews-desc':
        sorted.sort((a, b) => b.place.review_count - a.place.review_count);
        break;
      case 'price-asc':
        sorted.sort((a, b) => (a.place.price_level || '').length - (b.place.price_level || '').length);
        break;
      case 'price-desc':
        sorted.sort((a, b) => (b.place.price_level || '').length - (a.place.price_level || '').length);
        break;
      case 'name':
        sorted.sort((a, b) => (a.place.name_ar || '').localeCompare(b.place.name_ar || '', 'ar'));
        break;
      default:
        sorted.sort((a, b) => b.score - a.score || b.place.google_rating - a.place.google_rating);
    }
    return sorted;
  }

  // Auto-suggest — returns top matches for names & neighborhoods
  function autoSuggest(index, query, limit) {
    if (!query || query.length < 2) return [];
    const q = normalizeArabic(query);
    const suggestions = [];
    const seen = new Set();

    // Place name matches first
    for (const item of index) {
      if (suggestions.length >= (limit || 5)) break;
      if (item.name.includes(q)) {
        const key = 'place:' + item.place.id;
        if (!seen.has(key)) {
          seen.add(key);
          suggestions.push({
            type: 'place',
            text: item.place.name_ar,
            sub: item.place.neighborhood + ' · ' + (item.place.category_ar || item.place.category),
            id: item.place.id,
            icon: categoryIcons[item.place.category] || '📍'
          });
        }
      }
    }

    // Neighborhood matches
    if (suggestions.length < (limit || 5)) {
      const hoodMatches = new Set();
      for (const item of index) {
        if (item.neighborhood.includes(q) && !hoodMatches.has(item.place.neighborhood)) {
          hoodMatches.add(item.place.neighborhood);
          if (suggestions.length >= (limit || 5)) break;
          suggestions.push({
            type: 'neighborhood',
            text: item.place.neighborhood,
            sub: 'حي',
            icon: '🏘️'
          });
        }
      }
    }

    // Category matches
    if (suggestions.length < (limit || 5)) {
      const catMatches = new Set();
      for (const item of index) {
        const cat = item.place.category_ar || item.place.category;
        if (item.category.includes(q) && !catMatches.has(cat)) {
          catMatches.add(cat);
          if (suggestions.length >= (limit || 5)) break;
          suggestions.push({
            type: 'category',
            text: cat,
            sub: 'قسم',
            icon: categoryIcons[item.place.category] || '📂'
          });
        }
      }
    }

    return suggestions;
  }

  // Extract unique values for filter chips
  function extractFilterOptions(places) {
    const categories = new Map();
    const neighborhoods = new Map();
    const audiences = new Map();
    const perfectFor = new Map();
    const prices = new Set();

    places.forEach(p => {
      const cat = p.category_ar || p.category;
      categories.set(cat, (categories.get(cat) || 0) + 1);
      neighborhoods.set(p.neighborhood, (neighborhoods.get(p.neighborhood) || 0) + 1);
      (p.audience || []).forEach(a => audiences.set(a, (audiences.get(a) || 0) + 1));
      (p.perfect_for || []).forEach(pf => perfectFor.set(pf, (perfectFor.get(pf) || 0) + 1));
      if (p.price_level) prices.add(p.price_level);
    });

    // Sort by frequency
    const sortMap = (m) => [...m.entries()].sort((a, b) => b[1] - a[1]).map(([k, v]) => ({ label: k, count: v }));

    return {
      categories: sortMap(categories),
      neighborhoods: sortMap(neighborhoods).slice(0, 30),
      audiences: sortMap(audiences),
      perfectFor: sortMap(perfectFor),
      prices: ['$', '$$', '$$$', '$$$$', 'مجاني'].filter(p => prices.has(p))
    };
  }

  // categoryIcons reference (from main.js)
  const categoryIcons = {
    'cafe': '☕', 'restaurant': '🍽️', 'activity': '🎭',
    'تسوق': '🛍️', 'طبيعة': '🏞️', 'كافيه': '☕',
    'مطعم': '🍽️', 'ترفيه': '🎭', 'حلويات': '🍰',
    'فعاليات': '🎪', 'مولات': '🏬', 'متاحف': '🏛️',
    'شاليه': '🏡', 'فنادق': '🏨'
  };

  // Public API
  window.WaynSearch = {
    normalizeArabic,
    buildSearchIndex,
    searchPlaces,
    sortResults,
    autoSuggest,
    extractFilterOptions,
    categoryIcons
  };
})();
