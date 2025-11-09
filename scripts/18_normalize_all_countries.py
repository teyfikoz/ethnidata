#!/usr/bin/env python3
"""
TÜM ÜLKE KODLARINI STANDARDİZE ET
Dünyadaki bütün ülkeleri kapsayacak şekilde
"""

import sqlite3
from pathlib import Path
import json

DB_FILE = Path(__file__).parent.parent / "ethnidata" / "ethnidata.db"
RELIGION_FILE = Path(__file__).parent.parent / "data" / "raw" / "religion" / "country_religion_mapping.json"

# Load religion mapping
with open(RELIGION_FILE, 'r', encoding='utf-8') as f:
    religion_data = json.load(f)
    COUNTRY_RELIGION = religion_data['primary_religion']

# Kapsamlı ülke kodu mapping'i (standart olmayan → ISO 3166-1 alpha-3)
COUNTRY_CODE_MAPPING = {
    # Standart olmayan kodlar → ISO 3166-1 alpha-3
    'US': 'USA', 'DE': 'DEU', 'FR': 'FRA', 'IT': 'ITA', 'ES': 'ESP',
    'UK': 'GBR', 'RU': 'RUS', 'CN': 'CHN', 'JP': 'JPN', 'KR': 'KOR',

    # Alternatif kodlar
    'GER': 'DEU', 'SPA': 'ESP', 'FRE': 'FRA', 'ITA': 'ITA',
    'SWI': 'CHE', 'SUI': 'CHE', 'NET': 'NLD', 'HOL': 'NLD',
    'JAP': 'JPN', 'KOR': 'KOR', 'CHI': 'CHN', 'IRA': 'IRN',
    'GRE': 'GRC', 'ROM': 'ROU', 'DEN': 'DNK', 'SWE': 'SWE',
    'NOR': 'NOR', 'FIN': 'FIN', 'POR': 'PRT', 'BEL': 'BEL',
    'AUT': 'AUT', 'POL': 'POL', 'CZE': 'CZE', 'HUN': 'HUN',

    # Africa
    'NIG': 'NGA', 'EGY': 'EGY', 'ETH': 'ETH', 'MOR': 'MAR',
    'ALG': 'DZA', 'TUN': 'TUN', 'KEN': 'KEN', 'TAN': 'TZA',
    'UGA': 'UGA', 'GHA': 'GHA', 'CAM': 'CMR', 'SEN': 'SEN',
    'SOU': 'ZAF',  # South Africa

    # Americas
    'ARG': 'ARG', 'BRA': 'BRA', 'CAN': 'CAN', 'MEX': 'MEX',
    'CHI': 'CHL', 'COL': 'COL', 'PER': 'PER', 'VEN': 'VEN',
    'CUB': 'CUB', 'URU': 'URY', 'PAR': 'PRY', 'ECU': 'ECU',

    # Asia - Middle East
    'SAU': 'SAU', 'UAE': 'ARE', 'KUW': 'KWT', 'QAT': 'QAT',
    'OMA': 'OMN', 'JOR': 'JOR', 'LEB': 'LBN', 'SYR': 'SYR',
    'IRQ': 'IRQ', 'ISR': 'ISR', 'YEM': 'YEM', 'BAH': 'BHR',

    # Asia - Other
    'IND': 'IND', 'PAK': 'PAK', 'BAN': 'BGD', 'THA': 'THA',
    'VIE': 'VNM', 'PHI': 'PHL', 'INO': 'IDN', 'MAL': 'MYS',
    'SIN': 'SGP', 'NEP': 'NPL', 'SRI': 'LKA',

    # Oceania
    'AUS': 'AUS', 'NZL': 'NZL', 'FIJ': 'FJI',

    # Europe - Eastern
    'SER': 'SRB', 'CRO': 'HRV', 'BUL': 'BGR', 'UKR': 'UKR',
    'BLR': 'BLR', 'LIT': 'LTU', 'LAT': 'LVA', 'EST': 'EST',
    'SLO': 'SVN', 'SVK': 'SVK', 'ALB': 'ALB', 'MAC': 'MKD',
    'BIH': 'BIH', 'MON': 'MNE',

    # Small/Other
    'LUX': 'LUX', 'ICE': 'ISL', 'IRL': 'IRL', 'MLT': 'MLT',
}

