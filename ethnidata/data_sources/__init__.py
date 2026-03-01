"""
EthniData External Data Sources v4.4.0

Integrations for:
- Wikidata/Wikipedia SPARQL queries
- US Social Security Administration (SSA) baby names
- Government census datasets
- Kaggle name datasets
- Religious affiliation databases
"""

from .kaggle import KaggleNamesIntegration
from .religious import ReligiousNamesDatabase

__all__ = [
    "KaggleNamesIntegration",
    "ReligiousNamesDatabase",
]

# Optional imports (require extra dependencies)
try:
    from .wikidata import WikidataNameExtractor  # noqa: F401
    __all__.append("WikidataNameExtractor")
except ImportError:
    pass

try:
    from .ssa_names import SSABabyNamesLoader  # noqa: F401
    __all__.append("SSABabyNamesLoader")
except ImportError:
    pass

try:
    from .census import CensusDataLoader  # noqa: F401
    __all__.append("CensusDataLoader")
except ImportError:
    pass
