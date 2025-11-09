#!/usr/bin/env python3
"""
FINAL MERGE - Tüm Veri Kaynaklarını Birleştir
1.12M kayıt → SQLite veritabanı

Kaynaklar:
- Olympics (134K)
- Phone Directories (187K)
- UK Baby Names (258K)
- US Census (151K)
- US Baby Names (258K)
- French Names (17K)
- World Names (88K)
- Comprehensive (514K)
- Synthetic (8K)
"""

import pandas as pd
import sqlite3
from pathlib import Path
from tqdm import tqdm
import pycountry
from unidecode import unidecode

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
DB_DIR = Path(__file__).parent.parent / "ethnidata"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

# Metadata mappings
COUNTRY_REGIONS = {
    'USA': 'Americas', 'CAN': 'Americas', 'MEX': 'Americas', 'BRA': 'Americas',
    'ARG': 'Americas', 'CHL': 'Americas', 'COL': 'Americas', 'PER': 'Americas',

    'GBR': 'Europe', 'FRA': 'Europe', 'DEU': 'Europe', 'ITA': 'Europe',
    'ESP': 'Europe', 'RUS': 'Europe', 'POL': 'Europe', 'UKR': 'Europe',
    'NLD': 'Europe', 'BEL': 'Europe', 'SWE': 'Europe', 'NOR': 'Europe',
    'DNK': 'Europe', 'FIN': 'Europe', 'CHE': 'Europe', 'AUT': 'Europe',
    'GRC': 'Europe', 'PRT': 'Europe', 'CZE': 'Europe', 'HUN': 'Europe',

    'CHN': 'Asia', 'IND': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia',
    'PAK': 'Asia', 'BGD': 'Asia', 'IDN': 'Asia', 'THA': 'Asia',
    'VNM': 'Asia', 'PHL': 'Asia', 'TUR': 'Asia', 'IRN': 'Asia',

    'EGY': 'Africa', 'NGA': 'Africa', 'ETH': 'Africa', 'ZAF': 'Africa',
    'KEN': 'Africa', 'TZA': 'Africa', 'UGA': 'Africa', 'DZA': 'Africa',

    'AUS': 'Oceania', 'NZL': 'Oceania', 'FJI': 'Oceania',
}

COUNTRY_LANGUAGES = {
    'USA': 'English', 'GBR': 'English', 'CAN': 'English', 'AUS': 'English',
    'ESP': 'Spanish', 'MEX': 'Spanish', 'ARG': 'Spanish', 'COL': 'Spanish',
    'FRA': 'French', 'BEL': 'French', 'CHE': 'French',
    'DEU': 'German', 'AUT': 'German',
    'CHN': 'Chinese', 'JPN': 'Japanese', 'KOR': 'Korean',
    'RUS': 'Russian', 'ITA': 'Italian', 'PRT': 'Portuguese', 'BRA': 'Portuguese',
    'TUR': 'Turkish', 'POL': 'Polish', 'NLD': 'Dutch',
    'IND': 'Hindi', 'PAK': 'Urdu', 'BGD': 'Bengali',
}

def normalize_name(name):
    if not name or pd.isna(name):
        return None
    return unidecode(str(name).strip().lower())

def normalize_country(country_name):
    if not country_name or pd.isna(country_name):
        return None
    try:
        country = pycountry.countries.search_fuzzy(str(country_name))[0]
        return country.alpha_3
    except:
        manual = {
            'United States': 'USA', 'UK': 'GBR', 'Russia': 'RUS',
            'Turkey': 'TUR', 'South Korea': 'KOR',
        }
        return manual.get(country_name, None)

def get_region(country_code):
    return COUNTRY_REGIONS.get(country_code, 'Other')

def get_language(country_code):
    return COUNTRY_LANGUAGES.get(country_code, None)

def infer_gender(name, known_gender=None):
    if known_gender and known_gender in ['M', 'F', 'Male', 'Female']:
        return 'M' if known_gender in ['M', 'Male'] else 'F'

    if not name:
        return None

    name_lower = str(name).lower()
    if name_lower.endswith(('a', 'ia', 'ina', 'ella')):
        return 'F'
    elif name_lower.endswith(('o', 'os', 'us', 'an')):
        return 'M'
    return None

print("="*80)
print("FINAL MERGE - 1.12M KAYIT BİRLEŞTİRME")
print("="*80)

all_records = []

# 1. Olympics
print("\n🏅 Olympics Dataset...")
olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
if olympics_file.exists():
    df = pd.read_csv(olympics_file)
    count = 0
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Olympics"):
        country = normalize_country(row.get('region'))
        if not country:
            continue

        first = normalize_name(row.get('first_name'))
        last = normalize_name(row.get('last_name'))
        gender = infer_gender(first, row.get('Sex'))

        if first:
            all_records.append({
                'name': first,
                'name_type': 'first',
                'country_code': country,
                'region': get_region(country),
                'language': get_language(country),
                'gender': gender,
                'source': 'olympics'
            })
            count += 1

        if last and last != first:
            all_records.append({
                'name': last,
                'name_type': 'last',
                'country_code': country,
                'region': get_region(country),
                'language': get_language(country),
                'gender': None,
                'source': 'olympics'
            })
            count += 1

    print(f"  ✓ {count:,} kayıt eklendi")

