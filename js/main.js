// ===== وين نروح الرياض - Main JavaScript v2 =====

const categoryIcons = { 'cafe': '☕', 'restaurant': '🍽️', 'activity': '🎭', 'تسوق': '🛍️', 'طبيعة': '🏞️', 'كافيه': '☕', 'مطعم': '🍽️', 'ترفيه': '🎭', 'حلويات': '🍰', 'فعاليات': '🎪', 'شاليه': '🏕️', 'فنادق': '🏨', 'مولات': '🛒', 'متاحف': '🏛️' };
const categoryGradients = { 'مطعم': 'linear-gradient(135deg, #c0392b, #e74c3c)', 'كافيه': 'linear-gradient(135deg, #6F4E37, #A0785A)', 'ترفيه': 'linear-gradient(135deg, #8e44ad, #9b59b6)', 'حلويات': 'linear-gradient(135deg, #e84393, #fd79a8)', 'طبيعة': 'linear-gradient(135deg, #27ae60, #2ecc71)', 'تسوق': 'linear-gradient(135deg, #2980b9, #3498db)', 'شاليه': 'linear-gradient(135deg, #d35400, #e67e22)', 'فنادق': 'linear-gradient(135deg, #1a1a2e, #16213e)', 'مولات': 'linear-gradient(135deg, #2c3e50, #34495e)', 'متاحف': 'linear-gradient(135deg, #7f8c8d, #95a5a6)', 'فعاليات': 'linear-gradient(135deg, #f39c12, #f1c40f)' };
const categoryNames = { 'cafe': 'كافيه', 'restaurant': 'مطعم', 'activity': 'ترفيه', 'تسوق': 'تسوق', 'طبيعة': 'طبيعة', 'كافيه': 'كافيه', 'مطعم': 'مطعم', 'ترفيه': 'ترفيه', 'حلويات': 'حلويات', 'فعاليات': 'فعاليات' };

let placesData = [];

async function loadPlaces() {
  try {
    const response = await fetch('data/places-light.json');
    placesData = await response.json();
    return placesData;
  } catch (error) {
    void 0;
    return [];
  }
}

async function loadPlacesDetail() {
  try {
    const response = await fetch('data/places-detail.json');
    placesData = await response.json();
    return placesData;
  } catch (error) {
    void 0;
    return [];
  }
}

// Format number with Arabic locale
function formatNumber(num) {
  return num.toLocaleString('ar-SA');
}

// Generate star rating HTML
function generateStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.3;
  const empty = 5 - full - (half ? 1 : 0);
  return '★'.repeat(full) + (half ? '★' : '') + '☆'.repeat(empty);
}

// ===== Favorites System =====
function getFavorites() {
  try {
    return JSON.parse(localStorage.getItem('wain_favorites') || '[]');
  } catch { return []; }
}

function isFavorite(placeId) {
  return getFavorites().includes(placeId);
}

function toggleFavorite(placeId) {
  const favs = getFavorites();
  const index = favs.indexOf(placeId);
  if (index > -1) {
    favs.splice(index, 1);
  } else {
    favs.push(placeId);
  }
  localStorage.setItem('wain_favorites', JSON.stringify(favs));
  // Update all fav buttons on page
  document.querySelectorAll(`.fav-btn[data-id="${placeId}"]`).forEach(btn => {
    btn.classList.toggle('is-fav', favs.includes(placeId));
    btn.innerHTML = favs.includes(placeId) ? '❤️' : '🤍';
    btn.title = favs.includes(placeId) ? 'إزالة من المفضلة' : 'أضف للمفضلة';
  });
  return favs.includes(placeId);
}

// ===== Sharing =====
function shareWhatsApp(place) {
  const url = `${window.location.origin}/place.html?id=${place.id}`;
  const text = `🏙️ ${place.name_ar}\n⭐ ${place.google_rating} (${formatNumber(place.review_count)} تقييم)\n📍 ${place.neighborhood}\n\n${place.description_ar.slice(0, 100)}...\n\n${url}\n\nمن موقع وين نروح بالرياض؟`;
  window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
}

