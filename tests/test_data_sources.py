"""
Comprehensive tests for new data sources module (v4.1.0)

Tests for:
- WikidataNameExtractor
- SSABabyNamesLoader
- CensusDataLoader
- KaggleNamesIntegration
- ReligiousNamesDatabase
"""

import pytest
from ethnidata.data_sources import (
    WikidataNameExtractor,
    SSABabyNamesLoader,
    CensusDataLoader,
    KaggleNamesIntegration,
    ReligiousNamesDatabase,
)
from ethnidata.data_sources.religious import Religion


class TestWikidataExtractor:
    """Test WikidataNameExtractor."""

    def test_initialization(self):
        """Test extractor initialization."""
        extractor = WikidataNameExtractor(rate_limit_delay=0.5)
        assert extractor.rate_limit_delay == 0.5
        assert extractor.SPARQL_ENDPOINT == "https://query.wikidata.org/sparql"

    def test_country_mapping(self):
        """Test country Q-code mappings."""
        extractor = WikidataNameExtractor()
        assert extractor.COUNTRY_MAPPING["Q43"] == "TR"  # Turkey
        assert extractor.COUNTRY_MAPPING["Q17"] == "JP"  # Japan
        assert extractor.COUNTRY_MAPPING["Q30"] == "US"  # United States

    @pytest.mark.skip("Requires internet connection and is slow")
    def test_extract_turkish_names_live(self):
        """Test live Turkish name extraction (slow, skip by default)."""
        extractor = WikidataNameExtractor(rate_limit_delay=2.0)
        persons = extractor.extract_turkish_names(limit=10)
        assert len(persons) > 0
        assert all(p.country_code == "TR" for p in persons)

    def test_to_ethnidata_format(self):
        """Test conversion to EthniData format."""
        from ethnidata.data_sources.wikidata import WikidataPerson

        persons = [
            WikidataPerson(
                name="Mustafa Kemal Atatürk",
                first_name="Mustafa",
                last_name="Atatürk",
                nationality="Q43",
                country_code="TR"
            )
        ]

        extractor = WikidataNameExtractor()
        records = extractor.to_ethnidata_format(persons)

        assert len(records) == 2  # first + last
        assert records[0]["name"] == "Mustafa"
        assert records[0]["name_type"] == "first"
        assert records[0]["country"] == "TR"
        assert records[1]["name"] == "Atatürk"
        assert records[1]["name_type"] == "last"


class TestSSABabyNames:
    """Test SSABabyNamesLoader."""

    def test_initialization(self):
        """Test loader initialization."""
        loader = SSABabyNamesLoader()
        assert loader.NATIONAL_URL == "https://www.ssa.gov/oact/babynames/names.zip"

    @pytest.mark.skip("Requires large download (~7MB)")
    def test_download_national_data(self):
        """Test downloading SSA data (slow, skip by default)."""
        loader = SSABabyNamesLoader()
        zip_path = loader.download_national_data()
        assert zip_path.endswith(".zip")

    @pytest.mark.skip("Requires downloaded data")
    def test_load_national_data(self):
        """Test loading SSA data."""
        loader = SSABabyNamesLoader()
        records = loader.load_national_data(min_year=2020, max_year=2023, min_count=100)
        assert len(records) > 0
        assert all(r.year >= 2020 and r.year <= 2023 for r in records)
        assert all(r.count >= 100 for r in records)

    def test_aggregate_frequencies(self):
        """Test frequency aggregation."""
        from ethnidata.data_sources.ssa_names import SSANameRecord

        records = [
            SSANameRecord("Emma", "F", 1000, 2020),
            SSANameRecord("Emma", "F", 1100, 2021),
            SSANameRecord("Noah", "M", 900, 2020),
        ]

        loader = SSABabyNamesLoader()
        frequencies = loader.aggregate_frequencies(records)

        assert frequencies[("Emma", "F")] == 2100
        assert frequencies[("Noah", "M")] == 900

    def test_to_ethnidata_format(self):
        """Test conversion to EthniData format."""
        from ethnidata.data_sources.ssa_names import SSANameRecord

        records = [
            SSANameRecord("Emma", "F", 1000, 2020),
            SSANameRecord("Emma", "F", 1100, 2021),
        ]

        loader = SSABabyNamesLoader()
        ethni_records = loader.to_ethnidata_format(records, min_frequency=500)

        assert len(ethni_records) == 1
        assert ethni_records[0]["name"] == "Emma"
        assert ethni_records[0]["gender"] == "F"
        assert ethni_records[0]["frequency"] == 2100
        assert ethni_records[0]["country"] == "US"


