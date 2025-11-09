"""
Script 21: Create Mega Database with All Data
Mevcut veri + Sentetik veri = 2M+ kayıt

Kaynaklar:
1. Mevcut ethnidata.db (220K)
2. Synthetic religious names (1.1M)
3. Synthetic Christian/African names (600K)
TOPLAM: ~1.9M kayıt
"""

import sqlite3
import json
from pathlib import Path
from collections import Counter

# Paths
DB_PATH = Path("ethnidata/ethnidata.db")
SYNTHETIC_DIR = Path("data/synthetic")
NEW_DB_PATH = Path("ethnidata/ethnidata_mega.db")

def create_database():
    """Yeni mega veritabanı oluştur"""

    print("=" * 80)
    print("MEGA DATABASE OLUŞTURULUYOR")
    print("=" * 80)

    # Yeni veritabanı oluştur
    if NEW_DB_PATH.exists():
        NEW_DB_PATH.unlink()
        print(f"✓ Eski {NEW_DB_PATH.name} silindi")

    conn = sqlite3.connect(NEW_DB_PATH)
    cursor = conn.cursor()

    # Tablo oluştur
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

    # Index'ler
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON names(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON names(country_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON names(region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_religion ON names(religion)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_gender ON names(gender)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name_type ON names(name_type)")

    conn.commit()
    print("✓ Tablo ve index'ler oluşturuldu")

    return conn, cursor

def import_existing_data(cursor):
    """Mevcut veritabanından veriyi al"""

    print("\n1. Mevcut veritabanı aktarılıyor...")

    old_conn = sqlite3.connect(DB_PATH)
    old_cursor = old_conn.cursor()

    old_cursor.execute("SELECT * FROM names")
    rows = old_cursor.fetchall()

    count = 0
    for row in rows:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO names
                (name, name_type, country_code, region, language, religion, gender, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, row)
            count += 1
        except Exception as e:
            pass

    old_conn.close()

    print(f"✓ {count:,} kayıt aktarıldı (mevcut DB)")
    return count

def import_synthetic_data(cursor, filename):
    """Sentetik veriyi içe aktar"""

    filepath = SYNTHETIC_DIR / filename
    print(f"\n{filename} aktarılıyor...")

    if not filepath.exists():
        print(f"✗ Dosya bulunamadı: {filepath}")
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for record in data:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO names
                (name, name_type, country_code, region, language, religion, gender, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record['name'],
                record['name_type'],
                record['country_code'],
                record['region'],
                record['language'],
                record.get('religion'),
                record.get('gender'),
                record.get('source', 'synthetic')
            ))
            count += 1
        except Exception as e:
            pass

    print(f"✓ {count:,} kayıt eklendi")
    return count

def get_statistics(cursor):
    """Veritabanı istatistiklerini al"""

    print("\n" + "=" * 80)
    print("VERİTABANI İSTATİSTİKLERİ")
    print("=" * 80)

    # Toplam kayıt
    cursor.execute("SELECT COUNT(*) FROM names")
    total = cursor.fetchone()[0]
    print(f"\nToplam Kayıt: {total:,}")

    # Name type
    cursor.execute("SELECT name_type, COUNT(*) FROM names GROUP BY name_type")
    print("\nİsim Türü:")
    for row in cursor.fetchall():
        print(f"  {row[0]:10s}: {row[1]:>10,}")

    # Ülkeler
    cursor.execute("SELECT COUNT(DISTINCT country_code) FROM names")
    countries = cursor.fetchone()[0]
    print(f"\nÜlke Sayısı: {countries}")

    # Bölgeler
    cursor.execute("SELECT region, COUNT(*) FROM names WHERE region IS NOT NULL GROUP BY region ORDER BY COUNT(*) DESC")
    print("\nBölge Dağılımı:")
    for row in cursor.fetchall():
        pct = (row[1] / total) * 100
        print(f"  {row[0]:15s}: {row[1]:>10,} ({pct:>5.1f}%)")

    # Dinler
    cursor.execute("SELECT religion, COUNT(*) FROM names WHERE religion IS NOT NULL GROUP BY religion ORDER BY COUNT(*) DESC")
    print("\nDin Dağılımı:")
    for row in cursor.fetchall():
        pct = (row[1] / total) * 100
        print(f"  {row[0]:15s}: {row[1]:>10,} ({pct:>5.1f}%)")

    # Diller
    cursor.execute("SELECT COUNT(DISTINCT language) FROM names WHERE language IS NOT NULL")
    languages = cursor.fetchone()[0]
    print(f"\nDil Sayısı: {languages}")

    # Gender
    cursor.execute("SELECT gender, COUNT(*) FROM names WHERE gender IS NOT NULL GROUP BY gender")
    print("\nCinsiyet Dağılımı:")
    for row in cursor.fetchall():
        print(f"  {row[0]:10s}: {row[1]:>10,}")

    # Kaynaklar
    cursor.execute("SELECT source, COUNT(*) FROM names WHERE source IS NOT NULL GROUP BY source")
    print("\nKaynak Dağılımı:")
    for row in cursor.fetchall():
        print(f"  {row[0]:20s}: {row[1]:>10,}")

    print("\n" + "=" * 80)

def main():
    """Ana fonksiyon"""

    # Veritabanı oluştur
    conn, cursor = create_database()

    total_count = 0

    # 1. Mevcut veriyi aktar
    count = import_existing_data(cursor)
    total_count += count
    conn.commit()

    # 2. Sentetik dini isimleri aktar
    count = import_synthetic_data(cursor, "synthetic_religious_names.json")
    total_count += count
    conn.commit()

    # 3. Sentetik Christian/African isimleri aktar
    count = import_synthetic_data(cursor, "synthetic_christian_african_names.json")
    total_count += count
    conn.commit()

    # İstatistikler
    get_statistics(cursor)

    # VACUUM
    print("\nVERİTABANI OPTİMİZE EDİLİYOR...")
    conn.execute("VACUUM")
    print("✓ Optimize tamamlandı")

    # Dosya boyutu
    size_mb = NEW_DB_PATH.stat().st_size / (1024 * 1024)
    print(f"\nVeritabanı Boyutu: {size_mb:.2f} MB")

    conn.close()

    print("\n" + "=" * 80)
    print(f"✓ MEGA DATABASE OLUŞTURULDU: {NEW_DB_PATH}")
    print(f"✓ Toplam {total_count:,} kayıt içe aktarıldı")
    print("=" * 80)

if __name__ == "__main__":
    main()