# Bölge mapping'i - KAPSAMLI
REGION_MAPPING = {
    # Americas
    'USA': 'Americas', 'CAN': 'Americas', 'MEX': 'Americas', 'BRA': 'Americas',
    'ARG': 'Americas', 'CHL': 'Americas', 'COL': 'Americas', 'PER': 'Americas',
    'VEN': 'Americas', 'ECU': 'Americas', 'BOL': 'Americas', 'PRY': 'Americas',
    'URY': 'Americas', 'CUB': 'Americas', 'DOM': 'Americas', 'HTI': 'Americas',
    'JAM': 'Americas', 'CRI': 'Americas', 'PAN': 'Americas', 'GTM': 'Americas',
    'HND': 'Americas', 'SLV': 'Americas', 'NIC': 'Americas', 'BHS': 'Americas',
    'BRB': 'Americas', 'TTO': 'Americas',

    # Europe - Western
    'GBR': 'Europe', 'FRA': 'Europe', 'DEU': 'Europe', 'ITA': 'Europe',
    'ESP': 'Europe', 'PRT': 'Europe', 'NLD': 'Europe', 'BEL': 'Europe',
    'LUX': 'Europe', 'CHE': 'Europe', 'AUT': 'Europe', 'IRL': 'Europe',
    'ISL': 'Europe', 'MLT': 'Europe', 'AND': 'Europe', 'MCO': 'Europe',

    # Europe - Northern
    'SWE': 'Europe', 'NOR': 'Europe', 'DNK': 'Europe', 'FIN': 'Europe',

    # Europe - Eastern
    'POL': 'Europe', 'CZE': 'Europe', 'SVK': 'Europe', 'HUN': 'Europe',
    'ROU': 'Europe', 'BGR': 'Europe', 'SRB': 'Europe', 'HRV': 'Europe',
    'SVN': 'Europe', 'BIH': 'Europe', 'MKD': 'Europe', 'MNE': 'Europe',
    'ALB': 'Europe', 'GRC': 'Europe', 'UKR': 'Europe', 'BLR': 'Europe',
    'MDA': 'Europe', 'LTU': 'Europe', 'LVA': 'Europe', 'EST': 'Europe',
    'RUS': 'Europe',

    # Asia - East
    'CHN': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia', 'PRK': 'Asia',
    'TWN': 'Asia', 'MNG': 'Asia', 'HKG': 'Asia', 'MAC': 'Asia',

    # Asia - Southeast
    'IDN': 'Asia', 'THA': 'Asia', 'VNM': 'Asia', 'PHL': 'Asia',
    'MYS': 'Asia', 'SGP': 'Asia', 'MMR': 'Asia', 'KHM': 'Asia',
    'LAO': 'Asia', 'BRN': 'Asia', 'TLS': 'Asia',

    # Asia - South
    'IND': 'Asia', 'PAK': 'Asia', 'BGD': 'Asia', 'NPL': 'Asia',
    'LKA': 'Asia', 'BTN': 'Asia', 'MDV': 'Asia', 'AFG': 'Asia',

    # Asia - Central
    'KAZ': 'Asia', 'UZB': 'Asia', 'TKM': 'Asia', 'KGZ': 'Asia', 'TJK': 'Asia',

    # Asia - Middle East
    'TUR': 'Asia', 'IRN': 'Asia', 'IRQ': 'Asia', 'SAU': 'Asia',
    'ARE': 'Asia', 'ISR': 'Asia', 'JOR': 'Asia', 'LBN': 'Asia',
    'SYR': 'Asia', 'YEM': 'Asia', 'KWT': 'Asia', 'QAT': 'Asia',
    'OMN': 'Asia', 'BHR': 'Asia', 'PSE': 'Asia', 'GEO': 'Asia',
    'ARM': 'Asia', 'AZE': 'Asia',

    # Africa - North
    'EGY': 'Africa', 'MAR': 'Africa', 'DZA': 'Africa', 'TUN': 'Africa',
    'LBY': 'Africa', 'SDN': 'Africa', 'SSD': 'Africa', 'MRT': 'Africa',

    # Africa - West
    'NGA': 'Africa', 'GHA': 'Africa', 'CIV': 'Africa', 'SEN': 'Africa',
    'MLI': 'Africa', 'BFA': 'Africa', 'NER': 'Africa', 'TGO': 'Africa',
    'BEN': 'Africa', 'GMB': 'Africa', 'GIN': 'Africa', 'GNB': 'Africa',
    'SLE': 'Africa', 'LBR': 'Africa', 'CMR': 'Africa', 'TCD': 'Africa',

    # Africa - East
    'ETH': 'Africa', 'KEN': 'Africa', 'TZA': 'Africa', 'UGA': 'Africa',
    'RWA': 'Africa', 'BDI': 'Africa', 'SOM': 'Africa', 'DJI': 'Africa',
    'ERI': 'Africa', 'MDG': 'Africa', 'MWI': 'Africa', 'ZMB': 'Africa',
    'MOZ': 'Africa', 'ZWE': 'Africa', 'COM': 'Africa', 'MUS': 'Africa',

    # Africa - Southern
    'ZAF': 'Africa', 'BWA': 'Africa', 'NAM': 'Africa', 'LSO': 'Africa',
    'SWZ': 'Africa', 'AGO': 'Africa',

    # Africa - Central
    'COD': 'Africa', 'COG': 'Africa', 'CAF': 'Africa', 'GAB': 'Africa',
    'GNQ': 'Africa', 'STP': 'Africa',

    # Oceania
    'AUS': 'Oceania', 'NZL': 'Oceania', 'FJI': 'Oceania', 'PNG': 'Oceania',
    'WSM': 'Oceania', 'TON': 'Oceania', 'VUT': 'Oceania', 'SLB': 'Oceania',
    'KIR': 'Oceania', 'TUV': 'Oceania', 'NRU': 'Oceania', 'PLW': 'Oceania',
    'FSM': 'Oceania', 'MHL': 'Oceania',
}

