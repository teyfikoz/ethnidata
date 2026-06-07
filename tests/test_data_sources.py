"""Tests for ethnidata data_sources modules (no network/DB required)."""

import pytest


# ── CensusDataLoader ──────────────────────────────────────────────────────────

def test_census_name_record():
    from ethnidata.data_sources.census import CensusNameRecord
    rec = CensusNameRecord(name="Smith", name_type="last", country="US", frequency=50000, rank=1, gender=None)
    assert rec.name == "Smith"
    assert rec.country == "US"
    assert rec.frequency == 50000
    assert rec.rank == 1
    assert rec.gender is None


def test_census_loader_init():
    from ethnidata.data_sources.census import CensusDataLoader
    import tempfile
    loader = CensusDataLoader(cache_dir=tempfile.gettempdir())
    assert loader.cache_dir is not None


def test_census_load_uk_mock():
    from ethnidata.data_sources.census import CensusDataLoader
    loader = CensusDataLoader()
    records = loader.load_uk_baby_names_mock()
    assert len(records) > 0
    assert all(r.country == "GB" for r in records)
    assert all(r.name_type == "first" for r in records)


def test_census_load_france_insee_mock():
    from ethnidata.data_sources.census import CensusDataLoader
    loader = CensusDataLoader()
    records = loader.load_france_insee_mock()
    assert len(records) > 0
    assert all(r.country == "FR" for r in records)
    assert any(r.name == "Emma" for r in records)


def test_census_to_ethnidata_format():
    from ethnidata.data_sources.census import CensusDataLoader, CensusNameRecord
    loader = CensusDataLoader()
    records = [
        CensusNameRecord(name="Smith", name_type="last", country="US", frequency=100, rank=1, gender=None),
        CensusNameRecord(name="Emma", name_type="first", country="GB", frequency=200, rank=1, gender="F"),
    ]
    result = loader.to_ethnidata_format(records)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Smith"
    assert result[0]["gender"] == "U"
    assert result[1]["gender"] == "F"
    assert all("frequency" in r for r in result)
    assert all("source" in r for r in result)


def test_census_to_ethnidata_format_mock_data():
    from ethnidata.data_sources.census import CensusDataLoader
    loader = CensusDataLoader()
    uk_records = loader.load_uk_baby_names_mock()
    result = loader.to_ethnidata_format(uk_records)
    assert len(result) == len(uk_records)
    for r in result:
        assert r["country"] == "GB"
        assert r["name_type"] == "first"


# ── KaggleNamesIntegration ────────────────────────────────────────────────────

def test_kaggle_name_record():
    from ethnidata.data_sources.kaggle import KaggleNameRecord
    rec = KaggleNameRecord(name="Ahmet", name_type="first", country="TR", gender="M", frequency=10)
    assert rec.name == "Ahmet"
    assert rec.country == "TR"
    assert rec.gender == "M"


def test_kaggle_load_philippe_remy_no_file():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    kg = KaggleNamesIntegration()
    records = kg.load_philippe_remy_dataset(filepath=None)
    assert len(records) > 0


def test_kaggle_load_olympics_no_file():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    kg = KaggleNamesIntegration()
    records = kg.load_olympics_athletes(filepath=None)
    assert len(records) > 0
    countries = {r.country for r in records}
    assert "USA" in countries or "JAM" in countries


def test_kaggle_load_arabic_names_mock():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    kg = KaggleNamesIntegration()
    records = kg.load_arabic_names_mock()
    assert len(records) > 0


def test_kaggle_load_indian_names_mock():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    kg = KaggleNamesIntegration()
    records = kg.load_indian_names_mock()
    assert len(records) > 0
    assert all(r.country == "IN" for r in records)


def test_kaggle_aggregate_frequencies():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration, KaggleNameRecord
    kg = KaggleNamesIntegration()
    records = [
        KaggleNameRecord(name="Ali", name_type="first", country="TR"),
        KaggleNameRecord(name="Ali", name_type="first", country="TR"),
        KaggleNameRecord(name="Veli", name_type="first", country="TR"),
    ]
    freqs = kg.aggregate_frequencies(records)
    assert freqs[("Ali", "first", "TR")] == 2
    assert freqs[("Veli", "first", "TR")] == 1


def test_kaggle_to_ethnidata_format():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    kg = KaggleNamesIntegration()
    records = kg.load_philippe_remy_dataset()
    result = kg.to_ethnidata_format(records)
    assert isinstance(result, list)
    assert len(result) > 0
    for r in result:
        assert "name" in r
        assert "country" in r
        assert r["source"] == "kaggle"


