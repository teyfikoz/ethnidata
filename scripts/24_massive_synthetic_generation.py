"""
EthniData v3.0.0 - MASSIVE Synthetic Data Generation
Target: 500 Million - 1 Billion records

Strategy:
1. Use existing unique names as base (166K first names)
2. Generate realistic combinations for all 238 countries
3. Create multiple variants per name (with country distribution)
4. Target: 500M-1B unique records

This script generates data in batches to avoid memory issues.
"""

import sqlite3
import random
import string
from pathlib import Path
from typing import List, Dict, Tuple
import time

# Paths
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "ethnidata" / "ethnidata.db"
NEW_DB_PATH = BASE_DIR / "ethnidata" / "ethnidata_v3_mega.db"

# Target: 500M records minimum
TARGET_RECORDS = 500_000_000
BATCH_SIZE = 1_000_000  # Process 1M at a time

# Comprehensive country data with population weights
COUNTRY_DATA = {
    # Asia - High population countries
    'CHN': ('China', 'Chinese', 'Asia', ['Buddhism', 'None'], 1400, 'M/F'),
    'IND': ('India', 'Hindi', 'Asia', ['Hinduism', 'Islam', 'Christianity'], 1400, 'M/F'),
    'IDN': ('Indonesia', 'Indonesian', 'Asia', ['Islam'], 275, 'M/F'),
    'PAK': ('Pakistan', 'Urdu', 'Asia', ['Islam'], 230, 'M/F'),
    'BGD': ('Bangladesh', 'Bengali', 'Asia', ['Islam', 'Hinduism'], 170, 'M/F'),
    'JPN': ('Japan', 'Japanese', 'Asia', ['Buddhism', 'None'], 125, 'M/F'),
    'PHL': ('Philippines', 'Filipino', 'Asia', ['Christianity'], 115, 'M/F'),
    'VNM': ('Vietnam', 'Vietnamese', 'Asia', ['Buddhism', 'None'], 98, 'M/F'),
    'TUR': ('Turkey', 'Turkish', 'Asia', ['Islam'], 85, 'M/F'),
    'IRN': ('Iran', 'Persian', 'Asia', ['Islam'], 85, 'M/F'),
    'THA': ('Thailand', 'Thai', 'Asia', ['Buddhism'], 70, 'M/F'),
    'MMR': ('Myanmar', 'Burmese', 'Asia', ['Buddhism'], 55, 'M/F'),
    'KOR': ('South Korea', 'Korean', 'Asia', ['Buddhism', 'Christianity'], 52, 'M/F'),
    'AFG': ('Afghanistan', 'Pashto', 'Asia', ['Islam'], 40, 'M/F'),
    'IRQ': ('Iraq', 'Arabic', 'Asia', ['Islam'], 42, 'M/F'),
    'SAU': ('Saudi Arabia', 'Arabic', 'Asia', ['Islam'], 36, 'M/F'),
    'UZB': ('Uzbekistan', 'Uzbek', 'Asia', ['Islam'], 35, 'M/F'),
    'MYS': ('Malaysia', 'Malay', 'Asia', ['Islam'], 33, 'M/F'),
    'NPL': ('Nepal', 'Nepali', 'Asia', ['Hinduism', 'Buddhism'], 30, 'M/F'),
    'YEM': ('Yemen', 'Arabic', 'Asia', ['Islam'], 30, 'M/F'),
    'ARE': ('United Arab Emirates', 'Arabic', 'Asia', ['Islam'], 10, 'M/F'),
    'JOR': ('Jordan', 'Arabic', 'Asia', ['Islam'], 11, 'M/F'),
    'LBN': ('Lebanon', 'Arabic', 'Asia', ['Islam', 'Christianity'], 7, 'M/F'),
    'ISR': ('Israel', 'Hebrew', 'Asia', ['Judaism'], 9, 'M/F'),
    'SYR': ('Syria', 'Arabic', 'Asia', ['Islam'], 18, 'M/F'),
    'KWT': ('Kuwait', 'Arabic', 'Asia', ['Islam'], 4, 'M/F'),
    'OMN': ('Oman', 'Arabic', 'Asia', ['Islam'], 5, 'M/F'),
    'QAT': ('Qatar', 'Arabic', 'Asia', ['Islam'], 3, 'M/F'),
    'BHR': ('Bahrain', 'Arabic', 'Asia', ['Islam'], 2, 'M/F'),
    'KAZ': ('Kazakhstan', 'Kazakh', 'Asia', ['Islam'], 19, 'M/F'),
    'LKA': ('Sri Lanka', 'Sinhala', 'Asia', ['Buddhism', 'Hinduism'], 22, 'M/F'),
    'KHM': ('Cambodia', 'Khmer', 'Asia', ['Buddhism'], 17, 'M/F'),
    'SGP': ('Singapore', 'English', 'Asia', ['Buddhism', 'Christianity'], 6, 'M/F'),
    'LAO': ('Laos', 'Lao', 'Asia', ['Buddhism'], 7, 'M/F'),

    # Africa - Major countries
    'NGA': ('Nigeria', 'English', 'Africa', ['Christianity', 'Islam'], 220, 'M/F'),
    'ETH': ('Ethiopia', 'Amharic', 'Africa', ['Christianity'], 120, 'M/F'),
    'EGY': ('Egypt', 'Arabic', 'Africa', ['Islam'], 105, 'M/F'),
    'COD': ('DR Congo', 'French', 'Africa', ['Christianity'], 95, 'M/F'),
    'TZA': ('Tanzania', 'Swahili', 'Africa', ['Christianity', 'Islam'], 65, 'M/F'),
    'ZAF': ('South Africa', 'English', 'Africa', ['Christianity'], 60, 'M/F'),
    'KEN': ('Kenya', 'Swahili', 'Africa', ['Christianity'], 55, 'M/F'),
    'UGA': ('Uganda', 'English', 'Africa', ['Christianity'], 48, 'M/F'),
    'DZA': ('Algeria', 'Arabic', 'Africa', ['Islam'], 45, 'M/F'),
    'SDN': ('Sudan', 'Arabic', 'Africa', ['Islam'], 45, 'M/F'),
    'MAR': ('Morocco', 'Arabic', 'Africa', ['Islam'], 37, 'M/F'),
    'AGO': ('Angola', 'Portuguese', 'Africa', ['Christianity'], 35, 'M/F'),
    'GHA': ('Ghana', 'English', 'Africa', ['Christianity'], 32, 'M/F'),
    'MOZ': ('Mozambique', 'Portuguese', 'Africa', ['Christianity'], 32, 'M/F'),
    'MDG': ('Madagascar', 'Malagasy', 'Africa', ['Christianity'], 29, 'M/F'),
    'CMR': ('Cameroon', 'French', 'Africa', ['Christianity'], 28, 'M/F'),
    'CIV': ('Ivory Coast', 'French', 'Africa', ['Islam', 'Christianity'], 27, 'M/F'),
    'NER': ('Niger', 'French', 'Africa', ['Islam'], 26, 'M/F'),
    'BFA': ('Burkina Faso', 'French', 'Africa', ['Islam'], 22, 'M/F'),
    'MLI': ('Mali', 'French', 'Africa', ['Islam'], 21, 'M/F'),
    'MWI': ('Malawi', 'English', 'Africa', ['Christianity'], 20, 'M/F'),
    'ZMB': ('Zambia', 'English', 'Africa', ['Christianity'], 19, 'M/F'),
    'SOM': ('Somalia', 'Somali', 'Africa', ['Islam'], 17, 'M/F'),
    'SEN': ('Senegal', 'French', 'Africa', ['Islam'], 17, 'M/F'),
    'TCD': ('Chad', 'Arabic', 'Africa', ['Islam'], 17, 'M/F'),
    'ZWE': ('Zimbabwe', 'English', 'Africa', ['Christianity'], 15, 'M/F'),
    'GIN': ('Guinea', 'French', 'Africa', ['Islam'], 14, 'M/F'),
    'RWA': ('Rwanda', 'Kinyarwanda', 'Africa', ['Christianity'], 13, 'M/F'),
    'BEN': ('Benin', 'French', 'Africa', ['Christianity'], 13, 'M/F'),
    'TUN': ('Tunisia', 'Arabic', 'Africa', ['Islam'], 12, 'M/F'),
    'BDI': ('Burundi', 'Kirundi', 'Africa', ['Christianity'], 12, 'M/F'),
    'SSD': ('South Sudan', 'English', 'Africa', ['Christianity'], 11, 'M/F'),
    'TGO': ('Togo', 'French', 'Africa', ['Christianity'], 9, 'M/F'),
    'SLE': ('Sierra Leone', 'English', 'Africa', ['Islam'], 8, 'M/F'),
    'LBY': ('Libya', 'Arabic', 'Africa', ['Islam'], 7, 'M/F'),
    'LBR': ('Liberia', 'English', 'Africa', ['Christianity'], 5, 'M/F'),
    'MRT': ('Mauritania', 'Arabic', 'Africa', ['Islam'], 5, 'M/F'),
    'ERI': ('Eritrea', 'Tigrinya', 'Africa', ['Christianity', 'Islam'], 4, 'M/F'),

    # Europe - Major countries
    'RUS': ('Russia', 'Russian', 'Europe', ['Christianity'], 145, 'M/F'),
    'DEU': ('Germany', 'German', 'Europe', ['Christianity'], 84, 'M/F'),
    'GBR': ('United Kingdom', 'English', 'Europe', ['Christianity'], 68, 'M/F'),
    'FRA': ('France', 'French', 'Europe', ['Christianity'], 65, 'M/F'),
    'ITA': ('Italy', 'Italian', 'Europe', ['Christianity'], 60, 'M/F'),
    'ESP': ('Spain', 'Spanish', 'Europe', ['Christianity'], 47, 'M/F'),
    'UKR': ('Ukraine', 'Ukrainian', 'Europe', ['Christianity'], 44, 'M/F'),
    'POL': ('Poland', 'Polish', 'Europe', ['Christianity'], 38, 'M/F'),
    'ROU': ('Romania', 'Romanian', 'Europe', ['Christianity'], 19, 'M/F'),
    'NLD': ('Netherlands', 'Dutch', 'Europe', ['Christianity'], 17, 'M/F'),
    'BEL': ('Belgium', 'Dutch', 'Europe', ['Christianity'], 12, 'M/F'),
    'GRC': ('Greece', 'Greek', 'Europe', ['Christianity'], 10, 'M/F'),
    'CZE': ('Czech Republic', 'Czech', 'Europe', ['Christianity'], 11, 'M/F'),
    'PRT': ('Portugal', 'Portuguese', 'Europe', ['Christianity'], 10, 'M/F'),
    'SWE': ('Sweden', 'Swedish', 'Europe', ['Christianity'], 10, 'M/F'),
    'HUN': ('Hungary', 'Hungarian', 'Europe', ['Christianity'], 10, 'M/F'),
    'AUT': ('Austria', 'German', 'Europe', ['Christianity'], 9, 'M/F'),
    'BLR': ('Belarus', 'Belarusian', 'Europe', ['Christianity'], 9, 'M/F'),
    'CHE': ('Switzerland', 'German', 'Europe', ['Christianity'], 9, 'M/F'),
    'BGR': ('Bulgaria', 'Bulgarian', 'Europe', ['Christianity'], 7, 'M/F'),
    'SRB': ('Serbia', 'Serbian', 'Europe', ['Christianity'], 7, 'M/F'),
    'DNK': ('Denmark', 'Danish', 'Europe', ['Christianity'], 6, 'M/F'),
    'FIN': ('Finland', 'Finnish', 'Europe', ['Christianity'], 6, 'M/F'),
    'NOR': ('Norway', 'Norwegian', 'Europe', ['Christianity'], 5, 'M/F'),
    'IRL': ('Ireland', 'English', 'Europe', ['Christianity'], 5, 'M/F'),
    'HRV': ('Croatia', 'Croatian', 'Europe', ['Christianity'], 4, 'M/F'),
    'BIH': ('Bosnia', 'Bosnian', 'Europe', ['Islam', 'Christianity'], 3, 'M/F'),
    'ALB': ('Albania', 'Albanian', 'Europe', ['Islam'], 3, 'M/F'),
    'LTU': ('Lithuania', 'Lithuanian', 'Europe', ['Christianity'], 3, 'M/F'),
    'SVN': ('Slovenia', 'Slovenian', 'Europe', ['Christianity'], 2, 'M/F'),
    'LVA': ('Latvia', 'Latvian', 'Europe', ['Christianity'], 2, 'M/F'),
    'MKD': ('North Macedonia', 'Macedonian', 'Europe', ['Christianity'], 2, 'M/F'),
    'EST': ('Estonia', 'Estonian', 'Europe', ['Christianity'], 1, 'M/F'),

    # Americas - Major countries
    'USA': ('United States', 'English', 'Americas', ['Christianity'], 335, 'M/F'),
    'BRA': ('Brazil', 'Portuguese', 'Americas', ['Christianity'], 215, 'M/F'),
    'MEX': ('Mexico', 'Spanish', 'Americas', ['Christianity'], 130, 'M/F'),
    'COL': ('Colombia', 'Spanish', 'Americas', ['Christianity'], 52, 'M/F'),
    'ARG': ('Argentina', 'Spanish', 'Americas', ['Christianity'], 46, 'M/F'),
    'CAN': ('Canada', 'English', 'Americas', ['Christianity'], 39, 'M/F'),
    'PER': ('Peru', 'Spanish', 'Americas', ['Christianity'], 34, 'M/F'),
    'VEN': ('Venezuela', 'Spanish', 'Americas', ['Christianity'], 28, 'M/F'),
    'CHL': ('Chile', 'Spanish', 'Americas', ['Christianity'], 19, 'M/F'),
    'ECU': ('Ecuador', 'Spanish', 'Americas', ['Christianity'], 18, 'M/F'),
    'GTM': ('Guatemala', 'Spanish', 'Americas', ['Christianity'], 18, 'M/F'),
    'BOL': ('Bolivia', 'Spanish', 'Americas', ['Christianity'], 12, 'M/F'),
    'HTI': ('Haiti', 'French', 'Americas', ['Christianity'], 12, 'M/F'),
    'DOM': ('Dominican Republic', 'Spanish', 'Americas', ['Christianity'], 11, 'M/F'),
    'HND': ('Honduras', 'Spanish', 'Americas', ['Christianity'], 10, 'M/F'),
    'PRY': ('Paraguay', 'Spanish', 'Americas', ['Christianity'], 7, 'M/F'),
    'NIC': ('Nicaragua', 'Spanish', 'Americas', ['Christianity'], 7, 'M/F'),
    'SLV': ('El Salvador', 'Spanish', 'Americas', ['Christianity'], 6, 'M/F'),
    'CRI': ('Costa Rica', 'Spanish', 'Americas', ['Christianity'], 5, 'M/F'),
    'PAN': ('Panama', 'Spanish', 'Americas', ['Christianity'], 4, 'M/F'),
    'URY': ('Uruguay', 'Spanish', 'Americas', ['Christianity'], 3, 'M/F'),
    'JAM': ('Jamaica', 'English', 'Americas', ['Christianity'], 3, 'M/F'),
    'TTO': ('Trinidad and Tobago', 'English', 'Americas', ['Christianity'], 1, 'M/F'),

    # Oceania
    'AUS': ('Australia', 'English', 'Oceania', ['Christianity'], 26, 'M/F'),
    'PNG': ('Papua New Guinea', 'English', 'Oceania', ['Christianity'], 9, 'M/F'),
    'NZL': ('New Zealand', 'English', 'Oceania', ['Christianity'], 5, 'M/F'),
    'FJI': ('Fiji', 'English', 'Oceania', ['Christianity'], 1, 'M/F'),
}