class TestCensusData:
    """Test CensusDataLoader."""

    def test_initialization(self):
        """Test loader initialization."""
        loader = CensusDataLoader()
        assert loader.US_SURNAMES_URL.endswith("names.zip")

    @pytest.mark.skip("Requires download")
    def test_load_us_surnames(self):
        """Test loading US Census surnames."""
        loader = CensusDataLoader()
        records = loader.load_us_surnames(min_frequency=1000)
        assert len(records) > 0
        assert all(r.name_type == "last" for r in records)
        assert all(r.country == "US" for r in records)

    def test_mock_uk_names(self):
        """Test UK mock data."""
        loader = CensusDataLoader()
        records = loader.load_uk_baby_names_mock()
        assert len(records) > 0
        assert all(r.country == "GB" for r in records)
        assert all(r.gender in ["M", "F"] for r in records)

    def test_to_ethnidata_format(self):
        """Test conversion to EthniData format."""
        from ethnidata.data_sources.census import CensusNameRecord

        records = [
            CensusNameRecord("Smith", "last", "US", 2500000, rank=1),
            CensusNameRecord("Johnson", "last", "US", 2000000, rank=2),
        ]

        loader = CensusDataLoader()
        ethni_records = loader.to_ethnidata_format(records)

        assert len(ethni_records) == 2
        assert ethni_records[0]["name"] == "Smith"
        assert ethni_records[0]["frequency"] == 2500000
        assert ethni_records[0]["source"] == "census_us"


class TestKaggleIntegration:
    """Test KaggleNamesIntegration."""

    def test_initialization(self):
        """Test initialization."""
        kaggle = KaggleNamesIntegration()
        assert kaggle.data_dir is not None

    def test_mock_philippe_remy(self):
        """Test Philippe Remy mock data."""
        kaggle = KaggleNamesIntegration()
        records = kaggle.load_philippe_remy_dataset()
        assert len(records) > 0
        assert all(r.country in ["TR", "JP", "CN", "US", "ES"] for r in records)

    def test_mock_olympics(self):
        """Test Olympics mock data."""
        kaggle = KaggleNamesIntegration()
        records = kaggle.load_olympics_athletes()
        assert len(records) > 0
        assert all(r.gender in ["M", "F"] for r in records)

    def test_aggregate_frequencies(self):
        """Test frequency aggregation."""
        from ethnidata.data_sources.kaggle import KaggleNameRecord

        records = [
            KaggleNameRecord("Zhang", "last", "CN", frequency=1),
            KaggleNameRecord("Zhang", "last", "CN", frequency=1),
            KaggleNameRecord("Wang", "last", "CN", frequency=1),
        ]

        kaggle = KaggleNamesIntegration()
        frequencies = kaggle.aggregate_frequencies(records)

        assert frequencies[("Zhang", "last", "CN")] == 2
        assert frequencies[("Wang", "last", "CN")] == 1

    def test_to_ethnidata_format(self):
        """Test conversion to EthniData format."""
        kaggle = KaggleNamesIntegration()
        mock_records = kaggle.load_philippe_remy_dataset()
        ethni_records = kaggle.to_ethnidata_format(mock_records)

        assert len(ethni_records) > 0
        assert all("name" in r for r in ethni_records)
        assert all("country" in r for r in ethni_records)
        assert all("frequency" in r for r in ethni_records)


