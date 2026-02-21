#!/usr/bin/env python3
"""Build comprehensive Riyadh neighborhoods database from Wikipedia + existing data + places."""
import json
import re

# Wikipedia neighborhoods organized by municipality (بلدية)
# Source: https://ar.wikipedia.org/wiki/أحياء_الرياض
WIKI_NEIGHBORHOODS = [
    # بلدية الشمال - North Municipality
    {"name_ar": "الربيع", "name_en": "Ar Rabi", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8233, "lng": 46.6497, "character": "سكني راقي"},
    {"name_ar": "الندى", "name_en": "An Nada", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8401, "lng": 46.6298, "character": "سكني"},
    {"name_ar": "الصحافة", "name_en": "As Sahafah", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8106, "lng": 46.6759, "character": "سكني تجاري"},
    {"name_ar": "النرجس", "name_en": "An Narjis", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8560, "lng": 46.6650, "character": "سكني جديد"},
    {"name_ar": "العارض", "name_en": "Al Arid", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8700, "lng": 46.6350, "character": "سكني جديد"},
    {"name_ar": "النفل", "name_en": "An Nafl", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.7950, "lng": 46.6450, "character": "سكني"},
    {"name_ar": "العقيق", "name_en": "Al Aqiq", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.7870, "lng": 46.6270, "character": "سكني راقي"},
    {"name_ar": "الوادي", "name_en": "Al Wadi", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.7750, "lng": 46.6350, "character": "سكني"},
    {"name_ar": "الغدير", "name_en": "Al Ghadir", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8050, "lng": 46.6150, "character": "سكني"},
    {"name_ar": "الياسمين", "name_en": "Al Yasmin", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8280, "lng": 46.6100, "character": "سكني راقي"},
    {"name_ar": "الفلاح", "name_en": "Al Falah", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8000, "lng": 46.6800, "character": "سكني"},
    {"name_ar": "بنبان", "name_en": "Banban", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.9200, "lng": 46.6000, "character": "ضاحية"},
    {"name_ar": "القيروان", "name_en": "Al Qirawan", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8400, "lng": 46.5800, "character": "سكني جديد"},
    {"name_ar": "حطين", "name_en": "Hittin", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.7780, "lng": 46.6050, "character": "سكني راقي"},
    {"name_ar": "الملقا", "name_en": "Al Malqa", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8100, "lng": 46.5950, "character": "سكني راقي"},

    # بلدية الروضة - Rawdah Municipality
    {"name_ar": "الروضة", "name_en": "Ar Rawdah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7200, "lng": 46.7850, "character": "سكني"},
    {"name_ar": "الرمال", "name_en": "Ar Rimal", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7400, "lng": 46.8300, "character": "سكني"},
    {"name_ar": "المونسية", "name_en": "Al Munsiyah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7500, "lng": 46.8100, "character": "سكني"},
    {"name_ar": "قرطبة", "name_en": "Qurtubah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7350, "lng": 46.7700, "character": "سكني تجاري"},
    {"name_ar": "الجنادرية", "name_en": "Al Janadriyah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7800, "lng": 46.8700, "character": "ثقافي"},
    {"name_ar": "القادسية", "name_en": "Al Qadisiyah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7100, "lng": 46.7900, "character": "سكني"},
    {"name_ar": "اليرموك", "name_en": "Al Yarmuk", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7000, "lng": 46.7800, "character": "سكني"},
    {"name_ar": "غرناطة", "name_en": "Ghirnatah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7250, "lng": 46.7600, "character": "سكني تجاري"},
    {"name_ar": "إشبيلية", "name_en": "Ishbiliyah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7150, "lng": 46.7500, "character": "سكني"},
    {"name_ar": "الحمراء", "name_en": "Al Hamra", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7050, "lng": 46.7700, "character": "سكني"},
    {"name_ar": "المعيزلية", "name_en": "Al Muayzilah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7550, "lng": 46.8500, "character": "سكني"},
    {"name_ar": "الخليج", "name_en": "Al Khaleej", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7300, "lng": 46.7950, "character": "سكني"},
    {"name_ar": "الملك فيصل", "name_en": "King Faisal", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7180, "lng": 46.7750, "character": "سكني"},
    {"name_ar": "القدس", "name_en": "Al Quds", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7080, "lng": 46.7850, "character": "سكني"},
    {"name_ar": "النهضة", "name_en": "An Nahdah", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7450, "lng": 46.7750, "character": "سكني"},
    {"name_ar": "الأندلس", "name_en": "Al Andalus", "municipality": "بلدية الروضة", "district": "شرق الرياض", "lat": 24.7350, "lng": 46.7500, "character": "سكني"},

    # بلدية العليا - Olaya Municipality
    {"name_ar": "العليا", "name_en": "Al Olaya", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.6900, "lng": 46.6850, "character": "تجاري راقي"},
    {"name_ar": "السليمانية", "name_en": "As Sulimaniyah", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7050, "lng": 46.6950, "character": "سكني تجاري"},
    {"name_ar": "الملك عبد العزيز", "name_en": "King Abdulaziz", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7150, "lng": 46.6800, "character": "سكني"},
    {"name_ar": "الملك عبد الله", "name_en": "King Abdullah", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7250, "lng": 46.6750, "character": "سكني تجاري"},
    {"name_ar": "الورود", "name_en": "Al Wurud", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7350, "lng": 46.6850, "character": "سكني"},
    {"name_ar": "صلاح الدين", "name_en": "Salah Ad Din", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7200, "lng": 46.7100, "character": "سكني"},
    {"name_ar": "الملك فهد", "name_en": "King Fahd", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7300, "lng": 46.6700, "character": "سكني"},
    {"name_ar": "المرسلات", "name_en": "Al Mursalat", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7400, "lng": 46.6650, "character": "سكني"},
    {"name_ar": "النزهة", "name_en": "An Nuzhah", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7500, "lng": 46.6900, "character": "سكني"},
    {"name_ar": "المغرزات", "name_en": "Al Mughrizat", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7450, "lng": 46.7050, "character": "سكني"},
    {"name_ar": "المروج", "name_en": "Al Muruj", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7550, "lng": 46.6750, "character": "سكني"},
    {"name_ar": "المصيف", "name_en": "Al Masif", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7600, "lng": 46.6650, "character": "سكني"},
    {"name_ar": "التعاون", "name_en": "At Taawun", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7650, "lng": 46.6750, "character": "سكني تجاري"},
    {"name_ar": "الإزدهار", "name_en": "Al Izdihar", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7500, "lng": 46.7200, "character": "سكني"},

    # بلدية المعذر - Maathar Municipality
    {"name_ar": "المعذر", "name_en": "Al Maathar", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.6950, "lng": 46.6600, "character": "سكني تجاري"},
    {"name_ar": "المحمدية", "name_en": "Al Muhammadiyah", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.7100, "lng": 46.6400, "character": "سكني"},
    {"name_ar": "الرحمانية", "name_en": "Ar Rahmaniyah", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.7250, "lng": 46.6300, "character": "سكني"},
    {"name_ar": "الرائد", "name_en": "Ar Raid", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.7200, "lng": 46.6500, "character": "سكني"},
    {"name_ar": "النخيل", "name_en": "An Nakheel", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.7350, "lng": 46.6350, "character": "سكني راقي"},
    {"name_ar": "أم الحمام الشرقي", "name_en": "Umm Al Hamam East", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.6800, "lng": 46.6500, "character": "سكني"},
    {"name_ar": "أم الحمام الغربي", "name_en": "Umm Al Hamam West", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.6800, "lng": 46.6350, "character": "سكني"},

    # بلدية عرقة - Irqah Municipality
    {"name_ar": "السفارات", "name_en": "As Safarat", "municipality": "بلدية عرقة", "district": "غرب الرياض", "lat": 24.6650, "lng": 46.6200, "character": "دبلوماسي راقي"},
    {"name_ar": "المهدية", "name_en": "Al Mahdiyah", "municipality": "بلدية عرقة", "district": "غرب الرياض", "lat": 24.6500, "lng": 46.5800, "character": "سكني"},
    {"name_ar": "عرقة", "name_en": "Irqah", "municipality": "بلدية عرقة", "district": "غرب الرياض", "lat": 24.6700, "lng": 46.5700, "character": "سكني"},
    {"name_ar": "ظهرة لبن", "name_en": "Dhahrat Laban", "municipality": "بلدية عرقة", "district": "غرب الرياض", "lat": 24.6400, "lng": 46.5900, "character": "سكني"},
    {"name_ar": "الخزامى", "name_en": "Al Khuzama", "municipality": "بلدية عرقة", "district": "غرب الرياض", "lat": 24.6750, "lng": 46.6100, "character": "سكني راقي"},

    # بلدية النسيم - Naseem Municipality
    {"name_ar": "النسيم الشرقي", "name_en": "An Naseem East", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6700, "lng": 46.7700, "character": "شعبي"},
    {"name_ar": "النسيم الغربي", "name_en": "An Naseem West", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6700, "lng": 46.7500, "character": "شعبي"},
    {"name_ar": "السلام", "name_en": "As Salam", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6900, "lng": 46.7800, "character": "سكني"},
    {"name_ar": "الريان", "name_en": "Ar Rayyan", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6800, "lng": 46.7600, "character": "سكني"},
    {"name_ar": "الروابي", "name_en": "Ar Rawabi", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6850, "lng": 46.7900, "character": "سكني"},
    {"name_ar": "النظيم", "name_en": "An Nadheem", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.7000, "lng": 46.8100, "character": "سكني"},
    {"name_ar": "المنار", "name_en": "Al Manar", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6950, "lng": 46.8000, "character": "سكني"},
    {"name_ar": "الندوة", "name_en": "An Nadwa", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.7100, "lng": 46.8200, "character": "سكني"},

    # بلدية الملز - Malaz Municipality
    {"name_ar": "جرير", "name_en": "Jarir", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6950, "lng": 46.7200, "character": "تجاري"},
    {"name_ar": "الربوة", "name_en": "Ar Rabwah", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6850, "lng": 46.7300, "character": "سكني"},
    {"name_ar": "الزهراء", "name_en": "Az Zahra", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6800, "lng": 46.7250, "character": "سكني"},
    {"name_ar": "الصفا", "name_en": "As Safa", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6750, "lng": 46.7200, "character": "سكني"},
    {"name_ar": "الضباط", "name_en": "Ad Dubbat", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6900, "lng": 46.7150, "character": "سكني"},
    {"name_ar": "الملز", "name_en": "Malaz", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6800, "lng": 46.7100, "character": "سكني تجاري"},
    {"name_ar": "الوزارات", "name_en": "Al Wizarat", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6700, "lng": 46.7050, "character": "حكومي"},
    {"name_ar": "الفاروق", "name_en": "Al Faruq", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6650, "lng": 46.7150, "character": "سكني"},
    {"name_ar": "العمل", "name_en": "Al Amal", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6750, "lng": 46.7350, "character": "سكني"},
    {"name_ar": "ثليم", "name_en": "Thulaim", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6700, "lng": 46.7000, "character": "سكني"},
    {"name_ar": "المربع", "name_en": "Al Murabba", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6550, "lng": 46.7100, "character": "تاريخي حكومي"},
    {"name_ar": "الفوطة", "name_en": "Al Futah", "municipality": "بلدية الملز", "district": "وسط الرياض", "lat": 24.6600, "lng": 46.7200, "character": "سكني"},

    # بلدية الشميسي - Shumaisi Municipality
    {"name_ar": "الرفيعة", "name_en": "Ar Rafiah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6600, "lng": 46.6800, "character": "سكني"},
    {"name_ar": "الهدا", "name_en": "Al Hada", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6550, "lng": 46.6700, "character": "سكني"},
    {"name_ar": "الشرقية", "name_en": "Ash Sharqiyah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6500, "lng": 46.6900, "character": "سكني"},
    {"name_ar": "الناصرية", "name_en": "An Nasiriyah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6450, "lng": 46.6850, "character": "تاريخي"},
    {"name_ar": "صياح", "name_en": "Siyah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6400, "lng": 46.6750, "character": "سكني"},
    {"name_ar": "الوشام", "name_en": "Al Washam", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6480, "lng": 46.6650, "character": "سكني"},
    {"name_ar": "النموذجية", "name_en": "An Namudhajiyah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6520, "lng": 46.6600, "character": "سكني"},
    {"name_ar": "المؤتمرات", "name_en": "Al Mutamarat", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6550, "lng": 46.6550, "character": "حكومي"},
    {"name_ar": "البديعة", "name_en": "Al Badiah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6600, "lng": 46.6500, "character": "سكني"},
    {"name_ar": "أم سليم", "name_en": "Umm Saleem", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6650, "lng": 46.6450, "character": "سكني"},
    {"name_ar": "الشميسي", "name_en": "Ash Shumaisi", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6350, "lng": 46.6750, "character": "شعبي"},
    {"name_ar": "الجرادية", "name_en": "Al Jaradiyah", "municipality": "بلدية الشميسي", "district": "غرب الرياض", "lat": 24.6550, "lng": 46.6350, "character": "سكني"},
    {"name_ar": "الفاخرية", "name_en": "Al Fakhriyah", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6500, "lng": 46.6950, "character": "سكني"},
    {"name_ar": "عليشة", "name_en": "Ulaysha", "municipality": "بلدية الشميسي", "district": "وسط الرياض", "lat": 24.6450, "lng": 46.7000, "character": "سكني"},

    # بلدية العريجاء - Uraija Municipality
    {"name_ar": "العريجاء", "name_en": "Al Uraija", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6100, "lng": 46.6300, "character": "سكني"},
    {"name_ar": "العريجاء الوسطى", "name_en": "Al Uraija Central", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6050, "lng": 46.6250, "character": "سكني"},
    {"name_ar": "العريجاء الغربية", "name_en": "Al Uraija West", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6000, "lng": 46.6100, "character": "سكني"},
    {"name_ar": "الدريهمية", "name_en": "Ad Duraihimiyah", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6200, "lng": 46.6400, "character": "سكني"},
    {"name_ar": "شبرا", "name_en": "Shubra", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6150, "lng": 46.6500, "character": "شعبي"},
    {"name_ar": "السويدي", "name_en": "As Suwaidi", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6250, "lng": 46.6600, "character": "سكني"},
    {"name_ar": "السويدي الغربي", "name_en": "As Suwaidi West", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6200, "lng": 46.6500, "character": "سكني"},
    {"name_ar": "ظهرة البديعة", "name_en": "Dhahrat Al Badiah", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6300, "lng": 46.6350, "character": "سكني"},
    {"name_ar": "سلطانة", "name_en": "Sultanah", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6350, "lng": 46.6450, "character": "سكني"},
    {"name_ar": "الزهرة", "name_en": "Az Zahrah", "municipality": "بلدية العريجاء", "district": "جنوب غرب الرياض", "lat": 24.6400, "lng": 46.6550, "character": "سكني"},

    # بلدية نمار - Namar Municipality
    {"name_ar": "ظهرة نمار", "name_en": "Dhahrat Namar", "municipality": "بلدية نمار", "district": "جنوب غرب الرياض", "lat": 24.5600, "lng": 46.5800, "character": "سكني جديد"},
    {"name_ar": "ديراب", "name_en": "Dirab", "municipality": "بلدية نمار", "district": "جنوب غرب الرياض", "lat": 24.5200, "lng": 46.5500, "character": "ريفي"},
    {"name_ar": "نمار", "name_en": "Namar", "municipality": "بلدية نمار", "district": "جنوب غرب الرياض", "lat": 24.5400, "lng": 46.5700, "character": "سكني"},
    {"name_ar": "الحزم", "name_en": "Al Hazm", "municipality": "بلدية نمار", "district": "جنوب غرب الرياض", "lat": 24.5800, "lng": 46.6000, "character": "سكني"},
    {"name_ar": "لبن", "name_en": "Laban", "municipality": "بلدية نمار", "district": "جنوب غرب الرياض", "lat": 24.5900, "lng": 46.6100, "character": "سكني"},

    # بلدية الشفا - Shifa Municipality
    {"name_ar": "أحد", "name_en": "Uhud", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5500, "lng": 46.6500, "character": "سكني"},
    {"name_ar": "عكاظ", "name_en": "Ukaz", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5600, "lng": 46.6600, "character": "سكني"},
    {"name_ar": "الشفاء", "name_en": "Ash Shifa", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5700, "lng": 46.6700, "character": "سكني"},
    {"name_ar": "المروة", "name_en": "Al Marwah", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5800, "lng": 46.6800, "character": "سكني"},
    {"name_ar": "بدر", "name_en": "Badr", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5900, "lng": 46.6900, "character": "سكني"},
    {"name_ar": "المصانع", "name_en": "Al Masani", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5650, "lng": 46.7000, "character": "صناعي"},
    {"name_ar": "المنصورية", "name_en": "Al Mansuriyah", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5750, "lng": 46.7100, "character": "سكني"},
    {"name_ar": "عريض", "name_en": "Arid", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5850, "lng": 46.7200, "character": "سكني"},
    {"name_ar": "العماجية", "name_en": "Al Amajiyah", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5450, "lng": 46.6550, "character": "سكني"},

    # بلدية السلي - Sali Municipality
    {"name_ar": "خشم العان", "name_en": "Khashm Al An", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6000, "lng": 46.7600, "character": "سكني"},
    {"name_ar": "الدفاع", "name_en": "Ad Difa", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6100, "lng": 46.7500, "character": "عسكري"},
    {"name_ar": "المناخ", "name_en": "Al Manakh", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6050, "lng": 46.7400, "character": "تجاري"},
    {"name_ar": "السلي", "name_en": "As Sali", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6150, "lng": 46.7300, "character": "سكني"},
    {"name_ar": "النور", "name_en": "An Nur", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6200, "lng": 46.7200, "character": "سكني"},
    {"name_ar": "الإسكان", "name_en": "Al Iskan", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6250, "lng": 46.7350, "character": "سكني"},
    {"name_ar": "الصناعية الجديدة", "name_en": "New Industrial", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.5900, "lng": 46.7500, "character": "صناعي"},
    {"name_ar": "الفيحاء", "name_en": "Al Fayha", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6300, "lng": 46.7400, "character": "سكني"},
    {"name_ar": "الجزيرة", "name_en": "Al Jazirah", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6350, "lng": 46.7250, "character": "سكني"},
    {"name_ar": "السعادة", "name_en": "As Saadah", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6180, "lng": 46.7450, "character": "سكني"},
    {"name_ar": "هيت", "name_en": "Hit", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6100, "lng": 46.7550, "character": "سكني"},
    {"name_ar": "البرية", "name_en": "Al Bariyah", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.6050, "lng": 46.7650, "character": "سكني"},
    {"name_ar": "المشاعل", "name_en": "Al Mashael", "municipality": "بلدية السلي", "district": "جنوب شرق الرياض", "lat": 24.5950, "lng": 46.7550, "character": "سكني"},

    # بلدية البطحاء - Batha Municipality
    {"name_ar": "الدوبية", "name_en": "Ad Dubiyah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6400, "lng": 46.7100, "character": "شعبي"},
    {"name_ar": "القرى", "name_en": "Al Qura", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6380, "lng": 46.7050, "character": "شعبي"},
    {"name_ar": "الصناعية", "name_en": "As Sinaiyah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6350, "lng": 46.7150, "character": "صناعي"},
    {"name_ar": "الوسيطاء", "name_en": "Al Wusayta", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6320, "lng": 46.7080, "character": "شعبي"},
    {"name_ar": "معكال", "name_en": "Maakal", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6300, "lng": 46.7000, "character": "تاريخي"},
    {"name_ar": "الفيصلية", "name_en": "Al Faysaliyah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6280, "lng": 46.7120, "character": "سكني"},
    {"name_ar": "منفوحة", "name_en": "Manfuhah", "municipality": "بلدية البطحاء", "district": "جنوب الرياض", "lat": 24.6200, "lng": 46.7050, "character": "شعبي"},
    {"name_ar": "المنصورة", "name_en": "Al Mansurah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6250, "lng": 46.7000, "character": "سكني"},
    {"name_ar": "اليمامة", "name_en": "Al Yamamah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6350, "lng": 46.6950, "character": "سكني"},
    {"name_ar": "سلام", "name_en": "Salam", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6220, "lng": 46.7100, "character": "شعبي"},
    {"name_ar": "جبرة", "name_en": "Jabrah", "municipality": "بلدية البطحاء", "district": "جنوب الرياض", "lat": 24.6150, "lng": 46.7050, "character": "شعبي"},
    {"name_ar": "عتيقة", "name_en": "Utayqah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6300, "lng": 46.6900, "character": "تاريخي"},
    {"name_ar": "غبيراء", "name_en": "Ghubayra", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6350, "lng": 46.6950, "character": "شعبي"},
    {"name_ar": "البطيحا", "name_en": "Al Batiha", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6380, "lng": 46.7150, "character": "تجاري شعبي"},
    {"name_ar": "الخالدية", "name_en": "Al Khalidiyah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6420, "lng": 46.7050, "character": "سكني"},
    {"name_ar": "الديرة", "name_en": "Ad Dirah", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6340, "lng": 46.7100, "character": "تاريخي تجاري"},
    {"name_ar": "العود", "name_en": "Al Oud", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6400, "lng": 46.6950, "character": "سكني"},
    {"name_ar": "المرقب", "name_en": "Al Murqab", "municipality": "بلدية البطحاء", "district": "وسط الرياض", "lat": 24.6450, "lng": 46.7050, "character": "سكني"},
    {"name_ar": "منفوحة الجديدة", "name_en": "New Manfuhah", "municipality": "بلدية البطحاء", "district": "جنوب الرياض", "lat": 24.6100, "lng": 46.7050, "character": "سكني"},

    # بلدية العزيزية - Aziziyah Municipality
    {"name_ar": "العزيزية", "name_en": "Al Aziziyah", "municipality": "بلدية العزيزية", "district": "جنوب الرياض", "lat": 24.5800, "lng": 46.7200, "character": "سكني"},
    {"name_ar": "طيبة", "name_en": "Taybah", "municipality": "بلدية العزيزية", "district": "جنوب الرياض", "lat": 24.5700, "lng": 46.7300, "character": "سكني"},
    {"name_ar": "المصفاة", "name_en": "Al Musfah", "municipality": "بلدية العزيزية", "district": "جنوب الرياض", "lat": 24.5900, "lng": 46.7100, "character": "سكني"},
    {"name_ar": "الدار البيضاء", "name_en": "Ad Dar Al Bayda", "municipality": "بلدية العزيزية", "district": "جنوب الرياض", "lat": 24.5600, "lng": 46.7400, "character": "سكني"},

    # بلدية الحائر - Haeer Municipality
    {"name_ar": "الحائر", "name_en": "Al Haeer", "municipality": "بلدية الحائر", "district": "جنوب الرياض", "lat": 24.4200, "lng": 46.7400, "character": "ريفي"},
    {"name_ar": "الغنامية", "name_en": "Al Ghunamiyah", "municipality": "بلدية الحائر", "district": "جنوب الرياض", "lat": 24.4500, "lng": 46.7200, "character": "ريفي"},

    # Additional well-known areas not in Wikipedia list but in our data
    {"name_ar": "الدرعية", "name_en": "Diriyah", "municipality": "محافظة الدرعية", "district": "شمال غرب الرياض", "lat": 24.7340, "lng": 46.5730, "character": "تاريخي سياحي"},
    {"name_ar": "الثمامة", "name_en": "Thumamah", "municipality": "أمانة الرياض", "district": "شمال الرياض", "lat": 25.0000, "lng": 46.6500, "character": "ترفيهي صحراوي"},
    {"name_ar": "الحي الدبلوماسي", "name_en": "Diplomatic Quarter", "municipality": "بلدية عرقة", "district": "غرب الرياض", "lat": 24.6700, "lng": 46.6250, "character": "دبلوماسي راقي"},
    {"name_ar": "كافد", "name_en": "KAFD", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7670, "lng": 46.6430, "character": "مالي تجاري"},
    {"name_ar": "طويق", "name_en": "Tuwaiq", "municipality": "بلدية نمار", "district": "غرب الرياض", "lat": 24.6100, "lng": 46.5600, "character": "سكني جديد"},
    {"name_ar": "العروبة", "name_en": "Al Urubah", "municipality": "بلدية العليا", "district": "وسط الرياض", "lat": 24.7000, "lng": 46.7000, "character": "سكني"},
    {"name_ar": "الشهداء", "name_en": "Ash Shuhada", "municipality": "بلدية النسيم", "district": "شرق الرياض", "lat": 24.6750, "lng": 46.7850, "character": "سكني"},
    {"name_ar": "الملك سلمان", "name_en": "King Salman", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8000, "lng": 46.6000, "character": "جديد"},
    {"name_ar": "جاكس", "name_en": "JAX District", "municipality": "محافظة الدرعية", "district": "شمال غرب الرياض", "lat": 24.7350, "lng": 46.5750, "character": "فني إبداعي"},
    {"name_ar": "الريم", "name_en": "Al Reem", "municipality": "بلدية الشمال", "district": "شمال الرياض", "lat": 24.8500, "lng": 46.5900, "character": "سكني جديد"},
    {"name_ar": "البجيري", "name_en": "Al Bujairi", "municipality": "محافظة الدرعية", "district": "شمال غرب الرياض", "lat": 24.7330, "lng": 46.5720, "character": "تراثي سياحي"},
    {"name_ar": "الشفا", "name_en": "Ash Shifa", "municipality": "بلدية الشفا", "district": "جنوب الرياض", "lat": 24.5650, "lng": 46.6750, "character": "سكني"},
    {"name_ar": "المعذر الشمالي", "name_en": "Al Maathar North", "municipality": "بلدية المعذر", "district": "غرب الرياض", "lat": 24.7050, "lng": 46.6600, "character": "سكني تجاري"},
]

# Generate IDs
def make_id(name_en):
    return re.sub(r'[^a-z0-9]+', '-', name_en.lower()).strip('-')

# Build final list
neighborhoods = []
seen = set()
for n in WIKI_NEIGHBORHOODS:
    key = n['name_ar']
    if key in seen:
        continue
    seen.add(key)
    nid = make_id(n['name_en'])
    neighborhoods.append({
        "id": nid,
        "name_ar": n['name_ar'],
        "name_en": n['name_en'],
        "municipality": n['municipality'],
        "district": n['district'],
        "lat": n['lat'],
        "lng": n['lng'],
        "character": n['character'],
        "description_ar": ""
    })

print(f"Total neighborhoods: {len(neighborhoods)}")

# Count by district
districts = {}
for n in neighborhoods:
    d = n['district']
    districts[d] = districts.get(d, 0) + 1
for d, c in sorted(districts.items(), key=lambda x: -x[1]):
    print(f"  {d}: {c}")

# Count by municipality
muns = {}
for n in neighborhoods:
    m = n['municipality']
    muns[m] = muns.get(m, 0) + 1
print("\nBy municipality:")
for m, c in sorted(muns.items(), key=lambda x: -x[1]):
    print(f"  {m}: {c}")
