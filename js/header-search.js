// ===== Header Search — وين نروح بالرياض =====
(function() {
  'use strict';

  var searchIndex = null;
  var isOpen = false;
  var highlightIdx = -1;
  var suggestions = [];

  var toggle = document.getElementById('header-search-toggle');
  var box = document.getElementById('header-search-box');
  var input = document.getElementById('header-search-input');
  var dropdown = document.getElementById('header-search-dropdown');

  if (!toggle || !box || !input || !dropdown) return;

  // Build index lazily
  function ensureIndex() {
    if (searchIndex) return Promise.resolve();
    if (typeof WaynSearch === 'undefined') return Promise.resolve();
    return (typeof loadPlaces === 'function' ? loadPlaces() : fetch('data/places-light.json').then(function(r){return r.json();}))
      .then(function(places) {
        searchIndex = WaynSearch.buildSearchIndex(places);
      });
  }

  function openSearch() {
    isOpen = true;
    box.classList.add('open');
    input.focus();
    ensureIndex();
    showRecent();
  }

  function closeSearch() {
    isOpen = false;
    box.classList.remove('open');
    dropdown.classList.remove('visible');
    highlightIdx = -1;
  }

  toggle.addEventListener('click', function(e) {
    e.stopPropagation();
    isOpen ? closeSearch() : openSearch();
  });

  document.addEventListener('click', function(e) {
    if (isOpen && !box.contains(e.target) && e.target !== toggle) closeSearch();
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && isOpen) closeSearch();
    if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))) {
      e.preventDefault();
      openSearch();
    }
  });

  // Show recent searches when input is empty
  function showRecent() {
    if (input.value.trim()) return;
    if (typeof WaynSearch === 'undefined') return;
    var recent = WaynSearch.getRecent();
    if (!recent.length) return;

    var html = '<div class="search-dropdown-header">🕐 بحث سابق</div>';
    html += recent.map(function(q) {
      return '<a class="search-suggestion" href="search.html?q=' + encodeURIComponent(q) + '">' +
        '<span class="search-suggestion-icon">🕐</span>' +
        '<div class="search-suggestion-text"><div class="search-suggestion-name">' + q + '</div></div></a>';
    }).join('');
    html += '<div class="search-suggestion-footer" onclick="WaynSearch.clearRecent();this.parentElement.classList.remove(\'visible\')">مسح السجل</div>';
    dropdown.innerHTML = html;
    dropdown.classList.add('visible');
  }

  var debounceTimer;
  input.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(handleInput, 200);
  });

  input.addEventListener('focus', function() {
    if (!input.value.trim()) showRecent();
  });

  function handleInput() {
    var query = input.value.trim();
    if (!query || query.length < 2 || !searchIndex) {
      if (!query) showRecent();
      else dropdown.classList.remove('visible');
      suggestions = [];
      return;
    }

    suggestions = WaynSearch.autoSuggest(searchIndex, query, 5);
    highlightIdx = -1;

    if (suggestions.length === 0) {
      dropdown.innerHTML = '<div style="padding:16px;text-align:center;color:var(--text-muted,#888);font-size:13px;">لا نتائج — جرب كلمات أخرى</div>' +
        '<div class="search-suggestion-footer" onclick="window.location.href=\'search.html?q=' + encodeURIComponent(query) + '\'">🔍 بحث متقدم عن "' + query + '"</div>';
      dropdown.classList.add('visible');
      return;
    }

    var html = suggestions.map(function(s, i) {
      var href = s.type === 'place' ? 'place.html?id=' + s.id :
                 s.type === 'neighborhood' ? 'search.html?hood=' + encodeURIComponent(s.text) :
                 'search.html?cat=' + encodeURIComponent(s.text);
      var ratingHtml = s.rating ? ' <span style="color:#c9a84c;font-size:12px;">⭐ ' + s.rating + '</span>' : '';
      return '<a class="search-suggestion" href="' + href + '" data-index="' + i + '">' +
        '<span class="search-suggestion-icon">' + s.icon + '</span>' +
        '<div class="search-suggestion-text">' +
          '<div class="search-suggestion-name">' + s.text + ratingHtml + '</div>' +
          '<div class="search-suggestion-sub">' + s.sub + '</div>' +
        '</div>' +
        '<span class="search-suggestion-type">' + (s.type==='place'?'مكان':s.type==='neighborhood'?'حي':'قسم') + '</span></a>';
    }).join('');

    html += '<div class="search-suggestion-footer" onclick="window.location.href=\'search.html?q=' + encodeURIComponent(query) + '\'">🔍 عرض كل النتائج لـ "' + query + '"</div>';
    dropdown.innerHTML = html;
    dropdown.classList.add('visible');
  }

  // Keyboard navigation
  input.addEventListener('keydown', function(e) {
    if (!dropdown.classList.contains('visible')) {
      if (e.key === 'Enter') {
        e.preventDefault();
        WaynSearch.saveRecent(input.value.trim());
        window.location.href = 'search.html?q=' + encodeURIComponent(input.value);
      }
      return;
    }
    var items = dropdown.querySelectorAll('.search-suggestion');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      highlightIdx = Math.min(highlightIdx + 1, items.length - 1);
      updateHL(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      highlightIdx = Math.max(highlightIdx - 1, -1);
      updateHL(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      WaynSearch.saveRecent(input.value.trim());
      if (highlightIdx >= 0 && items[highlightIdx]) items[highlightIdx].click();
      else window.location.href = 'search.html?q=' + encodeURIComponent(input.value);
    }
  });

  function updateHL(items) {
    for (var i = 0; i < items.length; i++) {
      items[i].classList.toggle('highlighted', i === highlightIdx);
    }
    if (highlightIdx >= 0 && items[highlightIdx]) items[highlightIdx].scrollIntoView({block:'nearest'});
  }
})();
