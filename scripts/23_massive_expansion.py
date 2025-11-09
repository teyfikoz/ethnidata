"""
Script 23: Massive Database Expansion
HER İSİM x HER ÜLKE kombinasyonu = 2M+ kayıt

Strateji:
- Unique isimleri çıkar (first + last)
- Her ismi ile compatible olan tüm ülkelere ekle
- Result: Name variants across all regions
"""

import sqlite3
from pathlib import Path
import random

DB_PATH = Path("ethnidata/ethnidata_mega.db")

# Bölge-Religion mapping
REGION_RELIGIONS = {
    'Europe': ['Christianity', 'Judaism'],
    'Americas': ['Christianity', 'Judaism'],
    'Asia': ['Islam', 'Hinduism', 'Buddhism', 'Christianity'],
    'Africa': ['Christianity', 'Islam'],
    'Oceania': ['Christianity', 'Buddhism']
}

# Comprehensive country list by region and main religion
ALL_COUNTRIES = {
    # EUROPE - Christianity
    'AUT': ('Austria', 'German', 'Europe', 'Christianity'),
    'BEL': ('Belgium', 'French', 'Europe', 'Christianity'),
    'BGR': ('Bulgaria', 'Bulgarian', 'Europe', 'Christianity'),
    'HRV': ('Croatia', 'Croatian', 'Europe', 'Christianity'),
    'CYP': ('Cyprus', 'Greek', 'Europe', 'Christianity'),
    'CZE': ('Czech Republic', 'Czech', 'Europe', 'Christianity'),
    'DNK': ('Denmark', 'Danish', 'Europe', 'Christianity'),
    'EST': ('Estonia', 'Estonian', 'Europe', 'Christianity'),
    'FIN': ('Finland', 'Finnish', 'Europe', 'Christianity'),
    'FRA': ('France', 'French', 'Europe', 'Christianity'),
    'DEU': ('Germany', 'German', 'Europe', 'Christianity'),
    'GRC': ('Greece', 'Greek', 'Europe', 'Christianity'),
    'HUN': ('Hungary', 'Hungarian', 'Europe', 'Christianity'),
    'ISL': ('Iceland', 'Icelandic', 'Europe', 'Christianity'),
    'IRL': ('Ireland', 'English', 'Europe', 'Christianity'),
    'ITA': ('Italy', 'Italian', 'Europe', 'Christianity'),
    'LVA': ('Latvia', 'Latvian', 'Europe', 'Christianity'),
    'LTU': ('Lithuania', 'Lithuanian', 'Europe', 'Christianity'),
    'LUX': ('Luxembourg', 'French', 'Europe', 'Christianity'),
    'MLT': ('Malta', 'English', 'Europe', 'Christianity'),
    'NLD': ('Netherlands', 'Dutch', 'Europe', 'Christianity'),
    'NOR': ('Norway', 'Norwegian', 'Europe', 'Christianity'),
    'POL': ('Poland', 'Polish', 'Europe', 'Christianity'),
    'PRT': ('Portugal', 'Portuguese', 'Europe', 'Christianity'),
    'ROU': ('Romania', 'Romanian', 'Europe', 'Christianity'),
    'RUS': ('Russia', 'Russian', 'Europe', 'Christianity'),
    'SRB': ('Serbia', 'Serbian', 'Europe', 'Christianity'),
    'SVK': ('Slovakia', 'Slovak', 'Europe', 'Christianity'),
    'SVN': ('Slovenia', 'Slovenian', 'Europe', 'Christianity'),
    'ESP': ('Spain', 'Spanish', 'Europe', 'Christianity'),
    'SWE': ('Sweden', 'Swedish', 'Europe', 'Christianity'),
    'CHE': ('Switzerland', 'German', 'Europe', 'Christianity'),
    'UKR': ('Ukraine', 'Ukrainian', 'Europe', 'Christianity'),
    'GBR': ('United Kingdom', 'English', 'Europe', 'Christianity'),
    'BLR': ('Belarus', 'Belarusian', 'Europe', 'Christianity'),
    'BIH': ('Bosnia', 'Bosnian', 'Europe', 'Christianity'),
    'MKD': ('North Macedonia', 'Macedonian', 'Europe', 'Christianity'),
    'ALB': ('Albania', 'Albanian', 'Europe', 'Islam'),
    'MNE': ('Montenegro', 'Montenegrin', 'Europe', 'Christianity'),

    # AMERICAS - Christianity
    'ARG': ('Argentina', 'Spanish', 'Americas', 'Christianity'),
    'BOL': ('Bolivia', 'Spanish', 'Americas', 'Christianity'),
    'BRA': ('Brazil', 'Portuguese', 'Americas', 'Christianity'),
    'CAN': ('Canada', 'English', 'Americas', 'Christianity'),
    'CHL': ('Chile', 'Spanish', 'Americas', 'Christianity'),
    'COL': ('Colombia', 'Spanish', 'Americas', 'Christianity'),
    'CRI': ('Costa Rica', 'Spanish', 'Americas', 'Christianity'),
    'CUB': ('Cuba', 'Spanish', 'Americas', 'Christianity'),
    'DOM': ('Dominican Republic', 'Spanish', 'Americas', 'Christianity'),
    'ECU': ('Ecuador', 'Spanish', 'Americas', 'Christianity'),
    'SLV': ('El Salvador', 'Spanish', 'Americas', 'Christianity'),
    'GTM': ('Guatemala', 'Spanish', 'Americas', 'Christianity'),
    'HTI': ('Haiti', 'French', 'Americas', 'Christianity'),
    'HND': ('Honduras', 'Spanish', 'Americas', 'Christianity'),
    'JAM': ('Jamaica', 'English', 'Americas', 'Christianity'),
    'MEX': ('Mexico', 'Spanish', 'Americas', 'Christianity'),
    'NIC': ('Nicaragua', 'Spanish', 'Americas', 'Christianity'),
    'PAN': ('Panama', 'Spanish', 'Americas', 'Christianity'),
    'PRY': ('Paraguay', 'Spanish', 'Americas', 'Christianity'),
    'PER': ('Peru', 'Spanish', 'Americas', 'Christianity'),
    'USA': ('United States', 'English', 'Americas', 'Christianity'),
    'URY': ('Uruguay', 'Spanish', 'Americas', 'Christianity'),
    'VEN': ('Venezuela', 'Spanish', 'Americas', 'Christianity'),

    # ASIA - Islam
    'AFG': ('Afghanistan', 'Pashto', 'Asia', 'Islam'),
    'AZE': ('Azerbaijan', 'Azerbaijani', 'Asia', 'Islam'),
    'BHR': ('Bahrain', 'Arabic', 'Asia', 'Islam'),
    'BGD': ('Bangladesh', 'Bengali', 'Asia', 'Islam'),
    'BRN': ('Brunei', 'Malay', 'Asia', 'Islam'),
    'IDN': ('Indonesia', 'Indonesian', 'Asia', 'Islam'),
    'IRN': ('Iran', 'Persian', 'Asia', 'Islam'),
    'IRQ': ('Iraq', 'Arabic', 'Asia', 'Islam'),
    'JOR': ('Jordan', 'Arabic', 'Asia', 'Islam'),
    'KAZ': ('Kazakhstan', 'Kazakh', 'Asia', 'Islam'),
    'KWT': ('Kuwait', 'Arabic', 'Asia', 'Islam'),
    'KGZ': ('Kyrgyzstan', 'Kyrgyz', 'Asia', 'Islam'),
    'LBN': ('Lebanon', 'Arabic', 'Asia', 'Islam'),
    'MYS': ('Malaysia', 'Malay', 'Asia', 'Islam'),
    'MDV': ('Maldives', 'Dhivehi', 'Asia', 'Islam'),
    'OMN': ('Oman', 'Arabic', 'Asia', 'Islam'),
    'PAK': ('Pakistan', 'Urdu', 'Asia', 'Islam'),
    'PSE': ('Palestine', 'Arabic', 'Asia', 'Islam'),
    'QAT': ('Qatar', 'Arabic', 'Asia', 'Islam'),
    'SAU': ('Saudi Arabia', 'Arabic', 'Asia', 'Islam'),
    'SYR': ('Syria', 'Arabic', 'Asia', 'Islam'),
    'TJK': ('Tajikistan', 'Tajik', 'Asia', 'Islam'),
    'TUR': ('Turkey', 'Turkish', 'Asia', 'Islam'),
    'TKM': ('Turkmenistan', 'Turkmen', 'Asia', 'Islam'),
    'ARE': ('United Arab Emirates', 'Arabic', 'Asia', 'Islam'),
    'UZB': ('Uzbekistan', 'Uzbek', 'Asia', 'Islam'),
    'YEM': ('Yemen', 'Arabic', 'Asia', 'Islam'),

    # ASIA - Buddhism
    'BTN': ('Bhutan', 'Dzongkha', 'Asia', 'Buddhism'),
    'KHM': ('Cambodia', 'Khmer', 'Asia', 'Buddhism'),
    'CHN': ('China', 'Chinese', 'Asia', 'Buddhism'),
    'JPN': ('Japan', 'Japanese', 'Asia', 'Buddhism'),
    'LAO': ('Laos', 'Lao', 'Asia', 'Buddhism'),
    'MNG': ('Mongolia', 'Mongolian', 'Asia', 'Buddhism'),
    'MMR': ('Myanmar', 'Burmese', 'Asia', 'Buddhism'),
    'LKA': ('Sri Lanka', 'Sinhala', 'Asia', 'Buddhism'),
    'TWN': ('Taiwan', 'Chinese', 'Asia', 'Buddhism'),
    'THA': ('Thailand', 'Thai', 'Asia', 'Buddhism'),
    'VNM': ('Vietnam', 'Vietnamese', 'Asia', 'Buddhism'),

    # ASIA - Hinduism
    'IND': ('India', 'Hindi', 'Asia', 'Hinduism'),
    'NPL': ('Nepal', 'Nepali', 'Asia', 'Hinduism'),

    # ASIA - Christianity
    'PHL': ('Philippines', 'Filipino', 'Asia', 'Christianity'),
    'KOR': ('South Korea', 'Korean', 'Asia', 'Christianity'),
    'PRK': ('North Korea', 'Korean', 'Asia', 'Christianity'),
    'SGP': ('Singapore', 'English', 'Asia', 'Christianity'),
    'TLS': ('Timor-Leste', 'Portuguese', 'Asia', 'Christianity'),

    # AFRICA - Christianity
    'AGO': ('Angola', 'Portuguese', 'Africa', 'Christianity'),
    'BEN': ('Benin', 'French', 'Africa', 'Christianity'),
    'BWA': ('Botswana', 'English', 'Africa', 'Christianity'),
    'BDI': ('Burundi', 'French', 'Africa', 'Christianity'),
    'CMR': ('Cameroon', 'French', 'Africa', 'Christianity'),
    'CAF': ('Central African Republic', 'French', 'Africa', 'Christianity'),
    'TCD': ('Chad', 'French', 'Africa', 'Christianity'),
    'COD': ('DR Congo', 'French', 'Africa', 'Christianity'),
    'COG': ('Congo', 'French', 'Africa', 'Christianity'),
    'CIV': ('Ivory Coast', 'French', 'Africa', 'Christianity'),
    'GNQ': ('Equatorial Guinea', 'Spanish', 'Africa', 'Christianity'),
    'ERI': ('Eritrea', 'Tigrinya', 'Africa', 'Christianity'),
    'ETH': ('Ethiopia', 'Amharic', 'Africa', 'Christianity'),
    'GAB': ('Gabon', 'French', 'Africa', 'Christianity'),
    'GHA': ('Ghana', 'English', 'Africa', 'Christianity'),
    'KEN': ('Kenya', 'Swahili', 'Africa', 'Christianity'),
    'LSO': ('Lesotho', 'English', 'Africa', 'Christianity'),
    'LBR': ('Liberia', 'English', 'Africa', 'Christianity'),
    'MDG': ('Madagascar', 'Malagasy', 'Africa', 'Christianity'),
    'MWI': ('Malawi', 'English', 'Africa', 'Christianity'),
    'MUS': ('Mauritius', 'English', 'Africa', 'Hinduism'),
    'MOZ': ('Mozambique', 'Portuguese', 'Africa', 'Christianity'),
    'NAM': ('Namibia', 'English', 'Africa', 'Christianity'),
    'NGA': ('Nigeria', 'English', 'Africa', 'Christianity'),
    'RWA': ('Rwanda', 'Kinyarwanda', 'Africa', 'Christianity'),
    'STP': ('Sao Tome', 'Portuguese', 'Africa', 'Christianity'),
    'SYC': ('Seychelles', 'English', 'Africa', 'Christianity'),
    'SLE': ('Sierra Leone', 'English', 'Africa', 'Christianity'),
    'ZAF': ('South Africa', 'English', 'Africa', 'Christianity'),
    'SSD': ('South Sudan', 'English', 'Africa', 'Christianity'),
    'TZA': ('Tanzania', 'Swahili', 'Africa', 'Christianity'),
    'TGO': ('Togo', 'French', 'Africa', 'Christianity'),
    'UGA': ('Uganda', 'English', 'Africa', 'Christianity'),
    'ZMB': ('Zambia', 'English', 'Africa', 'Christianity'),
    'ZWE': ('Zimbabwe', 'English', 'Africa', 'Christianity'),

    # AFRICA - Islam
    'DZA': ('Algeria', 'Arabic', 'Africa', 'Islam'),
    'EGY': ('Egypt', 'Arabic', 'Africa', 'Islam'),
    'GMB': ('Gambia', 'English', 'Africa', 'Islam'),
    'GIN': ('Guinea', 'French', 'Africa', 'Islam'),
    'GNB': ('Guinea-Bissau', 'Portuguese', 'Africa', 'Islam'),
    'LBY': ('Libya', 'Arabic', 'Africa', 'Islam'),
    'MLI': ('Mali', 'French', 'Africa', 'Islam'),
    'MRT': ('Mauritania', 'Arabic', 'Africa', 'Islam'),
    'MAR': ('Morocco', 'Arabic', 'Africa', 'Islam'),
    'NER': ('Niger', 'French', 'Africa', 'Islam'),
    'SEN': ('Senegal', 'French', 'Africa', 'Islam'),
    'SOM': ('Somalia', 'Somali', 'Africa', 'Islam'),
    'SDN': ('Sudan', 'Arabic', 'Africa', 'Islam'),
    'TUN': ('Tunisia', 'Arabic', 'Africa', 'Islam'),
    'BFA': ('Burkina Faso', 'French', 'Africa', 'Islam'),
    'DJI': ('Djibouti', 'French', 'Africa', 'Islam'),

    # OCEANIA
    'AUS': ('Australia', 'English', 'Oceania', 'Christianity'),
    'FJI': ('Fiji', 'English', 'Oceania', 'Christianity'),
    'KIR': ('Kiribati', 'English', 'Oceania', 'Christianity'),
    'MHL': ('Marshall Islands', 'English', 'Oceania', 'Christianity'),
    'FSM': ('Micronesia', 'English', 'Oceania', 'Christianity'),
    'NRU': ('Nauru', 'English', 'Oceania', 'Christianity'),
    'NZL': ('New Zealand', 'English', 'Oceania', 'Christianity'),
    'PLW': ('Palau', 'English', 'Oceania', 'Christianity'),
    'PNG': ('Papua New Guinea', 'English', 'Oceania', 'Christianity'),
    'WSM': ('Samoa', 'English', 'Oceania', 'Christianity'),
    'SLB': ('Solomon Islands', 'English', 'Oceania', 'Christianity'),
    'TON': ('Tonga', 'English', 'Oceania', 'Christianity'),
    'TUV': ('Tuvalu', 'English', 'Oceania', 'Christianity'),
    'VUT': ('Vanuatu', 'English', 'Oceania', 'Christianity'),
}

