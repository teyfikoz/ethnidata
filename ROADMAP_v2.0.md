# EthniData v2.0 Roadmap
**Author**: Teyfik Oz
**License**: MIT
**Target Version**: v4.0.0 (Major version bump due to significant new features)

---

## 0. Vision & Scope

### Vision Statement
> EthniData is not an ethnicity classifier.
> It is a **cultural probability engine** built from open global name data.

### Strategic Goal
Transform EthniData from a simple name→nationality predictor into a **state-of-the-art, explainable, diaspora-aware cultural signal engine** that:
- ✅ Explains predictions (not just labels)
- ✅ Quantifies uncertainty and ambiguity
- ✅ Handles migration and diaspora contexts
- ✅ Respects temporal name evolution
- ✅ Generates privacy-safe synthetic data
- ✅ Maintains ZERO API costs and 100% open data

---

## 1. Product Principles (Non-Negotiables)

1. **Open Data First**: Use only freely available, legally open datasets
2. **Zero API Costs**: All computation local, no external API dependencies
3. **Legal Risk Minimization**:
   - No ToS violations
   - No scraping gray areas
   - Only open-licensed or official open data
4. **Reproducibility**:
   - Every dataset version hashed
   - Provenance files tracked
   - Build pipeline documented
5. **Deterministic**: Same version + same input = same output
6. **Offline-First**: Default usage requires no internet (DB-based lookup)
7. **Explainability**: Every prediction comes with reasoning
8. **Privacy-Safe**: Statistical signals only, not individual identification

---

## 2. v2.0 Core Modules

### 2.1 Enhanced Core Prediction Engine

**Current** (v3.1.5):
- Basic frequency-based prediction
- Simple confidence scores
- Single-source databases

**New** (v4.0.0):
- **Advanced Normalization**:
  - Unicode NFKC + casefold
  - Diacritics removal (optional)
  - Whitespace/hyphen/apostrophe normalization
  - Transliteration pipeline (unidecode-based, offline)

- **Enhanced Scoring**:
  - Multi-source weighted fusion
  - Name uniqueness features
  - Cross-source agreement metrics
  - **Entropy/Ambiguity Scoring**: Quantify prediction uncertainty (0-1 scale)

### 2.2 Explainability Layer ⭐

**API**: `explain_*()` methods

**Output Schema**:
```python
{
    "prediction": {
        "country": "TUR",
        "confidence": 0.89,
        "top_countries": [...]
    },
    "explanation": {
        "why": [
            "High frequency in Turkish name databases",
            "Strong morphological patterns (suffix: -oğlu)",
            "Cross-source agreement across 3 datasets"
        ],
        "confidence_breakdown": {
            "frequency_strength": 0.62,
            "cross_source_agreement": 0.21,
            "name_uniqueness": 0.11,
            "morphology_signal": 0.06
        },
        "ambiguity_score": 0.15,  # 0=very certain, 1=highly ambiguous
        "confidence_level": "High"  # Low/Medium/High
    }
}
```

### 2.3 Morphology & Linguistics Engine (Rule-Based)

**Pattern Library**:
- **Slavic**: -ov/-ova, -ev/-eva, -ski/-ska
- **Turkic**: -oğlu/-oglu, -soy, -gil, -başı
- **Nordic**: -son/-sen, -dottir
- **Arabic**: al-/el-, bin/binti/ibn, عبد (abd)
- **Gaelic**: Mc/Mac, O'
- **Iberian**: -ez (Hernandez), -es
- **Germanic**: -mann, -schmidt

**Output**:
```python
{
    "morphological_signal": {
        "detected_patterns": ["-oğlu"],
        "likely_regions": ["Anatolia", "Balkans"],
        "pattern_confidence": 0.74
    }
}
```

### 2.4 Diaspora-Aware Adjustment ⭐

**Problem**: "Ahmet" in Germany should reflect both Turkish origin AND German diaspora context

**Solution**: Context-aware probability adjustment using open migration data

**Data Sources** (All Free & Open):
- World Bank Bilateral Migration Matrix
- UN DESA International Migrant Stock
- OECD Migration Data (partial open access)

**Mechanism**:
```python
adjusted_prob(country | name, context) =
    base_prob(country | name) × diaspora_multiplier(context→country)^α
```

**API**:
```python
ed.predict_nationality(
    "Ahmet",
    name_type="first",
    context_country="DEU"  # Germany
)
# Returns: Higher probability for both TUR and DEU
```

### 2.5 Time-Aware Name Evolution ⭐

**Insight**: Name popularity shifts over decades

**Data**: Olympics + Wikidata birth years → decade distributions

**API**:
```python
ed.predict_nationality("Olga", year=1980)  # Soviet era
# vs
ed.predict_nationality("Olga", year=2020)  # Post-Soviet era
```

