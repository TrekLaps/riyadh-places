// ===== Header Search — وين نروح بالرياض =====
(function() {
  'use strict';

  let searchIndex = null;
  let isOpen = false;
  let highlightIndex = -1;
  let suggestions = [];

  const toggle = document.getElementById('header-search-toggle');
  const box = document.getElementById('header-search-box');
  const input = document.getElementById('header-search-input');
  const dropdown = document.getElementById('header-search-dropdown');

  if (!toggle || !box || !input || !dropdown) return;

  // Build index lazily
  async function ensureIndex() {
    if (searchIndex) return;
    if (typeof WaynSearch === 'undefined') return;
    const places = await loadPlaces();
    searchIndex = WaynSearch.buildSearchIndex(places);
  }

  // Toggle search box
  function openSearch() {
    isOpen = true;
    box.classList.add('open');
    input.focus();
    ensureIndex();
  }

  function closeSearch() {
    isOpen = false;
    box.classList.remove('open');
    dropdown.classList.remove('visible');
    highlightIndex = -1;
  }

  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    if (isOpen) closeSearch();
    else openSearch();
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (isOpen && !box.contains(e.target) && e.target !== toggle) {
      closeSearch();
    }
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) closeSearch();
  });

  // Global keyboard shortcut: Ctrl+K or / to open search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName))) {
      e.preventDefault();
      openSearch();
    }
  });

  // Debounce
  let debounceTimer;
  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(handleInput, 200);
  });

  function handleInput() {
    const query = input.value.trim();
    if (!query || query.length < 2 || !searchIndex) {
      dropdown.classList.remove('visible');
      suggestions = [];
      return;
    }

    suggestions = WaynSearch.autoSuggest(searchIndex, query, 5);

    if (suggestions.length === 0) {
      dropdown.innerHTML = `<div style="padding:16px;text-align:center;color:var(--text-muted);font-size:13px;">لا نتائج — جرب كلمات أخرى</div>
        <div class="search-suggestion-footer" onclick="window.location.href='search.html?q=${encodeURIComponent(query)}'">🔍 بحث متقدم عن "${query}"</div>`;
      dropdown.classList.add('visible');
      return;
    }

    highlightIndex = -1;
    let html = suggestions.map((s, i) => {
      const href = s.type === 'place' ? `place.html?id=${s.id}` :
                   s.type === 'neighborhood' ? `search.html?hood=${encodeURIComponent(s.text)}` :
                   `search.html?cat=${encodeURIComponent(s.text)}`;
      const typeLabel = s.type === 'place' ? 'مكان' : s.type === 'neighborhood' ? 'حي' : 'قسم';
      return `<a class="search-suggestion" href="${href}" data-index="${i}">
        <span class="search-suggestion-icon">${s.icon}</span>
        <div class="search-suggestion-text">
          <div class="search-suggestion-name">${s.text}</div>
          <div class="search-suggestion-sub">${s.sub}</div>
        </div>
        <span class="search-suggestion-type">${typeLabel}</span>
      </a>`;
    }).join('');

    html += `<div class="search-suggestion-footer" onclick="window.location.href='search.html?q=${encodeURIComponent(query)}'">🔍 عرض كل النتائج لـ "${query}"</div>`;

    dropdown.innerHTML = html;
    dropdown.classList.add('visible');
  }

  // Keyboard navigation
  input.addEventListener('keydown', (e) => {
    if (!dropdown.classList.contains('visible')) {
      if (e.key === 'Enter') {
        e.preventDefault();
        window.location.href = 'search.html?q=' + encodeURIComponent(input.value);
      }
      return;
    }

    const items = dropdown.querySelectorAll('.search-suggestion');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      highlightIndex = Math.min(highlightIndex + 1, items.length - 1);
      updateHighlight(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      highlightIndex = Math.max(highlightIndex - 1, -1);
      updateHighlight(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (highlightIndex >= 0 && items[highlightIndex]) {
        items[highlightIndex].click();
      } else {
        window.location.href = 'search.html?q=' + encodeURIComponent(input.value);
      }
    }
  });

  function updateHighlight(items) {
    items.forEach((item, i) => {
      item.classList.toggle('highlighted', i === highlightIndex);
    });
    if (highlightIndex >= 0 && items[highlightIndex]) {
      items[highlightIndex].scrollIntoView({ block: 'nearest' });
    }
  }
})();
