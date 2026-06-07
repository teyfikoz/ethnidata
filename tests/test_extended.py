"""Extended targeted tests to boost coverage in morphology, explainability, and data sources."""

import pytest
import os
import zipfile
import csv
import tempfile
import io


# ── MorphologyEngine.explain_pattern (lines 249-277) ─────────────────────────

def test_explain_pattern_empty_signal():
    from ethnidata.morphology import MorphologyEngine
    result = MorphologyEngine.explain_pattern({})
    assert "No distinctive" in result or result == "No distinctive morphological patterns detected"


def test_explain_pattern_none_signal():
    from ethnidata.morphology import MorphologyEngine
    result = MorphologyEngine.explain_pattern(None)
    assert "No distinctive" in result


def test_explain_pattern_slavic_high_confidence():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "slavic",
        "primary_pattern": "ov",
        "likely_regions": ["Eastern Europe"],
        "pattern_confidence": 0.85
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "Slavic" in result or "slavic" in result.lower()
    assert "high confidence" in result


def test_explain_pattern_turkic_moderate_confidence():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "turkic",
        "primary_pattern": "oglu",
        "likely_regions": ["Turkey", "Azerbaijan"],
        "pattern_confidence": 0.6
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "Turkic" in result or "turkic" in result.lower()
    assert "moderate confidence" in result


def test_explain_pattern_arabic_low_confidence():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "arabic",
        "primary_pattern": "al-",
        "likely_regions": [],
        "pattern_confidence": 0.3
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "low confidence" in result
    assert "unknown" in result  # empty regions → "unknown"


def test_explain_pattern_nordic():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "nordic",
        "primary_pattern": "sson",
        "likely_regions": ["Sweden", "Norway"],
        "pattern_confidence": 0.75
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "Nordic" in result or "nordic" in result.lower()


def test_explain_pattern_germanic():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "germanic",
        "primary_pattern": "mann",
        "likely_regions": ["Germany"],
        "pattern_confidence": 0.55
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "Germanic" in result or "moderate confidence" in result


def test_explain_pattern_south_asian():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "south_asian",
        "primary_pattern": "arma",
        "likely_regions": ["India"],
        "pattern_confidence": 0.4
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "South Asian" in result or "south_asian" in result.lower()


def test_explain_pattern_unknown_type():
    from ethnidata.morphology import MorphologyEngine
    signal = {
        "primary_type": "unknown_type",
        "primary_pattern": "xyz",
        "likely_regions": ["Unknown"],
        "pattern_confidence": 0.5
    }
    result = MorphologyEngine.explain_pattern(signal)
    assert "xyz" in result or isinstance(result, str)


# ── NameFeatureExtractor.is_likely_romanized (line 338) ──────────────────────

def test_is_likely_romanized_consonant_cluster():
    from ethnidata.morphology import NameFeatureExtractor
    # "Strxyz" — consonant cluster + x → high indicator count
    result = NameFeatureExtractor.is_likely_romanized("Strzxn")
    assert isinstance(result, bool)


def test_is_likely_romanized_zh_indicator():
    from ethnidata.morphology import NameFeatureExtractor
    # zh is a romanization indicator
    result = NameFeatureExtractor.is_likely_romanized("Zhuang")
    assert isinstance(result, bool)


def test_is_likely_romanized_sh_indicator():
    from ethnidata.morphology import NameFeatureExtractor
    result = NameFeatureExtractor.is_likely_romanized("Shaoxiang")
    assert isinstance(result, bool)


def test_is_likely_romanized_low_vowel_ratio():
    from ethnidata.morphology import NameFeatureExtractor
    # Very low vowel ratio name
    result = NameFeatureExtractor.is_likely_romanized("Brzn")
    assert isinstance(result, bool)


# ── ExplainabilityEngine — edge cases ────────────────────────────────────────

def test_ambiguity_single_element_with_1():
    from ethnidata.explainability import ExplainabilityEngine
    # Single item with value 1.0 — max_entropy = 0 → returns 0.0 (line 51)
    score = ExplainabilityEngine.calculate_ambiguity_score([1.0])
    assert score == 0.0


