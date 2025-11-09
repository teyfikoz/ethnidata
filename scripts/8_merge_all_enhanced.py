#!/usr/bin/env python3
"""
Gelişmiş Veri Birleştirme - Tüm kaynaklar + Ek özellikler
Eklenecek özellikler:
- Gender (Cinsiyet)
- Region (Bölge: Europe, Asia, Americas, Africa, Oceania)
- Language (Yaygın dil)
"""

import pandas as pd
from pathlib import Path
from unidecode import unidecode
import pycountry
from collections import Counter

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Ülke -> Bölge mapping
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
    'IRQ': 'Asia', 'SAU': 'Asia', 'ARE': 'Asia', 'ISR': 'Asia',

    'EGY': 'Africa', 'NGA': 'Africa', 'ETH': 'Africa', 'ZAF': 'Africa',
    'KEN': 'Africa', 'TZA': 'Africa', 'UGA': 'Africa', 'DZA': 'Africa',
    'MAR': 'Africa', 'GHA': 'Africa',

    'AUS': 'Oceania', 'NZL': 'Oceania', 'FJI': 'Oceania', 'PNG': 'Oceania',
}

# Ülke -> Ana Dil mapping
COUNTRY_LANGUAGES = {
    'USA': 'English', 'GBR': 'English', 'CAN': 'English', 'AUS': 'English',
    'NZL': 'English', 'IRL': 'English', 'ZAF': 'English',

    'ESP': 'Spanish', 'MEX': 'Spanish', 'ARG': 'Spanish', 'COL': 'Spanish',
    'PER': 'Spanish', 'VEN': 'Spanish', 'CHL': 'Spanish',

    'FRA': 'French', 'BEL': 'French', 'CHE': 'French', 'CAN': 'French',

    'DEU': 'German', 'AUT': 'German', 'CHE': 'German',

    'CHN': 'Chinese', 'TWN': 'Chinese', 'SGP': 'Chinese',

    'JPN': 'Japanese',
    'KOR': 'Korean', 'PRK': 'Korean',

    'RUS': 'Russian', 'UKR': 'Russian', 'BLR': 'Russian',

    'ITA': 'Italian',
    'PRT': 'Portuguese', 'BRA': 'Portuguese',

    'TUR': 'Turkish',
    'POL': 'Polish',
    'NLD': 'Dutch',
    'SWE': 'Swedish',
    'NOR': 'Norwegian',
    'DNK': 'Danish',
    'FIN': 'Finnish',

    'IND': 'Hindi', 'PAK': 'Urdu', 'BGD': 'Bengali',
    'IRN': 'Persian', 'SAU': 'Arabic', 'EGY': 'Arabic',
}

# Gender patterns (basit gender tahmin)
MALE_NAME_ENDINGS = ['o', 'os', 'us', 'is', 'an', 'en', 'ar', 'or']
FEMALE_NAME_ENDINGS = ['a', 'ia', 'ina', 'ella', 'ette', 'ie', 'y']

def normalize_country(country_name):
    """Ülke isimlerini ISO 3166-1 alpha-3'e çevir"""
    if not country_name or pd.isna(country_name):
        return None

    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_3
    except:
        manual = {
            'United States': 'USA', 'UK': 'GBR', 'Russia': 'RUS',
            'Turkey': 'TUR', 'South Korea': 'KOR', 'North Korea': 'PRK',
        }
        return manual.get(country_name, None)

def normalize_name(name):
    """İsim normalizasyonu"""
    if not name or pd.isna(name):
        return None
    return unidecode(str(name).strip().lower())

def infer_gender(name):
    """Basit gender tahmini (isim sonuna göre)"""
    if not name:
        return None

    name_lower = name.lower()

    # Female endings
    for ending in FEMALE_NAME_ENDINGS:
        if name_lower.endswith(ending):
            return 'F'

    # Male endings
    for ending in MALE_NAME_ENDINGS:
        if name_lower.endswith(ending):
            return 'M'

    return None  # Unknown

def get_region(country_code):
    """Ülke kodundan bölge al"""
    return COUNTRY_REGIONS.get(country_code, 'Other')

def get_language(country_code):
    """Ülke kodundan ana dili al"""
    return COUNTRY_LANGUAGES.get(country_code, None)

print("="*70)
print("GELİŞMİŞ VERİ BİRLEŞTİRME - TÜM KAYNAKLAR")
print("="*70)

all_data = []

