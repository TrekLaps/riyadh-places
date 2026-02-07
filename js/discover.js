// ===== Discover Page — "ما تدري وين تروح؟" =====

(function () {
  'use strict';

  let allPlaces = [];
  let currentOccasion = null;
  let currentBudget = null;

  // ===== Utility =====
  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function pickRandom(arr) {
    if (!arr.length) return null;
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function priceToNum(price) {
    if (!price) return 0;
    return price.length; // $=1, $$=2, $$$=3, $$$$=4
  }

  function priceToRiyals(price) {
    const map = { '$': 30, '$$': 80, '$$$': 180, '$$$$': 350 };
    return map[price] || 0;
  }

  // ===== Time Slot Definitions =====
  const TIME_SLOTS = [
    { key: 'morning',   icon: '☀️', label: 'الصباح',    time: '٨-١١ ص',   emoji: '☕' },
    { key: 'noon',      icon: '🌤️', label: 'الظهر',     time: '١٢-٣ م',   emoji: '🍽️' },
    { key: 'afternoon', icon: '☀️', label: 'العصر',     time: '٤-٦ م',    emoji: '🏞️' },
    { key: 'evening',   icon: '🌙', label: 'المساء',    time: '٧-٩ م',    emoji: '🍽️' },
    { key: 'night',     icon: '🌃', label: 'بعد العشاء', time: '٩-١١ م',   emoji: '🍰' },
  ];

  // ===== Filtering helpers =====
  function byCategory(places, cats) {
    return places.filter(p => cats.includes(p.category));
  }

  function byAudience(places, audience) {
    if (!audience) return places;
    return places.filter(p => p.audience && p.audience.includes(audience));
  }

  function byFree(places) {
    return places.filter(p => p.is_free);
  }

  function byPriceMax(places, maxDollars) {
    return places.filter(p => priceToNum(p.price_level) <= maxDollars || p.is_free);
  }

  function byPriceRange(places, minDollars, maxDollars) {
    return places.filter(p => {
      const n = priceToNum(p.price_level);
      return (n >= minDollars && n <= maxDollars) || p.is_free;
    });
  }

  function byMinRating(places, min) {
    return places.filter(p => p.google_rating >= min);
  }

  // Pick a place avoiding already-used neighborhoods
  function pickAvoiding(pool, usedNeighborhoods, usedIds) {
    // First try places from different neighborhoods
    const differentNeighborhood = pool.filter(
      p => !usedNeighborhoods.has(p.neighborhood) && !usedIds.has(p.id)
    );
    if (differentNeighborhood.length) return pickRandom(differentNeighborhood);

    // Fallback: just avoid same place
    const unused = pool.filter(p => !usedIds.has(p.id));
    if (unused.length) return pickRandom(unused);

    return pickRandom(pool);
  }

  // ===== Generate Random Day Plan =====
  function generateRandomPlan() {
    const usedNeighborhoods = new Set();
    const usedIds = new Set();
    const plan = [];

    // Slot rules
    const slotRules = [
      { // Morning: café or breakfast
        categories: ['كافيه'],
        fallbackCategories: ['حلويات'],
        minRating: 4.0,
      },
      { // Noon: restaurant (lunch) or shopping
        categories: ['مطعم', 'تسوق'],
        fallbackCategories: ['ترفيه'],
        minRating: 4.0,
      },
      { // Afternoon: nature or entertainment
        categories: ['طبيعة', 'ترفيه'],
        fallbackCategories: ['تسوق', 'فعاليات'],
        minRating: 3.8,
      },
      { // Evening: restaurant (dinner)
        categories: ['مطعم'],
        fallbackCategories: ['مطعم'],
        minRating: 4.0,
      },
      { // Night: desserts or café
        categories: ['حلويات', 'كافيه'],
        fallbackCategories: ['كافيه'],
        minRating: 4.0,
      },
    ];

    for (let i = 0; i < TIME_SLOTS.length; i++) {
      const rule = slotRules[i];
      let pool = byCategory(allPlaces, rule.categories);
      pool = byMinRating(pool, rule.minRating);
      pool = shuffle(pool);

      let place = pickAvoiding(pool, usedNeighborhoods, usedIds);

      if (!place) {
        pool = byCategory(allPlaces, rule.fallbackCategories);
        pool = shuffle(pool);
        place = pickAvoiding(pool, usedNeighborhoods, usedIds);
      }

      if (!place) {
        // Absolute fallback
        place = pickAvoiding(shuffle(allPlaces), usedNeighborhoods, usedIds);
      }

      if (place) {
        usedNeighborhoods.add(place.neighborhood);
        usedIds.add(place.id);
        plan.push({ slot: TIME_SLOTS[i], place });
      }
    }

    return plan;
  }

  // ===== Occasion Plans =====
  const OCCASION_CONFIGS = {
    romantic: {
      title: '💑 خطة موعد رومانسي',
      slots: [
        { slotIdx: 0, categories: ['كافيه'], audience: 'أزواج', prefer: 'quiet' },
        { slotIdx: 3, categories: ['مطعم'], audience: 'أزواج', minPrice: 3 },
        { slotIdx: 4, categories: ['حلويات', 'كافيه'], audience: 'أزواج' },
      ],
    },
    family: {
      title: '👨‍👩‍👧‍👦 خطة يوم عائلي',
      slots: [
        { slotIdx: 0, categories: ['كافيه'], audience: 'عوائل' },
        { slotIdx: 1, categories: ['مطعم'], audience: 'عوائل' },
        { slotIdx: 2, categories: ['طبيعة', 'ترفيه'], audience: 'أطفال' },
        { slotIdx: 3, categories: ['مطعم'], audience: 'عوائل' },
        { slotIdx: 4, categories: ['حلويات'], audience: 'أطفال' },
      ],
    },
    friends: {
      title: '👥 طلعة مع الربع',
      slots: [
        { slotIdx: 0, categories: ['كافيه'], audience: 'شباب' },
        { slotIdx: 1, categories: ['مطعم'], audience: 'شباب' },
        { slotIdx: 2, categories: ['ترفيه', 'فعاليات'], audience: 'شباب' },
        { slotIdx: 4, categories: ['كافيه', 'حلويات'], audience: 'شباب' },
      ],
    },
    free: {
      title: '🆓 يوم ببلاش',
      slots: [
        { slotIdx: 0, categories: ['طبيعة'], freeOnly: true },
        { slotIdx: 2, categories: ['طبيعة', 'ترفيه'], freeOnly: true },
        { slotIdx: 3, categories: ['طبيعة'], freeOnly: true },
      ],
    },
    night: {
      title: '🌙 خطة سهرة',
      slots: [
        { slotIdx: 3, categories: ['مطعم'] },
        { slotIdx: 4, categories: ['حلويات'] },
        { slotCustom: { key: 'latenight', icon: '🌃', label: 'آخر الليل', time: '١١-١ ص', emoji: '☕' }, categories: ['كافيه'] },
      ],
    },
    cafes: {
      title: '☕ يوم كافيهات',
      slots: [
        { slotIdx: 0, categories: ['كافيه'] },
        { slotCustom: { key: 'mid', icon: '🌤️', label: 'الضحى', time: '١١-١ م', emoji: '☕' }, categories: ['كافيه'] },
        { slotIdx: 2, categories: ['كافيه'] },
        { slotIdx: 4, categories: ['كافيه'] },
      ],
    },
    shopping: {
      title: '🛍️ يوم تسوق',
      slots: [
        { slotIdx: 0, categories: ['كافيه'] },
        { slotIdx: 1, categories: ['تسوق'] },
        { slotIdx: 2, categories: ['تسوق'] },
        { slotIdx: 3, categories: ['مطعم'] },
        { slotIdx: 4, categories: ['حلويات', 'كافيه'] },
      ],
    },
  };

  function generateOccasionPlan(occasionKey) {
    const config = OCCASION_CONFIGS[occasionKey];
    if (!config) return [];

    const usedNeighborhoods = new Set();
    const usedIds = new Set();
    const plan = [];

    for (const rule of config.slots) {
      let pool = byCategory(allPlaces, rule.categories);
      if (rule.audience) pool = byAudience(pool, rule.audience);
      if (rule.freeOnly) pool = byFree(pool);
      if (rule.minPrice) pool = pool.filter(p => priceToNum(p.price_level) >= rule.minPrice);

      pool = shuffle(pool);
      let place = pickAvoiding(pool, usedNeighborhoods, usedIds);

      if (!place) {
        pool = byCategory(allPlaces, rule.categories);
        pool = shuffle(pool);
        place = pickAvoiding(pool, usedNeighborhoods, usedIds);
      }

      if (!place) {
        place = pickAvoiding(shuffle(allPlaces), usedNeighborhoods, usedIds);
      }

      const slot = rule.slotCustom || TIME_SLOTS[rule.slotIdx];
      if (place && slot) {
        usedNeighborhoods.add(place.neighborhood);
        usedIds.add(place.id);
        plan.push({ slot, place });
      }
    }

    return plan;
  }

  // ===== Budget Plans =====
  function generateBudgetPlan(budgetKey) {
    let pool;
    let budgetLabel;
    let maxPerSlot;

    switch (budgetKey) {
      case 'free':
        pool = byFree(allPlaces);
        budgetLabel = '٠ ريال — مجاني بالكامل!';
        break;
      case '50':
        pool = allPlaces.filter(p => priceToNum(p.price_level) <= 1 || p.is_free);
        budgetLabel = 'أقل من ٥٠ ريال';
        maxPerSlot = 1;
        break;
      case '150':
        pool = allPlaces.filter(p => priceToNum(p.price_level) <= 2 || p.is_free);
        budgetLabel = '٥٠ — ١٥٠ ريال';
        maxPerSlot = 2;
        break;
      case '300':
        pool = allPlaces.filter(p => priceToNum(p.price_level) <= 3 || p.is_free);
        budgetLabel = '١٥٠ — ٣٠٠ ريال';
        maxPerSlot = 3;
        break;
      case 'plus':
        pool = [...allPlaces];
        budgetLabel = '٣٠٠+ ريال — بدون حدود';
        maxPerSlot = 4;
        break;
      default:
        pool = [...allPlaces];
        budgetLabel = '';
    }

    const usedNeighborhoods = new Set();
    const usedIds = new Set();
    const plan = [];

    const slotCategories = [
      ['كافيه'],
      ['مطعم', 'تسوق'],
      ['طبيعة', 'ترفيه'],
      ['مطعم'],
      ['حلويات', 'كافيه'],
    ];

    for (let i = 0; i < TIME_SLOTS.length; i++) {
      let slotPool = pool.filter(p => slotCategories[i].includes(p.category));
      if (maxPerSlot) {
        slotPool = slotPool.filter(p => priceToNum(p.price_level) <= maxPerSlot || p.is_free);
      }
      slotPool = shuffle(slotPool);

      let place = pickAvoiding(slotPool, usedNeighborhoods, usedIds);
      if (!place) {
        place = pickAvoiding(shuffle(pool), usedNeighborhoods, usedIds);
      }

      if (place) {
        usedNeighborhoods.add(place.neighborhood);
        usedIds.add(place.id);
        plan.push({ slot: TIME_SLOTS[i], place });
      }
    }

    // Calc estimated spend
    let totalEstimate = 0;
    plan.forEach(item => {
      totalEstimate += item.place.is_free ? 0 : priceToRiyals(item.place.price_level);
    });

    return { plan, budgetLabel, totalEstimate };
  }

  // ===== Render Plan =====
  function renderPlan(plan, container) {
    if (!plan.length) {
      container.innerHTML = `
        <div class="plan-loading">
          <p>😅 ما لقينا أماكن كافية، جرب خيار ثاني!</p>
        </div>
      `;
      return;
    }

    const categoryIconMap = {
      'كافيه': '☕', 'مطعم': '🍽️', 'ترفيه': '🎭',
      'تسوق': '🛍️', 'طبيعة': '🏞️', 'حلويات': '🍰', 'فعاليات': '🎪',
    };

    container.innerHTML = plan.map(({ slot, place }) => {
      const catIcon = categoryIconMap[place.category] || '📍';
      const ratingStars = typeof generateStars === 'function' ? generateStars(place.google_rating) : '';
      const freeTag = place.is_free ? '<span style="color:#27ae60;font-weight:700;font-size:12px;">🆓 مجاني</span>' : '';

      return `
        <div class="plan-slot">
          <div class="slot-time">
            <div class="time-icon">${slot.icon}</div>
            <div class="time-label">${slot.label}<br>${slot.time}</div>
          </div>
          <div class="slot-card">
            <span class="slot-category">${catIcon} ${place.category || ''}</span>
            <h3>${place.name_ar}</h3>
            <div class="slot-meta">
              <span>📍 ${place.neighborhood}</span>
              <span>⭐ ${place.google_rating}</span>
              <span>${place.price_level || ''} ${freeTag}</span>
            </div>
            <div class="slot-desc">${place.description_ar ? place.description_ar.slice(0, 120) + '...' : ''}</div>
            <div class="slot-actions">
              <a href="place.html?id=${place.id}" class="btn-detail">اعرف أكثر</a>
              <a href="${place.google_maps_url}" target="_blank" class="btn-map">📍 الموقع</a>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  function renderPlanSummary(plan, summaryEl) {
    if (!plan.length) { summaryEl.innerHTML = ''; return; }

    const neighborhoodCount = new Set(plan.map(i => i.place.neighborhood)).size;
    const totalEstimate = plan.reduce((sum, i) => sum + (i.place.is_free ? 0 : priceToRiyals(i.place.price_level)), 0);
    const avgRating = (plan.reduce((s, i) => s + i.place.google_rating, 0) / plan.length).toFixed(1);

    summaryEl.innerHTML = `
      <div class="summary-item">
        <span class="summary-icon">📍</span>
        <span><strong>${neighborhoodCount}</strong> أحياء مختلفة</span>
      </div>
      <div class="summary-item">
        <span class="summary-icon">⭐</span>
        <span>متوسط التقييم: <strong>${avgRating}</strong></span>
      </div>
      <div class="summary-item">
        <span class="summary-icon">💰</span>
        <span>تقدير الميزانية: <strong>~${totalEstimate} ريال</strong></span>
      </div>
      <div class="summary-item">
        <span class="summary-icon">🏷️</span>
        <span><strong>${plan.length}</strong> أماكن</span>
      </div>
    `;
  }

  // Share plan as text
  function planToText(plan, title) {
    let text = `🏙️ ${title || 'خطة يومك بالرياض'}\n`;
    text += `من موقع وين نروح بالرياض؟\n\n`;
    plan.forEach(({ slot, place }) => {
      text += `${slot.icon} ${slot.label} (${slot.time}):\n`;
      text += `  ${place.name_ar} — ${place.neighborhood}`;
      text += ` — ${place.price_level || 'مجاني'} — ⭐ ${place.google_rating}\n\n`;
    });
    text += `🔗 wain-nrooh.com/discover.html`;
    return text;
  }

  function sharePlan(plan, title) {
    const text = planToText(plan, title);
    if (navigator.share) {
      navigator.share({ title: title || 'خطة يومك بالرياض', text }).catch(() => {});
    } else {
      // Copy to clipboard
      navigator.clipboard.writeText(text).then(() => {
        if (typeof showToast === 'function') showToast('✅ تم نسخ الخطة');
      }).catch(() => {
        if (typeof showToast === 'function') showToast('✅ تم نسخ الخطة');
      });
    }
  }

  // Show loading animation then render
  function showPlanWithAnimation(container, generateFn, summaryEl, sectionEl) {
    sectionEl.style.display = 'block';

    container.innerHTML = `
      <div class="plan-loading">
        <div class="loading-dice">🎲</div>
        <p>جاري ترتيب خطتك...</p>
      </div>
    `;

    sectionEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

    setTimeout(() => {
      const plan = generateFn();
      renderPlan(plan, container);
      if (summaryEl) renderPlanSummary(plan, summaryEl);
      return plan;
    }, 800);
  }

  // ===== Initialization =====
  let lastRandomPlan = [];
  let lastOccasionPlan = [];
  let lastBudgetPlan = [];

  async function init() {
    allPlaces = await loadPlaces();

    // Update hero stat
    const countEl = document.getElementById('totalPlacesCount');
    if (countEl) countEl.textContent = allPlaces.length;

    // ===== Mega Dice Button =====
    const megaBtn = document.getElementById('megaDiceBtn');
    const randomSection = document.getElementById('randomPlanSection');
    const dayContainer = document.getElementById('dayPlanContainer');
    const planSummary = document.getElementById('planSummary');

    if (megaBtn) {
      megaBtn.addEventListener('click', () => {
        megaBtn.classList.add('rolling');
        setTimeout(() => megaBtn.classList.remove('rolling'), 800);

        randomSection.style.display = 'block';
        dayContainer.innerHTML = `
          <div class="plan-loading">
            <div class="loading-dice">🎲</div>
            <p>جاري ترتيب خطتك...</p>
          </div>
        `;
        randomSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        setTimeout(() => {
          lastRandomPlan = generateRandomPlan();
          renderPlan(lastRandomPlan, dayContainer);
          renderPlanSummary(lastRandomPlan, planSummary);
        }, 800);
      });
    }

    // Refresh random plan
    document.getElementById('refreshPlanBtn')?.addEventListener('click', () => {
      dayContainer.innerHTML = `
        <div class="plan-loading">
          <div class="loading-dice">🎲</div>
          <p>خطة جديدة جاية...</p>
        </div>
      `;
      setTimeout(() => {
        lastRandomPlan = generateRandomPlan();
        renderPlan(lastRandomPlan, dayContainer);
        renderPlanSummary(lastRandomPlan, planSummary);
      }, 600);
    });

    // Share random plan
    document.getElementById('sharePlanBtn')?.addEventListener('click', () => {
      sharePlan(lastRandomPlan, '🗓️ خطة يومي بالرياض');
    });

    // ===== Occasion Cards =====
    const occasionSection = document.getElementById('occasionPlanSection');
    const occasionContainer = document.getElementById('occasionPlanContainer');
    const occasionSummary = document.getElementById('occasionPlanSummary');
    const occasionTitle = document.getElementById('occasionPlanTitle');

    document.querySelectorAll('.occasion-card').forEach(card => {
      card.addEventListener('click', () => {
        const occasion = card.dataset.occasion;
        currentOccasion = occasion;

        // Mark active
        document.querySelectorAll('.occasion-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');

        const config = OCCASION_CONFIGS[occasion];
        if (occasionTitle) occasionTitle.textContent = config.title;

        occasionSection.style.display = 'block';
        occasionContainer.innerHTML = `
          <div class="plan-loading">
            <div class="loading-dice">🎲</div>
            <p>نرتب لك ${config.title}...</p>
          </div>
        `;
        occasionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        setTimeout(() => {
          lastOccasionPlan = generateOccasionPlan(occasion);
          renderPlan(lastOccasionPlan, occasionContainer);
          renderPlanSummary(lastOccasionPlan, occasionSummary);
        }, 800);
      });
    });

    document.getElementById('refreshOccasionBtn')?.addEventListener('click', () => {
      if (!currentOccasion) return;
      occasionContainer.innerHTML = `
        <div class="plan-loading">
          <div class="loading-dice">🎲</div>
          <p>خطة ثانية...</p>
        </div>
      `;
      setTimeout(() => {
        lastOccasionPlan = generateOccasionPlan(currentOccasion);
        renderPlan(lastOccasionPlan, occasionContainer);
        renderPlanSummary(lastOccasionPlan, occasionSummary);
      }, 600);
    });

    document.getElementById('shareOccasionBtn')?.addEventListener('click', () => {
      const config = OCCASION_CONFIGS[currentOccasion];
      sharePlan(lastOccasionPlan, config?.title || 'خطة');
    });

    document.getElementById('backToOccasions')?.addEventListener('click', () => {
      occasionSection.style.display = 'none';
      document.querySelectorAll('.occasion-card').forEach(c => c.classList.remove('active'));
      document.getElementById('occasionsGrid')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    // ===== Budget Cards =====
    const budgetSection = document.getElementById('budgetPlanSection');
    const budgetContainer = document.getElementById('budgetPlanContainer');
    const budgetSummary = document.getElementById('budgetPlanSummary');
    const budgetTitle = document.getElementById('budgetPlanTitle');
    const budgetEstimate = document.getElementById('budgetEstimate');

    document.querySelectorAll('.budget-card').forEach(card => {
      card.addEventListener('click', () => {
        const budget = card.dataset.budget;
        currentBudget = budget;

        document.querySelectorAll('.budget-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');

        budgetSection.style.display = 'block';
        budgetContainer.innerHTML = `
          <div class="plan-loading">
            <div class="loading-dice">🎲</div>
            <p>نبحث لك عن أماكن تناسب ميزانيتك...</p>
          </div>
        `;
        budgetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        setTimeout(() => {
          const result = generateBudgetPlan(budget);
          lastBudgetPlan = result.plan;

          if (budgetTitle) budgetTitle.textContent = `💰 خطتك: ${result.budgetLabel}`;
          if (budgetEstimate) {
            budgetEstimate.innerHTML = `
              <span>💰</span>
              <span>متوسط الصرف المتوقع:</span>
              <span class="budget-amount">~${result.totalEstimate} ريال</span>
            `;
          }

          renderPlan(lastBudgetPlan, budgetContainer);
          renderPlanSummary(lastBudgetPlan, budgetSummary);
        }, 800);
      });
    });

    document.getElementById('refreshBudgetBtn')?.addEventListener('click', () => {
      if (!currentBudget) return;
      budgetContainer.innerHTML = `
        <div class="plan-loading">
          <div class="loading-dice">🎲</div>
          <p>خطة ثانية...</p>
        </div>
      `;
      setTimeout(() => {
        const result = generateBudgetPlan(currentBudget);
        lastBudgetPlan = result.plan;
        if (budgetEstimate) {
          budgetEstimate.innerHTML = `
            <span>💰</span>
            <span>متوسط الصرف المتوقع:</span>
            <span class="budget-amount">~${result.totalEstimate} ريال</span>
          `;
        }
        renderPlan(lastBudgetPlan, budgetContainer);
        renderPlanSummary(lastBudgetPlan, budgetSummary);
      }, 600);
    });

    document.getElementById('shareBudgetBtn')?.addEventListener('click', () => {
      sharePlan(lastBudgetPlan, '💰 خطة يومي حسب الميزانية');
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
