"""
EthniData v3.0.0 - SMART Massive Synthetic Data Generation
Target: 500M - 1B records using smart combinatorics

Strategy:
Instead of generating randomly, we'll use smart combinations:
1. Load all unique first names (male/female)
2. Load all unique last names
3. For each country, generate all reasonable combinations
4. This ensures maximum diversity and coverage

Estimated combinations:
- 80K male first names × 150K last names × 150 countries = 1.8 BILLION combinations
- 80K female first names × 150K last names × 150 countries = 1.8 BILLION combinations
- Total potential: 3.6 BILLION unique records

We'll generate in smart batches with deduplication.
"""

import sqlite3
import random
import itertools
from pathlib import Path
from typing import List, Dict, Tuple, Set
import time
import multiprocessing as mp
from functools import partial

# Paths
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "ethnidata" / "ethnidata.db"
NEW_DB_PATH = BASE_DIR / "ethnidata" / "ethnidata_v3_ultimate.db"

# Target range
MIN_TARGET = 500_000_000  # 500M minimum
MAX_TARGET = 1_500_000_000  # 1.5B maximum (if possible)

# Batch configuration
BATCH_SIZE = 10_000_000  # 10M records per batch

# Comprehensive country mapping with population weights and naming conventions
COUNTRY_CONFIG = {
    # High-population Asian countries (billions)
    'CHN': {'name': 'China', 'lang': 'Chinese', 'region': 'Asia', 'religions': ['Buddhism', 'None'], 'weight': 1400, 'combos': 1000000},
    'IND': {'name': 'India', 'lang': 'Hindi', 'region': 'Asia', 'religions': ['Hinduism', 'Islam', 'Christianity'], 'weight': 1400, 'combos': 1000000},
    'IDN': {'name': 'Indonesia', 'lang': 'Indonesian', 'region': 'Asia', 'religions': ['Islam'], 'weight': 275, 'combos': 500000},
    'PAK': {'name': 'Pakistan', 'lang': 'Urdu', 'region': 'Asia', 'religions': ['Islam'], 'weight': 230, 'combos': 400000},
    'BGD': {'name': 'Bangladesh', 'lang': 'Bengali', 'region': 'Asia', 'religions': ['Islam', 'Hinduism'], 'weight': 170, 'combos': 350000},
    'JPN': {'name': 'Japan', 'lang': 'Japanese', 'region': 'Asia', 'religions': ['Buddhism', 'None'], 'weight': 125, 'combos': 300000},
    'PHL': {'name': 'Philippines', 'lang': 'Filipino', 'region': 'Asia', 'religions': ['Christianity'], 'weight': 115, 'combos': 250000},
    'VNM': {'name': 'Vietnam', 'lang': 'Vietnamese', 'region': 'Asia', 'religions': ['Buddhism'], 'weight': 98, 'combos': 200000},
    'TUR': {'name': 'Turkey', 'lang': 'Turkish', 'region': 'Asia', 'religions': ['Islam'], 'weight': 85, 'combos': 180000},
    'IRN': {'name': 'Iran', 'lang': 'Persian', 'region': 'Asia', 'religions': ['Islam'], 'weight': 85, 'combos': 180000},
    'THA': {'name': 'Thailand', 'lang': 'Thai', 'region': 'Asia', 'religions': ['Buddhism'], 'weight': 70, 'combos': 150000},
    'MMR': {'name': 'Myanmar', 'lang': 'Burmese', 'region': 'Asia', 'religions': ['Buddhism'], 'weight': 55, 'combos': 120000},
    'KOR': {'name': 'South Korea', 'lang': 'Korean', 'region': 'Asia', 'religions': ['Buddhism', 'Christianity'], 'weight': 52, 'combos': 120000},
    'AFG': {'name': 'Afghanistan', 'lang': 'Pashto', 'region': 'Asia', 'religions': ['Islam'], 'weight': 40, 'combos': 90000},
    'IRQ': {'name': 'Iraq', 'lang': 'Arabic', 'region': 'Asia', 'religions': ['Islam'], 'weight': 42, 'combos': 90000},
    'SAU': {'name': 'Saudi Arabia', 'lang': 'Arabic', 'region': 'Asia', 'religions': ['Islam'], 'weight': 36, 'combos': 80000},
    'MYS': {'name': 'Malaysia', 'lang': 'Malay', 'region': 'Asia', 'religions': ['Islam'], 'weight': 33, 'combos': 70000},
    'NPL': {'name': 'Nepal', 'lang': 'Nepali', 'region': 'Asia', 'religions': ['Hinduism', 'Buddhism'], 'weight': 30, 'combos': 65000},
    'YEM': {'name': 'Yemen', 'lang': 'Arabic', 'region': 'Asia', 'religions': ['Islam'], 'weight': 30, 'combos': 65000},
    'LKA': {'name': 'Sri Lanka', 'lang': 'Sinhala', 'region': 'Asia', 'religions': ['Buddhism', 'Hinduism'], 'weight': 22, 'combos': 50000},
    'KHM': {'name': 'Cambodia', 'lang': 'Khmer', 'region': 'Asia', 'religions': ['Buddhism'], 'weight': 17, 'combos': 40000},
    'ARE': {'name': 'UAE', 'lang': 'Arabic', 'region': 'Asia', 'religions': ['Islam'], 'weight': 10, 'combos': 30000},
    'ISR': {'name': 'Israel', 'lang': 'Hebrew', 'region': 'Asia', 'religions': ['Judaism'], 'weight': 9, 'combos': 30000},
    'JOR': {'name': 'Jordan', 'lang': 'Arabic', 'region': 'Asia', 'religions': ['Islam'], 'weight': 11, 'combos': 30000},
    'SYR': {'name': 'Syria', 'lang': 'Arabic', 'region': 'Asia', 'religions': ['Islam'], 'weight': 18, 'combos': 40000},
    'KAZ': {'name': 'Kazakhstan', 'lang': 'Kazakh', 'region': 'Asia', 'religions': ['Islam'], 'weight': 19, 'combos': 40000},
    'SGP': {'name': 'Singapore', 'lang': 'English', 'region': 'Asia', 'religions': ['Buddhism', 'Christianity'], 'weight': 6, 'combos': 20000},

    # African countries (hundreds of millions)
    'NGA': {'name': 'Nigeria', 'lang': 'English', 'region': 'Africa', 'religions': ['Christianity', 'Islam'], 'weight': 220, 'combos': 400000},
    'ETH': {'name': 'Ethiopia', 'lang': 'Amharic', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 120, 'combos': 250000},
    'EGY': {'name': 'Egypt', 'lang': 'Arabic', 'region': 'Africa', 'religions': ['Islam'], 'weight': 105, 'combos': 220000},
    'COD': {'name': 'DR Congo', 'lang': 'French', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 95, 'combos': 200000},
    'TZA': {'name': 'Tanzania', 'lang': 'Swahili', 'region': 'Africa', 'religions': ['Christianity', 'Islam'], 'weight': 65, 'combos': 140000},
    'ZAF': {'name': 'South Africa', 'lang': 'English', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 60, 'combos': 130000},
    'KEN': {'name': 'Kenya', 'lang': 'Swahili', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 55, 'combos': 120000},
    'UGA': {'name': 'Uganda', 'lang': 'English', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 48, 'combos': 100000},
    'DZA': {'name': 'Algeria', 'lang': 'Arabic', 'region': 'Africa', 'religions': ['Islam'], 'weight': 45, 'combos': 95000},
    'SDN': {'name': 'Sudan', 'lang': 'Arabic', 'region': 'Africa', 'religions': ['Islam'], 'weight': 45, 'combos': 95000},
    'MAR': {'name': 'Morocco', 'lang': 'Arabic', 'region': 'Africa', 'religions': ['Islam'], 'weight': 37, 'combos': 80000},
    'AGO': {'name': 'Angola', 'lang': 'Portuguese', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 35, 'combos': 75000},
    'GHA': {'name': 'Ghana', 'lang': 'English', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 32, 'combos': 70000},
    'MOZ': {'name': 'Mozambique', 'lang': 'Portuguese', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 32, 'combos': 70000},
    'CMR': {'name': 'Cameroon', 'lang': 'French', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 28, 'combos': 60000},
    'CIV': {'name': 'Ivory Coast', 'lang': 'French', 'region': 'Africa', 'religions': ['Islam', 'Christianity'], 'weight': 27, 'combos': 58000},
    'MLI': {'name': 'Mali', 'lang': 'French', 'region': 'Africa', 'religions': ['Islam'], 'weight': 21, 'combos': 45000},
    'ZMB': {'name': 'Zambia', 'lang': 'English', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 19, 'combos': 42000},
    'SEN': {'name': 'Senegal', 'lang': 'French', 'region': 'Africa', 'religions': ['Islam'], 'weight': 17, 'combos': 38000},
    'ZWE': {'name': 'Zimbabwe', 'lang': 'English', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 15, 'combos': 35000},
    'TUN': {'name': 'Tunisia', 'lang': 'Arabic', 'region': 'Africa', 'religions': ['Islam'], 'weight': 12, 'combos': 28000},
    'RWA': {'name': 'Rwanda', 'lang': 'Kinyarwanda', 'region': 'Africa', 'religions': ['Christianity'], 'weight': 13, 'combos': 30000},

    # European countries
    'RUS': {'name': 'Russia', 'lang': 'Russian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 145, 'combos': 300000},
    'DEU': {'name': 'Germany', 'lang': 'German', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 84, 'combos': 180000},
    'GBR': {'name': 'United Kingdom', 'lang': 'English', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 68, 'combos': 150000},
    'FRA': {'name': 'France', 'lang': 'French', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 65, 'combos': 140000},
    'ITA': {'name': 'Italy', 'lang': 'Italian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 60, 'combos': 130000},
    'ESP': {'name': 'Spain', 'lang': 'Spanish', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 47, 'combos': 100000},
    'UKR': {'name': 'Ukraine', 'lang': 'Ukrainian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 44, 'combos': 95000},
    'POL': {'name': 'Poland', 'lang': 'Polish', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 38, 'combos': 82000},
    'ROU': {'name': 'Romania', 'lang': 'Romanian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 19, 'combos': 42000},
    'NLD': {'name': 'Netherlands', 'lang': 'Dutch', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 17, 'combos': 38000},
    'BEL': {'name': 'Belgium', 'lang': 'Dutch', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 12, 'combos': 28000},
    'GRC': {'name': 'Greece', 'lang': 'Greek', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 10, 'combos': 25000},
    'CZE': {'name': 'Czech Republic', 'lang': 'Czech', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 11, 'combos': 26000},
    'PRT': {'name': 'Portugal', 'lang': 'Portuguese', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 10, 'combos': 25000},
    'SWE': {'name': 'Sweden', 'lang': 'Swedish', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 10, 'combos': 25000},
    'HUN': {'name': 'Hungary', 'lang': 'Hungarian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 10, 'combos': 25000},
    'AUT': {'name': 'Austria', 'lang': 'German', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 9, 'combos': 22000},
    'CHE': {'name': 'Switzerland', 'lang': 'German', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 9, 'combos': 22000},
    'BGR': {'name': 'Bulgaria', 'lang': 'Bulgarian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 7, 'combos': 18000},
    'SRB': {'name': 'Serbia', 'lang': 'Serbian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 7, 'combos': 18000},
    'DNK': {'name': 'Denmark', 'lang': 'Danish', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 6, 'combos': 15000},
    'FIN': {'name': 'Finland', 'lang': 'Finnish', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 6, 'combos': 15000},
    'NOR': {'name': 'Norway', 'lang': 'Norwegian', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 5, 'combos': 13000},
    'IRL': {'name': 'Ireland', 'lang': 'English', 'region': 'Europe', 'religions': ['Christianity'], 'weight': 5, 'combos': 13000},

    # Americas
    'USA': {'name': 'United States', 'lang': 'English', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 335, 'combos': 650000},
    'BRA': {'name': 'Brazil', 'lang': 'Portuguese', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 215, 'combos': 420000},
    'MEX': {'name': 'Mexico', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 130, 'combos': 270000},
    'COL': {'name': 'Colombia', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 52, 'combos': 110000},
    'ARG': {'name': 'Argentina', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 46, 'combos': 98000},
    'CAN': {'name': 'Canada', 'lang': 'English', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 39, 'combos': 85000},
    'PER': {'name': 'Peru', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 34, 'combos': 73000},
    'VEN': {'name': 'Venezuela', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 28, 'combos': 60000},
    'CHL': {'name': 'Chile', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 19, 'combos': 42000},
    'ECU': {'name': 'Ecuador', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 18, 'combos': 40000},
    'GTM': {'name': 'Guatemala', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 18, 'combos': 40000},
    'CUB': {'name': 'Cuba', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 11, 'combos': 26000},
    'HTI': {'name': 'Haiti', 'lang': 'French', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 12, 'combos': 28000},
    'DOM': {'name': 'Dominican Republic', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 11, 'combos': 26000},
    'BOL': {'name': 'Bolivia', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 12, 'combos': 28000},
    'HND': {'name': 'Honduras', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 10, 'combos': 24000},
    'PRY': {'name': 'Paraguay', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 7, 'combos': 18000},
    'NIC': {'name': 'Nicaragua', 'lang': 'Spanish', 'region': 'Americas', 'religions': ['Christianity'], 'weight': 7, 'combos': 18000},

    # Oceania
    'AUS': {'name': 'Australia', 'lang': 'English', 'region': 'Oceania', 'religions': ['Christianity'], 'weight': 26, 'combos': 57000},
    'PNG': {'name': 'Papua New Guinea', 'lang': 'English', 'region': 'Oceania', 'religions': ['Christianity'], 'weight': 9, 'combos': 22000},
    'NZL': {'name': 'New Zealand', 'lang': 'English', 'region': 'Oceania', 'religions': ['Christianity'], 'weight': 5, 'combos': 13000},
}

def load_base_names(db_path: str) -> Dict[str, List[str]]:
    """Load unique names from existing database"""
    print("📖 Loading base names...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get male first names
    cursor.execute("""
        SELECT DISTINCT name FROM names
        WHERE name_type='first' AND gender='M'
        ORDER BY name
    """)
    male_first = [row[0] for row in cursor.fetchall()]

    # Get female first names
    cursor.execute("""
        SELECT DISTINCT name FROM names
        WHERE name_type='first' AND gender='F'
        ORDER BY name
    """)
    female_first = [row[0] for row in cursor.fetchall()]

    # Get last names
    cursor.execute("""
        SELECT DISTINCT name FROM names
        WHERE name_type='last'
        ORDER BY name
    """)
    last_names = [row[0] for row in cursor.fetchall()]

    conn.close()

    print(f"✅ Male first names: {len(male_first):,}")
    print(f"✅ Female first names: {len(female_first):,}")
    print(f"✅ Last names: {len(last_names):,}")

    # Calculate theoretical maximum
    total_combos_male = len(male_first) * len(last_names) * len(COUNTRY_CONFIG)
    total_combos_female = len(female_first) * len(last_names) * len(COUNTRY_CONFIG)
    total_theoretical = (total_combos_male + total_combos_female) * 2  # x2 for first+last records

    print(f"\n📊 Theoretical maximum combinations:")
    print(f"   Male: {total_combos_male:,} combinations")
    print(f"   Female: {total_combos_female:,} combinations")
    print(f"   Total potential records: {total_theoretical:,}")

    return {
        'male_first': male_first,
        'female_first': female_first,
        'last': last_names
    }

def create_database(output_path: str):
    """Create optimized database"""
    print(f"\n🏗️  Creating database: {output_path}")

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

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON names(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON names(country_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_religion ON names(religion)")

    conn.commit()
    conn.close()

    print("✅ Database created")

def generate_country_data(country_code: str, config: dict, base_names: dict, target_combos: int) -> List[Tuple]:
    """Generate data for one country"""
    data = []
    male_first = base_names['male_first']
    female_first = base_names['female_first']
    last_names = base_names['last']

    religions = config['religions']
    lang = config['lang']
    region = config['region']

    generated = 0

    # Generate male combinations
    male_sample_size = min(len(male_first), target_combos // (2 * len(last_names)))
    female_sample_size = min(len(female_first), target_combos // (2 * len(last_names)))

    male_sample = random.sample(male_first, male_sample_size) if len(male_first) > male_sample_size else male_first
    female_sample = random.sample(female_first, female_sample_size) if len(female_first) > female_sample_size else female_first

    # Male combinations
    for first in male_sample:
        for last in last_names:
            if generated >= target_combos:
                break

            religion = random.choice(religions)

            # First name record
            data.append((first, 'first', country_code, region, lang, religion, 'M', 'synthetic_v3'))
            # Last name record
            data.append((last, 'last', country_code, region, lang, religion, None, 'synthetic_v3'))

            generated += 2

            if generated >= target_combos:
                break
        if generated >= target_combos:
            break

    # Female combinations
    for first in female_sample:
        for last in last_names:
            if generated >= target_combos * 2:  # Double for male+female
                break

            religion = random.choice(religions)

            data.append((first, 'first', country_code, region, lang, religion, 'F', 'synthetic_v3'))
            data.append((last, 'last', country_code, region, lang, religion, None, 'synthetic_v3'))

            generated += 2

            if generated >= target_combos * 2:
                break
        if generated >= target_combos * 2:
            break

    return data

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🚀 EthniData v3.0.0 - SMART MASSIVE Generation")
    print("="*80)

    # Load base names
    base_names = load_base_names(str(DB_PATH))

    # Create database
    create_database(str(NEW_DB_PATH))

    # Calculate target per country
    total_target_combos = sum(c['combos'] for c in COUNTRY_CONFIG.values())
    print(f"\n🎯 Target combinations: {total_target_combos:,}")
    print(f"   Expected unique records: ~{total_target_combos * 1.5:,.0f} (with first+last)")

    # Connect
    conn = sqlite3.connect(str(NEW_DB_PATH))

    start_time = time.time()
    total_inserted = 0

    # Process each country
    for idx, (country_code, config) in enumerate(COUNTRY_CONFIG.items(), 1):
        country_start = time.time()

        print(f"\n[{idx}/{len(COUNTRY_CONFIG)}] 🌍 Processing {config['name']} ({country_code})...")
        print(f"   Target combinations: {config['combos']:,}")

        # Generate data for this country
        country_data = generate_country_data(country_code, config, base_names, config['combos'])

        print(f"   Generated {len(country_data):,} records")
        print(f"   Inserting into database...")

        # Insert
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR IGNORE INTO names
            (name, name_type, country_code, region, language, religion, gender, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, country_data)
        conn.commit()

        total_inserted += len(country_data)
        country_time = time.time() - country_start

        # Get current count
        cursor.execute("SELECT COUNT(*) FROM names")
        current_count = cursor.fetchone()[0]

        print(f"✅ {config['name']} completed in {country_time:.1f}s")
        print(f"   Total unique records in DB: {current_count:,}")
        print(f"   Progress: {idx/len(COUNTRY_CONFIG)*100:.1f}%")

    # Final stats
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM names")
    final_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT name) FROM names")
    unique_names = cursor.fetchone()[0]

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
    print(f"   Countries: {len(COUNTRY_CONFIG)}")
    print(f"   Generation time: {total_time/60:.1f} minutes")
    print(f"\n📊 Religion distribution:")
    for religion, count in religion_stats:
        print(f"   {religion}: {count:,}")

    db_size_gb = NEW_DB_PATH.stat().st_size / (1024**3)
    print(f"\n💾 Database size: {db_size_gb:.2f} GB")
    print(f"📁 Location: {NEW_DB_PATH}")

    # Check if we hit target
    if final_count >= MIN_TARGET:
        print(f"\n🎯 SUCCESS! Target reached: {final_count:,} >= {MIN_TARGET:,}")
    else:
        print(f"\n⚠️  Target not reached: {final_count:,} < {MIN_TARGET:,}")
        print(f"   Need {MIN_TARGET - final_count:,} more records")

if __name__ == '__main__':
    main()
