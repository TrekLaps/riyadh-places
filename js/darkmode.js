// ===== Dark Mode Toggle — وين نروح بالرياض؟ =====
// Respects system preference, saves to localStorage, smooth transitions

(function() {
  const STORAGE_KEY = 'wain_theme';

  // Determine initial theme
  function getInitialTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'dark' || saved === 'light') return saved;
    // Respect system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  // Apply theme without transition (for initial load)
  function applyTheme(theme, animate) {
    if (animate) {
      document.documentElement.style.transition = 'background 0.4s ease, color 0.4s ease';
      document.body.style.transition = 'background 0.4s ease, color 0.4s ease';
    }
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);

    // Update all toggle buttons
    document.querySelectorAll('.dark-mode-toggle').forEach(btn => {
      btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
      btn.setAttribute('aria-label', theme === 'dark' ? 'وضع النهار' : 'الوضع الليلي');
      btn.title = theme === 'dark' ? 'وضع النهار' : 'الوضع الليلي';
    });

    // Update theme-color meta
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if (metaTheme) {
      metaTheme.setAttribute('content', theme === 'dark' ? '#0a1628' : '#0a1628');
    }
  }

  // Toggle theme
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next, true);
  }

  // Apply immediately (before DOM renders) to prevent flash
  applyTheme(getInitialTheme(), false);

  // Listen for system preference changes
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      // Only auto-switch if user hasn't manually set preference
      const saved = localStorage.getItem(STORAGE_KEY);
      if (!saved) {
        applyTheme(e.matches ? 'dark' : 'light', true);
      }
    });
  }

  // Attach click handlers once DOM is ready
  function attachToggleHandlers() {
    document.querySelectorAll('.dark-mode-toggle').forEach(btn => {
      btn.addEventListener('click', toggleTheme);
    });
    // Re-sync button state
    const theme = document.documentElement.getAttribute('data-theme') || 'light';
    document.querySelectorAll('.dark-mode-toggle').forEach(btn => {
      btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachToggleHandlers);
  } else {
    attachToggleHandlers();
  }

  // Expose globally
  window.WainDarkMode = { toggle: toggleTheme, apply: applyTheme };
})();
