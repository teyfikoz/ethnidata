#!/usr/bin/env python3
"""
SQLite veritabanı oluştur
"""

import sqlite3
import pandas as pd
from pathlib import Path
from tqdm import tqdm

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
DB_PATH = Path(__file__).parent.parent / "ethnidata" / "ethnidata.db"

def create_database():
    """SQLite veritabanı oluştur"""

    print("🗄️  SQLite veritabanı oluşturuluyor...")

    # Veritabanı dosyası
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabloları oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS first_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country_code TEXT NOT NULL,
            ethnicity TEXT,
            source TEXT,
            frequency INTEGER DEFAULT 1,
            UNIQUE(name, country_code)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS last_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country_code TEXT NOT NULL,
            ethnicity TEXT,
            source TEXT,
            frequency INTEGER DEFAULT 1,
            UNIQUE(name, country_code)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            country_code TEXT PRIMARY KEY,
            country_name TEXT,
            region TEXT,
            population INTEGER
        )
    """)

    # İndeksler
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_first_name ON first_names(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_last_name ON last_names(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_first_country ON first_names(country_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_last_country ON last_names(country_code)")

    conn.commit()

    print("  ✓ Tablolar ve indeksler oluşturuldu")

    # Birleştirilmiş veriyi yükle
    merged_file = PROCESSED_DIR / "merged_names.csv"

    if not merged_file.exists():
        print(f"  ❌ Veri dosyası bulunamadı: {merged_file}")
        print("  💡 Önce 5_merge_all_data.py çalıştırın")
        return

    print(f"\n📥 Veri yükleniyor: {merged_file}")
    df = pd.read_csv(merged_file)

    # First names
    print("\n🔤 First names ekleniyor...")
    first_names_df = df[df['first_name_norm'].notna()][['first_name_norm', 'country_code', 'ethnicity', 'source']]

    # Frekans hesapla (aynı isim-ülke kaç kez geçiyor)
    first_names_agg = first_names_df.groupby(['first_name_norm', 'country_code']).agg({
        'ethnicity': 'first',
        'source': 'first',
        'first_name_norm': 'count'
    }).rename(columns={'first_name_norm': 'frequency'}).reset_index()

    # Veritabanına ekle
    for _, row in tqdm(first_names_agg.iterrows(), total=len(first_names_agg), desc="First names"):
        cursor.execute("""
            INSERT OR REPLACE INTO first_names (name, country_code, ethnicity, source, frequency)
            VALUES (?, ?, ?, ?, ?)
        """, (row['first_name_norm'], row['country_code'], row['ethnicity'], row['source'], row['frequency']))

    # Last names
    print("\n🔤 Last names ekleniyor...")
    last_names_df = df[df['last_name_norm'].notna()][['last_name_norm', 'country_code', 'ethnicity', 'source']]

    # Frekans hesapla
    last_names_agg = last_names_df.groupby(['last_name_norm', 'country_code']).agg({
        'ethnicity': 'first',
        'source': 'first',
        'last_name_norm': 'count'
    }).rename(columns={'last_name_norm': 'frequency'}).reset_index()

    # Veritabanına ekle
    for _, row in tqdm(last_names_agg.iterrows(), total=len(last_names_agg), desc="Last names"):
        cursor.execute("""
            INSERT OR REPLACE INTO last_names (name, country_code, ethnicity, source, frequency)
            VALUES (?, ?, ?, ?, ?)
        """, (row['last_name_norm'], row['country_code'], row['ethnicity'], row['source'], row['frequency']))

    # Countries tablosu (pycountry kullanarak)
    print("\n🌍 Ülkeler ekleniyor...")
    import pycountry

    for country in pycountry.countries:
        cursor.execute("""
            INSERT OR REPLACE INTO countries (country_code, country_name)
            VALUES (?, ?)
        """, (country.alpha_3, country.name))

    conn.commit()

    # İstatistikler
    print("\n📊 Veritabanı istatistikleri:")

    cursor.execute("SELECT COUNT(*) FROM first_names")
    print(f"  First names: {cursor.fetchone()[0]:,}")

    cursor.execute("SELECT COUNT(*) FROM last_names")
    print(f"  Last names: {cursor.fetchone()[0]:,}")

    cursor.execute("SELECT COUNT(*) FROM countries")
    print(f"  Countries: {cursor.fetchone()[0]:,}")

    cursor.execute("SELECT COUNT(DISTINCT country_code) FROM first_names")
    print(f"  Unique countries (first names): {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(DISTINCT country_code) FROM last_names")
    print(f"  Unique countries (last names): {cursor.fetchone()[0]}")

    # En yaygın isimler
    print("\n📊 En yaygın first names (top 10):")
    cursor.execute("""
        SELECT name, country_code, frequency
        FROM first_names
        ORDER BY frequency DESC
        LIMIT 10
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]} ({row[1]}): {row[2]:,}")

    conn.close()

    print(f"\n✅ Veritabanı oluşturuldu: {DB_PATH}")
    print(f"📦 Dosya boyutu: {DB_PATH.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    create_database()
