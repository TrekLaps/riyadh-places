// Service Worker — وين نروح بالرياض؟
const CACHE_NAME = 'wain-nrooh-v2';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/cafes.html',
  '/restaurants.html',
  '/activities.html',
  '/shopping.html',
  '/nature.html',
  '/desserts.html',
  '/events.html',
  '/map.html',
  '/favorites.html',
  '/top-rated.html',
  '/new-places.html',
  '/place.html',
  '/css/style.css',
  '/js/main.js',
  '/data/places.json',
  '/manifest.json',
];

const CDN_ASSETS = [
  'https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css',
  'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css',
  'https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js',
];

// Install: cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      // Cache static assets (ignore failures for individual files)
      return Promise.allSettled(
        [...STATIC_ASSETS, ...CDN_ASSETS].map(url =>
          cache.add(url).catch(err => console.warn('Cache skip:', url))
        )
      );
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Fetch: network-first for API/data, cache-first for static
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Skip non-GET
  if (event.request.method !== 'GET') return;

  // Data files: network first, fallback to cache
  if (url.pathname.includes('/data/') || url.pathname.includes('places.json')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Images: cache first with network fallback
  if (event.request.destination === 'image') {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        }).catch(() => new Response('', { status: 404 }));
      })
    );
    return;
  }

  // Everything else: stale-while-revalidate
  event.respondWith(
    caches.match(event.request).then(cached => {
      const networkFetch = fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      }).catch(() => {
        // Return offline page if we have nothing
        if (event.request.mode === 'navigate') {
          return caches.match('/index.html');
        }
        return new Response('', { status: 404 });
      });

      return cached || networkFetch;
    })
  );
});