# Dil mapping'i - KAPSAMLI
LANGUAGE_MAPPING = {
    'USA': 'English', 'GBR': 'English', 'CAN': 'English', 'AUS': 'English',
    'NZL': 'English', 'IRL': 'English', 'ZAF': 'English', 'NGA': 'English',
    'GHA': 'English', 'KEN': 'English', 'UGA': 'English', 'ZWE': 'English',

    'ESP': 'Spanish', 'MEX': 'Spanish', 'ARG': 'Spanish', 'COL': 'Spanish',
    'PER': 'Spanish', 'VEN': 'Spanish', 'CHL': 'Spanish', 'ECU': 'Spanish',
    'GTM': 'Spanish', 'CUB': 'Spanish', 'BOL': 'Spanish', 'DOM': 'Spanish',
    'HND': 'Spanish', 'PRY': 'Spanish', 'SLV': 'Spanish', 'NIC': 'Spanish',
    'CRI': 'Spanish', 'PAN': 'Spanish', 'URY': 'Spanish',

    'FRA': 'French', 'BEL': 'French', 'CHE': 'French', 'CAN': 'French',
    'SEN': 'French', 'CIV': 'French', 'CMR': 'French', 'MLI': 'French',
    'BFA': 'French', 'NER': 'French', 'TCD': 'French', 'COD': 'French',
    'GAB': 'French', 'BEN': 'French', 'TGO': 'French', 'RWA': 'French',
    'BDI': 'French', 'DJI': 'French', 'COM': 'French', 'GIN': 'French',

    'DEU': 'German', 'AUT': 'German', 'CHE': 'German', 'LUX': 'German',

    'CHN': 'Chinese', 'TWN': 'Chinese', 'SGP': 'Chinese', 'HKG': 'Chinese',
    'JPN': 'Japanese', 'KOR': 'Korean', 'PRK': 'Korean',

    'RUS': 'Russian', 'UKR': 'Russian', 'KAZ': 'Russian', 'BLR': 'Russian',
    'KGZ': 'Russian', 'UZB': 'Russian', 'TKM': 'Russian', 'TJK': 'Russian',

    'ITA': 'Italian', 'CHE': 'Italian', 'PRT': 'Portuguese', 'BRA': 'Portuguese',
    'AGO': 'Portuguese', 'MOZ': 'Portuguese', 'CPV': 'Portuguese',

    'TUR': 'Turkish', 'POL': 'Polish', 'NLD': 'Dutch', 'BEL': 'Dutch',
    'SUR': 'Dutch', 'ROU': 'Romanian', 'MDA': 'Romanian',

    'IND': 'Hindi', 'PAK': 'Urdu', 'BGD': 'Bengali', 'IDN': 'Indonesian',
    'THA': 'Thai', 'VNM': 'Vietnamese', 'PHL': 'Tagalog', 'IRN': 'Persian',
    'AFG': 'Persian', 'IRQ': 'Arabic', 'SAU': 'Arabic', 'EGY': 'Arabic',
    'MAR': 'Arabic', 'DZA': 'Arabic', 'TUN': 'Arabic', 'LBY': 'Arabic',
    'SDN': 'Arabic', 'SYR': 'Arabic', 'JOR': 'Arabic', 'LBN': 'Arabic',
    'YEM': 'Arabic', 'KWT': 'Arabic', 'OMN': 'Arabic', 'QAT': 'Arabic',
    'BHR': 'Arabic', 'ARE': 'Arabic',

    'GRC': 'Greek', 'CYP': 'Greek', 'SWE': 'Swedish', 'NOR': 'Norwegian',
    'DNK': 'Danish', 'FIN': 'Finnish', 'ISL': 'Icelandic', 'HUN': 'Hungarian',
    'CZE': 'Czech', 'SVK': 'Slovak', 'BGR': 'Bulgarian', 'HRV': 'Croatian',
    'SRB': 'Serbian', 'SVN': 'Slovenian', 'MKD': 'Macedonian', 'ALB': 'Albanian',
    'LTU': 'Lithuanian', 'LVA': 'Latvian', 'EST': 'Estonian',

    'NPL': 'Nepali', 'LKA': 'Sinhala', 'MMR': 'Burmese', 'KHM': 'Khmer',
    'LAO': 'Lao', 'MNG': 'Mongolian', 'GEO': 'Georgian', 'ARM': 'Armenian',
    'AZE': 'Azerbaijani', 'ISR': 'Hebrew', 'ETH': 'Amharic', 'SWZ': 'Swati',
}

