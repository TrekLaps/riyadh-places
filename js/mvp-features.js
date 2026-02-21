// ===== MVP Features — وين نروح بالرياض =====
// 6 features: My Places Map, Deep Rating, Top 10, Occasion Filter, Trending, Shareable Lists

(function() {
  'use strict';

  // ===== Feature 2: Deep Rating — Radar Chart =====
  // Distribute google_rating into 4 dimensions with slight variation
  function generateDimensions(rating) {
    if (!rating || rating <= 0) return null;
    // Seed-based pseudo-random from rating for consistency
    const base = rating;
    const variance = 0.3;
    // Create slight offsets that sum to ~0
    const offsets = [0.15, -0.1, 0.05, -0.1];
    const dims = {
      quality: Math.min(5, Math.max(1, base + offsets[0] * (1 + (base % 1)))),
      service: Math.min(5, Math.max(1, base + offsets[1] * (1 + (base * 3 % 1)))),
      ambiance: Math.min(5, Math.max(1, base + offsets[2] * (1 + (base * 7 % 1)))),
      value: Math.min(5, Math.max(1, base + offsets[3] * (1 + (base * 11 % 1))))
    };
    // Round to 1 decimal
    Object.keys(dims).forEach(k => dims[k] = Math.round(dims[k] * 10) / 10);
    return dims;
  }

  function createRadarChartSVG(dims, size) {
    size = size || 70;
    if (!dims) return '';
    const cx = size / 2, cy = size / 2, r = size / 2 - 8;
    const labels = ['quality', 'service', 'ambiance', 'value'];
    const angles = labels.map((_, i) => (Math.PI * 2 * i / 4) - Math.PI / 2);

    // Background grid
    let gridLines = '';
    [0.25, 0.5, 0.75, 1].forEach(scale => {
      const pts = angles.map(a =>
        `${cx + r * scale * Math.cos(a)},${cy + r * scale * Math.sin(a)}`
      ).join(' ');
      gridLines += `<polygon points="${pts}" fill="none" stroke="rgba(201,168,76,0.15)" stroke-width="0.5"/>`;
    });

    // Axis lines
    let axisLines = angles.map(a =>
      `<line x1="${cx}" y1="${cy}" x2="${cx + r * Math.cos(a)}" y2="${cy + r * Math.sin(a)}" stroke="rgba(201,168,76,0.2)" stroke-width="0.5"/>`
    ).join('');

    // Data polygon
    const dataPoints = labels.map((label, i) => {
      const val = dims[label] / 5;
      return `${cx + r * val * Math.cos(angles[i])},${cy + r * val * Math.sin(angles[i])}`;
    }).join(' ');

    return `<svg class="radar-chart-svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
      ${gridLines}${axisLines}
      <polygon points="${dataPoints}" fill="rgba(201,168,76,0.25)" stroke="#c9a84c" stroke-width="1.5"/>
      ${labels.map((_, i) => {
        const val = dims[labels[i]] / 5;
        return `<circle cx="${cx + r * val * Math.cos(angles[i])}" cy="${cy + r * val * Math.sin(angles[i])}" r="2.5" fill="#c9a84c"/>`;
      }).join('')}
    </svg>`;
  }

  function createRadarWidget(rating) {
    const dims = generateDimensions(rating);
    if (!dims) return '';
    const labelMap = {
      quality: '⭐ جودة',
      service: '👤 خدمة',
      ambiance: '✨ أجواء',
      value: '💰 قيمة'
    };
    const labelsHtml = Object.entries(dims).map(([k, v]) =>
      `<span class="radar-label">${labelMap[k]} <span class="radar-label-val">${v}</span></span>`
    ).join('');

    return `<div class="radar-chart-wrapper">
      ${createRadarChartSVG(dims)}
      <div class="radar-labels">${labelsHtml}</div>
    </div>`;
  }

  // ===== Feature 3: Top 10 in Neighborhood =====
  function createTop10Section(places, neighborhoodName) {
    if (!places || places.length === 0) return '';
    const sorted = [...places].sort((a, b) => {
      const rA = a.rating || a.google_rating || 0;
      const rB = b.rating || b.google_rating || 0;
      if (rB !== rA) return rB - rA;
      const rcA = a.review_count || a.rc || 0;
      const rcB = b.review_count || b.rc || 0;
      return rcB - rcA;
    });
    const top10 = sorted.slice(0, 10);
    const medals = ['🥇', '🥈', '🥉'];

    let html = `<div class="top-neighborhood-section">
      <h3>🏆 أفضل ١٠ أماكن${neighborhoodName ? ' في ' + neighborhoodName : ''}</h3>`;

    top10.forEach((place, i) => {
      const rank = i + 1;
      const rankClass = rank <= 3 ? `rank-${rank}` : 'rank-other';
      const rating = place.rating || place.google_rating || 0;
      const name = place.name_ar || place.n || '';
      const cat = place.category || place.c || '';
      const icon = (typeof FilterEngine !== 'undefined' && FilterEngine.CATEGORY_ICONS)
        ? (FilterEngine.CATEGORY_ICONS[cat] || '📍') : '📍';
      const placeId = place.id;

      html += `
        <a href="place.html?id=${placeId}" class="top-place-item ${rankClass}">
          <div class="top-rank-badge">${rank <= 3 ? medals[rank-1] : rank}</div>
          <div class="top-place-info">
            <div class="top-place-name">${icon} ${name}</div>
            <div class="top-place-meta">
              <span>${cat}</span>
              ${place.price_level || place.p ? `<span>${place.price_level || place.p}</span>` : ''}
            </div>
          </div>
          <div class="top-place-rating">⭐ ${rating}</div>
        </a>`;
    });

    html += '</div>';
    return html;
  }

  // ===== Feature 4: Occasion Filter =====
  const OCCASION_MAP = {
    'سهرة-شباب': {
      label: '🌙 سهرة شباب',
      match: (p) => {
        const aud = p.audience || p.au || [];
        const tags = p.tags || [];
        const pf = p.perfect_for || p.features || [];
        const cat = p.category || p.c || '';
        // Must have شباب/أصدقاء audience
        if (!aud.includes('شباب') && !aud.includes('أصدقاء')) return false;
        // And must have nightlife/hangout signals
        return tags.some(t => ['shisha', 'late_night', 'sports_bar', 'شيشة', 'بلياردو', 'ألعاب'].includes(t)) ||
          pf.some(f => ['سهرة', 'شيشة', 'رياضة', 'سهر', 'أصدقاء', 'بلايستيشن', 'ألعاب'].includes(f)) ||
          (cat === 'ترفيه') ||
          (cat === 'مطعم' && (tags.includes('shisha') || pf.some(f => ['سهرة', 'سهر'].includes(f))));
      }
    },
    'عائلي': {
      label: '👨‍👩‍👧‍👦 عائلي',
      match: (p) => {
        const aud = p.audience || p.au || [];
        return aud.includes('عوائل') || aud.includes('أطفال');
      }
    },
    'رومانسي': {
      label: '💑 رومانسي',
      match: (p) => {
        const aud = p.audience || p.au || [];
        const pf = p.perfect_for || p.features || [];
        const tags = p.tags || [];
        return aud.includes('أزواج') ||
          pf.some(f => ['رومانسي', 'أجواء رومانسية', 'romantic'].includes(f)) ||
          tags.some(t => ['romantic', 'رومانسي'].includes(t));
      }
    },
    'بزنس': {
      label: '💼 بزنس',
      match: (p) => {
        const aud = p.audience || p.au || [];
        const pf = p.perfect_for || p.features || [];
        const tags = p.tags || [];
        return aud.includes('رجال أعمال') ||
          pf.some(f => ['اجتماعات', 'عمل', 'business', 'meeting', 'أعمال'].includes(f)) ||
          tags.some(t => ['business', 'meeting', 'work_friendly', 'co-working', 'أعمال', 'اجتماعات'].includes(t)) ||
          (p.category === 'كافيه' && pf.some(f => ['لابتوب', 'عمل', 'دراسة'].includes(f)));
      }
    },
    'قعدة-هادية': {
      label: '☕ قعدة هادية',
      match: (p) => {
        const tags = p.tags || [];
        const pf = p.perfect_for || p.features || [];
        return tags.some(t => ['هادي', 'quiet', 'chill', 'تقليدي'].includes(t)) ||
          pf.some(f => ['استرخاء', 'هدوء', 'قراءة', 'هادي'].includes(f));
      }
    }
  };

  function filterByOccasion(places, occasionKey) {
    if (!occasionKey || !OCCASION_MAP[occasionKey]) return [];
    const matcher = OCCASION_MAP[occasionKey];
    return places.filter(p => {
      try { return matcher.match(p); } catch { return false; }
    }).sort((a, b) => (b.rating || b.google_rating || 0) - (a.rating || a.google_rating || 0));
  }

  function initOccasionFilter(containerSelector, allPlaces) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    let html = `<div class="occasion-filter-section">
      <div class="section-title" style="margin-bottom:16px">
        <div>
          <h2>🎯 وش المناسبة؟</h2>
          <span class="subtitle">اختر نوع الطلعة واحنا نقترح لك</span>
        </div>
      </div>
      <div class="occasion-btns" id="occasion-btns">`;
    Object.entries(OCCASION_MAP).forEach(([key, val]) => {
      html += `<button class="occasion-btn" data-occasion="${key}">${val.label}</button>`;
    });
    html += `</div><div class="occasion-results" id="occasion-results"></div></div>`;
    container.innerHTML = html;

    const resultsEl = document.getElementById('occasion-results');
    document.querySelectorAll('#occasion-btns .occasion-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const wasActive = btn.classList.contains('active');
        document.querySelectorAll('#occasion-btns .occasion-btn').forEach(b => b.classList.remove('active'));
        
        if (wasActive) {
          resultsEl.innerHTML = '';
          return;
        }

        btn.classList.add('active');
        const key = btn.dataset.occasion;
        const filtered = filterByOccasion(allPlaces, key).slice(0, 8);
        
        if (filtered.length === 0) {
          resultsEl.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:20px;">ما لقينا نتائج لهالمناسبة 🤷‍♂️</p>';
          return;
        }

        if (typeof FilterEngine !== 'undefined' && FilterEngine.createPlaceCard) {
          resultsEl.innerHTML = '<div class="cards-grid-v2">' + filtered.map(p => FilterEngine.createPlaceCard(p)).join('') + '</div>';
        } else if (typeof generatePlaceCard === 'function') {
          resultsEl.innerHTML = '<div class="cards-grid">' + filtered.map(p => generatePlaceCard(p)).join('') + '</div>';
        }
      });
    });
  }

  // ===== Feature 5: Enhanced Trending + New =====
  function initTrendingNew(trendingSelector, newSelector, allPlaces) {
    // Trending
    const trendEl = document.querySelector(trendingSelector);
    if (trendEl) {
      const trending = allPlaces
        .filter(p => p.trending || p.tr)
        .sort((a, b) => (b.rating || b.google_rating || 0) - (a.rating || a.google_rating || 0))
        .slice(0, 8);
      if (trending.length > 0) {
        const renderCard = (typeof FilterEngine !== 'undefined' && FilterEngine.createPlaceCard)
          ? FilterEngine.createPlaceCard : (typeof generatePlaceCard === 'function' ? generatePlaceCard : null);
        if (renderCard) {
          trendEl.innerHTML = '<div class="cards-grid-v2">' + trending.map(p => renderCard(p)).join('') + '</div>';
        }
      }
    }

    // New
    const newEl = document.querySelector(newSelector);
    if (newEl) {
      const newest = allPlaces
        .filter(p => p.is_new || p.nw)
        .sort(() => Math.random() - 0.5)
        .slice(0, 8);
      if (newest.length > 0) {
        const renderCard = (typeof FilterEngine !== 'undefined' && FilterEngine.createPlaceCard)
          ? FilterEngine.createPlaceCard : (typeof generatePlaceCard === 'function' ? generatePlaceCard : null);
        if (renderCard) {
          newEl.innerHTML = '<div class="cards-grid-v2">' + newest.map(p => renderCard(p)).join('') + '</div>';
        }
      }
    }
  }

  // ===== Feature 6: Shareable Lists =====
  const SHARE_LISTS_KEY = 'wain_share_lists';

  function getShareLists() {
    try { return JSON.parse(localStorage.getItem(SHARE_LISTS_KEY) || '[]'); } catch { return []; }
  }

  function saveShareLists(lists) {
    localStorage.setItem(SHARE_LISTS_KEY, JSON.stringify(lists));
  }

  function generateListId() {
    return 'list-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  }

  function encodeListToURL(list, targetPage) {
    const data = {
      n: list.name,
      e: list.emoji || '📋',
      p: list.placeIds
    };
    const encoded = btoa(unescape(encodeURIComponent(JSON.stringify(data))));
    const baseUrl = window.location.origin + window.location.pathname.replace(/[^/]*$/, '');
    const page = targetPage || 'list.html';
    return baseUrl + page + '?shared=' + encodeURIComponent(encoded);
  }

  function decodeListFromURL() {
    const params = new URLSearchParams(window.location.search);
    const shared = params.get('shared');
    if (!shared) return null;
    try {
      const json = decodeURIComponent(escape(atob(decodeURIComponent(shared))));
      return JSON.parse(json);
    } catch { return null; }
  }

  function showCreateListModal(allPlaces) {
    // Remove existing
    document.querySelector('.list-create-modal-overlay')?.remove();

    const overlay = document.createElement('div');
    overlay.className = 'list-create-modal-overlay';
    overlay.innerHTML = `
      <div class="list-create-modal">
        <h3>📋 إنشاء قائمة جديدة</h3>
        <input type="text" id="new-list-name" placeholder="اسم القائمة..." maxlength="50">
        <div class="list-modal-search">
          <input type="text" id="list-search-input" placeholder="🔍 ابحث عن مكان لإضافته...">
        </div>
        <div class="list-modal-places" id="list-modal-places"></div>
        <div style="margin-bottom:12px;color:var(--text-muted);font-size:0.85rem;">
          تم اختيار <span class="selected-count-badge" id="selected-count">0</span> مكان
        </div>
        <div class="list-modal-actions">
          <button class="btn-cancel" id="list-cancel-btn">إلغاء</button>
          <button class="btn-create" id="list-create-btn" disabled>إنشاء ومشاركة</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    requestAnimationFrame(() => overlay.classList.add('show'));

    const selectedIds = new Set();
    const placesContainer = document.getElementById('list-modal-places');
    const searchInput = document.getElementById('list-search-input');
    const nameInput = document.getElementById('new-list-name');
    const createBtn = document.getElementById('list-create-btn');
    const cancelBtn = document.getElementById('list-cancel-btn');
    const countBadge = document.getElementById('selected-count');

    function renderPlacesList(query) {
      let filtered = allPlaces;
      if (query) {
        const q = query.toLowerCase();
        filtered = allPlaces.filter(p => {
          const name = (p.name_ar || p.n || '').toLowerCase();
          const nameEn = (p.name_en || p.ne || '').toLowerCase();
          return name.includes(q) || nameEn.includes(q);
        });
      }
      filtered = filtered.slice(0, 50);
      placesContainer.innerHTML = filtered.map(p => {
        const id = p.id;
        const sel = selectedIds.has(id);
        const name = p.name_ar || p.n || '';
        const cat = p.category || p.c || '';
        const hood = p.neighborhood || p.h || '';
        const rating = p.rating || p.google_rating || 0;
        return `<div class="list-modal-place-item ${sel ? 'selected' : ''}" data-id="${id}">
          <div class="place-check">${sel ? '✓' : ''}</div>
          <div>
            <div class="list-modal-place-name">${name}</div>
            <div class="list-modal-place-meta">⭐ ${rating} · ${cat} · ${hood}</div>
          </div>
        </div>`;
      }).join('');

      placesContainer.querySelectorAll('.list-modal-place-item').forEach(item => {
        item.addEventListener('click', () => {
          const id = item.dataset.id;
          if (selectedIds.has(id)) {
            selectedIds.delete(id);
          } else {
            selectedIds.add(id);
          }
          item.classList.toggle('selected');
          item.querySelector('.place-check').textContent = selectedIds.has(id) ? '✓' : '';
          countBadge.textContent = selectedIds.size;
          createBtn.disabled = selectedIds.size === 0 || !nameInput.value.trim();
        });
      });
    }

    renderPlacesList('');

    let searchTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => renderPlacesList(searchInput.value.trim()), 200);
    });

    nameInput.addEventListener('input', () => {
      createBtn.disabled = selectedIds.size === 0 || !nameInput.value.trim();
    });

    cancelBtn.addEventListener('click', () => {
      overlay.classList.remove('show');
      setTimeout(() => overlay.remove(), 300);
    });

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('show');
        setTimeout(() => overlay.remove(), 300);
      }
    });

    createBtn.addEventListener('click', () => {
      const name = nameInput.value.trim();
      if (!name || selectedIds.size === 0) return;

      const list = {
        id: generateListId(),
        name: name,
        emoji: '📋',
        placeIds: [...selectedIds],
        created: Date.now()
      };

      // Save locally
      const lists = getShareLists();
      lists.unshift(list);
      saveShareLists(lists);

      // Generate share link
      const shareUrl = encodeListToURL(list);

      // Show share result
      overlay.querySelector('.list-create-modal').innerHTML = `
        <h3>✅ تم إنشاء القائمة!</h3>
        <p style="margin-bottom:12px;">"${name}" — ${selectedIds.size} مكان</p>
        <div class="share-link-box">
          <input type="text" value="${shareUrl}" readonly id="share-link-input">
          <button onclick="navigator.clipboard.writeText(document.getElementById('share-link-input').value).then(()=>{this.textContent='✅ تم'})">📋 نسخ</button>
        </div>
        <div class="list-modal-actions" style="margin-top:16px;">
          <button class="btn-cancel" onclick="this.closest('.list-create-modal-overlay').classList.remove('show');setTimeout(()=>this.closest('.list-create-modal-overlay').remove(),300)">إغلاق</button>
          <button class="btn-create" onclick="window.open('https://wa.me/?text='+encodeURIComponent('${name} 📋\\n'+document.getElementById('share-link-input').value),'_blank')">📲 شارك واتساب</button>
        </div>
      `;

      // Dispatch event for other components
      window.dispatchEvent(new CustomEvent('list-created', { detail: list }));
    });
  }

  // ===== Feature 1: My Places Map Page Logic =====
  function initMyPlacesPage(allPlaces) {
    const container = document.getElementById('my-places-content');
    if (!container) return;

    // Check for shared list
    const shared = decodeListFromURL();
    const isSharedView = !!shared;

    let placeIds;
    let title;

    if (isSharedView) {
      placeIds = shared.p || [];
      title = shared.n || 'قائمة مشتركة';
    } else {
      placeIds = typeof getFavorites === 'function' ? getFavorites() : JSON.parse(localStorage.getItem('wain_favorites') || '[]');
      title = 'أماكني المفضلة';
    }

    const myPlaces = allPlaces.filter(p => placeIds.includes(p.id));
    const placesWithCoords = myPlaces.filter(p => (p.lat || p.la) && (p.lng || p.lo));

    // Stats
    const categories = {};
    myPlaces.forEach(p => {
      const cat = p.category || p.c || 'أخرى';
      categories[cat] = (categories[cat] || 0) + 1;
    });

    let html = '';

    if (isSharedView) {
      html += `<div class="shared-list-banner">
        <h3>${shared.e || '📋'} ${title}</h3>
        <p>${myPlaces.length} مكان في هالقائمة</p>
        <button class="btn-save-shared" onclick="MVPFeatures.saveSharedList()">❤️ احفظ القائمة عندي</button>
      </div>`;
    }

    html += `<div class="my-places-toolbar">
      <button class="btn-share-list" onclick="MVPFeatures.shareMyPlaces()">📲 شارك أماكنك</button>
    </div>`;

    html += `<div class="my-places-stats">
      <div class="my-places-stat"><span class="stat-num">${myPlaces.length}</span><span class="stat-label">مكان</span></div>
      <div class="my-places-stat"><span class="stat-num">${Object.keys(categories).length}</span><span class="stat-label">تصنيف</span></div>
      <div class="my-places-stat"><span class="stat-num">${placesWithCoords.length}</span><span class="stat-label">على الخريطة</span></div>
    </div>`;

    html += '<div class="my-places-map-container"><div id="my-places-map"></div></div>';

    // Search and filter bar for my places
    if (myPlaces.length > 3 && !isSharedView) {
      const catList = Object.keys(categories);
      html += `<div class="my-places-filter-bar">
        <input type="text" id="my-places-search" class="my-places-search-input" placeholder="🔍 ابحث في أماكنك..." autocomplete="off">
        <select id="my-places-cat-filter" class="my-places-filter-select">
          <option value="all">كل الأقسام</option>
          ${catList.map(c => `<option value="${c}">${c} (${categories[c]})</option>`).join('')}
        </select>
      </div>`;
    }

    // Places grid
    html += '<div id="my-places-grid">';
    if (myPlaces.length > 0) {
      const renderCard = (typeof FilterEngine !== 'undefined' && FilterEngine.createPlaceCard)
        ? FilterEngine.createPlaceCard : (typeof generatePlaceCard === 'function' ? generatePlaceCard : null);
      if (renderCard) {
        html += '<div class="cards-grid-v2">' + myPlaces.map(p => renderCard(p)).join('') + '</div>';
      }
    } else {
      html += `<div style="text-align:center;padding:40px;color:var(--text-muted)">
        <div style="font-size:3rem;margin-bottom:12px">❤️</div>
        <h3>ما عندك أماكن محفوظة بعد</h3>
        <p>اضغط ❤️ على أي مكان عشان يظهر هنا</p>
        <a href="index.html" style="display:inline-block;margin-top:16px;background:var(--gold);color:#fff;padding:10px 24px;border-radius:10px;text-decoration:none;font-weight:700;">اكتشف الأماكن</a>
      </div>`;
    }
    html += '</div>';

    container.innerHTML = html;

    // Bind search/filter events for my places
    if (myPlaces.length > 3 && !isSharedView) {
      const searchInput = document.getElementById('my-places-search');
      const catFilter = document.getElementById('my-places-cat-filter');
      const gridEl = document.getElementById('my-places-grid');
      const renderCard = (typeof FilterEngine !== 'undefined' && FilterEngine.createPlaceCard)
        ? FilterEngine.createPlaceCard : (typeof generatePlaceCard === 'function' ? generatePlaceCard : null);

      function filterMyPlaces() {
        const q = (searchInput?.value || '').toLowerCase().trim();
        const cat = catFilter?.value || 'all';
        let filtered = myPlaces;
        if (q) {
          filtered = filtered.filter(p => {
            const name = (p.name_ar || p.n || '').toLowerCase();
            const nameEn = (p.name_en || p.ne || '').toLowerCase();
            const hood = (p.neighborhood || p.h || '').toLowerCase();
            return name.includes(q) || nameEn.includes(q) || hood.includes(q);
          });
        }
        if (cat !== 'all') {
          filtered = filtered.filter(p => (p.category || p.c) === cat);
        }
        if (renderCard && gridEl) {
          if (filtered.length > 0) {
            gridEl.innerHTML = '<div class="cards-grid-v2">' + filtered.map(p => renderCard(p)).join('') + '</div>';
          } else {
            gridEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-muted);">ما لقينا نتائج 🤷‍♂️</div>';
          }
        }
      }

      let searchTimer;
      if (searchInput) searchInput.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(filterMyPlaces, 250); });
      if (catFilter) catFilter.addEventListener('change', filterMyPlaces);
    }

    // Initialize Leaflet map
    if (placesWithCoords.length > 0) {
      initLeafletMap(placesWithCoords);
    } else {
      const mapEl = document.getElementById('my-places-map');
      if (mapEl) {
        mapEl.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-muted);font-size:1.1rem;">🗺️ أضف أماكن مع إحداثيات لعرضها على الخريطة</div>';
      }
    }
  }

  function initLeafletMap(places) {
    const mapEl = document.getElementById('my-places-map');
    if (!mapEl || typeof L === 'undefined') return;

    const map = L.map('my-places-map').setView([24.7136, 46.6753], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map);

    const bounds = [];
    const goldIcon = L.divIcon({
      className: 'custom-map-marker',
      html: '<div style="background:linear-gradient(135deg,#c9a84c,#b08d3a);width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;box-shadow:0 4px 12px rgba(201,168,76,0.4);border:2px solid #fff;">📍</div>',
      iconSize: [30, 30],
      iconAnchor: [15, 15],
      popupAnchor: [0, -15]
    });

    places.forEach(p => {
      const lat = p.lat || p.la;
      const lng = p.lng || p.lo;
      if (!lat || !lng) return;
      const name = p.name_ar || p.n || '';
      const rating = p.rating || p.google_rating || 0;
      const cat = p.category || p.c || '';

      const marker = L.marker([lat, lng], { icon: goldIcon }).addTo(map);
      marker.bindPopup(`<div style="direction:rtl;text-align:right;font-family:Tajawal,sans-serif;min-width:150px;">
        <strong>${name}</strong><br>
        ⭐ ${rating} · ${cat}<br>
        <a href="place.html?id=${p.id}" style="color:#c9a84c;">اعرف أكثر</a>
      </div>`);
      bounds.push([lat, lng]);
    });

    if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [30, 30] });
    }
  }

  function shareMyPlaces() {
    const favIds = typeof getFavorites === 'function' ? getFavorites() : JSON.parse(localStorage.getItem('wain_favorites') || '[]');
    if (favIds.length === 0) {
      if (typeof showToast === 'function') showToast('أضف أماكن للمفضلة أولاً ❤️');
      return;
    }
    const list = { name: 'أماكني المفضلة', emoji: '❤️', placeIds: favIds };
    const url = encodeListToURL(list, 'list.html');
    navigator.clipboard.writeText(url).then(() => {
      if (typeof showToast === 'function') showToast('✅ تم نسخ رابط أماكنك!');
    }).catch(() => {
      prompt('انسخ الرابط:', url);
    });
  }

  function saveSharedList() {
    const shared = decodeListFromURL();
    if (!shared) return;
    const lists = getShareLists();
    lists.unshift({
      id: generateListId(),
      name: shared.n,
      emoji: shared.e || '📋',
      placeIds: shared.p,
      created: Date.now()
    });
    saveShareLists(lists);
    if (typeof showToast === 'function') showToast('✅ تم حفظ القائمة!');
  }

  // ===== Inject Radar Charts into existing cards =====
  function injectRadarCharts() {
    // For filter-engine v2 cards
    document.querySelectorAll('.card-v2-rating').forEach(el => {
      if (el.querySelector('.radar-chart-wrapper')) return;
      const ratingEl = el.querySelector('.card-v2-rating-num');
      if (ratingEl) {
        const rating = parseFloat(ratingEl.textContent);
        if (rating > 0) {
          const radarHtml = createRadarWidget(rating);
          if (radarHtml) {
            el.insertAdjacentHTML('afterend', radarHtml);
          }
        }
      }
    });

    // For main.js v1 cards
    document.querySelectorAll('.card-rating-block').forEach(el => {
      if (el.querySelector('.radar-chart-wrapper')) return;
      const bigNum = el.querySelector('.big-number');
      if (bigNum) {
        const rating = parseFloat(bigNum.textContent);
        if (rating > 0) {
          const radarHtml = createRadarWidget(rating);
          if (radarHtml) {
            el.insertAdjacentHTML('afterend', radarHtml);
          }
        }
      }
    });
  }

  // ===== Inject Top 10 into neighborhood pages =====
  function injectTop10(neighborhoodName) {
    const targetEl = document.getElementById('category-summary') || document.getElementById('filter-bar');
    if (!targetEl) return;

    if (typeof FilterEngine !== 'undefined' && FilterEngine.loadAllPlaces) {
      FilterEngine.loadAllPlaces().then(allPlaces => {
        const hoodPlaces = allPlaces.filter(p =>
          p.neighborhood === neighborhoodName ||
          (p.neighborhood && p.neighborhood.includes(neighborhoodName))
        );
        if (hoodPlaces.length >= 3) {
          const html = createTop10Section(hoodPlaces, neighborhoodName);
          targetEl.insertAdjacentHTML('afterend', html);
        }
      });
    }
  }

  // ===== Auto-init on DOMContentLoaded =====
  function autoInit() {
    const path = window.location.pathname;

    // Inject radar charts after cards render (with delay)
    setTimeout(injectRadarCharts, 1500);
    // Re-inject after scroll (infinite pagination)
    let radarTimer;
    window.addEventListener('scroll', () => {
      clearTimeout(radarTimer);
      radarTimer = setTimeout(injectRadarCharts, 500);
    });

    // Auto-detect neighborhood pages
    const neighborhoodMatch = path.match(/neighborhood-(.+)\.html/);
    if (neighborhoodMatch) {
      // Get neighborhood name from page header or FilterEngine config
      setTimeout(() => {
        const pageHeader = document.querySelector('.page-header h2');
        if (pageHeader) {
          const text = pageHeader.textContent.replace(/🏘️/g, '').replace(/أفضل أماكن/g, '').replace(/^حي\s+/g, '').trim();
          if (text) { injectTop10(text); return; }
        }
        // Fallback: try common mappings
          const slugMap = {
            'olaya': 'العليا', 'malqa': 'الملقا', 'hittin': 'حطين',
            'yasmin': 'الياسمين', 'rabee': 'الربيع', 'narjis': 'النرجس',
            'wurud': 'الورود', 'sahafa': 'الصحافة', 'muruj': 'المروج',
            'nakheel': 'النخيل', 'diriyah': 'الدرعية', 'kafd': 'KAFD',
            'safarat': 'السفارات', 'malz': 'الملز', 'malaz': 'الملز',
            'aqiq': 'العقيق', 'sulaymaniyah': 'السليمانية',
            'gharnata': 'غرناطة', 'rabwa': 'الربوة', 'arid': 'العارض',
            'ghdir': 'الغدير', 'suwaidi': 'السويدي', 'rawdah': 'الروضة',
            'muhammadiyah': 'المحمدية', 'yarmuk': 'اليرموك',
            'rawabi': 'الروابي', 'salam': 'السلام', 'ghadir': 'الغدير',
            'diplomasi': 'الدبلوماسي', 'king-faisal': 'الملك فيصل',
            'deira': 'الديرة', 'falah': 'الفلاح', 'manar': 'المنار',
            'nada': 'الندى', 'qirawan': 'القيروان', 'qayrawan': 'القيروان',
            'thumamah': 'الثمامة', 'urubah': 'العروبة', 'banban': 'بنبان',
            'mansurah': 'المنصورة', 'mansourah': 'المنصورة',
            'ammariyah': 'العمارية', 'ghirnatah2': 'غرناطة'
          };
          const slug = neighborhoodMatch[1];
          if (slugMap[slug]) injectTop10(slugMap[slug]);
      }, 800);
    }

    // Index page: add occasion filter section
    if (path.endsWith('index.html') || path.endsWith('/') || path === '') {
      const loadData = (typeof FilterEngine !== 'undefined' && FilterEngine.loadAllPlaces)
        ? FilterEngine.loadAllPlaces
        : (typeof loadPlaces === 'function' ? loadPlaces : null);

      if (loadData) {
        loadData().then(allPlaces => {
          if (allPlaces && allPlaces.length > 0) {
            // Add occasion filter before trending section
            const trendingSection = document.querySelector('#trending-places')?.closest('section');
            if (trendingSection) {
              const occasionDiv = document.createElement('section');
              occasionDiv.className = 'container';
              occasionDiv.id = 'occasion-filter-container';
              trendingSection.parentNode.insertBefore(occasionDiv, trendingSection);
              initOccasionFilter('#occasion-filter-container', allPlaces);
            }
          }
        });
      }
    }

    // My places page
    if (path.includes('my-places.html')) {
      const loadData = (typeof FilterEngine !== 'undefined' && FilterEngine.loadAllPlaces)
        ? FilterEngine.loadAllPlaces
        : (typeof loadPlaces === 'function' ? loadPlaces : null);

      if (loadData) {
        loadData().then(allPlaces => {
          if (allPlaces) initMyPlacesPage(allPlaces);
        });
      }
    }
  }

  document.addEventListener('DOMContentLoaded', autoInit);

  // ===== Expose =====
  window.MVPFeatures = {
    generateDimensions,
    createRadarChartSVG,
    createRadarWidget,
    createTop10Section,
    filterByOccasion,
    initOccasionFilter,
    initTrendingNew,
    showCreateListModal,
    initMyPlacesPage,
    shareMyPlaces,
    saveSharedList,
    injectRadarCharts,
    injectTop10,
    encodeListToURL,
    decodeListFromURL,
    getShareLists,
    saveShareLists,
    OCCASION_MAP
  };

})();