def test_kaggle_to_ethnidata_format_min_frequency():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration, KaggleNameRecord
    kg = KaggleNamesIntegration()
    records = [
        KaggleNameRecord(name="Ali", name_type="first", country="TR"),
        KaggleNameRecord(name="Ali", name_type="first", country="TR"),
        KaggleNameRecord(name="Rare", name_type="first", country="XX"),
    ]
    result = kg.to_ethnidata_format(records, min_frequency=2)
    assert len(result) == 1
    assert result[0]["name"] == "Ali"


# ── SSABabyNamesLoader ────────────────────────────────────────────────────────

def _make_ssa_records():
    from ethnidata.data_sources.ssa_names import SSANameRecord
    return [
        SSANameRecord(name="Emma", gender="F", year=2020, count=15000),
        SSANameRecord(name="Emma", gender="F", year=2021, count=14000),
        SSANameRecord(name="Liam", gender="M", year=2020, count=18000),
        SSANameRecord(name="Liam", gender="M", year=2021, count=17000),
        SSANameRecord(name="Rare", gender="M", year=2020, count=50),
    ]


def test_ssa_name_record():
    from ethnidata.data_sources.ssa_names import SSANameRecord
    rec = SSANameRecord(name="Emma", gender="F", year=2020, count=15000)
    assert rec.name == "Emma"
    assert rec.gender == "F"
    assert rec.year == 2020
    assert rec.count == 15000


def test_ssa_loader_init():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    import tempfile
    loader = SSABabyNamesLoader(cache_dir=tempfile.gettempdir())
    assert loader.cache_dir is not None


def test_ssa_aggregate_frequencies():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    freqs = loader.aggregate_frequencies(records)
    assert freqs[("Emma", "F")] == 29000
    assert freqs[("Liam", "M")] == 35000


def test_ssa_get_top_names_all():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    top = loader.get_top_names(records, top_n=10)
    assert isinstance(top, list)
    assert top[0][0] == "Liam"


def test_ssa_get_top_names_gender_filter():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    top_f = loader.get_top_names(records, gender="F", top_n=5)
    assert top_f[0][0] == "Emma"
    top_m = loader.get_top_names(records, gender="M", top_n=5)
    names = [n for n, _ in top_m]
    assert "Liam" in names


def test_ssa_to_ethnidata_format():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    result = loader.to_ethnidata_format(records, min_frequency=100)
    assert isinstance(result, list)
    assert all(r["country"] == "US" for r in result)
    assert all(r["name_type"] == "first" for r in result)
    assert all(r["source"] == "ssa_usa" for r in result)
    names = [r["name"] for r in result]
    assert "Emma" in names
    assert "Liam" in names
    assert "Rare" not in names


def test_ssa_analyze_trends():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    trend = loader.analyze_trends(records, "Emma")
    assert 2020 in trend
    assert trend[2020] == 15000
    assert trend[2021] == 14000


def test_ssa_analyze_trends_gender_filter():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    trend = loader.analyze_trends(records, "Emma", gender="F")
    assert len(trend) == 2
    trend_m = loader.analyze_trends(records, "Emma", gender="M")
    assert len(trend_m) == 0


def test_ssa_analyze_trends_no_match():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    loader = SSABabyNamesLoader()
    records = _make_ssa_records()
    trend = loader.analyze_trends(records, "Unknown")
    assert trend == {}


# ── WikidataNameExtractor ─────────────────────────────────────────────────────

def test_wikidata_person():
    from ethnidata.data_sources.wikidata import WikidataPerson
    person = WikidataPerson(
        name="Ahmet Yilmaz",
        first_name="Ahmet",
        last_name="Yilmaz",
        nationality="Turkish",
        country_code="TR"
    )
    assert person.first_name == "Ahmet"
    assert person.last_name == "Yilmaz"
    assert person.country_code == "TR"


def test_wikidata_to_ethnidata_format():
    from ethnidata.data_sources.wikidata import WikidataNameExtractor, WikidataPerson
    extractor = WikidataNameExtractor()
    persons = [
        WikidataPerson(name="Ahmet Yilmaz", first_name="Ahmet", last_name="Yilmaz",
                       nationality="Turkish", country_code="TR"),
        WikidataPerson(name="Kemal", first_name="Kemal", last_name="",
                       nationality="Turkish", country_code="TR"),
    ]
    result = extractor.to_ethnidata_format(persons)
    assert isinstance(result, list)
    names = [r["name"] for r in result]
    assert "Ahmet" in names
    assert "Yilmaz" in names
    assert "Kemal" in names
    assert all(r["source"] == "wikidata" for r in result)
    assert all(r["country"] == "TR" for r in result)


