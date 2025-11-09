#!/usr/bin/env python3
"""
Create Database with Sampled Data - Fast Version
Use only 10K samples from each large source
"""

import pandas as pd
import sqlite3
from pathlib import Path
import pycountry
from unidecode import unidecode

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
DB_DIR = Path(__file__).parent.parent / "ethnidata"
DB_FILE = DB_DIR / "names.db"

DB_DIR.mkdir(parents=True, exist_ok=True)

if DB_FILE.exists():
    DB_FILE.unlink()

# Mappings
COUNTRY_REGIONS = {
    'USA': 'Americas', 'CAN': 'Americas', 'MEX': 'Americas', 'BRA': 'Americas',
    'GBR': 'Europe', 'FRA': 'Europe', 'DEU': 'Europe', 'ITA': 'Europe',
    'ESP': 'Europe', 'RUS': 'Europe', 'POL': 'Europe', 'CHN': 'Asia',
    'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia', 'TUR': 'Asia',
}

COUNTRY_LANGUAGES = {
    'USA': 'English', 'GBR': 'English', 'FRA': 'French', 'DEU': 'German',
    'CHN': 'Chinese', 'JPN': 'Japanese', 'KOR': 'Korean', 'RUS': 'Russian',
}

def norm(name):
    if not name or pd.isna(name):
        return None
    return unidecode(str(name).strip().lower())

print("="*80)
print("FAST DATABASE CREATION (SAMPLED DATA)")
print("="*80)

all_records = []

# 1. Olympics - Sample 10K
print("\n🏅 Olympics (sample 10K)...")
oly = RAW_DIR / "olympics" / "olympics_names.csv"
if oly.exists():
    df = pd.read_csv(oly, nrows=10000)
    for _, row in df.iterrows():
        cc = row.get('region', 'USA')
        fn = norm(row.get('first_name'))
        ln = norm(row.get('last_name'))

        if fn:
            all_records.append({
                'name': fn, 'name_type': 'first', 'country_code': cc[:3].upper(),
                'region': COUNTRY_REGIONS.get(cc[:3].upper(), 'Other'),
                'language': COUNTRY_LANGUAGES.get(cc[:3].upper()),
                'gender': 'F' if fn.endswith('a') else ('M' if fn.endswith('o') else None),
                'source': 'olympics'
            })
        if ln and ln != fn:
            all_records.append({
                'name': ln, 'name_type': 'last', 'country_code': cc[:3].upper(),
                'region': COUNTRY_REGIONS.get(cc[:3].upper(), 'Other'),
                'language': COUNTRY_LANGUAGES.get(cc[:3].upper()),
                'gender': None, 'source': 'olympics'
            })
    print(f"  ✓ {len([r for r in all_records if r['source']=='olympics']):,} kayıt")

# 2. US Surnames - Sample 10K
print("\n🇺🇸 US Surnames (sample 10K)...")
us_sur = RAW_DIR / "comprehensive" / "us_surnames.csv"
if us_sur.exists():
    df = pd.read_csv(us_sur, nrows=10000)
    for val in df.iloc[:, 0]:
        n = norm(val)
        if n:
            all_records.append({
                'name': n, 'name_type': 'last', 'country_code': 'USA',
                'region': 'Americas', 'language': 'English',
                'gender': None, 'source': 'us_census'
            })
    print(f"  ✓ ~10K kayıt")

# 3. US Baby Names - Sample 10K
print("\n👶 US Baby Names (sample 10K)...")
us_baby = RAW_DIR / "comprehensive" / "us_baby_names.csv"
if us_baby.exists():
    df = pd.read_csv(us_baby, nrows=10000)
    for _, row in df.iterrows():
        n = norm(row.get('name'))
        if n:
            all_records.append({
                'name': n, 'name_type': 'first', 'country_code': 'USA',
                'region': 'Americas', 'language': 'English',
                'gender': 'F' if n.endswith('a') else None,
                'source': 'us_baby_names'
            })
    print(f"  ✓ ~10K kayıt")

# 4. World Names - Sample 10K
print("\n🌍 World Names (sample 10K)...")
world = RAW_DIR / "comprehensive" / "world_names_db.csv"
if world.exists():
    df = pd.read_csv(world, nrows=10000)
    for val in df['name']:
        n = norm(val)
        if n:
            all_records.append({
                'name': n, 'name_type': 'last', 'country_code': 'USA',
                'region': 'Other', 'language': None,
                'gender': None, 'source': 'world_names'
            })
    print(f"  ✓ ~10K kayıt")

# 5. Phone Directories - All (small files)
print("\n📞 Phone Directories...")
phone_dir = RAW_DIR / "phone_directories"
if phone_dir.exists():
    count = 0
    for fp in phone_dir.glob("*.txt"):
        cc = fp.stem.split('_')[0].upper()[:3]
        is_last = 'surname' in fp.stem.lower()

        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                n = norm(line.strip())
                if n:
                    all_records.append({
                        'name': n, 'name_type': 'last' if is_last else 'first',
                        'country_code': cc,
                        'region': COUNTRY_REGIONS.get(cc, 'Other'),
                        'language': COUNTRY_LANGUAGES.get(cc),
                        'gender': None, 'source': 'phone_dir'
                    })
                    count += 1
    print(f"  ✓ {count:,} kayıt")

print(f"\n📊 Toplam: {len(all_records):,} kayıt")

# Create DataFrame and deduplicate
print("\n🔄 Deduplicate...")
df = pd.DataFrame(all_records)
df = df.drop_duplicates(subset=['name', 'name_type', 'country_code'])
print(f"  → {len(df):,} unique kayıt")

# Save to SQLite
print(f"\n💾 SQLite kaydediliyor: {DB_FILE}")
conn = sqlite3.connect(DB_FILE)
df.to_sql('names', conn, if_exists='replace', index=False)

# Create indexes
cursor = conn.cursor()
cursor.execute("CREATE INDEX idx_name ON names(name)")
cursor.execute("CREATE INDEX idx_country ON names(country_code)")
conn.commit()

# Stats
cursor.execute("SELECT COUNT(*) FROM names")
total = cursor.fetchone()[0]

cursor.execute("SELECT name_type, COUNT(*) FROM names GROUP BY name_type")
print(f"\n📊 İsim tipi:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT region, COUNT(*) FROM names GROUP BY region ORDER BY COUNT(*) DESC")
print(f"\n📊 Bölge:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT source, COUNT(*) FROM names GROUP BY source")
print(f"\n📊 Kaynak:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Optimize
cursor.execute("VACUUM")
conn.commit()
conn.close()

size_mb = DB_FILE.stat().st_size / (1024 * 1024)
print(f"\n💾 Boyut: {size_mb:.2f} MB")

print("\n" + "="*80)
print(f"✅ VERİTABANI HAZIR: {total:,} KAYIT")
print("="*80)
