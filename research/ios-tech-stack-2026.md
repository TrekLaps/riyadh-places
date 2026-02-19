# iOS Tech Stack — محدث فبراير 2026

## الوضع الحالي
- **iOS 26** (سبتمبر 2025) — الإصدار الحالي
- **iOS 27** — WWDC يونيو 2026، بيتا يوليو، إصدار سبتمبر 2026
- **Xcode 26** — الحالي

## Liquid Glass (WWDC 2025) — أهم تحديث تصميمي
أكبر تحديث تصميم من Apple بـ 10+ سنوات:
- تصميم زجاجي سائل يتفاعل مع المحتوى
- Real-time rendering + specular highlights
- Contextual adaptation (الأزرار تتغير حسب السياق)
- Color adaptation تلقائي
- **مجرد recompile مع Xcode 26 = التصميم الجديد تلقائي!**
- APIs جديدة: `glassEffect()` للتخصيص

## SwiftUI Updates (WWDC 2025)
- Cross-platform consistency (نفس الكود على كل الأجهزة)
- أداء محسن
- مكونات UI جديدة
- تكامل أعمق مع MapKit

## التوصيات لتطبيقنا

### Target
- **Minimum:** iOS 17 (يغطي 95%+ من الأجهزة)
- **Optimized for:** iOS 26 (Liquid Glass)
- **Ready for:** iOS 27

### Tech Stack
```
SwiftUI (UI) + Liquid Glass design
├── MapKit (خرائط + GPS)
├── CoreLocation (موقع المستخدم)
├── CoreData / SwiftData (offline storage)
├── Speech framework (voice search بالعربي)
├── Foundation (URLSession networking)
├── CloudKit (sync favorites)
├── Firebase (push notifications + analytics)
└── Combine (reactive data flow)
```

### Design Language
- استخدم Liquid Glass = تطبيقنا يبان modern تلقائي
- Dark mode native (system-aware)
- RTL native support في SwiftUI
- Dynamic Type (accessibility)
- Arabic font: SF Arabic (system font)

### Architecture
- **MVVM** + Repository pattern
- **Swift Concurrency** (async/await)
- **SwiftData** for offline (replacement for CoreData)
- **Observation framework** (iOS 17+)

### حجم التطبيق المتوقع
- App binary: ~5 MB
- Data (places.json): ~2 MB
- Images cache: variable
- Total install: ~15 MB (خفيف جداً)
