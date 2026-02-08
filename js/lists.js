// ===== User Lists System — قوائمي 📋 =====
// Client-side shareable lists using localStorage

const LISTS_STORAGE_KEY = 'wain_user_lists';

// ===== Pre-made lists =====
const PREMADE_LISTS = [
  {
    id: 'premade-trending',
    name: 'الأكثر رواجاً هذا الأسبوع',
    emoji: '🔥',
    isPremade: true,
    getPlaces: (allPlaces) => allPlaces
      .filter(p => p.trending)
      .sort((a, b) => b.google_rating - a.google_rating)
      .slice(0, 10)
      .map(p => p.id)
  },
  {
    id: 'premade-budget',
    name: 'أفضل الخيارات الاقتصادية',
    emoji: '💰',
    isPremade: true,
    getPlaces: (allPlaces) => allPlaces
      .filter(p => p.price_level === '$' && p.google_rating >= 4.0)
      .sort((a, b) => b.google_rating - a.google_rating)
      .slice(0, 10)
      .map(p => p.id)
  },
  {
    id: 'premade-family',
    name: 'عائلي ١٠٠٪',
    emoji: '👨‍👩‍👧‍👦',
    isPremade: true,
    getPlaces: (allPlaces) => allPlaces
      .filter(p => p.audience && (p.audience.includes('عوائل') || p.audience.includes('أطفال')))
      .sort((a, b) => b.google_rating - a.google_rating)
      .slice(0, 10)
      .map(p => p.id)
  },
  {
    id: 'premade-cafes',
    name: 'كافيهات لازم تجربها',
    emoji: '☕',
    isPremade: true,
    getPlaces: (allPlaces) => allPlaces
      .filter(p => (p.category_en === 'cafe' || p.category === 'كافيه') && p.google_rating >= 4.3)
      .sort((a, b) => b.review_count - a.review_count)
      .slice(0, 10)
      .map(p => p.id)
  },
  {
    id: 'premade-nightlife',
    name: 'سهرة مثالية',
    emoji: '🌙',
    isPremade: true,
    getPlaces: (allPlaces) => {
      // Places that are busy late at night (after 9 PM)
      return allPlaces
        .filter(p => {
          if (!p.popular_times) return false;
          // Check if busy on Thursday night (typical late night)
          const thurs = p.popular_times.thursday;
          if (!thurs) return false;
          const lateActivity = (thurs[21] || 0) + (thurs[22] || 0) + (thurs[23] || 0);
          return lateActivity > 100 && p.google_rating >= 4.0;
        })
        .sort((a, b) => {
          const aLate = ((a.popular_times.thursday || [])[22] || 0);
          const bLate = ((b.popular_times.thursday || [])[22] || 0);
          return bLate - aLate;
        })
        .slice(0, 10)
        .map(p => p.id);
    }
  }
];

// ===== Common Emojis for picking =====
const LIST_EMOJIS = ['📋', '❤️', '🔥', '⭐', '🎉', '🍽️', '☕', '🎭', '🛍️', '🏞️', '🍰', '🌙', '💰', '👨‍👩‍👧‍👦', '🎮', '🏃', '📍', '🏠', '🎁', '🎊', '🇸🇦', '🌟', '💎', '🎯', '🍕', '🍔', '🥗', '🧋', '🎪', '🏟️'];

/**
 * Get all user lists from localStorage
 */
function getUserLists() {
  try {
    return JSON.parse(localStorage.getItem(LISTS_STORAGE_KEY) || '[]');
  } catch { return []; }
}

/**
 * Save user lists to localStorage
 */
function saveUserLists(lists) {
  localStorage.setItem(LISTS_STORAGE_KEY, JSON.stringify(lists));
}

/**
 * Create a new list
 */
function createUserList(name, emoji = '📋') {
  const lists = getUserLists();
  const id = 'list-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);
  const newList = {
    id,
    name,
    emoji,
    places: [],
    created: new Date().toISOString()
  };
  lists.push(newList);
  saveUserLists(lists);
  return newList;
}

/**
 * Delete a user list
 */
function deleteUserList(listId) {
  let lists = getUserLists();
  lists = lists.filter(l => l.id !== listId);
  saveUserLists(lists);
}

/**
 * Rename a user list
 */
function renameUserList(listId, newName, newEmoji) {
  const lists = getUserLists();
  const list = lists.find(l => l.id === listId);
  if (list) {
    if (newName) list.name = newName;
    if (newEmoji) list.emoji = newEmoji;
    saveUserLists(lists);
  }
}