function shareTwitter(place) {
  const url = `${window.location.origin}/place.html?id=${place.id}`;
  const text = `🏙️ ${place.name_ar} — ⭐ ${place.google_rating}\n📍 ${place.neighborhood}\n\nمن @wain_nrooh`;
  window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
}

function shareCopy(place) {
  const url = `${window.location.origin}/place.html?id=${place.id}`;
  const text = `${place.name_ar} — ⭐ ${place.google_rating} | ${place.neighborhood}\n${url}`;
  navigator.clipboard.writeText(text).then(() => {
    // Show quick toast
    showToast('✅ تم نسخ الرابط');
  }).catch(() => {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('✅ تم نسخ الرابط');
  });
}

function showToast(message) {
  let toast = document.getElementById('wain-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'wain-toast';
    toast.style.cssText = `
      position:fixed;bottom:80px;left:50%;transform:translateX(-50%) translateY(20px);
      background:#0a1628;color:#c9a84c;padding:12px 24px;border-radius:12px;
      font-family:'Tajawal',sans-serif;font-size:14px;font-weight:700;
      box-shadow:0 8px 30px rgba(0,0,0,0.3);z-index:9999;
      opacity:0;transition:all 0.3s ease;pointer-events:none;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.style.opacity = '1';
  toast.style.transform = 'translateX(-50%) translateY(0)';
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
  }, 2000);
}

// Generate place card HTML — enhanced with ratings, sharing, favorites
function generatePlaceCard(place) {
  const isFav = isFavorite(place.id);
  return `
    <article class="place-card" data-category="${place.category}" data-id="${place.id}" data-neighborhood="${place.neighborhood}" data-price="${place.price_level}">
      <div class="place-card-image" style="background:${categoryGradients[place.category] || 'linear-gradient(135deg, #0a1628, #162040)'}">
        <span class="card-category-icon">${categoryIcons[place.category] || '📍'}</span>
        ${place.trending ? '<span class="trending-badge">🔥 رائج</span>' : ''}
        ${place.is_new ? '<span class="new-badge">جديد</span>' : ''}
        <button class="fav-btn ${isFav ? 'is-fav' : ''}" data-id="${place.id}" title="${isFav ? 'إزالة من المفضلة' : 'أضف للمفضلة'}" onclick="toggleFavorite('${place.id}')">${isFav ? '❤️' : '🤍'}</button>
        <button class="compare-btn ${isInCompare(place.id) ? 'in-compare' : ''}" data-id="${place.id}" title="${isInCompare(place.id) ? 'إزالة من المقارنة' : 'أضف للمقارنة'}" onclick="event.stopPropagation();toggleCompare('${place.id}')">${isInCompare(place.id) ? '⚖️ ✓' : '⚖️'}</button>
        <button class="list-add-btn" data-id="${place.id}" title="أضف لقائمة" onclick="event.stopPropagation();if(typeof showAddToListModal==='function')showAddToListModal('${place.id}')">📋</button>
      </div>
      <div class="place-card-body">
        <span class="category-badge">${categoryNames[place.category] || place.category}</span>
        <h3>${place.name_ar}</h3>
        <div class="neighborhood">${place.neighborhood}</div>

        <div class="card-rating-block">
          <div class="card-rating-big">
            <span class="big-number">${place.google_rating}</span>
            <span class="stars-small">${generateStars(place.google_rating)}</span>
          </div>
          <div class="card-rating-meta">
            <span class="review-count"><span class="count-num">${formatNumber(place.review_count)}</span> تقييم</span>
            <span class="google-badge">⭐ تقييم قوقل</span>
          </div>
        </div>

        <div class="review-quote-line">${place.review_quote_ar || place.review_quote || ''}</div>

        ${typeof renderBusynessBadge === 'function' ? renderBusynessBadge(place) : ''}
        <span class="price-range">${place.price_level}</span>
        ${place.is_free ? '<span class="free-badge">🆓 مجاني</span>' : ''}
        <div class="card-actions">
          <a href="place.html?id=${place.id}" class="btn-primary">اعرف أكثر</a>
          <a href="${place.google_maps_url}" target="_blank" class="btn-outline">📍 الموقع</a>
        </div>
        <div class="card-share-row">
          <button class="share-btn share-whatsapp" onclick='shareWhatsApp(${JSON.stringify({id:place.id,name_ar:place.name_ar,google_rating:place.google_rating,review_count:place.review_count,neighborhood:place.neighborhood,description_ar:place.description_ar.slice(0,120)})})' title="شارك واتساب">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            واتساب
          </button>
          <button class="share-btn share-twitter" onclick='shareTwitter(${JSON.stringify({id:place.id,name_ar:place.name_ar,google_rating:place.google_rating,neighborhood:place.neighborhood})})' title="شارك تويتر">
            𝕏
          </button>
          <button class="share-btn share-copy" onclick='shareCopy(${JSON.stringify({id:place.id,name_ar:place.name_ar,google_rating:place.google_rating,neighborhood:place.neighborhood})})' title="نسخ الرابط">
            🔗
          </button>
        </div>
      </div>
    </article>
  `;
}

// Generate ad slot HTML
function generateAdSlot(location, type = 'inline') {
  return `
    <!-- AD SLOT: ${location} -->
    <div class="ad-slot ad-slot-${type}" data-ad-slot="${location}">
      <span>مساحة إعلانية - ${location}</span>
    </div>
  `;
}

// Render cards with interleaved ads
function renderCardsWithAds(places, container) {
  if (places.length === 0) {
    container.innerHTML = `
      <div class="no-results">
        <div class="emoji">🔍</div>
        <h3>ما لقينا نتائج</h3>
        <p>جرب تغيير الفلتر أو البحث</p>
      </div>
    `;
    return;
  }
  let html = '<div class="cards-grid">';
  places.forEach((place, index) => {
    html += generatePlaceCard(place);
    if ((index + 1) % 3 === 0 && index < places.length - 1) {
      html += '</div>';
      html += generateAdSlot(`بين البطاقات - بعد البطاقة ${index + 1}`, 'inline');
      html += '<div class="cards-grid">';
    }
  });
  html += '</div>';
  container.innerHTML = html;
}

// ===== Sort & Filter =====

function sortPlaces(places, sortBy) {
  const sorted = [...places];
  switch (sortBy) {
    case 'rating-desc':
      return sorted.sort((a, b) => b.google_rating - a.google_rating);
    case 'reviews-desc':
      return sorted.sort((a, b) => b.review_count - a.review_count);
    case 'trending':
      return sorted.sort((a, b) => (b.trending ? 1 : 0) - (a.trending ? 1 : 0));
    case 'newest':
      return sorted.sort((a, b) => (b.is_new ? 1 : 0) - (a.is_new ? 1 : 0));
    default:
      return sorted;
  }
}

function filterPlaces(places, filters) {
  return places.filter(p => {
    if (filters.category && filters.category !== 'all' && p.category !== filters.category) return false;
    if (filters.neighborhood && filters.neighborhood !== 'all' && p.neighborhood !== filters.neighborhood) return false;
    if (filters.priceLevel && filters.priceLevel !== 'all' && p.price_level !== filters.priceLevel) return false;
    if (filters.minRating && p.google_rating < parseFloat(filters.minRating)) return false;
    if (filters.audience && filters.audience !== 'all') {
      if (!p.audience || !p.audience.includes(filters.audience)) return false;
    }
    if (filters.freeOnly && !p.is_free) return false;
    if (filters.cuisine && filters.cuisine !== 'all') {
      if (p.cuisine !== filters.cuisine) return false;
    }
    if (filters.trendingOnly && !p.trending) return false;
    return true;
  });
}

// Get unique neighborhoods from a list
function getNeighborhoods(places) {
  return [...new Set(places.map(p => p.neighborhood))].sort();
}

// Get unique cuisines from places
function getCuisines(places) {
  return [...new Set(places.map(p => p.cuisine).filter(Boolean))].sort();
}

// Generate sort/filter bar HTML — enhanced v2
function generateSortFilterBar(totalCount, neighborhoods, opts = {}) {
  const showCategory = opts.showCategory !== false;
  const showNeighborhood = opts.showNeighborhood !== false;
  const showPrice = opts.showPrice !== false;
  const showAudience = opts.showAudience !== false;
  const showCuisine = opts.showCuisine || false;
  const cuisines = opts.cuisines || [];
  const showFree = opts.showFree !== false;
  const showTrending = opts.showTrending !== false;

  return `
    <div class="sort-filter-bar">
      <div class="results-count">عرض <strong>${formatNumber(totalCount)}</strong> مكان</div>
      <div class="sort-filter-controls">
        <select class="sort-select" id="sort-select">
          <option value="rating-desc">⭐ الأعلى تقييماً</option>
          <option value="reviews-desc">💬 الأكثر تقييمات</option>
          <option value="trending">🔥 الرائج</option>
          <option value="newest">🆕 الأحدث</option>
        </select>
        ${showNeighborhood ? `
        <select class="filter-select" id="filter-neighborhood">
          <option value="all">📍 كل الأحياء</option>
          ${neighborhoods.map(n => `<option value="${n}">${n}</option>`).join('')}
        </select>` : ''}
        ${showPrice ? `
        <select class="filter-select" id="filter-price">
          <option value="all">💰 كل الأسعار</option>
          <option value="$">$ اقتصادي</option>
          <option value="$$">$$ متوسط</option>
          <option value="$$$">$$$ مرتفع</option>
          <option value="$$$$">$$$$ فاخر</option>
        </select>` : ''}
        ${showCategory ? `
        <select class="filter-select" id="filter-category">
          <option value="all">📂 كل التصنيفات</option>
          <option value="كافيه">☕ كافيه</option>
          <option value="مطعم">🍽️ مطعم</option>
          <option value="ترفيه">🎭 ترفيه</option>
          <option value="تسوق">🛍️ تسوق</option>
          <option value="طبيعة">🏞️ طبيعة</option>
          <option value="حلويات">🍰 حلويات</option>
          <option value="فعاليات">🎪 فعاليات</option>
        </select>` : ''}
        ${showCuisine && cuisines.length > 0 ? `
        <select class="filter-select" id="filter-cuisine">
          <option value="all">🍴 كل المطابخ</option>
          ${cuisines.map(c => `<option value="${c}">${c}</option>`).join('')}
        </select>` : ''}
      </div>
    </div>
    <div class="advanced-filters">
      ${showAudience ? `
      <div class="filter-group">
        <span class="filter-label">👥 الجمهور:</span>
        <div class="audience-chips">
          <button class="audience-chip active" data-audience="all">الكل</button>
          <button class="audience-chip" data-audience="عوائل">👨‍👩‍👧‍👦 عوائل</button>
          <button class="audience-chip" data-audience="شباب">🧑‍🤝‍🧑 شباب</button>
          <button class="audience-chip" data-audience="أزواج">💑 أزواج</button>
          <button class="audience-chip" data-audience="أطفال">👶 أطفال</button>
        </div>
      </div>` : ''}
      <div class="filter-group">
        ${showFree ? `<button class="toggle-chip" id="filter-free">🆓 مجاني فقط</button>` : ''}
        ${showTrending ? `<button class="toggle-chip" id="filter-trending">🔥 هابّ الحين</button>` : ''}
      </div>
    </div>
  `;
}

// Initialize sort/filter controls — enhanced v2
function initSortFilter(sourcePlaces, container, resultsCountEl, opts = {}) {
  let currentAudience = 'all';
  let freeOnly = false;
  let trendingOnly = false;

  const applyAll = () => {
    const sortBy = document.getElementById('sort-select')?.value || 'rating-desc';
    const filters = {
      category: document.getElementById('filter-category')?.value || 'all',
      neighborhood: document.getElementById('filter-neighborhood')?.value || 'all',
      priceLevel: document.getElementById('filter-price')?.value || 'all',
      cuisine: document.getElementById('filter-cuisine')?.value || 'all',
      audience: currentAudience,
      freeOnly: freeOnly,
      trendingOnly: trendingOnly,
    };
    let result = filterPlaces(sourcePlaces, filters);
    result = sortPlaces(result, sortBy);
    renderCardsWithAds(result, container);
    if (resultsCountEl) {
      resultsCountEl.innerHTML = `عرض <strong>${formatNumber(result.length)}</strong> مكان`;
    }
  };

  ['sort-select', 'filter-category', 'filter-neighborhood', 'filter-price', 'filter-cuisine'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', applyAll);
  });

  // Audience chips
  document.querySelectorAll('.audience-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.audience-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentAudience = chip.dataset.audience;
      applyAll();
    });
  });

  // Free toggle
  const freeBtn = document.getElementById('filter-free');
  if (freeBtn) {
    freeBtn.addEventListener('click', () => {
      freeOnly = !freeOnly;
      freeBtn.classList.toggle('active', freeOnly);
      applyAll();
    });
  }

  // Trending toggle
  const trendingBtn = document.getElementById('filter-trending');
  if (trendingBtn) {
    trendingBtn.addEventListener('click', () => {
      trendingOnly = !trendingOnly;
      trendingBtn.classList.toggle('active', trendingOnly);
      applyAll();
    });
  }
}

// Search places
function searchPlaces(query) {
  const q = query.toLowerCase().trim();
  if (!q) return placesData;
  return placesData.filter(p =>
    p.name_ar.includes(q) || p.name_en.toLowerCase().includes(q) ||
    p.description_ar.includes(q) || p.neighborhood.includes(q) ||
    (categoryNames[p.category] || p.category || '').includes(q) || (p.review_quote_ar || p.review_quote || '').includes(q) ||
    (p.cuisine || '').includes(q)
  );
}

function getTrendingPlaces() { return placesData.filter(p => p.trending).slice(0, 5); }
function getNewPlaces() { return placesData.filter(p => p.is_new); }
function getPlaceById(id) { return placesData.find(p => p.id === id); }

// ===== Compare System =====
function getCompareList() {
  try { return JSON.parse(localStorage.getItem('wain_compare') || '[]'); }
  catch { return []; }
}

function isInCompare(placeId) {
  return getCompareList().includes(placeId);
}

function toggleCompare(placeId) {
  let list = getCompareList();
  const index = list.indexOf(placeId);
  if (index > -1) {
    list.splice(index, 1);
  } else {
    if (list.length >= 2) {
      // Replace the oldest
      list.shift();
    }
    list.push(placeId);
  }
  localStorage.setItem('wain_compare', JSON.stringify(list));
  updateCompareButtons();
  updateCompareBar();
  return list.includes(placeId);
}

function updateCompareButtons() {
  const list = getCompareList();
  document.querySelectorAll('.compare-btn').forEach(btn => {
    const id = btn.dataset.id;
    const inList = list.includes(id);
    btn.classList.toggle('in-compare', inList);
    btn.innerHTML = inList ? '⚖️ ✓' : '⚖️';
    btn.title = inList ? 'إزالة من المقارنة' : 'أضف للمقارنة';
  });
}

function updateCompareBar() {
  const list = getCompareList();
  let bar = document.getElementById('compare-floating-bar');
  
  if (list.length === 0) {
    if (bar) bar.remove();
    return;
  }

  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'compare-floating-bar';
    bar.style.cssText = `
      position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
      background:var(--primary,#0a1628);color:white;
      padding:12px 24px;border-radius:16px;
      font-family:'Tajawal',sans-serif;font-size:14px;font-weight:700;
      box-shadow:0 8px 30px rgba(0,0,0,0.3);z-index:9998;
      display:flex;align-items:center;gap:12px;
      transition:all 0.3s ease;
    `;
    document.body.appendChild(bar);
  }

  const names = list.map(id => {
    const p = placesData.find(x => x.id === id);
    return p ? p.name_ar : id;
  });

  bar.innerHTML = `
    <span>⚖️ ${names.join(' vs ')}</span>
    ${list.length === 2 ? `<a href="compare.html?p1=${list[0]}&p2=${list[1]}" style="background:#c9a84c;color:#0a1628;padding:6px 16px;border-radius:8px;font-weight:800;text-decoration:none;">قارن الآن</a>` : `<span style="color:rgba(255,255,255,0.5);">اختر مكان ثاني</span>`}
    <button onclick="clearCompare()" style="background:none;border:none;color:rgba(255,255,255,0.5);cursor:pointer;font-size:18px;padding:0 4px;">✕</button>
  `;
}

function clearCompare() {
  localStorage.removeItem('wain_compare');
  updateCompareButtons();
  updateCompareBar();
}

function goToCompare() {
  const list = getCompareList();
  if (list.length === 2) {
    window.location.href = `compare.html?p1=${list[0]}&p2=${list[1]}`;
  }
}

// Render trending sidebar widget
function renderTrendingSidebar(container) {
  const trending = getTrendingPlaces();
  let html = '<ul class="trending-list">';
  trending.forEach((place, index) => {
    html += `
      <li>
        <span class="rank">${index + 1}</span>
        <div style="flex:1;min-width:0;">
          <a href="place.html?id=${place.id}" style="font-weight:600;">${place.name_ar}</a>
          <div style="font-size:12px;color:var(--text-muted);">⭐ ${place.google_rating} · ${formatNumber(place.review_count)} تقييم</div>
        </div>
      </li>
    `;
  });
  html += '</ul>';
  container.innerHTML = html;
}

// Mobile menu toggle
function initMobileMenu() {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
  }
}

// Search input
function initSearch(onSearch) {
  const input = document.querySelector('.search-input');
  if (input) {
    let timeout;
    input.addEventListener('input', (e) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => { if (onSearch) onSearch(e.target.value); }, 300);
    });
  }
}

function getUrlParam(param) {
  return new URLSearchParams(window.location.search).get(param);
}

// Schema.org structured data
function generateSchemaMarkup(place) {
  return {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": place.name_en,
    "alternateName": place.name_ar,
    "description": place.description_ar,
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Riyadh",
      "addressRegion": place.neighborhood_en || place.neighborhood,
      "addressCountry": "SA"
    },
    "geo": place.lat && place.lng ? {
      "@type": "GeoCoordinates",
      "latitude": place.lat,
      "longitude": place.lng
    } : undefined,
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": place.google_rating,
      "reviewCount": place.review_count,
      "bestRating": "5",
      "worstRating": "1"
    },
    "priceRange": place.price_level,
    "url": place.google_maps_url
  };
}

function addSchemaToPage(schemaData) {
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.textContent = JSON.stringify(schemaData);
  document.head.appendChild(script);
}

// Rating analysis section for place detail
function generateRatingAnalysis(place) {
  return `
    <div class="rating-analysis">
      <h2>📊 تحليل التقييمات</h2>

      <div class="rating-overview">
        <div class="rating-big-display">
          <div class="big-score">${place.google_rating}</div>
          <div class="big-stars">${generateStars(place.google_rating)}</div>
          <div class="total-reviews">${formatNumber(place.review_count)} تقييم</div>
          <div class="google-label">⭐ من تقييمات قوقل</div>
        </div>
        <div class="rating-details">
          <div class="rating-detail-item">
            <span class="detail-icon">🕐</span>
            <div class="detail-content">
              <div class="detail-label">أفضل وقت للزيارة</div>
              <div class="detail-value">${place.best_time || 'غير محدد'}</div>
            </div>
          </div>
          <div class="rating-detail-item">
            <span class="detail-icon">💰</span>
            <div class="detail-content">
              <div class="detail-label">متوسط الإنفاق</div>
              <div class="detail-value">${place.avg_spend || place.price_level || 'غير محدد'}</div>
            </div>
          </div>
          <div class="rating-detail-item">
            <span class="detail-icon">📊</span>
            <div class="detail-content">
              <div class="detail-label">مستوى الأسعار</div>
              <div class="detail-value">${place.price_level} ${place.price_level === '$' ? '(اقتصادي)' : place.price_level === '$$' ? '(متوسط)' : place.price_level === '$$$' ? '(مرتفع)' : '(فاخر)'}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="pros-cons">
        <div class="pros-section">
          <h3>👍 الناس تمدح:</h3>
          <ul>
            ${(place.pros_ar || place.pros || []).map(p => `<li>${p}</li>`).join('')}
          </ul>
        </div>
        <div class="cons-section">
          <h3>👎 الناس تنتقد:</h3>
          <ul>
            ${(place.cons_ar || place.cons || []).map(c => `<li>${c}</li>`).join('')}
          </ul>
        </div>
      </div>

      <div class="visit-info">
        <div class="visit-info-card">
          <div class="info-label">🕐 أفضل وقت للزيارة</div>
          <div class="info-value">${place.best_time || 'غير محدد'}</div>
        </div>
        <div class="visit-info-card">
          <div class="info-label">💰 متوسط الإنفاق</div>
          <div class="info-value">${place.avg_spend || place.price_level || 'غير محدد'}</div>
        </div>
        <div class="visit-info-card">
          <div class="info-label">💬 عدد التقييمات</div>
          <div class="info-value">${formatNumber(place.review_count)} تقييم على قوقل</div>
        </div>
      </div>
    </div>
  `;
}

// ===== PWA Install Prompt =====
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallBanner();
});

function showInstallBanner() {
  if (document.getElementById('pwa-install-banner')) return;
  const banner = document.createElement('div');
  banner.id = 'pwa-install-banner';
  banner.innerHTML = `
    <div style="position:fixed;bottom:0;left:0;right:0;background:var(--primary);color:white;padding:14px 20px;display:flex;align-items:center;justify-content:center;gap:12px;z-index:9999;font-family:'Tajawal',sans-serif;box-shadow:0 -4px 20px rgba(0,0,0,0.3);">
      <span style="font-size:14px;">📱 أضف "وين نروح" للشاشة الرئيسية واستخدمه بدون إنترنت</span>
      <button onclick="installPWA()" style="background:var(--gold);color:var(--primary);border:none;padding:8px 20px;border-radius:8px;font-family:'Tajawal',sans-serif;font-weight:700;font-size:14px;cursor:pointer;">أضف الآن</button>
      <button onclick="this.parentElement.parentElement.remove()" style="background:none;border:none;color:rgba(255,255,255,0.5);font-size:20px;cursor:pointer;padding:4px 8px;">✕</button>
    </div>
  `;
  document.body.appendChild(banner);
}

function installPWA() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((result) => {
      deferredPrompt = null;
      const banner = document.getElementById('pwa-install-banner');
      if (banner) banner.remove();
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  
  // Initialize compare bar if items selected
  updateCompareBar();

  // Scroll to top button
  const scrollTopBtn = document.getElementById('scrollTop');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    }, { passive: true });

    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Register Service Worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js').catch(() => {});
  }
});
