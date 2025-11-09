#!/usr/bin/env python3
"""
Wikipedia Biyografi Scraper - 190+ ülke
Wikidata'dan isim-ülke-etnisite bilgisi çeker
"""

import requests
import json
import time
from pathlib import Path
from tqdm import tqdm

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "wikipedia"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def query_wikidata(limit=10000, offset=0):
    """
    Wikidata SPARQL sorgusu - İnsan isimleri ve ülkeleri
    """

    sparql_query = f"""
    SELECT DISTINCT ?person ?personLabel ?countryLabel ?ethnicityLabel ?birthDate
    WHERE {{
      ?person wdt:P31 wd:Q5.                # İnsan
      ?person wdt:P27 ?country.             # Vatandaşlık
      OPTIONAL {{ ?person wdt:P172 ?ethnicity. }}  # Etnisite
      OPTIONAL {{ ?person wdt:P569 ?birthDate. }}  # Doğum tarihi

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,tr". }}
    }}
    LIMIT {limit}
    OFFSET {offset}
    """

    url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "NBD-Database/1.0 (Educational Research)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            params={"query": sparql_query, "format": "json"},
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"❌ Wikidata sorgu hatası: {e}")
        return None

def parse_wikidata_results(data):
    """Wikidata sonuçlarını parse et"""

    if not data or 'results' not in data:
        return []

    results = []
    for binding in data['results']['bindings']:
        name = binding.get('personLabel', {}).get('value', '')
        country = binding.get('countryLabel', {}).get('value', '')
        ethnicity = binding.get('ethnicityLabel', {}).get('value', '')
        birth_date = binding.get('birthDate', {}).get('value', '')

        if name and country:
            results.append({
                'name': name,
                'country': country,
                'ethnicity': ethnicity,
                'birth_date': birth_date
            })

    return results

def fetch_wikipedia_data(total_limit=200000, batch_size=10000):
    """Wikipedia/Wikidata'dan toplu veri çek"""

    print("🌍 Wikipedia/Wikidata biyografi verisi çekiliyor...")

    all_results = []
    offset = 0

    with tqdm(total=total_limit, desc="Veri çekme") as pbar:
        while offset < total_limit:
            print(f"\n📥 Batch {offset // batch_size + 1}: offset={offset}")

            data = query_wikidata(limit=batch_size, offset=offset)

            if not data:
                print("⚠️  Veri çekilemedi, devam ediliyor...")
                break

            parsed = parse_wikidata_results(data)

            if not parsed:
                print("⚠️  Sonuç bulunamadı, durduruluyor...")
                break

            all_results.extend(parsed)
            pbar.update(len(parsed))

            offset += batch_size

            # Rate limiting (Wikidata API politikası)
            time.sleep(2)

    # Sonuçları kaydet
    output_file = OUTPUT_DIR / "wikidata_persons.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(all_results)} kişi kaydedildi: {output_file}")

    # İstatistikler
    countries = {}
    for item in all_results:
        country = item['country']
        countries[country] = countries.get(country, 0) + 1

    print(f"\n📊 Ülke dağılımı (top 20):")
    for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {country}: {count}")

if __name__ == "__main__":
    fetch_wikipedia_data(total_limit=200000, batch_size=10000)
