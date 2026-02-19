#!/usr/bin/env python3
"""Deduplicate places by name_en (keep first occurrence) and fix duplicate IDs."""

import json
from pathlib import Path
from collections import Counter

BASE = Path("/home/ubuntu/.openclaw/workspace/projects/riyadh-places")

with open(BASE / "data/places.json", encoding="utf-8") as f:
    places = json.load(f)

print(f"Before dedup: {len(places)} places")

# Dedup by name_en (case-insensitive, keep first)
seen_names = {}
deduped = []
removed = []
for p in places:
    key = p["name_en"].lower().strip()
    if key not in seen_names:
        seen_names[key] = p
        deduped.append(p)
    else:
        removed.append(p["name_en"])

print(f"Removed {len(removed)} duplicates by name_en")
if removed:
    for r in removed[:20]:
        print(f"  - {r}")

# Fix duplicate IDs
seen_ids = set()
for p in deduped:
    orig_id = p["id"]
    if orig_id in seen_ids:
        # Append suffix
        suffix = 2
        while f"{orig_id}-{suffix}" in seen_ids:
            suffix += 1
        p["id"] = f"{orig_id}-{suffix}"
        print(f"  Fixed ID: {orig_id} -> {p['id']}")
    seen_ids.add(p["id"])

# Verify no duplicate IDs
ids = [p["id"] for p in deduped]
id_counts = Counter(ids)
dupes = {k: v for k, v in id_counts.items() if v > 1}
if dupes:
    print(f"⚠️ Still have duplicate IDs: {dupes}")
else:
    print("✅ All IDs unique")

# Verify no duplicate names
names = [p["name_en"].lower().strip() for p in deduped]
name_counts = Counter(names)
name_dupes = {k: v for k, v in name_counts.items() if v > 1}
if name_dupes:
    print(f"⚠️ Still have duplicate names: {name_dupes}")
else:
    print("✅ All names unique")

print(f"\nAfter dedup: {len(deduped)} places")

# Save
with open(BASE / "data/places.json", "w", encoding="utf-8") as f:
    json.dump(deduped, f, ensure_ascii=False, indent=2)
print("💾 Saved places.json")

# Regenerate light version
light_fields = ["id", "name_ar", "name_en", "category", "category_ar", "category_en",
                "neighborhood", "neighborhood_en", "google_rating", "price_level",
                "trending", "is_new", "lat", "lng", "is_free", "audience", "district"]
light = [{k: p.get(k) for k in light_fields if k in p} for p in deduped]
with open(BASE / "data/places-light.json", "w", encoding="utf-8") as f:
    json.dump(light, f, ensure_ascii=False, indent=2)
print("💾 Saved places-light.json")
