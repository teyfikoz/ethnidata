#!/usr/bin/env python3
"""
Names Dataset Scraper - 106 ülke verisi
Kaynak: https://github.com/philipperemy/name-dataset
"""

import os
import json
import pandas as pd
import requests
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "names_dataset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_names_dataset():
    """names-dataset repository'den veri çek"""

    print("📦 names-dataset indiriliyor...")

    # GitHub raw URLs
    base_url = "https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/data"

    files = {
        "first_names": f"{base_url}/first_names.all.txt",
        "last_names": f"{base_url}/last_names.all.txt",
    }

    for file_name, url in files.items():
        print(f"  → {file_name} indiriliyor...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            output_file = OUTPUT_DIR / f"{file_name}.txt"
            output_file.write_text(response.text, encoding='utf-8')
            print(f"    ✓ Kaydedildi: {output_file}")

        except Exception as e:
            print(f"    ✗ Hata: {e}")

    # Python package olarak da yükleyelim
    print("\n📦 names-dataset Python paketi yükleniyor...")
    os.system("pip3 install -q names-dataset")

    # Paket kullanarak veri çıkar
    try:
        from names_dataset import NameDataset

        nd = NameDataset()

        print("\n🔍 Örnek veri çıkarılıyor...")

        # Örnek isimler
        test_names = [
            "Ahmet", "Muhammad", "John", "Maria", "Wei", "Yuki",
            "Ivan", "Ahmed", "Carlos", "Emma"
        ]

        results = []
        for name in test_names:
            info = nd.search(name)
            if info:
                results.append({
                    'name': name,
                    'country': info.get('country', {}),
                    'rank': info.get('rank', None)
                })

        # JSON olarak kaydet
        output_json = OUTPUT_DIR / "sample_names.json"
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"  ✓ {len(results)} örnek isim kaydedildi: {output_json}")

    except ImportError as e:
        print(f"  ⚠️  names-dataset paketi yüklenemedi: {e}")

    print("\n✅ names-dataset tamamlandı!")

if __name__ == "__main__":
    download_names_dataset()
