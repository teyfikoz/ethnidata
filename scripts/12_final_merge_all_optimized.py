#!/usr/bin/env python3
"""
FINAL MERGE - Optimized Version
Tüm veri kaynaklarını birleştir (vectorized operations)
"""

import pandas as pd
import sqlite3
from pathlib import Path
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

def normalize_name_vectorized(series):
    """Vectorized name normalization"""
    return series.fillna('').astype(str).str.strip().str.lower().apply(unidecode)

def normalize_country_vectorized(series):
    """Vectorized country normalization"""
    manual_map = {
        'United States': 'USA', 'UK': 'GBR', 'Russia': 'RUS',
        'Turkey': 'TUR', 'South Korea': 'KOR',
    }

    def normalize_single(name):
        if not name or pd.isna(name):
            return None
        if name in manual_map:
            return manual_map[name]
        try:
            country = pycountry.countries.search_fuzzy(str(name))[0]
            return country.alpha_3
        except:
            return None

    return series.apply(normalize_single)

def infer_gender_vectorized(names):
    """Vectorized gender inference"""
    def infer_single(name):
        if not name or pd.isna(name):
            return None
        name_lower = str(name).lower()
        if name_lower.endswith(('a', 'ia', 'ina', 'ella')):
            return 'F'
        elif name_lower.endswith(('o', 'os', 'us', 'an')):
            return 'M'
        return None

    return names.apply(infer_single)

print("="*80)
print("FINAL MERGE - OPTIMIZED VERSION")
print("="*80)

all_dfs = []

# 1. Olympics
print("\n🏅 Olympics Dataset...")
olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
if olympics_file.exists():
    df = pd.read_csv(olympics_file)
    print(f"  → Yüklendi: {len(df):,} satır")

    # Vectorized operations
    df['country_code'] = normalize_country_vectorized(df.get('region', pd.Series()))
    df = df.dropna(subset=['country_code'])

    # First names
    first_names = df[['first_name', 'country_code', 'Sex']].copy()
    first_names['name'] = normalize_name_vectorized(first_names['first_name'])
    first_names['name_type'] = 'first'
    first_names['gender'] = infer_gender_vectorized(first_names['name'])
    first_names['source'] = 'olympics'
    first_names = first_names[['name', 'name_type', 'country_code', 'gender', 'source']]
    first_names = first_names[first_names['name'].str.len() > 0]

    # Last names
    last_names = df[['last_name', 'country_code']].copy()
    last_names['name'] = normalize_name_vectorized(last_names['last_name'])
    last_names['name_type'] = 'last'
    last_names['gender'] = None
    last_names['source'] = 'olympics'
    last_names = last_names[['name', 'name_type', 'country_code', 'gender', 'source']]
    last_names = last_names[last_names['name'].str.len() > 0]

    combined = pd.concat([first_names, last_names], ignore_index=True)
    all_dfs.append(combined)
    print(f"  ✓ {len(combined):,} kayıt eklendi")

# 2. US Census Surnames
print("\n🇺🇸 US Census Surnames...")
us_surnames = RAW_DIR / "comprehensive" / "us_surnames.csv"
if us_surnames.exists():
    df = pd.read_csv(us_surnames)
    df['name'] = normalize_name_vectorized(df[df.columns[0]])  # First column
    df = df[df['name'].str.len() > 1]
    df['name_type'] = 'last'
    df['country_code'] = 'USA'
    df['gender'] = None
    df['source'] = 'us_census'
    df = df[['name', 'name_type', 'country_code', 'gender', 'source']]
    all_dfs.append(df)
    print(f"  ✓ {len(df):,} kayıt eklendi")

# 3. US Baby Names
print("\n👶 US Baby Names...")
us_baby = RAW_DIR / "comprehensive" / "us_baby_names.csv"
if us_baby.exists():
    df = pd.read_csv(us_baby, nrows=100000)  # Limit to 100K
    df['name'] = normalize_name_vectorized(df['name'])
    df = df[df['name'].str.len() > 1]
    df['name_type'] = 'first'
    df['country_code'] = 'USA'
    df['gender'] = infer_gender_vectorized(df['name'])
    df['source'] = 'us_baby_names'
    df = df[['name', 'name_type', 'country_code', 'gender', 'source']]
    all_dfs.append(df)
    print(f"  ✓ {len(df):,} kayıt eklendi")

