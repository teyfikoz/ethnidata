"""
US Social Security Administration (SSA) Baby Names Database

The SSA publishes annual lists of baby names with frequencies.
Data available from 1880 to present.

Source: https://www.ssa.gov/oact/babynames/limits.html
Format: CSV files by year with columns: name, sex, count
"""

import os
import csv
import zipfile
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.request import urlretrieve
import tempfile


@dataclass
class SSANameRecord:
    """SSA baby name record."""
    name: str
    gender: str  # "M" or "F"
    count: int
    year: int
    rank: Optional[int] = None


class SSABabyNamesLoader:
    """
    Load and process US Social Security Administration baby names data.

    Features:
    - Download national dataset (all years)
    - Download state-specific datasets
    - Frequency aggregation
    - Trend analysis
    """

    NATIONAL_URL = "https://www.ssa.gov/oact/babynames/names.zip"
    STATE_URL_TEMPLATE = "https://www.ssa.gov/oact/babynames/state/{state}.TXT"

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize SSA names loader.

        Args:
            cache_dir: Directory to cache downloaded files
        """
        self.cache_dir = cache_dir or tempfile.gettempdir()
        os.makedirs(self.cache_dir, exist_ok=True)

    def download_national_data(self, force: bool = False) -> str:
        """
        Download national baby names dataset (all years).

        Args:
            force: Force re-download even if cached

        Returns:
            Path to downloaded zip file
        """
        zip_path = os.path.join(self.cache_dir, "ssa_names_national.zip")

        if os.path.exists(zip_path) and not force:
            print(f"✅ Using cached SSA data: {zip_path}")
            return zip_path

        print(f"📥 Downloading SSA national baby names data...")
        print(f"   Source: {self.NATIONAL_URL}")

        try:
            urlretrieve(self.NATIONAL_URL, zip_path)
            print(f"   ✅ Downloaded to: {zip_path}")
            return zip_path
        except Exception as e:
            raise RuntimeError(f"Failed to download SSA data: {e}")

    def load_national_data(
        self,
        min_year: int = 1990,
        max_year: int = 2023,
        min_count: int = 5
    ) -> List[SSANameRecord]:
        """
        Load national baby names data.

        Args:
            min_year: Earliest year to include
            max_year: Latest year to include
            min_count: Minimum occurrences to include

        Returns:
            List of SSANameRecord objects
        """
        zip_path = self.download_national_data()
        records = []

        print(f"📖 Loading SSA data (years {min_year}-{max_year})...")

        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Files are named yob1880.txt, yob1881.txt, ..., yob2023.txt
            for year in range(min_year, max_year + 1):
                filename = f"yob{year}.txt"

                if filename not in zf.namelist():
                    continue

                with zf.open(filename) as f:
                    # Format: name,sex,count
                    lines = f.read().decode('utf-8').strip().split('\n')

                    for line in lines:
                        parts = line.strip().split(',')
                        if len(parts) != 3:
                            continue

                        name, sex, count_str = parts
                        count = int(count_str)

                        if count < min_count:
                            continue

                        record = SSANameRecord(
                            name=name,
                            gender=sex,
                            count=count,
                            year=year
                        )
                        records.append(record)

        print(f"   ✅ Loaded {len(records):,} name records")
        return records

    def aggregate_frequencies(
        self,
        records: List[SSANameRecord]
    ) -> Dict[Tuple[str, str], int]:
        """
        Aggregate name frequencies across all years.

        Args:
            records: List of SSANameRecord objects

        Returns:
            Dictionary mapping (name, gender) to total count
        """
        frequencies = {}

        for record in records:
            key = (record.name, record.gender)
            frequencies[key] = frequencies.get(key, 0) + record.count

        return frequencies

    def get_top_names(
        self,
        records: List[SSANameRecord],
        gender: Optional[str] = None,
        top_n: int = 1000
    ) -> List[Tuple[str, int]]:
        """
        Get top N most popular names.

        Args:
            records: List of SSANameRecord objects
            gender: Filter by gender ("M" or "F"), or None for both
            top_n: Number of top names to return

        Returns:
            List of (name, total_count) tuples, sorted by count descending
        """
        if gender:
            records = [r for r in records if r.gender == gender]

        frequencies = self.aggregate_frequencies(records)

        # Sort by count descending
        sorted_names = sorted(
            [(name, count) for (name, _), count in frequencies.items()],
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_names[:top_n]

    def to_ethnidata_format(
        self,
        records: List[SSANameRecord],
        min_frequency: int = 100
    ) -> List[Dict]:
        """
        Convert SSA records to EthniData database format.

        Args:
            records: List of SSANameRecord objects
            min_frequency: Minimum total frequency to include

        Returns:
            List of dictionaries with EthniData schema
        """
        # Aggregate frequencies
        frequencies = self.aggregate_frequencies(records)

        ethni_records = []

        for (name, gender), count in frequencies.items():
            if count < min_frequency:
                continue

            ethni_records.append({
                "name": name,
                "name_type": "first",
                "country": "US",
                "gender": gender,
                "frequency": count,
                "source": "ssa_usa"
            })

        # Sort by frequency descending
        ethni_records.sort(key=lambda x: x["frequency"], reverse=True)

        return ethni_records

    def analyze_trends(
        self,
        records: List[SSANameRecord],
        name: str,
        gender: Optional[str] = None
    ) -> Dict[int, int]:
        """
        Analyze popularity trend for a specific name over time.

        Args:
            records: List of SSANameRecord objects
            name: Name to analyze
            gender: Filter by gender (optional)

        Returns:
            Dictionary mapping year to count
        """
        trend = {}

        for record in records:
            if record.name != name:
                continue
            if gender and record.gender != gender:
                continue

            trend[record.year] = record.count

        return trend


# Example usage
if __name__ == "__main__":
    loader = SSABabyNamesLoader()

    # Load data from 2010-2023
    records = loader.load_national_data(min_year=2010, max_year=2023)

    # Get top 20 male names
    top_male = loader.get_top_names(records, gender="M", top_n=20)
    print("\n📊 Top 20 Male Names (2010-2023):")
    for i, (name, count) in enumerate(top_male, 1):
        print(f"   {i:2d}. {name:15s} {count:,}")

    # Get top 20 female names
    top_female = loader.get_top_names(records, gender="F", top_n=20)
    print("\n📊 Top 20 Female Names (2010-2023):")
    for i, (name, count) in enumerate(top_female, 1):
        print(f"   {i:2d}. {name:15s} {count:,}")

    # Analyze trend for "Emma"
    emma_trend = loader.analyze_trends(records, "Emma", gender="F")
    print("\n📈 Trend for 'Emma' (Female):")
    for year in sorted(emma_trend.keys()):
        print(f"   {year}: {emma_trend[year]:,}")

    # Convert to EthniData format
    ethni_records = loader.to_ethnidata_format(records, min_frequency=1000)
    print(f"\n✅ Converted {len(ethni_records)} names to EthniData format")
