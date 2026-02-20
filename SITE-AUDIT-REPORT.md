# 🔍 Riyadh Places — Full Site Audit Report

**Date:** 2026-02-20
**Pages Audited:** 87 HTML files
**Site:** wain-nrooh.com (hosted at treklaps.github.io/riyadh-places/)

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 4 |
| 🟠 HIGH | 8 |
| 🟡 MEDIUM | 9 |
| 🟢 LOW | 6 |

---

## 🔴 CRITICAL Issues (Broken Functionality)

### C1. Sitemap Domain Mismatch with Canonical URLs
- **Sitemap** uses: `https://treklaps.github.io/riyadh-places/`
- **Canonical URLs** (in 83 pages) use: `https://wain-nrooh.com/`
- **robots.txt** references: `https://treklaps.github.io/riyadh-places/sitemap.xml`
- **Impact:** Google sees conflicting signals about the authoritative domain. This causes indexing confusion, potential duplicate content penalties, and wasted crawl budget.
- **Fix:** Update sitemap.xml and robots.txt to use `wain-nrooh.com` domain consistently.

### C2. Template Literal Strings Detected as Broken Links (15 instances)
JavaScript template literals (`${variable}`) are being used in HTML `href`/`src` attributes that get parsed as literal strings before JS executes. Affected pages:
- `ai-search.html` — `${p.google_maps_url}`
- `best.html` — `${place.google_maps_url}`, `${place.image_url}`
- `compare.html` — `${p1/p2.google_maps_url}`, `${p1/p2.image_url}`
- `map.html` — `${place.google_maps_url}`
- `place.html` — `${place.google_maps_url}`, `${place.image_url}`, `${categoryPages[...]}`
- `top-rated.html` — `${place.google_maps_url}`, `${place.image_url}`
- `trending.html` — `${place.google_maps_url}`, `${place.image_url}`
- **Impact:** These are in JavaScript-generated HTML (innerHTML), so they work at runtime. **Not actually broken** — but if JS fails to load/execute, users see broken links. Consider progressive enhancement.

### C3. Service Worker Not Registered in Any Page
- `service-worker.js` exists (3.4KB) with offline caching logic, but **0 out of 87 pages** register it.
- **Impact:** PWA functionality (offline support, install prompt) is completely non-functional.
- **Fix:** Add `navigator.serviceWorker.register('/service-worker.js')` to the main JS or all pages.

### C4. Missing `og:image` on ALL 87 Pages
- Not a single page has an `og:image` meta tag.
- **Impact:** When shared on WhatsApp, Twitter, Telegram, Facebook — no preview image appears. This severely hurts social sharing virality.
- **Fix:** Add a default og:image (site logo/hero) to all pages, and category-specific images where relevant.

---

## 🟠 HIGH Issues (SEO/Performance Impact)

### H1. 24 Pages Missing Structured Data (LD+JSON)
Pages without `application/ld+json` schema markup:
`about.html`, `activities.html`, `ai-search.html`, `best.html`, `cafes.html`, `compare.html`, `delivery-compare.html`, `desserts.html`, `discover.html`, `events.html`, `favorites.html`, `google-site-verification.html`, `lists.html`, `map.html`, `nature.html`, `new-places.html`, `place.html`, `prices.html`, `restaurants.html`, `search.html`, `shopping.html`, `stats.html`, `top-rated.html`, `trending.html`
- **Impact:** Missing rich snippets in Google results. Category pages (cafes, restaurants, etc.) should have `ItemList` schema; place.html should have `LocalBusiness` schema.
- 63/87 pages DO have structured data (mostly neighborhood pages).

### H2. 76 Pages Missing Twitter Card Meta Tags
Only 11 pages have `twitter:card` tags: `breakfast-riyadh.html`, `cheap-eats.html`, `discover.html`, `family-places.html`, `guide-weekend.html`, `index.html`, `open-late.html`, `ramadan.html`, `riyadh-season.html`, `romantic-places.html`, `work-cafes.html`
- **Impact:** Twitter/X shares show minimal previews for 76 pages.

### H3. `ai-search.html` Loads 2.8MB `places.json`
- `data/places.json` is **2,787KB** — loaded in full on the AI search page.
- `data/places-light.json` exists at 1,293KB but isn't used here.
- **Impact:** Slow initial load, especially on mobile. Users may abandon before search works.
- **Fix:** Use `places-light.json` or implement server-side search/pagination.

