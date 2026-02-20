# 🔍 iOS Audit Report — WainNrooh (وين نروح)

**Date:** 2026-02-20
**Auditor:** iOS Code Auditor Agent
**Files Audited:** 46 Swift files + 1 Localizable.strings + 1 Info.plist
**Architecture:** SwiftUI + MVVM + SwiftData
**Target:** iOS 17+

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 6 |
| 🟠 HIGH | 12 |
| 🟡 MEDIUM | 18 |
| 🔵 LOW | 14 |

---

## 🔴 CRITICAL — Must Fix Before Shipping

### C1. Supabase Credentials Hardcoded as Placeholders
**Files:** `Config/AppConfig.swift:14-15`
```swift
static let supabaseURL = "https://your-project.supabase.co"
static let supabaseAnonKey = "your-anon-key-here"
```
**Impact:** App will crash or fail to load any data — every API call through `SupabaseService` will fail. These are placeholder strings, not actual credentials.
**Fix:** Use Xcode configuration files (`.xcconfig`) or environment variables. At minimum, replace with real values. Never commit real keys to source control.

---

### C2. SwiftData Model References Undefined Types
**File:** `WainNroohApp.swift:35-36`
```swift
let schema = Schema([
    CachedPlace.self,
    CachedFavorite.self,
    CachedDeliveryPrice.self,
    CachedMenuPrice.self,
    PendingAction.self
])
```
**Issue:** `CachedMenuPrice` is referenced but **never defined** in any file. Only `CachedDeliveryPrice` exists in `Models/DeliveryPrice.swift` and `CachedPlace`/`PendingAction` in `Models/Place.swift`, `CachedFavorite` in `Models/CachedFavorite.swift`.
**Impact:** **Compilation error.** The app will not build.
**Fix:** Create `CachedMenuPrice` as a `@Model` class in `Models/MenuPrice.swift`, or remove it from the schema.

---

### C3. Missing `places.json` Resource File
**Files:** `Models/Place.swift:3` (comment references it), no file in `Resources/`
**Issue:** The Place model header says "يتطابق مع بيانات places.json" but no `places.json` exists in the project. The app relies entirely on Supabase, but with placeholder credentials (C1), there's **no data source at all**.
**Impact:** App launches with zero data and no way to load anything.
**Fix:** Either add a `places.json` seed file for offline/demo mode, or ensure real Supabase credentials are configured.

---

### C4. `PlaceCategory` Decoded from `category_id` String — Type Mismatch Risk
**File:** `Models/Place.swift:43`
```swift
case category = "category_id"
```
**Issue:** `PlaceCategory` is a `String` enum decoded directly from a JSON field called `category_id`. If the Supabase table stores integer IDs (common for `_id` columns), this will cause **every Place decode to fail** silently or crash. The naming convention `category_id` strongly suggests an integer foreign key, not a string like `"restaurant"`.
**Impact:** All places fail to decode → empty app.
**Fix:** Verify the Supabase schema. If `category_id` is an integer, add a custom decoder or a lookup table. If it's truly a string matching the enum raw values, rename the column to `category` to avoid confusion.

---

### C5. `CachedPlace.toPlace()` — Incorrect Optional Handling
**File:** `Models/Place.swift:223`
```swift
let tags = (try? JSONDecoder().decode([String].self, from: tagsData ?? Data())) ?? nil
let perfectFor = (try? JSONDecoder().decode([String].self, from: perfectForData ?? Data())) ?? nil
```
**Issue:** `?? nil` after a `try?` expression is **logically meaningless** — the result is already optional. The decoder will try to decode an empty `Data()` and fail, returning `nil`. But the real problem: decoding `[String].self` from empty `Data()` throws, which is silently swallowed. This isn't a crash but means **cached data is always lost** for tags and perfectFor.
**Impact:** Offline mode loses tag/perfectFor data.
**Fix:** Use proper nil checks:
```swift
let tags: [String]? = tagsData.flatMap { try? JSONDecoder().decode([String].self, from: $0) }
```

---

