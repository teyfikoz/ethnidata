#!/usr/bin/env python3
"""
Tam Veritabanı Oluşturma - DİN BİLGİSİ İLE
- Tüm Olympics verisi
- Tüm Phone Directory verisi
- Din bilgisi eklendi
- Africa kıtası eklendi
- Gelişmiş ülke-bölge mapping'i
"""

import pandas as pd
import sqlite3
from pathlib import Path
import pycountry
from unidecode import unidecode
import json

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
DB_DIR = Path(__file__).parent.parent / "ethnidata"
DB_FILE = DB_DIR / "ethnidata.db"

DB_DIR.mkdir(parents=True, exist_ok=True)

# Remove old database
if DB_FILE.exists():
    DB_FILE.unlink()
    print(f"🗑️  Eski veritabanı silindi")

# Gelişmiş Metadata Mappings
COUNTRY_REGIONS = {
    # Americas
    'USA': 'Americas', 'CAN': 'Americas', 'MEX': 'Americas', 'BRA': 'Americas',
    'ARG': 'Americas', 'CHL': 'Americas', 'COL': 'Americas', 'PER': 'Americas',
    'VEN': 'Americas', 'ECU': 'Americas', 'BOL': 'Americas', 'PRY': 'Americas',
    'URY': 'Americas', 'CUB': 'Americas', 'DOM': 'Americas', 'HTI': 'Americas',
    'JAM': 'Americas', 'CRI': 'Americas', 'PAN': 'Americas', 'GTM': 'Americas',

    # Europe
    'GBR': 'Europe', 'FRA': 'Europe', 'DEU': 'Europe', 'ITA': 'Europe',
    'ESP': 'Europe', 'RUS': 'Europe', 'POL': 'Europe', 'UKR': 'Europe',
    'NLD': 'Europe', 'BEL': 'Europe', 'SWE': 'Europe', 'NOR': 'Europe',
    'DNK': 'Europe', 'FIN': 'Europe', 'CHE': 'Europe', 'AUT': 'Europe',
    'GRC': 'Europe', 'PRT': 'Europe', 'CZE': 'Europe', 'HUN': 'Europe',
    'ROU': 'Europe', 'BGR': 'Europe', 'SRB': 'Europe', 'HRV': 'Europe',
    'SVK': 'Europe', 'SVN': 'Europe', 'LTU': 'Europe', 'LVA': 'Europe',
    'EST': 'Europe', 'IRL': 'Europe', 'ISL': 'Europe', 'ALB': 'Europe',

    # Asia
    'CHN': 'Asia', 'IND': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia',
    'PAK': 'Asia', 'BGD': 'Asia', 'IDN': 'Asia', 'THA': 'Asia',
    'VNM': 'Asia', 'PHL': 'Asia', 'TUR': 'Asia', 'IRN': 'Asia',
    'IRQ': 'Asia', 'SAU': 'Asia', 'ARE': 'Asia', 'ISR': 'Asia',
    'JOR': 'Asia', 'LBN': 'Asia', 'SYR': 'Asia', 'YEM': 'Asia',
    'KWT': 'Asia', 'QAT': 'Asia', 'OMN': 'Asia', 'BHR': 'Asia',
    'AFG': 'Asia', 'KAZ': 'Asia', 'UZB': 'Asia', 'TKM': 'Asia',
    'KGZ': 'Asia', 'TJK': 'Asia', 'MNG': 'Asia', 'NPL': 'Asia',
    'LKA': 'Asia', 'MMR': 'Asia', 'KHM': 'Asia', 'LAO': 'Asia',
    'SGP': 'Asia', 'MYS': 'Asia', 'TWN': 'Asia',

    # Africa
    'EGY': 'Africa', 'NGA': 'Africa', 'ETH': 'Africa', 'ZAF': 'Africa',
    'KEN': 'Africa', 'TZA': 'Africa', 'UGA': 'Africa', 'DZA': 'Africa',
    'MAR': 'Africa', 'TUN': 'Africa', 'LBY': 'Africa', 'SDN': 'Africa',
    'GHA': 'Africa', 'CMR': 'Africa', 'CIV': 'Africa', 'AGO': 'Africa',
    'MOZ': 'Africa', 'MDG': 'Africa', 'ZWE': 'Africa', 'ZMB': 'Africa',
    'MWI': 'Africa', 'SEN': 'Africa', 'MLI': 'Africa', 'NER': 'Africa',
    'TCD': 'Africa', 'SOM': 'Africa', 'RWA': 'Africa', 'BDI': 'Africa',
    'BWA': 'Africa', 'NAM': 'Africa', 'LSO': 'Africa', 'SWZ': 'Africa',

    # Oceania
    'AUS': 'Oceania', 'NZL': 'Oceania', 'FJI': 'Oceania', 'PNG': 'Oceania',
    'WSM': 'Oceania', 'TON': 'Oceania', 'VUT': 'Oceania', 'SLB': 'Oceania',
}

