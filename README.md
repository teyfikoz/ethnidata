# EthniData

**State-of-the-art name analysis engine** — predict nationality, ethnicity, gender, language, religion, and region from first/last names. 5.9M+ records, 238 countries, explainable AI, morphology detection, and synthetic data generation.

[![PyPI version](https://badge.fury.io/py/ethnidata.svg)](https://pypi.org/project/ethnidata/)
[![Build](https://github.com/teyfikoz/ethnidata/actions/workflows/publish.yml/badge.svg)](https://github.com/teyfikoz/ethnidata/actions/workflows/publish.yml)
[![CI](https://github.com/teyfikoz/ethnidata/actions/workflows/ci.yml/badge.svg)](https://github.com/teyfikoz/ethnidata/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install ethnidata
```

## Quick Start

```python
from ethnidata import EthniData

ed = EthniData()

# Predict nationality from first name
result = ed.predict_nationality("Ahmet")
print(result["nationality"])     # Turkey
print(result["confidence"])      # 0.87
print(result["region"])          # Middle East

# With full explainability
result = ed.predict_nationality("Yılmaz", name_type="last", explain=True)
print(result["ambiguity_score"])        # 0.21 (low = confident)
print(result["confidence_level"])       # High
print(result["morphology_signal"])      # {'primary_pattern': 'maz_suffix', ...}
print(result["explanation"]["why"])     # 'Suffix -maz is strongly Turkish/Azerbaijani'
```

---

## Features at a Glance

| Feature | Description |
|---------|-------------|
| **Nationality** | 238 countries — predict country of origin from name |
| **Gender** | Male/female/neutral with probability score |
| **Religion** | 6 major world religions (see breakdown below) |
| **Ethnicity** | Fine-grained ethnic group prediction |
| **Region** | 5 continental regions |
| **Language** | 72 languages associated with name origin |
| **Explainability** | Human-readable reasons for every prediction |
| **Morphology** | 9 cultural pattern detectors (Gaelic, Slavic, Arabic, etc.) |
| **Ambiguity Score** | Shannon entropy — 0 = certain, 1 = maximally ambiguous |
| **Synthetic Data** | Privacy-safe name generation for testing/research |

---

## Database Coverage

| Religion | Records | Coverage |
|----------|---------|----------|
| Christianity | 3.9M+ | 65.2% |
| Buddhism | 1.3M+ | 22.1% |
| Islam | 504K+ | 8.5% |
| Judaism | 121K+ | 2.0% |
| Hinduism | 90K+ | 1.5% |
| Sikhism | 24K+ | 0.4% |

**Total: 5.9M+ records · 238 countries · 72 languages**

---

## Nationality Prediction

```python
from ethnidata import EthniData

ed = EthniData()

# First name
r = ed.predict_nationality("Hiroshi")
print(r["nationality"])    # Japan
print(r["confidence"])     # 0.91
print(r["alternatives"])   # [{'nationality': 'China', 'prob': 0.06}, ...]

# Last name
r = ed.predict_nationality("Okonkwo", name_type="last")
print(r["nationality"])    # Nigeria
print(r["region"])         # Africa

# With explanation
r = ed.predict_nationality("O'Brien", name_type="last", explain=True)
print(r["explanation"]["why"])  # "O' prefix is a strong Gaelic/Irish marker"
print(r["morphology_signal"])   # {'primary_pattern': "o'", 'pattern_type': 'gaelic'}
```

---

## Full Name Analysis

```python
from ethnidata import EthniData

ed = EthniData()

# Analyze first + last name together
result = ed.predict_full_name("Mehmet", "Yılmaz")
print(result["nationality"])   # Turkey
print(result["confidence"])    # 0.95
print(result["gender"])        # Male
print(result["religion"])      # Islam
print(result["language"])      # Turkish

# With explainability
result = ed.predict_full_name("John", "Smith", explain=True)
print(result["explanation"]["first_name_signal"])  # 'English/Christian'
print(result["explanation"]["last_name_signal"])   # 'Anglo-Saxon occupational'
print(result["ambiguity_score"])   # 0.15 (highly confident)
```

---

## Gender Prediction

```python
from ethnidata import EthniData

ed = EthniData()

for name in ["Maria", "Carlos", "Alex", "Kim"]:
    r = ed.predict_nationality(name)
    print(f"{name:10s} → gender: {r.get('gender', 'N/A'):8s}  confidence: {r.get('gender_confidence', 0):.2f}")
# Maria      → gender: Female    confidence: 0.97
# Carlos     → gender: Male      confidence: 0.94
# Alex       → gender: Neutral   confidence: 0.52
# Kim        → gender: Neutral   confidence: 0.61
```

---

## Religion Prediction

```python
from ethnidata import EthniData

ed = EthniData()

names = [
    ("Fatima", "Al-Rashid"),
    ("Arjun", "Sharma"),
    ("David", "Cohen"),
    ("Harpreet", "Singh"),
]

for first, last in names:
    r = ed.predict_full_name(first, last)
    print(f"{first} {last}: {r['religion']} ({r['nationality']})")
# Fatima Al-Rashid: Islam (Saudi Arabia)
# Arjun Sharma: Hinduism (India)
# David Cohen: Judaism (Israel)
# Harpreet Singh: Sikhism (India)
```

---

## Morphology Detection

```python
from ethnidata.morphology import MorphologyEngine, NameFeatureExtractor

# Detect cultural pattern from name morphology alone
signal = MorphologyEngine.get_morphological_signal("O'Connor", "last")
print(signal)
# {'primary_pattern': "o'", 'pattern_type': 'gaelic', 'cultural_group': 'Irish', 'confidence': 0.88}

signal = MorphologyEngine.get_morphological_signal("Kowalski", "last")
print(signal)
# {'primary_pattern': 'ski_suffix', 'pattern_type': 'slavic', 'cultural_group': 'Polish', ...}

# Extract morphological features for analysis
features = NameFeatureExtractor.extract("Nakamura", "last")
print(features["suffix"])           # 'mura'
print(features["length"])           # 8
print(features["phonetic_family"])  # 'japanese'
```

---

## Ambiguity Scoring

```python
from ethnidata import EthniData

ed = EthniData()

# Shannon entropy: 0.0 = certain, 1.0 = maximally ambiguous
names = ["Yılmaz", "Kim", "Alex", "Mohammed"]
for name in names:
    r = ed.predict_nationality(name, explain=True)
    print(f"{name:12s}  ambiguity={r['ambiguity_score']:.2f}  level={r['confidence_level']}")
# Yılmaz       ambiguity=0.11  level=High
# Kim          ambiguity=0.74  level=Low
# Alex         ambiguity=0.68  level=Low
# Mohammed     ambiguity=0.22  level=High
```

---

## Synthetic Data Generation

```python
from ethnidata import EthniData, SyntheticDataEngine, SyntheticConfig

ed = EthniData()

# Generate privacy-safe synthetic name dataset for Turkish names
engine = SyntheticDataEngine(ed.freq_provider)
config = SyntheticConfig(size=1000, country="TUR", include_gender=True)
records = engine.generate(config)

print(f"Generated {len(records)} synthetic records")
for r in records[:3]:
    print(f"  {r.first_name} {r.last_name} ({r.gender}) — {r.nationality}")
# Mehmet Yılmaz (Male) — Turkey
# Fatma Demir (Female) — Turkey
# Ali Kaya (Male) — Turkey

# Generate multi-country dataset
config_multi = SyntheticConfig(
    size=5000,
    countries=["USA", "DEU", "JPN", "BRA"],
    balanced=True,
)
dataset = engine.generate(config_multi)
```

---

## Explainability Engine

```python
from ethnidata import ExplainabilityEngine, EthniData

ed = EthniData()

result = ed.predict_full_name("Giuseppe", "Rossi", explain=True)

print(result["explanation"]["why"])
# 'Giuseppe is a classic Italian form of Joseph; Rossi (pl. of rosso) is the most common Italian surname'

print(result["explanation"]["confidence_breakdown"])
# {'database_frequency': 0.91, 'morphology_match': 0.88, 'phonetic_score': 0.85}

print(result["explanation"]["similar_names"])
# ['Gioseppe', 'Beppe', 'Peppe'] — Italian variants
```

---

## Batch Processing

```python
import pandas as pd
from ethnidata import EthniData

ed = EthniData()

df = pd.DataFrame({
    "first_name": ["Ahmet", "Maria", "Hiroshi", "John"],
    "last_name":  ["Yılmaz", "Garcia", "Tanaka", "Smith"],
})

results = []
for _, row in df.iterrows():
    r = ed.predict_full_name(row["first_name"], row["last_name"])
    results.append({
        "nationality": r["nationality"],
        "religion":    r.get("religion", "Unknown"),
        "confidence":  r["confidence"],
    })

df = df.join(pd.DataFrame(results))
print(df[["first_name", "last_name", "nationality", "religion", "confidence"]])
```

---

## Ethical Use

EthniData is designed for:
- **Research and analytics**: population studies, historical data analysis
- **Data quality**: enriching and validating name-country datasets
- **Privacy testing**: generating synthetic test data instead of using real PII
- **Academic use**: reproducible, transparent, citable

Not intended for individual profiling, discrimination, or surveillance. All predictions are probabilistic — treat with appropriate uncertainty.

---

## License

MIT — [Teyfik Öz](https://github.com/teyfikoz)