**Use Cases**:
- Historical demography research
- Sociology studies
- Name trend analysis

### 2.6 Multi-Label Ethnicity Output

**Current**: Single ethnicity label
**New**: Probabilistic ethnic profile

```python
# OLD (v3.x)
{
    "ethnicity": "Arab"
}

# NEW (v4.0)
{
    "ethnic_profile": [
        {"ethnicity": "Arab", "probability": 0.61},
        {"ethnicity": "North African", "probability": 0.22},
        {"ethnicity": "South Asian Muslim", "probability": 0.17}
    ]
}
```

**Ethnicity Taxonomy**:
- Broad categories: Arab, Slavic, Turkic, East Asian, South Asian, Nordic, Latin, Sub-Saharan, etc.
- Region/culture groups for heterogeneous countries

### 2.7 Synthetic Data Engine ⭐ (Privacy-Safe)

**Purpose**: Generate statistically realistic synthetic name populations WITHOUT creating real individuals

**Features**:
- Country-level name distribution sampling
- Diaspora mixture modeling
- Controllable parameters:
  - `seed` (reproducibility)
  - `diaspora_ratio` (migration mix)
  - `rare_name_boost` (diversity control)
  - `noise_level` (avoid overfitting)

**API**:
```python
from ethnidata.synthetic import SyntheticDataEngine, SyntheticConfig

config = SyntheticConfig(
    seed=42,
    size=100000,
    country="TUR",
    context_country="DEU",
    diaspora_ratio=0.25
)

engine = SyntheticDataEngine(freq_provider)
records = engine.generate(config)
engine.export(records, config)
```

**Output Formats**: CSV, JSONL, Parquet

**Use Cases**:
- ML model training (privacy-safe)
- Simulation studies
- Testing and QA

### 2.8 Data Provenance & Versioning

**Manifest System**:
```json
{
    "dataset_name": "ethnidata_core",
    "version": "4.0.0",
    "sources": [
        {
            "name": "wikidata_names",
            "license": "CC0",
            "url": "https://wikidata.org/",
            "retrieval_date": "2025-01-15",
            "sha256": "abc123..."
        }
    ]
}
```

**Build Pipeline**:
```
raw → cleaned → merged → sqlite → packaged
 ↓      ↓         ↓        ↓         ↓
artifacts tracked + checksummed at each step
```

---

## 3. API Design (v2.0)

### 3.1 Core Prediction API (Enhanced)

```python
ed.predict_nationality(
    name: str,
    name_type: str = "first",
    top_n: int = 5,
    context_country: Optional[str] = None,  # NEW
    year: Optional[int] = None,              # NEW
    explain: bool = False                    # NEW
) -> dict
```

```python
ed.predict_ethnicity(
    name: str,
    name_type: str = "first",
    top_n: int = 3,
    context_country: Optional[str] = None,  # NEW
    year: Optional[int] = None,              # NEW
    explain: bool = False                    # NEW
) -> dict
```

### 3.2 New Explainability API

```python
ed.explain(
    name: str,
    name_type: str = "first"
) -> dict
```

### 3.3 Advanced APIs

```python
# Batch processing → DataFrame
ed.predict_batch(
    names: List[dict],
    **kwargs
) -> pd.DataFrame

# Get detailed name profile
ed.get_name_profile(name: str) -> dict

# Calibration (for research)
ed.calibrate_confidence(method="temperature"|"isotonic")
```

---

## 4. Database Schema (SQLite v2)

### Proposed Schema

```sql
-- Enhanced first names table
CREATE TABLE names_first (
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    source TEXT NOT NULL,
    freq INT NOT NULL,
    decade INT,  -- NEW: for time-aware
    PRIMARY KEY (name, country, source)
);

-- Enhanced last names table
CREATE TABLE names_last (
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    source TEXT NOT NULL,
    freq INT NOT NULL,
    decade INT,  -- NEW
    PRIMARY KEY (name, country, source)
);

-- NEW: Ethnicity mapping
CREATE TABLE ethnicity_map (
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    ethnicity TEXT NOT NULL,
    source TEXT NOT NULL,
    weight REAL DEFAULT 1.0
);

-- NEW: Country metadata
CREATE TABLE country_meta (
    country TEXT PRIMARY KEY,
    region TEXT,
    iso3 TEXT,
    population INT,
    migration_index REAL
);

-- Indexes for performance
CREATE INDEX idx_first_name ON names_first(name);
CREATE INDEX idx_first_country ON names_first(country);
CREATE INDEX idx_last_name ON names_last(name);
CREATE INDEX idx_last_country ON names_last(country);
```

### Performance Optimizations

```python
# PRAGMA tuning
PRAGMA cache_size = 10000;
PRAGMA synchronous = NORMAL;
PRAGMA journal_mode = WAL;
PRAGMA temp_store = MEMORY;
```

---

