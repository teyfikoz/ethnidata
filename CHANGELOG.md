# Changelog - EthniData

All notable changes to this project will be documented in this file.

## [4.1.1] - 2025-12-23

### 🐛 BUG FIXES: Morphology Pattern Detection

#### Fixed
- **Turkish Names**: Fixed incorrect Iberian pattern detection for Turkish surnames
  - "Yilmaz" now correctly detects as Turkish (not Iberian -az suffix)
  - Added Turkish character detection (ığşçöü) with 95% confidence
  - Added common Turkish surnames: yilmaz, demir, kaya, arslan, celik, sahin, yildiz
  - Turkish patterns now take priority over other patterns

- **East Asian Names**: Fixed missing morphology signals for Japanese/Chinese/Korean names
  - Added Japanese common surnames: tanaka, suzuki, sato, ito, watanabe, yamamoto, nakamura, kobayashi, kato, yoshida
  - Added Chinese common surnames: zhang, wang, li, chen, liu, yang, huang, zhao, wu, zhou
  - Added Korean common surnames: kim, lee, park, choi, jung, kang, cho, yoon, jang, lim
  - East Asian names now return morphology signal with 90% confidence

#### Tests
- All regression tests passing (Yilmaz → TUR, Tanaka → JPN, Zhang → CHN)
- Morphology signal no longer returns None for common East Asian surnames

---

## [4.1.0] - 2025-12-23

### 🌐 MAJOR UPDATE: External Data Sources Integration

#### Added
- **WikidataNameExtractor**: SPARQL integration for extracting person names from Wikidata
  - Support for 20+ countries via Q-codes
  - Automatic conversion to EthniData format
  - Rate-limited requests to respect Wikidata's guidelines

- **SSABabyNamesLoader**: US Social Security Administration baby names database
  - Download and parse national datasets (1880-2023)
  - Frequency aggregation and trend analysis

- **CensusDataLoader**: Government census and national statistics
  - US Census Bureau surname data (2010 Census)
  - UK ONS, France INSEE mock loaders

- **KaggleNamesIntegration**: Integration with Kaggle name datasets
  - Philippe Remy's name-dataset, Olympics athletes, Arabic/Indian/Chinese names

- **ReligiousNamesDatabase**: Religious affiliation name database
  - 6 major world religions with ~100+ curated names

#### Enhanced
- Database: Expanded to **6M+ records** (from 5.9M)
- Morphology: Improved Turkish/Japanese/Chinese pattern detection
- Accuracy: Enhanced through multi-source frequency weighting

#### Tests
- 60+ new test cases in `tests/test_data_sources.py`
- Integration tests for all data sources

#### Documentation
- Comprehensive Library Guide created
- API documentation for all new modules

### 📦 New Dependencies
```
requests>=2.31.0  # For Wikidata SPARQL queries
```

---

## [4.0.3] - 2024-XX-XX

### Fixed
- Morphology improvements for Turkish surnames
- Confidence threshold adjustments
- Explainability enhancements

---

## [4.0.0] - 2024-XX-XX

### MAJOR RELEASE: Explainable AI
- ExplainabilityEngine
- Ambiguity scoring (Shannon entropy)
- Morphology detection (9 cultural groups)
- 5.9M+ records, 238 countries, 6 religions

---

See full history at: https://github.com/teyfikoz/ethnidata
