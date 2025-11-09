#!/usr/bin/env python3
"""
Olympics Dataset Scraper
Kaynak: Kaggle Olympics Historical Dataset
120 yıllık Olimpiyat sporcu verileri
"""

import pandas as pd
import requests
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "olympics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_olympics_data():
    """
    Olympics dataset'i indir
    Kaynak: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
    GitHub mirror: https://github.com/rgriff23/Olympic_history
    """

    print("🏅 Olympics dataset indiriliyor...")

    # GitHub'dan CSV dosyasını çek
    url = "https://raw.githubusercontent.com/rgriff23/Olympic_history/master/data/athlete_events.csv"

    try:
        print(f"  → {url}")
        df = pd.read_csv(url)

        # Dosyayı kaydet
        output_file = OUTPUT_DIR / "athlete_events.csv"
        df.to_csv(output_file, index=False, encoding='utf-8')

        print(f"  ✓ {len(df)} sporcu kaydedildi: {output_file}")

        # İsim-Ülke eşleştirmesi çıkar
        print("\n🔍 İsim-Ülke verileri işleniyor...")

        # NOC (National Olympic Committee) kodlarını ülke isimlerine çevir
        noc_url = "https://raw.githubusercontent.com/rgriff23/Olympic_history/master/data/noc_regions.csv"
        noc_df = pd.read_csv(noc_url)

        # Merge
        merged = df.merge(noc_df, on='NOC', how='left')

        # İsim parse et (first, last name)
        name_country = merged[['Name', 'region', 'NOC', 'Team', 'Sex']].copy()
        name_country = name_country.dropna(subset=['Name', 'region'])
        name_country = name_country.drop_duplicates(subset=['Name'])

        # First name ve Last name ayır
        name_country['first_name'] = name_country['Name'].str.split().str[0]
        name_country['last_name'] = name_country['Name'].str.split().str[-1]

        # Kaydet
        output_processed = OUTPUT_DIR / "olympics_names.csv"
        name_country.to_csv(output_processed, index=False, encoding='utf-8')

        print(f"  ✓ {len(name_country)} benzersiz isim kaydedildi: {output_processed}")

        # İstatistikler
        print("\n📊 Ülke dağılımı (top 20):")
        country_counts = name_country['region'].value_counts().head(20)
        for country, count in country_counts.items():
            print(f"  {country}: {count}")

        print("\n✅ Olympics dataset tamamlandı!")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    fetch_olympics_data()