/**
 * Add a place to a list
 */
function addToList(listId, placeId) {
  const lists = getUserLists();
  const list = lists.find(l => l.id === listId);
  if (list && !list.places.includes(placeId)) {
    list.places.push(placeId);
    saveUserLists(lists);
    return true;
  }
  return false;
}

/**
 * Remove a place from a list
 */
function removeFromList(listId, placeId) {
  const lists = getUserLists();
  const list = lists.find(l => l.id === listId);
  if (list) {
    list.places = list.places.filter(id => id !== placeId);
    saveUserLists(lists);
    return true;
  }
  return false;
}

/**
 * Check if a place is in any list
 */
function getListsContainingPlace(placeId) {
  return getUserLists().filter(l => l.places.includes(placeId));
}

/**
 * Generate a shareable URL for a list
 */
function generateListShareUrl(list) {
  const base = window.location.origin + window.location.pathname.replace(/[^/]*$/, '') + 'lists.html';
  const params = new URLSearchParams();
  params.set('name', list.name);
  params.set('emoji', list.emoji);
  params.set('places', list.places.join(','));
  return base + '?' + params.toString();
}

/**
 * Parse shared list from URL
 */
function parseSharedListFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const name = params.get('name');
  const emoji = params.get('emoji') || '📋';
  const placesStr = params.get('places');
  
  if (!name || !placesStr) return null;
  
  return {
    name,
    emoji,
    places: placesStr.split(',').filter(Boolean),
    isShared: true
  };
}

/**
 * Share list via WhatsApp
 */
function shareListWhatsApp(list, allPlaces) {
  const url = generateListShareUrl(list);
  const placeNames = list.places
    .map(id => allPlaces.find(p => p.id === id))
    .filter(Boolean)
    .slice(0, 5)
    .map((p, i) => `${i + 1}. ${p.name_ar} ⭐${p.google_rating}`)
    .join('\n');
  
  const text = `${list.emoji} ${list.name}\n\n${placeNames}${list.places.length > 5 ? `\n... و${list.places.length - 5} أماكن أخرى` : ''}\n\n🔗 شوف القائمة كاملة:\n${url}\n\nمن موقع وين نروح بالرياض؟`;
  window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
}

/**
 * Share list via Twitter/X
 */
function shareListTwitter(list) {
  const url = generateListShareUrl(list);
  const text = `${list.emoji} ${list.name} — ${list.places.length} مكان مميز بالرياض\n\nمن @wain_nrooh`;
  window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
}

/**
 * Copy list share link
 */
function copyListLink(list) {
  const url = generateListShareUrl(list);
  navigator.clipboard.writeText(url).then(() => {
    showToast('✅ تم نسخ رابط القائمة');
  }).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = url;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('✅ تم نسخ رابط القائمة');
  });
}

/**
 * Show "Add to List" modal
 */