class TestReligiousNames:
    """Test ReligiousNamesDatabase."""

    def test_initialization(self):
        """Test database initialization."""
        db = ReligiousNamesDatabase()
        assert len(db.christian_names) > 0
        assert len(db.islamic_names) > 0
        assert len(db.jewish_names) > 0

    def test_get_names_by_religion(self):
        """Test getting names by religion."""
        db = ReligiousNamesDatabase()

        islamic_names = db.get_names_by_religion(Religion.ISLAM)
        assert len(islamic_names) > 0
        assert all(r.religion == Religion.ISLAM for r in islamic_names)

        christian_names = db.get_names_by_religion(Religion.CHRISTIANITY)
        assert len(christian_names) > 0
        assert all(r.religion == Religion.CHRISTIANITY for r in christian_names)

    def test_infer_religion(self):
        """Test religion inference."""
        db = ReligiousNamesDatabase()

        assert db.infer_religion("Muhammad") == Religion.ISLAM
        assert db.infer_religion("Mary") == Religion.CHRISTIANITY
        assert db.infer_religion("David") == Religion.JUDAISM
        assert db.infer_religion("Krishna") == Religion.HINDUISM
        assert db.infer_religion("Buddha") == Religion.BUDDHISM

        # Unknown name
        assert db.infer_religion("Xyz123") is None

    def test_get_all_names(self):
        """Test getting all religious names."""
        db = ReligiousNamesDatabase()
        all_names = db.get_all_names()

        assert Religion.CHRISTIANITY in all_names
        assert Religion.ISLAM in all_names
        assert Religion.JUDAISM in all_names
        assert len(all_names[Religion.CHRISTIANITY]) > 0

    def test_to_ethnidata_format(self):
        """Test conversion to EthniData format."""
        db = ReligiousNamesDatabase()
        ethni_records = db.to_ethnidata_format(Religion.ISLAM)

        assert len(ethni_records) > 0
        assert all(r["country"] == "XX" for r in ethni_records)  # Religion-based
        assert all("religion" in r["metadata"] for r in ethni_records)
        assert all(r["metadata"]["religion"] == "islam" for r in ethni_records)


# Integration tests
class TestDataSourcesIntegration:
    """Integration tests for all data sources."""

    def test_all_sources_produce_valid_ethnidata_format(self):
        """Test that all sources produce valid EthniData format."""
        # Wikidata
        from ethnidata.data_sources.wikidata import WikidataPerson
        wikidata_persons = [
            WikidataPerson("Test", "Test", "Name", "Q43", "TR")
        ]
        extractor = WikidataNameExtractor()
        wikidata_records = extractor.to_ethnidata_format(wikidata_persons)

        # SSA
        from ethnidata.data_sources.ssa_names import SSANameRecord
        ssa_records_raw = [SSANameRecord("Emma", "F", 1000, 2020)]
        ssa_loader = SSABabyNamesLoader()
        ssa_records = ssa_loader.to_ethnidata_format(ssa_records_raw)

        # Census
        from ethnidata.data_sources.census import CensusNameRecord
        census_records_raw = [CensusNameRecord("Smith", "last", "US", 1000)]
        census_loader = CensusDataLoader()
        census_records = census_loader.to_ethnidata_format(census_records_raw)

        # Kaggle
        kaggle = KaggleNamesIntegration()
        kaggle_mock = kaggle.load_philippe_remy_dataset()
        kaggle_records = kaggle.to_ethnidata_format(kaggle_mock)

        # Religious
        db = ReligiousNamesDatabase()
        religious_records = db.to_ethnidata_format(Religion.ISLAM)

        # Verify all have required fields
        all_records = (
            wikidata_records + ssa_records + census_records +
            kaggle_records + religious_records
        )

        required_fields = ["name", "name_type", "country", "gender", "frequency", "source"]

        for record in all_records:
            for field in required_fields:
                assert field in record, f"Missing field: {field}"
            assert record["name_type"] in ["first", "last"]
            assert record["gender"] in ["M", "F", "U"]
            assert isinstance(record["frequency"], int)
            assert record["frequency"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