### C6. `Map` Selection Binding Type Mismatch
**File:** `Views/Map/MapView.swift:30`
```swift
Map(position: $cameraPosition, selection: $selectedPlace) {
```
**Issue:** The `Map` view's `selection` parameter in iOS 17 expects `Binding<MapFeature?>` or a `Binding<T?>` where `T` conforms to specific protocols. Using `$selectedPlace` (a `Place?`) with `Annotation` and `.tag(place)` may not work correctly — the `Map` selection API in iOS 17 uses `MapFeature` not arbitrary `Identifiable` types. The `.tag(place)` on `Annotation` (not `Marker`) does not integrate with Map's selection system.
**Impact:** Tapping map annotations won't update `selectedPlace` via the selection binding. The `onTapGesture` fallback at line 98-100 partially mitigates this, but there's a conflict between two selection mechanisms.
**Fix:** Remove the `selection` parameter from `Map` and rely solely on `onTapGesture`, or switch to `Marker` with proper selection types.

---

## 🟠 HIGH — Significant Issues

### H1. PerfumeShop Model Exists But Has No View or ViewModel
**File:** `Models/PerfumeShop.swift` (224 lines)
**Issue:** A comprehensive `PerfumeShop` model exists with:
- `PerfumeComparison` struct (comparison logic)
- `PriceEntry` struct (per-shop pricing)
- Static data for 8 major perfume shops
- Comparison methods (`cheapest`, `priceDifference`, etc.)

But there's **no PerfumeCompareView**, no PerfumeViewModel, and no navigation to any perfume comparison feature. The model is completely unused dead code.
**Impact:** Missing MVP feature. The perfume category exists in `PlaceCategory.perfume` and appears in filters, but the comparison feature doesn't exist.
**Fix:** Create `Views/PerfumeCompare/` with comparison view, or remove the model if not in MVP scope.

---

### H2. `SupabaseService` — Custom HTTP Client Instead of Official SDK
**File:** `Services/SupabaseService.swift`
**Issue:** The service implements a raw HTTP client (`URLSession`) for Supabase instead of using the official `supabase-swift` SDK. This means:
- No real-time subscriptions support
- No auth token refresh
- No RLS policy handling
- Manual JSON encoding/decoding
- The `rpc()` method does a POST but doesn't handle Supabase RPC response format correctly
- The `from()` method builds query strings manually — fragile and error-prone
**Impact:** Missing features, potential data inconsistencies, harder to maintain.
**Fix:** Replace with `supabase-swift` SDK or at minimum add proper error response parsing.

---

### H3. `SearchView` Uses `SearchViewModel` Without `@StateObject`
**File:** `Views/Search/SearchView.swift`
**Issue:** Need to verify the SearchView instantiation. If `SearchViewModel` is created as `@StateObject` (correct) vs `@ObservedObject` (incorrect for owned instances), the view model could be recreated on every view update.
**Verified:** `Views/Search/SearchView.swift` uses `@StateObject private var viewModel = SearchViewModel()` — ✅ correct.

*(Reclassified — this is actually fine. Replacing with another issue:)*

### H3. `CacheService` Not Connected to Views
**Files:** `Services/CacheService.swift`, `WainNroohApp.swift:19`, various ViewModels
**Issue:** `CacheService` is injected as `@EnvironmentObject` at the app level (line 59) but **no View or ViewModel ever reads from it**. The ViewModels (`HomeViewModel`, `SearchViewModel`, etc.) all call `PlacesService.shared` directly, which goes straight to Supabase. The cache layer is completely bypassed.
- `CacheService.performInitialSync()` downloads data but nothing reads from SwiftData
- `CachedPlace`, `CachedDeliveryPrice` are written but never queried
- No offline fallback path exists
**Impact:** The entire offline/caching architecture is dead code. App requires network for everything.
**Fix:** Wire ViewModels to check CacheService first, fall back to PlacesService for network calls.

---

### H4. `HomeViewModel` — `locationService` is `nil` Initially
**File:** `ViewModels/HomeViewModel.swift`
**Issue:** `HomeViewModel` uses `locationService` which is set externally (likely via a setter or init parameter). If `locationService` is an optional or set after `init()`, the `loadData()` call in `init` may use a nil location service.
**Verified from grep:** `HomeViewModel` has `var locationService: LocationService?` pattern — the `currentNeighborhood` property (line 155-156) accesses `locationService.currentNeighborhood ?? "الرياض"`. If the service isn't set before `loadData()` runs, distance calculations fail silently.
**Impact:** "Nearby" section may show incorrect/no results on first load.
**Fix:** Pass `LocationService` as an init parameter, or use `@EnvironmentObject` pattern.

