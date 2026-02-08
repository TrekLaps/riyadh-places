#!/usr/bin/env python3
"""
Add "perfect_for" situational tags to all places in places.json.
Tags are contextually assigned based on category, price, audience, description, and other attributes.
"""

import json
import re

TAGS = {
    "عوائل": "families",
    "شباب": "young people/friends",
    "أزواج": "couples/date night",
    "دراسة": "studying/working",
    "اجتماع عمل": "business meeting",
    "فطور": "breakfast",
    "سهرة": "late night",
    "أطفال": "kids",
    "تصوير": "photography/instagrammable",
    "هدوء": "quiet/peaceful",
    "أجواء حماسية": "lively atmosphere",
    "ميزانية محدودة": "budget-friendly",
    "مناسبات": "celebrations/special occasions",
    "تجمع كبير": "large groups",
    "solo": "solo visit",
}

def assign_tags(place):
    tags = set()
    cat_en = (place.get("category_en") or "").lower()
    cat_ar = place.get("category_ar") or place.get("category") or ""
    price = place.get("price_level", "")
    audience = place.get("audience", [])
    desc = (place.get("description_ar") or "").lower()
    name = (place.get("name_ar") or "") + " " + (place.get("name_en") or "").lower()
    pros = " ".join(place.get("pros_ar") or place.get("pros") or []).lower()
    cons = " ".join(place.get("cons_ar") or place.get("cons") or []).lower()
    best_time = (place.get("best_time") or "").lower()
    review = (place.get("review_quote_ar") or place.get("review_quote") or "").lower()
    is_free = place.get("is_free", False)
    rating = place.get("google_rating", 0)
    all_text = f"{desc} {pros} {cons} {best_time} {review} {name}"

    # ===== Category-based rules =====

    # Cafes
    if cat_en == "cafe" or cat_ar == "كافيه":
        tags.add("شباب")
        # Quiet/study cafes
        if any(w in all_text for w in ["هاد", "هدوء", "عمل", "قراءة", "دراس", "كتب", "لابتوب", "ريموت", "عن بعد"]):
            tags.add("دراسة")
            tags.add("هدوء")
        # If described as cozy/calm but not explicitly study
        if any(w in all_text for w in ["هاد", "مريح", "هدوء", "سكون"]):
            tags.add("هدوء")
        # Breakfast cafes
        if any(w in all_text for w in ["فطور", "فطار", "breakfast", "صباح"]):
            tags.add("فطور")
        # Instagrammable
        if any(w in all_text for w in ["تصميم", "انستقرام", "تصوير", "جذاب", "عصري", "أوروب", "فريد"]):
            tags.add("تصوير")
        # Expensive cafes → couples
        if price in ["$$$", "$$$$"]:
            tags.add("أزواج")
            tags.add("مناسبات")
        # Budget cafes
        if price == "$" or is_free:
            tags.add("ميزانية محدودة")
        # Solo-friendly if small/quiet
        if any(w in all_text for w in ["هاد", "قراءة", "لوحدك", "فردي"]):
            tags.add("solo")

    # Restaurants
    elif cat_en == "restaurant" or cat_ar == "مطعم":
        # Expensive restaurants → special occasions, couples
        if price in ["$$$", "$$$$"]:
            tags.add("مناسبات")
            tags.add("أزواج")
        # Mid-range
        if price == "$$":
            tags.add("شباب")
        # Budget
        if price == "$" or is_free:
            tags.add("ميزانية محدودة")
            tags.add("شباب")
        # Family restaurants
        if "عوائل" in audience or "أطفال" in audience or any(w in all_text for w in ["عائل", "عوائل", "أطفال", "عائلي"]):
            tags.add("عوائل")
        # Breakfast places
        if any(w in all_text for w in ["فطور", "فطار", "breakfast", "صباح"]):
            tags.add("فطور")
        # Late night
        if any(w in all_text for w in ["سهر", "ليل", "متأخر", "late"]):
            tags.add("سهرة")
        # Business meetings
        if any(w in all_text for w in ["عمل", "اجتماع", "رجال أعمال", "business", "راق", "فاخر"]):
            tags.add("اجتماع عمل")
        # Large groups
        if any(w in all_text for w in ["تجمع", "مجموع", "كبير", "بوفيه", "حفل"]):
            tags.add("تجمع كبير")
        # Photography
        if any(w in all_text for w in ["تصميم", "إطلالة", "فيو", "view", "بانوراما", "أجواء", "انستقرام"]):
            tags.add("تصوير")
        # Lively atmosphere
        if any(w in all_text for w in ["حماس", "حيوي", "نشيط", "موسيق", "أجواء حلو"]):
            tags.add("أجواء حماسية")

    # Entertainment / Activities
    elif cat_en in ["activity", "entertainment"] or cat_ar == "ترفيه":
        tags.add("شباب")
        tags.add("عوائل")
        # Kids activities
        if any(w in all_text for w in ["أطفال", "طفل", "kids", "ملاهي", "لعب", "ألعاب", "تعليم"]):
            tags.add("أطفال")
        # Lively
        tags.add("أجواء حماسية")
        # Photography
        if any(w in all_text for w in ["تصوير", "منظر", "فيو", "إطلالة"]):
            tags.add("تصوير")
        # Budget
        if is_free or price == "$":
            tags.add("ميزانية محدودة")
        # Large groups
        if any(w in all_text for w in ["مجموع", "تجمع", "فريق"]):
            tags.add("تجمع كبير")

    # Nature
    elif cat_en == "nature" or cat_ar == "طبيعة":
        tags.add("عوائل")
        tags.add("تصوير")
        tags.add("هدوء")
        if is_free or price in ["$", "مجاني"]:
            tags.add("ميزانية محدودة")
        if any(w in all_text for w in ["أطفال", "لعب", "ملعب", "حديقة"]):
            tags.add("أطفال")
        if any(w in all_text for w in ["مشي", "رياض", "رحل", "مغامر", "هايك"]):
            tags.add("شباب")
        tags.add("solo")

    # Shopping / Malls
    elif cat_en in ["shopping", "mall"] or cat_ar in ["تسوق", "مولات"]:
        tags.add("عوائل")
        tags.add("شباب")
        if any(w in all_text for w in ["أطفال", "ألعاب", "ملاهي", "ترفيه"]):
            tags.add("أطفال")
        if any(w in all_text for w in ["فاخر", "ماركات", "luxury", "عالمي"]):
            tags.add("مناسبات")
        if any(w in all_text for w in ["شعبي", "رخيص", "اقتصاد"]):
            tags.add("ميزانية محدودة")
        tags.add("تجمع كبير")
        # Photography for malls with nice design
        if any(w in all_text for w in ["تصميم", "معمار", "فن", "بوليفارد"]):
            tags.add("تصوير")

    # Desserts
    elif cat_en in ["dessert", "desserts"] or cat_ar == "حلويات":
        tags.add("شباب")
        tags.add("عوائل")
        if price == "$" or is_free:
            tags.add("ميزانية محدودة")
        if any(w in all_text for w in ["أطفال", "آيس كريم", "كيك"]):
            tags.add("أطفال")
        if any(w in all_text for w in ["تصميم", "فريد", "انستقرام"]):
            tags.add("تصوير")

    # Hotels
    elif cat_en == "hotel" or cat_ar == "فنادق":
        tags.add("أزواج")
        tags.add("مناسبات")
        if price in ["$$$", "$$$$"]:
            tags.add("اجتماع عمل")
        if any(w in all_text for w in ["عائل", "عوائل", "أطفال", "مسبح", "ملاهي"]):
            tags.add("عوائل")
        if any(w in all_text for w in ["تصوير", "إطلال", "فيو", "بانوراما"]):
            tags.add("تصوير")
        tags.add("سهرة")

    # Chalets
    elif cat_en == "chalet" or cat_ar == "شاليه":
        tags.add("عوائل")
        tags.add("شباب")
        tags.add("تجمع كبير")
        if any(w in all_text for w in ["أطفال", "مسبح", "ملعب", "ألعاب"]):
            tags.add("أطفال")
        if any(w in all_text for w in ["أزواج", "رومانس", "خاص", "خصوصي"]):
            tags.add("أزواج")
        tags.add("سهرة")
        tags.add("مناسبات")

    # Museums
    elif cat_en == "museum" or cat_ar == "متاحف":
        tags.add("عوائل")
        tags.add("تصوير")
        if is_free or price in ["$", "مجاني"]:
            tags.add("ميزانية محدودة")
        tags.add("solo")
        if any(w in all_text for w in ["أطفال", "تعليم", "تفاعل"]):
            tags.add("أطفال")

    # Events
    elif cat_en in ["event", "events"] or cat_ar == "فعاليات":
        tags.add("شباب")
        tags.add("أجواء حماسية")
        if any(w in all_text for w in ["عائل", "عوائل", "أطفال"]):
            tags.add("عوائل")
            tags.add("أطفال")
        if any(w in all_text for w in ["تصوير", "معرض", "فن"]):
            tags.add("تصوير")
        tags.add("تجمع كبير")

    # ===== Cross-category audience-based enrichment =====
    
    # Audience field enrichment
    for a in audience:
        if a == "عوائل":
            tags.add("عوائل")
        elif a == "شباب" or a == "أصدقاء":
            tags.add("شباب")
        elif a == "أزواج":
            tags.add("أزواج")
        elif a == "أطفال":
            tags.add("أطفال")
        elif a == "رجال أعمال" or a == "موظفين":
            tags.add("اجتماع عمل")
        elif a == "عاملين عن بعد" or a == "طلاب" or a == "محبي القراءة":
            tags.add("دراسة")
        elif a == "سياح":
            tags.add("تصوير")
        elif a == "مغامرين" or a == "رياضيين":
            tags.add("شباب")

    # ===== Description/text-based cross-category rules =====
    
    # Late night indicators
    if any(w in all_text for w in ["سهر", "ليل", "متأخر", "24 ساع", "٢٤", "منتصف الليل"]):
        tags.add("سهرة")

    # Budget indicators
    if is_free or price == "مجاني":
        tags.add("ميزانية محدودة")

    # Ensure at least 2 tags
    if len(tags) < 2:
        # Add generic based on category
        if cat_en in ["cafe", "restaurant"] or cat_ar in ["كافيه", "مطعم"]:
            tags.add("شباب")
        tags.add("solo")

    # Cap at 5 tags — prioritize most relevant
    if len(tags) > 5:
        # Priority order for trimming
        priority = [
            "عوائل", "شباب", "أزواج", "أطفال",  # audience
            "مناسبات", "تصوير", "هدوء",  # vibe
            "دراسة", "فطور", "سهرة", "اجتماع عمل",  # situation
            "أجواء حماسية", "ميزانية محدودة", "تجمع كبير", "solo"  # extra
        ]
        # Keep tags that exist, in priority order, up to 5
        ordered = [t for t in priority if t in tags]
        tags = set(ordered[:5])

    return list(tags)


def main():
    with open("places.json", "r", encoding="utf-8") as f:
        places = json.load(f)

    print(f"Processing {len(places)} places...")

    tag_counts = {}
    for place in places:
        tags = assign_tags(place)
        place["perfect_for"] = tags
        for t in tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    with open("places.json", "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Added perfect_for tags to all {len(places)} places.")
    print("\n📊 Tag distribution:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count}")

    # Verify
    no_tags = [p["id"] for p in places if not p.get("perfect_for")]
    if no_tags:
        print(f"\n⚠️ Places without tags: {no_tags}")
    else:
        print("\n✅ All places have perfect_for tags!")

    # Check min/max
    min_tags = min(len(p["perfect_for"]) for p in places)
    max_tags = max(len(p["perfect_for"]) for p in places)
    avg_tags = sum(len(p["perfect_for"]) for p in places) / len(places)
    print(f"\n📈 Tags per place: min={min_tags}, max={max_tags}, avg={avg_tags:.1f}")


if __name__ == "__main__":
    main()
