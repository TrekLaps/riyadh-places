// ===== وين نروح بالرياض — Reviews Component v1 =====

let reviewsData = [];

/**
 * Load reviews data from JSON
 */
async function loadReviews() {
  try {
    const response = await fetch('data/reviews.json');
    reviewsData = await response.json();
    return reviewsData;
  } catch (error) {
    void 0;
    return [];
  }
}

/**
 * Get reviews for a specific place
 */
function getPlaceReviews(placeId) {
  const entry = reviewsData.find(r => r.place_id === placeId);
  return entry ? entry.reviews : [];
}

/**
 * Get place review stats
 */
function getPlaceReviewStats(placeId) {
  const entry = reviewsData.find(r => r.place_id === placeId);
  if (!entry || !entry.reviews.length) return null;
  
  const reviews = entry.reviews;
  const total = reviews.length;
  const avgRating = reviews.reduce((sum, r) => sum + r.rating, 0) / total;
  
  // Star distribution
  const dist = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
  reviews.forEach(r => { dist[r.rating] = (dist[r.rating] || 0) + 1; });
  
  const distribution = {};
  for (let i = 5; i >= 1; i--) {
    distribution[i] = {
      count: dist[i],
      percent: Math.round((dist[i] / total) * 100)
    };
  }
  
  return {
    avgRating: Math.round(avgRating * 10) / 10,
    totalReviews: total,
    googleRating: entry.google_rating,
    googleReviewCount: entry.review_count,
    distribution
  };
}

/**
 * Generate star rating with filled/empty stars
 */
function generateReviewStars(rating) {
  let stars = '';
  for (let i = 1; i <= 5; i++) {
    if (i <= rating) {
      stars += '<span class="review-star filled">★</span>';
    } else {
      stars += '<span class="review-star empty">☆</span>';
    }
  }
  return stars;
}

/**
 * Format date to Arabic
 */
function formatReviewDate(dateStr) {
  const months = {
    '01': 'يناير', '02': 'فبراير', '03': 'مارس', '04': 'أبريل',
    '05': 'مايو', '06': 'يونيو', '07': 'يوليو', '08': 'أغسطس',
    '09': 'سبتمبر', '10': 'أكتوبر', '11': 'نوفمبر', '12': 'ديسمبر'
  };
  const parts = dateStr.split('-');
  if (parts.length >= 2) {
    return `${months[parts[1]] || parts[1]} ${parts[0]}`;
  }
  return dateStr;
}

/**
 * Get source label
 */
function getSourceLabel(source) {
  const labels = {
    'google': '⭐ Google',
    'tripadvisor': '🦉 TripAdvisor',
    'timeout': '⏰ TimeOut',
    'other': '📝 زائر'
  };
  return labels[source] || labels.other;
}

/**
 * Generate a single review card HTML
 */
function generateReviewCard(review, index) {
  const initials = review.author.charAt(0);
  const colorIndex = index % 6;
  const colors = ['#c9a84c', '#0891b2', '#7c3aed', '#059669', '#dc2626', '#ea580c'];
  const bgColor = colors[colorIndex];
  
  return `
    <div class="review-card" style="animation-delay: ${index * 0.1}s">
      <div class="review-card-header">
        <div class="review-avatar" style="background: ${bgColor}">${initials}</div>
        <div class="review-author-info">
          <span class="review-author-name">${review.author}</span>
          <span class="review-date">${formatReviewDate(review.date)}</span>
        </div>
        <div class="review-source-badge">${getSourceLabel(review.source)}</div>
      </div>
      <div class="review-rating">
        ${generateReviewStars(review.rating)}
      </div>
      <p class="review-text">${review.text_ar}</p>
    </div>
  `;
}

/**
 * Generate star distribution bar chart
 */
function generateDistributionChart(stats) {
  if (!stats) return '';
  
  let barsHtml = '';
  for (let i = 5; i >= 1; i--) {
    const d = stats.distribution[i];
    barsHtml += `
      <div class="dist-row">
        <span class="dist-label">${i}★</span>
        <div class="dist-bar-bg">
          <div class="dist-bar-fill" style="width: ${d.percent}%"></div>
        </div>
        <span class="dist-percent">${d.percent}%</span>
      </div>
    `;
  }
  
  return `
    <div class="rating-distribution">
      <div class="dist-summary">
        <div class="dist-big-score">${stats.googleRating}</div>
        <div class="dist-stars">${generateReviewStars(Math.round(stats.googleRating))}</div>
        <div class="dist-total">${stats.googleReviewCount ? stats.googleReviewCount.toLocaleString('ar-SA') : stats.totalReviews} تقييم</div>
      </div>
      <div class="dist-chart">
        ${barsHtml}
      </div>
    </div>
  `;
}

/**
 * Generate the full reviews section HTML
 */