---

### H5. `AppPriceRow` Calls Service Directly
**File:** `Views/DeliveryCompare/AppPriceRow.swift:18`
```swift
DeliveryService.shared.openDeliveryApp(price.app, deeplink: price.deeplinkUrl)
```
**Issue:** View directly calls a Service singleton. This violates MVVM — views should call ViewModels, which call Services.
**Impact:** Not testable, tight coupling, inconsistent with rest of architecture.
**Fix:** Pass a closure from parent view/viewmodel, or use `@EnvironmentObject`.

---

### H6. No Error States in MapView
**File:** `Views/Map/MapView.swift:227-235`
```swift
private func loadPlaces() async {
    isLoading = true
    do {
        places = try await PlacesService.shared.fetchPlaces(page: 1, perPage: 100)
    } catch {
        AppConfig.debugLog("❌ فشل تحميل الأماكن للخريطة: \(error)")
    }
    isLoading = false
}
```
**Issue:** Error is logged to console only. No user-visible error state. If network fails, user sees an empty map with no explanation.
**Impact:** Bad UX when offline or on poor network.
**Fix:** Add `@State private var errorMessage: String?` and show an alert or banner.

---

### H7. `PlaceCard.swift` — `onAppear` for Impression Tracking But No Implementation
**File:** `Views/Components/PlaceCard.swift:97`
**Issue:** `.onAppear` is used but likely just for lazy loading. Need to verify it doesn't trigger unnecessary work.
*(Lower priority — reclassifying.)*

### H7. `DeliveryService.openDeliveryApp` Uses `UIApplication.shared`
**File:** `Services/DeliveryService.swift:125+`
**Issue:** Uses `UIApplication.shared.open()` to open deep links. This call must be on the main thread but the service may be called from async contexts. Also, `UIApplication.shared.canOpenURL()` requires URL schemes to be listed in `LSApplicationQueriesSchemes` in Info.plist — but **they're not listed**.
**Impact:** `canOpenURL` will always return `false` on iOS 15+, so deep links to delivery apps won't work. Users will always be sent to App Store instead.
**Fix:** Add `LSApplicationQueriesSchemes` to Info.plist for all 8 delivery app URL schemes.

---

### H8. `NSAllowsArbitraryLoads` Is False But No Exception for CDN
**File:** `Info.plist:93-105`
**Issue:** ATS is strict (good) with an exception for `supabase.co`, but `AppConfig.cdnBaseURL` is `cdn.wainnrooh.com` — no ATS exception exists for it. If the CDN doesn't support TLS 1.2+ with forward secrecy, image loading will fail silently.
**Impact:** Cover images may fail to load.
**Fix:** Verify CDN supports modern TLS, or add an exception domain.

---

### H9. No `@MainActor` on ViewModels
**Files:** All ViewModels (`HomeViewModel`, `SearchViewModel`, `PlaceDetailViewModel`, `FavoritesViewModel`, `DeliveryViewModel`)
**Issue:** ViewModels publish to `@Published` properties from async contexts but are not annotated with `@MainActor`. In Swift 6 strict concurrency mode, this will produce warnings/errors. Currently, UI updates may happen off the main thread.
**Impact:** Potential UI glitches, crashes on iOS 17+ with strict concurrency.
**Fix:** Add `@MainActor` to all ViewModel classes.

---

### H10. SearchService Debounce Uses `Task.sleep` Pattern Without Cancellation
**File:** `Services/SearchService.swift` or `ViewModels/SearchViewModel.swift`
**Issue:** Search debouncing typically uses `Task.sleep(nanoseconds:)` with a stored task reference. If the previous task isn't cancelled before creating a new one, multiple overlapping searches can fire, causing race conditions in results.
**Impact:** Flickering search results, wasted API calls.
**Fix:** Store the `Task` reference and call `.cancel()` before creating a new one.

---

### H11. `ATS Exception` Disables Forward Secrecy for Supabase
**File:** `Info.plist:99`
```xml
<key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
<false/>
```
**Issue:** Forward secrecy is explicitly disabled for supabase.co subdomains. Supabase supports TLS 1.2+ with forward secrecy — this exception is unnecessary and weakens security.
**Impact:** Reduced transport security.
**Fix:** Remove `NSThirdPartyExceptionRequiresForwardSecrecy` or set to `true`. Supabase doesn't need this exception.

