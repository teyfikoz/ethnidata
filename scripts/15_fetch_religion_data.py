#!/usr/bin/env python3
"""
Din Verisi Toplama
World Religion Projections ve diğer kaynaklardan din verisi
"""

import requests
import pandas as pd
from pathlib import Path
import json

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "religion"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("DİN VERİSİ TOPLAMA")
print("="*80)

# 1. World Religion Projections (GitHub)
print("\n🕌 World Religion Projections...")
try:
    url = "https://raw.githubusercontent.com/datasets/world-religion-projections/master/data/world-religion-projections.csv"
    df = pd.read_csv(url)
    output = OUTPUT_DIR / "world_religion_projections.csv"
    df.to_csv(output, index=False)
    print(f"  ✓ {len(df):,} kayıt: {output}")
    print(f"  → Sütunlar: {list(df.columns)}")
    print(f"  → İlk birkaç satır:")
    print(df.head())
except Exception as e:
    print(f"  ✗ Hata: {e}")

# 2. Manuel ülke-din mapping oluştur
print("\n📊 Manuel Ülke-Din Mapping...")

# Ülkelerin baskın dinleri (CIA World Factbook ve Pew Research'e göre)
COUNTRY_RELIGION_MAP = {
    # Americas
    'USA': 'Christianity', 'CAN': 'Christianity', 'MEX': 'Christianity',
    'BRA': 'Christianity', 'ARG': 'Christianity', 'CHL': 'Christianity',
    'COL': 'Christianity', 'PER': 'Christianity', 'VEN': 'Christianity',
    'CUB': 'Christianity', 'DOM': 'Christianity', 'JAM': 'Christianity',

    # Europe
    'GBR': 'Christianity', 'FRA': 'Christianity', 'DEU': 'Christianity',
    'ITA': 'Christianity', 'ESP': 'Christianity', 'POL': 'Christianity',
    'UKR': 'Christianity', 'RUS': 'Christianity', 'NLD': 'Christianity',
    'BEL': 'Christianity', 'SWE': 'Christianity', 'NOR': 'Christianity',
    'DNK': 'Christianity', 'FIN': 'Christianity', 'CHE': 'Christianity',
    'AUT': 'Christianity', 'GRC': 'Christianity', 'PRT': 'Christianity',
    'CZE': 'Christianity', 'HUN': 'Christianity', 'IRL': 'Christianity',

    # Asia - Muslim Majority
    'TUR': 'Islam', 'IRN': 'Islam', 'IRQ': 'Islam', 'SAU': 'Islam',
    'PAK': 'Islam', 'BGD': 'Islam', 'IDN': 'Islam', 'MYS': 'Islam',
    'ARE': 'Islam', 'EGY': 'Islam', 'JOR': 'Islam', 'SYR': 'Islam',
    'AFG': 'Islam', 'KAZ': 'Islam', 'UZB': 'Islam',

    # Asia - Hindu/Buddhist
    'IND': 'Hinduism', 'NPL': 'Hinduism', 'LKA': 'Buddhism',
    'THA': 'Buddhism', 'MMR': 'Buddhism', 'KHM': 'Buddhism',
    'LAO': 'Buddhism', 'VNM': 'Buddhism',

    # Asia - Other
    'CHN': 'Buddhism', 'JPN': 'Buddhism', 'KOR': 'Christianity',
    'TWN': 'Buddhism', 'SGP': 'Buddhism', 'PHL': 'Christianity',
    'ISR': 'Judaism',

    # Africa - Muslim Majority
    'DZA': 'Islam', 'MAR': 'Islam', 'TUN': 'Islam', 'LBY': 'Islam',
    'SDN': 'Islam', 'SOM': 'Islam', 'SEN': 'Islam', 'MLI': 'Islam',
    'NER': 'Islam', 'TCD': 'Islam', 'MRT': 'Islam',

    # Africa - Christian Majority
    'ZAF': 'Christianity', 'NGA': 'Christianity', 'ETH': 'Christianity',
    'KEN': 'Christianity', 'TZA': 'Christianity', 'UGA': 'Christianity',
    'RWA': 'Christianity', 'GHA': 'Christianity', 'CMR': 'Christianity',
    'AGO': 'Christianity', 'MOZ': 'Christianity', 'ZWE': 'Christianity',
    'ZMB': 'Christianity', 'MWI': 'Christianity', 'BWA': 'Christianity',

    # Oceania
    'AUS': 'Christianity', 'NZL': 'Christianity', 'FJI': 'Christianity',
    'PNG': 'Christianity', 'WSM': 'Christianity',
}