# 1. Olympics
print("\n🏅 Olympics Dataset...")
olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
if olympics_file.exists():
    df = pd.read_csv(olympics_file)
    for _, row in df.iterrows():
        first_norm = normalize_name(row.get('first_name'))
        last_norm = normalize_name(row.get('last_name'))
        country = normalize_country(row.get('region'))

        if country:
            if first_norm:
                all_data.append({
                    'name': first_norm,
                    'name_type': 'first',
                    'country_code': country,
                    'region': get_region(country),
                    'language': get_language(country),
                    'gender': row.get('Sex', infer_gender(first_norm)),
                    'ethnicity': None,
                    'source': 'olympics'
                })

            if last_norm and last_norm != first_norm:
                all_data.append({
                    'name': last_norm,
                    'name_type': 'last',
                    'country_code': country,
                    'region': get_region(country),
                    'language': get_language(country),
                    'gender': None,  # Surnames don't have gender
                    'ethnicity': None,
                    'source': 'olympics'
                })

    print(f"  ✓ {len(all_data)} kayıt eklendi")

# 2. Phone Directories
print("\n📞 Phone Directories...")
phone_dir = RAW_DIR / "phone_directories"
start_len = len(all_data)

if phone_dir.exists():
    for file_path in phone_dir.glob("*.txt"):
        filename = file_path.stem
        parts = filename.split('_')

        if len(parts) >= 1:
            country_code = parts[0].upper()
            if len(country_code) > 3:
                continue

            is_surname = 'surname' in filename.lower()

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    name = normalize_name(line.strip())
                    if name:
                        all_data.append({
                            'name': name,
                            'name_type': 'last' if is_surname else 'first',
                            'country_code': country_code,
                            'region': get_region(country_code),
                            'language': get_language(country_code),
                            'gender': None if is_surname else infer_gender(name),
                            'ethnicity': None,
                            'source': 'phone_directory'
                        })

print(f"  ✓ {len(all_data) - start_len} kayıt eklendi")

# 3. UK Baby Names
print("\n🇬🇧 UK Baby Names...")
uk_file = RAW_DIR / "additional" / "uk_baby_names.csv"
start_len = len(all_data)

if uk_file.exists():
    df = pd.read_csv(uk_file)

    for _, row in df.iterrows():
        name = normalize_name(row.get('name', ''))
        sex = row.get('sex', row.get('gender', None))

        if name:
            all_data.append({
                'name': name,
                'name_type': 'first',
                'country_code': 'GBR',
                'region': 'Europe',
                'language': 'English',
                'gender': sex,
                'ethnicity': None,
                'source': 'uk_baby_names'
            })

print(f"  ✓ {len(all_data) - start_len} kayıt eklendi")

# 4. French Names
print("\n🇫🇷 French Names...")
fr_file = RAW_DIR / "additional" / "french_names.csv"
start_len = len(all_data)

if fr_file.exists():
    df = pd.read_csv(fr_file)

    for _, row in df.iterrows():
        name = normalize_name(row.get('name', row.get('Country Name', '')))

        if name and len(name) > 2:
            all_data.append({
                'name': name,
                'name_type': 'first',
                'country_code': 'FRA',
                'region': 'Europe',
                'language': 'French',
                'gender': infer_gender(name),
                'ethnicity': None,
                'source': 'french_names'
            })

print(f"  ✓ {len(all_data) - start_len} kayıt eklendi")

# DataFrame oluştur
print(f"\n📊 Toplam ham kayıt: {len(all_data):,}")

df = pd.DataFrame(all_data)

# Temizlik
df = df.dropna(subset=['name', 'country_code'])
df = df[df['name'].str.len() > 1]  # Çok kısa isimleri çıkar
df = df[df['country_code'].notna()]

print(f"📊 Temizlenmiş kayıt: {len(df):,}")

# Kaydet
output_file = PROCESSED_DIR / "merged_names_enhanced.csv"
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"\n✅ Kaydedildi: {output_file}")

# İstatistikler
print("\n" + "="*70)
print("İSTATİSTİKLER")
print("="*70)

print(f"\n📊 Kaynak dağılımı:")
print(df['source'].value_counts())

print(f"\n📊 İsim tipi:")
print(df['name_type'].value_counts())

print(f"\n📊 Bölge dağılımı:")
print(df['region'].value_counts())

print(f"\n📊 Dil dağılımı (top 15):")
print(df['language'].value_counts().head(15))

print(f"\n📊 Gender dağılımı:")
print(df['gender'].value_counts())

print(f"\n📊 Ülke dağılımı (top 20):")
print(df['country_code'].value_counts().head(20))

print("\n" + "="*70)
print(f"✅ TAMAMLANDI - {len(df):,} KAY İT")
print("="*70)
