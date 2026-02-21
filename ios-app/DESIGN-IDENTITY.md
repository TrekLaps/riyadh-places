# هوية وين نروح — التصميم البصري

## الفلسفة
"ليالي الرياض" — تطبيق يحسسك إنك تتمشى بالرياض بالليل. أخضر سعودي غامق، ذهب صحراوي، وزجاج شفاف (Liquid Glass) فوق خلفيات حية.

**مو نسخة من أحد.** هوية فريدة ١٠٠٪.

---

## لوحة الألوان

### الأخضر السعودي (Primary)
| الاسم | Hex | الاستخدام |
|-------|-----|-----------|
| أخضر-900 (ليل) | #050F0B | خلفية رئيسية |
| أخضر-800 | #0A1F16 | خلفية البطاقات |
| أخضر-700 | #0D3B2E | headers, navigation |
| أخضر-600 | #1A6B4A | أزرار ثانوية |
| أخضر-500 | #2E8B62 | hover states |
| أخضر-400 | #3CC98E | أزرار رئيسية، highlights |
| أخضر-300 | #6EDBA8 | نصوص مميزة |
| أخضر-200 | #A8EBC8 | badges خفيفة |
| أخضر-100 | #D4F4E5 | light mode خلفية |

### الذهب الصحراوي (Accent)
| الاسم | Hex | الاستخدام |
|-------|-----|-----------|
| ذهب-600 | #A08530 | نجوم التقييم (pressed) |
| ذهب-500 | #C9A84C | نجوم التقييم، أيقونات مميزة |
| ذهب-400 | #DFC474 | highlights خفيفة |
| ذهب-300 | #F0DFA0 | badges |

### ألوان الأجواء
| الاسم | Hex | الاستخدام |
|-------|-----|-----------|
| رمل | #B8A88A | نص ثانوي (dark mode) |
| كريمي | #F0EDE5 | نص رئيسي (dark mode) |
| سماء ليل | #0B1A2E | تدرج مع الأخضر |
| نخل | #1B4332 | تفاصيل أيقونات |

### ألوان دلالية
| الدلالة | Hex |
|---------|-----|
| نجاح/مفتوح | #3CC98E |
| خطأ/مغلق | #E74C3C |
| تحذير | #F0AD4E |
| معلومة | #5DADE2 |

---

## الخطوط

### Arabic
- **العناوين:** SF Arabic Rounded Bold (مدمج بـ iOS)
- **النص:** SF Arabic Regular
- **الأرقام:** SF Mono (أسعار وتقييمات)

### English (أسماء الأماكن)
- **العناوين:** SF Pro Rounded Bold
- **النص:** SF Pro Regular

### التدرج
| المستوى | الحجم | الوزن |
|---------|-------|-------|
| عنوان كبير | 28pt | Bold |
| عنوان | 22pt | Bold |
| عنوان فرعي | 18pt | Semibold |
| نص عادي | 16pt | Regular |
| تفاصيل | 14pt | Regular |
| توضيح | 12pt | Regular |
| بادج | 11pt | Medium |

---

## مكونات التصميم

### ١. بطاقة المكان (PlaceCard)
```
┌─────────────────────────────┐
│ [صورة المكان بتأثير gradient]│
│  ┌───────┐    ┌──────────┐  │
│  │ ★ ٤.٧ │    │ مطاعم 🍽 │  │
│  └───────┘    └──────────┘  │
├─────────────────────────────┤
│ ◀︎ حراء كافيه                │  ← RTL
│ حي العليا · $$              │
│ ┌────┐┌────┐┌──────┐       │
│ │قهوة││عائلي││أجواء ││       │  ← glass pills
│ └────┘└────┘└──────┘       │
└─────────────────────────────┘
```
- خلفية: `أخضر-800` مع glass effect
- الصورة: gradient overlay أخضر-900 → transparent
- التقييم: badge ذهبية
- Tags: glass capsules

### ٢. شريط التنقل (Tab Bar)
- **Liquid Glass** الحقيقي (iOS 26 `.glassEffect()`)
- ٥ تابات: 🏠 الرئيسية | 🔍 استكشف | 🗺 الخريطة | ❤️ مفضلاتي | 👤 حسابي
- النص بالعربي فقط
- Active = أخضر-400, Inactive = رمل

