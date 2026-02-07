// ===== Weather & Prayer Times — Smart Suggestions =====
// وين نروح بالرياض؟ — اقتراحات ذكية حسب الطقس وأوقات الصلاة

const WeatherPrayer = (() => {
  let weatherData = null;
  let prayerData = null;
  let placesData = [];

  const WEATHER_API = 'https://wttr.in/Riyadh?format=j1';
  const PRAYER_API = 'https://api.aladhan.com/v1/timingsByCity?city=Riyadh&country=SA&method=4';

  const prayerNames = {
    Fajr: 'الفجر',
    Sunrise: 'الشروق',
    Dhuhr: 'الظهر',
    Asr: 'العصر',
    Maghrib: 'المغرب',
    Isha: 'العشاء'
  };

  const prayerOrder = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];

  // Fetch weather data
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
      console.warn('Weather API error:', e);
      return null;
    }
  }

  // Fetch prayer times
  async function fetchPrayerTimes() {
    try {
      const res = await fetch(PRAYER_API);
      const data = await res.json();
      if (data.code === 200) {
        prayerData = data.data.timings;
        return prayerData;
      }
    } catch (e) {
      console.warn('Prayer API error:', e);
    }
    return null;
  }

  // Get current time in Riyadh (UTC+3)
  function getRiyadhTime() {
    const now = new Date();
    const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    return new Date(utc + (3 * 3600000));
  }

  // Parse prayer time string "HH:MM" to minutes since midnight
  function prayerToMinutes(timeStr) {
    const [h, m] = timeStr.split(':').map(Number);
    return h * 60 + m;
  }

  // Get next prayer
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

  // Get time period
  function getTimePeriod() {
    const now = getRiyadhTime();
    const h = now.getHours();
    if (h >= 5 && h < 10) return 'morning';
    if (h >= 10 && h < 14) return 'noon';
    if (h >= 14 && h < 17) return 'afternoon';
    if (h >= 17 && h < 20) return 'evening';
    return 'night';
  }

  // Is after Maghrib?
  function isAfterMaghrib() {
    if (!prayerData) return false;
    const now = getRiyadhTime();
    const nowMinutes = now.getHours() * 60 + now.getMinutes();
    return nowMinutes >= prayerToMinutes(prayerData.Maghrib);
  }

  // Generate smart suggestion based on context
  function getSmartSuggestion() {
    const suggestions = [];
    const period = getTimePeriod();
    const nextPrayer = getNextPrayer();

    // Weather-based suggestions
    if (weatherData) {
      if (weatherData.temp > 38) {
        suggestions.push({
          icon: '🌡️',
          text: `حار اليوم ${weatherData.temp}°! جرب أماكن داخلية مكيّفة`,
          filter: 'indoor',
          priority: 3
        });
      } else if (weatherData.temp < 25 && weatherData.temp >= 15) {
        suggestions.push({
          icon: '🌤️',
          text: `الجو حلو ${weatherData.temp}°! روح أماكن مفتوحة`,
          filter: 'outdoor',
          priority: 3
        });
      } else if (weatherData.temp < 15) {
        suggestions.push({
          icon: '🧥',
          text: `الجو بارد ${weatherData.temp}°! كافيه دافي أو مطعم داخلي`,
          filter: 'indoor',
          priority: 2
        });
      }

      if (weatherData.weatherCode >= 200 && weatherData.weatherCode < 400) {
        suggestions.push({
          icon: '🌧️',
          text: 'ممطر اليوم! أماكن داخلية أفضل',
          filter: 'indoor',
          priority: 4
        });
      }
    }

    // Time-based suggestions
    if (isAfterMaghrib()) {
      suggestions.push({
        icon: '🌙',
        text: 'وقت السهرة! أماكن مسائية تناسبك',
        filter: 'evening',
        priority: 2
      });
    }

    // Prayer-based suggestions
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

    // Sort by priority
    suggestions.sort((a, b) => b.priority - a.priority);
    return suggestions;
  }

  // Filter places by suggestion type
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

  // Render the banner
  function renderBanner(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const suggestions = getSmartSuggestion();
    if (suggestions.length === 0) {
      container.style.display = 'none';
      return;
    }

    const mainSuggestion = suggestions[0];

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

    // Prayer times strip
    let prayerStrip = '';
    if (prayerData) {
      prayerStrip = '<div class="wp-prayer-strip">';
      const now = getRiyadhTime();
      const nowMinutes = now.getHours() * 60 + now.getMinutes();

      for (const name of prayerOrder) {
        const pm = prayerToMinutes(prayerData[name]);
        const isPast = pm < nowMinutes;
        const isNext = !isPast && getNextPrayer()?.name === name;
        prayerStrip += `
          <span class="wp-prayer-item ${isPast ? 'past' : ''} ${isNext ? 'next' : ''}">
            <span class="wp-prayer-name">${prayerNames[name]}</span>
            <span class="wp-prayer-time">${prayerData[name]}</span>
          </span>
        `;
      }
      prayerStrip += '</div>';
    }

    // All suggestion badges
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
        <div class="wp-suggestions">
          ${badgesHtml}
        </div>
      </div>
    `;
    container.style.display = 'block';

    // Add click listeners for filter badges
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

  // Initialize
  async function init(places) {
    placesData = places || [];
    const [w, p] = await Promise.all([fetchWeather(), fetchPrayerTimes()]);
    renderBanner('weather-prayer-banner');

    // Auto-refresh every 5 minutes
    setInterval(() => {
      fetchWeather().then(() => fetchPrayerTimes()).then(() => renderBanner('weather-prayer-banner'));
    }, 300000);
  }

  return { init, fetchWeather, fetchPrayerTimes, getSmartSuggestion, filterByContext, getNextPrayer, getRiyadhTime };
})();
