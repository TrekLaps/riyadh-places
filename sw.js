// Service Worker for وين نروح بالرياض؟
const CACHE_NAME = 'riyadh-places-v2';
const OFFLINE_URL = './index.html';

const PRECACHE_URLS = [
  './',
  './index.html',
  './cafes.html',
  './restaurants.html',
  './activities.html',
  './events.html',
  './shopping.html',
  './nature.html',
  './desserts.html',
  './best.html',
  './neighborhoods.html',
  './discover.html',
  './search.html',
  './favorites.html',
  './ramadan.html',
  './css/style.css',
  './css/ramadan.css',
  './css/search-header.css',
  './js/main.js',
  './js/search.js',
  './js/header-search.js',
  './images/icon-192.svg',
  './images/icon-512.svg',
  './data/places-light.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(OFFLINE_URL))
    );
  } else {
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