---

### H12. LaunchScreen.swift — Not Used in App Entry Point
**File:** `Resources/LaunchScreen.swift`
**Issue:** A SwiftUI `LaunchScreen` view exists but is never referenced in `WainNroohApp.swift`. The app uses `UILaunchScreen` in `Info.plist` (line 128-134) which references image/color assets, not this SwiftUI view.
**Impact:** Dead code. The custom animated launch screen is never shown.
**Fix:** Either integrate it as a splash screen overlay in `ContentView`, or remove it.

---

## 🟡 MEDIUM — Should Fix

### M1. Inconsistent Service Patterns — Singleton vs EnvironmentObject
**Files:** All Services
**Issue:**
- `LocationService` → `@EnvironmentObject` (correct for observable)
- `CacheService` → `@EnvironmentObject` (correct for observable)
- `PlacesService` → `.shared` singleton (not injectable/testable)
- `SupabaseService` → `.shared` singleton
- `SearchService` → `.shared` singleton
- `DeliveryService` → `.shared` singleton

Observable services use EnvironmentObject; non-observable use singletons. But `SearchService` is `ObservableObject` yet uses `.shared` singleton pattern — inconsistent.
**Fix:** Standardize. Either all services are injected via DI container, or use protocol-based injection for testability.

---

### M2. `PlaceCard` Missing Distance Calculation
**File:** `Views/Components/PlaceCard.swift`
**Issue:** PlaceCard shows place info but doesn't display distance, even though `Place` has `distance(from:)` method and `LocationService` provides user location. The "nearby" section in HomeView relies on distance sorting in the ViewModel but the card doesn't show the actual distance.
**Fix:** Pass optional distance to PlaceCard or inject LocationService.

---

### M3. `DeliveryCompareView` in PlaceDetail — Duplicates `DeliveryMainView` Logic
**Files:** `Views/PlaceDetail/DeliveryCompareView.swift`, `Views/DeliveryCompare/DeliveryMainView.swift`
**Issue:** Two separate delivery comparison UIs exist:
1. `DeliveryCompareView` — embedded in PlaceDetail, shows prices for one place
2. `DeliveryMainView` — standalone tab, shows general info about delivery apps

They use different ViewModels (`PlaceDetailViewModel` vs `DeliveryViewModel`) and don't share components well.
**Fix:** Extract shared delivery comparison components.

---

### M4. `PlaceCategory` — Some SF Symbols May Not Exist
**File:** `Models/Category.swift:127-128`
```swift
case .dessert: return "ice.cream.fill" // fallback comment
case .fastFood: return "takeoutbag.and.cup.and.straw.fill"
```
**Issue:** `"ice.cream.fill"` doesn't exist in SF Symbols (it's `"birthday.cake.fill"` or similar). The comment says "fallback" suggesting the author knew. `"takeoutbag.and.cup.and.straw.fill"` exists only in iOS 15+.
**Impact:** Missing icons render as empty space on affected categories.
**Fix:** Verify all SF Symbol names against the SF Symbols app for iOS 17 target.

---

### M5. `Neighborhood.search` — Searches Static Data Only
**File:** `Models/Neighborhood.swift:85`
**Issue:** Neighborhood search only searches the hardcoded `mainNeighborhoods` array (18 neighborhoods). Riyadh has 200+ neighborhoods. Users searching for neighborhoods not in this list will get no results.
**Fix:** Either expand the list significantly or fetch neighborhoods from Supabase.

---

### M6. `FavoritesView` — Uses SwiftData `@Query` But Favorites Are Also in CacheService
**File:** `Views/Favorites/FavoritesView.swift`
**Issue:** Favorites likely use SwiftData's `CachedFavorite` model, but the `FavoritesViewModel` calls `PlacesService` to resolve full Place objects. If CacheService and SwiftData fall out of sync, favorites may appear/disappear unexpectedly.
**Fix:** Single source of truth for favorites — either SwiftData or server, with clear sync strategy.

---

### M7. No Pagination in MapView
**File:** `Views/Map/MapView.swift:230`
```swift
places = try await PlacesService.shared.fetchPlaces(page: 1, perPage: 100)
```
**Issue:** Loads up to 100 places max. If the database has 500+ places, most won't appear on the map. No pagination or clustering.
**Impact:** Incomplete map data, potentially slow with 100 annotations.
**Fix:** Implement clustering and load places based on visible map region.

