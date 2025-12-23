"""
Kaggle Name Datasets Integration

Popular Kaggle datasets for names:
- "name-dataset" by Philippe Remy (100k+ names with nationality)
- "Nationality prediction from names"
- "Arabic names dataset"
- "Indian names dataset"
- "Chinese names dataset"
- "120 years of Olympic history" (athletes with nationality)
"""

import csv
import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.request import urlretrieve
import tempfile


@dataclass
class KaggleNameRecord:
    """Kaggle dataset name record."""
    name: str
    name_type: str  # "first" or "last"
    country: str
    gender: Optional[str] = None
    frequency: int = 1
    metadata: Optional[Dict] = None


class KaggleNamesIntegration:
    """
    Integration with Kaggle name datasets.

    Note: Actual Kaggle API requires authentication.
    This class provides mock data and parsers for manual downloads.
    """

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize Kaggle integration.

        Args:
            data_dir: Directory containing manually downloaded Kaggle datasets
        """
        self.data_dir = data_dir or tempfile.gettempdir()

    def load_philippe_remy_dataset(
        self,
        filepath: Optional[str] = None
    ) -> List[KaggleNameRecord]:
        """
        Load Philippe Remy's name-dataset.

        Format: CSV with columns: name, country
        Source: https://www.kaggle.com/datasets/philipperemy/name-dataset

        Args:
            filepath: Path to manually downloaded CSV file

        Returns:
            List of KaggleNameRecord objects
        """
        if not filepath:
            print("⚠️  Please provide path to downloaded CSV from Kaggle")
            return self._mock_philippe_remy_data()

        records = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row.get('name', '').strip()
                country = row.get('country', '').strip()

                if not name or not country:
                    continue

                # Infer first/last based on structure
                # (actual dataset might have this info)
                parts = name.split()
                name_type = "first" if len(parts) == 1 else "last"

                record = KaggleNameRecord(
                    name=name,
                    name_type=name_type,
                    country=country,
                    frequency=1
                )
                records.append(record)

        return records

    def _mock_philippe_remy_data(self) -> List[KaggleNameRecord]:
        """Mock data for Philippe Remy dataset."""
        mock_data = [
            ("Ahmet", "first", "TR"),
            ("Yilmaz", "last", "TR"),
            ("Tanaka", "last", "JP"),
            ("Hiroshi", "first", "JP"),
            ("Zhang", "last", "CN"),
            ("Wei", "first", "CN"),
            ("Smith", "last", "US"),
            ("John", "first", "US"),
            ("García", "last", "ES"),
            ("María", "first", "ES"),
        ]

        return [
            KaggleNameRecord(name=n, name_type=t, country=c)
            for n, t, c in mock_data
        ]

    def load_olympics_athletes(
        self,
        filepath: Optional[str] = None
    ) -> List[KaggleNameRecord]:
        """
        Load Olympic athletes dataset.

        Format: CSV with athlete names and nationalities
        Source: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

        Args:
            filepath: Path to downloaded CSV

        Returns:
            List of KaggleNameRecord objects
        """
        if not filepath:
            return self._mock_olympics_data()

        records = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row.get('Name', '').strip()
                noc = row.get('NOC', '').strip()  # National Olympic Committee code
                sex = row.get('Sex', 'U').strip()

                if not name or not noc:
                    continue

                # Split full name
                parts = name.split()
                if len(parts) >= 2:
                    first_name = parts[0]
                    last_name = " ".join(parts[1:])

                    records.append(KaggleNameRecord(
                        name=first_name,
                        name_type="first",
                        country=noc,
                        gender=sex,
                        frequency=1
                    ))

                    records.append(KaggleNameRecord(
                        name=last_name,
                        name_type="last",
                        country=noc,
                        gender=sex,
                        frequency=1
                    ))

        return records

    def _mock_olympics_data(self) -> List[KaggleNameRecord]:
        """Mock Olympic athletes data."""
        mock_athletes = [
            ("Usain Bolt", "JAM", "M"),
            ("Michael Phelps", "USA", "M"),
            ("Simone Biles", "USA", "F"),
            ("Nadia Comăneci", "ROU", "F"),
            ("Naim Süleymanoğlu", "TUR", "M"),
        ]

        records = []
        for full_name, country, gender in mock_athletes:
            parts = full_name.split()
            first = parts[0]
            last = " ".join(parts[1:])

            records.extend([
                KaggleNameRecord(name=first, name_type="first", country=country, gender=gender),
                KaggleNameRecord(name=last, name_type="last", country=country, gender=gender),
            ])

        return records

    def load_arabic_names_mock(self) -> List[KaggleNameRecord]:
        """Mock Arabic names dataset."""
        mock_data = [
            ("محمد", "first", "SA", "M"),  # Muhammad
            ("فاطمة", "first", "EG", "F"),  # Fatima
            ("أحمد", "first", "AE", "M"),   # Ahmad
        ]

        return [
            KaggleNameRecord(name=n, name_type=t, country=c, gender=g)
            for n, t, c, g in mock_data
        ]

    def load_indian_names_mock(self) -> List[KaggleNameRecord]:
        """Mock Indian names dataset."""
        mock_data = [
            ("Sharma", "last", "IN"),
            ("Kumar", "first", "IN", "M"),
            ("Patel", "last", "IN"),
            ("Priya", "first", "IN", "F"),
        ]

        return [
            KaggleNameRecord(name=n, name_type=t, country=c, gender=g if len(args := [n, t, c, g]) == 4 else None)
            for *args in mock_data
        ]

    def aggregate_frequencies(
        self,
        records: List[KaggleNameRecord]
    ) -> Dict[tuple, int]:
        """
        Aggregate name frequencies.

        Args:
            records: List of KaggleNameRecord objects

        Returns:
            Dictionary mapping (name, name_type, country) to count
        """
        frequencies = {}

        for record in records:
            key = (record.name, record.name_type, record.country)
            frequencies[key] = frequencies.get(key, 0) + 1

        return frequencies

    def to_ethnidata_format(
        self,
        records: List[KaggleNameRecord],
        min_frequency: int = 1
    ) -> List[Dict]:
        """
        Convert Kaggle records to EthniData database format.

        Args:
            records: List of KaggleNameRecord objects
            min_frequency: Minimum frequency to include

        Returns:
            List of dictionaries with EthniData schema
        """
        # Aggregate frequencies
        frequencies = self.aggregate_frequencies(records)

        ethni_records = []

        for (name, name_type, country), count in frequencies.items():
            if count < min_frequency:
                continue

            # Find a record with this key to get gender
            gender = next(
                (r.gender for r in records if r.name == name and r.name_type == name_type and r.country == country),
                "U"
            )

            ethni_records.append({
                "name": name,
                "name_type": name_type,
                "country": country,
                "gender": gender or "U",
                "frequency": count,
                "source": "kaggle"
            })

        # Sort by frequency descending
        ethni_records.sort(key=lambda x: x["frequency"], reverse=True)

        return ethni_records


# Example usage
if __name__ == "__main__":
    kaggle = KaggleNamesIntegration()

    # Load mock data (in production, use actual CSV files)
    print("📦 Loading Kaggle name datasets (mock data)...\n")

    philippe_data = kaggle.load_philippe_remy_dataset()
    print(f"📊 Philippe Remy dataset: {len(philippe_data)} records")
    for record in philippe_data[:5]:
        print(f"   {record.name} ({record.name_type}): {record.country}")

    olympics_data = kaggle.load_olympics_athletes()
    print(f"\n🏅 Olympics athletes: {len(olympics_data)} records")
    for record in olympics_data[:5]:
        print(f"   {record.name} ({record.name_type}, {record.gender}): {record.country}")

    # Aggregate and convert
    all_records = philippe_data + olympics_data
    ethni_records = kaggle.to_ethnidata_format(all_records)
    print(f"\n✅ Converted {len(ethni_records)} records to EthniData format")