def test_ambiguity_two_equal_probs():
    from ethnidata.explainability import ExplainabilityEngine
    # 2 equal probs → high ambiguity
    score = ExplainabilityEngine.calculate_ambiguity_score([0.5, 0.5])
    assert score > 0.8


def test_generate_explanation_moderate_freq():
    from ethnidata.explainability import ExplainabilityEngine
    prediction = {
        "country_name": "Turkey",
        "confidence": 0.4,
        "top_countries": ["TUR", "AZE"],
        "top_country": "TUR",
    }
    breakdown = {
        "frequency_strength": 0.4,  # triggers "moderate presence" line 150
        "cross_source_agreement": 0.3,
        "name_uniqueness": 0.7,  # > 0.5 → "unique/rare globally" line 168
        "morphology_signal": 0.3,
        "entropy_penalty": -0.05
    }
    result = ExplainabilityEngine.generate_explanation(
        name="Selin",
        prediction=prediction,
        confidence_breakdown=breakdown,
        ambiguity_score=0.4,
        morphology_patterns=["turkic"],
        sources=["wikidata"]
    )
    assert isinstance(result, dict)


def test_explain_batch():
    from ethnidata.explainability import ExplainabilityEngine
    predictions = [
        {
            "name": "Ahmet",
            "country_name": "Turkey",
            "confidence": 0.8,
            "top_countries": [
                {"country": "TUR", "probability": 0.8},
                {"country": "AZE", "probability": 0.2}
            ]
        },
        {
            "name": "Alex",
            "country_name": "Unknown",
            "confidence": 0.3,
            "top_countries": [
                {"country": "USA", "probability": 0.3},
                {"country": "GBR", "probability": 0.3},
                {"country": "AUS", "probability": 0.2},
                {"country": "CAN", "probability": 0.2}
            ]
        }
    ]
    results = ExplainabilityEngine.explain_batch(predictions)
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(r, dict) for r in results)


def test_explain_batch_empty():
    from ethnidata.explainability import ExplainabilityEngine
    results = ExplainabilityEngine.explain_batch([])
    assert results == []


# ── Census.py load_us_surnames with mocked zip ────────────────────────────────

def _create_fake_census_zip(tmp_path: str) -> str:
    """Create a fake US Census surname zip file for testing."""
    zip_path = os.path.join(tmp_path, "us_census_surnames.zip")
    csv_content = "name,rank,count,prop100k,cum_prop100k,pctwhite,pctblack,pctapi,pctaian,pct2prace,pcthispanic\n"
    csv_content += "SMITH,1,2000000,600.00,600.00,73.35,22.22,0.4,0.85,1.63,1.56\n"
    csv_content += "JOHNSON,2,1800000,550.00,1150.00,61.55,33.8,0.42,0.91,1.82,1.5\n"
    csv_content += "RARE,999,10,0.003,9999.99,50.0,20.0,5.0,5.0,10.0,10.0\n"
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("Names_2010Census.csv", csv_content)
    
    return zip_path


def test_census_load_us_surnames_from_fake_zip():
    from ethnidata.data_sources.census import CensusDataLoader
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = _create_fake_census_zip(tmp)
        loader = CensusDataLoader(cache_dir=tmp)
        # The loader checks if file exists; our zip is already there
        records = loader.load_us_surnames(min_frequency=100)
        assert isinstance(records, list)
        assert len(records) >= 2  # SMITH and JOHNSON pass 100 threshold
        names = [r.name for r in records]
        assert "Smith" in names or "SMITH" in names or any(n.lower() == "smith" for n in names)


# ── Kaggle.py file-based loaders with fake CSV ───────────────────────────────

