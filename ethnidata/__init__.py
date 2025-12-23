"""
EthniData v4.0.0 - STATE-OF-THE-ART NAME ANALYSIS ENGINE
Predict nationality, ethnicity, gender, region, language AND religion!

🔥 NEW in v4.0.0 - EXPLAINABLE AI & TRANSPARENCY:
- 🧠 **Explainability Layer** - Understand WHY predictions are made
- 📊 **Ambiguity Scoring** - Shannon entropy for uncertainty quantification (0-1)
- 🔍 **Morphology Detection** - Rule-based pattern recognition (9 cultural groups)
- 📈 **Confidence Breakdown** - Interpretable confidence components
- 🎯 **Synthetic Data Engine** - Privacy-safe test data generation
- 📚 **Academic-Grade** - Transparent, reproducible, legally compliant

Database:
- 📊 **5.9M+ records** (14x increase from v2.0.0)
- 🌍 **238 countries** - complete global coverage
- 🗣️  **72 languages**
- 🕌 **6 MAJOR WORLD RELIGIONS**:
  - Christianity: 3.9M+ records (65.2%)
  - Buddhism: 1.3M+ records (22.1%)
  - Islam: 504K+ records (8.5%)
  - Judaism: 121K+ records (2.0%)
  - Hinduism: 90K+ records (1.5%)
  - Sikhism: 24K+ records (0.4%)

Features:
- ✅ Nationality prediction (238 countries)
- ✅ Religion prediction (6 major world religions)
- ✅ Gender prediction
- ✅ Region prediction (5 continents)
- ✅ Language prediction (72 languages)
- ✅ Ethnicity prediction
- ✅ Full name analysis
- 🆕 Explainable AI (explain=True)
- 🆕 Morphology pattern detection
- 🆕 Ambiguity scoring (Shannon entropy)
- 🆕 Confidence breakdown
- 🆕 Synthetic data generation

Usage:
    from ethnidata import EthniData

    ed = EthniData()

    # Basic prediction
    result = ed.predict_nationality("Ahmet")

    # v4.0.0: With explainability
    result = ed.predict_nationality("Yılmaz", name_type="last", explain=True)
    print(result['ambiguity_score'])      # Shannon entropy
    print(result['confidence_level'])     # 'High', 'Medium', 'Low'
    print(result['morphology_signal'])    # Detected patterns
    print(result['explanation']['why'])   # Human-readable reasons

    # Full name with explanation
    result = ed.predict_full_name("Mehmet", "Yılmaz", explain=True)

    # Morphology-only analysis
    from ethnidata.morphology import MorphologyEngine
    signal = MorphologyEngine.get_morphological_signal("O'Connor", "last")
    # Returns: {'primary_pattern': "o'", 'pattern_type': 'gaelic', ...}

    # Synthetic data generation
    from ethnidata.synthetic import SyntheticDataEngine, SyntheticConfig
    engine = SyntheticDataEngine(freq_provider)
    config = SyntheticConfig(size=10000, country="TUR")
    records = engine.generate(config)
"""

__version__ = "4.1.1"
__author__ = "Teyfik Oz"
__license__ = "MIT"

from .predictor import EthniData
from .explainability import ExplainabilityEngine
from .morphology import MorphologyEngine, NameFeatureExtractor

# Synthetic module imports (optional, may not have freq_provider)
try:
    from .synthetic import SyntheticDataEngine, SyntheticConfig, SyntheticRecord, FrequencyProvider
    __all__ = [
        "EthniData",
        "ExplainabilityEngine",
        "MorphologyEngine",
        "NameFeatureExtractor",
        "SyntheticDataEngine",
        "SyntheticConfig",
        "SyntheticRecord",
        "FrequencyProvider"
    ]
except ImportError:
    __all__ = [
        "EthniData",
        "ExplainabilityEngine",
        "MorphologyEngine",
        "NameFeatureExtractor"
    ]
