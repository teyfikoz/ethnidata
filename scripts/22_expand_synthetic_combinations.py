"""
Script 22: Expand Synthetic Data with Full Combinations
Her isim her ülke ile kombinasyonu yaparak 2M+ unique kayıt oluştur
"""

import sqlite3
import random
from pathlib import Path
import itertools

DB_PATH = Path("ethnidata/ethnidata_mega.db")

# Her dinin ülkeleri ve o ülkeden kullanılabilecek isim havuzu
RELIGION_EXPANSIONS = {
    'Islam': {
        'countries': [
            ('SAU', 'Saudi Arabia', 'Arabic', 'Asia'),
            ('ARE', 'United Arab Emirates', 'Arabic', 'Asia'),
            ('QAT', 'Qatar', 'Arabic', 'Asia'),
            ('KWT', 'Kuwait', 'Arabic', 'Asia'),
            ('BHR', 'Bahrain', 'Arabic', 'Asia'),
            ('OMN', 'Oman', 'Arabic', 'Asia'),
            ('YEM', 'Yemen', 'Arabic', 'Asia'),
            ('JOR', 'Jordan', 'Arabic', 'Asia'),
            ('SYR', 'Syria', 'Arabic', 'Asia'),
            ('LBN', 'Lebanon', 'Arabic', 'Asia'),
            ('IRQ', 'Iraq', 'Arabic', 'Asia'),
            ('PSE', 'Palestine', 'Arabic', 'Asia'),
            ('EGY', 'Egypt', 'Arabic', 'Africa'),
            ('DZA', 'Algeria', 'Arabic', 'Africa'),
            ('MAR', 'Morocco', 'Arabic', 'Africa'),
            ('TUN', 'Tunisia', 'Arabic', 'Africa'),
            ('LBY', 'Libya', 'Arabic', 'Africa'),
            ('SDN', 'Sudan', 'Arabic', 'Africa'),
            ('SOM', 'Somalia', 'Somali', 'Africa'),
            ('MRT', 'Mauritania', 'Arabic', 'Africa'),
            ('IDN', 'Indonesia', 'Indonesian', 'Asia'),
            ('PAK', 'Pakistan', 'Urdu', 'Asia'),
            ('BGD', 'Bangladesh', 'Bengali', 'Asia'),
            ('MYS', 'Malaysia', 'Malay', 'Asia'),
            ('TUR', 'Turkey', 'Turkish', 'Asia'),
            ('IRN', 'Iran', 'Persian', 'Asia'),
            ('AFG', 'Afghanistan', 'Pashto', 'Asia'),
            ('AZE', 'Azerbaijan', 'Azerbaijani', 'Asia'),
            ('UZB', 'Uzbekistan', 'Uzbek', 'Asia'),
            ('KAZ', 'Kazakhstan', 'Kazakh', 'Asia'),
            ('NGA', 'Nigeria', 'English', 'Africa'),
            ('SEN', 'Senegal', 'French', 'Africa'),
            ('MLI', 'Mali', 'French', 'Africa'),
        ],
        'target': 500000
    },
    'Hinduism': {
        'countries': [
            ('IND', 'India', 'Hindi', 'Asia'),
            ('NPL', 'Nepal', 'Nepali', 'Asia'),
            ('LKA', 'Sri Lanka', 'Sinhala', 'Asia'),
            ('BTN', 'Bhutan', 'Dzongkha', 'Asia'),
            ('MUS', 'Mauritius', 'English', 'Africa'),
            ('FJI', 'Fiji', 'English', 'Oceania'),
            ('SGP', 'Singapore', 'English', 'Asia'),
            ('MYS', 'Malaysia', 'Malay', 'Asia'),
        ],
        'target': 300000
    },
    'Buddhism': {
        'countries': [
            ('THA', 'Thailand', 'Thai', 'Asia'),
            ('MMR', 'Myanmar', 'Burmese', 'Asia'),
            ('LKA', 'Sri Lanka', 'Sinhala', 'Asia'),
            ('BTN', 'Bhutan', 'Dzongkha', 'Asia'),
            ('KHM', 'Cambodia', 'Khmer', 'Asia'),
            ('LAO', 'Laos', 'Lao', 'Asia'),
            ('VNM', 'Vietnam', 'Vietnamese', 'Asia'),
            ('JPN', 'Japan', 'Japanese', 'Asia'),
            ('TWN', 'Taiwan', 'Chinese', 'Asia'),
            ('MNG', 'Mongolia', 'Mongolian', 'Asia'),
            ('CHN', 'China', 'Chinese', 'Asia'),
            ('KOR', 'South Korea', 'Korean', 'Asia'),
        ],
        'target': 200000
    },
    'Judaism': {
        'countries': [
            ('ISR', 'Israel', 'Hebrew', 'Asia'),
            ('USA', 'United States', 'English', 'Americas'),
            ('GBR', 'United Kingdom', 'English', 'Europe'),
            ('FRA', 'France', 'French', 'Europe'),
            ('CAN', 'Canada', 'English', 'Americas'),
            ('ARG', 'Argentina', 'Spanish', 'Americas'),
            ('DEU', 'Germany', 'German', 'Europe'),
            ('AUS', 'Australia', 'English', 'Oceania'),
            ('RUS', 'Russia', 'Russian', 'Europe'),
            ('UKR', 'Ukraine', 'Ukrainian', 'Europe'),
            ('NLD', 'Netherlands', 'Dutch', 'Europe'),
            ('BEL', 'Belgium', 'French', 'Europe'),
            ('ITA', 'Italy', 'Italian', 'Europe'),
            ('POL', 'Poland', 'Polish', 'Europe'),
            ('HUN', 'Hungary', 'Hungarian', 'Europe'),
        ],
        'target': 100000
    },
    'Christianity': {
        'countries': [
            # Batı Avrupa
            ('GBR', 'United Kingdom', 'English', 'Europe'),
            ('IRL', 'Ireland', 'English', 'Europe'),
            ('FRA', 'France', 'French', 'Europe'),
            ('DEU', 'Germany', 'German', 'Europe'),
            ('NLD', 'Netherlands', 'Dutch', 'Europe'),
            ('BEL', 'Belgium', 'French', 'Europe'),
            ('LUX', 'Luxembourg', 'French', 'Europe'),
            ('CHE', 'Switzerland', 'German', 'Europe'),
            ('AUT', 'Austria', 'German', 'Europe'),
            # Güney Avrupa
            ('ESP', 'Spain', 'Spanish', 'Europe'),
            ('PRT', 'Portugal', 'Portuguese', 'Europe'),
            ('ITA', 'Italy', 'Italian', 'Europe'),
            ('GRC', 'Greece', 'Greek', 'Europe'),
            ('MLT', 'Malta', 'English', 'Europe'),
            # Doğu Avrupa
            ('POL', 'Poland', 'Polish', 'Europe'),
            ('CZE', 'Czech Republic', 'Czech', 'Europe'),
            ('SVK', 'Slovakia', 'Slovak', 'Europe'),
            ('HUN', 'Hungary', 'Hungarian', 'Europe'),
            ('ROU', 'Romania', 'Romanian', 'Europe'),
            ('BGR', 'Bulgaria', 'Bulgarian', 'Europe'),
            ('SRB', 'Serbia', 'Serbian', 'Europe'),
            ('HRV', 'Croatia', 'Croatian', 'Europe'),
            ('SVN', 'Slovenia', 'Slovenian', 'Europe'),
            ('RUS', 'Russia', 'Russian', 'Europe'),
            ('UKR', 'Ukraine', 'Ukrainian', 'Europe'),
            ('BLR', 'Belarus', 'Belarusian', 'Europe'),
            # Kuzey Avrupa
            ('SWE', 'Sweden', 'Swedish', 'Europe'),
            ('NOR', 'Norway', 'Norwegian', 'Europe'),
            ('DNK', 'Denmark', 'Danish', 'Europe'),
            ('FIN', 'Finland', 'Finnish', 'Europe'),
            ('ISL', 'Iceland', 'Icelandic', 'Europe'),
            # Amerika
            ('USA', 'United States', 'English', 'Americas'),
            ('CAN', 'Canada', 'English', 'Americas'),
            ('MEX', 'Mexico', 'Spanish', 'Americas'),
            ('BRA', 'Brazil', 'Portuguese', 'Americas'),
            ('ARG', 'Argentina', 'Spanish', 'Americas'),
            ('CHL', 'Chile', 'Spanish', 'Americas'),
            ('COL', 'Colombia', 'Spanish', 'Americas'),
            ('PER', 'Peru', 'Spanish', 'Americas'),
            ('VEN', 'Venezuela', 'Spanish', 'Americas'),
            ('ECU', 'Ecuador', 'Spanish', 'Americas'),
            ('CUB', 'Cuba', 'Spanish', 'Americas'),
            ('DOM', 'Dominican Republic', 'Spanish', 'Americas'),
            ('GTM', 'Guatemala', 'Spanish', 'Americas'),
            ('HND', 'Honduras', 'Spanish', 'Americas'),
            ('SLV', 'El Salvador', 'Spanish', 'Americas'),
            ('NIC', 'Nicaragua', 'Spanish', 'Americas'),
            ('CRI', 'Costa Rica', 'Spanish', 'Americas'),
            ('PAN', 'Panama', 'Spanish', 'Americas'),
            ('URY', 'Uruguay', 'Spanish', 'Americas'),
            ('PRY', 'Paraguay', 'Spanish', 'Americas'),
            ('BOL', 'Bolivia', 'Spanish', 'Americas'),
            # Afrika
            ('NGA', 'Nigeria', 'English', 'Africa'),
            ('GHA', 'Ghana', 'English', 'Africa'),
            ('KEN', 'Kenya', 'Swahili', 'Africa'),
            ('TZA', 'Tanzania', 'Swahili', 'Africa'),
            ('UGA', 'Uganda', 'English', 'Africa'),
            ('RWA', 'Rwanda', 'Kinyarwanda', 'Africa'),
            ('ETH', 'Ethiopia', 'Amharic', 'Africa'),
            ('ZAF', 'South Africa', 'English', 'Africa'),
            ('ZWE', 'Zimbabwe', 'English', 'Africa'),
            ('ZMB', 'Zambia', 'English', 'Africa'),
            ('COD', 'DR Congo', 'French', 'Africa'),
            ('AGO', 'Angola', 'Portuguese', 'Africa'),
            ('MOZ', 'Mozambique', 'Portuguese', 'Africa'),
            ('CMR', 'Cameroon', 'French', 'Africa'),
            # Okyanusya
            ('AUS', 'Australia', 'English', 'Oceania'),
            ('NZL', 'New Zealand', 'English', 'Oceania'),
            ('PNG', 'Papua New Guinea', 'English', 'Oceania'),
            ('FJI', 'Fiji', 'English', 'Oceania'),
            # Asya
            ('PHL', 'Philippines', 'Filipino', 'Asia'),
            ('KOR', 'South Korea', 'Korean', 'Asia'),
        ],
        'target': 800000
    }
}