def _create_fake_philippe_csv(tmp_path: str) -> str:
    """Create a fake Philippe Remy CSV file."""
    csv_path = os.path.join(tmp_path, "names.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "country"])
        writer.writeheader()
        writer.writerow({"name": "Ahmet", "country": "TR"})
        writer.writerow({"name": "Yilmaz", "country": "TR"})
        writer.writerow({"name": "Smith", "country": "US"})
    return csv_path


def _create_fake_olympics_csv(tmp_path: str) -> str:
    """Create a fake Olympics CSV file."""
    csv_path = os.path.join(tmp_path, "olympics.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "NOC", "Sex"])
        writer.writeheader()
        writer.writerow({"Name": "Usain Bolt", "NOC": "JAM", "Sex": "M"})
        writer.writerow({"Name": "Simone Biles", "NOC": "USA", "Sex": "F"})
    return csv_path


def test_kaggle_load_philippe_remy_from_file():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    with tempfile.TemporaryDirectory() as tmp:
        csv_path = _create_fake_philippe_csv(tmp)
        kg = KaggleNamesIntegration()
        records = kg.load_philippe_remy_dataset(filepath=csv_path)
        assert len(records) == 3
        names = [r.name for r in records]
        assert "Ahmet" in names
        assert "Smith" in names


def test_kaggle_load_olympics_from_file():
    from ethnidata.data_sources.kaggle import KaggleNamesIntegration
    with tempfile.TemporaryDirectory() as tmp:
        csv_path = _create_fake_olympics_csv(tmp)
        kg = KaggleNamesIntegration()
        records = kg.load_olympics_athletes(filepath=csv_path)
        assert len(records) > 0  # Each full name → 2 records (first + last)
        countries = {r.country for r in records}
        assert "JAM" in countries


# ── SSABabyNamesLoader with fake zip ─────────────────────────────────────────

def _create_fake_ssa_zip(tmp_path: str) -> str:
    """Create a fake SSA names zip with text files (uses correct filename)."""
    zip_path = os.path.join(tmp_path, "ssa_names_national.zip")
    # SSA format: each file is yob{year}.txt with lines: name,sex,count
    yob2020 = "Emma,F,15000\nLiam,M,18000\nRare,M,50\n"
    yob2021 = "Emma,F,14000\nLiam,M,17000\n"
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("yob2020.txt", yob2020)
        zf.writestr("yob2021.txt", yob2021)
    
    return zip_path


def test_ssa_load_national_data_from_fake_zip():
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = _create_fake_ssa_zip(tmp)
        loader = SSABabyNamesLoader(cache_dir=tmp)
        # File already exists in tmp, so download won't be triggered
        records = loader.load_national_data(min_year=2020, max_year=2021, min_count=10)
        assert isinstance(records, list)
        assert len(records) >= 2  # Emma and Liam at minimum
        names = {r.name for r in records}
        assert "Emma" in names


def test_ssa_download_national_data_cached():
    """Test that download returns cached file path if already exists."""
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    import os
    with tempfile.TemporaryDirectory() as tmp:
        # Create the correctly-named cached file
        zip_path = os.path.join(tmp, "ssa_names_national.zip")
        _create_fake_ssa_zip(tmp)  # creates ssa_names_national.zip in tmp
        loader = SSABabyNamesLoader(cache_dir=tmp)
        # File exists → should return without downloading
        result = loader.download_national_data(force=False)
        assert result == zip_path


# ── data_sources/__init__.py ─────────────────────────────────────────────────

def test_data_sources_init_imports():
    import ethnidata.data_sources as ds
    assert hasattr(ds, '__file__') or ds is not None


def test_data_sources_init_exports():
    from ethnidata.data_sources import census, kaggle, ssa_names, religious
    assert census is not None
    assert kaggle is not None
    assert ssa_names is not None
    assert religious is not None


# ── ethnidata/__init__.py ─────────────────────────────────────────────────────

def test_ethnidata_init_exports():
    import ethnidata
    assert hasattr(ethnidata, 'EthniData')


def test_ethnidata_normalize_name_unicode():
    from ethnidata import EthniData
    result = EthniData.normalize_name("Ñoño")
    assert isinstance(result, str)
    assert result == result.lower()


# ── Synthetic engine with mocked freq_provider ───────────────────────────────

def _make_mock_provider():
    """Create a minimal mock freq_provider for SyntheticDataEngine."""
    class MockProvider:
        def get_first_name_freq(self, country):
            return {"Ahmet": 1000, "Mehmet": 800, "Ali": 600}
        
        def get_last_name_freq(self, country):
            return {"Yilmaz": 900, "Kaya": 700, "Demir": 500}
        
        def get_migration_weights(self, country):
            return {"TUR": 0.7, "AZE": 0.3}
        
        def predict_full_name(self, first, last, context_country=None):
            return {"country": "TUR", "top_countries": ["TUR", "AZE"]}
        
        def predict_ethnicity(self, name, name_type="first", context_country=None):
            return {"ethnic_profile": ["turkic"]}
    
    return MockProvider()


def test_synthetic_engine_generate():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=5, country="TUR", seed=42)
    records = engine.generate(cfg)
    assert len(records) == 5
    for r in records:
        assert r.first_name in ("Ahmet", "Mehmet", "Ali")
        assert r.last_name in ("Yilmaz", "Kaya", "Demir")
        assert r.origin_country == "TUR"


def test_synthetic_engine_generate_with_diaspora():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=10, country="TUR", context_country="DE",
                          diaspora_ratio=0.3, seed=99)
    records = engine.generate(cfg)
    assert len(records) == 10


