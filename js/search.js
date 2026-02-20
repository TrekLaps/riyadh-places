// ===== وين نروح بالرياض — Search Engine v3 =====
// Pure JS, Arabic-optimized, <50ms search on 4000+ places
(function() {
  'use strict';

  // ── Arabic Normalization ──
  var NORM = {};
  'أإآٱ'.split('').forEach(function(c){ NORM[c]='ا'; });
  NORM['ة']='ه'; NORM['ى']='ي'; NORM['ؤ']='و'; NORM['ئ']='ي';
  // Diacritics
  ['\u064B','\u064C','\u064D','\u064E','\u064F','\u0650','\u0651','\u0652','\u0670'].forEach(function(c){ NORM[c]=''; });

  function norm(text) {
    if (!text) return '';
    var r = '', c, i, t = text.toLowerCase();
    for (i = 0; i < t.length; i++) {
      c = t[i];
      if (c === '\u0640') continue; // tatweel
      r += (NORM[c] !== undefined ? NORM[c] : c);
    }
    return r.replace(/\s+/g, ' ').trim();
  }

  // ── Expand Light Fields ──
  function expand(p) {
    return {
      id: p.id, name_ar: p.n, name_en: p.ne,
      category: p.c, category_ar: p.ca || p.c,
      neighborhood: p.h, neighborhood_en: p.he,
      description_ar: p.d || '',
      google_rating: p.r || 0, review_count: p.rc || 0,
      price_level: p.p || '',
      lat: p.la, lng: p.lo,
      trending: !!p.tr, is_new: !!p.nw, is_free: !!p.fr,
      audience: p.au || [], perfect_for: p.pf || [],
      google_maps_url: p.gm || ''
    };
  }

  // ── Build Index ──
  function buildSearchIndex(rawPlaces) {
    var idx = new Array(rawPlaces.length);
    for (var i = 0; i < rawPlaces.length; i++) {
      var p = rawPlaces[i].name_ar ? rawPlaces[i] : expand(rawPlaces[i]);
      var fields = [p.name_ar, p.name_en, p.description_ar,
        p.neighborhood, p.neighborhood_en, p.category,
        p.category_ar].concat(p.audience || [], p.perfect_for || []);
      var combined = '';
      for (var j = 0; j < fields.length; j++) {
        if (fields[j]) combined += fields[j] + ' ';
      }
      idx[i] = {
        place: p,
        text: norm(combined),
        name: norm((p.name_ar||'') + ' ' + (p.name_en||'')),
        hood: norm(p.neighborhood || ''),
        cat: norm(p.category || '')
      };
    }
    return idx;
  }

  // ── Search with Scoring ──
  function searchPlaces(index, query, filters) {
    var nq = norm(query || '');
    var tokens = nq ? nq.split(/\s+/).filter(function(t){ return t.length > 0; }) : [];
    var hasQuery = tokens.length > 0;
    var hasFilters = filters && Object.keys(filters).some(function(k){ return !!filters[k]; });
    var results = [];

    for (var i = 0; i < index.length; i++) {
      var item = index[i];
      var p = item.place;
      var score = 0;

      if (hasQuery) {
        // Full query in name = highest
        if (item.name.indexOf(nq) !== -1) score += 100;

        var allMatch = true;
        for (var t = 0; t < tokens.length; t++) {
          var tok = tokens[t];
          var tokFound = false;
          // Name match
          if (item.name.indexOf(tok) !== -1) { score += 30; tokFound = true; }
          // Neighborhood match
          if (item.hood.indexOf(tok) !== -1) { score += 15; tokFound = true; }
          // Category match (also check prefix for plural forms like شاليهات→شاليه)
          if (item.cat && (item.cat.indexOf(tok) !== -1 || tok.indexOf(item.cat) !== -1)) { score += 15; tokFound = true; }

          if (item.text.indexOf(tok) !== -1) {
            score += 5; tokFound = true;
          } else if (tok.length >= 4) {
            // Stem match: handle Arabic plurals (شاليهات→شاليه)
            // Try removing common suffixes: ات, ين, ون, ة
            var stems = [tok.slice(0,-2), tok.slice(0,-1)];
            for (var si = 0; si < stems.length; si++) {
              if (stems[si].length >= 4 && item.text.indexOf(stems[si]) !== -1) {
                score += 3; tokFound = true; break;
              }
            }
          }
          if (!tokFound) allMatch = false;
        }
        if (allMatch && tokens.length > 1) score += 20;
        if (score === 0) continue;
      } else {
        score = 1;
      }

      // Apply filters inline
      if (hasFilters) {
        if (filters.category) {
          var fc = norm(filters.category);
          if (norm(p.category) !== fc && norm(p.category_ar) !== fc) continue;
        }
        if (filters.neighborhood) {
          if (norm(p.neighborhood).indexOf(norm(filters.neighborhood)) === -1) continue;
        }
        if (filters.price) {
          if (p.price_level !== filters.price) continue;
        }
        if (filters.audience) {
          var fa = norm(filters.audience);
          var found = false;
          var aud = p.audience || [];
          for (var a = 0; a < aud.length; a++) {
            if (norm(aud[a]).indexOf(fa) !== -1) { found = true; break; }
          }
          if (!found) continue;
        }
        if (filters.perfect_for) {
          var fp = norm(filters.perfect_for);
          var found2 = false;
          var pfs = p.perfect_for || [];
          for (var pfi = 0; pfi < pfs.length; pfi++) {
            if (norm(pfs[pfi]).indexOf(fp) !== -1) { found2 = true; break; }
          }
          if (!found2) continue;
        }
        if (filters.minRating && p.google_rating < filters.minRating) continue;
      }

      // Rating boost
      score += (p.google_rating || 0) * 2;
      if (p.trending) score += 5;

      results.push({ place: p, score: score });
    }

    return results;
  }

  // ── Sort ──
  function sortResults(results, sortBy) {
    var s = results.slice();
    switch (sortBy) {
      case 'rating-desc':
        s.sort(function(a,b){ return (b.place.google_rating||0)-(a.place.google_rating||0) || (b.place.review_count||0)-(a.place.review_count||0); });
        break;
      case 'reviews-desc':
        s.sort(function(a,b){ return (b.place.review_count||0)-(a.place.review_count||0); });
        break;
      case 'price-asc':
        s.sort(function(a,b){ return (a.place.price_level||'').length-(b.place.price_level||'').length; });
        break;
      case 'price-desc':
        s.sort(function(a,b){ return (b.place.price_level||'').length-(a.place.price_level||'').length; });
        break;
      case 'name':
        s.sort(function(a,b){ return (a.place.name_ar||'').localeCompare(b.place.name_ar||'','ar'); });
        break;
      default: // relevance
        s.sort(function(a,b){ return b.score-a.score; });
    }
    return s;
  }

  // ── Auto-Suggest ──
  function autoSuggest(index, query, limit) {
    if (!query || query.length < 2) return [];
    var q = norm(query);
    limit = limit || 5;
    var out = [], seen = {};

    // Places by name
    for (var i = 0; i < index.length && out.length < limit; i++) {
      var item = index[i];
      if (item.name.indexOf(q) !== -1) {
        var k = item.place.id;
        if (!seen[k]) {
          seen[k] = 1;
          out.push({
            type: 'place', text: item.place.name_ar,
            sub: (item.place.neighborhood||'') + ' · ' + (item.place.category_ar||item.place.category),
            id: item.place.id,
            icon: catIcons[item.place.category] || '📍',
            rating: item.place.google_rating
          });
        }
      }
    }

    // Neighborhoods
    if (out.length < limit) {
      var hoods = {};
      for (var j = 0; j < index.length && out.length < limit; j++) {
        var h = index[j].place.neighborhood;
        if (index[j].hood.indexOf(q) !== -1 && !hoods[h]) {
          hoods[h] = 1;
          out.push({ type: 'neighborhood', text: h, sub: 'حي', icon: '🏘️' });
        }
      }
    }

    // Categories
    if (out.length < limit) {
      var cats = {};
      for (var c = 0; c < index.length && out.length < limit; c++) {
        var cat = index[c].place.category_ar || index[c].place.category;
        if (index[c].cat.indexOf(q) !== -1 && !cats[cat]) {
          cats[cat] = 1;
          out.push({ type: 'category', text: cat, sub: 'قسم', icon: catIcons[index[c].place.category] || '📂' });
        }
      }
    }

    return out;
  }

  // ── Filter Options ──
  function extractFilterOptions(places) {
    var catMap = {}, hoodMap = {}, audMap = {}, pfMap = {}, priceSet = {};
    for (var i = 0; i < places.length; i++) {
      var p = places[i].name_ar ? places[i] : expand(places[i]);
      var cat = p.category_ar || p.category;
      catMap[cat] = (catMap[cat]||0) + 1;
      if (p.neighborhood) hoodMap[p.neighborhood] = (hoodMap[p.neighborhood]||0) + 1;
      var aud = p.audience || [];
      for (var a = 0; a < aud.length; a++) audMap[aud[a]] = (audMap[aud[a]]||0) + 1;
      var pf = p.perfect_for || [];
      for (var f = 0; f < pf.length; f++) pfMap[pf[f]] = (pfMap[pf[f]]||0) + 1;
      if (p.price_level) priceSet[p.price_level] = 1;
    }

    function toSorted(m) {
      return Object.keys(m).map(function(k){ return {label:k,count:m[k]}; })
        .sort(function(a,b){ return b.count-a.count; });
    }

    return {
      categories: toSorted(catMap),
      neighborhoods: toSorted(hoodMap).slice(0, 30),
      audiences: toSorted(audMap),
      perfectFor: toSorted(pfMap),
      prices: ['$','$$','$$$','$$$$','مجاني'].filter(function(p){ return priceSet[p]; })
    };
  }

  // ── Recent Searches ──
  var RECENT_KEY = 'wayn_recent_searches';
  function getRecent() {
    try { return JSON.parse(localStorage.getItem(RECENT_KEY)) || []; }
    catch(e) { return []; }
  }
  function saveRecent(query) {
    if (!query || query.length < 2) return;
    var list = getRecent().filter(function(q){ return q !== query; });
    list.unshift(query);
    if (list.length > 8) list = list.slice(0, 8);
    try { localStorage.setItem(RECENT_KEY, JSON.stringify(list)); } catch(e){}
  }
  function clearRecent() {
    try { localStorage.removeItem(RECENT_KEY); } catch(e){}
  }

  // ── Category Icons ──
  var catIcons = {
    'cafe':'☕','restaurant':'🍽️','activity':'🎭',
    'تسوق':'🛍️','طبيعة':'🏞️','كافيه':'☕',
    'مطعم':'🍽️','ترفيه':'🎭','حلويات':'🍰',
    'فعاليات':'🎪','مولات':'🏬','متاحف':'🏛️',
    'شاليه':'🏡','فنادق':'🏨'
  };

  // ── Public API ──
  window.WaynSearch = {
    normalizeArabic: norm,
    buildSearchIndex: buildSearchIndex,
    searchPlaces: searchPlaces,
    sortResults: sortResults,
    autoSuggest: autoSuggest,
    extractFilterOptions: extractFilterOptions,
    expand: expand,
    categoryIcons: catIcons,
    getRecent: getRecent,
    saveRecent: saveRecent,
    clearRecent: clearRecent
  };
})();
