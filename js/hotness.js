// ===== Hotness Algorithm — Heat Map Engine =====
// Calculates a "hotness" score for each place based on multiple signals

/**
 * Calculate hotness score for a place
 * hotness = (trending ? 30 : 0) + (is_new ? 20 : 0) + (rating * 10) + (log(reviews) * 5)
 */
function calculateHotness(place) {
  const trending = place.trending ? 30 : 0;
  const isNew = place.is_new ? 20 : 0;
  const rating = (place.google_rating || 0) * 10;
  const reviews = Math.log(Math.max(place.review_count || 1, 1)) * 5;
  return trending + isNew + rating + reviews;
}

/**
 * Get hotness tier from score
 */
function getHotnessTier(score) {
  if (score >= 85) return { tier: 'hot', label: '🔴 حار جداً', color: '#e74c3c', markerColor: 'red', emoji: '🔴' };
  if (score >= 70) return { tier: 'warm', label: '🟡 رائج', color: '#f39c12', markerColor: 'orange', emoji: '🟡' };
  return { tier: 'normal', label: '🟢 عادي', color: '#2ecc71', markerColor: 'green', emoji: '🟢' };
}

/**
 * Get trending reasons for a place
 */
function getTrendingReasons(place) {
  const reasons = [];
  if (place.is_new) reasons.push({ icon: '🆕', text: 'افتتاح جديد' });
  if (place.trending) reasons.push({ icon: '🔥', text: 'رائج الآن' });
  if (place.google_rating >= 4.5) reasons.push({ icon: '⭐', text: `تقييم عالي (${place.google_rating})` });
  if (place.review_count >= 5000) reasons.push({ icon: '💬', text: `${formatNumber(place.review_count)}+ تقييم` });
  if (place.review_count >= 2000 && place.review_count < 5000) reasons.push({ icon: '📈', text: 'شعبية متزايدة' });
  
  // Busyness-based
  const busyness = getCurrentBusyness ? getCurrentBusyness(place) : null;
  if (busyness && busyness.value >= 70) reasons.push({ icon: '🏃', text: 'مزدحم الحين' });
  
  return reasons;
}

/**
 * Get top N hottest places, optionally filtered by category
 */
function getHottestPlaces(places, limit = 20, category = 'all') {
  let filtered = places;
  if (category !== 'all') {
    filtered = places.filter(p => {
      const cat = p.category_en || p.category;
      return cat === category;
    });
  }
  
  return filtered
    .map(p => ({
      ...p,
      hotnessScore: calculateHotness(p),
      hotnessTier: getHotnessTier(calculateHotness(p)),
      trendingReasons: getTrendingReasons(p)
    }))
    .sort((a, b) => b.hotnessScore - a.hotnessScore)
    .slice(0, limit);
}

/**
 * Create a Leaflet heat marker icon based on hotness tier
 */
function createHeatMarkerIcon(place, rank) {
  const score = calculateHotness(place);
  const tier = getHotnessTier(score);
  
  const size = rank && rank <= 3 ? 44 : (rank && rank <= 10 ? 38 : 32);
  const fontSize = rank && rank <= 3 ? 16 : (rank && rank <= 10 ? 13 : 11);
  
  const bgColors = {
    'hot': 'linear-gradient(135deg, #e74c3c, #c0392b)',
    'warm': 'linear-gradient(135deg, #f39c12, #e67e22)',
    'normal': 'linear-gradient(135deg, #2ecc71, #27ae60)'
  };
  
  const label = rank ? rank : tier.emoji;
  const textColor = tier.tier === 'warm' ? '#333' : '#fff';
  
  return L.divIcon({
    html: `<div style="
      background: ${bgColors[tier.tier]};
      color: ${textColor};
      border-radius: 50%;
      width: ${size}px;
      height: ${size}px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: ${fontSize}px;
      font-weight: 900;
      font-family: 'Tajawal', sans-serif;
      box-shadow: 0 3px 12px rgba(0,0,0,0.35);
      border: 3px solid rgba(255,255,255,0.9);
      transition: transform 0.2s;
    " class="heat-marker-inner">${label}</div>`,
    className: 'heat-marker',
    iconSize: [size, size],
    iconAnchor: [size/2, size/2],
    popupAnchor: [0, -size/2],
  });
}

/**
 * Create heat popup content
 */
function createHeatPopup(place, rank) {
  const score = calculateHotness(place);
  const tier = getHotnessTier(score);
  const reasons = getTrendingReasons(place);
  const catIcon = categoryIcons[place.category_en] || categoryIcons[place.category] || '📍';
  const catName = categoryNames[place.category_en] || categoryNames[place.category] || place.category;
  
  const stars = generateStars(place.google_rating);
  
  const reasonsHtml = reasons.map(r => 
    `<span style="display:inline-flex;align-items:center;gap:3px;background:rgba(201,168,76,0.1);padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">${r.icon} ${r.text}</span>`
  ).join(' ');
  
  return `
    <div style="font-family:'Tajawal',sans-serif;direction:rtl;min-width:230px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        ${rank ? `<span style="background:${tier.color};color:#fff;width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:14px;">${rank}</span>` : ''}
        <div>
          <div style="font-size:16px;font-weight:800;color:#0a1628;">${place.name_ar}</div>
          <div style="font-size:12px;color:#888;">${catIcon} ${catName} · 📍 ${place.neighborhood}</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
        <span style="font-weight:800;color:#0a1628;">${place.google_rating}</span>
        <span style="color:#c9a84c;font-size:13px;">${stars}</span>
        <span style="font-size:12px;color:#888;">(${formatNumber(place.review_count)})</span>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;">${reasonsHtml}</div>
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;">
        <span style="background:${tier.color};color:#fff;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:700;">${tier.label}</span>
        <span style="font-size:12px;color:#888;">نقاط الحرارة: ${Math.round(score)}</span>
      </div>
      <div style="display:flex;gap:8px;">
        <a href="place.html?id=${place.id}" style="background:#c9a84c;color:#0a1628;padding:6px 14px;border-radius:8px;font-size:12px;font-weight:700;text-decoration:none;">اعرف أكثر</a>
        <a href="${place.google_maps_url}" target="_blank" style="background:rgba(10,22,40,0.06);color:#0a1628;padding:6px 14px;border-radius:8px;font-size:12px;font-weight:700;text-decoration:none;">📍 خرائط قوقل</a>
      </div>
    </div>
  `;
}
