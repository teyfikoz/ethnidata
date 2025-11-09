"""
EthniData v3.0.0 - PRACTICAL Massive Generation
Target: 50-100 Million records (practical and usable)

Realistic Strategy:
- Current: 415K records
- Target: 50M-100M records (100x-200x growth)
- This is massive enough for any real-world use case
- Database will remain usable (< 50GB)

Approach:
1. Expand existing names with realistic variations
2. Smart distribution across 238 countries
3. Each country gets proportional records based on population
4. Optimized batch processing
"""

import sqlite3
import random
from pathlib import Path
from typing import List, Dict, Tuple
import time

# Paths
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "ethnidata" / "ethnidata.db"
NEW_DB_PATH = BASE_DIR / "ethnidata" / "ethnidata_v3.db"

# Realistic target: 50-100M
TARGET_RECORDS = 20_000_000
BATCH_SIZE = 1_000_000

# Name variations for realistic expansion
VARIATIONS = {
    'male_suffix': ['', 'son', 'sen', 'ovich', 'ev', 'ov', 'ski', 'yan'],
    'female_suffix': ['', 'a', 'ova', 'eva', 'dottir', 'yan'],
    'last_prefix': ['', 'van', 'de', 'el', 'al', 'bin', 'von', 'mac'],
}

# Population-weighted country allocation (simplified)
COUNTRY_WEIGHTS = {
    # Top countries by allocation
    'CHN': 8000000,   # China - 8M
    'IND': 8000000,   # India - 8M
    'USA': 6000000,   # USA - 6M
    'IDN': 4000000,   # Indonesia - 4M
    'PAK': 3000000,   # Pakistan - 3M
    'BRA': 3000000,   # Brazil - 3M
    'NGA': 3000000,   # Nigeria - 3M
    'BGD': 2500000,   # Bangladesh - 2.5M
    'RUS': 2000000,   # Russia - 2M
    'MEX': 2000000,   # Mexico - 2M
    'JPN': 1500000,   # Japan - 1.5M
    'ETH': 1500000,   # Ethiopia - 1.5M
    'PHL': 1500000,   # Philippines - 1.5M
    'EGY': 1200000,   # Egypt - 1.2M
    'VNM': 1200000,   # Vietnam - 1.2M
    'COD': 1000000,   # DR Congo - 1M
    'TUR': 1000000,   # Turkey - 1M
    'IRN': 1000000,   # Iran - 1M
    'DEU': 1000000,   # Germany - 1M
    'THA': 900000,    # Thailand - 900K
    'GBR': 900000,    # UK - 900K
    'FRA': 900000,    # France - 900K
    'ITA': 800000,    # Italy - 800K
    'TZA': 800000,    # Tanzania - 800K
    'ZAF': 800000,    # South Africa - 800K
    'MMR': 700000,    # Myanmar - 700K
    'KEN': 700000,    # Kenya - 700K
    'KOR': 700000,    # South Korea - 700K
    'COL': 600000,    # Colombia - 600K
    'ESP': 600000,    # Spain - 600K
    # Medium countries - 300-600K each
    'ARG': 500000, 'DZA': 500000, 'SDN': 500000, 'UKR': 500000, 'UGA': 500000,
    'IRQ': 500000, 'AFG': 500000, 'POL': 500000, 'CAN': 500000, 'MAR': 500000,
    'SAU': 400000, 'UZB': 400000, 'PER': 400000, 'AGO': 400000, 'GHA': 400000,
    'MOZ': 400000, 'YEM': 400000, 'NPL': 400000, 'VEN': 400000, 'MYS': 400000,
    # Smaller countries - 100-300K each (rest of the 238 countries)
    'AUS': 300000, 'ROU': 300000, 'LKA': 300000, 'CHL': 300000, 'KAZ': 300000,
    'CMR': 300000, 'NLD': 300000, 'CIV': 300000, 'ECU': 300000, 'GTM': 300000,
    'MLI': 250000, 'BFA': 250000, 'ZMB': 250000, 'SEN': 250000, 'SOM': 250000,
    'KHM': 250000, 'ZWE': 250000, 'GIN': 250000, 'RWA': 250000, 'BEN': 250000,
    'TUN': 250000, 'BDI': 250000, 'BOL': 250000, 'HTI': 250000, 'DOM': 250000,
    'CZE': 200000, 'GRC': 200000, 'PRT': 200000, 'BEL': 200000, 'HUN': 200000,
    'SWE': 200000, 'AZE': 200000, 'JOR': 200000, 'ARE': 200000, 'HND': 200000,
    'TCD': 200000, 'SSD': 200000, 'TGO': 200000, 'SLE': 200000, 'LBY': 200000,
    'LBR': 200000, 'MRT': 200000, 'PAN': 150000, 'URY': 150000, 'MNG': 150000,
    'ARM': 150000, 'JAM': 150000, 'QAT': 150000, 'ALB': 150000, 'NIC': 150000,
    'OMN': 150000, 'PRY': 150000, 'KWT': 150000, 'SLV': 150000, 'CRI': 150000,
    'LBN': 150000, 'SYR': 150000, 'ISR': 150000, 'DNK': 150000, 'FIN': 150000,
    'NOR': 150000, 'BGR': 150000, 'SRB': 150000, 'CHE': 150000, 'AUT': 150000,
    'PNG': 150000, 'NZL': 150000, 'IRL': 150000, 'HRV': 150000, 'BIH': 150000,
    'LTU': 120000, 'SVN': 120000, 'LVA': 120000, 'MKD': 120000, 'BWA': 120000,
    'GAB': 120000, 'GMB': 120000, 'GIN': 120000, 'MUS': 120000, 'NAM': 120000,
    'BLR': 150000, 'GEO': 120000, 'SWZ': 100000, 'EST': 100000, 'TTO': 100000,
    'BHR': 100000, 'SGP': 150000, 'FJI': 100000, 'CYP': 100000, 'DJI': 100000,
    'GNQ': 100000, 'BTN': 100000, 'SLB': 100000, 'MAC': 100000, 'LUX': 100000,
    'SUR': 100000, 'CPV': 100000, 'MLT': 100000, 'BRN': 100000, 'BLZ': 100000,
    'MDV': 100000, 'ISL': 100000, 'VUT': 100000, 'BRB': 100000, 'SYC': 100000,
    'TON': 80000, 'GRD': 80000, 'VCT': 80000, 'LCA': 80000, 'ATG': 80000,
    'PLW': 80000, 'AND': 80000, 'DMA': 80000, 'KNA': 80000, 'LIE': 80000,
    'MCO': 80000, 'SMR': 80000, 'TUV': 80000, 'NRU': 80000, 'VAT': 50000,
}

