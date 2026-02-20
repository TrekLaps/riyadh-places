// ===== Weather & Prayer Times — Smart Suggestions v2 =====
// وين نروح بالرياض؟ — اقتراحات ذكية حسب الطقس وأوقات الصلاة

const WeatherPrayer = (() => {
  let weatherData = null;
  let prayerData = null;
  let placesData = [];

  const WEATHER_API = 'https://wttr.in/Riyadh?format=j1';
  const PRAYER_API = 'https://api.aladhan.com/v1/timingsByCity?city=Riyadh&country=Saudi+Arabia&method=4';

  const prayerNames = {
    Fajr: 'الفجر',
    Sunrise: 'الشروق',
    Dhuhr: 'الظهر',
    Asr: 'العصر',
    Maghrib: 'المغرب',
    Isha: 'العشاء'
  };

  const prayerOrder = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];

  // ===== Fetch Weather =====
  async function fetchWeather() {
    try {
      const res = await fetch(WEATHER_API);
      const data = await res.json();
      weatherData = {
        temp: parseInt(data.current_condition[0].temp_C),
        feelsLike: parseInt(data.current_condition[0].FeelsLikeC),
        humidity: parseInt(data.current_condition[0].humidity),
        desc: data.current_condition[0].lang_ar?.[0]?.value || data.current_condition[0].weatherDesc[0].value,
        windSpeed: parseInt(data.current_condition[0].windspeedKmph),
        weatherCode: parseInt(data.current_condition[0].weatherCode),
        maxTemp: parseInt(data.weather[0].maxtempC),
        minTemp: parseInt(data.weather[0].mintempC),
      };
      return weatherData;
    } catch (e) {
      void 0;
      return null;
    }
  }

  // ===== Fetch Prayer Times =====
  async function fetchPrayerTimes() {
    try {
      const res = await fetch(PRAYER_API);
      const data = await res.json();
      if (data.code === 200) {
        prayerData = data.data.timings;
        return prayerData;
      }
    } catch (e) {
      void 0;
    }
    return null;
  }

  // ===== Time Helpers =====
  function getRiyadhTime() {
    const now = new Date();
    const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    return new Date(utc + (3 * 3600000));
  }

  function prayerToMinutes(timeStr) {
    const [h, m] = timeStr.split(':').map(Number);
    return h * 60 + m;
  }

  function toArabicNumerals(num) {
    const arabicDigits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return String(num).replace(/[0-9]/g, d => arabicDigits[parseInt(d)]);
  }

  // ===== Next Prayer with Countdown =====
  function getNextPrayer() {
    if (!prayerData) return null;
    const now = getRiyadhTime();
    const nowMinutes = now.getHours() * 60 + now.getMinutes();

    for (const name of prayerOrder) {
      const prayerTime = prayerToMinutes(prayerData[name]);
      if (prayerTime > nowMinutes) {
        const diff = prayerTime - nowMinutes;
        return { name, nameAr: prayerNames[name], time: prayerData[name], minutesLeft: diff };
      }
    }
    // After Isha — next is Fajr tomorrow
    const fajrMinutes = prayerToMinutes(prayerData.Fajr);
    const diff = (1440 - nowMinutes) + fajrMinutes;
    return { name: 'Fajr', nameAr: 'الفجر', time: prayerData.Fajr, minutesLeft: diff };
  }

  function getTimePeriod() {
    const now = getRiyadhTime();
    const h = now.getHours();
    if (h >= 5 && h < 10) return 'morning';
    if (h >= 10 && h < 14) return 'noon';
    if (h >= 14 && h < 17) return 'afternoon';
    if (h >= 17 && h < 20) return 'evening';
    return 'night';
  }

  function isAfterMaghrib() {
    if (!prayerData) return false;
    const now = getRiyadhTime();
    const nowMinutes = now.getHours() * 60 + now.getMinutes();
    return nowMinutes >= prayerToMinutes(prayerData.Maghrib);
  }

  // ===== Weather-Smart Suggestion =====
  function getWeatherSuggestion() {
    if (!weatherData) return null;

    const temp = weatherData.temp;
    const code = weatherData.weatherCode;
    const isRaining = code >= 200 && code < 400;

    if (isRaining) {
      return {
        icon: '🌧️',
        text: 'يوم ممطر نادر! استمتع بكافيه دافي',
        filter: 'indoor',
        class: 'wp-rain'
      };
    }
    if (temp > 40) {
      return {
        icon: '🌡️',
        text: 'حار اليوم! أماكن مكيفة تناسبك',
        filter: 'indoor',
        class: 'wp-hot'
      };
    }
    if (temp >= 25 && temp <= 40) {
      return {
        icon: '☀️',
        text: 'جو حلو! جرب أماكن خارجية',
        filter: 'outdoor',
        class: 'wp-nice'
      };
    }
    if (temp < 25) {
      return {
        icon: '🌤️',
        text: 'جو رايق! وقت مثالي للمشي والطبيعة',
        filter: 'outdoor',
        class: 'wp-cool'
      };
    }
    return null;
  }

  // ===== Get Smart Suggestions (all) =====
  function getSmartSuggestion() {
    const suggestions = [];
    const period = getTimePeriod();
    const nextPrayer = getNextPrayer();

    // Weather-based
    const ws = getWeatherSuggestion();
    if (ws) {
      suggestions.push({ ...ws, priority: 3 });
    }

    // Time-based
    if (isAfterMaghrib()) {
      suggestions.push({
        icon: '🌙',
        text: 'وقت السهرة! أماكن مسائية تناسبك',
        filter: 'evening',
        priority: 2
      });
    }

    // Prayer-based
    if (nextPrayer && nextPrayer.minutesLeft <= 60 && nextPrayer.minutesLeft > 0) {
      const hrs = Math.floor(nextPrayer.minutesLeft / 60);
      const mins = nextPrayer.minutesLeft % 60;
      const timeStr = hrs > 0 ? `${hrs} ساعة و ${mins} دقيقة` : `${mins} دقيقة`;
      suggestions.push({
        icon: '⏰',
        text: `باقي ${timeStr} على ${nextPrayer.nameAr} (${nextPrayer.time})`,
        filter: null,
        priority: 1
      });
    }

    suggestions.sort((a, b) => b.priority - a.priority);
    return suggestions;
  }

  // ===== Filter Places by Context =====
  function filterByContext(places, filterType) {
    if (!filterType) return places.slice(0, 6);

    switch (filterType) {
      case 'indoor':
        return places.filter(p =>
          p.category === 'كافيه' || p.category === 'مطعم' ||
          p.category === 'تسوق' || p.category === 'حلويات' ||
          p.category === 'ترفيه'
        ).slice(0, 6);

      case 'outdoor':
        return places.filter(p =>
          p.category === 'طبيعة' || p.category === 'فعاليات' ||
          (p.description_ar && (p.description_ar.includes('مفتوح') || p.description_ar.includes('حديقة') || p.description_ar.includes('طبيعة')))
        ).slice(0, 6);

      case 'evening':
        return places.filter(p =>
          p.category === 'مطعم' || p.category === 'ترفيه' ||
          p.category === 'حلويات' ||
          (p.best_time && p.best_time.includes('مساء'))
        ).slice(0, 6);

      default:
        return places.slice(0, 6);
    }
  }

  // ===== Prayer Countdown Formatter =====
  function formatCountdown(minutesLeft) {
    const hrs = Math.floor(minutesLeft / 60);
    const mins = minutesLeft % 60;
    if (hrs > 0) {
      return `${toArabicNumerals(hrs)} ساعة و ${toArabicNumerals(mins)} دقيقة`;
    }
    return `${toArabicNumerals(mins)} دقيقة`;
  }

  // ===== Render Weather Suggestion Banner =====
  function renderWeatherSuggestionBanner(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const ws = getWeatherSuggestion();
    if (!ws && !weatherData) {
      container.style.display = 'none';
      return;
    }

    const filtered = ws ? filterByContext(placesData, ws.filter) : [];

    let placesHtml = '';
    if (filtered.length > 0) {
      placesHtml = `
        <div class="wp-suggested-places">
          ${filtered.map(p => `
            <a href="place.html?id=${p.id}" class="wp-suggested-card">
              <span class="wp-suggested-icon">${p.category === 'كافيه' ? '☕' : p.category === 'مطعم' ? '🍽️' : p.category === 'طبيعة' ? '🏞️' : p.category === 'ترفيه' ? '🎭' : p.category === 'تسوق' ? '🛍️' : p.category === 'حلويات' ? '🍰' : '📍'}</span>
              <span class="wp-suggested-name">${p.name_ar}</span>
              <span class="wp-suggested-rating">⭐ ${p.google_rating}</span>
            </a>
          `).join('')}
        </div>
      `;
    }

    container.innerHTML = `
      <div class="wp-weather-suggestion ${ws ? ws.class : ''}">
        <div class="wp-suggestion-text">
          <span class="wp-suggestion-icon-big">${ws ? ws.icon : '🌡️'}</span>
          <div>
            <strong>${ws ? ws.text : `درجة الحرارة ${weatherData.temp}°`}</strong>
            <span class="wp-suggestion-temp">${weatherData.temp}° | ${weatherData.desc}</span>
          </div>
        </div>
        ${placesHtml}
      </div>
    `;
    container.style.display = 'block';
  }

  // ===== Render Main Banner (Weather + Prayer Combined) =====
  function renderBanner(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const suggestions = getSmartSuggestion();
    if (suggestions.length === 0 && !weatherData && !prayerData) {
      container.style.display = 'none';
      return;
    }

    // Weather info strip
    let weatherStrip = '';
    if (weatherData) {
      weatherStrip = `
        <div class="wp-weather-strip">
          <span class="wp-temp">${weatherData.temp}°</span>
          <span class="wp-desc">${weatherData.desc}</span>
          <span class="wp-range">↑${weatherData.maxTemp}° ↓${weatherData.minTemp}°</span>
        </div>
      `;
    }

    // Prayer times strip with next prayer highlight
    let prayerStrip = '';
    if (prayerData) {
      const nextPrayer = getNextPrayer();
      prayerStrip = '<div class="wp-prayer-strip">';
      const now = getRiyadhTime();
      const nowMinutes = now.getHours() * 60 + now.getMinutes();

      for (const name of prayerOrder) {
        const pm = prayerToMinutes(prayerData[name]);
        const isPast = pm < nowMinutes;
        const isNext = !isPast && nextPrayer?.name === name;
        prayerStrip += `
          <span class="wp-prayer-item ${isPast ? 'past' : ''} ${isNext ? 'next' : ''}">
            <span class="wp-prayer-name">${prayerNames[name]}</span>
            <span class="wp-prayer-time">${prayerData[name]}</span>
            ${isNext ? `<span class="wp-prayer-countdown">بعد ${formatCountdown(nextPrayer.minutesLeft)}</span>` : ''}
          </span>
        `;
      }
      prayerStrip += '</div>';
    }

    // Prayer break warning
    let prayerWarning = '';
    const nextPrayer = getNextPrayer();
    if (nextPrayer && nextPrayer.minutesLeft <= 30 && nextPrayer.minutesLeft > 0) {
      prayerWarning = `
        <div class="wp-prayer-warning">
          ⚠️ المحلات تقفل وقت الصلاة — الصلاة الجاية: ${nextPrayer.nameAr} بعد ${formatCountdown(nextPrayer.minutesLeft)}
        </div>
      `;
    }

    // Suggestion badges
    let badgesHtml = suggestions.map(s => `
      <span class="wp-suggestion-badge" ${s.filter ? `data-filter="${s.filter}"` : ''}>
        ${s.icon} ${s.text}
      </span>
    `).join('');

    container.innerHTML = `
      <div class="wp-banner">
        <div class="wp-banner-top">
          ${weatherStrip}
          ${prayerStrip}
        </div>
        ${prayerWarning}
        <div class="wp-suggestions">
          ${badgesHtml}
        </div>
      </div>
    `;
    container.style.display = 'block';

    // Click listeners for filter badges
    container.querySelectorAll('.wp-suggestion-badge[data-filter]').forEach(badge => {
      badge.style.cursor = 'pointer';
      badge.addEventListener('click', () => {
        const filterType = badge.dataset.filter;
        const placesContainer = document.getElementById('places-container');
        if (placesContainer && placesData.length) {
          const filtered = filterByContext(placesData, filterType);
          if (typeof renderCardsWithAds === 'function') {
            renderCardsWithAds(filtered, placesContainer);
          }
          badge.classList.add('wp-badge-active');
          setTimeout(() => badge.classList.remove('wp-badge-active'), 2000);
        }
      });
    });
  }

  // ===== Start Countdown Timer (auto-update every minute) =====
  function startCountdown() {
    setInterval(() => {
      // Update prayer countdown in banner
      const nextPrayer = getNextPrayer();
      if (nextPrayer) {
        // Update countdown elements
        document.querySelectorAll('.wp-prayer-countdown').forEach(el => {
          el.textContent = `بعد ${formatCountdown(nextPrayer.minutesLeft)}`;
        });

        // Update/show/hide prayer warning
        const warningEl = document.querySelector('.wp-prayer-warning');
        if (nextPrayer.minutesLeft <= 30 && nextPrayer.minutesLeft > 0) {
          if (warningEl) {
            warningEl.innerHTML = `⚠️ المحلات تقفل وقت الصلاة — الصلاة الجاية: ${nextPrayer.nameAr} بعد ${formatCountdown(nextPrayer.minutesLeft)}`;
            warningEl.style.display = '';
          }
        } else if (warningEl) {
          warningEl.style.display = 'none';
        }

        // Update "open after prayer" badges
        document.querySelectorAll('.wp-after-prayer-badge').forEach(el => {
          if (nextPrayer.minutesLeft <= 30) {
            el.style.display = 'inline-flex';
          } else {
            el.style.display = 'none';
          }
        });
      }
    }, 60000); // Every minute
  }

  // ===== Generate "Open After Prayer" Badge HTML =====
  function getAfterPrayerBadge() {
    const next = getNextPrayer();
    if (!next || next.minutesLeft > 30) return '';
    return `<span class="wp-after-prayer-badge" style="display:inline-flex;">🕌 مفتوح بعد الصلاة</span>`;
  }

  // ===== Initialize =====
  async function init(places) {
    placesData = places || [];
    const [w, p] = await Promise.all([fetchWeather(), fetchPrayerTimes()]);

    // Render main banner (sidebar/combined)
    renderBanner('weather-prayer-banner');

    // Render weather suggestion banner (below hero on index)
    renderWeatherSuggestionBanner('weather-suggestion-banner');

    // Start countdown timer
    startCountdown();

    // Auto-refresh every 5 minutes
    setInterval(() => {
      fetchWeather().then(() => fetchPrayerTimes()).then(() => {
        renderBanner('weather-prayer-banner');
        renderWeatherSuggestionBanner('weather-suggestion-banner');
      });
    }, 300000);
  }

  return {
    init,
    fetchWeather,
    fetchPrayerTimes,
    getSmartSuggestion,
    getWeatherSuggestion,
    filterByContext,
    getNextPrayer,
    getRiyadhTime,
    getAfterPrayerBadge,
    formatCountdown,
    toArabicNumerals
  };
})();