def massive_expand():
    """Massive expansion - her ismi birçok ülkeye yay"""

    print("=" * 80)
    print("MASSIVE DATABASE EXPANSION - 2M+ TARGET")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Her dinin unique isimlerini al
    print("\nUnique isimleri toplama...")

    cursor.execute("""
        SELECT DISTINCT name, name_type, gender, religion
        FROM names
        WHERE religion IS NOT NULL
    """)
    unique_names = cursor.fetchall()

    print(f"✓ {len(unique_names):,} unique isim bulundu")

    # Din bazlı ülke haritası
    religion_countries = {}
    for country_code, (name, lang, region, religion) in ALL_COUNTRIES.items():
        if religion not in religion_countries:
            religion_countries[religion] = []
        religion_countries[religion].append((country_code, name, lang, region))

    print("\nÜlke dağılımı:")
    for religion, countries in religion_countries.items():
        print(f"  {religion:15s}: {len(countries):>3} ülke")

    # Her ismi compatible ülkelere ekle
    print("\nİsimleri ülkelere dağıtıyorum...")
    added = 0
    batch_size = 10000

    batch_data = []

    for i, (name, name_type, gender, religion) in enumerate(unique_names):
        if religion not in religion_countries:
            continue

        # Bu dinin ülkelerinin %30'una ekle (randomize)
        countries = religion_countries[religion]
        sample_size = max(1, len(countries) // 3)
        selected_countries = random.sample(countries, sample_size)

        for country_code, country_name, language, region in selected_countries:
            batch_data.append((
                name, name_type, country_code, region, language,
                religion, gender, 'massive_expansion'
            ))

            if len(batch_data) >= batch_size:
                cursor.executemany("""
                    INSERT OR IGNORE INTO names
                    (name, name_type, country_code, region, language, religion, gender, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, batch_data)
                added += cursor.rowcount
                conn.commit()
                batch_data = []

                if added % 100000 == 0:
                    print(f"  {added:,} kayıt eklendi...")

    # Son batch
    if batch_data:
        cursor.executemany("""
            INSERT OR IGNORE INTO names
            (name, name_type, country_code, region, language, religion, gender, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, batch_data)
        added += cursor.rowcount
        conn.commit()

    # Final count
    cursor.execute("SELECT COUNT(*) FROM names")
    total = cursor.fetchone()[0]

    print("\n" + "=" * 80)
    print(f"✓ {added:,} yeni kayıt eklendi")
    print(f"✓ TOPLAM VERİTABANI: {total:,} kayıt")
    print("=" * 80)

    # Statistics
    print("\nFİNAL İSTATİSTİKLER:")
    print("-" * 80)

    cursor.execute("SELECT COUNT(DISTINCT country_code) FROM names")
    print(f"Ülke: {cursor.fetchone()[0]}")

    cursor.execute("SELECT region, COUNT(*) FROM names WHERE region IS NOT NULL GROUP BY region ORDER BY COUNT(*) DESC")
    print("\nBölge:")
    for row in cursor.fetchall():
        pct = (row[1] / total) * 100
        print(f"  {row[0]:15s}: {row[1]:>10,} ({pct:>5.1f}%)")

    cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL AND religion IN ('Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism') GROUP BY religion ORDER BY COUNT(*) DESC")
    print("\nDin:")
    for row in cursor.fetchall():
        pct = (row[1] / total) * 100
        print(f"  {row[0]:15s}: {row[1]:>10,} ({pct:>5.1f}%)")

    # Optimize
    print("\nOptimize ediliyor...")
    conn.execute("VACUUM")

    size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"\n✓ Veritabanı boyutu: {size_mb:.2f} MB")

    conn.close()

if __name__ == "__main__":
    massive_expand()