### H4. Large Data Files on Disk
| File | Size |
|------|------|
| `data/places.json` | 2,787KB |
| `data/places-detail.json` | 2,537KB |
| `data/places-light.json` | 1,293KB |
| `supabase/seed.sql` | 1,278KB |
- These are served as static files on GitHub Pages. Consider gzip/CDN optimization.

### H5. 4 Pages Missing Canonical URL
- `ai-search.html`, `compare.html`, `google-site-verification.html`, `stats.html`
- **Impact:** Search engines may index duplicate versions of these pages.

### H6. 54 Pages Missing `manifest.json` Link
All 49 neighborhood pages plus `ai-search.html`, `compare.html`, `guide-ramadan.html`, `neighborhoods.html`, `riyadh-season.html` lack `<link rel="manifest">`.
- **Impact:** PWA install prompt won't work on these pages; inconsistent PWA experience.

### H7. 28 Neighborhood Pages Missing `ramadan.css`
During Ramadan season, these neighborhood pages won't show Ramadan theming:
`neighborhood-ammariyah.html`, `neighborhood-aziziyah.html`, `neighborhood-banban.html`, `neighborhood-batha.html`, `neighborhood-deira.html`, `neighborhood-diplomasi.html`, `neighborhood-hamra.html`, `neighborhood-maathar.html`, `neighborhood-malik-fahd.html`, `neighborhood-mansourah.html`, `neighborhood-muaiqiliyah.html`, `neighborhood-mughrazat.html`, `neighborhood-munsiyah.html`, `neighborhood-murabba.html`, `neighborhood-nafal.html`, `neighborhood-namar.html`, `neighborhood-naseem.html`, `neighborhood-nuzha.html`, `neighborhood-qayrawan.html`, `neighborhood-rahmaniyah.html`, `neighborhood-rawdah.html`, `neighborhood-rimal.html`, `neighborhood-salam.html`, `neighborhood-shifa.html`, `neighborhood-suwaidi.html`, `neighborhood-taawun.html`, `neighborhood-thumamah.html`, `neighborhood-umm-alhamam.html`
- Also missing from: `neighborhoods.html` (hub page), `ai-search.html`, `delivery-compare.html`
- **Impact:** Inconsistent seasonal theming across the site.

### H8. `google-site-verification.html` — Bare Minimum Page
This page is missing virtually everything:
- No `<title>`, no meta description, no OG tags
- No `dir="rtl"`, no `lang="ar"`
- No CSS, no JS, no navigation, no footer
- Not in sitemap (correctly excluded)
- **Impact:** Low — this is a verification-only page. But if Google indexes it, it looks broken.
- **Fix:** Add `<meta name="robots" content="noindex">` to prevent indexing.

---

## 🟡 MEDIUM Issues (Quality/Consistency)

### M1. `stats.html` — Missing Navigation and Footer
- No `<nav>` element or header section
- No footer
- **Impact:** Users who land on this page have no way to navigate back to the main site.

### M2. `ai-search.html` — Missing Footer
- Has header/navigation but no footer.
- **Impact:** Inconsistent with the other 85 pages that have footers.

### M3. 4 Pages Missing `main.js`
- `ai-search.html`, `delivery-compare.html`, `google-site-verification.html`, `stats.html`
- These pages may lack shared functionality (navigation, favorites, etc.).

### M4. Console Statements Left in Production
- `ai-search.html` — 1 console statement
- `delivery-compare.html` — 1 console statement
- `prices.html` — 1 console statement
- `ramadan.html` — 1 console statement
- **Impact:** Minor — clutters browser console. Should be removed for production.

### M5. 5 Pages Missing `search-header.css`
- `ai-search.html`, `delivery-compare.html`, `google-site-verification.html`, `guide-weekend.html`, `lists.html`
- **Impact:** Search header may render incorrectly or be unstyled on these pages.

### M6. `discover.css` Only Used by 1 Page
- `css/discover.css` is only loaded by `discover.html`.
- **Impact:** Not a bug, but consider inlining critical CSS or merging into `style.css` to reduce HTTP requests.

### M7. Manifest `start_url` Uses Absolute Path
- `manifest.json` has `"start_url": "/index.html"` — but on GitHub Pages the site is at `/riyadh-places/`, not `/`.
- **Impact:** PWA start URL would be wrong on GitHub Pages deployment. Works correctly only on custom domain (wain-nrooh.com).