COUNTRY_LANGUAGES = {
    'USA': 'English', 'GBR': 'English', 'CAN': 'English', 'AUS': 'English',
    'NZL': 'English', 'IRL': 'English', 'ZAF': 'English', 'NGA': 'English',

    'ESP': 'Spanish', 'MEX': 'Spanish', 'ARG': 'Spanish', 'COL': 'Spanish',
    'PER': 'Spanish', 'VEN': 'Spanish', 'CHL': 'Spanish', 'ECU': 'Spanish',

    'FRA': 'French', 'BEL': 'French', 'CHE': 'French', 'CAN': 'French',
    'SEN': 'French', 'CIV': 'French', 'CMR': 'French', 'MLI': 'French',

    'DEU': 'German', 'AUT': 'German', 'CHE': 'German',

    'CHN': 'Chinese', 'TWN': 'Chinese', 'SGP': 'Chinese',
    'JPN': 'Japanese', 'KOR': 'Korean',

    'RUS': 'Russian', 'UKR': 'Russian', 'KAZ': 'Russian', 'BLR': 'Russian',

    'ITA': 'Italian', 'PRT': 'Portuguese', 'BRA': 'Portuguese',
    'TUR': 'Turkish', 'POL': 'Polish', 'NLD': 'Dutch',

    'IND': 'Hindi', 'PAK': 'Urdu', 'BGD': 'Bengali',
    'IDN': 'Indonesian', 'THA': 'Thai', 'VNM': 'Vietnamese',
    'PHL': 'Tagalog', 'IRN': 'Persian', 'IRQ': 'Arabic',
    'SAU': 'Arabic', 'EGY': 'Arabic', 'MAR': 'Arabic', 'DZA': 'Arabic',
}

# Din mapping'i yükle
religion_file = RAW_DIR / "religion" / "country_religion_mapping.json"
if religion_file.exists():
    with open(religion_file, 'r', encoding='utf-8') as f:
        religion_data = json.load(f)
        COUNTRY_RELIGION = religion_data['primary_religion']
else:
    COUNTRY_RELIGION = {}

def normalize_name(name):
    if not name or pd.isna(name):
        return None
    return unidecode(str(name).strip().lower())

def normalize_country(country_name):
    if not country_name or pd.isna(country_name):
        return None
    manual = {
        'United States': 'USA', 'UK': 'GBR', 'Great Britain': 'GBR',
        'Russia': 'RUS', 'Turkey': 'TUR', 'South Korea': 'KOR',
        'North Korea': 'PRK', 'Iran': 'IRN', 'Syria': 'SYR'
    }
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
    if name_lower.endswith(('a', 'ia', 'ina', 'ella', 'ette')):
        return 'F'
    elif name_lower.endswith(('o', 'os', 'us', 'an', 'on')):
        return 'M'
    return None

def infer_religion_from_name(name):
    """İsimden din tahmini"""
    if not name:
        return None

    name_lower = str(name).lower()

    # İslam isimleri
    islam_names = ['muhammad', 'ahmed', 'ali', 'hassan', 'hussain', 'fatima',
                   'aisha', 'omar', 'khalid', 'ibrahim', 'yusuf', 'mustafa']
    if any(n in name_lower for n in islam_names):
        return 'Islam'

    if name_lower.startswith(('abd', 'abu', 'al')) or name_lower.endswith(('ullah', 'din')):
        return 'Islam'

    # Hint isimleri
    hindu_suffixes = ['kumar', 'singh', 'sharma', 'patel', 'reddy']
    if any(name_lower.endswith(s) for s in hindu_suffixes):
        return 'Hinduism'

    # Yahudi isimleri
    if name_lower.endswith(('stein', 'berg', 'man', 'witz', 'feld', 'baum')):
        return 'Judaism'

    return None

print("="*80)
print("TAM VERİTABANI OLUŞTURMA - DİN BİLGİSİ İLE")
print("="*80)

# Create database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table with RELIGION column
cursor.execute("""
    CREATE TABLE names (
        name TEXT NOT NULL,
        name_type TEXT,
        country_code TEXT,
        region TEXT,
        language TEXT,
        religion TEXT,
        gender TEXT,
        source TEXT,
        PRIMARY KEY (name, name_type, country_code)
    )
""")

total_inserted = 0

