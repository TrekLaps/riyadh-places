// ===== AI Search Engine — وين نروح بالرياض =====
// بحث ذكي بالعربي السعودي — client-side, no server needed
(function() {
  'use strict';

  // === Keyword Mappings (Arabic Saudi + English) ===
  const CATEGORY_KEYWORDS = {
    'مطعم': ['مطعم','مطاعم','أكل','عشاء','غداء','فطور','restaurant','restaurants','food','dinner','lunch','breakfast','dining'],
    'كافيه': ['كافيه','كوفي','قهوة','كابتشينو','لاتيه','كافيهات','cafe','coffee','cappuccino','latte','espresso','coffeeshop'],
    'ترفيه': ['ترفيه','ملاهي','ألعاب','سينما','بولينج','كارتنج','ترامبولين','entertainment','games','cinema','bowling','fun','activities','escape'],
    'حلويات': ['حلويات','حلا','كنافة','آيسكريم','دونات','كيك','شوكولاتة','dessert','sweets','ice cream','donuts','cake','chocolate','bakery'],
    'تسوق': ['تسوق','محلات','محل','shopping','shop','store','سوق'],
    'فنادق': ['فندق','فنادق','hotel','hotels','إقامة','نزل','accommodation'],
    'طبيعة': ['طبيعة','حديقة','حدائق','منتزه','وادي','تخييم','مشي','park','garden','nature','hiking','camping','trail','outdoor'],
    'شاليه': ['شاليه','شاليهات','استراحة','استراحات','مزرعة','chalet','resort','farm','glamping'],
    'فعاليات': ['فعالية','فعاليات','حفلة','حفلات','موسم','event','events','concert','festival','season'],
    'متاحف': ['متحف','متاحف','معرض','تاريخي','ثقافي','museum','gallery','historical','cultural','heritage'],
    'مولات': ['مول','مولات','مركز تجاري','mall','shopping center']
  };

  const CUISINE_KEYWORDS = {
    'ياباني': ['ياباني','سوشي','رامن','japanese','sushi','ramen'],
    'إيطالي': ['إيطالي','بيتزا','باستا','italian','pizza','pasta'],
    'لبناني': ['لبناني','مشاوي','حمص','lebanese','hummus','grill'],
    'سعودي': ['سعودي','كبسة','مندي','جريش','saudi','kabsa','mandi'],
    'هندي': ['هندي','كاري','بريياني','indian','curry','biryani'],
    'تركي': ['تركي','كباب','شاورما','turkish','kebab','shawarma'],
    'صيني': ['صيني','نودلز','chinese','noodles','dim sum'],
    'كوري': ['كوري','korean','bibimbap'],
    'مكسيكي': ['مكسيكي','تاكو','mexican','tacos','burrito'],
    'أمريكي': ['أمريكي','برجر','ستيك','american','burger','steak'],
    'بحري': ['بحري','سمك','أسماك','seafood','fish','shrimp'],
    'فطور': ['فطور','breakfast','brunch','eggs'],
    'برجر': ['برجر','burger','burgers','smash'],
    'بيتزا': ['بيتزا','pizza']
  };

  const PRICE_KEYWORDS = {
    '$': ['رخيص','اقتصادي','حلو السعر','ببلاش','مجاني','cheap','affordable','budget','free','inexpensive'],
    '$$': ['متوسط','معقول','عادي','moderate','mid-range','reasonable'],
    '$$$': ['غالي','فاخر','راقي','expensive','upscale','fine dining','premium'],
    '$$$$': ['فخم','luxury','luxurious','exclusive','أفخم']
  };

  const AUDIENCE_KEYWORDS = {
    'عوائل': ['عوائل','عائلة','أطفال','أولاد','بنات','kids','family','families','children'],
    'شباب': ['شباب','أصدقاء','رجال','guys','friends','hangout'],
    'أزواج': ['رومانسي','زوجين','رومانسية','date','romantic','couples','anniversary'],
    'الكل': ['الكل','عام','everyone','all']
  };

  const PERFECT_FOR_KEYWORDS = {
    'دراسة': ['دراسة','مذاكرة','لابتوب','عمل','study','work','laptop','quiet','هادي','هادئ'],
    'صور': ['صور','تصوير','انستقرام','photo','instagram','instagrammable','aesthetic'],
    'رومانسي': ['رومانسي','رومانسية','date','romantic','candle','كاندل'],
    'أطفال': ['أطفال','ألعاب أطفال','kids','playground','play area'],
    'فطور': ['فطور','صباح','morning','breakfast','brunch'],
    'سهرة': ['سهر','سهرة','ليل','night','late','open late','24']
  };

  const NEIGHBORHOOD_ALIASES = {
    'العليا': ['العليا','عليا','olaya','al olaya'],
    'الملقا': ['الملقا','ملقا','malqa','al malqa'],
    'حطين': ['حطين','hittin','al hittin'],
    'الياسمين': ['الياسمين','ياسمين','yasmin','al yasmin'],
    'النرجس': ['النرجس','نرجس','narjis','al narjis'],
    'الربيع': ['الربيع','ربيع','rabee','al rabee'],
    'السحاب': ['الصحافة','صحافة','sahafa'],
    'الورود': ['الورود','ورود','wurud'],
    'KAFD': ['kafd','كافد','المالي','حي المال'],
    'الدرعية': ['الدرعية','درعية','diriyah'],
    'الربوة': ['الربوة','rabwa'],
    'النخيل': ['النخيل','nakheel'],
    'السليمانية': ['السليمانية','سليمانية','sulaymaniyah'],
    'المربع': ['المربع','murabba'],
    'الدبلوماسي': ['الدبلوماسي','diplomasi','diplomatic quarter','dq'],
    'الروضة': ['الروضة','rawdah'],
    'الريان': ['الريان'],
    'الشفا': ['الشفا','shifa']
  };

  const SORT_KEYWORDS = {
    'rating_desc': ['أفضل','أحسن','أعلى تقييم','best','top','highest rated','top rated'],
    'price_asc': ['أرخص','أقل سعر','cheapest','lowest price'],
    'price_desc': ['أغلى','أعلى سعر','most expensive'],
    'newest': ['جديد','جديدة','أحدث','new','newest','latest','recently opened']
  };

  const QUANTITY_KEYWORDS = {
    'best_of': ['أفضل','أحسن','top','best'],
    'all': ['كل','جميع','all','every']
  };

  // === Query Parser ===
  function parseQuery(query) {
    const q = query.toLowerCase().trim();
    const tokens = q.split(/\s+/);
    
    const result = {
      category: null,
      cuisine: null,
      priceLevel: null,
      audience: null,
      perfectFor: null,
      neighborhood: null,
      sort: 'rating_desc',
      isFree: false,
      isNew: false,
      limit: 10,
      rawQuery: query,
      matchedFilters: []
    };

    // Check free
    if (q.includes('مجان') || q.includes('ببلاش') || q.includes('free')) {
      result.isFree = true;
      result.matchedFilters.push('مجاني');
    }

    // Check new
    if (q.includes('جديد') || q.includes('new') || q.includes('أحدث')) {
      result.isNew = true;
      result.matchedFilters.push('جديد');
    }

    // Match category
    for (const [cat, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
      if (keywords.some(kw => q.includes(kw))) {
        result.category = cat;
        result.matchedFilters.push('فئة: ' + cat);
        break;
      }
    }

    // Match cuisine
    for (const [cuisine, keywords] of Object.entries(CUISINE_KEYWORDS)) {
      if (keywords.some(kw => q.includes(kw))) {
        result.cuisine = cuisine;
        result.matchedFilters.push('مطبخ: ' + cuisine);
        if (!result.category) result.category = 'مطعم';
        break;
      }
    }

    // Match price
    for (const [level, keywords] of Object.entries(PRICE_KEYWORDS)) {
      if (keywords.some(kw => q.includes(kw))) {
        result.priceLevel = level;
        result.matchedFilters.push('سعر: ' + level);
        break;
      }
    }

    // Match audience
    for (const [aud, keywords] of Object.entries(AUDIENCE_KEYWORDS)) {
      if (keywords.some(kw => q.includes(kw))) {
        result.audience = aud;
        result.matchedFilters.push('جمهور: ' + aud);
        break;
      }
    }

    // Match perfect for
    for (const [pf, keywords] of Object.entries(PERFECT_FOR_KEYWORDS)) {
      if (keywords.some(kw => q.includes(kw))) {
        result.perfectFor = pf;
        result.matchedFilters.push('مناسب لـ: ' + pf);
        break;
      }
    }

    // Match neighborhood
    for (const [hood, aliases] of Object.entries(NEIGHBORHOOD_ALIASES)) {
      if (aliases.some(a => q.includes(a))) {
        result.neighborhood = hood;
        result.matchedFilters.push('حي: ' + hood);
        break;
      }
    }

    // Match sort
    for (const [sort, keywords] of Object.entries(SORT_KEYWORDS)) {
      if (keywords.some(kw => q.includes(kw))) {
        result.sort = sort;
        break;
      }
    }

    // Extract number (أفضل 5, top 10)
    const numMatch = q.match(/(\d+)/);
    if (numMatch) {
      result.limit = Math.min(parseInt(numMatch[1]), 50);
    }

    return result;
  }

  // === Search Engine ===
  function searchPlaces(places, query) {
    const filters = parseQuery(query);
    let results = [...places];

    // Apply filters
    if (filters.category) {
      results = results.filter(p => p.category === filters.category);
    }

    if (filters.cuisine) {
      const cuisineKws = CUISINE_KEYWORDS[filters.cuisine] || [];
      results = results.filter(p => {
        const desc = (p.description_ar || '').toLowerCase() + ' ' + (p.name_en || '').toLowerCase() + ' ' + (p.name_ar || '').toLowerCase();
        return cuisineKws.some(kw => desc.includes(kw));
      });
    }

    if (filters.priceLevel) {
      results = results.filter(p => p.price_level === filters.priceLevel);
    }

    if (filters.audience) {
      results = results.filter(p => p.audience === filters.audience || 
        (p.perfect_for && p.perfect_for.includes(filters.audience)));
    }

    if (filters.perfectFor) {
      results = results.filter(p => 
        p.perfect_for && p.perfect_for.some(pf => pf.includes(filters.perfectFor)));
    }

    if (filters.neighborhood) {
      const aliases = NEIGHBORHOOD_ALIASES[filters.neighborhood] || [filters.neighborhood];
      results = results.filter(p => {
        const hood = (p.neighborhood || '').toLowerCase() + ' ' + (p.neighborhood_en || '').toLowerCase();
        return aliases.some(a => hood.includes(a));
      });
    }

    if (filters.isFree) {
      results = results.filter(p => p.is_free === true || p.price_level === 'مجاني' || p.price_level === 'free');
    }

    if (filters.isNew) {
      results = results.filter(p => p.is_new === true);
    }

    // Sort
    switch (filters.sort) {
      case 'rating_desc':
        results.sort((a, b) => (b.google_rating || 0) - (a.google_rating || 0));
        break;
      case 'price_asc':
        const priceOrder = {'$':1,'مجاني':0,'free':0,'$$':2,'$$$':3,'$$$$':4};
        results.sort((a, b) => (priceOrder[a.price_level]||2) - (priceOrder[b.price_level]||2));
        break;
      case 'price_desc':
        const priceOrder2 = {'$':1,'مجاني':0,'free':0,'$$':2,'$$$':3,'$$$$':4};
        results.sort((a, b) => (priceOrder2[b.price_level]||2) - (priceOrder2[a.price_level]||2));
        break;
      case 'newest':
        results = results.filter(p => p.is_new).concat(results.filter(p => !p.is_new));
        break;
    }

    // Limit
    results = results.slice(0, filters.limit);

    // Generate response text
    const responseText = generateResponse(filters, results);

    return {
      filters: filters,
      results: results,
      total: results.length,
      responseText: responseText
    };
  }

  // === Natural Language Response ===
  function generateResponse(filters, results) {
    if (results.length === 0) {
      return 'ما لقيت نتائج تطابق بحثك 😕 جرب تغير الفلاتر';
    }

    let parts = [];
    
    if (filters.category) parts.push(filters.category);
    if (filters.cuisine) parts.push(filters.cuisine);
    if (filters.neighborhood) parts.push('بـ' + filters.neighborhood);
    if (filters.priceLevel) {
      const priceNames = {'$':'رخيص','$$':'متوسط','$$$':'غالي','$$$$':'فاخر'};
      parts.push(priceNames[filters.priceLevel] || '');
    }
    if (filters.audience) parts.push('لـ' + filters.audience);
    if (filters.perfectFor) parts.push('لـ' + filters.perfectFor);

    let text = `لقيت ${results.length} `;
    text += parts.length > 0 ? parts.join(' ') : 'مكان';
    
    if (results.length > 0) {
      const best = results[0];
      text += ` — أفضلها "${best.name_ar}" `;
      if (best.google_rating) text += `(${best.google_rating}⭐)`;
      if (best.price_level) text += ` ${best.price_level}`;
    }

    return text;
  }

  // === Fuzzy Text Search (fallback) ===
  function fuzzySearch(places, query) {
    const q = query.toLowerCase().trim();
    const tokens = q.split(/\s+/).filter(t => t.length > 1);
    
    return places.map(p => {
      const searchable = [
        p.name_ar, p.name_en, p.category, p.neighborhood,
        p.neighborhood_en, p.description_ar, p.category_en,
        ...(p.perfect_for || [])
      ].join(' ').toLowerCase();

      let score = 0;
      tokens.forEach(token => {
        if (searchable.includes(token)) score += 1;
        if ((p.name_ar || '').toLowerCase().includes(token)) score += 3;
        if ((p.name_en || '').toLowerCase().includes(token)) score += 3;
      });

      return { place: p, score: score };
    })
    .filter(r => r.score > 0)
    .sort((a, b) => b.score - a.score || (b.place.google_rating || 0) - (a.place.google_rating || 0))
    .slice(0, 20)
    .map(r => r.place);
  }

  // === Recommendations Engine ===
  function getRecommendations(places, context) {
    const { currentPlace, favorites, timeOfDay, budget } = context || {};
    let recommendations = [];

    // Content-based: similar to current place
    if (currentPlace) {
      recommendations = places.filter(p => 
        p.id !== currentPlace.id &&
        (p.category === currentPlace.category || p.neighborhood === currentPlace.neighborhood)
      ).sort((a, b) => {
        let scoreA = 0, scoreB = 0;
        if (a.category === currentPlace.category) scoreA += 2;
        if (b.category === currentPlace.category) scoreB += 2;
        if (a.neighborhood === currentPlace.neighborhood) scoreA += 1;
        if (b.neighborhood === currentPlace.neighborhood) scoreB += 1;
        scoreA += (a.google_rating || 0);
        scoreB += (b.google_rating || 0);
        return scoreB - scoreA;
      }).slice(0, 10);
    }

    // Time-based suggestions
    if (timeOfDay) {
      const hour = typeof timeOfDay === 'number' ? timeOfDay : new Date().getHours();
      if (hour >= 6 && hour < 11) {
        // Morning = breakfast
        recommendations = places.filter(p => 
          (p.perfect_for && p.perfect_for.some(pf => pf.includes('فطور'))) ||
          p.category === 'كافيه'
        ).sort((a,b) => (b.google_rating||0) - (a.google_rating||0)).slice(0, 10);
      } else if (hour >= 11 && hour < 15) {
        // Lunch
        recommendations = places.filter(p => p.category === 'مطعم')
          .sort((a,b) => (b.google_rating||0) - (a.google_rating||0)).slice(0, 10);
      } else if (hour >= 15 && hour < 19) {
        // Afternoon = cafe or dessert
        recommendations = places.filter(p => p.category === 'كافيه' || p.category === 'حلويات')
          .sort((a,b) => (b.google_rating||0) - (a.google_rating||0)).slice(0, 10);
      } else {
        // Evening/night = dinner or entertainment
        recommendations = places.filter(p => p.category === 'مطعم' || p.category === 'ترفيه')
          .sort((a,b) => (b.google_rating||0) - (a.google_rating||0)).slice(0, 10);
      }
    }

    // Budget filter
    if (budget) {
      recommendations = recommendations.filter(p => {
        const priceOrder = {'$':1,'مجاني':0,'free':0,'$$':2,'$$$':3,'$$$$':4};
        return (priceOrder[p.price_level] || 2) <= budget;
      });
    }

    return recommendations;
  }

  // === Public API ===
  window.WaynroohAI = {
    search: searchPlaces,
    fuzzySearch: fuzzySearch,
    recommend: getRecommendations,
    parseQuery: parseQuery,
    
    // Quick search helpers
    bestInCategory: function(places, category, limit) {
      return places.filter(p => p.category === category)
        .sort((a,b) => (b.google_rating||0) - (a.google_rating||0))
        .slice(0, limit || 10);
    },
    
    bestInNeighborhood: function(places, hood, limit) {
      return places.filter(p => 
        (p.neighborhood || '').includes(hood) || (p.neighborhood_en || '').toLowerCase().includes(hood.toLowerCase())
      ).sort((a,b) => (b.google_rating||0) - (a.google_rating||0))
        .slice(0, limit || 10);
    },

    bestValue: function(places, category, limit) {
      const priceOrder = {'$':1,'مجاني':0,'free':0,'$$':2,'$$$':3,'$$$$':4};
      return places.filter(p => !category || p.category === category)
        .map(p => ({
          ...p,
          valueScore: (p.google_rating || 0) / Math.max(priceOrder[p.price_level] || 2, 0.5)
        }))
        .sort((a,b) => b.valueScore - a.valueScore)
        .slice(0, limit || 10);
    },

    nearbyPlaces: function(places, lat, lng, radiusKm, limit) {
      return places.filter(p => p.lat && p.lng)
        .map(p => {
          const d = haversine(lat, lng, p.lat, p.lng);
          return { ...p, distance: d };
        })
        .filter(p => p.distance <= radiusKm)
        .sort((a,b) => a.distance - b.distance)
        .slice(0, limit || 20);
    }
  };

  // Haversine distance (km)
  function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  }
})();
