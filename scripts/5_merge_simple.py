#!/usr/bin/env python3
"""
Sadece Olympics ve Phone Directory verilerini birleştir (hızlı versiyon)
"""

import pandas as pd
from pathlib import Path
from unidecode import unidecode
import pycountry

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def normalize_country_name(country_name):
    """Ülke isimlerini standardize et (ISO 3166)"""
    if not country_name or pd.isna(country_name):
        return None

    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_3
    except:
        manual_mapping = {
            'United States': 'USA', 'UK': 'GBR', 'Russia': 'RUS',
            'Turkey': 'TUR', 'Türkiye': 'TUR', 'South Korea': 'KOR',
        }
        return manual_mapping.get(country_name, None)

def normalize_name(name):
    """İsimleri normalize et"""
    if not name or pd.isna(name):
        return None
    normalized = unidecode(str(name).strip().lower())
    return normalized if normalized else None

print("🔗 Olympics ve Phone Directory birleştiriliyor...\n")

# Olympics
print("🏅 Olympics yükleniyor...")
olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
olympics_df = pd.read_csv(olympics_file)
olympics_df['first_name_norm'] = olympics_df['first_name'].apply(normalize_name)
olympics_df['last_name_norm'] = olympics_df['last_name'].apply(normalize_name)
olympics_df['country_code'] = olympics_df['region'].apply(normalize_country_name)
olympics_result = olympics_df[['first_name_norm', 'last_name_norm', 'country_code']].copy()
olympics_result['ethnicity'] = None
olympics_result['source'] = 'olympics'
print(f"  ✓ {len(olympics_result)} kayıt")

# Phone Directory
print("\n📞 Telefon rehberleri yükleniyor...")
phone_dir = RAW_DIR / "phone_directories"
all_phone = []

for file_path in phone_dir.glob("*.txt"):
    filename = file_path.stem
    parts = filename.split('_')
    if len(parts) >= 1:
        country_code = parts[0].upper()
        is_surname = 'surname' in filename.lower()

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                name = line.strip()
                if name:
                    normalized = normalize_name(name)
                    all_phone.append({
                        'first_name_norm': None if is_surname else normalized,
                        'last_name_norm': normalized if is_surname else None,
                        'country_code': country_code if len(country_code) <= 3 else None,
                        'ethnicity': None,
                        'source': 'phone_directory'
                    })

phone_df = pd.DataFrame(all_phone)
print(f"  ✓ {len(phone_df)} kayıt")

# Birleştir
print("\n🔗 Birleştiriliyor...")
all_data = pd.concat([olympics_result, phone_df], ignore_index=True)
all_data = all_data.dropna(subset=['country_code'])
all_data = all_data[all_data['country_code'].notna()]

print(f"\n📊 Toplam kayıt: {len(all_data):,}")
print(f"📊 Benzersiz first names: {all_data['first_name_norm'].nunique():,}")
print(f"📊 Benzersiz last names: {all_data['last_name_norm'].nunique():,}")

# Kaydet
output_file = PROCESSED_DIR / "merged_names.csv"
all_data.to_csv(output_file, index=False, encoding='utf-8')
print(f"\n✅ Kaydedildi: {output_file}")

print("\n📊 Kaynak dağılımı:")
print(all_data['source'].value_counts())

print("\n📊 Ülke dağılımı (top 20):")
print(all_data['country_code'].value_counts().head(20))