# 1. Olympics (FULL DATA - no limit)
print("\n🏅 Olympics Dataset (TÜM VERİ)...")
olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
if olympics_file.exists():
    chunk_size = 5000
    count = 0
    for chunk in pd.read_csv(olympics_file, chunksize=chunk_size):
        records = []

        for _, row in chunk.iterrows():
            country = normalize_country(row.get('region'))
            if not country:
                continue

            first = normalize_name(row.get('first_name'))
            last = normalize_name(row.get('last_name'))

            religion = COUNTRY_RELIGION.get(country) or infer_religion_from_name(first)

            if first and len(first) > 1:
                records.append((
                    first, 'first', country,
                    COUNTRY_REGIONS.get(country, 'Other'),
                    COUNTRY_LANGUAGES.get(country),
                    religion,
                    infer_gender(first),
                    'olympics'
                ))

            if last and len(last) > 1 and last != first:
                records.append((
                    last, 'last', country,
                    COUNTRY_REGIONS.get(country, 'Other'),
                    COUNTRY_LANGUAGES.get(country),
                    religion,
                    None,
                    'olympics'
                ))

        cursor.executemany(
            "INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?,?)",
            records
        )
        count += len(records)
        if count % 10000 == 0:
            print(f"  → {count:,} kayıt işlendi...")

    conn.commit()
    print(f"  ✓ {count:,} kayıt eklendi")
    total_inserted += count

# 2. US Census Surnames (FULL)
print("\n🇺🇸 US Census Surnames (TÜM VERİ)...")
us_surnames = RAW_DIR / "comprehensive" / "us_surnames.csv"
if us_surnames.exists():
    df = pd.read_csv(us_surnames)  # No limit
    records = []

    for name_val in df.iloc[:, 0]:
        name = normalize_name(name_val)
        if name and len(name) > 1:
            records.append((
                name, 'last', 'USA', 'Americas', 'English',
                'Christianity', None, 'us_census'
            ))

    cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?,?)", records)
    conn.commit()
    print(f"  ✓ {len(records):,} kayıt eklendi")
    total_inserted += len(records)

# 3. US Baby Names (FULL)
print("\n👶 US Baby Names (TÜM VERİ)...")
us_baby = RAW_DIR / "comprehensive" / "us_baby_names.csv"
if us_baby.exists():
    df = pd.read_csv(us_baby)  # No limit
    records = []

    for _, row in df.iterrows():
        name = normalize_name(row.get('name', ''))
        if name and len(name) > 1:
            records.append((
                name, 'first', 'USA', 'Americas', 'English',
                'Christianity', infer_gender(name), 'us_baby_names'
            ))

        if len(records) >= 100000:  # Limit to prevent memory issues
            break

    cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?,?)", records)
    conn.commit()
    print(f"  ✓ {len(records):,} kayıt eklendi")
    total_inserted += len(records)

# 4. World Names DB (FULL)
print("\n🌍 World Names DB (TÜM VERİ)...")
world_names = RAW_DIR / "comprehensive" / "world_names_db.csv"
if world_names.exists():
    df = pd.read_csv(world_names)  # No limit
    records = []

    for name_val in df['name']:
        name = normalize_name(name_val)
        if name and len(name) > 2:
            records.append((
                name, 'last', 'USA', 'Americas', 'English',
                None, None, 'world_names_db'
            ))

    cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?,?)", records)
    conn.commit()
    print(f"  ✓ {len(records):,} kayıt eklendi")
    total_inserted += len(records)

# 5. Phone Directories (FULL - ALL FILES)
print("\n📞 Phone Directories (TÜM DOSYALAR)...")
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
                    religion = COUNTRY_RELIGION.get(country_code) or infer_religion_from_name(name)

                    records.append((
                        name,
                        'last' if is_surname else 'first',
                        country_code,
                        COUNTRY_REGIONS.get(country_code, 'Other'),
                        COUNTRY_LANGUAGES.get(country_code),
                        religion,
                        None if is_surname else infer_gender(name),
                        'phone_directory'
                    ))

        cursor.executemany("INSERT OR IGNORE INTO names VALUES (?,?,?,?,?,?,?,?)", records)
        count += len(records)
        print(f"  → {file_path.name}: {len(records):,} kayıt")

    conn.commit()
    print(f"  ✓ TOPLAM: {count:,} kayıt eklendi")
    total_inserted += count

# Create indexes
print("\n🔍 İndeksler oluşturuluyor...")
cursor.execute("CREATE INDEX idx_name ON names(name)")
cursor.execute("CREATE INDEX idx_country ON names(country_code)")
cursor.execute("CREATE INDEX idx_name_type ON names(name_type)")
cursor.execute("CREATE INDEX idx_religion ON names(religion)")
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

cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL GROUP BY religion ORDER BY COUNT(*) DESC")
print(f"\n📊 Din:")
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
print(f"✅ YENİ: DİN BİLGİSİ EKLENDİ!")
print("="*80)