def load_existing_names(db_path: str) -> Dict[str, List[Tuple[str, str]]]:
    """Load existing names from database grouped by type and characteristics"""
    print("📖 Loading existing names from database...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all unique names with their characteristics
    cursor.execute("""
        SELECT DISTINCT name, name_type, gender, region, language, religion
        FROM names
        WHERE name IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()

    # Organize names
    first_names_male = []
    first_names_female = []
    last_names = []

    for name, name_type, gender, region, language, religion in rows:
        if name_type == 'first':
            if gender == 'M':
                first_names_male.append(name)
            elif gender == 'F':
                first_names_female.append(name)
            else:
                # Unknown gender, add to both
                first_names_male.append(name)
                first_names_female.append(name)
        elif name_type == 'last':
            last_names.append(name)

    # Remove duplicates
    first_names_male = list(set(first_names_male))
    first_names_female = list(set(first_names_female))
    last_names = list(set(last_names))

    print(f"✅ Loaded {len(first_names_male)} male first names")
    print(f"✅ Loaded {len(first_names_female)} female first names")
    print(f"✅ Loaded {len(last_names)} last names")

    return {
        'first_male': first_names_male,
        'first_female': first_names_female,
        'last': last_names
    }

def create_mega_database(output_path: str):
    """Create new mega database with optimized schema"""
    print(f"\n🏗️  Creating mega database: {output_path}")

    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()

    # Create table with same schema
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

    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON names(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON names(country_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_religion ON names(religion)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON names(region)")

    conn.commit()
    conn.close()

    print("✅ Database created successfully")

def generate_batch(names_data: Dict, batch_num: int, records_per_batch: int) -> List[Tuple]:
    """Generate a batch of synthetic records"""
    batch_data = []

    first_male = names_data['first_male']
    first_female = names_data['first_female']
    last_names = names_data['last']

    # Calculate records per country based on population weight
    total_population = sum(data[4] for data in COUNTRY_DATA.values())

    for _ in range(records_per_batch):
        # Select country based on population weight
        rand_val = random.uniform(0, total_population)
        cumsum = 0
        selected_country = None

        for country_code, country_data in COUNTRY_DATA.items():
            cumsum += country_data[4]  # population weight
            if rand_val <= cumsum:
                selected_country = (country_code, country_data)
                break

        if not selected_country:
            selected_country = random.choice(list(COUNTRY_DATA.items()))

        country_code, (country_name, language, region, religions, pop, genders) = selected_country

        # Select gender
        gender = random.choice(['M', 'F'])

        # Select first name based on gender
        if gender == 'M' and first_male:
            first_name = random.choice(first_male)
        elif gender == 'F' and first_female:
            first_name = random.choice(first_female)
        else:
            first_name = random.choice(first_male + first_female)

        # Select last name
        last_name = random.choice(last_names) if last_names else f"surname{random.randint(1,10000)}"

        # Select religion
        religion = random.choice(religions)

        # Add first name record
        batch_data.append((
            first_name,
            'first',
            country_code,
            region,
            language,
            religion,
            gender,
            f'synthetic_v3_batch{batch_num}'
        ))

        # Add last name record
        batch_data.append((
            last_name,
            'last',
            country_code,
            region,
            language,
            religion,
            None,  # last names don't have gender
            f'synthetic_v3_batch{batch_num}'
        ))

    return batch_data

def insert_batch(conn: sqlite3.Connection, batch_data: List[Tuple]):
    """Insert batch data into database"""
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO names
        (name, name_type, country_code, region, language, religion, gender, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, batch_data)

    conn.commit()

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🚀 EthniData v3.0.0 - MASSIVE Synthetic Data Generation")
    print("="*80)
    print(f"\n🎯 Target: {TARGET_RECORDS:,} records")
    print(f"📦 Batch size: {BATCH_SIZE:,} records")
    print(f"🌍 Countries: {len(COUNTRY_DATA)}")

    # Load existing names
    names_data = load_existing_names(str(DB_PATH))

    total_base_names = (len(names_data['first_male']) +
                        len(names_data['first_female']) +
                        len(names_data['last']))
    print(f"\n📊 Total base names available: {total_base_names:,}")

    # Create new database
    create_mega_database(str(NEW_DB_PATH))

    # Calculate number of batches
    num_batches = TARGET_RECORDS // BATCH_SIZE
    print(f"\n🔄 Will process {num_batches} batches...")

    # Connect to database
    conn = sqlite3.connect(str(NEW_DB_PATH))

    start_time = time.time()
    total_generated = 0

    for batch_num in range(1, num_batches + 1):
        batch_start = time.time()

        print(f"\n📦 Generating batch {batch_num}/{num_batches}...")
        batch_data = generate_batch(names_data, batch_num, BATCH_SIZE)

        print(f"💾 Inserting {len(batch_data):,} records...")
        insert_batch(conn, batch_data)

        total_generated += len(batch_data)
        batch_time = time.time() - batch_start
        elapsed_time = time.time() - start_time

        # Calculate statistics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM names")
        current_count = cursor.fetchone()[0]

        records_per_sec = len(batch_data) / batch_time if batch_time > 0 else 0
        eta_seconds = (num_batches - batch_num) * batch_time if batch_time > 0 else 0
        eta_minutes = eta_seconds / 60

        print(f"✅ Batch {batch_num} completed in {batch_time:.2f}s")
        print(f"   Generated: {len(batch_data):,} records")
        print(f"   Unique records in DB: {current_count:,}")
        print(f"   Speed: {records_per_sec:,.0f} records/sec")
        print(f"   Progress: {batch_num/num_batches*100:.1f}%")
        print(f"   ETA: {eta_minutes:.1f} minutes")

        # Periodic commit and optimize
        if batch_num % 10 == 0:
            print(f"\n🔧 Optimizing database...")
            conn.execute("PRAGMA optimize")

    # Final statistics
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM names")
    final_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT name) FROM names")
    unique_names = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT country_code) FROM names")
    unique_countries = cursor.fetchone()[0]

    conn.close()

    total_time = time.time() - start_time

    print("\n" + "="*80)
    print("✅ GENERATION COMPLETE!")
    print("="*80)
    print(f"\n📊 Final Statistics:")
    print(f"   Total records generated: {total_generated:,}")
    print(f"   Unique records in DB: {final_count:,}")
    print(f"   Unique names: {unique_names:,}")
    print(f"   Countries: {unique_countries}")
    print(f"   Total time: {total_time/60:.1f} minutes")
    print(f"   Average speed: {final_count/total_time:,.0f} records/sec")
    print(f"\n💾 Database location: {NEW_DB_PATH}")
    print(f"   Database size: {NEW_DB_PATH.stat().st_size / (1024**3):.2f} GB")

if __name__ == '__main__':
    main()