def load_and_expand_names(db_path: str) -> Dict:
    """Load base names and create expanded versions"""
    print("📖 Loading and expanding names...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load base
    cursor.execute("SELECT DISTINCT name FROM names WHERE name_type='first' AND gender='M' LIMIT 5000")
    male_base = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT name FROM names WHERE name_type='first' AND gender='F' LIMIT 5000")
    female_base = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT name FROM names WHERE name_type='last' LIMIT 20000")
    last_base = [row[0] for row in cursor.fetchall()]

    conn.close()

    # Expand with variations
    male_expanded = set(male_base)
    for name in male_base:
        for suffix in VARIATIONS['male_suffix']:
            male_expanded.add(name + suffix)

    female_expanded = set(female_base)
    for name in female_base:
        for suffix in VARIATIONS['female_suffix']:
            female_expanded.add(name + suffix)

    last_expanded = set(last_base)
    for name in last_base[:5000]:  # Limit for performance
        for prefix in VARIATIONS['last_prefix']:
            if prefix and len(name) > 3:
                last_expanded.add(f"{prefix}{name}")

    result = {
        'male': list(male_expanded),
        'female': list(female_expanded),
        'last': list(last_expanded)
    }

    print(f"✅ Male names: {len(result['male']):,}")
    print(f"✅ Female names: {len(result['female']):,}")
    print(f"✅ Last names: {len(result['last']):,}")

    return result

def get_country_info(country_code: str) -> Tuple:
    """Get country metadata"""
    # Comprehensive mapping (simplified)
    info_map = {
        'CHN': ('China', 'Chinese', 'Asia', ['Buddhism', 'None']),
        'IND': ('India', 'Hindi', 'Asia', ['Hinduism', 'Islam', 'Christianity']),
        'USA': ('United States', 'English', 'Americas', ['Christianity']),
        'IDN': ('Indonesia', 'Indonesian', 'Asia', ['Islam']),
        'PAK': ('Pakistan', 'Urdu', 'Asia', ['Islam']),
        'BRA': ('Brazil', 'Portuguese', 'Americas', ['Christianity']),
        'NGA': ('Nigeria', 'English', 'Africa', ['Christianity', 'Islam']),
        'BGD': ('Bangladesh', 'Bengali', 'Asia', ['Islam', 'Hinduism']),
        'RUS': ('Russia', 'Russian', 'Europe', ['Christianity']),
        'MEX': ('Mexico', 'Spanish', 'Americas', ['Christianity']),
        'JPN': ('Japan', 'Japanese', 'Asia', ['Buddhism', 'None']),
        'ETH': ('Ethiopia', 'Amharic', 'Africa', ['Christianity']),
        'PHL': ('Philippines', 'Filipino', 'Asia', ['Christianity']),
        'EGY': ('Egypt', 'Arabic', 'Africa', ['Islam']),
        'VNM': ('Vietnam', 'Vietnamese', 'Asia', ['Buddhism']),
        'COD': ('DR Congo', 'French', 'Africa', ['Christianity']),
        'TUR': ('Turkey', 'Turkish', 'Asia', ['Islam']),
        'IRN': ('Iran', 'Persian', 'Asia', ['Islam']),
        'DEU': ('Germany', 'German', 'Europe', ['Christianity']),
        'THA': ('Thailand', 'Thai', 'Asia', ['Buddhism']),
        'GBR': ('United Kingdom', 'English', 'Europe', ['Christianity']),
        'FRA': ('France', 'French', 'Europe', ['Christianity']),
        'ITA': ('Italy', 'Italian', 'Europe', ['Christianity']),
        # Default for unmapped countries
    }

    if country_code in info_map:
        return info_map[country_code]
    else:
        # Default
        return (country_code, 'English', 'Europe', ['Christianity'])

def create_database(path: str):
    """Create optimized database"""
    print(f"\n🏗️  Creating database: {path}")

    conn = sqlite3.connect(path)
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

    conn.commit()
    conn.close()
    print("✅ Database created")

def generate_batch_data(names: Dict, country_code: str, info: Tuple, count: int) -> List[Tuple]:
    """Generate batch of records"""
    country_name, lang, region, religions = info

    data = []
    for _ in range(count // 2):  # Half male, half female
        # Male record
        first_m = random.choice(names['male'])
        last = random.choice(names['last'])
        religion = random.choice(religions)

        data.append((first_m, 'first', country_code, region, lang, religion, 'M', 'synthetic_v3'))
        data.append((last, 'last', country_code, region, lang, religion, None, 'synthetic_v3'))

        # Female record
        first_f = random.choice(names['female'])
        last = random.choice(names['last'])
        religion = random.choice(religions)

        data.append((first_f, 'first', country_code, region, lang, religion, 'F', 'synthetic_v3'))
        data.append((last, 'last', country_code, region, lang, religion, None, 'synthetic_v3'))

    return data

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🚀 EthniData v3.0.0 - Practical Massive Generation")
    print("="*80)
    print(f"\n🎯 Target: {TARGET_RECORDS:,} records")
    print(f"🌍 Countries: {len(COUNTRY_WEIGHTS)}")

    total_planned = sum(COUNTRY_WEIGHTS.values())
    print(f"📊 Planned total: {total_planned:,} records")

    # Load names
    names = load_and_expand_names(str(DB_PATH))

    # Create database
    create_database(str(NEW_DB_PATH))

    # Connect
    conn = sqlite3.connect(str(NEW_DB_PATH))

    start_time = time.time()

    # Process each country
    for idx, (country_code, target_count) in enumerate(COUNTRY_WEIGHTS.items(), 1):
        country_start = time.time()

        info = get_country_info(country_code)
        country_name = info[0]

        print(f"\n[{idx}/{len(COUNTRY_WEIGHTS)}] 🌍 {country_name} ({country_code})")
        print(f"   Target: {target_count:,} records")

        generated = 0
        while generated < target_count:
            batch_size = min(BATCH_SIZE, target_count - generated)

            # Generate and insert
            batch_data = generate_batch_data(names, country_code, info, batch_size)

            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR IGNORE INTO names
                (name, name_type, country_code, region, language, religion, gender, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, batch_data)
            conn.commit()

            generated += len(batch_data)

        # Stats
        cursor.execute("SELECT COUNT(*) FROM names")
        current_total = cursor.fetchone()[0]

        country_time = time.time() - country_start
        elapsed = time.time() - start_time

        print(f"✅ Completed in {country_time:.1f}s")
        print(f"   Total in DB: {current_total:,} unique records")
        print(f"   Overall progress: {current_total/total_planned*100:.1f}%")
        print(f"   Elapsed: {elapsed/60:.1f} min")

        # Optimize periodically
        if idx % 20 == 0:
            print(f"\n🔧 Optimizing database...")
            conn.execute("PRAGMA optimize")

    # Final stats
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM names")
    final_total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT name) FROM names")
    unique_names = cursor.fetchone()[0]

    cursor.execute("SELECT region, COUNT(*) FROM names GROUP BY region")
    regions = cursor.fetchall()

    cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL GROUP BY religion ORDER BY COUNT(*) DESC")
    religions = cursor.fetchall()

    conn.close()

    total_time = time.time() - start_time

    print("\n" + "="*80)
    print("✅ GENERATION COMPLETE!")
    print("="*80)
    print(f"\n📊 Final Statistics:")
    print(f"   Total records: {final_total:,}")
    print(f"   Unique names: {unique_names:,}")
    print(f"   Countries: {len(COUNTRY_WEIGHTS)}")
    print(f"   Time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
    print(f"   Speed: {final_total/total_time:,.0f} records/sec")

    print(f"\n🌍 Regional Distribution:")
    for region, count in regions:
        pct = count / final_total * 100
        print(f"   {region}: {count:,} ({pct:.1f}%)")

    print(f"\n🕌 Religion Distribution:")
    for religion, count in religions:
        pct = count / final_total * 100
        print(f"   {religion}: {count:,} ({pct:.1f}%)")

    db_size = NEW_DB_PATH.stat().st_size / (1024**3)
    print(f"\n💾 Database Size: {db_size:.2f} GB")
    print(f"📁 Location: {NEW_DB_PATH}")

    if final_total >= TARGET_RECORDS:
        print(f"\n🎯 ✅ SUCCESS! Target reached!")
        print(f"   Growth: {final_total/415734:.1f}x from v2.0.0")
    else:
        print(f"\n📊 Generated {final_total:,} records")
        print(f"   Growth: {final_total/415734:.1f}x from v2.0.0")

if __name__ == '__main__':
    main()
