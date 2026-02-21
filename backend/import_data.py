"""Import places.json → SQLite + FTS5 — وين نروح بالرياض."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from database import init_db, insert_place, insert_fts, DATABASE_PATH


def main(json_path: str | None = None, db_path: str | None = None) -> int:
    """Import places from JSON into SQLite."""
    data_file = Path(json_path or "../data/places.json")
    if not data_file.exists():
        print(f"❌ ملف البيانات مو موجود: {data_file}")
        return 1

    print(f"📂 قراءة البيانات من: {data_file}")
    with open(data_file, "r", encoding="utf-8") as f:
        places = json.load(f)

    print(f"📊 عدد الأماكن: {len(places)}")

    # Initialize database
    target_db = Path(db_path) if db_path else DATABASE_PATH
    print(f"🗄️ إنشاء قاعدة البيانات: {target_db}")
    conn = init_db(target_db)

    # Clear existing data for fresh import
    conn.execute("DELETE FROM places_fts")
    conn.execute("DELETE FROM places")
    conn.commit()

    # Insert places
    start = time.time()
    batch_size = 500
    inserted = 0
    errors = 0

    for i in range(0, len(places), batch_size):
        batch = places[i : i + batch_size]
        for place in batch:
            try:
                insert_place(conn, place)
                insert_fts(conn, place)
                inserted += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  ⚠️ خطأ في: {place.get('id', '?')} — {e}")

        conn.commit()
        pct = min(100, int((i + len(batch)) / len(places) * 100))
        print(f"  ⏳ {pct}% ({inserted}/{len(places)})")

    elapsed = time.time() - start

    # Verify
    count = conn.execute("SELECT COUNT(*) as cnt FROM places").fetchone()["cnt"]
    fts_count = conn.execute("SELECT COUNT(*) as cnt FROM places_fts").fetchone()["cnt"]

    print(f"\n✅ تم الاستيراد بنجاح!")
    print(f"   📍 الأماكن: {count}")
    print(f"   🔍 FTS index: {fts_count}")
    print(f"   ❌ أخطاء: {errors}")
    print(f"   ⏱️ الوقت: {elapsed:.1f}s")

    # Quick stats
    categories = conn.execute(
        "SELECT category, COUNT(*) as cnt FROM places GROUP BY category ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    print(f"\n📊 أكبر الفئات:")
    for row in categories:
        print(f"   {row['category']}: {row['cnt']}")

    neighborhoods = conn.execute(
        "SELECT COUNT(DISTINCT neighborhood) as cnt FROM places"
    ).fetchone()
    print(f"\n🏘️ عدد الأحياء: {neighborhoods['cnt']}")

    conn.close()
    return 0


if __name__ == "__main__":
    json_path = sys.argv[1] if len(sys.argv) > 1 else None
    db_path = sys.argv[2] if len(sys.argv) > 2 else None
    sys.exit(main(json_path, db_path))
