#!/usr/bin/env python3
"""
Wikipedia - Küçük batch ile dene
"""

import requests
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw" / "wikipedia"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def query_wikidata_small():
    """Küçük bir sorgu - sadece 1000 kişi"""

    sparql_query = """
    SELECT DISTINCT ?person ?personLabel ?countryLabel ?ethnicityLabel
    WHERE {
      ?person wdt:P31 wd:Q5.                # İnsan
      ?person wdt:P27 ?country.             # Vatandaşlık
      OPTIONAL { ?person wdt:P172 ?ethnicity. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 1000
    """

    url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "EthniData/1.0 (Research)",
        "Accept": "application/json"
    }

    print("🌍 Wikipedia/Wikidata (1000 kayıt) çekiliyor...")

    try:
        response = requests.get(
            url,
            params={"query": sparql_query, "format": "json"},
            headers=headers,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()

        # Parse
        results = []
        for binding in data['results']['bindings']:
            name = binding.get('personLabel', {}).get('value', '')
            country = binding.get('countryLabel', {}).get('value', '')
            ethnicity = binding.get('ethnicityLabel', {}).get('value', '')

            if name and country:
                results.append({
                    'name': name,
                    'country': country,
                    'ethnicity': ethnicity
                })

        # Kaydet
        output_file = OUTPUT_DIR / "wikidata_persons_small.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✅ {len(results)} kişi kaydedildi: {output_file}")

        # Stats
        countries = {}
        for item in results:
            c = item['country']
            countries[c] = countries.get(c, 0) + 1

        print(f"\n📊 Ülke dağılımı (top 10):")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {country}: {count}")

        return len(results)

    except Exception as e:
        print(f"❌ Hata: {e}")
        return 0

if __name__ == "__main__":
    query_wikidata_small()