print("="*80)
print("TÜM ÜLKE KODLARINI STANDARDİZE ET")
print("="*80)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 1. Normalize country codes
print("\n🔄 Ülke kodları standardize ediliyor...")
for old_code, new_code in COUNTRY_CODE_MAPPING.items():
    cursor.execute(
        "UPDATE names SET country_code = ? WHERE country_code = ?",
        (new_code, old_code)
    )
    if cursor.rowcount > 0:
        print(f"  → {old_code} → {new_code}: {cursor.rowcount:,} kayıt")

conn.commit()

# 2. Update regions
print("\n🌍 Bölgeler güncelleniyor...")
for country, region in REGION_MAPPING.items():
    cursor.execute(
        "UPDATE names SET region = ? WHERE country_code = ?",
        (region, country)
    )

conn.commit()

# 3. Update languages
print("\n🗣️  Diller güncelleniyor...")
for country, language in LANGUAGE_MAPPING.items():
    cursor.execute(
        "UPDATE names SET language = ? WHERE country_code = ?",
        (language, country)
    )

conn.commit()

# 4. Update religions
print("\n🕌 Dinler güncelleniyor...")
for country, religion in COUNTRY_RELIGION.items():
    cursor.execute(
        "UPDATE names SET religion = ? WHERE country_code = ? AND religion IS NULL",
        (religion, country)
    )

conn.commit()

# Final statistics
print("\n" + "="*80)
print("GÜNCEL İSTATİSTİKLER")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM names")
total = cursor.fetchone()[0]
print(f"\n📊 Toplam kayıt: {total:,}")

cursor.execute("SELECT COUNT(DISTINCT country_code) FROM names")
countries = cursor.fetchone()[0]
print(f"📊 Ülke sayısı: {countries}")

cursor.execute("SELECT region, COUNT(*) FROM names GROUP BY region ORDER BY COUNT(*) DESC")
print(f"\n🌍 Bölge dağılımı:")
for row in cursor.fetchall():
    pct = (row[1] / total) * 100
    print(f"  {row[0]}: {row[1]:,} ({pct:.1f}%)")

cursor.execute("SELECT COUNT(*) FROM names WHERE religion IS NOT NULL")
with_religion = cursor.fetchone()[0]
print(f"\n🕌 Din bilgisi olan: {with_religion:,} ({with_religion/total*100:.1f}%)")

cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL GROUP BY religion ORDER BY COUNT(*) DESC")
print(f"\n📊 Din dağılımı:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

cursor.execute("SELECT language, COUNT(*) FROM names WHERE language IS NOT NULL GROUP BY language ORDER BY COUNT(*) DESC LIMIT 15")
print(f"\n🗣️  En yaygın 15 dil:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Top countries
cursor.execute("SELECT country_code, COUNT(*) FROM names GROUP BY country_code ORDER BY COUNT(*) DESC LIMIT 20")
print(f"\n🌐 En fazla kayıt olan 20 ülke:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# VACUUM to optimize
print("\n🗜️  Veritabanı optimize ediliyor...")
cursor.execute("VACUUM")
conn.commit()

conn.close()

db_size_mb = DB_FILE.stat().st_size / (1024 * 1024)
print(f"\n💾 Veritabanı boyutu: {db_size_mb:.2f} MB")

print("\n" + "="*80)
print("✅ STANDARDİZASYON TAMAMLANDI!")
print(f"✅ {countries} ÜLKE, {total:,} KAYIT")
print("✅ 5 KITA (Americas, Europe, Asia, Africa, Oceania)")
print("="*80)
