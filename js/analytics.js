// Simple Analytics for وين نروح بالرياض
(function() {
  const STORAGE_KEY = 'waynrooh_stats';
  
  // Track page view
  function trackView() {
    const page = window.location.pathname + window.location.search;
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{"views":0,"pages":{}}');
    data.views++;
    data.pages[page] = (data.pages[page] || 0) + 1;
    data.lastVisit = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    
    // Send to counter (GitHub-friendly - using image pixel)
    const img = new Image();
    img.src = 'https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=' + 
      encodeURIComponent('https://treklaps.github.io/riyadh-places' + page) +
      '&count_bg=%230a1628&title_bg=%23c9a84c&icon=&icon_color=%23E7E7E7&title=views&edge_flat=true';
  }
  
  // Run on load
  if (document.readyState === 'complete') trackView();
  else window.addEventListener('load', trackView);
})();
