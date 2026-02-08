#!/usr/bin/env python3
"""Merge all batches into the main places.json."""

import json
from collections import Counter

# Load all files
with open('places.json') as f:
    existing = json.load(f)

with open('new-batch-2026.json') as f:
    batch1 = json.load(f)

with open('new-remaining-2026.json') as f:
    batch2 = json.load(f)

with open('new-extra-2026.json') as f:
    batch3 = json.load(f)

print(f"Existing: {len(existing)}")
print(f"Batch 1: {len(batch1)}")
print(f"Batch 2: {len(batch2)}")
print(f"Batch 3: {len(batch3)}")

# Check for duplicate IDs
existing_ids = set(p['id'] for p in existing)
all_new = batch1 + batch2 + batch3
new_ids = set()
dupes = 0
clean_new = []

for p in all_new:
    if p['id'] in existing_ids or p['id'] in new_ids:
        dupes += 1
        # Try to fix by appending suffix
        p['id'] = p['id'] + '-new'
        if p['id'] in existing_ids or p['id'] in new_ids:
            p['id'] = p['id'] + '-' + str(len(new_ids))
            if p['id'] in existing_ids or p['id'] in new_ids:
                continue  # Skip this one
    new_ids.add(p['id'])
    clean_new.append(p)

print(f"\nDuplicates found and handled: {dupes}")
print(f"Clean new places: {len(clean_new)}")

# Merge
all_places = existing + clean_new
print(f"\nTotal merged: {len(all_places)}")

# Verify no duplicate IDs
all_merged_ids = [p['id'] for p in all_places]
unique_ids = set(all_merged_ids)
print(f"Unique IDs: {len(unique_ids)}")
if len(all_merged_ids) != len(unique_ids):
    print(f"WARNING: {len(all_merged_ids) - len(unique_ids)} duplicate IDs remain!")
    # Find and remove duplicates
    seen = set()
    deduped = []
    for p in all_places:
        if p['id'] not in seen:
            seen.add(p['id'])
            deduped.append(p)
    all_places = deduped
    print(f"After dedup: {len(all_places)}")

# Category counts
cats = Counter(p.get('category','unknown') for p in all_places)
print("\nCategory counts:")
for k, v in cats.most_common():
    print(f"  {k}: {v}")

# District counts
districts = Counter(p.get('district','unknown') for p in all_places)
print("\nDistrict counts:")
for k, v in districts.most_common():
    print(f"  {k}: {v}")

# Save
with open('places.json', 'w', encoding='utf-8') as f:
    json.dump(all_places, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(all_places)} places to places.json")
print(f"File size: {len(json.dumps(all_places, ensure_ascii=False)):,} chars")
