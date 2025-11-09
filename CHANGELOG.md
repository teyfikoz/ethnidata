# Changelog

## [1.2.0] - 2025-11-09

### Added
- **Enhanced Database**: 310K+ unique names (119K first names, 190K last names)
- **Expanded Coverage**: 172 countries, 4 major regions
- **New Data Sources**:
  - US Census Surnames: 50K surnames
  - US Baby Names: 50K first names
  - World Names DB: 50K global names
  - Olympics Dataset: Optimized sampling
  - Phone Directories: 274K names from multiple countries

### Changed
- **Unified Schema**: Single `names` table instead of separate first/last tables
- **Better Performance**: Faster queries with improved indexing
- **Improved Country Mapping**: Better region and language assignment
- Database size: 21 MB (optimized)

### Fixed
- Country code normalization issues
- Gender inference accuracy improved
- Region mapping for 170+ countries

## [1.1.0] - 2024-11-09

### Added
- **Gender Prediction**: `predict_gender()` - Predict gender from first names
- **Region Prediction**: `predict_region()` - Predict geographic region (Europe, Asia, Americas, Africa, Oceania)
- **Language Prediction**: `predict_language()` - Predict most likely language
- **Unified Prediction**: `predict_all()` - Get all predictions at once
- **Enhanced Data**: 600K+ names from multiple sources:
  - Olympics Dataset: 134K names
  - Phone Directories: 187K names
  - UK Baby Names: 258K names
  - French Names: 17K names

### Changed
- Enhanced `predict_nationality()` - Now returns `region` and `language`
- Enhanced `predict_full_name()` - Now returns `region` and `language`
- Enhanced `predict_ethnicity()` - Now returns `region` and `language`
- Database schema updated with `gender`, `region`, and `language` columns

### Improved
- Better data normalization
- More accurate predictions with larger dataset
- Faster queries with optimized indexes

## [1.0.0] - 2024-11-08

### Initial Release
- Basic nationality prediction
- Ethnicity prediction (limited)
- First name and last name support
- SQLite database
- 322K names from Olympics and Phone Directories