def expand_database():
    """Veritabanını genişlet"""

    print("=" * 80)
    print("VERİTABANI GENİŞLETME - FULL COMBINATIONS")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Her din için işlem
    total_added = 0

    for religion, config in RELIGION_EXPANSIONS.items():
        print(f"\n{religion} genişletiliyor...")

        # Bu dinin mevcut first name'lerini al
        cursor.execute("""
            SELECT DISTINCT name, gender
            FROM names
            WHERE religion = ? AND name_type = 'first'
        """, (religion,))
        first_names = cursor.fetchall()

        # Bu dinin mevcut last name'lerini al
        cursor.execute("""
            SELECT DISTINCT name
            FROM names
            WHERE religion = ? AND name_type = 'last'
        """, (religion,))
        last_names = [row[0] for row in cursor.fetchall()]

        if not first_names or not last_names:
            print(f"  ✗ {religion} için isim bulunamadı")
            continue

        print(f"  First names: {len(first_names):,}")
        print(f"  Last names: {len(last_names):,}")
        print(f"  Countries: {len(config['countries'])}")

        # Her ülke için kayıt oluştur
        countries = config['countries']
        added = 0

        # Target'a ulaşana kadar döngü
        target = config['target']
        per_country = target // len(countries)

        for country_code, country_name, language, region in countries:
            country_added = 0

            # First names
            for first_name, gender in random.sample(first_names, min(len(first_names), per_country // 2)):
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO names
                        (name, name_type, country_code, region, language, religion, gender, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (first_name, 'first', country_code, region, language, religion, gender, 'synthetic_expanded'))

                    if cursor.rowcount > 0:
                        country_added += 1
                except:
                    pass

            # Last names
            for last_name in random.sample(last_names, min(len(last_names), per_country // 2)):
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO names
                        (name, name_type, country_code, region, language, religion, gender, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (last_name, 'last', country_code, region, language, religion, None, 'synthetic_expanded'))

                    if cursor.rowcount > 0:
                        country_added += 1
                except:
                    pass

            added += country_added

        conn.commit()
        print(f"  ✓ {added:,} yeni kayıt eklendi")
        total_added += added

    # Final stats
    cursor.execute("SELECT COUNT(*) FROM names")
    total = cursor.fetchone()[0]

    print("\n" + "=" * 80)
    print(f"✓ TOPLAM {total_added:,} yeni kayıt eklendi")
    print(f"✓ Veritabanı toplam kayıt: {total:,}")
    print("=" * 80)

    # Optimize
    print("\nVERİTABANI OPTİMİZE EDİLİYOR...")
    conn.execute("VACUUM")
    print("✓ Optimize tamamlandı")

    # Boyut
    size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"\nVeritabanı Boyutu: {size_mb:.2f} MB")

    conn.close()

if __name__ == "__main__":
    expand_database()