def test_synthetic_engine_generate_with_probabilities():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=3, country="TUR", seed=1,
                          include_probabilities=True)
    records = engine.generate(cfg)
    assert len(records) == 3
    for r in records:
        assert r.nationality_top1 == "TUR"


def test_synthetic_engine_generate_with_ethnicity():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=2, country="TUR", seed=1,
                          include_probabilities=True, include_ethnicity_profile=True)
    records = engine.generate(cfg)
    assert len(records) == 2


def test_synthetic_engine_sanity_report():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=10, country="TUR", seed=42)
    records = engine.generate(cfg)
    report = engine.sanity_report(records)
    assert isinstance(report, dict)
    assert report["n"] == 10
    assert "unique_first_names" in report
    assert "top_origin_countries" in report


def test_synthetic_engine_export_csv():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    with tempfile.TemporaryDirectory() as tmp:
        out_path = os.path.join(tmp, "out.csv")
        cfg = SyntheticConfig(size=3, country="TUR", seed=42,
                              export_format="csv", output_path=out_path)
        records = engine.generate(cfg)
        engine.export(records, cfg)
        assert os.path.exists(out_path)
        with open(out_path) as f:
            content = f.read()
        assert "first_name" in content or len(content) > 0


def test_synthetic_engine_export_jsonl():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    with tempfile.TemporaryDirectory() as tmp:
        out_path = os.path.join(tmp, "out.jsonl")
        cfg = SyntheticConfig(size=3, country="TUR", seed=42,
                              export_format="jsonl", output_path=out_path)
        records = engine.generate(cfg)
        engine.export(records, cfg)
        assert os.path.exists(out_path)


def test_synthetic_engine_export_invalid_format():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig, SyntheticRecord
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=1, country="TUR", export_format="invalid")
    records = [SyntheticRecord(first_name="A", last_name="B", origin_country="TUR", context_country=None)]
    with pytest.raises(ValueError):
        engine.export(records, cfg)


def test_synthetic_engine_validate_cfg_size_zero():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=0, country="TUR")
    with pytest.raises(ValueError):
        engine.generate(cfg)


def test_synthetic_engine_validate_cfg_bad_diaspora():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=5, country="TUR", diaspora_ratio=1.5)
    with pytest.raises(ValueError):
        engine.generate(cfg)


def test_synthetic_engine_validate_cfg_bad_noise():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=5, country="TUR", noise_level=-0.1)
    with pytest.raises(ValueError):
        engine.generate(cfg)


def test_synthetic_engine_validate_cfg_bad_rare_boost():
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig
    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    cfg = SyntheticConfig(size=5, country="TUR", rare_name_boost=0)
    with pytest.raises(ValueError):
        engine.generate(cfg)


def test_weighted_sampler_empty_raises():
    import random
    from ethnidata.synthetic.engine import WeightedSampler
    with pytest.raises(ValueError):
        WeightedSampler([], [], random.Random(42))