function showAddToListModal(placeId) {
  // Remove existing modal
  const existing = document.getElementById('list-modal-overlay');
  if (existing) existing.remove();

  const lists = getUserLists();
  const place = placesData.find(p => p.id === placeId);
  if (!place) return;

  const listsHtml = lists.length > 0 ? lists.map(list => {
    const isInList = list.places.includes(placeId);
    return `
      <button class="list-modal-item ${isInList ? 'in-list' : ''}" onclick="handleAddToListFromModal('${list.id}', '${placeId}')">
        <span class="list-modal-emoji">${list.emoji}</span>
        <span class="list-modal-name">${list.name}</span>
        <span class="list-modal-count">${list.places.length} مكان</span>
        <span class="list-modal-check">${isInList ? '✓' : '+'}</span>
      </button>
    `;
  }).join('') : '<div class="list-modal-empty">ما عندك قوائم بعد</div>';

  const modalHtml = `
    <div id="list-modal-overlay" class="list-modal-overlay" onclick="if(event.target===this)this.remove()">
      <div class="list-modal">
        <div class="list-modal-header">
          <h3>📋 أضف لقائمة</h3>
          <button onclick="document.getElementById('list-modal-overlay').remove()" class="list-modal-close">✕</button>
        </div>
        <div class="list-modal-place">
          <strong>${place.name_ar}</strong>
          <span style="color:var(--text-muted);font-size:13px;">⭐ ${place.google_rating} · ${place.neighborhood}</span>
        </div>
        <div class="list-modal-items" id="list-modal-items">
          ${listsHtml}
        </div>
        <button class="list-modal-create" onclick="handleCreateListFromModal('${placeId}')">
          ➕ إنشاء قائمة جديدة
        </button>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

/**
 * Handle adding to list from modal
 */
function handleAddToListFromModal(listId, placeId) {
  const lists = getUserLists();
  const list = lists.find(l => l.id === listId);
  if (!list) return;

  if (list.places.includes(placeId)) {
    removeFromList(listId, placeId);
    showToast(`🗑️ تم الإزالة من "${list.name}"`);
  } else {
    addToList(listId, placeId);
    showToast(`✅ تم الإضافة لـ "${list.name}"`);
  }
  
  // Refresh modal
  showAddToListModal(placeId);
}

/**
 * Handle creating a new list from modal
 */
function handleCreateListFromModal(placeId) {
  const name = prompt('اسم القائمة:');
  if (!name || !name.trim()) return;
  
  const newList = createUserList(name.trim(), '📋');
  addToList(newList.id, placeId);
  showToast(`✅ تم إنشاء "${name}" وإضافة المكان`);
  
  // Refresh modal
  showAddToListModal(placeId);
}

// ===== Inject List Modal CSS =====
function injectListStyles() {
  if (document.getElementById('list-styles')) return;
  const style = document.createElement('style');
  style.id = 'list-styles';
  style.textContent = `
    .list-modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.5);
      backdrop-filter: blur(4px);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      animation: fadeIn 0.2s ease;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    .list-modal {
      background: var(--card-bg, #fff);
      border-radius: 20px;
      width: 100%;
      max-width: 400px;
      max-height: 80vh;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      display: flex;
      flex-direction: column;
      animation: slideUp 0.3s ease;
    }
    @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    
    .list-modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 18px 20px;
      border-bottom: 1px solid var(--border, #e8e0d4);
    }
    .list-modal-header h3 {
      font-size: 18px;
      font-weight: 800;
      color: var(--primary, #0a1628);
      margin: 0;
    }
    .list-modal-close {
      background: none;
      border: none;
      font-size: 20px;
      color: var(--text-muted, #888);
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 8px;
      transition: background 0.2s;
    }
    .list-modal-close:hover { background: rgba(0,0,0,0.05); }
    
    .list-modal-place {
      padding: 12px 20px;
      background: rgba(201,168,76,0.06);
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    
    .list-modal-items {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      max-height: 300px;
    }
    
    .list-modal-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 14px;
      border: none;
      background: none;
      width: 100%;
      text-align: right;
      cursor: pointer;
      border-radius: 12px;
      transition: background 0.2s;
      font-family: 'Tajawal', sans-serif;
      font-size: 14px;
      color: var(--text, #1a1a1a);
    }
    .list-modal-item:hover { background: rgba(201,168,76,0.08); }
    .list-modal-item.in-list { background: rgba(46,204,113,0.08); }
    .list-modal-item.in-list .list-modal-check { color: #27ae60; font-weight: 800; }
    
    .list-modal-emoji { font-size: 22px; flex-shrink: 0; }
    .list-modal-name { flex: 1; font-weight: 600; }
    .list-modal-count { font-size: 12px; color: var(--text-muted, #888); }
    .list-modal-check { font-size: 18px; font-weight: 700; color: var(--gold, #c9a84c); flex-shrink: 0; }
    
    .list-modal-empty {
      padding: 30px 20px;
      text-align: center;
      color: var(--text-muted, #888);
      font-size: 14px;
    }
    
    .list-modal-create {
      display: block;
      width: calc(100% - 32px);
      margin: 8px 16px 16px;
      padding: 12px;
      background: var(--primary, #0a1628);
      color: var(--gold, #c9a84c);
      border: none;
      border-radius: 12px;
      font-family: 'Tajawal', sans-serif;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    .list-modal-create:hover { opacity: 0.9; transform: translateY(-1px); }

    /* Add to list button on cards */
    .list-add-btn {
      background: none;
      border: 2px solid var(--border, #e8e0d4);
      border-radius: 8px;
      padding: 4px 8px;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
      position: absolute;
      top: 10px;
      left: 46px;
      z-index: 2;
      backdrop-filter: blur(4px);
      background: rgba(255,255,255,0.8);
    }
    .list-add-btn:hover {
      border-color: var(--gold, #c9a84c);
      background: var(--gold, #c9a84c);
    }
  `;
  document.head.appendChild(style);
}

// Auto-inject on load
injectListStyles();