# 4. UK Baby Names
print("\n🇬🇧 UK Baby Names...")
uk_baby = RAW_DIR / "additional" / "uk_baby_names.csv"
if uk_baby.exists():
    df = pd.read_csv(uk_baby, nrows=100000)
    df['name'] = normalize_name_vectorized(df['name'])
    df = df[df['name'].str.len() > 1]
    df['name_type'] = 'first'
    df['country_code'] = 'GBR'
    df['gender'] = infer_gender_vectorized(df['name'])
    df['source'] = 'uk_baby_names'
    df = df[['name', 'name_type', 'country_code', 'gender', 'source']]
    all_dfs.append(df)
    print(f"  ✓ {len(df):,} kayıt eklendi")

# 5. Phone Directories
print("\n📞 Phone Directories...")
phone_dir = RAW_DIR / "phone_directories"
if phone_dir.exists():
    for file_path in phone_dir.glob("*.txt"):
        parts = file_path.stem.split('_')
        if len(parts) < 1 or len(parts[0]) > 3:
            continue

        country_code = parts[0].upper()
        is_surname = 'surname' in file_path.stem.lower()

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            names = [line.strip() for line in f if len(line.strip()) > 1]

        df = pd.DataFrame({'name': names})
        df['name'] = normalize_name_vectorized(df['name'])
        df = df[df['name'].str.len() > 1]
        df['name_type'] = 'last' if is_surname else 'first'
        df['country_code'] = country_code
        df['gender'] = None if is_surname else infer_gender_vectorized(df['name'])
        df['source'] = 'phone_directory'
        all_dfs.append(df)

    total = sum(len(df) for df in all_dfs if 'phone_directory' in df['source'].values)
    print(f"  ✓ {total:,} kayıt eklendi")

# 6. World Names DB
print("\n🌍 World Names DB...")
world_names = RAW_DIR / "comprehensive" / "world_names_db.csv"
if world_names.exists():
    df = pd.read_csv(world_names)
    df['name'] = normalize_name_vectorized(df['name'])
    df = df[df['name'].str.len() > 2]
    df['name_type'] = 'last'
    df['country_code'] = 'USA'  # Default
    df['gender'] = None
    df['source'] = 'world_names_db'
    df = df[['name', 'name_type', 'country_code', 'gender', 'source']]
    all_dfs.append(df)
    print(f"  ✓ {len(df):,} kayıt eklendi")

# Combine all
print("\n🔄 Birleştirme...")
final_df = pd.concat(all_dfs, ignore_index=True)

# Add region and language
print("🗺️  Region ve language ekleniyor...")
final_df['region'] = final_df['country_code'].map(COUNTRY_REGIONS).fillna('Other')
final_df['language'] = final_df['country_code'].map(COUNTRY_LANGUAGES)

# Clean
print("🧹 Temizlik...")
final_df = final_df.dropna(subset=['name', 'country_code'])
final_df = final_df[final_df['name'].str.len() > 1]
final_df = final_df.drop_duplicates(subset=['name', 'name_type', 'country_code'])

print(f"\n📊 Toplam kayıt: {len(final_df):,}")

# Save
output_file = PROCESSED_DIR / "final_merged_data.csv"
print(f"\n💾 Kaydediliyor: {output_file}")
final_df.to_csv(output_file, index=False, encoding='utf-8')

# Stats
print("\n" + "="*80)
print("İSTATİSTİKLER")
print("="*80)

print(f"\n📊 İsim tipi:")
print(final_df['name_type'].value_counts())

print(f"\n📊 Bölge:")
print(final_df['region'].value_counts())

print(f"\n📊 Kaynak:")
print(final_df['source'].value_counts())

print(f"\n📊 Ülke (top 20):")
print(final_df['country_code'].value_counts().head(20))

print(f"\n📊 Gender:")
print(final_df['gender'].value_counts())

print("\n" + "="*80)
print(f"✅ BİRLEŞTİRME TAMAMLANDI: {len(final_df):,} KAYIT")
print("="*80)
