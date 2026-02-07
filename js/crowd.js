// ===== Popular Times / Crowd Component =====
// CSS-only bar charts, real-time busyness indicators

const CROWD_DAYS_AR = {
  saturday: 'السبت',
  sunday: 'الأحد',
  monday: 'الاثنين',
  tuesday: 'الثلاثاء',
  wednesday: 'الأربعاء',
  thursday: 'الخميس',
  friday: 'الجمعة'
};

const CROWD_DAYS_ORDER = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'];

/**
 * Get current day name (in our key format)
 */
function getCurrentDay() {
  const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
  // Riyadh is UTC+3
  const now = new Date();
  const riyadhTime = new Date(now.getTime() + (3 * 60 * 60 * 1000));
  return days[riyadhTime.getUTCDay()];
}

/**
 * Get current hour in Riyadh time (0-23)
 */
function getCurrentHour() {
  const now = new Date();
  const riyadhTime = new Date(now.getTime() + (3 * 60 * 60 * 1000));
  return riyadhTime.getUTCHours();
}

/**
 * Get busyness level from a 0-100 value
 */
function getBusynessLevel(value) {
  if (value <= 0) return { level: 'closed', label: 'مغلق', icon: '⚫', color: '#666' };
  if (value <= 20) return { level: 'quiet', label: 'هادي', icon: '🟢', color: '#2ecc71' };
  if (value <= 45) return { level: 'moderate', label: 'معتدل', icon: '🟡', color: '#f39c12' };
  if (value <= 70) return { level: 'busy', label: 'مزدحم', icon: '🔴', color: '#e74c3c' };
  return { level: 'very_busy', label: 'مزدحم جداً', icon: '🔴', color: '#c0392b' };
}

/**
 * Get current busyness for a place
 */
function getCurrentBusyness(place) {
  if (!place.popular_times) return null;
  const day = getCurrentDay();
  const hour = getCurrentHour();
  const dayData = place.popular_times[day];
  if (!dayData) return null;
  const value = dayData[hour] || 0;
  return { ...getBusynessLevel(value), value };
}

/**
 * Render a mini busyness indicator (for cards)
 */
function renderBusynessBadge(place) {
  const info = getCurrentBusyness(place);
  if (!info) return '';
  return `<span class="busyness-badge busyness-${info.level}" title="الازدحام الحين">
    ${info.icon} ${info.label}
  </span>`;
}

/**
 * Render busyness indicator row (for place detail / trending)
 */
function renderBusynessIndicator(place) {
  const info = getCurrentBusyness(place);
  if (!info) return '';
  
  const hour = getCurrentHour();
  const ampm = hour >= 12 ? 'م' : 'ص';
  const displayHour = hour > 12 ? hour - 12 : (hour === 0 ? 12 : hour);
  
  return `
    <div class="busyness-indicator">
      <div class="busyness-now">
        <span class="busyness-icon-big">${info.icon}</span>
        <div class="busyness-text">
          <strong>الحين ${info.label}</strong>
          <span class="busyness-time">الساعة ${displayHour} ${ampm} · مستوى الازدحام ${info.value}%</span>
        </div>
      </div>
      ${place.best_visit_time ? `<div class="busyness-tip">💡 أفضل وقت للزيارة: <strong>${place.best_visit_time}</strong></div>` : ''}
    </div>
  `;
}

/**
 * Render full popular times chart for a day
 */