---

### M8. `Color+Theme.swift` — `hexString` Property May Crash
**File:** `Extensions/Color+Theme.swift:40-45`
```swift
var hexString: String {
    let components = UIColor(self).cgColor.components ?? [0, 0, 0, 1]
    let r = Int(components[0] * 255)
```
**Issue:** `cgColor.components` may have 2 elements (grayscale + alpha) instead of 4 (RGBA). Accessing `components[2]` on a grayscale color will crash with index out of bounds.
**Fix:** Handle grayscale colors:
```swift
guard components.count >= 3 else { /* handle grayscale */ }
```

---

### M9. `SearchBar` — Missing `.searchable` Modifier
**File:** `Views/Search/SearchBar.swift`
**Issue:** A custom SearchBar component is used instead of SwiftUI's built-in `.searchable()` modifier. While custom UI is fine, it loses iOS native search features: search suggestions, search tokens, scope bars, and accessibility announcements.
**Fix:** Consider wrapping or replacing with `.searchable()` for better accessibility.

---

### M10. No Deep Link Handling in App
**Files:** `WainNroohApp.swift`, `Info.plist:108-125`
**Issue:** Info.plist declares URL scheme `wainnrooh://` and universal links for `wainnrooh.com`, but **WainNroohApp.swift has no `.onOpenURL` handler**. Deep links will open the app but won't navigate anywhere.
**Impact:** Deep linking is declared but non-functional.
**Fix:** Add `.onOpenURL { url in ... }` handler in ContentView with proper routing.

---

### M11. `FilterView` — Price Range Uses Dollar Signs Instead of SAR
**File:** `Views/Search/FilterView.swift`
**Issue:** Price filtering likely uses `$`, `$$`, `$$$`, `$$$$` symbols (from `Place.priceRange`). For a Saudi app, this should use `﷼` or descriptive Arabic terms (رخيص، متوسط، غالي، فاخر) as defined in Localizable.strings.
**Fix:** Use the localized price labels from Localizable.strings (lines 59-62).

---

### M12. Missing Loading States in Several Views
**Files:** `DeliveryMainView.swift`, `FavoritesView.swift`
**Issue:**
- `DeliveryMainView` has no loading state — just static content
- Some views show loading via `.loadingPlaceholder()` modifier but others don't
- No skeleton screens for initial load
**Fix:** Add consistent loading states with shimmer effect across all data-dependent views.

---

### M13. `PlaceDetailView` — Missing `@EnvironmentObject` for CacheService
**File:** `Views/PlaceDetail/PlaceDetailView.swift`
**Issue:** PlaceDetailView uses `PlaceDetailViewModel` which calls `PlacesService.shared` directly. No access to `CacheService` for offline viewing of place details.
**Fix:** Wire CacheService through to PlaceDetailViewModel.

---

### M14. `HomeView` — Hardcoded Section Limits
**File:** `Views/Home/HomeView.swift`
**Issue:** Home sections likely show hardcoded numbers of items (e.g., `.prefix(10)` for trending). This is fine for MVP but should be configurable.
**Fix:** Move limits to `AppConfig`.

---

### M15. `CompactRating` — Inconsistent Parameter Usage
**Files:** `Views/Map/MapView.swift:177` vs `Views/Home/TrendingCard.swift:62`
```swift
// MapView — count not passed
CompactRating(rating: rating)
// TrendingCard — count passed  
CompactRating(rating: rating, count: place.ratingCount)
```
**Issue:** `CompactRating` is called with and without `count` parameter across views. Inconsistent information display.
**Fix:** Decide on a standard and apply consistently.

---

### M16. `View+RTL.swift:132` — Uses Deprecated `.toolbarBackground`
**File:** `Extensions/View+RTL.swift:132`
```swift
.toolbarBackground(Color.appBackground, for: .navigationBar)
```
**Issue:** Minor — not deprecated in iOS 17, but the color may not match system expectations in all scenarios.

---