## 5. Testing Strategy (v2.0)

### 5.1 Unit Tests

- Normalization tests (unicode, punctuation, casing)
- Scoring tests (probabilities sum to 1.0)
- Entropy calculation tests
- Morphology pattern detection tests
- Diaspora adjustment tests
- Time-aware tests (year=1980 vs 2020)
- Synthetic engine tests (determinism + distribution sanity)

### 5.2 Golden Test Sets

- 200-500 names per major region
- Expected top-1 country/region
- Top-k coverage metrics

**Metrics**:
- Top-1 accuracy
- Top-3 accuracy
- Calibration error (ECE)
- Ambiguity correlation (high ambiguity → lower accuracy expected)

### 5.3 Property-Based Tests (Hypothesis)

```python
@given(st.text(min_size=1, max_size=50))
def test_no_crash_on_random_input(name):
    result = ed.predict_nationality(name)
    assert isinstance(result, dict)
```

---

## 6. Version Plan

### v3.2.0 (Stabilization - Immediate)
- API backward compatibility
- Enhanced normalization
- Basic entropy scoring
- Minimal explainability (`explain` flag)
- DB migration scripts

### v4.0.0 (Major Release - v2.0 Features)
- ⭐ Diaspora-aware module
- ⭐ Time-aware prediction
- ⭐ Multi-label ethnicity output
- ⭐ Synthetic data engine v1
- ⭐ Full explainability layer
- Provenance + manifests
- Comprehensive tests + docs

### v4.1.0+ (Future Enhancements)
- Optional embeddings (offline models)
- FastText language family signals
- Better calibration toolkit
- Interactive visualization tools

---

## 7. Documentation Requirements

### Must-Have Docs

1. **README Updates**:
   - "Not for identification" disclaimer
   - "Probabilistic signals only"
   - Legal/ethical boundaries

2. **API Reference**: Full docstrings for all new methods

3. **Data Provenance Page**: Dataset sources + licenses

4. **Reproducible Build Guide**: Step-by-step DB construction

5. **Example Notebooks**:
   - Diaspora context demo
   - Time-aware demo
   - Synthetic data generation demo
   - Explainability demo

---

## 8. Ethics, Privacy & Legal

### Core Principles

✅ **DO Use For**:
- Aggregate analytics
- A/B testing segmentation
- Localization decisions
- Research and education

❌ **DON'T Use For**:
- Individual decision-making (credit, hiring, legal)
- Identity verification
- Profiling for discrimination
- Automated decision systems (GDPR/AI Act restricted)

### Legal Safeguards

```markdown
⚠️ **IMPORTANT DISCLAIMER**

EthniData provides **probabilistic cultural signals** based on name statistics.

- NOT for individual identification
- NOT for sensitive decisions (employment, credit, legal)
- Predictions reflect **statistical patterns**, not deterministic facts
- Always combine with explicit user input for sensitive applications
- Compliant with GDPR/CCPA when used for aggregate analytics only
```

---

## 9. Success Metrics (3 Months Post-Launch)

- 📈 **Adoption**: 50,000+ downloads/month
- ⭐ **GitHub Stars**: 500+ stars
- ✅ **Test Coverage**: 90%+ maintained
- 🎯 **Top-1 Accuracy**: >75% on golden sets
- 📊 **Calibration**: ECE < 0.10
- 🌍 **Community**: 20+ contributors
- 📝 **Citations**: 10+ academic papers

---

## 10. Implementation Priority (Phase-by-Phase)

### Phase 1: Foundation (Weeks 1-2) ✅
- ✅ Roadmap documentation
- ✅ Enhanced normalization
- ✅ Basic entropy scoring
- ✅ Synthetic engine skeleton

### Phase 2: Core Features (Weeks 3-4)
- Explainability layer (confidence breakdown)
- Morphology pattern engine
- Multi-source fusion improvements

### Phase 3: Advanced Features (Weeks 5-6)
- Diaspora-aware adjustment
- Time-aware prediction
- Multi-label ethnicity

### Phase 4: Data & Testing (Weeks 7-8)
- Golden test sets
- Migration data integration
- Comprehensive test suite

### Phase 5: Polish & Release (Weeks 9-10)
- Documentation complete
- Examples + tutorials
- CI/CD pipeline
- v4.0.0 release

---

## 11. Done Definition (v4.0.0)

- [x] 100% test pass rate
- [x] Reproducible DB build
- [x] Deterministic outputs (same seed → same result)
- [x] Documentation complete
- [x] All examples runnable
- [x] CI: lint + typecheck + tests + build
- [x] PyPI package published
- [x] GitHub release with changelog
- [x] Academic paper draft prepared

---

**Motto**: *"Intelligence Without APIs, Privacy Without Compromise"*

---

**Next Steps**: Begin Phase 1 implementation → Create synthetic engine module
