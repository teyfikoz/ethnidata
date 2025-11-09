#!/usr/bin/env python3
"""
Kapsamlı Veri Kaynakları Toplama
Tüm kıtalar, tüm ülkeler için isim verileri

Kaynaklar:
1. Nüfus daireleri (Census bureaus)
2. Açık devlet verileri (Open government data)
3. GitHub'daki büyük isim veritabanları
4. Akademik veri setleri
"""

import requests
import pandas as pd
from pathlib import Path
import json

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "comprehensive"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_us_census():
    """US Census Bureau - En yaygın isimler"""
    print("🇺🇸 US Census Bureau...")

    # SSA Baby Names (1880-2023)
    urls = {
        'baby_names_national': 'https://www.ssa.gov/oact/babynames/names.zip',
        'baby_names_state': 'https://www.ssa.gov/oact/babynames/state/namesbystate.zip',
    }

    # GitHub mirrors
    github_sources = {
        'us_surnames': 'https://raw.githubusercontent.com/fivethirtyeight/data/master/most-common-name/surnames.csv',
        'us_baby_names': 'https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv',
    }

    total = 0
    for name, url in github_sources.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt: {output}")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_uk_ons():
    """UK Office for National Statistics - Baby names"""
    print("\n🇬🇧 UK ONS Baby Names...")

    # GitHub mirror
    urls = {
        'uk_baby_2020': 'https://raw.githubusercontent.com/datasets/baby-names-england-wales/main/data/baby-names-england-wales-2020.csv',
    }

    total = 0
    for name, url in urls.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_canadian_data():
    """Canadian Open Data - Names"""
    print("\n🇨🇦 Canada Open Data...")

    urls = {
        'canada_names': 'https://raw.githubusercontent.com/datasets/canada-baby-names/main/data/canada-baby-names.csv',
    }

    total = 0
    for name, url in urls.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_european_names():
    """Avrupa ülkeleri isim verileri"""
    print("\n🇪🇺 European Names...")

    sources = {
        'german_names': 'https://raw.githubusercontent.com/datasets/german-names/main/data/names.csv',
        'french_names': 'https://raw.githubusercontent.com/datasets/french-names/main/data/names.csv',
        'spanish_names': 'https://raw.githubusercontent.com/datasets/spanish-names/main/data/names.csv',
        'italian_names': 'https://raw.githubusercontent.com/datasets/italian-names/main/data/names.csv',
    }

    total = 0
    for name, url in sources.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_asian_names():
    """Asya ülkeleri isim verileri"""
    print("\n🌏 Asian Names...")

    sources = {
        'chinese_surnames': 'https://raw.githubusercontent.com/psychbruce/ChineseNames/master/data/Chinese_Names_Corpus.csv',
        'japanese_names': 'https://raw.githubusercontent.com/datasets/japanese-names/main/data/names.csv',
        'korean_names': 'https://raw.githubusercontent.com/datasets/korean-names/main/data/names.csv',
        'indian_names': 'https://raw.githubusercontent.com/datasets/indian-names/main/data/names.csv',
    }

    total = 0
    for name, url in sources.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_github_name_databases():
    """GitHub'daki büyük isim veritabanları"""
    print("\n💾 GitHub Name Databases...")

    # Büyük veritabanları
    sources = {
        'world_names_db': 'https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/surnames/all.txt',
        'global_names': 'https://raw.githubusercontent.com/datasets/population/main/data/population.csv',
    }

    total = 0
    for name, url in sources.items():
        try:
            print(f"  → {name}")

            if url.endswith('.txt'):
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                names = response.text.strip().split('\n')
                df = pd.DataFrame({'name': names})

                output = OUTPUT_DIR / f"{name}.csv"
                df.to_csv(output, index=False)
                print(f"    ✓ {len(df):,} kayıt")
                total += len(df)
            else:
                df = pd.read_csv(url)
                output = OUTPUT_DIR / f"{name}.csv"
                df.to_csv(output, index=False)
                print(f"    ✓ {len(df):,} kayıt")
                total += len(df)

        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_latin_american_names():
    """Latin Amerika ülkeleri"""
    print("\n🌎 Latin American Names...")

    sources = {
        'mexican_names': 'https://raw.githubusercontent.com/datasets/mexican-names/main/data/names.csv',
        'brazilian_names': 'https://raw.githubusercontent.com/datasets/brazilian-names/main/data/names.csv',
        'argentinian_names': 'https://raw.githubusercontent.com/datasets/argentinian-names/main/data/names.csv',
    }

    total = 0
    for name, url in sources.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_african_names():
    """Afrika ülkeleri"""
    print("\n🌍 African Names...")

    sources = {
        'south_african_names': 'https://raw.githubusercontent.com/datasets/south-african-names/main/data/names.csv',
        'nigerian_names': 'https://raw.githubusercontent.com/datasets/nigerian-names/main/data/names.csv',
        'ethiopian_names': 'https://raw.githubusercontent.com/datasets/ethiopian-names/main/data/names.csv',
    }

    total = 0
    for name, url in sources.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def fetch_middle_eastern_names():
    """Orta Doğu ülkeleri"""
    print("\n🕌 Middle Eastern Names...")

    sources = {
        'arabic_names': 'https://raw.githubusercontent.com/datasets/arabic-names/main/data/names.csv',
        'turkish_names': 'https://raw.githubusercontent.com/datasets/turkish-names/main/data/names.csv',
        'persian_names': 'https://raw.githubusercontent.com/datasets/persian-names/main/data/names.csv',
    }

    total = 0
    for name, url in sources.items():
        try:
            print(f"  → {name}")
            df = pd.read_csv(url)
            output = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output, index=False)
            print(f"    ✓ {len(df):,} kayıt")
            total += len(df)
        except Exception as e:
            print(f"    ✗ Hata: {e}")

    return total

def main():
    print("=" * 70)
    print("KAPSAMLI VERİ TOPLAMA - TÜM DÜNYA")
    print("=" * 70)

    total_records = 0

    # Kuzey Amerika
    total_records += fetch_us_census()
    total_records += fetch_canadian_data()

    # Avrupa
    total_records += fetch_uk_ons()
    total_records += fetch_european_names()

    # Asya
    total_records += fetch_asian_names()

    # Latin Amerika
    total_records += fetch_latin_american_names()

    # Afrika
    total_records += fetch_african_names()

    # Orta Doğu
    total_records += fetch_middle_eastern_names()

    # GitHub databases
    total_records += fetch_github_name_databases()

    print("\n" + "=" * 70)
    print(f"✅ TOPLAM YENİ VERİ: {total_records:,} kayıt")
    print("=" * 70)

    # Özet kaydet
    summary = {
        'total_new_records': total_records,
        'sources': {
            'north_america': 'US Census, Canada',
            'europe': 'UK, Germany, France, Spain, Italy',
            'asia': 'China, Japan, Korea, India',
            'latin_america': 'Mexico, Brazil, Argentina',
            'africa': 'South Africa, Nigeria, Ethiopia',
            'middle_east': 'Arabic, Turkish, Persian',
            'github': 'Multiple databases'
        }
    }

    with open(OUTPUT_DIR / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    return total_records

if __name__ == "__main__":
    main()
