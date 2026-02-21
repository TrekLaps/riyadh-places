// ===== وين نروح — Filter Engine v1.0 =====
// Shared filtering, pagination, URL state, and card rendering for places-light.json
// Data uses abbreviated fields: id, n, ne, c, ca, h, he, d, r, rc, p, la, lo, tr, nw, fr, au, pf, gm

(function() {
  'use strict';

  const PAGE_SIZE = 24;

  const CATEGORY_ICONS = {
    'مطعم': '🍽️', 'كافيه': '☕', 'ترفيه': '🎭', 'تسوق': '🛍️',
    'طبيعة': '🏞️', 'حلويات': '🍰', 'فعاليات': '🎪', 'شاليه': '🏕️',
    'فنادق': '🏨', 'مولات': '🛒', 'متاحف': '🏛️', 'أخرى': '📍'
  };

  const CATEGORY_GRADIENTS = {
    'مطعم': 'linear-gradient(135deg, #c0392b, #e74c3c)',
    'كافيه': 'linear-gradient(135deg, #6F4E37, #A0785A)',
    'ترفيه': 'linear-gradient(135deg, #8e44ad, #9b59b6)',
    'حلويات': 'linear-gradient(135deg, #e84393, #fd79a8)',
    'طبيعة': 'linear-gradient(135deg, #27ae60, #2ecc71)',
    'تسوق': 'linear-gradient(135deg, #2980b9, #3498db)',
    'شاليه': 'linear-gradient(135deg, #d35400, #e67e22)',
    'فنادق': 'linear-gradient(135deg, #1a1a2e, #16213e)',
    'مولات': 'linear-gradient(135deg, #2c3e50, #34495e)',
    'متاحف': 'linear-gradient(135deg, #7f8c8d, #95a5a6)',
    'فعاليات': 'linear-gradient(135deg, #f39c12, #f1c40f)',
    'أخرى': 'linear-gradient(135deg, #0a1628, #162040)'
  };

  const CATEGORY_LABELS = {
    'مطعم': 'مطعم', 'كافيه': 'كافيه', 'ترفيه': 'ترفيه', 'تسوق': 'تسوق',
    'طبيعة': 'طبيعة', 'حلويات': 'حلويات', 'فعاليات': 'فعاليات',
    'شاليه': 'شاليه', 'فنادق': 'فندق', 'مولات': 'مول', 'متاحف': 'متحف', 'أخرى': 'أخرى'
  };

  const CATEGORY_PLURAL = {
    'مطعم': 'مطعم', 'كافيه': 'كافيه', 'ترفيه': 'مكان ترفيهي', 'تسوق': 'متجر',
    'طبيعة': 'مكان طبيعي', 'حلويات': 'محل حلويات', 'فعاليات': 'فعالية',
    'شاليه': 'شاليه', 'فنادق': 'فندق', 'مولات': 'مول', 'متاحف': 'متحف', 'أخرى': 'مكان'
  };

  const PRICE_ORDER = { '$': 1, '$$': 2, '$$$': 3, '$$$$': 4, 'مجاني': 0, 'free': 0, '': -1 };
  const PRICE_LABELS = { '$': 'رخيص', '$$': 'متوسط', '$$$': 'غالي', '$$$$': 'فاخر', 'مجاني': 'مجاني', 'free': 'مجاني' };

  // ===== Data Loading =====
  let _placesCache = null;

  async function loadAllPlaces() {
    if (_placesCache) return _placesCache;
    try {
      const resp = await fetch('data/places-light.json');
      const data = await resp.json();
      _placesCache = data.map(p => ({
        id: p.id,
        name_ar: p.n,
        name_en: p.ne || '',
        category: p.c,
        neighborhood: p.h || 'غير محدد',
        neighborhood_en: p.he || '',
        description: p.d || '',
        rating: p.r || 0,
        review_count: p.rc || 0,
        price_level: p.p || '',
        price_order: PRICE_ORDER[p.p] ?? -1,
        lat: p.la || null,
        lng: p.lo || null,
        trending: !!p.tr,
        is_new: !!p.nw,
        is_free: !!p.fr || p.p === 'مجاني' || p.p === 'free',
        audience: p.au || [],
        features: p.pf || [],
        google_maps_url: p.gm || ''
      }));
      return _placesCache;
    } catch (e) {
      // load error handled silently
      return [];
    }
  }

  // ===== Arabic Number Formatting =====
  function toArabicNum(n) {
    return n.toLocaleString('ar-SA');
  }

  // Generate star rating
  function generateStars(rating) {
    if (!rating) return '';
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.3;
    return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(5 - full - (half ? 1 : 0));
  }

  // ===== URL State Management =====
  function getURLParams() {
    return new URLSearchParams(window.location.search);
  }

  function setURLParams(params) {
    const url = new URL(window.location);
    Object.entries(params).forEach(([k, v]) => {
      if (v && v !== 'all' && v !== '') {
        url.searchParams.set(k, v);
      } else {
        url.searchParams.delete(k);
      }
    });
    window.history.replaceState({}, '', url);
  }

  // ===== Filtering =====
  function filterPlaces(places, filters) {
    return places.filter(p => {
      if (filters.category && filters.category !== 'all' && p.category !== filters.category) return false;
      if (filters.neighborhood && filters.neighborhood !== 'all') {
        if (p.neighborhood !== filters.neighborhood && !p.neighborhood.includes(filters.neighborhood)) return false;
      }
      if (filters.price && filters.price !== 'all' && p.price_level !== filters.price) return false;
      if (filters.minRating && p.rating < parseFloat(filters.minRating)) return false;
      if (filters.audience && filters.audience !== 'all') {
        if (!p.audience.includes(filters.audience)) return false;
      }
      if (filters.trendingOnly && !p.trending) return false;
      if (filters.freeOnly && !p.is_free) return false;
      if (filters.search) {
        const q = filters.search.toLowerCase();
        const matchAr = p.name_ar.includes(q);
        const matchEn = p.name_en.toLowerCase().includes(q);
        const matchHood = p.neighborhood.includes(q);
        const matchDesc = p.description.includes(q);
        if (!matchAr && !matchEn && !matchHood && !matchDesc) return false;
      }
      return true;
    });
  }

  // ===== Sorting =====
  function sortPlaces(places, sortBy) {
    const sorted = [...places];
    switch (sortBy) {
      case 'rating-desc':
        return sorted.sort((a, b) => b.rating - a.rating);
      case 'rating-asc':
        return sorted.sort((a, b) => a.rating - b.rating);
      case 'name-asc':
        return sorted.sort((a, b) => a.name_ar.localeCompare(b.name_ar, 'ar'));
      case 'name-desc':
        return sorted.sort((a, b) => b.name_ar.localeCompare(a.name_ar, 'ar'));
      case 'price-asc':
        return sorted.sort((a, b) => a.price_order - b.price_order);
      case 'price-desc':
        return sorted.sort((a, b) => b.price_order - a.price_order);
      case 'trending':
        return sorted.sort((a, b) => (b.trending ? 1 : 0) - (a.trending ? 1 : 0) || b.rating - a.rating);
      case 'random':
        for (let i = sorted.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [sorted[i], sorted[j]] = [sorted[j], sorted[i]];
        }
        return sorted;
      default:
        return sorted.sort((a, b) => b.rating - a.rating);
    }
  }

  // ===== Card Rendering =====
  function createPlaceCard(place) {
    const icon = CATEGORY_ICONS[place.category] || '📍';
    const gradient = CATEGORY_GRADIENTS[place.category] || CATEGORY_GRADIENTS['أخرى'];
    const label = CATEGORY_LABELS[place.category] || place.category;
    const priceLabel = PRICE_LABELS[place.price_level] || '';
    const mapUrl = place.google_maps_url || (place.lat && place.lng ? `https://www.google.com/maps?q=${place.lat},${place.lng}` : '');
    const desc = place.description ? place.description.slice(0, 80) + (place.description.length > 80 ? '...' : '') : '';

    return `
      <article class="place-card-v2" data-category="${place.category}" data-neighborhood="${place.neighborhood}" data-price="${place.price_level}" data-id="${place.id}">
        <div class="card-v2-header" style="background:${gradient}">
          <span class="card-v2-icon">${icon}</span>
          <span class="card-v2-cat">${label}</span>
          ${place.trending ? '<span class="card-v2-trending">🔥</span>' : ''}
          ${place.is_new ? '<span class="card-v2-new">جديد</span>' : ''}
          ${place.is_free ? '<span class="card-v2-free">🆓</span>' : ''}
        </div>
        <div class="card-v2-body">
          <h3 class="card-v2-title">${place.name_ar}</h3>
          ${place.name_en ? `<p class="card-v2-subtitle">${place.name_en}</p>` : ''}
          ${place.rating ? `
            <div class="card-v2-rating">
              <span class="card-v2-rating-num">${place.rating}</span>
              <span class="card-v2-stars">${generateStars(place.rating)}</span>
            </div>
          ` : ''}
          ${desc ? `<p class="card-v2-desc">${desc}</p>` : ''}
          <div class="card-v2-meta">
            <span class="card-v2-hood">📍 ${place.neighborhood}</span>
            ${priceLabel && !place.is_free ? `<span class="card-v2-price">${place.price_level} · ${priceLabel}</span>` : ''}
          </div>
          ${place.audience.length > 0 ? `<div class="card-v2-tags">${place.audience.slice(0, 3).map(t => `<span class="card-v2-tag">${t}</span>`).join('')}</div>` : ''}
          <div class="card-v2-actions">
            <a href="place.html?id=${place.id}" class="card-v2-btn card-v2-btn-detail">اعرف أكثر</a>
            ${mapUrl ? `<a href="${mapUrl}" target="_blank" rel="noopener" class="card-v2-btn card-v2-btn-map">📍 الموقع</a>` : ''}
          </div>
        </div>
      </article>
    `;
  }

  // ===== Pagination with Intersection Observer =====
  function createPaginatedGrid(container, allCards, pageSize) {
    pageSize = pageSize || PAGE_SIZE;
    let currentPage = 0;
    let totalPages = Math.ceil(allCards.length / pageSize);
    let sentinel = null;
    let io = null;

    function renderPage() {
      const start = currentPage * pageSize;
      const end = start + pageSize;
      const chunk = allCards.slice(start, end);
      const wrapper = document.createElement('div');
      wrapper.className = 'cards-grid-v2';
      wrapper.innerHTML = chunk.join('');
      container.appendChild(wrapper);
      currentPage++;
      updateSentinel();
    }

    function updateSentinel() {
      if (currentPage < totalPages) {
        if (!sentinel) {
          sentinel = document.createElement('div');
          sentinel.className = 'scroll-sentinel';
          sentinel.innerHTML = '<div class="load-more-indicator">⏳ جاري تحميل المزيد...</div>';
        }
        if (!sentinel.parentNode) container.appendChild(sentinel);
      } else if (sentinel) {
        sentinel.remove();
        // Show end message if we loaded more than 1 page
        if (currentPage > 1) {
          const endMsg = document.createElement('div');
          endMsg.className = 'end-of-results';
          endMsg.innerHTML = '✅ عرضنا كل النتائج';
          container.appendChild(endMsg);
        }
      }
    }

    function cleanup() {
      if (io) io.disconnect();
      if (sentinel) sentinel.remove();
    }

    // Initial render
    container.innerHTML = '';
    if (allCards.length === 0) {
      container.innerHTML = `
        <div class="no-results-v2">
          <div class="no-results-emoji">🔍</div>
          <h3>ما لقينا نتائج</h3>
          <p>جرب تغيير الفلتر أو ابحث عن شي ثاني</p>
        </div>
      `;
      return { refresh: null, cleanup };
    }

    renderPage();
    sentinel = document.createElement('div');
    sentinel.className = 'scroll-sentinel';
    sentinel.innerHTML = '<div class="load-more-indicator">⏳ جاري تحميل المزيد...</div>';
    container.appendChild(sentinel);

    io = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && currentPage < totalPages) {
        renderPage();
      }
    }, { rootMargin: '600px' });
    io.observe(sentinel);
    updateSentinel();

    return {
      refresh: function(newCards) {
        cleanup();
        currentPage = 0;
        allCards = newCards;
        totalPages = Math.ceil(allCards.length / pageSize);
        container.innerHTML = '';
        if (newCards.length === 0) {
          container.innerHTML = `
            <div class="no-results-v2">
              <div class="no-results-emoji">🔍</div>
              <h3>ما لقينا نتائج</h3>
              <p>جرب تغيير الفلتر أو ابحث عن شي ثاني</p>
            </div>
          `;
          return;
        }
        renderPage();
        sentinel = document.createElement('div');
        sentinel.className = 'scroll-sentinel';
        sentinel.innerHTML = '<div class="load-more-indicator">⏳ جاري تحميل المزيد...</div>';
        container.appendChild(sentinel);
        io = new IntersectionObserver(entries => {
          if (entries[0].isIntersecting && currentPage < totalPages) {
            renderPage();
          }
        }, { rootMargin: '600px' });
        io.observe(sentinel);
        updateSentinel();
      },
      cleanup
    };
  }

  // ===== Filter Bar Generator =====
  function createFilterBar(config) {
    const {
      neighborhoods = [],
      showSearch = true,
      showSort = true,
      showPrice = true,
      showNeighborhood = true,
      showRating = true,
      showAudience = false,
      showCategory = false,
      categories = [],
      totalCount = 0,
      categoryLabel = 'مكان',
      initialFilters = {}
    } = config;

    const currentHood = initialFilters.neighborhood || 'all';
    const currentPrice = initialFilters.price || 'all';
    const currentSort = initialFilters.sort || 'rating-desc';
    const currentSearch = initialFilters.search || '';
    const currentRating = initialFilters.minRating || 'all';
    const currentAudience = initialFilters.audience || 'all';
    const currentCategory = initialFilters.category || 'all';

    let html = `<div class="filter-bar-v2">`;
    html += `<div class="filter-bar-count"><span class="count-badge" id="results-count-badge">${toArabicNum(totalCount)}</span> ${categoryLabel} في الرياض</div>`;
    html += `<div class="filter-bar-controls">`;

    if (showSearch) {
      html += `<div class="filter-group filter-group-search">
        <input type="text" class="filter-search-input" id="filter-search" placeholder="🔍 ابحث بالاسم..." value="${currentSearch}" autocomplete="off">
      </div>`;
    }

    if (showCategory && categories.length > 0) {
      html += `<div class="filter-group">
        <label>القسم</label>
        <select id="filter-category" class="filter-select">
          <option value="all">كل الأقسام</option>
          ${categories.map(c => `<option value="${c}" ${c === currentCategory ? 'selected' : ''}>${CATEGORY_ICONS[c] || '📍'} ${CATEGORY_LABELS[c] || c}</option>`).join('')}
        </select>
      </div>`;
    }

    if (showNeighborhood && neighborhoods.length > 0) {
      html += `<div class="filter-group">
        <label>الحي</label>
        <select id="filter-neighborhood" class="filter-select">
          <option value="all">كل الأحياء</option>
          ${neighborhoods.map(h => `<option value="${h}" ${h === currentHood ? 'selected' : ''}>${h}</option>`).join('')}
        </select>
      </div>`;
    }

    if (showRating) {
      html += `<div class="filter-group">
        <label>التقييم</label>
        <select id="filter-rating" class="filter-select">
          <option value="all">الكل</option>
          <option value="4.5" ${'4.5' === currentRating ? 'selected' : ''}>⭐ ٤.٥+</option>
          <option value="4" ${'4' === currentRating ? 'selected' : ''}>⭐ ٤+</option>
          <option value="3.5" ${'3.5' === currentRating ? 'selected' : ''}>⭐ ٣.٥+</option>
        </select>
      </div>`;
    }

    if (showPrice) {
      html += `<div class="filter-group">
        <label>السعر</label>
        <select id="filter-price" class="filter-select">
          <option value="all">الكل</option>
          <option value="مجاني" ${'مجاني' === currentPrice ? 'selected' : ''}>🆓 مجاني</option>
          <option value="$" ${'$' === currentPrice ? 'selected' : ''}>$ رخيص</option>
          <option value="$$" ${'$$' === currentPrice ? 'selected' : ''}>$$ متوسط</option>
          <option value="$$$" ${'$$$' === currentPrice ? 'selected' : ''}>$$$ غالي</option>
          <option value="$$$$" ${'$$$$' === currentPrice ? 'selected' : ''}>$$$$ فاخر</option>
        </select>
      </div>`;
    }

    if (showAudience) {
      html += `<div class="filter-group">
        <label>مناسب لـ</label>
        <select id="filter-audience" class="filter-select">
          <option value="all">الكل</option>
          <option value="عوائل" ${'عوائل' === currentAudience ? 'selected' : ''}>👨‍👩‍👧 عوائل</option>
          <option value="شباب" ${'شباب' === currentAudience ? 'selected' : ''}>👥 شباب</option>
          <option value="أصدقاء" ${'أصدقاء' === currentAudience ? 'selected' : ''}>🤝 أصدقاء</option>
          <option value="أزواج" ${'أزواج' === currentAudience ? 'selected' : ''}>💑 أزواج</option>
          <option value="نساء" ${'نساء' === currentAudience ? 'selected' : ''}>👩 نساء</option>
        </select>
      </div>`;
    }

    if (showSort) {
      html += `<div class="filter-group">
        <label>ترتيب</label>
        <select id="filter-sort" class="filter-select">
          <option value="rating-desc" ${'rating-desc' === currentSort ? 'selected' : ''}>⭐ الأعلى تقييماً</option>
          <option value="name-asc" ${'name-asc' === currentSort ? 'selected' : ''}>أ → ي</option>
          <option value="name-desc" ${'name-desc' === currentSort ? 'selected' : ''}>ي → أ</option>
          <option value="price-asc" ${'price-asc' === currentSort ? 'selected' : ''}>الأرخص أولاً</option>
          <option value="price-desc" ${'price-desc' === currentSort ? 'selected' : ''}>الأغلى أولاً</option>
          <option value="trending" ${'trending' === currentSort ? 'selected' : ''}>🔥 الأكثر رواجاً</option>
          <option value="random" ${'random' === currentSort ? 'selected' : ''}>🎲 عشوائي</option>
        </select>
      </div>`;
    }

    html += `</div></div>`;
    return html;
  }

  // ===== Full Page Controller =====
  function initCategoryPage(config) {
    const {
      containerSelector = '#places-grid',
      filterBarSelector = '#filter-bar',
      category = null,
      neighborhoodFilter = null,
      categoryLabel = 'مكان',
      showSearch = true,
      showNeighborhood = true,
      showRating = true,
      showAudience = true,
      showCategory = false,
      onLoaded = null
    } = config;

    const container = document.querySelector(containerSelector);
    const filterBarEl = document.querySelector(filterBarSelector);
    if (!container) return;

    // Show skeleton
    container.innerHTML = '<div class="cards-grid-v2">' + Array(6).fill(`
      <div class="place-card-v2 skeleton-card">
        <div class="card-v2-header skeleton" style="min-height:70px"></div>
        <div class="card-v2-body">
          <div class="skeleton" style="height:20px;width:60%;margin-bottom:8px;border-radius:4px"></div>
          <div class="skeleton" style="height:14px;width:40%;margin-bottom:12px;border-radius:4px"></div>
          <div class="skeleton" style="height:14px;width:80%;border-radius:4px"></div>
        </div>
      </div>
    `).join('') + '</div>';

    loadAllPlaces().then(allPlaces => {
      let basePlaces = allPlaces;
      if (category) basePlaces = basePlaces.filter(p => p.category === category);
      if (neighborhoodFilter) basePlaces = basePlaces.filter(p => p.neighborhood === neighborhoodFilter || p.neighborhood.includes(neighborhoodFilter));

      const neighborhoods = [...new Set(basePlaces.map(p => p.neighborhood))].filter(h => h && h !== 'غير محدد').sort((a, b) => a.localeCompare(b, 'ar'));
      const categories = [...new Set(basePlaces.map(p => p.category))].filter(Boolean).sort();

      // URL params
      const params = getURLParams();
      const initialFilters = {
        neighborhood: params.get('neighborhood') || 'all',
        price: params.get('price') || 'all',
        sort: params.get('sort') || 'rating-desc',
        search: params.get('q') || '',
        minRating: params.get('rating') || 'all',
        audience: params.get('audience') || 'all',
        category: params.get('cat') || 'all'
      };

      if (filterBarEl) {
        filterBarEl.innerHTML = createFilterBar({
          neighborhoods: showNeighborhood ? neighborhoods : [],
          showSearch,
          showNeighborhood,
          showRating,
          showAudience,
          showCategory,
          categories,
          totalCount: basePlaces.length,
          categoryLabel,
          initialFilters
        });
      }

      function getFilters() {
        return {
          neighborhood: document.getElementById('filter-neighborhood')?.value || 'all',
          price: document.getElementById('filter-price')?.value || 'all',
          search: document.getElementById('filter-search')?.value?.trim() || '',
          minRating: document.getElementById('filter-rating')?.value || 'all',
          audience: document.getElementById('filter-audience')?.value || 'all',
          category: document.getElementById('filter-category')?.value || 'all'
        };
      }

      function getSort() {
        return document.getElementById('filter-sort')?.value || 'rating-desc';
      }

      let gridController = null;

      function applyFilters() {
        const filters = getFilters();
        const sortBy = getSort();
        let filtered = filterPlaces(basePlaces, filters);
        filtered = sortPlaces(filtered, sortBy);

        setURLParams({
          neighborhood: filters.neighborhood,
          price: filters.price,
          sort: sortBy,
          q: filters.search,
          rating: filters.minRating,
          audience: filters.audience,
          cat: filters.category
        });

        // Update count
        const countBadge = document.getElementById('results-count-badge');
        if (countBadge) countBadge.textContent = toArabicNum(filtered.length);

        const cards = filtered.map(p => createPlaceCard(p));
        if (gridController && gridController.refresh) {
          gridController.refresh(cards);
        } else {
          gridController = createPaginatedGrid(container, cards);
        }
      }

      // Bind events
      ['filter-neighborhood', 'filter-price', 'filter-sort', 'filter-rating', 'filter-audience', 'filter-category'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', applyFilters);
      });

      // Debounced search
      let searchTimeout;
      const searchEl = document.getElementById('filter-search');
      if (searchEl) {
        searchEl.addEventListener('input', () => {
          clearTimeout(searchTimeout);
          searchTimeout = setTimeout(applyFilters, 300);
        });
      }

      applyFilters();
      if (onLoaded) onLoaded(basePlaces, neighborhoods);
    });
  }

  // ===== Neighborhood Page Controller =====
  function initNeighborhoodPage(config) {
    const {
      neighborhood,
      containerSelector = '#places-grid',
      filterBarSelector = '#filter-bar',
      categorySummarySelector = '#category-summary'
    } = config;

    loadAllPlaces().then(allPlaces => {
      const hoodPlaces = allPlaces.filter(p => p.neighborhood === neighborhood || p.neighborhood.includes(neighborhood));

      // Category breakdown
      const catCounts = {};
      hoodPlaces.forEach(p => { catCounts[p.category] = (catCounts[p.category] || 0) + 1; });

      const summaryEl = document.querySelector(categorySummarySelector);
      if (summaryEl) {
        let summaryHtml = '<div class="cat-summary-grid">';
        summaryHtml += `<button class="cat-summary-card active" data-cat="all">
          <span class="cat-summary-icon">📍</span>
          <span class="cat-summary-label">الكل</span>
          <span class="cat-summary-count">${toArabicNum(hoodPlaces.length)}</span>
        </button>`;
        Object.entries(catCounts)
          .sort((a, b) => b[1] - a[1])
          .forEach(([cat, count]) => {
            summaryHtml += `
              <button class="cat-summary-card" data-cat="${cat}">
                <span class="cat-summary-icon">${CATEGORY_ICONS[cat] || '📍'}</span>
                <span class="cat-summary-label">${CATEGORY_LABELS[cat] || cat}</span>
                <span class="cat-summary-count">${toArabicNum(count)}</span>
              </button>
            `;
          });
        summaryHtml += '</div>';
        summaryEl.innerHTML = summaryHtml;

        // Click to filter
        let activeCat = 'all';
        summaryEl.querySelectorAll('.cat-summary-card').forEach(btn => {
          btn.addEventListener('click', () => {
            const cat = btn.dataset.cat;
            summaryEl.querySelectorAll('.cat-summary-card').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeCat = cat === 'all' ? null : cat;

            initCategoryPage({
              containerSelector,
              filterBarSelector,
              category: activeCat,
              neighborhoodFilter: neighborhood,
              categoryLabel: activeCat ? (CATEGORY_PLURAL[activeCat] || 'مكان') : 'مكان',
              showNeighborhood: false,
              showCategory: false,
              showAudience: true
            });
          });
        });
      }

      // Initial full render
      initCategoryPage({
        containerSelector,
        filterBarSelector,
        neighborhoodFilter: neighborhood,
        categoryLabel: 'مكان',
        showNeighborhood: false,
        showCategory: false,
        showAudience: true
      });
    });
  }

  // ===== Discover Page =====
  function createHorizontalRow(title, subtitle, places, maxItems) {
    maxItems = maxItems || 15;
    const items = places.slice(0, maxItems);
    if (items.length === 0) return '';

    let html = `
      <div class="discover-section">
        <div class="discover-section-header">
          <h3>${title}</h3>
          <p>${subtitle}</p>
        </div>
        <div class="discover-scroll-row">
    `;
    items.forEach(p => {
      const icon = CATEGORY_ICONS[p.category] || '📍';
      const gradient = CATEGORY_GRADIENTS[p.category] || CATEGORY_GRADIENTS['أخرى'];
      const mapUrl = p.google_maps_url || (p.lat && p.lng ? `https://www.google.com/maps?q=${p.lat},${p.lng}` : '');
      html += `
        <div class="discover-card" style="--card-gradient:${gradient}">
          <div class="discover-card-icon">${icon}</div>
          <h4>${p.name_ar}</h4>
          <p class="discover-card-en">${p.name_en || ''}</p>
          ${p.rating ? `<span class="discover-card-rating">⭐ ${p.rating}</span>` : ''}
          <span class="discover-card-hood">📍 ${p.neighborhood}</span>
          ${p.price_level ? `<span class="discover-card-price">${p.price_level}</span>` : ''}
          ${mapUrl ? `<a href="${mapUrl}" target="_blank" rel="noopener" class="discover-card-link">الموقع ←</a>` : ''}
        </div>
      `;
    });
    html += `</div></div>`;
    return html;
  }

  async function initDiscoverPage(containerSelector) {
    containerSelector = containerSelector || '#discover-content';
    const container = document.querySelector(containerSelector);
    if (!container) return;

    container.innerHTML = '<div class="discover-loading">جاري تحميل الأماكن...</div>';

    const allPlaces = await loadAllPlaces();
    const shuffle = arr => [...arr].sort(() => Math.random() - 0.5);
    const topRated = arr => [...arr].sort((a, b) => b.rating - a.rating);
    let html = '';

    // 1. Nearby
    html += `
      <div class="discover-section discover-nearby">
        <div class="discover-section-header">
          <h3>📍 قريب مني</h3>
          <p>اكتشف أقرب الأماكن لموقعك</p>
        </div>
        <button class="discover-nearby-btn" id="nearby-btn">
          <span>🗺️</span> فعّل الموقع واكتشف
        </button>
        <div id="nearby-results" class="discover-scroll-row" style="display:none"></div>
      </div>
    `;

    // 2. Top rated
    const topAll = topRated(allPlaces.filter(p => p.rating >= 4.5));
    html += createHorizontalRow('⭐ الأعلى تقييماً', 'أفضل الأماكن في الرياض بتقييم ٤.٥ فما فوق', topAll, 20);

    // 3. Trending
    const trending = shuffle(allPlaces.filter(p => p.trending));
    html += createHorizontalRow('🔥 ترند الحين', 'الأماكن اللي الكل يتكلم عنها', trending.slice(0, 20));

    // 4. Budget
    const budget = shuffle(allPlaces.filter(p => p.price_level === '$'));
    html += createHorizontalRow('💰 ميزانية محدودة', 'أماكن حلوة وما تكلفك كثير', budget, 15);

    // 5. Families
    const families = shuffle(allPlaces.filter(p => p.audience.includes('عوائل') && p.rating >= 4));
    html += createHorizontalRow('👨‍👩‍👧 عوائل', 'أماكن مناسبة للعائلات', families, 15);

    // 6. Couples / romantic
    const couples = shuffle(allPlaces.filter(p => p.audience.includes('أزواج')));
    html += createHorizontalRow('💑 رومانسي', 'أماكن مثالية للأزواج', couples, 15);

    // 7. Free
    const free = shuffle(allPlaces.filter(p => p.is_free));
    html += createHorizontalRow('🆓 مجاني', 'استمتع بدون ما تصرف', free, 15);

    // 8. Luxury
    const luxury = shuffle(allPlaces.filter(p => p.price_level === '$$$$'));
    html += createHorizontalRow('👑 فاخر', 'تجارب استثنائية لمحبي الفخامة', luxury, 15);

    // 9. Coffee shops
    const cafes = topRated(allPlaces.filter(p => p.category === 'كافيه'));
    html += createHorizontalRow('☕ أفضل الكافيهات', 'قهوة مختصة وأجواء مميزة', cafes.slice(0, 20));

    // 10. Nature
    const nature = shuffle(allPlaces.filter(p => p.category === 'طبيعة'));
    html += createHorizontalRow('🏞️ طبيعة', 'هروب من زحمة المدينة', nature, 15);

    // 11. New
    const newPlaces = shuffle(allPlaces.filter(p => p.is_new)).slice(0, 20);
    html += createHorizontalRow('🆕 أماكن جديدة', 'أحدث الإضافات على الدليل', newPlaces);

    container.innerHTML = html;

    // Nearby handler
    const nearbyBtn = document.getElementById('nearby-btn');
    if (nearbyBtn) {
      nearbyBtn.addEventListener('click', () => {
        nearbyBtn.textContent = '⏳ جاري تحديد موقعك...';
        nearbyBtn.disabled = true;
        if ('geolocation' in navigator) {
          navigator.geolocation.getCurrentPosition(pos => {
            const { latitude: uLat, longitude: uLng } = pos.coords;
            const withDist = allPlaces
              .filter(p => p.lat && p.lng)
              .map(p => ({
                ...p,
                _dist: Math.sqrt(Math.pow((p.lat - uLat) * 111, 2) + Math.pow((p.lng - uLng) * 111 * Math.cos(uLat * Math.PI / 180), 2))
              }))
              .sort((a, b) => a._dist - b._dist)
              .slice(0, 20);

            const resultsEl = document.getElementById('nearby-results');
            if (resultsEl && withDist.length > 0) {
              resultsEl.style.display = 'flex';
              resultsEl.innerHTML = withDist.map(p => {
                const icon = CATEGORY_ICONS[p.category] || '📍';
                const gradient = CATEGORY_GRADIENTS[p.category] || CATEGORY_GRADIENTS['أخرى'];
                const mapUrl = p.google_maps_url || `https://www.google.com/maps?q=${p.lat},${p.lng}`;
                return `
                  <div class="discover-card" style="--card-gradient:${gradient}">
                    <div class="discover-card-icon">${icon}</div>
                    <h4>${p.name_ar}</h4>
                    <span class="discover-card-dist">${p._dist < 1 ? (p._dist * 1000).toFixed(0) + ' م' : p._dist.toFixed(1) + ' كم'}</span>
                    <span class="discover-card-hood">📍 ${p.neighborhood}</span>
                    ${p.rating ? `<span class="discover-card-rating">⭐ ${p.rating}</span>` : ''}
                    <a href="${mapUrl}" target="_blank" rel="noopener" class="discover-card-link">الموقع ←</a>
                  </div>
                `;
              }).join('');
              nearbyBtn.style.display = 'none';
            }
          }, () => {
            nearbyBtn.textContent = '❌ ما قدرنا نحدد موقعك';
            nearbyBtn.disabled = false;
          }, { enableHighAccuracy: true, timeout: 10000 });
        } else {
          nearbyBtn.textContent = '❌ المتصفح ما يدعم تحديد الموقع';
        }
      });
    }
  }

  // ===== Index Page Helpers =====
  async function renderIndexSections(config) {
    const allPlaces = await loadAllPlaces();

    // Category counts
    if (config.categoryCountsSelector) {
      const el = document.querySelector(config.categoryCountsSelector);
      if (el) {
        const counts = {};
        allPlaces.forEach(p => { counts[p.category] = (counts[p.category] || 0) + 1; });
        el.querySelectorAll('[data-category-count]').forEach(badge => {
          const cat = badge.dataset.categoryCount;
          if (counts[cat]) badge.textContent = toArabicNum(counts[cat]);
        });
      }
    }

    // Trending section
    if (config.trendingSelector) {
      const el = document.querySelector(config.trendingSelector);
      if (el) {
        const trending = allPlaces
          .filter(p => p.trending && p.rating >= 4)
          .sort((a, b) => b.rating - a.rating)
          .slice(0, 8);
        el.innerHTML = '<div class="cards-grid-v2">' + trending.map(p => createPlaceCard(p)).join('') + '</div>';
      }
    }

    // New places section
    if (config.newSelector) {
      const el = document.querySelector(config.newSelector);
      if (el) {
        const newest = allPlaces.filter(p => p.is_new).sort(() => Math.random() - 0.5).slice(0, 8);
        el.innerHTML = '<div class="cards-grid-v2">' + newest.map(p => createPlaceCard(p)).join('') + '</div>';
      }
    }
  }

  // ===== Expose =====
  window.FilterEngine = {
    loadAllPlaces,
    filterPlaces,
    sortPlaces,
    createPlaceCard,
    createPaginatedGrid,
    createFilterBar,
    initCategoryPage,
    initNeighborhoodPage,
    initDiscoverPage,
    renderIndexSections,
    createHorizontalRow,
    toArabicNum,
    generateStars,
    CATEGORY_ICONS,
    CATEGORY_GRADIENTS,
    CATEGORY_LABELS,
    CATEGORY_PLURAL,
    PRICE_LABELS
  };

})();
