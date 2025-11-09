#!/usr/bin/env python3
"""
Mevcut veritabanına din bilgisi ekle - HIZLI
"""

import sqlite3
from pathlib import Path
import json

DB_FILE = Path(__file__).parent.parent / "ethnidata" / "ethnidata.db"
RELIGION_FILE = Path(__file__).parent.parent / "data" / "raw" / "religion" / "country_religion_mapping.json"

# Load religion mapping
with open(RELIGION_FILE, 'r', encoding='utf-8') as f:
    religion_data = json.load(f)
    COUNTRY_RELIGION = religion_data['primary_religion']

print("="*80)
print("DİN BİLGİSİ EKLEME - MEVCUT VERİTABANINA")
print("="*80)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Check current state
cursor.execute("SELECT COUNT(*) FROM names")
total = cursor.fetchone()[0]
print(f"\n📊 Toplam kayıt: {total:,}")

cursor.execute("SELECT COUNT(*) FROM names WHERE religion IS NOT NULL")
with_religion = cursor.fetchone()[0]
print(f"📊 Din bilgisi olan: {with_religion:,}")
print(f"📊 Din bilgisi olmayan: {(total - with_religion):,}")

# Update religions based on country code
print("\n🔄 Ülke koduna göre din ekleniyor...")
updated = 0
for country_code, religion in COUNTRY_RELIGION.items():
    cursor.execute(
        "UPDATE names SET religion = ? WHERE country_code = ? AND religion IS NULL",
        (religion, country_code)
    )
    updated += cursor.rowcount

conn.commit()
print(f"  ✓ {updated:,} kayıt güncellendi")

# Infer religion from name patterns
print("\n🔄 İsim pattern'lerinden din tahmini...")

# Islam
cursor.execute("""
    UPDATE names SET religion = 'Islam'
    WHERE religion IS NULL
    AND (
        name LIKE 'muhammad%' OR name LIKE 'ahmed%' OR name LIKE 'ali%'
        OR name LIKE 'hassan%' OR name LIKE 'hussain%' OR name LIKE 'fatima%'
        OR name LIKE 'abd%' OR name LIKE 'abu%' OR name LIKE '%ullah'
        OR name LIKE '%din'
    )
""")
islam_count = cursor.rowcount
print(f"  → Islam: {islam_count:,} kayıt")

# Hinduism
cursor.execute("""
    UPDATE names SET religion = 'Hinduism'
    WHERE religion IS NULL
    AND (
        name LIKE '%kumar' OR name LIKE '%singh' OR name LIKE '%sharma'
        OR name LIKE '%patel' OR name LIKE '%reddy'
    )
""")
hindu_count = cursor.rowcount
print(f"  → Hinduism: {hindu_count:,} kayıt")

# Judaism
cursor.execute("""
    UPDATE names SET religion = 'Judaism'
    WHERE religion IS NULL
    AND (
        name LIKE '%stein' OR name LIKE '%berg' OR name LIKE '%man'
        OR name LIKE '%witz' OR name LIKE '%feld' OR name LIKE '%baum'
    )
""")
jewish_count = cursor.rowcount
print(f"  → Judaism: {jewish_count:,} kayıt")

conn.commit()

# Final statistics
print("\n" + "="*80)
print("GÜNCEL İSTATİSTİKLER")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM names WHERE religion IS NOT NULL")
with_religion_final = cursor.fetchone()[0]
print(f"\n📊 Din bilgisi olan: {with_religion_final:,} ({with_religion_final/total*100:.1f}%)")

cursor.execute("SELECT region, COUNT(*) FROM names GROUP BY region ORDER BY COUNT(*) DESC")
print(f"\n📊 Bölge dağılımı:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL GROUP BY religion ORDER BY COUNT(*) DESC")
print(f"\n📊 Din dağılımı:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT COUNT(DISTINCT country_code) FROM names")
countries = cursor.fetchone()[0]
print(f"\n📊 Ülke sayısı: {countries}")

# Africa statistics
cursor.execute("SELECT COUNT(*) FROM names WHERE region = 'Africa'")
africa_count = cursor.fetchone()[0]
print(f"\n🌍 Africa kayıt sayısı: {africa_count:,}")

cursor.execute("SELECT country_code, COUNT(*) FROM names WHERE region = 'Africa' GROUP BY country_code ORDER BY COUNT(*) DESC LIMIT 10")
print(f"\n🌍 Africa'dan ilk 10 ülke:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

conn.close()

db_size_mb = DB_FILE.stat().st_size / (1024 * 1024)
print(f"\n💾 Veritabanı boyutu: {db_size_mb:.2f} MB")

print("\n" + "="*80)
print("✅ DİN BİLGİSİ EKLENDİ!")
print("="*80)
