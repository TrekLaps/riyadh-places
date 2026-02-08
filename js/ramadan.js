// ===== Ramadan Mode — وضع رمضان =====
// Auto-activates based on date. Preview toggle for testing.
// Ramadan 2026: ~Feb 28 - Mar 29 (1 Ramadan - 30 Ramadan 1447)

const RamadanMode = (() => {
  // ===== Configuration =====
  const RAMADAN_START = new Date('2026-02-28T00:00:00+03:00'); // 1 Ramadan 1447
  const RAMADAN_END = new Date('2026-03-30T00:00:00+03:00');   // 1 Shawwal 1447
  const PRE_RAMADAN_DAYS = 7;  // Show banner 7 days before
  const POST_RAMADAN_DAYS = 1; // Keep for 1 day after

  const PRAYER_API = 'https://api.aladhan.com/v1/timingsByCity';
  const RIYADH_PARAMS = 'city=Riyadh&country=SA&method=4'; // Umm al-Qura method

  let prayerTimes = null;
  let countdownInterval = null;
  let isPreview = false;

  // ===== Date Detection =====
  function getRiyadhNow() {
    // Get current time in Riyadh (UTC+3)
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    return new Date(utc + 3 * 3600000);
  }

  function isRamadanActive() {
    if (isPreview) return true;
    const now = getRiyadhNow();
    return now >= RAMADAN_START && now <= RAMADAN_END;
  }

  function isPreRamadan() {
    const now = getRiyadhNow();
    const preStart = new Date(RAMADAN_START);
    preStart.setDate(preStart.getDate() - PRE_RAMADAN_DAYS);
    return now >= preStart && now < RAMADAN_START;
  }

  function isPostRamadan() {
    const now = getRiyadhNow();
    const postEnd = new Date(RAMADAN_END);
    postEnd.setDate(postEnd.getDate() + POST_RAMADAN_DAYS);
    return now > RAMADAN_END && now <= postEnd;
  }

  function shouldShowRamadan() {
    return isPreview || isRamadanActive() || isPreRamadan() || isPostRamadan();
  }

  function getDaysUntilRamadan() {
    const now = getRiyadhNow();
    const diff = RAMADAN_START - now;
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }

  // ===== Prayer Times =====
  async function fetchPrayerTimes() {
    try {
      const cached = sessionStorage.getItem('ramadan_prayer_times');
      const cachedDate = sessionStorage.getItem('ramadan_prayer_date');
      const today = getRiyadhNow().toISOString().split('T')[0];

      if (cached && cachedDate === today) {
        prayerTimes = JSON.parse(cached);
        return prayerTimes;
      }

      const res = await fetch(`${PRAYER_API}?${RIYADH_PARAMS}`);
      const data = await res.json();

      if (data.code === 200) {
        const t = data.data.timings;
        prayerTimes = {
          Fajr: parseTime(t.Fajr),
          Sunrise: parseTime(t.Sunrise),
          Dhuhr: parseTime(t.Dhuhr),
          Asr: parseTime(t.Asr),
          Maghrib: parseTime(t.Maghrib),
          Isha: parseTime(t.Isha),
          raw: t
        };

        sessionStorage.setItem('ramadan_prayer_times', JSON.stringify(prayerTimes));
        sessionStorage.setItem('ramadan_prayer_date', today);
        return prayerTimes;
      }
    } catch (e) {
      console.warn('Ramadan: Prayer API error:', e);
    }
    return null;
  }

  function parseTime(timeStr) {
    // Format: "HH:MM" or "HH:MM (AST)"
    const clean = timeStr.replace(/\s*\(.*\)/, '');
    const [h, m] = clean.split(':').map(Number);
    const now = getRiyadhNow();
    return new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, 0);
  }

  // ===== Time Period Detection =====
  function getCurrentPeriod() {
    if (!prayerTimes) return 'unknown';
    const now = getRiyadhNow();
    const hour = now.getHours();

    // After Fajr but before Maghrib = fasting time → show iftar spots
    if (now >= prayerTimes.Fajr && now < prayerTimes.Maghrib) {
      return 'fasting'; // Show iftar countdown + iftar spots
    }

    // Between Maghrib and Isha = iftar time
    if (now >= prayerTimes.Maghrib && now < prayerTimes.Isha) {
      return 'iftar'; // "رمضان كريم! وقت الإفطار"
    }

    // After Isha until 2 AM = suhoor/night time
    if (now >= prayerTimes.Isha || (hour >= 0 && hour < 2)) {
      return 'night'; // Show suhoor spots + cafes + desserts
    }

    // 2 AM - Fajr = late night/pre-suhoor
    if (hour >= 2 && now < prayerTimes.Fajr) {
      return 'suhoor'; // Show suhoor spots, "السحور قبل الفجر"
    }

    return 'fasting';
  }

  function getPeriodMessage() {
    const period = getCurrentPeriod();
    switch (period) {
      case 'fasting':
        return { icon: '⏰', text: getIftarCountdown(), subtext: 'أماكن إفطار مقترحة', filter: 'iftar' };
      case 'iftar':
        return { icon: '🌙', text: 'رمضان كريم! وقت الإفطار', subtext: 'تقبل الله صيامكم', filter: 'iftar' };
      case 'night':
        return { icon: '🌙', text: 'أماكن السحور المفتوحة الحين', subtext: 'كافيهات وحلويات ومطاعم سحور', filter: 'suhoor' };
      case 'suhoor':
        return { icon: '🍽️', text: 'وقت السحور — لا تنسون السحور!', subtext: 'أماكن سحور قريبة منك', filter: 'suhoor' };
      default:
        return { icon: '🌙', text: 'رمضان كريم', subtext: 'اكتشف أماكن الإفطار والسحور', filter: 'all' };
    }
  }

  function getIftarCountdown() {
    if (!prayerTimes || !prayerTimes.Maghrib) return 'الإفطار بعد قليل';
    const now = getRiyadhNow();
    const diff = prayerTimes.Maghrib - now;

    if (diff <= 0) return 'حان وقت الإفطار! 🌙';

    const hours = Math.floor(diff / 3600000);
    const minutes = Math.floor((diff % 3600000) / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);

    const toArabic = (n) => n.toLocaleString('ar-SA');

    if (hours > 0) {
      return `الإفطار بعد ${toArabic(hours)} ساعة و ${toArabic(minutes)} دقيقة`;
    }
    if (minutes > 0) {
      return `الإفطار بعد ${toArabic(minutes)} دقيقة و ${toArabic(seconds)} ثانية`;
    }
    return `الإفطار بعد ${toArabic(seconds)} ثانية! 🎉`;
  }

  // ===== Banner =====
  function createBanner() {
    // Check if dismissed in this session
    const dismissed = sessionStorage.getItem('ramadan_banner_dismissed');
    if (dismissed === 'true' && !isPreview) return;

    // Remove existing banner if any
    const existing = document.getElementById('ramadan-banner');
    if (existing) existing.remove();

    const banner = document.createElement('div');
    banner.id = 'ramadan-banner';
    banner.className = 'ramadan-banner';

    const isActive = isRamadanActive();
    const isPre = isPreRamadan();
    const daysUntil = getDaysUntilRamadan();

    let bannerContent = '';

    if (isPre && !isPreview) {
      bannerContent = `
        <div class="ramadan-banner-inner">
          <span class="ramadan-banner-crescent">🌙</span>
          <span class="ramadan-banner-text">
            رمضان بعد ${daysUntil.toLocaleString('ar-SA')} أيام! جهّزنا لك دليل رمضان الشامل
          </span>
          <div class="ramadan-banner-links">
            <a href="ramadan.html" class="ramadan-banner-link">🌙 دليل رمضان</a>
            <a href="guide-ramadan.html" class="ramadan-banner-link">📖 الدليل الشامل</a>
          </div>
          <button class="ramadan-banner-dismiss" onclick="RamadanMode.dismissBanner()" title="إغلاق">×</button>
        </div>`;
    } else {
      const period = getPeriodMessage();
      bannerContent = `
        <div class="ramadan-banner-inner">
          <span class="ramadan-banner-crescent">🌙</span>
          <span class="ramadan-banner-text">
            رمضان كريم — اكتشف أماكن الإفطار والسحور
          </span>
          <span class="ramadan-banner-countdown" id="ramadan-banner-countdown">
            ${period.icon} ${period.text}
          </span>
          <div class="ramadan-banner-links">
            <a href="ramadan.html" class="ramadan-banner-link">🌙 أماكن رمضان</a>
            <a href="guide-ramadan.html" class="ramadan-banner-link">📖 الدليل الشامل</a>
          </div>
          <button class="ramadan-banner-dismiss" onclick="RamadanMode.dismissBanner()" title="إغلاق">×</button>
        </div>`;
    }

    banner.innerHTML = bannerContent;

    // Insert before the header
    const header = document.querySelector('.header');
    if (header) {
      header.parentNode.insertBefore(banner, header);
    } else {
      document.body.prepend(banner);
    }
  }

  function dismissBanner() {
    const banner = document.getElementById('ramadan-banner');
    if (banner) {
      banner.style.animation = 'ramadanBannerFadeIn 0.3s ease reverse forwards';
      setTimeout(() => banner.remove(), 300);
    }
    sessionStorage.setItem('ramadan_banner_dismissed', 'true');
  }

  // ===== Countdown Timer Update =====
  function startCountdownUpdate() {
    if (countdownInterval) clearInterval(countdownInterval);
    countdownInterval = setInterval(() => {
      const el = document.getElementById('ramadan-banner-countdown');
      if (el && prayerTimes) {
        const period = getPeriodMessage();
        el.innerHTML = `${period.icon} ${period.text}`;
      }

      // Also update the section countdown if exists
      const sectionTimer = document.getElementById('ramadan-section-timer');
      if (sectionTimer && prayerTimes) {
        const period = getPeriodMessage();
        sectionTimer.innerHTML = `<span class="timer-icon">${period.icon}</span> ${period.text}`;
      }
    }, 1000);
  }

  // ===== Ramadan Section for index.html =====
  function createRamadanSection() {
    const existing = document.getElementById('ramadan-section');
    if (existing) existing.remove();

    const section = document.createElement('section');
    section.id = 'ramadan-section';
    section.className = 'ramadan-section';

    const period = getPeriodMessage();

    section.innerHTML = `
      <div class="ramadan-section-card">
        <div class="ramadan-section-header">
          <h2>🌙 رمضان بالرياض</h2>
          <p>دليلك لأفضل أماكن الإفطار والسحور والتحلية في رمضان ١٤٤٧</p>
        </div>

        <div class="ramadan-countdown">
          <div class="ramadan-countdown-timer" id="ramadan-section-timer">
            <span class="timer-icon">${period.icon}</span>
            ${period.text}
          </div>
          <div class="ramadan-countdown-label">${period.subtext}</div>
        </div>

        <div class="ramadan-quick-links">
          <a href="ramadan.html?filter=iftar" class="ramadan-quick-link">
            <span class="link-icon">🍽️</span>
            <span class="link-label">إفطار</span>
            <span class="link-count">بوفيهات ومطاعم</span>
          </a>
          <a href="ramadan.html?filter=suhoor" class="ramadan-quick-link">
            <span class="link-icon">🌙</span>
            <span class="link-label">سحور</span>
            <span class="link-count">كافيهات ومطاعم</span>
          </a>
          <a href="ramadan.html?filter=tent" class="ramadan-quick-link">
            <span class="link-icon">⛺</span>
            <span class="link-label">خيم رمضانية</span>
            <span class="link-count">خيم فاخرة</span>
          </a>
          <a href="desserts.html" class="ramadan-quick-link">
            <span class="link-icon">🍰</span>
            <span class="link-label">حلويات رمضان</span>
            <span class="link-count">تحلية بعد الإفطار</span>
          </a>
          <a href="guide-ramadan.html" class="ramadan-quick-link">
            <span class="link-icon">📖</span>
            <span class="link-label">الدليل الشامل</span>
            <span class="link-count">نصائح وتجارب</span>
          </a>
          <a href="events.html" class="ramadan-quick-link">
            <span class="link-icon">🎪</span>
            <span class="link-label">فعاليات رمضان</span>
            <span class="link-count">معارض وأمسيات</span>
          </a>
        </div>
      </div>
    `;

    // Insert after the categories section on index.html
    const categories = document.querySelector('.categories');
    if (categories) {
      categories.parentNode.insertBefore(section, categories.nextSibling);
    }
  }

  // ===== Theme Application =====
  function applyRamadanTheme() {
    document.body.classList.add('ramadan-mode');

    // Load Ramadan CSS if not already loaded
    if (!document.getElementById('ramadan-css')) {
      const link = document.createElement('link');
      link.id = 'ramadan-css';
      link.rel = 'stylesheet';
      link.href = 'css/ramadan.css';
      document.head.appendChild(link);
    }
  }

  function removeRamadanTheme() {
    document.body.classList.remove('ramadan-mode');
    const css = document.getElementById('ramadan-css');
    if (css) css.remove();
    const banner = document.getElementById('ramadan-banner');
    if (banner) banner.remove();
    const section = document.getElementById('ramadan-section');
    if (section) section.remove();
    if (countdownInterval) {
      clearInterval(countdownInterval);
      countdownInterval = null;
    }
  }

  // ===== Ramadan Place Badges =====
  function addRamadanBadges() {
    // This is called from the card rendering if ramadan mode is active
    // It adds badges to place cards that have ramadan tags
    document.querySelectorAll('.card[data-place-id]').forEach(card => {
      const placeId = card.dataset.placeId;
      // We need places data — check if global placesData is available
      if (typeof placesData !== 'undefined' && Array.isArray(placesData)) {
        const place = placesData.find(p => p.id === placeId);
        if (place) {
          addBadgesToCard(card, place);
        }
      }
    });
  }

  function addBadgesToCard(card, place) {
    if (!shouldShowRamadan()) return;

    const badgeContainer = card.querySelector('.card-badges') || card.querySelector('.card-meta');
    if (!badgeContainer) return;

    // Check if badges already added
    if (card.querySelector('.ramadan-badge')) return;

    const badges = [];
    if (place.ramadan_iftar) {
      badges.push('<span class="ramadan-badge iftar">🍽️ إفطار</span>');
    }
    if (place.ramadan_suhoor) {
      badges.push('<span class="ramadan-badge suhoor">🌙 سحور</span>');
    }
    if (place.ramadan_tent) {
      badges.push('<span class="ramadan-badge tent">⛺ خيمة</span>');
    }

    if (badges.length > 0) {
      const wrapper = document.createElement('div');
      wrapper.style.cssText = 'display:flex;gap:4px;flex-wrap:wrap;margin-top:6px;';
      wrapper.innerHTML = badges.join('');
      badgeContainer.appendChild(wrapper);
    }
  }

  // ===== Preview Toggle =====
  function createPreviewToggle() {
    // Only show toggle outside of actual Ramadan (or always for dev)
    const existing = document.getElementById('ramadan-preview-toggle');
    if (existing) existing.remove();

    const btn = document.createElement('button');
    btn.id = 'ramadan-preview-toggle';
    btn.className = 'ramadan-preview-toggle' + (isPreview ? ' active' : '');
    btn.innerHTML = `
      <span class="toggle-dot"></span>
      🌙 ${isPreview ? 'إيقاف المعاينة' : 'معاينة رمضان'}
    `;
    btn.onclick = togglePreview;
    document.body.appendChild(btn);
  }

  function togglePreview() {
    isPreview = !isPreview;
    localStorage.setItem('ramadan_preview', isPreview ? 'true' : 'false');

    if (isPreview || shouldShowRamadan()) {
      activate();
    } else {
      removeRamadanTheme();
    }

    // Update toggle button
    const btn = document.getElementById('ramadan-preview-toggle');
    if (btn) {
      btn.className = 'ramadan-preview-toggle' + (isPreview ? ' active' : '');
      btn.innerHTML = `
        <span class="toggle-dot"></span>
        🌙 ${isPreview ? 'إيقاف المعاينة' : 'معاينة رمضان'}
      `;
    }
  }

  // ===== Activation =====
  async function activate() {
    applyRamadanTheme();
    createBanner();

    // Fetch prayer times
    await fetchPrayerTimes();

    // Start countdown updates
    if (isRamadanActive() || isPreview) {
      startCountdownUpdate();
    }

    // Add ramadan section on index page
    if (document.querySelector('.categories')) {
      createRamadanSection();
    }

    // Add badges after a short delay (wait for cards to render)
    setTimeout(addRamadanBadges, 1500);

    // Observe for dynamically added cards
    observeNewCards();
  }

  // ===== MutationObserver for dynamic cards =====
  function observeNewCards() {
    const containers = document.querySelectorAll('#places-container, .places-grid, .cards-grid');
    containers.forEach(container => {
      const observer = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
          mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.classList && node.classList.contains('card')) {
              const placeId = node.dataset?.placeId;
              if (placeId && typeof placesData !== 'undefined') {
                const place = placesData.find(p => p.id === placeId);
                if (place) addBadgesToCard(node, place);
              }
            }
          });
        });
      });
      observer.observe(container, { childList: true, subtree: true });
    });
  }

  // ===== Initialization =====
  function init() {
    // Check for saved preview state
    isPreview = localStorage.getItem('ramadan_preview') === 'true';

    // Create preview toggle (always available)
    createPreviewToggle();

    // Auto-activate if within Ramadan period
    if (shouldShowRamadan()) {
      activate();
    }
  }

  // ===== Ramadan Filter Helpers (for ramadan.html) =====
  function filterPlacesForRamadan(places, filterType) {
    switch (filterType) {
      case 'iftar':
        return places.filter(p => p.ramadan_iftar);
      case 'suhoor':
        return places.filter(p => p.ramadan_suhoor);
      case 'tent':
        return places.filter(p => p.ramadan_tent);
      case 'sweets':
        return places.filter(p => p.category === 'حلويات' || p.ramadan_special?.includes('حلو'));
      case 'all':
      default:
        return places.filter(p => p.ramadan_iftar || p.ramadan_suhoor || p.ramadan_tent || p.ramadan_special);
    }
  }

  function getTimeBasedFilter() {
    const period = getCurrentPeriod();
    switch (period) {
      case 'fasting': return 'iftar';
      case 'iftar': return 'iftar';
      case 'night':
      case 'suhoor': return 'suhoor';
      default: return 'all';
    }
  }

  // ===== Public API =====
  return {
    init,
    isActive: shouldShowRamadan,
    isRamadanActive,
    dismissBanner,
    getPeriodMessage,
    getIftarCountdown,
    filterPlacesForRamadan,
    getTimeBasedFilter,
    getCurrentPeriod,
    addBadgesToCard,
    togglePreview,
    prayerTimes: () => prayerTimes,
  };
})();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', RamadanMode.init);
} else {
  RamadanMode.init();
}
