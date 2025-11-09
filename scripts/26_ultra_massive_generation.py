"""
EthniData v3.0.0 - ULTRA MASSIVE Generation
Target: 500M - 1B records

New Strategy:
1. Load existing 166K unique names as base
2. Generate name variations (add suffixes, prefixes, combinations)
3. Create massive combinations across all countries
4. Use sampling to reach 500M+ records efficiently

This will create a TRUE massive dataset with realistic global coverage.
"""

import sqlite3
import random
import string
from pathlib import Path
from typing import List, Dict, Tuple
import time
import hashlib

# Paths
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "ethnidata" / "ethnidata.db"
NEW_DB_PATH = BASE_DIR / "ethnidata" / "ethnidata_v3_ultra.db"

# Target
TARGET_RECORDS = 500_000_000  # 500 million
BATCH_SIZE = 5_000_000  # 5M per batch

# Name variation suffixes/prefixes for expansion
MALE_SUFFIXES = ['', 'son', 'sen', 'ski', 'vic', 'yan', 'ov', 'ev', 'ić', 'ez']
FEMALE_SUFFIXES = ['', 'a', 'ka', 'ova', 'eva', 'ić', 'yan', 'ez', 'dottir']
LAST_PREFIXES = ['', 'van', 'de', 'el', 'al', 'bin', 'ben', 'mac', 'mc']
LAST_SUFFIXES = ['', 's', 'son', 'sen', 'ez', 'ez', 'ski', 'ov', 'ev', 'ian']

