# 📱 MVP Workflow — وين نروح بالرياض iOS App

*محدث: 2026-02-19*

---

## 🏆 أفضل MVP Approach لتطبيقنا

### الخيار المختار: **SwiftUI Native + AI-Assisted Development**

**لماذا SwiftUI Native (مو Flutter/React Native)?**
1. ✅ أفضل أداء (native = سلس 100%)
2. ✅ Liquid Glass تلقائي (أحدث تصميم Apple)
3. ✅ MapKit أقوى من أي map library ثانية
4. ✅ Arabic RTL مدعوم native
5. ✅ Speech framework للبحث الصوتي بالعربي
6. ✅ SwiftUI = أقل كود (declarative)
7. ✅ **Xcode 26.3 + MCP = AI agents تبني التطبيق!** (جديد جداً)

---

## 🔥 Xcode 26.3 — Game Changer (فبراير 2026)

**Apple أطلقت دعم MCP (Model Context Protocol) بـ Xcode:**

```
Claude Code / Cursor / Codex
        ↕ MCP Protocol
    xcrun mcpbridge
        ↕ XPC
       Xcode
```

**الـ AI agents الحين يقدرون:**
- يكتبون كود SwiftUI
- يبنون المشروع ويقرأون الأخطاء
- يشغلون tests ويصلحون لحد ما تمشي
- **يشوفون SwiftUI previews كصور** (يتحققون من الـ UI!)
- يبحثون بوثائق Apple + WWDC transcripts
- يديرون الملفات وهيكل المشروع

**Setup:**
```bash
# Claude Code
claude mcp add --transport stdio xcode -- xcrun mcpbridge

# Cursor
# يشتغل عبر MCP config
```

**هذا يعني:** نقدر نبني التطبيق بسرعة خيالية — AI يكتب الكود + يتحقق من الـ UI + يصلح الأخطاء تلقائي!

---

## 🛠️ Resources اللي نحتاجها

### Hardware
- **Mac** (أي Mac بـ Apple Silicon — M1+)
  - MacBook Air M1 = كافي للـ MVP
  - MacBook Pro M3/M4 = أفضل للتطوير السريع
- **iPhone** للاختبار (أو Simulator يكفي مبدئياً)

### Software (مجاني)
- **Xcode 26** (مجاني من App Store)
- **Apple Developer Account** ($99/سنة للنشر على App Store)
- **Cursor** أو **Claude Code** (AI-assisted development)
- **Git** (version control)
- **Figma** (تصميم — مجاني)

### Data (جاهز عندنا!)
- ✅ places.json (3,074 مكان)
- ✅ prices-initial.json (أسعار حقيقية)
- ✅ delivery-prices.json (مقارنة توصيل)
- ✅ analysis-results.json (تحليلات)
- ✅ places-detailed.json (تفاصيل — قيد الجمع)

### Services
- **Firebase** (مجاني حتى 10K مستخدم):
  - Push Notifications
  - Analytics
  - Crashlytics
- **GitHub** (مجاني — لتخزين الكود)
- **TestFlight** (مجاني — لتوزيع البيتا)

---

## 📋 MVP Features (أول نسخة)

### Must Have (Sprint 1-2):
1. 🏠 **Home** — featured + categories + trending
2. 🔍 **Search** — بحث عربي ذكي + فلاتر
3. 🗺️ **Map** — كل الأماكن على الخريطة + "قريب مني"
4. 📍 **Place Detail** — معلومات + تقييم + أسعار + خريطة
5. ❤️ **Favorites** — حفظ محلي

### Nice to Have (Sprint 3-4):
6. 💰 **Price Compare** — مقارنة أسعار التوصيل
7. 🌙 **Ramadan Mode** — محتوى رمضان
8. 🌗 **Dark/Light Mode**
9. 🔊 **Voice Search** — بحث صوتي عربي
10. 📱 **Share** — مشاركة الأماكن

### Post-MVP:
11. 🤖 **AI Recommendations** — اقتراحات مخصصة
12. 📋 **Custom Lists** — قوائم مخصصة
13. 🔔 **Push Notifications** — أماكن جديدة + عروض
14. 🌐 **API Backend** — بدل static JSON
15. 👥 **Social Features** — متابعة + مشاركة قوائم

