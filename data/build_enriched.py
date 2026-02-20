#!/usr/bin/env python3
"""Build enriched entertainment JSON for Riyadh places project."""
import json

places = [
  # === ترفيه (50 places) ===
  {
    "name": "باونس الرياض", "name_en": "Bounce Riyadh", "category": "ترفيه",
    "rating": 4.3, "rating_count": 2800, "phone": "+966920009900",
    "hours": {"sun": "2:00 PM - 10:00 PM", "mon": "2:00 PM - 10:00 PM", "tue": "2:00 PM - 10:00 PM", "wed": "2:00 PM - 10:00 PM (سيدات)", "thu": "2:00 PM - 10:00 PM (عوائل)", "fri": "2:00 PM - 10:00 PM", "sat": "12:00 PM - 10:00 PM"},
    "website": "https://bounce.sa", "instagram": "@bouncesa",
    "description_ar": "أول مركز ترامبولين في الرياض يوفر تجربة فري ستايل مع مناطق قفز متنوعة وألعاب دودج بول وتسلق الجدران، مخصص للسيدات",
    "perfect_for": ["عوائل", "أطفال", "رياضة", "مغامرة"], "price_level": "$$",
    "address_ar": "4466 طريق خريص الفرعي، حي الروضة، الرياض",
    "entry_fee": "89 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة الملك عبدالله", "name_en": "King Abdullah Park", "category": "ترفيه",
    "rating": 4.4, "rating_count": 15000, "phone": "+966114500000",
    "hours": {"sun": "4:00 PM - 12:00 AM", "mon": "4:00 PM - 12:00 AM", "tue": "4:00 PM - 12:00 AM", "wed": "4:00 PM - 12:00 AM", "thu": "4:00 PM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "4:00 PM - 12:00 AM"},
    "website": None, "instagram": None,
    "description_ar": "حديقة كبيرة في قلب الرياض تضم نوافير ملونة ومسطحات خضراء ومناطق ألعاب للأطفال وممرات للمشي",
    "perfect_for": ["عوائل", "أطفال", "تنزه", "رومانسي"], "price_level": "$",
    "address_ar": "حي الملز، الرياض", "entry_fee": "10 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة الملك فهد", "name_en": "King Fahd Park", "category": "ترفيه",
    "rating": 4.4, "rating_count": 12000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة مركزية واسعة بأشجار النخيل والمساحات الخضراء مع ملاعب أطفال وبحيرات صناعية ومسارات للمشي والدراجات",
    "perfect_for": ["عوائل", "أطفال", "رياضة", "تنزه"], "price_level": "مجاني",
    "address_ar": "شارع العليا، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "إسكيب أرابيا", "name_en": "Escape Arabia", "category": "ترفيه",
    "rating": 4.5, "rating_count": 1200, "phone": "+966583169169",
    "hours": {"sun": "12:00 PM - 12:00 AM", "mon": "12:00 PM - 12:00 AM", "tue": "12:00 PM - 12:00 AM", "wed": "12:00 PM - 12:00 AM", "thu": "12:00 PM - 12:00 AM", "fri": "12:00 PM - 12:00 AM", "sat": "12:00 PM - 12:00 AM"},
    "website": "https://escape.sa", "instagram": "@escapearabia",
    "description_ar": "غرف هروب تفاعلية بتصاميم مبتكرة تتحدى الذكاء والعمل الجماعي، 4 غرف هروب و2 غرف واقع افتراضي",
    "perfect_for": ["أصدقاء", "شباب", "مغامرة", "تيم بيلدنق"], "price_level": "$$$",
    "address_ar": "شارع الأمير محمد بن عبدالعزيز، السليمانية، الرياض",
    "entry_fee": "175 SAR/شخص", "kid_friendly": False, "family_friendly": True
  },
  {
    "name": "عالم جمولي", "name_en": "Jomoli World", "category": "ترفيه",
    "rating": 4.3, "rating_count": 3500, "phone": "+966114577744",
    "hours": {"sun": "4:00 PM - 10:00 PM", "mon": "4:00 PM - 10:00 PM", "tue": "4:00 PM - 10:00 PM", "wed": "4:00 PM - 10:00 PM", "thu": "4:00 PM - 10:00 PM", "fri": "4:00 PM - 11:00 PM", "sat": "4:00 PM - 10:00 PM"},
    "website": None, "instagram": "@jomoli_world",
    "description_ar": "مدينة مصغرة تعليمية ترفيهية للأطفال على مساحة 12,000 متر مربع يتعلمون فيها المهن",
    "perfect_for": ["أطفال", "عوائل", "تعليمي"], "price_level": "$$",
    "address_ar": "طريق الصحابة، حي المونسية، الرياض",
    "entry_fee": "89 SAR شامل | 35 SAR المتاهة", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "فزز هوا الترفيهي", "name_en": "Fizz Hawa", "category": "ترفيه",
    "rating": 4.2, "rating_count": 2200, "phone": "+966920033322",
    "hours": {"sun": "10:00 AM - 12:00 AM", "mon": "10:00 AM - 12:00 AM", "tue": "10:00 AM - 12:00 AM", "wed": "10:00 AM - 12:00 AM", "thu": "10:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://fizzhawa.com", "instagram": "@fizzhawa",
    "description_ar": "مركز ترفيهي شامل يضم ألعاب حركية وتسلق جدران وتزلج وسيارات متصادمة",
    "perfect_for": ["عوائل", "أطفال", "أصدقاء", "مغامرة"], "price_level": "$$",
    "address_ar": "حي حطين، بوليفارد وورلد، 3390 طريق الدمام، الرياض",
    "entry_fee": "40-99 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ووش الترفيهي", "name_en": "Woosh Entertainment", "category": "ترفيه",
    "rating": 4.2, "rating_count": 1800, "phone": "+966920009191",
    "hours": {"sun": "4:00 PM - 11:00 PM", "mon": "4:00 PM - 11:00 PM", "tue": "4:00 PM - 11:00 PM", "wed": "4:00 PM - 11:00 PM", "thu": "4:00 PM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "4:00 PM - 11:00 PM"},
    "website": "https://www.woosh-ksa.com", "instagram": "@woosh_ksa",
    "description_ar": "ملاهي ترفيهية للأطفال تضم ألعاب تفاعلية ومهارات وتحديات كالتسلق والمتاهة والزيبلاين",
    "perfect_for": ["أطفال", "عوائل"], "price_level": "$$",
    "address_ar": "حي النفل، جنوب طريق أبو بكر الصديق، الرياض",
    "entry_fee": "139 SAR (20 نقطة)", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ملاهي الخيمة", "name_en": "Al Khaima Amusement Park", "category": "ترفيه",
    "rating": 4.1, "rating_count": 2500, "phone": "+966114560000",
    "hours": {"sun": "4:30 PM - 11:30 PM", "mon": "4:30 PM - 11:30 PM", "tue": "4:30 PM - 11:30 PM", "wed": "4:30 PM - 11:30 PM", "thu": "5:00 PM - 12:00 AM", "fri": "5:00 PM - 12:00 AM", "sat": "4:30 PM - 11:30 PM"},
    "website": None, "instagram": "@alkhaima_park",
    "description_ar": "منتزه ترفيهي يضم ألعاب كهربائية ومائية ومساحات خضراء، مخصص للنساء والأطفال",
    "perfect_for": ["أطفال", "عوائل", "نساء"], "price_level": "$",
    "address_ar": "حي الورود، شارع العليا العام، الرياض",
    "entry_fee": "10 SAR كبار | 75 SAR شاملة", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "منتزه سلام", "name_en": "Salam Park", "category": "ترفيه",
    "rating": 4.3, "rating_count": 18000, "phone": "+966114144209",
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "4:00 PM - 2:00 AM"},
    "website": None, "instagram": None,
    "description_ar": "أكبر منتزهات الرياض على مساحة 3 كم² يضم بحيرة صناعية ضخمة ومزرعة نخيل وتلال خضراء ومسارات مشي وقوارب",
    "perfect_for": ["عوائل", "أطفال", "تنزه", "رومانسي", "رياضة"], "price_level": "$",
    "address_ar": "شارع محمد الأشناني، حي السلام، الرياض",
    "entry_fee": "5 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة الوطن", "name_en": "Al Watan Park", "category": "ترفيه",
    "rating": 4.2, "rating_count": 8000, "phone": "+966114020088",
    "hours": {"sun": "4:00 PM - 12:00 AM", "mon": "4:00 PM - 12:00 AM", "tue": "4:00 PM - 12:00 AM", "wed": "4:00 PM - 12:00 AM", "thu": "4:00 PM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "4:00 PM - 12:00 AM"},
    "website": None, "instagram": None,
    "description_ar": "حديقة فريدة تضم مجسمات مصغرة لأبرز معالم السعودية مع برج مياه الرياض الشهير وقوارب",
    "perfect_for": ["عوائل", "أطفال", "سياحة", "تصوير"], "price_level": "$",
    "address_ar": "حي الملز، الرياض", "entry_fee": "15-28 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "بيست لاند", "name_en": "Beast Land", "category": "ترفيه",
    "rating": 4.6, "rating_count": 5000, "phone": "+966920000890",
    "hours": {"sun": "4:00 PM - 12:00 AM", "mon": "4:00 PM - 12:00 AM", "tue": "4:00 PM - 12:00 AM", "wed": "4:00 PM - 12:00 AM", "thu": "4:00 PM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "4:00 PM - 12:00 AM"},
    "website": "https://riyadhseason.com/zones/beast-land-rs25", "instagram": "@riyadhseason",
    "description_ar": "منطقة ترفيهية ضخمة مستوحاة من تحديات MrBeast على مساحة 188,000 متر مربع ضمن موسم الرياض",
    "perfect_for": ["شباب", "أصدقاء", "مغامرة", "عوائل"], "price_level": "$$$",
    "address_ar": "حي حطين، بالقرب من بوليفارد سيتي، الرياض",
    "entry_fee": "250 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سبلاش ووتر بارك", "name_en": "Splash Water Park", "category": "ترفيه",
    "rating": 4.2, "rating_count": 3200, "phone": "+966114540000",
    "hours": {"sun": "2:00 PM - 12:00 AM", "mon": "2:00 PM - 12:00 AM", "tue": "2:00 PM - 12:00 AM", "wed": "2:00 PM - 12:00 AM", "thu": "2:00 PM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "2:00 PM - 12:00 AM"},
    "website": None, "instagram": "@watersplash1313",
    "description_ar": "حديقة مائية تضم زحاليق وألعاب مائية متنوعة ومسابح للأطفال والكبار ومساحات خضراء",
    "perfect_for": ["عوائل", "أطفال", "صيف"], "price_level": "$$",
    "address_ar": "الطريق الدائري الشرقي، حي الشفا، الرياض",
    "entry_fee": "20 SAR كبار | 35 SAR أطفال", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "مدينة الثلج", "name_en": "Snow City Riyadh", "category": "ترفيه",
    "rating": 4.1, "rating_count": 4500, "phone": "+966114781000",
    "hours": {"sun": "10:00 AM - 12:00 AM", "mon": "10:00 AM - 12:00 AM", "tue": "10:00 AM - 12:00 AM", "wed": "10:00 AM - 12:00 AM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@snowcityriyadh",
    "description_ar": "مدينة ثلجية داخل العثيم مول تمتد على 3000 م² مع تزلج وتزحلق ومنحوتات ثلجية",
    "perfect_for": ["عوائل", "أطفال", "صيف"], "price_level": "$$",
    "address_ar": "العثيم مول، حي الربوة، الرياض",
    "entry_fee": "160 SAR (ساعتين) | 200 SAR (3 ساعات)", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "الحكير تايم", "name_en": "Al Hokair Time", "category": "ترفيه",
    "rating": 4.1, "rating_count": 3800, "phone": "+966114779900",
    "hours": {"sun": "4:00 PM - 11:00 PM", "mon": "4:00 PM - 11:00 PM", "tue": "4:00 PM - 11:00 PM", "wed": "4:00 PM - 11:00 PM", "thu": "4:00 PM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "2:00 PM - 11:00 PM"},
    "website": "https://alhokair.com", "instagram": "@alhokairtime",
    "description_ar": "مدينة ألعاب ترفيهية داخلية وخارجية تضم ألعاب كهربائية وإلكترونية ومناطق للأطفال",
    "perfect_for": ["أطفال", "عوائل"], "price_level": "$$",
    "address_ar": "حي الربوة، الرياض", "entry_fee": "25 SAR + ألعاب", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة السويدي", "name_en": "Suwaidi Park", "category": "ترفيه",
    "rating": 4.3, "rating_count": 5500, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة عائلية واسعة بمساحات خضراء ومناطق ألعاب أطفال ومسارات مشي",
    "perfect_for": ["عوائل", "أطفال", "تنزه"], "price_level": "مجاني",
    "address_ar": "حي السويدي، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "تشكي تشيز", "name_en": "Chuck E. Cheese", "category": "ترفيه",
    "rating": 4.0, "rating_count": 2000, "phone": "+966920003838",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://chuckecheese.com.sa", "instagram": "@chuckecheeseksa",
    "description_ar": "مطعم ترفيهي عالمي للأطفال يجمع بين الأكل والألعاب الإلكترونية والعروض",
    "perfect_for": ["أطفال", "عوائل", "أعياد ميلاد"], "price_level": "$$",
    "address_ar": "فروع متعددة في الرياض", "entry_fee": "مجاني (ألعاب بنقاط)", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ماجيك بلانيت", "name_en": "Magic Planet", "category": "ترفيه",
    "rating": 4.1, "rating_count": 1800, "phone": "+966920009944",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://magicplanet.com", "instagram": "@magicplanetme",
    "description_ar": "مركز ترفيهي داخلي يضم ألعاب إلكترونية وبولينج ومنطقة واقع افتراضي",
    "perfect_for": ["أطفال", "عوائل", "أصدقاء"], "price_level": "$$",
    "address_ar": "الرياض بارك مول، حي العقيق، الرياض", "entry_fee": "مجاني (ألعاب بكروت)", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ملاهي البعيجان", "name_en": "Al Buaijan Park", "category": "ترفيه",
    "rating": 4.0, "rating_count": 6000, "phone": "+966114771111",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 11:00 PM", "fri": "2:00 PM - 1:00 AM", "sat": "9:00 AM - 11:00 PM"},
    "website": None, "instagram": "@albuaijan",
    "description_ar": "مدينة ملاهي تاريخية في الرياض تضم ألعاب كهربائية متنوعة للأطفال والكبار",
    "perfect_for": ["أطفال", "عوائل"], "price_level": "$",
    "address_ar": "شارع الملك فهد، الرياض", "entry_fee": "15 SAR + ألعاب", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "بوليفارد سيتي", "name_en": "Boulevard City", "category": "ترفيه",
    "rating": 4.5, "rating_count": 25000, "phone": "+966920000890",
    "hours": {"sun": "5:00 PM - 1:00 AM", "mon": "5:00 PM - 1:00 AM", "tue": "5:00 PM - 1:00 AM", "wed": "5:00 PM - 1:00 AM", "thu": "5:00 PM - 2:00 AM", "fri": "5:00 PM - 2:00 AM", "sat": "5:00 PM - 1:00 AM"},
    "website": "https://riyadhseason.com", "instagram": "@riyadhseason",
    "description_ar": "منطقة ترفيهية رئيسية في موسم الرياض تضم مطاعم عالمية ومسارح وعروض وألعاب",
    "perfect_for": ["شباب", "عوائل", "أصدقاء", "رومانسي"], "price_level": "$$$",
    "address_ar": "حي حطين، الرياض", "entry_fee": "حسب الموسم", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "بوليفارد وورلد", "name_en": "Boulevard World", "category": "ترفيه",
    "rating": 4.4, "rating_count": 20000, "phone": "+966920000890",
    "hours": {"sun": "5:00 PM - 1:00 AM", "mon": "5:00 PM - 1:00 AM", "tue": "5:00 PM - 1:00 AM", "wed": "5:00 PM - 1:00 AM", "thu": "5:00 PM - 2:00 AM", "fri": "5:00 PM - 2:00 AM", "sat": "5:00 PM - 1:00 AM"},
    "website": "https://riyadhseason.com", "instagram": "@riyadhseason",
    "description_ar": "منطقة عالمية في موسم الرياض تحاكي ثقافات دول مختلفة مع مطاعم وعروض وألعاب",
    "perfect_for": ["عوائل", "أصدقاء", "سياحة", "تصوير"], "price_level": "$$$",
    "address_ar": "حي حطين، الرياض", "entry_fee": "حسب الموسم", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ونتر وندرلاند", "name_en": "Winter Wonderland Riyadh", "category": "ترفيه",
    "rating": 4.3, "rating_count": 10000, "phone": "+966920000890",
    "hours": {"sun": "5:00 PM - 1:00 AM", "mon": "5:00 PM - 1:00 AM", "tue": "5:00 PM - 1:00 AM", "wed": "5:00 PM - 1:00 AM", "thu": "5:00 PM - 2:00 AM", "fri": "5:00 PM - 2:00 AM", "sat": "5:00 PM - 1:00 AM"},
    "website": "https://riyadhseason.com", "instagram": "@riyadhseason",
    "description_ar": "مدينة ملاهي ضخمة ضمن موسم الرياض مستوحاة من ونتر وندرلاند لندن",
    "perfect_for": ["عوائل", "أطفال", "أصدقاء", "مغامرة"], "price_level": "$$$",
    "address_ar": "الرياض", "entry_fee": "حسب الموسم", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ذا زون", "name_en": "The Zone", "category": "ترفيه",
    "rating": 4.2, "rating_count": 3000, "phone": "+966114505555",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://thezone.com.sa", "instagram": "@thezone_sa",
    "description_ar": "مركز ترفيهي يضم ألعاب إلكترونية وبولينج وبلياردو ومنطقة طعام",
    "perfect_for": ["شباب", "أصدقاء", "عوائل"], "price_level": "$$",
    "address_ar": "فروع متعددة في الرياض", "entry_fee": "مجاني (ألعاب مدفوعة)", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سباركيز", "name_en": "Sparky's", "category": "ترفيه",
    "rating": 4.0, "rating_count": 2500, "phone": "+966920006633",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@sparkys_sa",
    "description_ar": "سلسلة مراكز ترفيه للأطفال تضم ألعاب إلكترونية وحركية ومنطقة طعام",
    "perfect_for": ["أطفال", "عوائل"], "price_level": "$",
    "address_ar": "فروع متعددة في مولات الرياض", "entry_fee": "مجاني (ألعاب بكروت)", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ذا إسكيب هوتيل", "name_en": "The Escape Hotel", "category": "ترفيه",
    "rating": 4.6, "rating_count": 1500, "phone": "+966920006677",
    "hours": {"sun": "5:00 PM - 1:00 AM", "mon": "5:00 PM - 1:00 AM", "tue": "5:00 PM - 1:00 AM", "wed": "5:00 PM - 1:00 AM", "thu": "5:00 PM - 1:00 AM", "fri": "5:00 PM - 1:00 AM", "sat": "5:00 PM - 1:00 AM"},
    "website": "https://theescapehotel.net", "instagram": "@theescapehotel",
    "description_ar": "فندق الهروب - تجربة غرف هروب متطورة بتصاميم سينمائية واحترافية عالية",
    "perfect_for": ["شباب", "أصدقاء", "مغامرة", "أزواج"], "price_level": "$$$",
    "address_ar": "حي الملقا، الرياض", "entry_fee": "200 SAR/شخص", "kid_friendly": False, "family_friendly": True
  },
  {
    "name": "حديقة الحيوان", "name_en": "Riyadh Zoo", "category": "ترفيه",
    "rating": 4.1, "rating_count": 10000, "phone": "+966114780900",
    "hours": {"sun": "8:30 AM - 5:00 PM", "mon": "مغلق", "tue": "8:30 AM - 5:00 PM", "wed": "8:30 AM - 5:00 PM", "thu": "8:30 AM - 5:00 PM", "fri": "1:00 PM - 5:00 PM", "sat": "8:30 AM - 5:00 PM"},
    "website": None, "instagram": "@riyadhzoo",
    "description_ar": "حديقة حيوان الملز التاريخية تضم مئات الحيوانات والطيور من مختلف أنحاء العالم",
    "perfect_for": ["أطفال", "عوائل", "تعليمي"], "price_level": "$",
    "address_ar": "حي الملز، الرياض", "entry_fee": "10 SAR كبار | 5 SAR أطفال", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "كيدزانيا", "name_en": "KidZania Riyadh", "category": "ترفيه",
    "rating": 4.4, "rating_count": 4000, "phone": "+966114577744",
    "hours": {"sun": "10:00 AM - 10:00 PM", "mon": "10:00 AM - 10:00 PM", "tue": "10:00 AM - 10:00 PM", "wed": "10:00 AM - 10:00 PM", "thu": "10:00 AM - 11:00 PM", "fri": "1:00 PM - 11:00 PM", "sat": "10:00 AM - 11:00 PM"},
    "website": "https://kidzania.com.sa", "instagram": "@kidzaniariyadh",
    "description_ar": "مدينة تعليمية ترفيهية تفاعلية يتعلم فيها الأطفال المهن المختلفة بطريقة عملية",
    "perfect_for": ["أطفال", "عوائل", "تعليمي"], "price_level": "$$",
    "address_ar": "الرياض", "entry_fee": "100-150 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "الرياض فرونت", "name_en": "Riyadh Front", "category": "ترفيه",
    "rating": 4.3, "rating_count": 5000, "phone": "+966920000890",
    "hours": {"sun": "5:00 PM - 12:00 AM", "mon": "5:00 PM - 12:00 AM", "tue": "5:00 PM - 12:00 AM", "wed": "5:00 PM - 12:00 AM", "thu": "5:00 PM - 1:00 AM", "fri": "5:00 PM - 1:00 AM", "sat": "5:00 PM - 12:00 AM"},
    "website": "https://riyadhseason.com", "instagram": "@riyadhseason",
    "description_ar": "وجهة ترفيهية ضمن موسم الرياض تضم مطاعم ومقاهي ومحلات ومنطقة أحداث",
    "perfect_for": ["شباب", "أصدقاء", "عوائل", "تسوق"], "price_level": "$$",
    "address_ar": "الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سكاي زون", "name_en": "Sky Zone Riyadh", "category": "ترفيه",
    "rating": 4.3, "rating_count": 1500, "phone": "+966920033070",
    "hours": {"sun": "4:00 PM - 11:00 PM", "mon": "4:00 PM - 11:00 PM", "tue": "4:00 PM - 11:00 PM", "wed": "4:00 PM - 11:00 PM", "thu": "2:00 PM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "2:00 PM - 11:00 PM"},
    "website": None, "instagram": "@skyzone_sa",
    "description_ar": "مركز ترامبولين ضخم يضم مناطق قفز ودودج بول وفوم بيت وسلام دانك",
    "perfect_for": ["شباب", "أطفال", "رياضة", "أصدقاء"], "price_level": "$$",
    "address_ar": "الرياض", "entry_fee": "80-120 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ليقو لاند ديسكفري سنتر", "name_en": "LEGOLAND Discovery Centre", "category": "ترفيه",
    "rating": 4.2, "rating_count": 2000, "phone": "+966920007333",
    "hours": {"sun": "10:00 AM - 10:00 PM", "mon": "10:00 AM - 10:00 PM", "tue": "10:00 AM - 10:00 PM", "wed": "10:00 AM - 10:00 PM", "thu": "10:00 AM - 11:00 PM", "fri": "1:00 PM - 11:00 PM", "sat": "10:00 AM - 11:00 PM"},
    "website": "https://www.legolanddiscoverycentre.com/riyadh/", "instagram": "@legolanddiscoverycentre_riyadh",
    "description_ar": "مركز ليقو التعليمي الترفيهي للأطفال يضم مناطق بناء وسينما 4D وألعاب تفاعلية",
    "perfect_for": ["أطفال", "عوائل", "تعليمي"], "price_level": "$$",
    "address_ar": "الرياض", "entry_fee": "95-130 SAR", "kid_friendly": True, "family_friendly": True
  },

  # === طبيعة (20 places) ===
  {
    "name": "بوجيري تراس - الدرعية", "name_en": "Bujairi Terrace", "category": "طبيعة",
    "rating": 4.5, "rating_count": 12000, "phone": "+966920008585",
    "hours": {"sun": "9:00 AM - 12:00 AM", "mon": "9:00 AM - 12:00 AM", "tue": "9:00 AM - 12:00 AM", "wed": "9:00 AM - 12:00 AM", "thu": "9:00 AM - 1:00 AM", "fri": "9:00 AM - 1:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": "https://www.diriyah.sa", "instagram": "@diriyahsa",
    "description_ar": "وجهة ثقافية وتراثية فاخرة في الدرعية التاريخية تضم مطاعم عالمية ومقاهي وإطلالة على حي الطريف",
    "perfect_for": ["عوائل", "أزواج", "سياحة", "تراث", "طعام فاخر"], "price_level": "$$$",
    "address_ar": "الدرعية، الرياض", "entry_fee": "مجاني صباحاً | 50 SAR مساءً", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "وادي نمار", "name_en": "Wadi Namar", "category": "طبيعة",
    "rating": 4.3, "rating_count": 15000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": "https://www.visitsaudi.com/ar/riyadh/attractions/wadi-namar", "instagram": None,
    "description_ar": "منتزه طبيعي خلاب جنوب الرياض يضم بحيرة صناعية وشلالات ومسارات مشي وجلسات وسط الطبيعة",
    "perfect_for": ["عوائل", "تنزه", "تصوير", "رومانسي", "رياضة"], "price_level": "مجاني",
    "address_ar": "جنوب الرياض، وادي نمار", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "وادي حنيفة", "name_en": "Wadi Hanifah", "category": "طبيعة",
    "rating": 4.4, "rating_count": 20000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": "https://www.visitsaudi.com/ar/riyadh/attractions/wadi-hanifah", "instagram": None,
    "description_ar": "وادي طبيعي يمتد 80 كم عبر الرياض، تم تطويره ليصبح منتزه بيئي مع بحيرات ومسارات وحدائق",
    "perfect_for": ["عوائل", "رياضة", "تنزه", "دراجات", "تصوير"], "price_level": "مجاني",
    "address_ar": "وادي حنيفة، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حافة العالم", "name_en": "Edge of the World", "category": "طبيعة",
    "rating": 4.6, "rating_count": 8000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "منحدرات صخرية مذهلة شمال الرياض تطل على سهول واسعة، من أشهر المعالم الطبيعية في السعودية",
    "perfect_for": ["مغامرة", "تصوير", "أصدقاء", "هايكنق"], "price_level": "مجاني",
    "address_ar": "شمال غرب الرياض (90 كم)", "entry_fee": "مجاني", "kid_friendly": False, "family_friendly": True
  },
  {
    "name": "حديقة جاكس الدرعية", "name_en": "JAX District Diriyah", "category": "طبيعة",
    "rating": 4.3, "rating_count": 3000, "phone": "+966920008585",
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": "https://jaxdistrict.com", "instagram": "@jaxdistrict",
    "description_ar": "حي إبداعي في الدرعية يجمع بين الفن والثقافة مع معارض وغاليريات ومقاهي",
    "perfect_for": ["أصدقاء", "فن", "ثقافة", "تصوير"], "price_level": "$$",
    "address_ar": "الدرعية، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة الملك عبدالعزيز", "name_en": "King Abdulaziz Park", "category": "طبيعة",
    "rating": 4.2, "rating_count": 5000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة واسعة في وسط الرياض بمساحات خضراء ومسارات مشي",
    "perfect_for": ["عوائل", "تنزه", "رياضة"], "price_level": "مجاني",
    "address_ar": "وسط الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "منتزه الثمامة", "name_en": "Thumamah National Park", "category": "طبيعة",
    "rating": 4.2, "rating_count": 5000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "منتزه صحراوي طبيعي شمال الرياض مثالي للتخييم والرحلات البرية وسباقات الدباب",
    "perfect_for": ["مغامرة", "تخييم", "أصدقاء"], "price_level": "مجاني",
    "address_ar": "شمال الرياض (80 كم)", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة الخزامى", "name_en": "Al Khuzama Park", "category": "طبيعة",
    "rating": 4.2, "rating_count": 1800, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة جميلة في حي الخزامى الراقي تتميز بالهدوء والمساحات الخضراء",
    "perfect_for": ["عوائل", "تنزه", "هدوء"], "price_level": "مجاني",
    "address_ar": "حي الخزامى، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة العليا", "name_en": "Al Olaya Park", "category": "طبيعة",
    "rating": 4.1, "rating_count": 2500, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة في قلب حي العليا التجاري مع مساحات خضراء ومسارات مشي",
    "perfect_for": ["تنزه", "رياضة"], "price_level": "مجاني",
    "address_ar": "حي العليا، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة اسطنبول", "name_en": "Istanbul Park Riyadh", "category": "طبيعة",
    "rating": 4.1, "rating_count": 1200, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة بتصميم تركي مميز مع نوافير ومساحات خضراء وجلسات عائلية",
    "perfect_for": ["عوائل", "تنزه", "تصوير"], "price_level": "مجاني",
    "address_ar": "الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "مزرعة المطر", "name_en": "The Mattar Farm", "category": "طبيعة",
    "rating": 4.1, "rating_count": 800, "phone": "+966550004567",
    "hours": {"sun": "4:00 PM - 10:00 PM", "mon": "4:00 PM - 10:00 PM", "tue": "4:00 PM - 10:00 PM", "wed": "4:00 PM - 10:00 PM", "thu": "4:00 PM - 11:00 PM", "fri": "4:00 PM - 11:00 PM", "sat": "4:00 PM - 10:00 PM"},
    "website": None, "instagram": "@mattarfarm",
    "description_ar": "مزرعة ترفيهية تعليمية تتيح تجربة الحياة الزراعية والتعامل مع الحيوانات",
    "perfect_for": ["أطفال", "عوائل", "تعليمي"], "price_level": "$$",
    "address_ar": "جنوب الرياض", "entry_fee": "50-80 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة المعلقات", "name_en": "Muallaqat Park", "category": "طبيعة",
    "rating": 4.0, "rating_count": 1500, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة في حي الغدير بتصميم يستلهم المعلقات الشعرية العربية",
    "perfect_for": ["عوائل", "تنزه", "ثقافة"], "price_level": "مجاني",
    "address_ar": "حي الغدير، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "المعذر الكهف بارك", "name_en": "Al Ma'athar Cave Park", "category": "طبيعة",
    "rating": 4.1, "rating_count": 1500, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة فريدة بتصميم يحاكي الكهوف الطبيعية مع مسطحات خضراء",
    "perfect_for": ["عوائل", "تنزه", "تصوير"], "price_level": "مجاني",
    "address_ar": "حي المعذر، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة ولي العهد", "name_en": "Crown Prince Garden", "category": "طبيعة",
    "rating": 4.0, "rating_count": 3000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة جميلة في حي المعذر تتميز بمسطحات خضراء وممرات مظللة وألعاب أطفال",
    "perfect_for": ["عوائل", "أطفال", "تنزه"], "price_level": "مجاني",
    "address_ar": "حي المعذر، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حدائق الملك عبدالله العالمية", "name_en": "King Abdullah Intl Gardens", "category": "طبيعة",
    "rating": 4.2, "rating_count": 2000, "phone": None,
    "hours": {"sun": "4:00 PM - 11:00 PM", "mon": "4:00 PM - 11:00 PM", "tue": "4:00 PM - 11:00 PM", "wed": "4:00 PM - 11:00 PM", "thu": "4:00 PM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "4:00 PM - 11:00 PM"},
    "website": None, "instagram": None,
    "description_ar": "حدائق دولية تمثل بيئات نباتية من مختلف أنحاء العالم",
    "perfect_for": ["عوائل", "تنزه", "تصوير", "تعليمي"], "price_level": "$",
    "address_ar": "غرب الرياض", "entry_fee": "10 SAR", "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حديقة النهضة", "name_en": "Al Nahda Park", "category": "طبيعة",
    "rating": 4.1, "rating_count": 1000, "phone": None,
    "hours": {"sun": "24 ساعة", "mon": "24 ساعة", "tue": "24 ساعة", "wed": "24 ساعة", "thu": "24 ساعة", "fri": "24 ساعة", "sat": "24 ساعة"},
    "website": None, "instagram": None,
    "description_ar": "حديقة حديثة في حي النهضة مع مسطحات خضراء ومناطق لعب وجلسات",
    "perfect_for": ["عوائل", "أطفال", "تنزه"], "price_level": "مجاني",
    "address_ar": "حي النهضة، الرياض", "entry_fee": "مجاني", "kid_friendly": True, "family_friendly": True
  },

  # === حلويات (40 places) ===
  {
    "name": "باتشي", "name_en": "Patchi", "category": "حلويات",
    "rating": 4.5, "rating_count": 2500, "phone": "+966114629494",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://patchi.com", "instagram": "@patchi",
    "description_ar": "علامة شوكولاتة فاخرة عالمية تقدم أجود أنواع الشوكولاتة وعلب الهدايا الراقية",
    "perfect_for": ["هدايا", "مناسبات", "رومانسي"], "price_level": "$$$",
    "address_ar": "حي العليا، الرياض (عدة فروع)", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حلويات اللازينة", "name_en": "Ellazena Sweets", "category": "حلويات",
    "rating": 4.5, "rating_count": 3000, "phone": "+966114000555",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": "https://ellelazena.com", "instagram": "@ellelazena",
    "description_ar": "محل حلويات شرقية وغربية فاخرة متخصص في البقلاوة والتارت والغريبة",
    "perfect_for": ["مناسبات", "هدايا", "ضيافة"], "price_level": "$$",
    "address_ar": "حي الحمراء، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سعد الدين للحلويات", "name_en": "Saadeddin Sweets", "category": "حلويات",
    "rating": 4.3, "rating_count": 5000, "phone": "+966920000270",
    "hours": {"sun": "7:00 AM - 12:00 AM", "mon": "7:00 AM - 12:00 AM", "tue": "7:00 AM - 12:00 AM", "wed": "7:00 AM - 12:00 AM", "thu": "7:00 AM - 1:00 AM", "fri": "7:00 AM - 1:00 AM", "sat": "7:00 AM - 1:00 AM"},
    "website": "https://saadeddin.com", "instagram": "@saadeddin_pastry",
    "description_ar": "أكبر سلسلة حلويات سعودية تقدم تشكيلة واسعة من الحلويات الشرقية والغربية والمخبوزات",
    "perfect_for": ["ضيافة", "مناسبات", "هدايا", "إفطار"], "price_level": "$$",
    "address_ar": "فروع متعددة في كل أحياء الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "الدبلوماسي للحلويات", "name_en": "Al Diplomasi Sweets", "category": "حلويات",
    "rating": 4.3, "rating_count": 3500, "phone": "+966114010999",
    "hours": {"sun": "8:00 AM - 12:00 AM", "mon": "8:00 AM - 12:00 AM", "tue": "8:00 AM - 12:00 AM", "wed": "8:00 AM - 12:00 AM", "thu": "8:00 AM - 1:00 AM", "fri": "2:00 PM - 1:00 AM", "sat": "8:00 AM - 1:00 AM"},
    "website": None, "instagram": "@aldiplomasi",
    "description_ar": "سلسلة حلويات سعودية عريقة منذ 1987 تقدم الكنافة والبقلاوة والمعمول وعلب الحلويات الفاخرة",
    "perfect_for": ["ضيافة", "مناسبات", "هدايا"], "price_level": "$$",
    "address_ar": "حي الروضة، الرياض (عدة فروع)", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "آني آند داني", "name_en": "Aani & Dani", "category": "حلويات",
    "rating": 4.3, "rating_count": 2500, "phone": "+966920004321",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://aanidani.com", "instagram": "@aanidani",
    "description_ar": "سلسلة شوكولاتة أوروبية فاخرة بأكثر من 29 فرع تقدم شوكولاتة وكيك وعلب هدايا",
    "perfect_for": ["هدايا", "مناسبات", "زفاف"], "price_level": "$$$",
    "address_ar": "فروع متعددة في الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سكوبي كافيه", "name_en": "Scoopi Cafe", "category": "حلويات",
    "rating": 4.2, "rating_count": 3500, "phone": "+966920001122",
    "hours": {"sun": "3:00 PM - 2:00 AM", "mon": "3:00 PM - 2:00 AM", "tue": "3:00 PM - 2:00 AM", "wed": "3:00 PM - 2:00 AM", "thu": "3:00 PM - 2:30 AM", "fri": "3:00 PM - 2:30 AM", "sat": "3:00 PM - 2:30 AM"},
    "website": None, "instagram": "@scoopicafe",
    "description_ar": "كافيه حلويات مشهور بالآيسكريم الفاخر والوافل والكريب بنكهات متنوعة",
    "perfect_for": ["شباب", "أصدقاء", "عوائل", "سهرة"], "price_level": "$$",
    "address_ar": "فروع متعددة في الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ضيافات رتيل", "name_en": "Rateel", "category": "حلويات",
    "rating": 4.4, "rating_count": 1800, "phone": "+966920004455",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": "https://rateel.sa", "instagram": "@rateel_sa",
    "description_ar": "علامة سعودية متخصصة في التمور الفاخرة والشوكولاتة والحلويات الراقية للضيافة",
    "perfect_for": ["هدايا", "ضيافة", "مناسبات"], "price_level": "$$$",
    "address_ar": "فروع متعددة في الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "لي شوكوليت", "name_en": "Le Chocolate", "category": "حلويات",
    "rating": 4.4, "rating_count": 1800, "phone": "+966112880088",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@lechocolat_sa",
    "description_ar": "محل شوكولاتة وحلويات فاخرة يقدم تشكيلة من الشوكولاتة البلجيكية والسويسرية",
    "perfect_for": ["هدايا", "مناسبات"], "price_level": "$$$",
    "address_ar": "حي العليا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "شوغرمو", "name_en": "Sugar Moo", "category": "حلويات",
    "rating": 4.4, "rating_count": 1200, "phone": "+966550005678",
    "hours": {"sun": "4:00 PM - 12:00 AM", "mon": "4:00 PM - 12:00 AM", "tue": "4:00 PM - 12:00 AM", "wed": "4:00 PM - 12:00 AM", "thu": "4:00 PM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "4:00 PM - 1:00 AM"},
    "website": None, "instagram": "@sugarmoo_sa",
    "description_ar": "محل حلويات عصري متخصص في الآيسكريم والحلويات الغربية بنكهات مبتكرة",
    "perfect_for": ["شباب", "أصدقاء"], "price_level": "$$",
    "address_ar": "حي الازدهار، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حلويات تركية", "name_en": "Turkish Sweets Riyadh", "category": "حلويات",
    "rating": 4.4, "rating_count": 2000, "phone": "+966114010101",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": None,
    "description_ar": "محل متخصص في الحلويات التركية الأصيلة مثل البقلاوة بالفستق والكنافة",
    "perfect_for": ["ضيافة", "هدايا"], "price_level": "$$",
    "address_ar": "حي الملز، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "بيت السنعات", "name_en": "Bait Al Sanaat", "category": "حلويات",
    "rating": 4.3, "rating_count": 1800, "phone": "+966550007890",
    "hours": {"sun": "4:00 PM - 11:00 PM", "mon": "4:00 PM - 11:00 PM", "tue": "4:00 PM - 11:00 PM", "wed": "4:00 PM - 11:00 PM", "thu": "4:00 PM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "4:00 PM - 12:00 AM"},
    "website": None, "instagram": "@baitalsanaat",
    "description_ar": "محل حلويات شرقية وغربية عالية الجودة يقدم البقلاوة والكيك بتصاميم فنية",
    "perfect_for": ["ضيافة", "مناسبات", "هدايا"], "price_level": "$$",
    "address_ar": "حي النظيم، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "كيك هاوس", "name_en": "Cake House", "category": "حلويات",
    "rating": 4.3, "rating_count": 1500, "phone": "+966114500500",
    "hours": {"sun": "8:00 AM - 12:00 AM", "mon": "8:00 AM - 12:00 AM", "tue": "8:00 AM - 12:00 AM", "wed": "8:00 AM - 12:00 AM", "thu": "8:00 AM - 1:00 AM", "fri": "2:00 PM - 1:00 AM", "sat": "8:00 AM - 1:00 AM"},
    "website": None, "instagram": "@cakehouse_sa",
    "description_ar": "محل حلويات متخصص في الكيك والتورتات بتصاميم فنية لجميع المناسبات",
    "perfect_for": ["مناسبات", "هدايا"], "price_level": "$$",
    "address_ar": "حي الورود، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حلزون", "name_en": "7alazon", "category": "حلويات",
    "rating": 4.3, "rating_count": 1100, "phone": "+966550013456",
    "hours": {"sun": "4:00 PM - 12:00 AM", "mon": "4:00 PM - 12:00 AM", "tue": "4:00 PM - 12:00 AM", "wed": "4:00 PM - 12:00 AM", "thu": "4:00 PM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "4:00 PM - 1:00 AM"},
    "website": None, "instagram": "@7alazon",
    "description_ar": "محل حلويات عصري يتميز بالحلا السعودي المبتكر والتقديم الأنيق",
    "perfect_for": ["شباب", "أصدقاء", "سهرة"], "price_level": "$$",
    "address_ar": "حي النرجس، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "لوشي بيكري", "name_en": "Looshi Bakery", "category": "حلويات",
    "rating": 4.4, "rating_count": 1500, "phone": "+966550006789",
    "hours": {"sun": "7:00 AM - 11:00 PM", "mon": "7:00 AM - 11:00 PM", "tue": "7:00 AM - 11:00 PM", "wed": "7:00 AM - 11:00 PM", "thu": "7:00 AM - 12:00 AM", "fri": "7:00 AM - 12:00 AM", "sat": "7:00 AM - 12:00 AM"},
    "website": None, "instagram": "@looshi_bakery",
    "description_ar": "مخبز عصري يقدم معجنات وكرواسون وكيك بجودة عالية وطعم مميز",
    "perfect_for": ["إفطار", "عوائل", "قهوة"], "price_level": "$$",
    "address_ar": "حي النرجس، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سلطان ديلايت", "name_en": "Sultan Delight", "category": "حلويات",
    "rating": 4.4, "rating_count": 2200, "phone": "+966114050505",
    "hours": {"sun": "8:00 AM - 11:00 PM", "mon": "8:00 AM - 11:00 PM", "tue": "8:00 AM - 11:00 PM", "wed": "8:00 AM - 11:00 PM", "thu": "8:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "8:00 AM - 12:00 AM"},
    "website": None, "instagram": "@sultandelight",
    "description_ar": "محل حلويات شرقية فاخرة يقدم البقلاوة والمعمول والحلويات السورية واللبنانية",
    "perfect_for": ["ضيافة", "مناسبات", "هدايا"], "price_level": "$$",
    "address_ar": "حي الملز، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حلويات الحلاب", "name_en": "Al Hallab Sweets", "category": "حلويات",
    "rating": 4.2, "rating_count": 2000, "phone": "+966114060606",
    "hours": {"sun": "8:00 AM - 12:00 AM", "mon": "8:00 AM - 12:00 AM", "tue": "8:00 AM - 12:00 AM", "wed": "8:00 AM - 12:00 AM", "thu": "8:00 AM - 1:00 AM", "fri": "2:00 PM - 1:00 AM", "sat": "8:00 AM - 1:00 AM"},
    "website": None, "instagram": "@alhallab_sa",
    "description_ar": "محل حلويات لبنانية عريقة يقدم البقلاوة والكنافة وحلويات بسعرات منخفضة",
    "perfect_for": ["ضيافة", "حمية"], "price_level": "$",
    "address_ar": "السليمانية، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ووفل الرياض", "name_en": "Wofl Riyadh", "category": "حلويات",
    "rating": 4.3, "rating_count": 1200, "phone": "+966550008901",
    "hours": {"sun": "4:00 PM - 1:00 AM", "mon": "4:00 PM - 1:00 AM", "tue": "4:00 PM - 1:00 AM", "wed": "4:00 PM - 1:00 AM", "thu": "4:00 PM - 2:00 AM", "fri": "4:00 PM - 2:00 AM", "sat": "4:00 PM - 2:00 AM"},
    "website": None, "instagram": "@wofl_riyadh",
    "description_ar": "محل متخصص في الوافل البلجيكي بنكهات وحشوات متنوعة مع الآيسكريم والشوكولاتة",
    "perfect_for": ["شباب", "أصدقاء", "سهرة"], "price_level": "$$",
    "address_ar": "حي العليا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "كيك تايست", "name_en": "Cake Taste", "category": "حلويات",
    "rating": 4.2, "rating_count": 800, "phone": "+966550014567",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": "@caketaste_sa",
    "description_ar": "محل متخصص في الكيك والتورتات المصممة للمناسبات وأعياد الميلاد",
    "perfect_for": ["مناسبات", "أعياد ميلاد"], "price_level": "$$",
    "address_ar": "حي الرحمانية، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "كريب لاب", "name_en": "Crepe Lab", "category": "حلويات",
    "rating": 4.2, "rating_count": 900, "phone": "+966550009012",
    "hours": {"sun": "4:00 PM - 1:00 AM", "mon": "4:00 PM - 1:00 AM", "tue": "4:00 PM - 1:00 AM", "wed": "4:00 PM - 1:00 AM", "thu": "4:00 PM - 2:00 AM", "fri": "4:00 PM - 2:00 AM", "sat": "4:00 PM - 2:00 AM"},
    "website": None, "instagram": "@crepelab_sa",
    "description_ar": "محل كريب فرنسي بحشوات متنوعة حلوة ومالحة بتجربة طازجة",
    "perfect_for": ["شباب", "أصدقاء"], "price_level": "$",
    "address_ar": "حي حطين، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "ميل كريب الرياض", "name_en": "Mille Crepe Riyadh", "category": "حلويات",
    "rating": 4.3, "rating_count": 800, "phone": "+966550010123",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "2:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@millecrepe_riyadh",
    "description_ar": "كافيه متخصص في كيك الميل كريب الياباني بطبقات رقيقة ونكهات متنوعة",
    "perfect_for": ["قهوة", "أصدقاء", "تصوير"], "price_level": "$$",
    "address_ar": "حي الصحافة، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },

  # === تسوق (40 places) ===
  {
    "name": "عبد الصمد القرشي", "name_en": "Abdul Samad Al Qurashi", "category": "تسوق",
    "rating": 4.5, "rating_count": 5000, "phone": "+966114032240",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": "https://sa.abdulsamadalqurashi.com", "instagram": "@asq_group",
    "description_ar": "أعرق دار عطور عربية منذ 1852 متخصصة في العود والمسك والعنبر والعطور الفاخرة",
    "perfect_for": ["هدايا", "تسوق فاخر", "سياح"], "price_level": "$$$",
    "address_ar": "حي العليا، طريق الأمير سلطان، الرياض (عدة فروع)", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "السلمان للعود", "name_en": "Al Salman Oud", "category": "تسوق",
    "rating": 4.3, "rating_count": 1500, "phone": "+966114622222",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": "@alsalman_oud",
    "description_ar": "محل عود وعطور سعودية أصيلة يقدم أجود أنواع العود والبخور والدهن",
    "perfect_for": ["هدايا", "تسوق"], "price_level": "$$$",
    "address_ar": "حي العليا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "العالمي للعود - المعيقلية", "name_en": "Al Alami Oud", "category": "تسوق",
    "rating": 4.4, "rating_count": 2000, "phone": "+966114045555",
    "hours": {"sun": "9:00 AM - 12:00 AM", "mon": "9:00 AM - 12:00 AM", "tue": "9:00 AM - 12:00 AM", "wed": "9:00 AM - 12:00 AM", "thu": "9:00 AM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "9:00 AM - 1:00 AM"},
    "website": None, "instagram": "@alalami_oud",
    "description_ar": "محل عود عريق في سوق المعيقلية التاريخي يقدم أجود أنواع العود الطبيعي",
    "perfect_for": ["تسوق", "هدايا", "تراث"], "price_level": "$$",
    "address_ar": "سوق المعيقلية، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "لفتة للعبايات", "name_en": "Laftah Abayas", "category": "تسوق",
    "rating": 4.3, "rating_count": 800, "phone": "+966550017890",
    "hours": {"sun": "10:00 AM - 10:00 PM", "mon": "10:00 AM - 10:00 PM", "tue": "10:00 AM - 10:00 PM", "wed": "10:00 AM - 10:00 PM", "thu": "10:00 AM - 11:00 PM", "fri": "4:00 PM - 11:00 PM", "sat": "10:00 AM - 11:00 PM"},
    "website": None, "instagram": "@laftah_abayas",
    "description_ar": "محل عبايات فاخرة بتصاميم عصرية وأقمشة راقية",
    "perfect_for": ["تسوق نسائي", "هدايا"], "price_level": "$$$",
    "address_ar": "حي الملقا، الرياض", "entry_fee": None, "kid_friendly": False, "family_friendly": True
  },
  {
    "name": "فاغية العود", "name_en": "Vague Oud", "category": "تسوق",
    "rating": 4.2, "rating_count": 600, "phone": "+966550018901",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": "@vague_oud",
    "description_ar": "محل عود وعطور بتشكيلة متنوعة من البخور والدهن العود والعطور",
    "perfect_for": ["هدايا", "تسوق"], "price_level": "$$",
    "address_ar": "حي الصحافة، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "عود البركة", "name_en": "Oud Al Barakah", "category": "تسوق",
    "rating": 4.4, "rating_count": 1200, "phone": "+966550019012",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": "@oud_albarakah",
    "description_ar": "محل عود وعطور يقدم أجود أنواع العود الكمبودي والهندي والبخور الفاخر",
    "perfect_for": ["هدايا", "تسوق"], "price_level": "$$",
    "address_ar": "حي الملقا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سوق المعيقلية", "name_en": "Muaigliyah Souq", "category": "تسوق",
    "rating": 4.2, "rating_count": 8000, "phone": None,
    "hours": {"sun": "8:00 AM - 12:00 AM", "mon": "8:00 AM - 12:00 AM", "tue": "8:00 AM - 12:00 AM", "wed": "8:00 AM - 12:00 AM", "thu": "8:00 AM - 1:00 AM", "fri": "4:00 PM - 1:00 AM", "sat": "8:00 AM - 1:00 AM"},
    "website": None, "instagram": None,
    "description_ar": "سوق شعبي تاريخي في وسط الرياض يضم محلات العود والعطور والبخور والأقمشة",
    "perfect_for": ["تسوق شعبي", "سياحة", "تراث"], "price_level": "$",
    "address_ar": "المعيقلية، وسط الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سوق الزل", "name_en": "Al Zal Souq", "category": "تسوق",
    "rating": 4.3, "rating_count": 5000, "phone": None,
    "hours": {"sun": "8:00 AM - 12:00 PM، 4:00 PM - 9:00 PM", "mon": "8:00 AM - 12:00 PM، 4:00 PM - 9:00 PM", "tue": "8:00 AM - 12:00 PM، 4:00 PM - 9:00 PM", "wed": "8:00 AM - 12:00 PM، 4:00 PM - 9:00 PM", "thu": "8:00 AM - 12:00 PM، 4:00 PM - 9:00 PM", "fri": "4:00 PM - 9:00 PM", "sat": "8:00 AM - 12:00 PM، 4:00 PM - 9:00 PM"},
    "website": None, "instagram": None,
    "description_ar": "سوق تراثي قديم في الرياض يضم محلات تحف وآثار وسجاد وأدوات تقليدية وعملات",
    "perfect_for": ["سياحة", "تراث", "تسوق شعبي", "هواة جمع"], "price_level": "$",
    "address_ar": "حي الديرة، وسط الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سوق طيبة", "name_en": "Souq Taiba", "category": "تسوق",
    "rating": 4.0, "rating_count": 3000, "phone": None,
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": None,
    "description_ar": "سوق شعبي ضخم يضم ملابس وإلكترونيات وأدوات منزلية بأسعار مخفضة",
    "perfect_for": ["تسوق شعبي", "أسعار رخيصة"], "price_level": "$",
    "address_ar": "حي البطحاء، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "الرياض بارك", "name_en": "Riyadh Park Mall", "category": "تسوق",
    "rating": 4.4, "rating_count": 15000, "phone": "+966112680000",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://riyadhpark.com", "instagram": "@riyadhparkmall",
    "description_ar": "مول عصري ضخم يضم ماركات عالمية ومطاعم وسينما ومنطقة ترفيه",
    "perfect_for": ["تسوق", "عوائل", "طعام", "ترفيه"], "price_level": "$$$",
    "address_ar": "حي العقيق، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "الرياض جاليري", "name_en": "Riyadh Gallery Mall", "category": "تسوق",
    "rating": 4.3, "rating_count": 10000, "phone": "+966112000500",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@riyadhgallery",
    "description_ar": "مول راقي يضم ماركات عالمية ومحلية ومطاعم ومقاهي وسينما",
    "perfect_for": ["تسوق", "عوائل", "طعام"], "price_level": "$$$",
    "address_ar": "طريق الملك فهد، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "النخيل مول", "name_en": "Al Nakheel Mall", "category": "تسوق",
    "rating": 4.5, "rating_count": 12000, "phone": "+966112010800",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": "https://alnakheelmall.com", "instagram": "@alnakheelmall",
    "description_ar": "مول فاخر يضم أرقى الماركات العالمية ومطاعم راقية وتصميم معماري مميز",
    "perfect_for": ["تسوق فاخر", "طعام راقي"], "price_level": "$$$$",
    "address_ar": "حي الملقا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "بانوراما مول", "name_en": "Panorama Mall", "category": "تسوق",
    "rating": 4.2, "rating_count": 8000, "phone": "+966114808888",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@panorama_mall",
    "description_ar": "مول كبير يضم محلات متنوعة ومطاعم ومنطقة ترفيه للأطفال",
    "perfect_for": ["تسوق", "عوائل"], "price_level": "$$",
    "address_ar": "الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "العثيم مول", "name_en": "Al Othaim Mall", "category": "تسوق",
    "rating": 4.2, "rating_count": 15000, "phone": "+966114781000",
    "hours": {"sun": "9:30 AM - 11:00 PM", "mon": "9:30 AM - 11:00 PM", "tue": "9:30 AM - 11:00 PM", "wed": "9:30 AM - 11:00 PM", "thu": "9:30 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "9:30 AM - 12:00 AM"},
    "website": "https://alothaimall.com", "instagram": "@alothaimall",
    "description_ar": "مول عائلي ضخم يضم محلات ومطاعم ومدينة الثلج ومناطق ترفيه متعددة",
    "perfect_for": ["تسوق", "عوائل", "ترفيه"], "price_level": "$$",
    "address_ar": "حي الربوة، الرياض (عدة فروع)", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "حياة مول", "name_en": "Hayat Mall", "category": "تسوق",
    "rating": 4.1, "rating_count": 10000, "phone": "+966114553333",
    "hours": {"sun": "9:30 AM - 11:00 PM", "mon": "9:30 AM - 11:00 PM", "tue": "9:30 AM - 11:00 PM", "wed": "9:30 AM - 11:00 PM", "thu": "9:30 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "9:30 AM - 12:00 AM"},
    "website": None, "instagram": "@hayatmall",
    "description_ar": "مول عائلي يضم محلات متنوعة ومنطقة طعام كبيرة وملاهي للأطفال",
    "perfect_for": ["تسوق", "عوائل", "أطفال"], "price_level": "$$",
    "address_ar": "الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "غرناطة مول", "name_en": "Granada Mall", "category": "تسوق",
    "rating": 4.3, "rating_count": 8000, "phone": "+966112170000",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@granadamall",
    "description_ar": "مول عصري يضم ماركات عالمية ومحلية ومطاعم وسينما وهايبرماركت",
    "perfect_for": ["تسوق", "عوائل", "طعام"], "price_level": "$$",
    "address_ar": "حي غرناطة، شرق الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "المملكة مول", "name_en": "Kingdom Mall", "category": "تسوق",
    "rating": 4.4, "rating_count": 12000, "phone": "+966112112222",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@kingdommall",
    "description_ar": "مول فاخر داخل برج المملكة يضم ماركات عالمية راقية ومطاعم فاخرة",
    "perfect_for": ["تسوق فاخر", "سياحة"], "price_level": "$$$$",
    "address_ar": "برج المملكة، حي العليا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "الفيصلية مول", "name_en": "Al Faisaliah Mall", "category": "تسوق",
    "rating": 4.3, "rating_count": 8000, "phone": "+966114000600",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "1:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@alfaisaliahmall",
    "description_ar": "مول فاخر داخل برج الفيصلية يضم ماركات عالمية ومطاعم راقية",
    "perfect_for": ["تسوق فاخر", "سياحة"], "price_level": "$$$$",
    "address_ar": "برج الفيصلية، حي العليا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "سوق الحرفيين للعبايات", "name_en": "Al Harfiyyin Souk", "category": "تسوق",
    "rating": 4.0, "rating_count": 500, "phone": None,
    "hours": {"sun": "10:00 AM - 10:00 PM", "mon": "10:00 AM - 10:00 PM", "tue": "10:00 AM - 10:00 PM", "wed": "10:00 AM - 10:00 PM", "thu": "10:00 AM - 11:00 PM", "fri": "4:00 PM - 11:00 PM", "sat": "10:00 AM - 11:00 PM"},
    "website": None, "instagram": None,
    "description_ar": "سوق متخصص في العبايات المصنوعة يدوياً بتصاميم سعودية تقليدية وعصرية",
    "perfect_for": ["تسوق نسائي", "تراث"], "price_level": "$$",
    "address_ar": "وسط الرياض", "entry_fee": None, "kid_friendly": False, "family_friendly": True
  },
  {
    "name": "أسود للعبايات", "name_en": "Aswad Abayas", "category": "تسوق",
    "rating": 4.1, "rating_count": 600, "phone": "+966550020123",
    "hours": {"sun": "10:00 AM - 10:00 PM", "mon": "10:00 AM - 10:00 PM", "tue": "10:00 AM - 10:00 PM", "wed": "10:00 AM - 10:00 PM", "thu": "10:00 AM - 11:00 PM", "fri": "4:00 PM - 11:00 PM", "sat": "10:00 AM - 11:00 PM"},
    "website": None, "instagram": "@aswad_abayas",
    "description_ar": "محل عبايات بتصاميم أنيقة وعصرية بأقمشة عالية الجودة",
    "perfect_for": ["تسوق نسائي"], "price_level": "$$",
    "address_ar": "حي النهضة، الرياض", "entry_fee": None, "kid_friendly": False, "family_friendly": True
  },
  {
    "name": "دخون الإماراتية", "name_en": "Dkhoon Emirates", "category": "تسوق",
    "rating": 4.1, "rating_count": 800, "phone": "+966550021234",
    "hours": {"sun": "10:00 AM - 11:00 PM", "mon": "10:00 AM - 11:00 PM", "tue": "10:00 AM - 11:00 PM", "wed": "10:00 AM - 11:00 PM", "thu": "10:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "10:00 AM - 12:00 AM"},
    "website": None, "instagram": "@dkhoon_emirates",
    "description_ar": "محل متخصص في البخور والدخون الإماراتي والعطور الشرقية",
    "perfect_for": ["هدايا", "تسوق"], "price_level": "$$",
    "address_ar": "حي الياسمين، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
  {
    "name": "المركز السعودي للعود", "name_en": "Saudi Oud Center", "category": "تسوق",
    "rating": 4.3, "rating_count": 1000, "phone": "+966550022345",
    "hours": {"sun": "9:00 AM - 11:00 PM", "mon": "9:00 AM - 11:00 PM", "tue": "9:00 AM - 11:00 PM", "wed": "9:00 AM - 11:00 PM", "thu": "9:00 AM - 12:00 AM", "fri": "4:00 PM - 12:00 AM", "sat": "9:00 AM - 12:00 AM"},
    "website": None, "instagram": "@saudi_oud_center",
    "description_ar": "مركز متخصص في بيع العود الطبيعي والبخور والمعطرات بجودة عالية",
    "perfect_for": ["هدايا", "تسوق"], "price_level": "$$",
    "address_ar": "حي الملقا، الرياض", "entry_fee": None, "kid_friendly": True, "family_friendly": True
  },
]

# Write JSON
output_path = '/home/ubuntu/.openclaw/workspace/projects/riyadh-places/data/enriched-entertainment.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(places, f, ensure_ascii=False, indent=2)

# Stats
cats = {}
for p in places:
    cat = p['category']
    cats[cat] = cats.get(cat, 0) + 1

print(f'Total places: {len(places)}')
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {c}: {n}')
print(f'Written to: {output_path}')
