#!/usr/bin/env python3
"""
Direct Database Creation - Skip CSV merge, build SQLite directly
Much faster by using chunked reads and SQL INSERT
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

# Remove old database
if DB_FILE.exists():
    DB_FILE.unlink()
    print(f"🗑️  Eski veritabanı silindi")

# Metadata mappings
COUNTRY_REGIONS = {
    'USA': 'Americas', 'CAN': 'Americas', 'MEX': 'Americas', 'BRA': 'Americas',
    'GBR': 'Europe', 'FRA': 'Europe', 'DEU': 'Europe', 'ITA': 'Europe',
    'ESP': 'Europe', 'RUS': 'Europe', 'POL': 'Europe', 'CHN': 'Asia',
    'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia', 'TUR': 'Asia',
    'EGY': 'Africa', 'ZAF': 'Africa', 'AUS': 'Oceania', 'NZL': 'Oceania',
}

COUNTRY_LANGUAGES = {
    'USA': 'English', 'GBR': 'English', 'CAN': 'English', 'AUS': 'English',
    'ESP': 'Spanish', 'MEX': 'Spanish', 'FRA': 'French', 'DEU': 'German',
    'CHN': 'Chinese', 'JPN': 'Japanese', 'KOR': 'Korean', 'RUS': 'Russian',
    'ITA': 'Italian', 'PRT': 'Portuguese', 'BRA': 'Portuguese', 'TUR': 'Turkish',
}

def normalize_name(name):
    if not name or pd.isna(name):
        return None
    return unidecode(str(name).strip().lower())

def normalize_country(country_name):
    if not country_name or pd.isna(country_name):
        return None
    manual = {'United States': 'USA', 'UK': 'GBR', 'Russia': 'RUS', 'Turkey': 'TUR'}
    if country_name in manual:
        return manual[country_name]
    try:
        country = pycountry.countries.search_fuzzy(str(country_name))[0]
        return country.alpha_3
    except:
        return None

def infer_gender(name):
    if not name:
        return None
    name_lower = str(name).lower()
    if name_lower.endswith(('a', 'ia', 'ina', 'ella')):
        return 'F'
    elif name_lower.endswith(('o', 'os', 'us', 'an')):
        return 'M'
    return None

print("="*80)
print("DIRECT DATABASE CREATION")
print("="*80)

# Create database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE names (
        name TEXT NOT NULL,
        name_type TEXT,
        country_code TEXT,
        region TEXT,
        language TEXT,
        gender TEXT,
        source TEXT,
        PRIMARY KEY (name, name_type, country_code)
    )
""")

total_inserted = 0

# 1. Olympics (chunk processing)
print("\n🏅 Olympics Dataset...")
olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
if olympics_file.exists():
    chunk_size = 10000
    count = 0
    for chunk in pd.read_csv(olympics_file, chunksize=chunk_size):
        records = []

        for _, row in chunk.iterrows():
            country = normalize_country(row.get('region'))
            if not country:
                continue

            first = normalize_name(row.get('first_name'))
            last = normalize_name(row.get('last_name'))

            if first and len(first) > 1:
                records.append((
                    first, 'first', country,
                    COUNTRY_REGIONS.get(country, 'Other'),
                    COUNTRY_LANGUAGES.get(country),
                    infer_gender(first),
                    'olympics'
                ))

            if last and len(last) > 1 and last != first:
                records.append((
                    last, 'last', country,
                    COUNTRY_REGIONS.get(country, 'Other'),
                    COUNTRY_LANGUAGES.get(country),
                    None,
                    'olympics'
                ))

        cursor.executemany(
            "INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?)",
            records
        )
        count += len(records)

    conn.commit()
    print(f"  ✓ {count:,} kayıt eklendi")
    total_inserted += count

