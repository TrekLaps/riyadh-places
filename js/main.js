// ===== وين نروح الرياض - Main JavaScript =====

const categoryIcons = { cafe: '☕', restaurant: '🍽️', activity: '🎭' };
const categoryNames = { cafe: 'كافيه', restaurant: 'مطعم', activity: 'ترفيه' };

let placesData = [];

async function loadPlaces() {
  try {
    const response = await fetch('data/places.json');
    placesData = await response.json();
    return placesData;
  } catch (error) {
    console.error('Error loading places:', error);
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

// Generate place card HTML — enhanced with ratings
function generatePlaceCard(place) {
  return `
    <article class="place-card" data-category="${place.category}" data-id="${place.id}" data-neighborhood="${place.neighborhood}" data-price="${place.price_level}">
      <div class="place-card-image">
        ${categoryIcons[place.category] || '📍'}
        ${place.trending ? '<span class="trending-badge">🔥 رائج</span>' : ''}
        ${place.is_new ? '<span class="new-badge">جديد</span>' : ''}
      </div>
      <div class="place-card-body">
        <span class="category-badge">${place.category_ar}</span>
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

        <div class="review-quote-line">${place.review_quote}</div>

        <span class="price-range">${place.price_level}</span>
        <div class="card-actions">
          <a href="place.html?id=${place.id}" class="btn-primary">اعرف أكثر</a>
          <a href="${place.google_maps_url}" target="_blank" class="btn-outline">📍 الموقع</a>
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
    return true;
  });
}

// Get unique neighborhoods from a list
function getNeighborhoods(places) {
  return [...new Set(places.map(p => p.neighborhood))].sort();
}

// Generate sort/filter bar HTML
function generateSortFilterBar(totalCount, neighborhoods, opts = {}) {
  const showCategory = opts.showCategory !== false;
  const showNeighborhood = opts.showNeighborhood !== false;
  const showPrice = opts.showPrice !== false;

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
          <option value="cafe">☕ كافيه</option>
          <option value="restaurant">🍽️ مطعم</option>
          <option value="activity">🎭 ترفيه</option>
        </select>` : ''}
      </div>
    </div>
  `;
}

// Initialize sort/filter controls
function initSortFilter(sourcePlaces, container, resultsCountEl, opts = {}) {
  const applyAll = () => {
    const sortBy = document.getElementById('sort-select')?.value || 'rating-desc';
    const filters = {
      category: document.getElementById('filter-category')?.value || 'all',
      neighborhood: document.getElementById('filter-neighborhood')?.value || 'all',
      priceLevel: document.getElementById('filter-price')?.value || 'all',
    };
    let result = filterPlaces(sourcePlaces, filters);
    result = sortPlaces(result, sortBy);
    renderCardsWithAds(result, container);
    if (resultsCountEl) {
      resultsCountEl.innerHTML = `عرض <strong>${formatNumber(result.length)}</strong> مكان`;
    }
  };

  ['sort-select', 'filter-category', 'filter-neighborhood', 'filter-price'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', applyAll);
  });
}

// Search places
function searchPlaces(query) {
  const q = query.toLowerCase().trim();
  if (!q) return placesData;
  return placesData.filter(p =>
    p.name_ar.includes(q) || p.name_en.toLowerCase().includes(q) ||
    p.description_ar.includes(q) || p.neighborhood.includes(q) ||
    p.category_ar.includes(q) || (p.review_quote && p.review_quote.includes(q))
  );
}

function getTrendingPlaces() { return placesData.filter(p => p.trending).slice(0, 5); }
function getNewPlaces() { return placesData.filter(p => p.is_new); }
function getPlaceById(id) { return placesData.find(p => p.id === id); }

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
              <div class="detail-value">${place.best_time}</div>
            </div>
          </div>
          <div class="rating-detail-item">
            <span class="detail-icon">💰</span>
            <div class="detail-content">
              <div class="detail-label">متوسط الإنفاق</div>
              <div class="detail-value">${place.avg_spend}</div>
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
            ${place.pros.map(p => `<li>${p}</li>`).join('')}
          </ul>
        </div>
        <div class="cons-section">
          <h3>👎 الناس تنتقد:</h3>
          <ul>
            ${place.cons.map(c => `<li>${c}</li>`).join('')}
          </ul>
        </div>
      </div>

      <div class="visit-info">
        <div class="visit-info-card">
          <div class="info-label">🕐 أفضل وقت للزيارة</div>
          <div class="info-value">${place.best_time}</div>
        </div>
        <div class="visit-info-card">
          <div class="info-label">💰 متوسط الإنفاق</div>
          <div class="info-value">${place.avg_spend}</div>
        </div>
        <div class="visit-info-card">
          <div class="info-label">💬 عدد التقييمات</div>
          <div class="info-value">${formatNumber(place.review_count)} تقييم على قوقل</div>
        </div>
      </div>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', () => { initMobileMenu(); });