### M8. No `<lastmod>` in Sitemap
- sitemap.xml uses `<changefreq>` and `<priority>` but no `<lastmod>` dates.
- **Impact:** Search engines rely on `<lastmod>` to prioritize recrawling. Without it, crawl efficiency is reduced.

### M9. External JS Dependencies (Leaflet) Loaded Without Fallback
- 2 pages load Leaflet from `unpkg.com` CDN (CSS + JS, 4 resources).
- No fallback if CDN is down.
- **Impact:** Map functionality breaks entirely if unpkg goes down.

---

## 🟢 LOW Issues (Nice to Have)

### L1. No Favicon Declared
- No `<link rel="icon">` found in pages (SVG icons exist in `/images/` but only used in manifest).
- **Impact:** Browser tabs show generic icon. Minor but looks unprofessional.

### L2. `a1b2c3d4e5f6g7h8.txt` — Mystery File
- A text file at root with a hash-like name. Likely a domain verification file.
- **Impact:** None, but should be documented or cleaned up.

### L3. Service Worker Caches Only Subset of Pages
- `service-worker.js` only caches 13 pages in `STATIC_ASSETS`, not all 87.
- **Impact:** Even if SW is registered, most pages won't work offline.

### L4. Python Scripts in `/data/` and `/scripts/`
- Multiple `.py` files for data generation/enrichment are shipped with the site.
- **Impact:** Exposes internal tooling publicly. Not a security risk but unnecessary bloat.

### L5. No 404 Page
- No `404.html` found. GitHub Pages shows its default 404.
- **Impact:** Users hitting broken URLs see a generic English error page instead of branded Arabic page.

### L6. `screenshots` Array Empty in Manifest
- `manifest.json` has `"screenshots": []`.
- **Impact:** Richer PWA install experiences (especially on Android) use screenshots. Missing opportunity.

---

## ✅ What's Working Well

| Area | Status |
|------|--------|
| **HTML structure** | All 86 main pages have proper `<html lang="ar" dir="rtl">` |
| **Viewport meta** | All 86 main pages have responsive viewport tag |
| **Title tags** | All 86 main pages have unique titles (no duplicates!) |
| **Meta descriptions** | All 86 main pages have descriptions |
| **Internal links** | 0 broken internal page-to-page links |
| **CSS consistency** | 86/87 pages use `css/style.css`; 82/87 use `css/search-header.css` |
| **JS loading** | 83/87 pages include `main.js`; 86/87 have `analytics.js` + `darkmode.js` |
| **Dark mode** | Supported across 86 pages |
| **Lazy loading** | All pages with `<img>` tags use `loading="lazy"` |
| **No render-blocking scripts** | All scripts use `defer` or are at bottom of body |
| **Alt tags** | All images have `alt` attributes |
| **Data files** | All 5 fetch() JSON references resolve to existing files |
| **Sitemap coverage** | 86/87 pages in sitemap (only verification page excluded — correct) |
| **Arabic/RTL** | Consistent across all main pages |
| **OG tags** | 86/87 pages have basic OG title/description (just missing og:image) |

---

## 📊 Priority Action Plan

### Immediate (This Week)
1. ⬜ Fix sitemap.xml domain → `wain-nrooh.com` (**C1**)
2. ⬜ Fix robots.txt sitemap URL → `wain-nrooh.com` (**C1**)
3. ⬜ Add `og:image` to all pages (**C4**)
4. ⬜ Register service worker in main.js (**C3**)
5. ⬜ Add `noindex` to google-site-verification.html (**H8**)

### This Sprint
6. ⬜ Add `twitter:card` to remaining 76 pages (**H2**)
7. ⬜ Add structured data to 24 missing pages (**H1**)
8. ⬜ Add canonical URLs to 4 missing pages (**H5**)
9. ⬜ Add manifest.json link to 54 pages (**H6**)
10. ⬜ Add ramadan.css to 28 neighborhood pages (**H7**)
11. ⬜ Add navigation/footer to stats.html (**M1**)

### Backlog
12. ⬜ Add `<lastmod>` to sitemap entries (**M8**)
13. ⬜ Remove console.log statements (**M4**)
14. ⬜ Create custom 404.html page (**L5**)
15. ⬜ Add favicon link to pages (**L1**)
16. ⬜ Optimize ai-search to use lighter data file (**H3**)
17. ⬜ Add CDN fallback for Leaflet (**M9**)
18. ⬜ Add PWA screenshots to manifest (**L6**)

---

*Report generated automatically by site-auditor subagent*
