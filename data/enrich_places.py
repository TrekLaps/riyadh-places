#!/usr/bin/env python3
"""
Build initial enrichment structure from existing places.json data.
This creates the base file that we'll then enrich with web searches.
"""
import json

with open('/home/ubuntu/.openclaw/workspace/projects/riyadh-places/data/places.json', 'r') as f:
    places = json.load(f)

# Filter restaurants and cafes
rc = [p for p in places if p.get('category_en','') in ('cafe','restaurant','كافيه','مطعم') 
      or p.get('category','') in ('كافيه','مطعم','مطاعم')]

enriched = []
for p in rc[:200]:
    entry = {
        "name": p.get("name_ar", ""),
        "name_en": p.get("name_en", ""),
        "id": p.get("id", ""),
        "rating": p.get("google_rating", None),
        "rating_count": None,
        "phone": None,
        "hours": None,
        "website": None,
        "instagram": None,
        "cuisine": None,
        "description_ar": p.get("description_ar", None),
        "perfect_for": p.get("perfect_for", []) if p.get("perfect_for") else [],
        "price_level": p.get("price_level", None),
        "address_ar": p.get("neighborhood", None),
        "neighborhood": p.get("neighborhood", ""),
        "category": p.get("category_en", p.get("category", "")),
    }
    enriched.append(entry)

with open('/home/ubuntu/.openclaw/workspace/projects/riyadh-places/data/enriched-base.json', 'w') as f:
    json.dump(enriched, f, ensure_ascii=False, indent=2)

print(f"Created base enrichment for {len(enriched)} places")
# Print first 5 for verification
for e in enriched[:3]:
    print(json.dumps(e, ensure_ascii=False, indent=2))
