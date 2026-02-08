// ===== Enhanced Analytics for وين نروح بالرياض v2 =====
(function() {
  'use strict';
  
  const STORAGE_KEY = 'waynrooh_analytics';
  const SESSION_KEY = 'waynrooh_session';
  const VISITOR_KEY = 'waynrooh_visitor_id';
  
  // Generate UUID for unique visitor tracking
  function generateUUID() {
    return 'xxxx-xxxx-xxxx'.replace(/x/g, () => Math.floor(Math.random() * 16).toString(16));
  }
  
  // Get or create visitor ID
  function getVisitorId() {
    let id = localStorage.getItem(VISITOR_KEY);
    if (!id) {
      id = generateUUID();
      localStorage.setItem(VISITOR_KEY, id);
    }
    return id;
  }
  
  // Get or create session (expires after 30 min inactivity)
  function getSession() {
    const now = Date.now();
    let session = null;
    try { session = JSON.parse(sessionStorage.getItem(SESSION_KEY)); } catch(e) {}
    
    if (!session || (now - session.lastActivity) > 30 * 60 * 1000) {
      session = {
        id: generateUUID(),
        start: now,
        lastActivity: now,
        pageViews: 0
      };
    }
    session.lastActivity = now;
    session.pageViews++;
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return session;
  }
  
  // Get today's date key
  function getDateKey() {
    return new Date().toISOString().split('T')[0];
  }
  
  // Get analytics data
  function getAnalytics() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null') || createEmptyAnalytics();
    } catch(e) {
      return createEmptyAnalytics();
    }
  }
  
  function createEmptyAnalytics() {
    return {
      totalViews: 0,
      pages: {},        // { "/index.html": { views: N, uniqueVisitors: Set } }
      daily: {},        // { "2026-02-08": { views: N, visitors: [], sessions: N } }
      referrers: {},    // { "google.com": N }
      firstSeen: new Date().toISOString(),
      lastSeen: new Date().toISOString()
    };
  }
  
  // Save analytics
  function saveAnalytics(data) {
    try {
      // Prune old daily data (keep last 90 days)
      const cutoff = new Date();
      cutoff.setDate(cutoff.getDate() - 90);
      const cutoffKey = cutoff.toISOString().split('T')[0];
      Object.keys(data.daily).forEach(k => {
        if (k < cutoffKey) delete data.daily[k];
      });
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch(e) {
      // localStorage full — prune more aggressively
      try {
        const keys = Object.keys(data.daily).sort();
        const half = Math.floor(keys.length / 2);
        keys.slice(0, half).forEach(k => delete data.daily[k]);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } catch(e2) { /* give up */ }
    }
  }
  
  // Get page path (normalized)
  function getPagePath() {
    let path = window.location.pathname;
    // Normalize: remove trailing slash, handle index
    if (path.endsWith('/')) path += 'index.html';
    if (path === '' || path === '/') path = '/index.html';
    return path;
  }
  
  // Get referrer domain
  function getReferrer() {
    try {
      if (!document.referrer) return 'direct';
      const url = new URL(document.referrer);
      if (url.hostname === window.location.hostname) return 'internal';
      return url.hostname;
    } catch(e) {
      return 'direct';
    }
  }
  
  // Track page view
  function trackView() {
    const visitorId = getVisitorId();
    const session = getSession();
    const page = getPagePath();
    const dateKey = getDateKey();
    const referrer = getReferrer();
    const data = getAnalytics();
    
    // Total views
    data.totalViews++;
    data.lastSeen = new Date().toISOString();
    
    // Page views
    if (!data.pages[page]) {
      data.pages[page] = { views: 0, visitors: [] };
    }
    data.pages[page].views++;
    if (!data.pages[page].visitors.includes(visitorId)) {
      data.pages[page].visitors.push(visitorId);
      // Keep only last 500 unique visitor IDs per page
      if (data.pages[page].visitors.length > 500) {
        data.pages[page].visitors = data.pages[page].visitors.slice(-500);
      }
    }
    
    // Daily tracking
    if (!data.daily[dateKey]) {
      data.daily[dateKey] = { views: 0, visitors: [], sessions: 0 };
    }
    data.daily[dateKey].views++;
    if (!data.daily[dateKey].visitors.includes(visitorId)) {
      data.daily[dateKey].visitors.push(visitorId);
    }
    // Track unique sessions per day
    if (!data.daily[dateKey]._sessionIds) data.daily[dateKey]._sessionIds = [];
    if (!data.daily[dateKey]._sessionIds.includes(session.id)) {
      data.daily[dateKey]._sessionIds.push(session.id);
      data.daily[dateKey].sessions = data.daily[dateKey]._sessionIds.length;
    }
    
    // Referrers (skip internal)
    if (referrer !== 'internal') {
      data.referrers[referrer] = (data.referrers[referrer] || 0) + 1;
    }
    
    saveAnalytics(data);
    
    // Also hit the external counter (seeyoufarm)
    try {
      const img = new Image();
      img.src = 'https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=' + 
        encodeURIComponent('https://treklaps.github.io/riyadh-places' + page) +
        '&count_bg=%230a1628&title_bg=%23c9a84c&icon=&icon_color=%23E7E7E7&title=views&edge_flat=true';
    } catch(e) {}
    
    // Update visitor counter in footer
    updateFooterCounter(data);
  }
  
  // Add visitor counter to footer
  function updateFooterCounter(data) {
    const dateKey = getDateKey();
    const todayVisitors = data.daily[dateKey] ? data.daily[dateKey].visitors.length : 0;
    
    // Find or create the counter element
    let counter = document.getElementById('waynrooh-visitor-counter');
    if (!counter) {
      const footerHeart = document.querySelector('.footer-heart');
      if (footerHeart) {
        counter = document.createElement('div');
        counter.id = 'waynrooh-visitor-counter';
        counter.style.cssText = 'text-align:center;padding:8px 0;color:var(--text-muted,#888);font-size:13px;font-family:Tajawal,sans-serif;';
        footerHeart.parentNode.insertBefore(counter, footerHeart);
      }
    }
    if (counter) {
      const totalViews = data.totalViews.toLocaleString('ar-SA');
      const todayCount = todayVisitors.toLocaleString('ar-SA');
      counter.innerHTML = `👁️ ${totalViews} زيارة · 👤 ${todayCount} زائر اليوم`;
    }
  }
  
  // Public API for stats page
  window.WaynroohAnalytics = {
    getData: getAnalytics,
    getVisitorId: getVisitorId,
    
    // Get stats summary
    getSummary: function() {
      const data = getAnalytics();
      const dateKey = getDateKey();
      const today = data.daily[dateKey] || { views: 0, visitors: [], sessions: 0 };
      
      // Count unique visitors across all days
      const allVisitors = new Set();
      Object.values(data.daily).forEach(d => {
        (d.visitors || []).forEach(v => allVisitors.add(v));
      });
      
      return {
        totalViews: data.totalViews,
        totalUniqueVisitors: allVisitors.size,
        todayViews: today.views,
        todayVisitors: today.visitors.length,
        todaySessions: today.sessions,
        firstSeen: data.firstSeen,
        lastSeen: data.lastSeen
      };
    },
    
    // Get page rankings
    getTopPages: function(limit) {
      const data = getAnalytics();
      return Object.entries(data.pages)
        .map(([page, info]) => ({
          page: page,
          views: info.views,
          uniqueVisitors: (info.visitors || []).length
        }))
        .sort((a, b) => b.views - a.views)
        .slice(0, limit || 20);
    },
    
    // Get daily data for chart
    getDailyData: function(days) {
      const data = getAnalytics();
      const result = [];
      const now = new Date();
      
      for (let i = (days || 30) - 1; i >= 0; i--) {
        const d = new Date(now);
        d.setDate(d.getDate() - i);
        const key = d.toISOString().split('T')[0];
        const day = data.daily[key] || { views: 0, visitors: [], sessions: 0 };
        result.push({
          date: key,
          label: d.toLocaleDateString('ar-SA', { month: 'short', day: 'numeric' }),
          views: day.views,
          visitors: (day.visitors || []).length,
          sessions: day.sessions || 0
        });
      }
      return result;
    },
    
    // Get top referrers
    getTopReferrers: function(limit) {
      const data = getAnalytics();
      return Object.entries(data.referrers || {})
        .map(([source, count]) => ({ source, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, limit || 10);
    }
  };
  
  // Run on load
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    trackView();
  } else {
    window.addEventListener('DOMContentLoaded', trackView);
  }
})();