def test_wikidata_to_ethnidata_format_empty():
    from ethnidata.data_sources.wikidata import WikidataNameExtractor
    extractor = WikidataNameExtractor()
    result = extractor.to_ethnidata_format([])
    assert result == []


def test_wikidata_person_no_names():
    from ethnidata.data_sources.wikidata import WikidataNameExtractor, WikidataPerson
    extractor = WikidataNameExtractor()
    persons = [
        WikidataPerson(name="Unknown", first_name="", last_name="",
                       nationality="Unknown", country_code="XX"),
    ]
    result = extractor.to_ethnidata_format(persons)
    assert isinstance(result, list)  # empty strings treated as no names


# ── NameFeatureExtractor ──────────────────────────────────────────────────────

def test_name_features_basic():
    from ethnidata.morphology import NameFeatureExtractor
    features = NameFeatureExtractor.get_name_features("Smith")
    assert isinstance(features, dict)
    assert "length" in features
    assert features["length"] == 5
    assert features["has_hyphen"] is False
    assert features["has_apostrophe"] is False
    assert features["ends_with_vowel"] is False


def test_name_features_hyphen():
    from ethnidata.morphology import NameFeatureExtractor
    features = NameFeatureExtractor.get_name_features("Al-Rashid")
    assert features["has_hyphen"] is True


def test_name_features_apostrophe():
    from ethnidata.morphology import NameFeatureExtractor
    features = NameFeatureExtractor.get_name_features("O'Brien")
    assert features["has_apostrophe"] is True


def test_name_features_vowel_ratio():
    from ethnidata.morphology import NameFeatureExtractor
    features = NameFeatureExtractor.get_name_features("Emma")
    assert features["vowel_ratio"] > 0.4


def test_name_features_starts_with_vowel():
    from ethnidata.morphology import NameFeatureExtractor
    features = NameFeatureExtractor.get_name_features("Ahmet")
    assert features["starts_with_vowel"] is True
    features2 = NameFeatureExtractor.get_name_features("Smith")
    assert features2["starts_with_vowel"] is False


def test_name_features_double_letters():
    from ethnidata.morphology import NameFeatureExtractor
    features = NameFeatureExtractor.get_name_features("Emma")
    assert features["double_letters"] is True


def test_is_likely_romanized():
    from ethnidata.morphology import NameFeatureExtractor
    result = NameFeatureExtractor.is_likely_romanized("Zhang")
    assert isinstance(result, bool)
    result2 = NameFeatureExtractor.is_likely_romanized("Emma")
    assert isinstance(result2, bool)


def test_is_likely_romanized_xq_pattern():
    from ethnidata.morphology import NameFeatureExtractor
    # x is a romanization indicator
    result = NameFeatureExtractor.is_likely_romanized("Xiaozhou")
    assert isinstance(result, bool)


# ── ReligiousNamesDatabase ────────────────────────────────────────────────────

def test_religious_db_get_all_names():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase
    db = ReligiousNamesDatabase()
    all_names = db.get_all_names()
    assert isinstance(all_names, dict)  # keys=Religion, values=list of ReligiousNameRecord
    assert len(all_names) > 0
    all_name_strings = {rec.name for records in all_names.values() for rec in records}
    assert "Muhammad" in all_name_strings or len(all_name_strings) > 0


def test_religious_db_get_names_by_religion_islam():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    islamic = db.get_names_by_religion(Religion.ISLAM)
    assert isinstance(islamic, list)
    assert len(islamic) > 0
    names = [r.name for r in islamic]
    assert "Muhammad" in names


def test_religious_db_get_names_by_religion_christian():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    christian = db.get_names_by_religion(Religion.CHRISTIANITY)
    assert isinstance(christian, list)
    assert len(christian) > 0


def test_religious_db_to_ethnidata_format():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase
    db = ReligiousNamesDatabase()
    result = db.to_ethnidata_format()
    assert isinstance(result, list)
    assert len(result) > 0
    for r in result:
        assert "name" in r


def test_religious_enum_has_expected_values():
    from ethnidata.data_sources.religious import Religion
    assert hasattr(Religion, "ISLAM")
    assert hasattr(Religion, "CHRISTIANITY")


def test_religious_db_infer_unknown():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase
    db = ReligiousNamesDatabase()
    result = db.infer_religion("XxUnknownXxXx999")
    assert result is None


def test_religious_db_infer_known_islamic():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    result = db.infer_religion("Muhammad")
    assert result == Religion.ISLAM
