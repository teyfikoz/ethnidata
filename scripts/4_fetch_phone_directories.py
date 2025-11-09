#!/usr/bin/env python3
"""
Açık Kaynak Telefon Rehberi Verileri
Kaynaklar:
- OpenPhoneBook Project
- Public domain name lists
- Government open data portals
"""

import requests
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "phone_directories"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_us_census_names():
    """
    US Census Bureau - En yaygın isimler
    Kaynak: https://www.census.gov/topics/population/genealogy/data/2010_surnames.html
    """

    print("🇺🇸 US Census Bureau isimleri indiriliyor...")

    # Sık kullanılan isimler
    urls = {
        "surnames": "https://www2.census.gov/topics/genealogy/2010surnames/names.zip",
    }

    # Not: ZIP dosyası olduğu için manuel indirme gerekebilir
    # Alternatif: GitHub'da hazır CSV listeler

    # Public domain name lists
    github_lists = {
        "common_surnames": "https://raw.githubusercontent.com/aruljohn/popular-baby-names/master/2019/boy_names_2019.txt",
        "world_names": "https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/surnames/us.txt"
    }

    for name, url in github_lists.items():
        try:
            print(f"  → {name}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            output_file = OUTPUT_DIR / f"{name}.txt"
            output_file.write_text(response.text, encoding='utf-8')

            lines = len(response.text.splitlines())
            print(f"    ✓ {lines} satır kaydedildi: {output_file}")

        except Exception as e:
            print(f"    ✗ Hata: {e}")

def fetch_world_name_databases():
    """
    GitHub smashew/NameDatabases - Dünya çapında isimler
    """

    print("\n🌍 Dünya isim veritabanları indiriliyor...")

    base_url = "https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases"

    countries = [
        "us", "gb", "ca", "au", "de", "fr", "es", "it", "nl", "se",
        "no", "dk", "fi", "pl", "ru", "tr", "cn", "jp", "kr", "in"
    ]

    for country in countries:
        for name_type in ["surnames", "first names"]:
            url = f"{base_url}/{name_type}/{country}.txt"

            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()

                output_file = OUTPUT_DIR / f"{country}_{name_type.replace(' ', '_')}.txt"
                output_file.write_text(response.text, encoding='utf-8')

                lines = len(response.text.splitlines())
                print(f"  ✓ {country} {name_type}: {lines} isim")

            except Exception as e:
                # Bazı ülkeler için dosya olmayabilir
                pass

def fetch_unicode_cldr_names():
    """
    Unicode CLDR - Kişi isimleri (100+ dil)
    """

    print("\n🔤 Unicode CLDR isimleri indiriliyor...")

    # CLDR person names
    url = "https://raw.githubusercontent.com/unicode-org/cldr/main/common/annotations/en.xml"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        output_file = OUTPUT_DIR / "unicode_cldr_names.xml"
        output_file.write_text(response.text, encoding='utf-8')

        print(f"  ✓ Kaydedildi: {output_file}")

    except Exception as e:
        print(f"  ✗ Hata: {e}")

def main():
    print("📞 Telefon rehberi ve isim listeleri indiriliyor...\n")

    fetch_us_census_names()
    fetch_world_name_databases()
    fetch_unicode_cldr_names()

    print("\n✅ Telefon rehberi verileri tamamlandı!")

if __name__ == "__main__":
    main()