---

## 🔄 Development Workflow

### الطريقة المثلى (AI-Assisted):

```
1. تصميم الشاشة (Figma أو وصف نصي)
        ↓
2. Claude Code / Cursor يكتب SwiftUI
        ↓
3. Xcode 26.3 MCP → يبني ويتحقق
        ↓
4. AI يشوف Preview → يصلح UI
        ↓
5. يشغل Tests → يصلح أخطاء
        ↓
6. مراجعة سريعة → Commit
        ↓
7. TestFlight → اختبار على الجهاز
```

### Sprint Structure:
```
Sprint 1 (أسبوع): Setup + Data Layer + Home Screen
Sprint 2 (أسبوع): Search + Map + Place Detail
Sprint 3 (أسبوع): Favorites + Prices + Ramadan
Sprint 4 (أسبوع): Polish + Voice + TestFlight
```

---

## 📁 Xcode Project Structure

```
WaynNrooh/
├── App/
│   ├── WaynNroohApp.swift          # Entry point
│   └── ContentView.swift            # Tab bar
│
├── Models/
│   ├── Place.swift                  # المكان
│   ├── PriceInfo.swift              # الأسعار
│   ├── DeliveryPrice.swift          # أسعار التوصيل
│   └── Category.swift               # الفئات
│
├── ViewModels/
│   ├── HomeViewModel.swift
│   ├── SearchViewModel.swift
│   ├── MapViewModel.swift
│   ├── PlaceDetailViewModel.swift
│   └── FavoritesViewModel.swift
│
├── Views/
│   ├── Home/
│   │   ├── HomeView.swift
│   │   ├── FeaturedSection.swift
│   │   ├── CategoryGrid.swift
│   │   └── TrendingSection.swift
│   ├── Search/
│   │   ├── SearchView.swift
│   │   ├── FilterSheet.swift
│   │   └── SearchResultCard.swift
│   ├── Map/
│   │   ├── MapView.swift
│   │   └── PlaceAnnotation.swift
│   ├── PlaceDetail/
│   │   ├── PlaceDetailView.swift
│   │   ├── PriceSection.swift
│   │   ├── DeliveryCompare.swift
│   │   └── SimilarPlaces.swift
│   ├── Favorites/
│   │   └── FavoritesView.swift
│   └── Common/
│       ├── PlaceCard.swift
│       ├── RatingBadge.swift
│       ├── PriceBadge.swift
│       └── LoadingView.swift
│
├── Services/
│   ├── DataService.swift            # Load JSON data
│   ├── LocationService.swift        # GPS
│   ├── SearchEngine.swift           # AI search
│   ├── FavoritesService.swift       # UserDefaults
│   └── AnalyticsService.swift       # Firebase
│
├── Resources/
│   ├── Assets.xcassets/
│   ├── data/
│   │   ├── places.json
│   │   ├── prices-initial.json
│   │   └── delivery-prices.json
│   └── Localizable/
│       ├── ar.lproj/
│       └── en.lproj/
│
└── Supporting/
    ├── Info.plist
    ├── LaunchScreen.storyboard
    └── Extensions/
```

---

## ⏱️ Timeline

| الأسبوع | المهمة | الناتج |
|---------|--------|--------|
| 1 | Setup + Data + Home | تطبيق يفتح ويعرض أماكن |
| 2 | Search + Map + Detail | بحث + خريطة + تفاصيل |
| 3 | Prices + Favorites + Polish | مقارنة أسعار + مفضلة |
| 4 | Testing + TestFlight | نسخة بيتا جاهزة |

---

## 💡 نصائح للتطوير السريع

1. **استخدم Cursor + Xcode MCP** — AI يكتب 80% من الكود
2. **ابدأ بالبيانات** — DataService أول شي (نفس JSON الموقع)
3. **SwiftUI Previews** — شف التصميم فوري بدون تشغيل
4. **لا تبالغ بالتصميم** — Liquid Glass يسوي الشغل
5. **TestFlight من أسبوع 2** — اختبر على أجهزة حقيقية بدري
6. **نفس البيانات** — الموقع + التطبيق = نفس JSON files