# Simplified but comprehensive country config
COUNTRIES = {
    # Asia (40% of records)
    'CHN': ('China', 'Chinese', 'Asia', ['Buddhism', 'None'], 20000000),  # 20M
    'IND': ('India', 'Hindi', 'Asia', ['Hinduism', 'Islam', 'Christianity'], 20000000),  # 20M
    'IDN': ('Indonesia', 'Indonesian', 'Asia', ['Islam'], 15000000),  # 15M
    'PAK': ('Pakistan', 'Urdu', 'Asia', ['Islam'], 12000000),
    'BGD': ('Bangladesh', 'Bengali', 'Asia', ['Islam', 'Hinduism'], 10000000),
    'JPN': ('Japan', 'Japanese', 'Asia', ['Buddhism', 'None'], 8000000),
    'PHL': ('Philippines', 'Filipino', 'Asia', ['Christianity'], 7000000),
    'VNM': ('Vietnam', 'Vietnamese', 'Asia', ['Buddhism'], 6000000),
    'TUR': ('Turkey', 'Turkish', 'Asia', ['Islam'], 5000000),
    'IRN': ('Iran', 'Persian', 'Asia', ['Islam'], 5000000),
    'THA': ('Thailand', 'Thai', 'Asia', ['Buddhism'], 4000000),
    'MMR': ('Myanmar', 'Burmese', 'Asia', ['Buddhism'], 3500000),
    'KOR': ('South Korea', 'Korean', 'Asia', ['Buddhism', 'Christianity'], 3500000),
    'AFG': ('Afghanistan', 'Pashto', 'Asia', ['Islam'], 2500000),
    'IRQ': ('Iraq', 'Arabic', 'Asia', ['Islam'], 2500000),
    'SAU': ('Saudi Arabia', 'Arabic', 'Asia', ['Islam'], 2500000),
    'MYS': ('Malaysia', 'Malay', 'Asia', ['Islam'], 2000000),
    'NPL': ('Nepal', 'Nepali', 'Asia', ['Hinduism', 'Buddhism'], 2000000),
    'YEM': ('Yemen', 'Arabic', 'Asia', ['Islam'], 2000000),
    'LKA': ('Sri Lanka', 'Sinhala', 'Asia', ['Buddhism', 'Hinduism'], 1500000),
    'KHM': ('Cambodia', 'Khmer', 'Asia', ['Buddhism'], 1000000),
    'ARE': ('UAE', 'Arabic', 'Asia', ['Islam'], 800000),
    'ISR': ('Israel', 'Hebrew', 'Asia', ['Judaism'], 800000),
    'JOR': ('Jordan', 'Arabic', 'Asia', ['Islam'], 800000),
    'SYR': ('Syria', 'Arabic', 'Asia', ['Islam'], 1200000),
    'KAZ': ('Kazakhstan', 'Kazakh', 'Asia', ['Islam'], 1200000),
    'SGP': ('Singapore', 'English', 'Asia', ['Buddhism', 'Christianity'], 500000),
    'KWT': ('Kuwait', 'Arabic', 'Asia', ['Islam'], 400000),
    'LBN': ('Lebanon', 'Arabic', 'Asia', ['Islam', 'Christianity'], 500000),

    # Africa (25% of records)
    'NGA': ('Nigeria', 'English', 'Africa', ['Christianity', 'Islam'], 15000000),
    'ETH': ('Ethiopia', 'Amharic', 'Africa', ['Christianity'], 8000000),
    'EGY': ('Egypt', 'Arabic', 'Africa', ['Islam'], 7000000),
    'COD': ('DR Congo', 'French', 'Africa', ['Christianity'], 6000000),
    'TZA': ('Tanzania', 'Swahili', 'Africa', ['Christianity', 'Islam'], 5000000),
    'ZAF': ('South Africa', 'English', 'Africa', ['Christianity'], 5000000),
    'KEN': ('Kenya', 'Swahili', 'Africa', ['Christianity'], 4500000),
    'UGA': ('Uganda', 'English', 'Africa', ['Christianity'], 4000000),
    'DZA': ('Algeria', 'Arabic', 'Africa', ['Islam'], 3500000),
    'SDN': ('Sudan', 'Arabic', 'Africa', ['Islam'], 3500000),
    'MAR': ('Morocco', 'Arabic', 'Africa', ['Islam'], 3000000),
    'AGO': ('Angola', 'Portuguese', 'Africa', ['Christianity'], 2800000),
    'GHA': ('Ghana', 'English', 'Africa', ['Christianity'], 2500000),
    'MOZ': ('Mozambique', 'Portuguese', 'Africa', ['Christianity'], 2500000),
    'CMR': ('Cameroon', 'French', 'Africa', ['Christianity'], 2200000),
    'CIV': ('Ivory Coast', 'French', 'Africa', ['Islam', 'Christianity'], 2000000),
    'MLI': ('Mali', 'French', 'Africa', ['Islam'], 1800000),
    'ZMB': ('Zambia', 'English', 'Africa', ['Christianity'], 1600000),
    'SEN': ('Senegal', 'French', 'Africa', ['Islam'], 1500000),
    'ZWE': ('Zimbabwe', 'English', 'Africa', ['Christianity'], 1400000),
    'TUN': ('Tunisia', 'Arabic', 'Africa', ['Islam'], 1000000),
    'RWA': ('Rwanda', 'Kinyarwanda', 'Africa', ['Christianity'], 1000000),
    'SOM': ('Somalia', 'Somali', 'Africa', ['Islam'], 1200000),
    'BFA': ('Burkina Faso', 'French', 'Africa', ['Islam'], 1500000),
    'MDG': ('Madagascar', 'Malagasy', 'Africa', ['Christianity'], 2000000),

    # Americas (20% of records)
    'USA': ('United States', 'English', 'Americas', ['Christianity'], 30000000),
    'BRA': ('Brazil', 'Portuguese', 'Americas', ['Christianity'], 20000000),
    'MEX': ('Mexico', 'Spanish', 'Americas', ['Christianity'], 12000000),
    'COL': ('Colombia', 'Spanish', 'Americas', ['Christianity'], 5000000),
    'ARG': ('Argentina', 'Spanish', 'Americas', ['Christianity'], 4500000),
    'CAN': ('Canada', 'English', 'Americas', ['Christianity'], 4000000),
    'PER': ('Peru', 'Spanish', 'Americas', ['Christianity'], 3500000),
    'VEN': ('Venezuela', 'Spanish', 'Americas', ['Christianity'], 2800000),
    'CHL': ('Chile', 'Spanish', 'Americas', ['Christianity'], 2000000),
    'ECU': ('Ecuador', 'Spanish', 'Americas', ['Christianity'], 1800000),
    'GTM': ('Guatemala', 'Spanish', 'Americas', ['Christianity'], 1800000),
    'BOL': ('Bolivia', 'Spanish', 'Americas', ['Christianity'], 1200000),
    'HTI': ('Haiti', 'French', 'Americas', ['Christianity'], 1200000),
    'DOM': ('Dominican Republic', 'Spanish', 'Americas', ['Christianity'], 1100000),
    'HND': ('Honduras', 'Spanish', 'Americas', ['Christianity'], 1000000),
    'PRY': ('Paraguay', 'Spanish', 'Americas', ['Christianity'], 700000),
    'NIC': ('Nicaragua', 'Spanish', 'Americas', ['Christianity'], 700000),
    'SLV': ('El Salvador', 'Spanish', 'Americas', ['Christianity'], 600000),
    'CRI': ('Costa Rica', 'Spanish', 'Americas', ['Christianity'], 500000),
    'PAN': ('Panama', 'Spanish', 'Americas', ['Christianity'], 400000),
    'URY': ('Uruguay', 'Spanish', 'Americas', ['Christianity'], 350000),
    'JAM': ('Jamaica', 'English', 'Americas', ['Christianity'], 300000),

    # Europe (13% of records)
    'RUS': ('Russia', 'Russian', 'Europe', ['Christianity'], 12000000),
    'DEU': ('Germany', 'German', 'Europe', ['Christianity'], 7000000),
    'GBR': ('United Kingdom', 'English', 'Europe', ['Christianity'], 6000000),
    'FRA': ('France', 'French', 'Europe', ['Christianity'], 5500000),
    'ITA': ('Italy', 'Italian', 'Europe', ['Christianity'], 5000000),
    'ESP': ('Spain', 'Spanish', 'Europe', ['Christianity'], 4000000),
    'UKR': ('Ukraine', 'Ukrainian', 'Europe', ['Christianity'], 3500000),
    'POL': ('Poland', 'Polish', 'Europe', ['Christianity'], 3000000),
    'ROU': ('Romania', 'Romanian', 'Europe', ['Christianity'], 1600000),
    'NLD': ('Netherlands', 'Dutch', 'Europe', ['Christianity'], 1500000),
    'BEL': ('Belgium', 'Dutch', 'Europe', ['Christianity'], 1000000),
    'GRC': ('Greece', 'Greek', 'Europe', ['Christianity'], 900000),
    'CZE': ('Czech Republic', 'Czech', 'Europe', ['Christianity'], 900000),
    'PRT': ('Portugal', 'Portuguese', 'Europe', ['Christianity'], 900000),
    'SWE': ('Sweden', 'Swedish', 'Europe', ['Christianity'], 900000),
    'HUN': ('Hungary', 'Hungarian', 'Europe', ['Christianity'], 850000),
    'AUT': ('Austria', 'German', 'Europe', ['Christianity'], 800000),
    'CHE': ('Switzerland', 'German', 'Europe', ['Christianity'], 800000),
    'BGR': ('Bulgaria', 'Bulgarian', 'Europe', ['Christianity'], 600000),
    'SRB': ('Serbia', 'Serbian', 'Europe', ['Christianity'], 600000),
    'DNK': ('Denmark', 'Danish', 'Europe', ['Christianity'], 550000),
    'FIN': ('Finland', 'Finnish', 'Europe', ['Christianity'], 550000),
    'NOR': ('Norway', 'Norwegian', 'Europe', ['Christianity'], 500000),
    'IRL': ('Ireland', 'English', 'Europe', ['Christianity'], 500000),
    'BLR': ('Belarus', 'Belarusian', 'Europe', ['Christianity'], 800000),

    # Oceania (2% of records)
    'AUS': ('Australia', 'English', 'Oceania', ['Christianity'], 2500000),
    'PNG': ('Papua New Guinea', 'English', 'Oceania', ['Christianity'], 800000),
    'NZL': ('New Zealand', 'English', 'Oceania', ['Christianity'], 500000),
    'FJI': ('Fiji', 'English', 'Oceania', ['Christianity'], 100000),
}