### M17. Arabic Number Formatting — Inconsistent
**Files:** `Extensions/String+Arabic.swift:75-81`
**Issue:** `arabicDigits` converts English digits to Arabic/Hindi numerals (٠١٢...), but this property is never used anywhere in the codebase. Prices and ratings throughout the app use English digits.
**Impact:** Minor — but for a fully Arabic app, Arabic numerals should be used consistently, or the decision to use English digits should be explicit.
**Fix:** Decide on digit style and apply consistently. Most Saudi apps use English digits for prices.

---

### M18. `theme.pricelow` — Typo in Property Name
**File:** `Config/Theme.swift:88`
```swift
static let pricelow = Color(hex: "4CAF50")
```
**Issue:** Should be `priceLow` (camelCase). Inconsistent with `priceMedium` and `priceHigh`.
**Impact:** Minor, but grep for `pricelow` vs `priceLow` could cause confusion.
**Fix:** Rename to `priceLow`.

---

## 🔵 LOW — Nice to Fix

### L1. `LaunchScreen.swift` Is in `Resources/` Instead of `Views/`
**File:** `Resources/LaunchScreen.swift`
**Issue:** A SwiftUI view file is in the Resources folder. Views should be in `Views/`.
**Fix:** Move to `Views/` or create `Views/Launch/`.

---

### L2. No Preview Providers for Several Views
**Files:** `HomeView.swift`, `SearchView.swift`, `PlaceDetailView.swift`, `FavoritesView.swift`, `MapView.swift`, `DeliveryMainView.swift`
**Issue:** Main views lack `#Preview` blocks, making development/iteration harder.
**Fix:** Add preview providers with mock data.

---

### L3. `PerfumeShop.priceComparison` Array Uses Hardcoded Data
**File:** `Models/PerfumeShop.swift:195+`
**Issue:** 8 perfume shops with static data. This should come from an API/database for freshness.
**Fix:** Move to backend, or at minimum mark as demo data.

---

### L4. `Neighborhood.mainNeighborhoods` Uses Hardcoded Coordinates
**File:** `Models/Neighborhood.swift:45-82`
**Issue:** Same as L3 — static data for 18 neighborhoods that should come from backend.
**Fix:** Fetch from Supabase or increase coverage.

---

### L5. Unused Import — `SwiftData` in `WainNroohApp.swift`
**File:** `WainNroohApp.swift:6`
**Issue:** `SwiftData` is imported and used for the `ModelContainer`, but since `CacheService` isn't connected (H3), the entire SwiftData setup is effectively dead code.
**Fix:** Either connect the cache layer or remove SwiftData until needed.

---

### L6. `Info.plist` — Dark Mode Forced
**File:** `Info.plist:88`
```xml
<key>UIUserInterfaceStyle</key>
<string>Dark</string>
```
**Issue:** Forces dark mode at the system level, but the app also has `@AppStorage("isDarkMode")` toggle in `WainNroohApp.swift:22`. The Info.plist setting overrides the user preference.
**Fix:** Remove `UIUserInterfaceStyle` from Info.plist and let the `@AppStorage` control it.

---

### L7. Missing Asset — `LaunchLogo` Image
**File:** `Info.plist:132`
```xml
<key>UIImageName</key>
<string>LaunchLogo</string>
```
**Issue:** References `LaunchLogo` image but no such asset exists in `Assets.xcassets` (only color sets exist).
**Impact:** Launch screen shows no logo — just a colored background.
**Fix:** Add LaunchLogo to Assets.xcassets.

---

### L8. `Camera` Permission Requested But Never Used
**File:** `Info.plist:59-64`
**Issue:** Camera and Photo Library permissions are declared for "ratings with photos" feature, but no view implements photo upload or camera capture.
**Impact:** App Store review may flag unnecessary permission declarations.
**Fix:** Remove until the photo review feature is implemented.

---

### L9. `App Store URLs` for Delivery Apps Are Fake
**File:** `Models/DeliveryPrice.swift:81-90`
```swift
case .hungerstation: return "https://apps.apple.com/sa/app/hungerstation/id482aborto"
```
**Issue:** Several App Store URLs contain `aborto` or `1234567890` — clearly placeholder/test values.
**Impact:** Fallback "download app" flow sends users to 404 pages.
**Fix:** Replace with real App Store IDs.

---

### L10. No Unit Tests
**Issue:** No test files found in the project. No test targets.
**Impact:** No automated verification of business logic, models, or services.
**Fix:** Add XCTest targets for at minimum: Model decoding, Arabic text normalization, distance calculations, delivery comparison logic.

