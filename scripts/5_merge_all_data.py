#!/usr/bin/env python3
"""
Tüm veri kaynaklarını birleştir ve normalize et
"""

import json
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

    # pycountry ile eşleştir
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_3  # ISO 3166-1 alpha-3 code (USA, GBR, TUR)
    except:
        # Manuel düzeltmeler
        manual_mapping = {
            'United States': 'USA',
            'United Kingdom': 'GBR',
            'Russia': 'RUS',
            'Turkey': 'TUR',
            'Türkiye': 'TUR',
            'South Korea': 'KOR',
            'North Korea': 'PRK',
        }
        return manual_mapping.get(country_name, None)

def normalize_name(name):
    """İsimleri normalize et (lowercase, unicode)"""

    if not name or pd.isna(name):
        return None

    # Küçük harfe çevir, unicode normalize
    normalized = unidecode(str(name).strip().lower())
    return normalized if normalized else None

def load_wikipedia_data():
    """Wikipedia/Wikidata verilerini yükle"""

    print("📚 Wikipedia verileri yükleniyor...")

    file_path = RAW_DIR / "wikipedia" / "wikidata_persons.json"

    if not file_path.exists():
        print(f"  ⚠️  Dosya bulunamadı: {file_path}")
        return pd.DataFrame()

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Parse names
    df['first_name'] = df['name'].str.split().str[0]
    df['last_name'] = df['name'].str.split().str[-1]

    # Normalize
    df['first_name_norm'] = df['first_name'].apply(normalize_name)
    df['last_name_norm'] = df['last_name'].apply(normalize_name)
    df['country_code'] = df['country'].apply(normalize_country_name)

    # Columns
    result = df[['first_name_norm', 'last_name_norm', 'country_code', 'ethnicity']].copy()
    result['source'] = 'wikipedia'

    print(f"  ✓ {len(result)} kayıt yüklendi")
    return result

def load_olympics_data():
    """Olympics verilerini yükle"""

    print("🏅 Olympics verileri yükleniyor...")

    file_path = RAW_DIR / "olympics" / "olympics_names.csv"

    if not file_path.exists():
        print(f"  ⚠️  Dosya bulunamadı: {file_path}")
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    # Normalize
    df['first_name_norm'] = df['first_name'].apply(normalize_name)
    df['last_name_norm'] = df['last_name'].apply(normalize_name)
    df['country_code'] = df['region'].apply(normalize_country_name)

    # Columns
    result = df[['first_name_norm', 'last_name_norm', 'country_code']].copy()
    result['ethnicity'] = None
    result['source'] = 'olympics'

    print(f"  ✓ {len(result)} kayıt yüklendi")
    return result

def load_phone_directories_data():
    """Telefon rehberi verilerini yükle"""

    print("📞 Telefon rehberi verileri yükleniyor...")

    phone_dir = RAW_DIR / "phone_directories"

    if not phone_dir.exists():
        print(f"  ⚠️  Klasör bulunamadı: {phone_dir}")
        return pd.DataFrame()

    all_data = []

    # Tüm .txt dosyalarını oku
    for file_path in phone_dir.glob("*.txt"):
        # Dosya adından ülke kodu çıkar (örn: us_surnames.txt -> US)
        filename = file_path.stem
        parts = filename.split('_')

        if len(parts) >= 1:
            country_code = parts[0].upper()

            # İsim tipini belirle
            is_surname = 'surname' in filename.lower()

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    name = line.strip()
                    if name:
                        normalized = normalize_name(name)

                        all_data.append({
                            'first_name_norm': None if is_surname else normalized,
                            'last_name_norm': normalized if is_surname else None,
                            'country_code': country_code if len(country_code) <= 3 else None,
                            'ethnicity': None,
                            'source': 'phone_directory'
                        })

    df = pd.DataFrame(all_data)
    print(f"  ✓ {len(df)} kayıt yüklendi")
    return df

def merge_all_sources():
    """Tüm kaynakları birleştir"""

    print("\n🔗 Tüm kaynaklar birleştiriliyor...\n")

    # Tüm kaynakları yükle
    wiki_df = load_wikipedia_data()
    olympics_df = load_olympics_data()
    phone_df = load_phone_directories_data()

    # Birleştir
    all_data = pd.concat([wiki_df, olympics_df, phone_df], ignore_index=True)

    # Temizlik
    all_data = all_data.dropna(subset=['first_name_norm', 'country_code'], how='all')
    all_data = all_data[all_data['country_code'].notna()]

    # Duplicate kontrolü (aynı isim-ülke çifti)
    print(f"\n📊 Toplam kayıt: {len(all_data)}")
    print(f"📊 Benzersiz first name-country: {all_data[['first_name_norm', 'country_code']].drop_duplicates().shape[0]}")
    print(f"📊 Benzersiz last name-country: {all_data[['last_name_norm', 'country_code']].drop_duplicates().shape[0]}")

    # Kaydet
    output_file = PROCESSED_DIR / "merged_names.csv"
    all_data.to_csv(output_file, index=False, encoding='utf-8')

    print(f"\n✅ Birleştirilmiş veri kaydedildi: {output_file}")

    # İstatistikler
    print("\n📊 Kaynak dağılımı:")
    print(all_data['source'].value_counts())

    print("\n📊 Ülke dağılımı (top 30):")
    print(all_data['country_code'].value_counts().head(30))

    return all_data

if __name__ == "__main__":
    merge_all_sources()