### ٣. شريط البحث
```
┌──────────────────────────────┐
│ 🔍  وش تبي تسوي اليوم؟      │  ← glass capsule
└──────────────────────────────┘
```
- Glass capsule بتأثير blur
- Placeholder بالعامية السعودية

### ٤. أقسام الهوم
```
┌──────────────────────────────┐
│ 🌙 وش المناسبة؟              │  ← occasion pills
│ ┌────┐┌────┐┌────┐┌────┐   │
│ │قهوة ││عشاء││عوائل││مغامرة│   │  ← glass pills
│ └────┘└────┘└────┘└────┘   │
├──────────────────────────────┤
│ 🔥 الترند هالأسبوع           │
│ [PlaceCard] [PlaceCard] →    │  ← horizontal scroll
├──────────────────────────────┤
│ ⭐ الأعلى تقييم              │
│ [PlaceCard] [PlaceCard] →    │
├──────────────────────────────┤
│ 📍 قريب منك                  │
│ [PlaceCard] [PlaceCard] →    │
└──────────────────────────────┘
```

### ٥. صفحة التفاصيل
```
┌──────────────────────────────┐
│ [Hero Image - full width]     │
│  ← ◀︎    ♡    📤              │  ← glass nav overlay
├──────────────────────────────┤
│ حراء كافيه                    │
│ Haraa Coffee                  │  ← English name smaller
│ ★★★★☆ ٤.٧ · $$ · مفتوح الحين│
│                               │
│ ┌─────┐┌─────┐┌─────┐       │
│ │الطعم ││الأجواء││الخدمة│       │  ← radar mini
│ │ ٤.٨  ││ ٤.٦  ││ ٤.٥ │       │
│ └─────┘└─────┘└─────┘       │
│                               │
│ 📍 حي العليا، طريق التحلية   │
│ 🕐 ٧ ص - ١٢ م                │
│ 📞 ٠١١٢٣٤٥٦٧٨               │
│                               │
│ [  🧭 ودّني هناك  ]           │  ← green button
│ [  💬 اسأل الذكاء  ]          │  ← glass button
└──────────────────────────────┘
```

---

## التأثيرات البصرية

### Liquid Glass (iOS 26)
```swift
.glassEffect(.regular.tint(.green.opacity(0.1)))
```
- Navigation bar, tab bar, search bar, pills, buttons
- NOT on content (cards, lists, images)

### Gradient Overlays
```swift
LinearGradient(
    colors: [Color("green900"), .clear],
    startPoint: .bottom, endPoint: .center
)
```
- على الصور لقراءة النص فوقها

### Microinteractions
- Press: scale(0.96) + haptic
- Favorite: heart pulse + haptic
- Pull refresh: palm tree animation
- Card appear: fade + slide من اليمين (RTL)
- Tab switch: spring animation

### Shadows
- Cards: shadow(color: .black.opacity(0.3), radius: 12, y: 6)
- Glass elements: NO shadow (Liquid Glass handles depth)

---

## RTL — من اليمين لليسار

- `Environment(\.layoutDirection, .rightToLeft)` على كل التطبيق
- كل النصوص `.multilineTextAlignment(.trailing)`
- الأيقونات اللي لها اتجاه = معكوسة
- Scroll أفقي = يبدأ من اليمين
- NavigationStack = back button يمين

---

## اللغة

### العربي (افتراضي)
- عامية سعودية نجدية للـ UI
- "وش تبي تسوي؟" مو "ماذا تريد أن تفعل؟"
- "مفتوح الحين" مو "مفتوح حالياً"
- "قريب منك" مو "أماكن قريبة من موقعك"
- "ودّني هناك" مو "الانتقال إلى الموقع"

### الإنقليزي
- أسماء الأماكن الإنقليزية تبقى زي ما هي
- ZERO ترجمة لمصطلحات تقنية بالـ UI

---

## Dark Mode = Default

التطبيق يفتح dark mode تلقائياً.
Light mode متاح بس الأولوية للدارك.

### Dark Mode Colors
- Background: #050F0B
- Card: #0A1F16
- Text Primary: #F0EDE5
- Text Secondary: #B8A88A

### Light Mode Colors  
- Background: #F5F2EB
- Card: #FFFFFF
- Text Primary: #1A1A1A
- Text Secondary: #6B6B6B
- Primary stays #3CC98E

---

*هذي هوية وين نروح. فريدة. سعودية. حديثة.*