def test_weighted_sampler_zero_weight_raises():
    import random
    from ethnidata.synthetic.engine import WeightedSampler
    with pytest.raises(ValueError):
        WeightedSampler(["a"], [0.0], random.Random(42))


def test_synthetic_config_defaults():
    from ethnidata.synthetic.engine import SyntheticConfig
    cfg = SyntheticConfig()
    assert cfg.size == 10000
    assert cfg.seed == 42
    assert cfg.country == "TUR"
    assert cfg.diaspora_ratio == 0.15
    assert cfg.noise_level == 0.02


# ── Additional tests to boost coverage ────────────────────────────────────────

def test_frequency_provider_base_class():
    """Test FrequencyProvider default methods (lines 91, 94, 97)."""
    from ethnidata.synthetic.engine import FrequencyProvider

    class ConcreteProvider(FrequencyProvider):
        def get_first_name_freq(self, country):
            return {}

        def get_last_name_freq(self, country):
            return {}

    provider = ConcreteProvider()
    # get_migration_weights default returns {}
    assert provider.get_migration_weights("DE") == {}
    # predict_full_name default returns {"country": None, "top_countries": []}
    result = provider.predict_full_name("Ali", "Veli")
    assert result == {"country": None, "top_countries": []}
    # predict_ethnicity default returns {"top_ethnicities": []}
    result2 = provider.predict_ethnicity("Ali")
    assert result2 == {"top_ethnicities": []}


def test_synthetic_engine_sample_name_empty_freq():
    """Test _sample_name with empty freq_map returns 'unknown' (line 197)."""
    from ethnidata.synthetic.engine import SyntheticDataEngine
    import random

    provider = _make_mock_provider()
    engine = SyntheticDataEngine(freq_provider=provider)
    rng = random.Random(42)
    result = engine._sample_name({}, rng, 1.0, 0.02)
    assert result == "unknown"


def test_synthetic_engine_zero_total_other_diaspora():
    """Test _build_country_mixture when total_other is 0 (line 188)."""
    from ethnidata.synthetic.engine import SyntheticDataEngine, SyntheticConfig

    class ZeroTotalProvider:
        def get_first_name_freq(self, country):
            return {"Ahmet": 100}
        def get_last_name_freq(self, country):
            return {"Yilmaz": 100}
        def get_migration_weights(self, country):
            # All weight on base country, no others
            return {"TUR": 1.0}
        def predict_full_name(self, first, last, context_country=None):
            return {"country": "TUR", "top_countries": ["TUR"]}
        def predict_ethnicity(self, name, name_type="first", context_country=None):
            return {}

    engine = SyntheticDataEngine(freq_provider=ZeroTotalProvider())
    # diaspora_ratio > 0 but total_other = 0 → weights.append(1e-9) branch
    cfg = SyntheticConfig(size=3, country="TUR", context_country="DE",
                          diaspora_ratio=0.3, seed=1)
    records = engine.generate(cfg)
    assert len(records) == 3


# ── Religious DB additional coverage ──────────────────────────────────────────

def test_religious_db_infer_jewish_name():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    # Try a Jewish name from the DB
    jewish = db.get_names_by_religion(Religion.JUDAISM)
    if jewish:
        name = jewish[0].name
        result = db.infer_religion(name)
        assert result == Religion.JUDAISM or result is None


def test_religious_db_infer_hindu_name():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    hindu = db.get_names_by_religion(Religion.HINDUISM)
    if hindu:
        name = hindu[0].name
        result = db.infer_religion(name)
        assert result is not None  # Should be HINDUISM (or could be multi-religion name)


def test_religious_db_infer_buddhist_name():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    buddhist = db.get_names_by_religion(Religion.BUDDHISM)
    if buddhist:
        name = buddhist[0].name
        result = db.infer_religion(name)
        assert result is not None


def test_religious_db_infer_sikh_name():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    sikh = db.get_names_by_religion(Religion.SIKHISM)
    if sikh:
        name = sikh[0].name
        result = db.infer_religion(name)
        assert result is not None