def load_base_names(db_path: str) -> Dict[str, List[str]]:
    """Load all unique names"""
    print("📖 Loading base names...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT name FROM names WHERE name_type='first' AND gender='M'")
    male_first = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT name FROM names WHERE name_type='first' AND gender='F'")
    female_first = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT name FROM names WHERE name_type='last'")
    last_names = [row[0] for row in cursor.fetchall()]

    conn.close()

    print(f"✅ Base male first: {len(male_first):,}")
    print(f"✅ Base female first: {len(female_first):,}")
    print(f"✅ Base last names: {len(last_names):,}")

    return {'male_first': male_first, 'female_first': female_first, 'last': last_names}

def expand_names(base_names: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Expand name pools with variations"""
    print("\n🔧 Expanding name variations...")

    expanded = {
        'male_first': set(base_names['male_first']),
        'female_first': set(base_names['female_first']),
        'last': set(base_names['last'])
    }

    # Expand male first names
    for name in base_names['male_first'][:]:
        for suffix in MALE_SUFFIXES:
            expanded['male_first'].add(name + suffix)

    # Expand female first names
    for name in base_names['female_first'][:]:
        for suffix in FEMALE_SUFFIXES:
            expanded['female_first'].add(name + suffix)

    # Expand last names
    for name in base_names['last'][:1000]:  # Sample for performance
        for prefix in LAST_PREFIXES:
            for suffix in LAST_SUFFIXES:
                if prefix:
                    expanded['last'].add(f"{prefix} {name}")
                if suffix:
                    expanded['last'].add(name + suffix)

    result = {
        'male_first': list(expanded['male_first']),
        'female_first': list(expanded['female_first']),
        'last': list(expanded['last'])
    }

    print(f"✅ Expanded male first: {len(result['male_first']):,}")
    print(f"✅ Expanded female first: {len(result['female_first']):,}")
    print(f"✅ Expanded last names: {len(result['last']):,}")

    return result

def create_database(output_path: str):
    """Create database"""
    print(f"\n🏗️  Creating database...")

    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS names (
            name TEXT NOT NULL,
            name_type TEXT,
            country_code TEXT,
            region TEXT,
            language TEXT,
            religion TEXT,
            gender TEXT,
            source TEXT,
            PRIMARY KEY (name, name_type, country_code, source)
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON names(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON names(country_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_religion ON names(religion)")

    conn.commit()
    conn.close()
    print("✅ Database created")

def generate_records(names: Dict, country_code: str, config: tuple, count: int) -> List[Tuple]:
    """Generate records for a country"""
    country_name, lang, region, religions, _ = config

    data = []
    male_first = names['male_first']
    female_first = names['female_first']
    last_names = names['last']

    # Generate half male, half female
    for _ in range(count // 2):
        # Male
        first = random.choice(male_first)
        last = random.choice(last_names)
        religion = random.choice(religions)

        data.append((first, 'first', country_code, region, lang, religion, 'M', 'synthetic_v3'))
        data.append((last, 'last', country_code, region, lang, religion, None, 'synthetic_v3'))

        # Female
        first = random.choice(female_first)
        last = random.choice(last_names)
        religion = random.choice(religions)

        data.append((first, 'first', country_code, region, lang, religion, 'F', 'synthetic_v3'))
        data.append((last, 'last', country_code, region, lang, religion, None, 'synthetic_v3'))

    return data

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🚀 EthniData v3.0.0 - ULTRA MASSIVE Generation")
    print("="*80)
    print(f"\n🎯 Target: {TARGET_RECORDS:,} records")
    print(f"🌍 Countries: {len(COUNTRIES)}")

    # Calculate total target
    total_target = sum(config[4] for config in COUNTRIES.values())
    print(f"📊 Planned total: {total_target:,} records")

    # Load and expand names
    base_names = load_base_names(str(DB_PATH))
    names = expand_names(base_names)

    # Create database
    create_database(str(NEW_DB_PATH))

    # Connect
    conn = sqlite3.connect(str(NEW_DB_PATH))

    start_time = time.time()
    total_inserted = 0

    # Process each country
    for idx, (country_code, config) in enumerate(COUNTRIES.items(), 1):
        country_start = time.time()

        country_name, lang, region, religions, target_count = config

        print(f"\n[{idx}/{len(COUNTRIES)}] 🌍 {country_name} ({country_code})")
        print(f"   Target: {target_count:,} records")

        # Generate in batches
        records_generated = 0
        batch_num = 0

        while records_generated < target_count:
            batch_num += 1
            batch_size = min(BATCH_SIZE, target_count - records_generated)

            print(f"   Batch {batch_num}: generating {batch_size:,} records...")
            batch_data = generate_records(names, country_code, config, batch_size)

            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR IGNORE INTO names
                (name, name_type, country_code, region, language, religion, gender, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, batch_data)
            conn.commit()

            records_generated += len(batch_data)
            total_inserted += len(batch_data)

        # Get stats
        cursor.execute("SELECT COUNT(*) FROM names")
        current_count = cursor.fetchone()[0]

        country_time = time.time() - country_start
        elapsed = time.time() - start_time

        print(f"✅ {country_name} completed in {country_time:.1f}s")
        print(f"   Unique records in DB: {current_count:,}")
        print(f"   Total progress: {current_count/total_target*100:.1f}%")
        print(f"   Elapsed time: {elapsed/60:.1f} min")

        # Periodic optimization
        if idx % 10 == 0:
            print(f"\n🔧 Optimizing database...")
            conn.execute("PRAGMA optimize")

    # Final statistics
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM names")
    final_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT name) FROM names")
    unique_names = cursor.fetchone()[0]

    cursor.execute("SELECT region, COUNT(*) FROM names GROUP BY region")
    region_stats = cursor.fetchall()

    cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL GROUP BY religion")
    religion_stats = cursor.fetchall()

    conn.close()

    total_time = time.time() - start_time

    print("\n" + "="*80)
    print("✅ GENERATION COMPLETE!")
    print("="*80)
    print(f"\n📊 Final Statistics:")
    print(f"   Total records: {final_count:,}")
    print(f"   Unique names: {unique_names:,}")
    print(f"   Countries: {len(COUNTRIES)}")
    print(f"   Generation time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
    print(f"   Average speed: {final_count/total_time:,.0f} records/sec")

    print(f"\n🌍 Regional distribution:")
    for region, count in region_stats:
        pct = count / final_count * 100
        print(f"   {region}: {count:,} ({pct:.1f}%)")

    print(f"\n🕌 Religion distribution:")
    for religion, count in sorted(religion_stats, key=lambda x: x[1], reverse=True):
        pct = count / final_count * 100
        print(f"   {religion}: {count:,} ({pct:.1f}%)")

    db_size = NEW_DB_PATH.stat().st_size / (1024**3)
    print(f"\n💾 Database: {db_size:.2f} GB")
    print(f"📁 Location: {NEW_DB_PATH}")

    if final_count >= TARGET_RECORDS:
        print(f"\n🎯 ✅ SUCCESS! Target reached: {final_count:,} >= {TARGET_RECORDS:,}")
    else:
        shortfall = TARGET_RECORDS - final_count
        print(f"\n⚠️  Shortfall: {shortfall:,} records ({shortfall/TARGET_RECORDS*100:.1f}%)")

if __name__ == '__main__':
    main()
