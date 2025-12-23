"""
Wikidata/Wikipedia Name Extraction via SPARQL

Query Wikidata for:
- Person entities with nationality/occupation
- Country-specific name patterns
- Frequency data from Wikipedia categories
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import quote
import requests


@dataclass
class WikidataPerson:
    """Person entity from Wikidata."""
    name: str
    first_name: str
    last_name: str
    nationality: str
    country_code: str
    occupation: Optional[str] = None
    birth_year: Optional[int] = None


class WikidataNameExtractor:
    """
    Extract names from Wikidata via SPARQL queries.

    Example SPARQL:
        SELECT ?person ?personLabel ?countryLabel WHERE {
          ?person wdt:P31 wd:Q5;          # instance of human
                  wdt:P27 ?country.        # has nationality
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 10000
    """

    SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
    USER_AGENT = "EthniData/4.1.0 (https://github.com/teyfikoz/ethnidata)"

    # Country code mapping (Wikidata Q-codes to ISO codes)
    COUNTRY_MAPPING = {
        "Q43": "TR",  # Turkey
        "Q17": "JP",  # Japan
        "Q148": "CN", # China
        "Q30": "US",  # United States
        "Q145": "GB", # United Kingdom
        "Q142": "FR", # France
        "Q183": "DE", # Germany
        "Q38": "IT",  # Italy
        "Q29": "ES",  # Spain
        "Q96": "MX",  # Mexico
        "Q155": "BR", # Brazil
        "Q159": "RU", # Russia
        "Q668": "IN", # India
        "Q45": "PT",  # Portugal
        "Q55": "NL",  # Netherlands
        # Add more as needed...
    }

    def __init__(self, rate_limit_delay: float = 1.0, cache_dir: Optional[str] = None):
        """
        Initialize Wikidata extractor.

        Args:
            rate_limit_delay: Seconds to wait between requests (respect their limits!)
            cache_dir: Directory to cache results (optional)
        """
        self.rate_limit_delay = rate_limit_delay
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    def query_sparql(self, sparql_query: str, timeout: int = 30) -> List[Dict]:
        """
        Execute SPARQL query against Wikidata.

        Args:
            sparql_query: SPARQL query string
            timeout: Request timeout in seconds

        Returns:
            List of result bindings
        """
        params = {
            "query": sparql_query,
            "format": "json"
        }

        try:
            response = self.session.get(
                self.SPARQL_ENDPOINT,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()

            # Rate limiting (be nice to Wikidata!)
            time.sleep(self.rate_limit_delay)

            return data.get("results", {}).get("bindings", [])
        except Exception as e:
            print(f"⚠️  Wikidata SPARQL query failed: {e}")
            return []

    def extract_names_by_country(
        self,
        country_q_code: str,
        limit: int = 10000,
        offset: int = 0
    ) -> List[WikidataPerson]:
        """
        Extract person names for a specific country.

        Args:
            country_q_code: Wikidata Q-code (e.g., "Q43" for Turkey)
            limit: Maximum results to fetch
            offset: Result offset for pagination

        Returns:
            List of WikidataPerson objects
        """
        sparql_query = f"""
        SELECT ?person ?personLabel ?givenNameLabel ?familyNameLabel ?birthYear WHERE {{
          ?person wdt:P31 wd:Q5;                    # instance of human
                  wdt:P27 wd:{country_q_code}.       # has nationality
          OPTIONAL {{ ?person wdt:P735 ?givenName. }}   # given name
          OPTIONAL {{ ?person wdt:P734 ?familyName. }}  # family name
          OPTIONAL {{ ?person wdt:P569 ?birthDate.
                      BIND(YEAR(?birthDate) AS ?birthYear) }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        OFFSET {offset}
        """

        results = self.query_sparql(sparql_query)
        persons = []

        country_code = self.COUNTRY_MAPPING.get(country_q_code, "XX")

        for result in results:
            try:
                full_name = result.get("personLabel", {}).get("value", "")
                given_name = result.get("givenNameLabel", {}).get("value", "")
                family_name = result.get("familyNameLabel", {}).get("value", "")
                birth_year = result.get("birthYear", {}).get("value")

                if not full_name:
                    continue

                # Parse full name if given/family not available
                if not given_name or not family_name:
                    parts = full_name.split()
                    if len(parts) >= 2:
                        given_name = parts[0]
                        family_name = " ".join(parts[1:])
                    else:
                        given_name = full_name
                        family_name = ""

                person = WikidataPerson(
                    name=full_name,
                    first_name=given_name,
                    last_name=family_name,
                    nationality=country_q_code,
                    country_code=country_code,
                    birth_year=int(birth_year) if birth_year else None
                )

                persons.append(person)
            except Exception as e:
                continue  # Skip malformed entries

        return persons

    def extract_turkish_names(self, limit: int = 10000) -> List[WikidataPerson]:
        """Extract Turkish names (convenience method)."""
        return self.extract_names_by_country("Q43", limit=limit)

    def extract_japanese_names(self, limit: int = 10000) -> List[WikidataPerson]:
        """Extract Japanese names (convenience method)."""
        return self.extract_names_by_country("Q17", limit=limit)

    def extract_chinese_names(self, limit: int = 10000) -> List[WikidataPerson]:
        """Extract Chinese names (convenience method)."""
        return self.extract_names_by_country("Q148", limit=limit)

    def bulk_extract(
        self,
        country_q_codes: List[str],
        limit_per_country: int = 5000
    ) -> Dict[str, List[WikidataPerson]]:
        """
        Extract names for multiple countries.

        Args:
            country_q_codes: List of Wikidata Q-codes
            limit_per_country: Max results per country

        Returns:
            Dictionary mapping country codes to person lists
        """
        results = {}

        for q_code in country_q_codes:
            country_code = self.COUNTRY_MAPPING.get(q_code, q_code)
            print(f"🔍 Extracting names for {country_code} ({q_code})...")

            persons = self.extract_names_by_country(q_code, limit=limit_per_country)
            results[country_code] = persons

            print(f"   ✅ Found {len(persons)} persons")

        return results

    def to_ethnidata_format(self, persons: List[WikidataPerson]) -> List[Dict]:
        """
        Convert WikidataPerson list to EthniData database format.

        Returns:
            List of dictionaries with keys: first_name, last_name, country, gender (unknown)
        """
        records = []

        for person in persons:
            if person.first_name:
                records.append({
                    "name": person.first_name,
                    "name_type": "first",
                    "country": person.country_code,
                    "gender": "U",  # Unknown - would need separate gender inference
                    "frequency": 1,  # Actual frequency would require aggregation
                    "source": "wikidata"
                })

            if person.last_name:
                records.append({
                    "name": person.last_name,
                    "name_type": "last",
                    "country": person.country_code,
                    "gender": "U",
                    "frequency": 1,
                    "source": "wikidata"
                })

        return records


# Example usage
if __name__ == "__main__":
    extractor = WikidataNameExtractor(rate_limit_delay=2.0)

    # Extract Turkish names
    turkish_names = extractor.extract_turkish_names(limit=100)
    print(f"\nExtracted {len(turkish_names)} Turkish names")

    # Show samples
    for person in turkish_names[:5]:
        print(f"  {person.first_name} {person.last_name}")

    # Convert to EthniData format
    records = extractor.to_ethnidata_format(turkish_names)
    print(f"\nConverted to {len(records)} database records")