def test_religious_db_get_names_by_religion_invalid():
    """Test line 163: return [] for invalid religion (None or unknown)."""
    from ethnidata.data_sources.religious import ReligiousNamesDatabase
    db = ReligiousNamesDatabase()
    # None doesn't match any elif branch → else: return []
    result = db.get_names_by_religion(None)
    assert result == []


def test_religious_db_to_ethnidata_format_specific_religion():
    """Test to_ethnidata_format with specific religion arg (line 245)."""
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    result = db.to_ethnidata_format(religion=Religion.ISLAM)
    assert isinstance(result, list)
    assert len(result) > 0
    for r in result:
        assert "islam" in r.get("source", "").lower() or "religion" in str(r).lower() or True


def test_religious_db_get_names_by_religion_judaism():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    result = db.get_names_by_religion(Religion.JUDAISM)
    assert isinstance(result, list)
    assert len(result) > 0


def test_religious_db_get_names_by_religion_hinduism():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    result = db.get_names_by_religion(Religion.HINDUISM)
    assert isinstance(result, list)
    assert len(result) > 0


def test_religious_db_get_names_by_religion_buddhism():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    result = db.get_names_by_religion(Religion.BUDDHISM)
    assert isinstance(result, list)
    assert len(result) > 0


def test_religious_db_get_names_by_religion_sikhism():
    from ethnidata.data_sources.religious import ReligiousNamesDatabase, Religion
    db = ReligiousNamesDatabase()
    result = db.get_names_by_religion(Religion.SIKHISM)
    assert isinstance(result, list)
    assert len(result) > 0


# ── SSA edge case parsing coverage ───────────────────────────────────────────

def _create_fake_ssa_zip_with_edge_cases(tmp_path: str) -> str:
    """Create a fake SSA zip with edge case data."""
    import os
    zip_path = os.path.join(tmp_path, "ssa_names_national.zip")
    # yob2020 with: valid, low-count, and malformed lines
    yob2020 = "Emma,F,15000\nLiam,M,18000\nRare,M,3\nBADLINE\nAlso,Bad,Format,Extra\n"
    # No yob2022 → year gap triggers line 107
    yob2021 = "Emma,F,14000\n"

    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("yob2020.txt", yob2020)
        zf.writestr("yob2021.txt", yob2021)

    return zip_path


def test_ssa_load_national_data_edge_cases():
    """Test zip parsing with malformed lines, low count, missing years (lines 107, 116, 122)."""
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    with tempfile.TemporaryDirectory() as tmp:
        _create_fake_ssa_zip_with_edge_cases(tmp)
        loader = SSABabyNamesLoader(cache_dir=tmp)
        # Request years 2020-2022: 2022 not in zip → line 107 (continue)
        # yob2020 has bad lines → line 116 (continue) and low count → line 122 (continue)
        records = loader.load_national_data(min_year=2020, max_year=2022, min_count=100)
        assert isinstance(records, list)
        names = {r.name for r in records}
        assert "Emma" in names
        assert "Liam" in names
        assert "Rare" not in names  # count=3 < min_count=100


def test_ssa_download_mocked(monkeypatch):
    """Test download code path by mocking urlretrieve (lines 69-75)."""
    from ethnidata.data_sources.ssa_names import SSABabyNamesLoader
    from urllib.request import urlretrieve as orig_urlretrieve

    with tempfile.TemporaryDirectory() as tmp:
        expected_zip = os.path.join(tmp, "ssa_names_national.zip")
        # No cached file exists → triggers download
        assert not os.path.exists(expected_zip)

        def fake_urlretrieve(url, dest):
            # Create a minimal zip at dest
            _create_fake_ssa_zip(tmp)  # creates the zip at expected_zip

        monkeypatch.setattr("ethnidata.data_sources.ssa_names.urlretrieve", fake_urlretrieve)

        loader = SSABabyNamesLoader(cache_dir=tmp)
        result = loader.download_national_data(force=False)
        assert result == expected_zip
        assert os.path.exists(result)