# Detaylı din dağılımı (bazı ülkeler için)
COUNTRY_RELIGION_DETAIL = {
    'USA': {'Christianity': 0.65, 'Unaffiliated': 0.26, 'Judaism': 0.02, 'Islam': 0.01, 'Other': 0.06},
    'IND': {'Hinduism': 0.79, 'Islam': 0.14, 'Christianity': 0.02, 'Sikhism': 0.02, 'Buddhism': 0.01},
    'IDN': {'Islam': 0.87, 'Christianity': 0.10, 'Hinduism': 0.02, 'Buddhism': 0.01},
    'CHN': {'Unaffiliated': 0.52, 'Buddhism': 0.18, 'Christianity': 0.05, 'Folk': 0.22},
    'ISR': {'Judaism': 0.74, 'Islam': 0.18, 'Christianity': 0.02, 'Druze': 0.02},
    'LBN': {'Islam': 0.54, 'Christianity': 0.40, 'Druze': 0.05},
    'NGA': {'Islam': 0.50, 'Christianity': 0.48, 'Traditional': 0.02},
    'ETH': {'Christianity': 0.63, 'Islam': 0.34, 'Traditional': 0.03},
}

# JSON olarak kaydet
output_json = OUTPUT_DIR / "country_religion_mapping.json"
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump({
        'primary_religion': COUNTRY_RELIGION_MAP,
        'detailed_distribution': COUNTRY_RELIGION_DETAIL
    }, f, indent=2, ensure_ascii=False)

print(f"  ✓ {len(COUNTRY_RELIGION_MAP)} ülke için din mapping: {output_json}")
print(f"  → Dinler: {set(COUNTRY_RELIGION_MAP.values())}")

# 3. İsim-Din ilişkisi için pattern'ler
print("\n📖 İsim-Din Pattern'leri...")

NAME_RELIGION_PATTERNS = {
    'Islam': {
        'prefixes': ['abd', 'abu', 'al', 'bin', 'bint', 'ibn'],
        'names': ['muhammad', 'ahmed', 'ali', 'hassan', 'hussain', 'fatima',
                  'aisha', 'omar', 'umar', 'khalid', 'ibrahim', 'yusuf',
                  'mustafa', 'mohammed', 'ahmad', 'hamza', 'zahra'],
        'suffixes': ['ullah', 'din', 'rahman']
    },
    'Christianity': {
        'names': ['john', 'mary', 'michael', 'david', 'joseph', 'paul',
                  'peter', 'james', 'sarah', 'elizabeth', 'matthew', 'mark',
                  'luke', 'jesus', 'christ', 'moses', 'abraham', 'isaac']
    },
    'Hinduism': {
        'names': ['krishna', 'rama', 'lakshmi', 'saraswati', 'ganesh', 'shiva',
                  'vishnu', 'brahma', 'parvati', 'durga', 'kali', 'radha',
                  'arjun', 'dev', 'raj', 'amit', 'priya', 'maya'],
        'suffixes': ['kumar', 'singh', 'sharma', 'patel', 'reddy']
    },
    'Buddhism': {
        'names': ['bodhi', 'dharma', 'karma', 'buddha', 'zen', 'tenzin',
                  'dalai', 'lama', 'thich', 'nhat'],
        'prefixes': ['lama', 'rinpoche']
    },
    'Judaism': {
        'names': ['abraham', 'isaac', 'jacob', 'sarah', 'rebecca', 'rachel',
                  'david', 'solomon', 'moses', 'aaron', 'miriam', 'esther',
                  'benjamin', 'levi', 'cohen', 'ruth'],
        'suffixes': ['stein', 'berg', 'man', 'witz', 'feld', 'baum']
    },
    'Sikhism': {
        'names': ['singh', 'kaur', 'guru', 'nanak', 'gobind'],
    }
}

output_patterns = OUTPUT_DIR / "name_religion_patterns.json"
with open(output_patterns, 'w', encoding='utf-8') as f:
    json.dump(NAME_RELIGION_PATTERNS, f, indent=2, ensure_ascii=False)

print(f"  ✓ {len(NAME_RELIGION_PATTERNS)} din için isim pattern'leri: {output_patterns}")

print("\n" + "="*80)
print("✅ DİN VERİSİ TOPLANDI")
print("="*80)
print(f"\nDosyalar:")
print(f"  - world_religion_projections.csv")
print(f"  - country_religion_mapping.json ({len(COUNTRY_RELIGION_MAP)} ülke)")
print(f"  - name_religion_patterns.json ({len(NAME_RELIGION_PATTERNS)} din)")