function generateReviewsSection(placeId) {
  const reviews = getPlaceReviews(placeId);
  const stats = getPlaceReviewStats(placeId);
  
  if (!reviews.length) return '';
  
  const reviewCardsHtml = reviews.map((r, i) => generateReviewCard(r, i)).join('');
  
  return `
    <div class="reviews-section">
      <div class="section-title">
        <div>
          <h2>💬 آراء الزوار</h2>
          <span class="subtitle">تقييمات حقيقية من زوار المكان</span>
        </div>
      </div>
      
      ${stats ? generateDistributionChart(stats) : ''}
      
      <div class="reviews-slider-container">
        <button class="reviews-nav-btn reviews-nav-prev" aria-label="السابق" onclick="slideReviews(-1)">‹</button>
        <div class="reviews-slider" id="reviews-slider">
          ${reviewCardsHtml}
        </div>
        <button class="reviews-nav-btn reviews-nav-next" aria-label="التالي" onclick="slideReviews(1)">›</button>
      </div>
      
      <div class="reviews-dots" id="reviews-dots"></div>
    </div>
  `;
}

/**
 * Initialize reviews slider with touch support
 */
function initReviewsSlider() {
  const slider = document.getElementById('reviews-slider');
  if (!slider) return;
  
  const cards = slider.querySelectorAll('.review-card');
  if (cards.length === 0) return;
  
  // Create dots
  const dotsContainer = document.getElementById('reviews-dots');
  if (dotsContainer) {
    let dotsHtml = '';
    cards.forEach((_, i) => {
      dotsHtml += `<button class="review-dot ${i === 0 ? 'active' : ''}" data-index="${i}" onclick="goToReview(${i})"></button>`;
    });
    dotsContainer.innerHTML = dotsHtml;
  }
  
  // Touch/swipe support
  let startX = 0;
  let startY = 0;
  let isDragging = false;
  let startScrollLeft = 0;
  
  slider.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
    startScrollLeft = slider.scrollLeft;
    isDragging = true;
  }, { passive: true });
  
  slider.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    const diffX = startX - e.touches[0].clientX;
    const diffY = Math.abs(startY - e.touches[0].clientY);
    
    // Only horizontal swipe
    if (diffY > Math.abs(diffX)) {
      isDragging = false;
      return;
    }
    
    slider.scrollLeft = startScrollLeft + diffX;
  }, { passive: true });
  
  slider.addEventListener('touchend', () => {
    isDragging = false;
    snapToNearestCard();
  });
  
  // Mouse drag support for desktop
  slider.addEventListener('mousedown', (e) => {
    startX = e.clientX;
    startScrollLeft = slider.scrollLeft;
    isDragging = true;
    slider.style.cursor = 'grabbing';
    slider.style.userSelect = 'none';
  });
  
  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const diff = startX - e.clientX;
    slider.scrollLeft = startScrollLeft + diff;
  });
  
  document.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      slider.style.cursor = 'grab';
      slider.style.userSelect = '';
      snapToNearestCard();
    }
  });
  
  // Scroll event for updating dots
  slider.addEventListener('scroll', () => {
    updateActiveDot();
  }, { passive: true });
  
  function snapToNearestCard() {
    const cardWidth = cards[0].offsetWidth + 16; // card width + gap
    const index = Math.round(slider.scrollLeft / cardWidth);
    slider.scrollTo({ left: index * cardWidth, behavior: 'smooth' });
  }
  
  function updateActiveDot() {
    const cardWidth = cards[0].offsetWidth + 16;
    const currentIndex = Math.round(slider.scrollLeft / cardWidth);
    const dots = document.querySelectorAll('.review-dot');
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentIndex);
    });
  }
}

/**
 * Slide reviews in a direction
 */
function slideReviews(direction) {
  const slider = document.getElementById('reviews-slider');
  if (!slider) return;
  
  const cards = slider.querySelectorAll('.review-card');
  if (cards.length === 0) return;
  
  const cardWidth = cards[0].offsetWidth + 16;
  const currentIndex = Math.round(slider.scrollLeft / cardWidth);
  let newIndex = currentIndex + direction;
  
  // Wrap around
  if (newIndex < 0) newIndex = cards.length - 1;
  if (newIndex >= cards.length) newIndex = 0;
  
  slider.scrollTo({ left: newIndex * cardWidth, behavior: 'smooth' });
}

/**
 * Go to specific review
 */
function goToReview(index) {
  const slider = document.getElementById('reviews-slider');
  if (!slider) return;
  
  const cards = slider.querySelectorAll('.review-card');
  if (cards.length === 0 || index >= cards.length) return;
  
  const cardWidth = cards[0].offsetWidth + 16;
  slider.scrollTo({ left: index * cardWidth, behavior: 'smooth' });
}