function renderDayChart(dayData, highlightHour = -1) {
  if (!dayData || !Array.isArray(dayData)) return '';
  
  // Only show hours 6-24 (6 AM to midnight) - skip sleeping hours
  const startHour = 6;
  const endHour = 24;
  
  let barsHtml = '';
  for (let h = startHour; h < endHour; h++) {
    const value = dayData[h] || 0;
    const info = getBusynessLevel(value);
    const isNow = h === highlightHour;
    const hourLabel = h > 12 ? `${h - 12}م` : (h === 12 ? '12م' : `${h}ص`);
    
    barsHtml += `
      <div class="pt-bar-wrapper ${isNow ? 'pt-bar-now' : ''}" title="${hourLabel}: ${info.label} (${value}%)">
        <div class="pt-bar" style="height: ${Math.max(value, 2)}%; background: ${info.color};${isNow ? ' box-shadow: 0 0 8px ' + info.color + ';' : ''}"></div>
        ${isNow ? '<div class="pt-now-marker">▲</div>' : ''}
        <span class="pt-hour-label">${h % 3 === 0 ? hourLabel : ''}</span>
      </div>
    `;
  }
  
  return `<div class="pt-chart">${barsHtml}</div>`;
}

/**
 * Render full popular times section with day tabs
 */
function renderPopularTimes(place) {
  if (!place.popular_times) return '';
  
  const currentDay = getCurrentDay();
  const currentHour = getCurrentHour();
  
  // Day tabs
  let tabsHtml = '';
  CROWD_DAYS_ORDER.forEach(day => {
    const isActive = day === currentDay;
    const shortName = CROWD_DAYS_AR[day];
    tabsHtml += `<button class="pt-day-tab ${isActive ? 'active' : ''}" data-day="${day}">${shortName}</button>`;
  });
  
  // Charts for each day (only current day visible initially)
  let chartsHtml = '';
  CROWD_DAYS_ORDER.forEach(day => {
    const isActive = day === currentDay;
    const highlight = isActive ? currentHour : -1;
    chartsHtml += `
      <div class="pt-day-chart ${isActive ? 'active' : ''}" data-day="${day}">
        ${renderDayChart(place.popular_times[day], highlight)}
      </div>
    `;
  });
  
  return `
    <div class="popular-times-section" id="popular-times">
      <h3>📊 أوقات الازدحام</h3>
      ${renderBusynessIndicator(place)}
      <div class="pt-days-tabs">${tabsHtml}</div>
      <div class="pt-charts-container">${chartsHtml}</div>
      ${place.peak_hours ? `<div class="pt-peak-info">🔥 أوقات الذروة: <strong>${place.peak_hours}</strong></div>` : ''}
    </div>
  `;
}

/**
 * Initialize day tab switching
 */
function initPopularTimesTabs() {
  document.querySelectorAll('.pt-day-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const day = tab.dataset.day;
      const section = tab.closest('.popular-times-section');
      
      // Switch active tab
      section.querySelectorAll('.pt-day-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Switch active chart
      section.querySelectorAll('.pt-day-chart').forEach(c => c.classList.remove('active'));
      section.querySelector(`.pt-day-chart[data-day="${day}"]`).classList.add('active');
    });
  });
}

/**
 * Get trending places right now (sorted by current busyness)
 */
function getTrendingNow(places, limit = 20) {
  const day = getCurrentDay();
  const hour = getCurrentHour();
  
  return places
    .filter(p => p.popular_times && p.popular_times[day])
    .map(p => {
      const value = p.popular_times[day][hour] || 0;
      return { ...p, currentBusyness: value, busynessInfo: getBusynessLevel(value) };
    })
    .filter(p => p.currentBusyness > 0)
    .sort((a, b) => b.currentBusyness - a.currentBusyness)
    .slice(0, limit);
}

/**
 * Render a compact busyness mini-chart (for trending cards)
 */
function renderMiniChart(place) {
  if (!place.popular_times) return '';
  
  const day = getCurrentDay();
  const dayData = place.popular_times[day];
  const currentHour = getCurrentHour();
  
  if (!dayData) return '';
  
  // Show just 6AM-midnight, compact
  let barsHtml = '';
  for (let h = 6; h < 24; h++) {
    const value = dayData[h] || 0;
    const info = getBusynessLevel(value);
    const isNow = h === currentHour;
    barsHtml += `<div class="mini-bar ${isNow ? 'mini-bar-now' : ''}" style="height: ${Math.max(value, 3)}%; background: ${info.color};"></div>`;
  }
  
  return `<div class="mini-chart">${barsHtml}</div>`;
}