# 2. US Census Surnames
print("\n🇺🇸 US Census Surnames...")
us_surnames = RAW_DIR / "comprehensive" / "us_surnames.csv"
if us_surnames.exists():
    df = pd.read_csv(us_surnames, nrows=50000)  # Limit
    records = []

    for name_val in df.iloc[:, 0]:  # First column
        name = normalize_name(name_val)
        if name and len(name) > 1:
            records.append((name, 'last', 'USA', 'Americas', 'English', None, 'us_census'))

    cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?)", records)
    conn.commit()
    print(f"  ✓ {len(records):,} kayıt eklendi")
    total_inserted += len(records)

# 3. US Baby Names
print("\n👶 US Baby Names...")
us_baby = RAW_DIR / "comprehensive" / "us_baby_names.csv"
if us_baby.exists():
    df = pd.read_csv(us_baby, nrows=50000)
    records = []

    for _, row in df.iterrows():
        name = normalize_name(row.get('name', ''))
        if name and len(name) > 1:
            records.append((
                name, 'first', 'USA', 'Americas', 'English',
                infer_gender(name), 'us_baby_names'
            ))

    cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?)", records)
    conn.commit()
    print(f"  ✓ {len(records):,} kayıt eklendi")
    total_inserted += len(records)

# 4. World Names DB
print("\n🌍 World Names DB...")
world_names = RAW_DIR / "comprehensive" / "world_names_db.csv"
if world_names.exists():
    df = pd.read_csv(world_names, nrows=50000)
    records = []

    for name_val in df['name']:
        name = normalize_name(name_val)
        if name and len(name) > 2:
            records.append((name, 'last', 'USA', 'Other', None, None, 'world_names_db'))

    cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?)", records)
    conn.commit()
    print(f"  ✓ {len(records):,} kayıt eklendi")
    total_inserted += len(records)

# 5. Phone Directories
print("\n📞 Phone Directories...")
phone_dir = RAW_DIR / "phone_directories"
if phone_dir.exists():
    count = 0
    for file_path in phone_dir.glob("*.txt"):
        parts = file_path.stem.split('_')
        if len(parts) < 1 or len(parts[0]) > 3:
            continue

        country_code = parts[0].upper()
        is_surname = 'surname' in file_path.stem.lower()
        records = []

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                name = normalize_name(line.strip())
                if name and len(name) > 1:
                    records.append((
                        name,
                        'last' if is_surname else 'first',
                        country_code,
                        COUNTRY_REGIONS.get(country_code, 'Other'),
                        COUNTRY_LANGUAGES.get(country_code),
                        None if is_surname else infer_gender(name),
                        'phone_directory'
                    ))

        cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?)", records)
        count += len(records)

    conn.commit()
    print(f"  ✓ {count:,} kayıt eklendi")
    total_inserted += count

# Create indexes
print("\n🔍 İndeksler oluşturuluyor...")
cursor.execute("CREATE INDEX idx_name ON names(name)")
cursor.execute("CREATE INDEX idx_country ON names(country_code)")
cursor.execute("CREATE INDEX idx_name_type ON names(name_type)")
conn.commit()

# Statistics
print("\n" + "="*80)
print("VERİTABANI İSTATİSTİKLERİ")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM names")
total = cursor.fetchone()[0]
print(f"\n📊 Toplam kayıt: {total:,}")

cursor.execute("SELECT name_type, COUNT(*) FROM names GROUP BY name_type")
print(f"\n📊 İsim tipi:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT region, COUNT(*) FROM names GROUP BY region ORDER BY COUNT(*) DESC")
print(f"\n📊 Bölge:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT source, COUNT(*) FROM names GROUP BY source ORDER BY COUNT(*) DESC")
print(f"\n📊 Kaynak:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT gender, COUNT(*) FROM names WHERE gender IS NOT NULL GROUP BY gender")
print(f"\n📊 Gender:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Optimize
print("\n🗜️  Veritabanı optimize ediliyor...")
cursor.execute("VACUUM")
conn.commit()

conn.close()

db_size_mb = DB_FILE.stat().st_size / (1024 * 1024)
print(f"\n💾 Veritabanı boyutu: {db_size_mb:.2f} MB")

print("\n" + "="*80)
print(f"✅ VERİTABANI OLUŞTURULDU: {DB_FILE}")
print(f"✅ TOPLAM: {total:,} KAYIT")
print("="*80)