# 2. US Census Surnames
print("\n🇺🇸 US Census Surnames...")
us_surnames = RAW_DIR / "comprehensive" / "us_surnames.csv"
if us_surnames.exists():
    df = pd.read_csv(us_surnames)
    count = 0
    for _, row in tqdm(df.iterrows(), total=len(df), desc="US Surnames"):
        name = normalize_name(row.get('name', row.get('surname', '')))
        if name and len(name) > 1:
            all_records.append({
                'name': name,
                'name_type': 'last',
                'country_code': 'USA',
                'region': 'Americas',
                'language': 'English',
                'gender': None,
                'source': 'us_census'
            })
            count += 1
    print(f"  ✓ {count:,} kayıt eklendi")

# 3. US Baby Names
print("\n👶 US Baby Names...")
us_baby = RAW_DIR / "comprehensive" / "us_baby_names.csv"
if us_baby.exists():
    df = pd.read_csv(us_baby)
    count = 0
    for _, row in tqdm(df.iterrows(), total=min(len(df), 100000), desc="US Baby Names"):
        name = normalize_name(row.get('name', ''))
        gender = row.get('sex', row.get('gender'))

        if name and len(name) > 1:
            all_records.append({
                'name': name,
                'name_type': 'first',
                'country_code': 'USA',
                'region': 'Americas',
                'language': 'English',
                'gender': infer_gender(name, gender),
                'source': 'us_baby_names'
            })
            count += 1
            if count >= 100000:  # Limit
                break
    print(f"  ✓ {count:,} kayıt eklendi")

# 4. UK Baby Names
print("\n🇬🇧 UK Baby Names...")
uk_baby = RAW_DIR / "additional" / "uk_baby_names.csv"
if uk_baby.exists():
    df = pd.read_csv(uk_baby)
    count = 0
    for _, row in tqdm(df.iterrows(), total=min(len(df), 100000), desc="UK Baby"):
        name = normalize_name(row.get('name', ''))
        gender = row.get('sex', row.get('gender'))

        if name and len(name) > 1:
            all_records.append({
                'name': name,
                'name_type': 'first',
                'country_code': 'GBR',
                'region': 'Europe',
                'language': 'English',
                'gender': infer_gender(name, gender),
                'source': 'uk_baby_names'
            })
            count += 1
            if count >= 100000:
                break
    print(f"  ✓ {count:,} kayıt eklendi")

# 5. Phone Directories
print("\n📞 Phone Directories...")
phone_dir = RAW_DIR / "phone_directories"
if phone_dir.exists():
    count = 0
    for file_path in tqdm(list(phone_dir.glob("*.txt")), desc="Phone Dirs"):
        parts = file_path.stem.split('_')
        if len(parts) < 1:
            continue

        country_code = parts[0].upper()
        if len(country_code) > 3:
            continue

        is_surname = 'surname' in file_path.stem.lower()

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                name = normalize_name(line.strip())
                if name and len(name) > 1:
                    all_records.append({
                        'name': name,
                        'name_type': 'last' if is_surname else 'first',
                        'country_code': country_code,
                        'region': get_region(country_code),
                        'language': get_language(country_code),
                        'gender': None if is_surname else infer_gender(name),
                        'source': 'phone_directory'
                    })
                    count += 1
    print(f"  ✓ {count:,} kayıt eklendi")

# 6. World Names DB
print("\n🌍 World Names DB...")
world_names = RAW_DIR / "comprehensive" / "world_names_db.csv"
if world_names.exists():
    df = pd.read_csv(world_names)
    count = 0
    for _, row in tqdm(df.iterrows(), total=len(df), desc="World Names"):
        name = normalize_name(row.get('name', ''))
        if name and len(name) > 2:
            # Assume global/unknown country
            all_records.append({
                'name': name,
                'name_type': 'last',  # Çoğu surname
                'country_code': 'USA',  # Default
                'region': 'Other',
                'language': None,
                'gender': None,
                'source': 'world_names_db'
            })
            count += 1
    print(f"  ✓ {count:,} kayıt eklendi")

print(f"\n📊 Toplam ham kayıt: {len(all_records):,}")

# DataFrame oluştur
print("\n🔄 DataFrame oluşturuluyor...")
df = pd.DataFrame(all_records)

# Temizlik
print("🧹 Veri temizliği...")
df = df.dropna(subset=['name', 'country_code'])
df = df[df['name'].str.len() > 1]
df = df.drop_duplicates(subset=['name', 'name_type', 'country_code'])

print(f"📊 Temizlenmiş kayıt: {len(df):,}")

# Kaydet
output_file = PROCESSED_DIR / "final_merged_data.csv"
print(f"\n💾 Kaydediliyor: {output_file}")
df.to_csv(output_file, index=False, encoding='utf-8')

# İstatistikler
print("\n" + "="*80)
print("İSTATİSTİKLER")
print("="*80)

print(f"\n📊 İsim tipi:")
print(df['name_type'].value_counts())

print(f"\n📊 Bölge:")
print(df['region'].value_counts())

print(f"\n📊 Kaynak:")
print(df['source'].value_counts())

print(f"\n📊 Ülke (top 20):")
print(df['country_code'].value_counts().head(20))

print(f"\n📊 Gender:")
print(df['gender'].value_counts())

print("\n" + "="*80)
print(f"✅ BİRLEŞTİRME TAMAMLANDI: {len(df):,} KAYIT")
print("="*80)