// ===== Inject crowd CSS =====
function injectCrowdStyles() {
  if (document.getElementById('crowd-styles')) return;
  const style = document.createElement('style');
  style.id = 'crowd-styles';
  style.textContent = `
    /* ===== Busyness Badge (on cards) ===== */
    .busyness-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 6px;
    }
    .busyness-quiet { background: rgba(46,204,113,0.1); color: #27ae60; }
    .busyness-moderate { background: rgba(243,156,18,0.1); color: #e67e22; }
    .busyness-busy { background: rgba(231,76,60,0.1); color: #e74c3c; }
    .busyness-very_busy { background: rgba(192,57,43,0.15); color: #c0392b; }
    .busyness-closed { background: rgba(100,100,100,0.1); color: #666; }

    /* ===== Busyness Indicator (detail) ===== */
    .busyness-indicator {
      margin: 16px 0;
      padding: 16px;
      background: linear-gradient(135deg, rgba(201,168,76,0.06), rgba(201,168,76,0.02));
      border-radius: var(--radius, 16px);
      border: 1px solid rgba(201,168,76,0.15);
    }
    .busyness-now {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }
    .busyness-icon-big {
      font-size: 32px;
      line-height: 1;
    }
    .busyness-text {
      display: flex;
      flex-direction: column;
    }
    .busyness-text strong {
      font-size: 16px;
      color: var(--primary, #0a1628);
    }
    .busyness-time {
      font-size: 13px;
      color: var(--text-muted, #888);
    }
    .busyness-tip {
      font-size: 13px;
      color: var(--text-light, #555);
      padding: 8px 12px;
      background: rgba(46,204,113,0.06);
      border-radius: 8px;
      border-right: 3px solid #2ecc71;
    }

    /* ===== Popular Times Section ===== */
    .popular-times-section {
      margin: 24px 0;
      padding: 24px;
      background: var(--card-bg, #fff);
      border-radius: var(--radius, 16px);
      box-shadow: var(--shadow, 0 4px 20px rgba(10,22,40,0.08));
      border-top: 3px solid var(--gold, #c9a84c);
    }
    .popular-times-section h3 {
      font-size: 20px;
      font-weight: 800;
      color: var(--primary, #0a1628);
      margin-bottom: 16px;
    }

    /* Day Tabs */
    .pt-days-tabs {
      display: flex;
      gap: 4px;
      margin-bottom: 16px;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .pt-days-tabs::-webkit-scrollbar { display: none; }
    .pt-day-tab {
      padding: 8px 14px;
      border: 2px solid var(--border, #e8e0d4);
      border-radius: 8px;
      background: var(--card-bg, #fff);
      cursor: pointer;
      font-family: 'Tajawal', sans-serif;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.2s ease;
      white-space: nowrap;
      color: var(--text, #1a1a1a);
      min-height: 40px;
    }
    .pt-day-tab:hover {
      border-color: var(--gold, #c9a84c);
    }
    .pt-day-tab.active {
      background: var(--gold, #c9a84c);
      border-color: var(--gold, #c9a84c);
      color: var(--primary, #0a1628);
      font-weight: 700;
    }

    /* Chart Container */
    .pt-charts-container { position: relative; }
    .pt-day-chart { display: none; }
    .pt-day-chart.active { display: block; }

    /* Bar Chart */
    .pt-chart {
      display: flex;
      align-items: flex-end;
      gap: 2px;
      height: 120px;
      padding: 0 4px;
    }
    .pt-bar-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 100%;
      position: relative;
      justify-content: flex-end;
    }
    .pt-bar {
      width: 100%;
      border-radius: 3px 3px 0 0;
      transition: height 0.3s ease;
      min-height: 2px;
    }
    .pt-bar-wrapper:hover .pt-bar {
      opacity: 0.8;
      filter: brightness(1.1);
    }
    .pt-bar-now .pt-bar {
      border: 2px solid var(--primary, #0a1628);
      border-bottom: none;
    }
    .pt-now-marker {
      font-size: 10px;
      color: var(--primary, #0a1628);
      line-height: 1;
      margin-top: 1px;
    }
    .pt-hour-label {
      font-size: 10px;
      color: var(--text-muted, #888);
      margin-top: 4px;
      white-space: nowrap;
    }

    /* Peak Info */
    .pt-peak-info {
      margin-top: 14px;
      font-size: 13px;
      color: var(--text-light, #555);
      padding: 8px 12px;
      background: rgba(231,76,60,0.05);
      border-radius: 8px;
      border-right: 3px solid #e74c3c;
    }

    /* ===== Mini Chart (for trending cards) ===== */
    .mini-chart {
      display: flex;
      align-items: flex-end;
      gap: 1px;
      height: 40px;
      margin: 8px 0;
    }
    .mini-bar {
      flex: 1;
      border-radius: 2px 2px 0 0;
      min-height: 1px;
      transition: height 0.2s;
    }
    .mini-bar-now {
      border: 1.5px solid var(--primary, #0a1628);
      border-bottom: none;
    }

    /* ===== Trending Now Cards ===== */
    .trending-now-card {
      background: var(--card-bg, #fff);
      border-radius: var(--radius, 16px);
      overflow: hidden;
      box-shadow: var(--shadow, 0 4px 20px rgba(10,22,40,0.08));
      transition: all 0.3s ease;
      border-top: 3px solid var(--gold, #c9a84c);
      animation: fadeInUp 0.5s ease forwards;
      opacity: 0;
    }
    .trending-now-card:nth-child(1) { animation-delay: 0.05s; }
    .trending-now-card:nth-child(2) { animation-delay: 0.1s; }
    .trending-now-card:nth-child(3) { animation-delay: 0.15s; }
    .trending-now-card:nth-child(4) { animation-delay: 0.2s; }
    .trending-now-card:nth-child(5) { animation-delay: 0.25s; }
    .trending-now-card:nth-child(6) { animation-delay: 0.3s; }
    .trending-now-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 40px rgba(10,22,40,0.15);
    }
    .trending-card-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 16px 0;
    }
    .trending-rank {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, var(--gold, #c9a84c), #b08d3a);
      color: var(--primary, #0a1628);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 900;
      flex-shrink: 0;
    }
    .trending-rank.rank-1 { background: linear-gradient(135deg, #FFD700, #FFA500); font-size: 18px; }
    .trending-rank.rank-2 { background: linear-gradient(135deg, #C0C0C0, #A0A0A0); }
    .trending-rank.rank-3 { background: linear-gradient(135deg, #CD7F32, #A0522D); color: #fff; }
    .trending-card-info {
      flex: 1;
      min-width: 0;
    }
    .trending-card-info h3 {
      font-size: 16px;
      font-weight: 700;
      color: var(--primary, #0a1628);
      margin: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .trending-card-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: var(--text-muted, #888);
      margin-top: 2px;
    }
    .trending-card-body {
      padding: 8px 16px 16px;
    }
    .trending-busyness-bar {
      height: 8px;
      background: var(--border, #e8e0d4);
      border-radius: 4px;
      overflow: hidden;
      margin: 8px 0;
    }
    .trending-busyness-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.5s ease;
    }
    .trending-card-actions {
      display: flex;
      gap: 8px;
      margin-top: 10px;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .popular-times-section { padding: 16px; }
      .pt-chart { height: 90px; gap: 1px; }
      .pt-hour-label { font-size: 8px; }
      .pt-day-tab { padding: 6px 10px; font-size: 12px; }
      .busyness-icon-big { font-size: 26px; }
      .busyness-text strong { font-size: 14px; }
      .mini-chart { height: 30px; }
    }
  `;
  document.head.appendChild(style);
}

// Auto-inject styles when script loads
injectCrowdStyles();