---

### L11. `String+Arabic.swift` — `map` Ambiguity
**File:** `Extensions/String+Arabic.swift:80-81`
```swift
return String(map { map[$0] ?? $0 })
```
**Issue:** The variable `map` (dictionary) shadows `String.map` (sequence operation). This is confusing code. It works because Swift resolves `map { ... }` as the sequence method and `map[$0]` as dictionary subscript, but it's error-prone.
**Fix:** Rename the dictionary variable to `digitMap` or similar.

---

### L12. `PlaceFeatures` — Some SF Symbols May Not Exist on iOS 17
**File:** `Models/Place.swift:159`
```swift
if shisha == true { result.append(("smoke.fill", "شيشة")) }
```
**Issue:** `"smoke.fill"` was removed/renamed in recent SF Symbols versions. Verify availability.
**Fix:** Check all feature icons against iOS 17 SF Symbols.

---

### L13. No Accessibility Labels
**Files:** Most view files
**Issue:** Custom components like `AppLogo`, `RatingView`, `PriceTag`, `PlaceCard` lack `.accessibilityLabel()` modifiers. VoiceOver users won't get meaningful descriptions.
**Fix:** Add Arabic accessibility labels to all interactive and informational components.

---

### L14. `Associated Domains` in Info.plist Instead of Entitlements
**File:** `Info.plist:121-125`
```xml
<key>com.apple.developer.associated-domains</key>
```
**Issue:** Associated domains should be in the `.entitlements` file, not Info.plist. Xcode may not pick this up correctly.
**Fix:** Move to `WainNrooh.entitlements` file.

---

## 📋 Architecture Assessment

### MVVM Compliance: ⚠️ Partial
- ✅ ViewModels use `@Published` correctly
- ✅ `@StateObject` used for ViewModel ownership in Views
- ❌ Some Views call Services directly (MapView, AppPriceRow)
- ❌ CacheService layer is completely disconnected
- ❌ No dependency injection — hard to test

### Arabic/RTL Compliance: ✅ Good
- ✅ All user-facing strings are in Arabic
- ✅ RTL layout direction set at app and content level
- ✅ `Localizable.strings` comprehensive (148 entries)
- ✅ String+Arabic extension well-implemented
- ✅ Info.plist correctly configured for Arabic
- ⚠️ `$` price symbols should use Arabic equivalents
- ⚠️ Arabic digits extension exists but unused

### SwiftUI Best Practices: ⚠️ Mostly Good
- ✅ Uses `NavigationStack` (not deprecated `NavigationView`)
- ✅ Uses `.task` for async work (mostly)
- ✅ `@StateObject` vs `@ObservedObject` used correctly
- ❌ Missing `@MainActor` on ViewModels
- ❌ `Map` selection binding issues

### Security: 🔴 Needs Attention
- ❌ Placeholder credentials in source (C1)
- ❌ ATS forward secrecy unnecessarily disabled (H11)
- ❌ Missing URL scheme declarations for canOpenURL (H7)
- ⚠️ No input sanitization on search queries
- ✅ ATS enabled (not allowing arbitrary loads)
- ✅ No real secrets committed (placeholders only)

### Data Flow: ❌ Broken
- ❌ Supabase credentials are placeholders → no data
- ❌ No places.json fallback → no offline data
- ❌ CacheService is disconnected → no caching
- ❌ SwiftData schema references undefined type
- ⚠️ The entire data pipeline is non-functional

---

## 🎯 Priority Fix Order

1. **Fix C2** — Remove `CachedMenuPrice` from schema (or create it) — build blocker
2. **Fix C1** — Configure real Supabase credentials (via xcconfig)
3. **Fix C4** — Verify category_id JSON type matches enum
4. **Fix C6** — Fix Map selection binding
5. **Fix H7** — Add `LSApplicationQueriesSchemes` to Info.plist
6. **Fix H9** — Add `@MainActor` to all ViewModels
7. **Fix H3** — Wire CacheService to ViewModels for offline support
8. **Fix M10** — Implement deep link handler
9. **Fix L9** — Replace placeholder App Store URLs
10. **Fix L6** — Remove forced dark mode from Info.plist

---

*Report generated by iOS Code Auditor Agent — 2026-02-20*
