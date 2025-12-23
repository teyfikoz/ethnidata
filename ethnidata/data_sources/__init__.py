"""
EthniData External Data Sources v4.1.0

Integrations for:
- Wikidata/Wikipedia SPARQL queries
- US Social Security Administration (SSA) baby names
- Government census datasets
- Kaggle name datasets
- Religious affiliation databases
"""

from .wikidata import WikidataNameExtractor
from .ssa_names import SSABabyNamesLoader
from .census import CensusDataLoader
from .kaggle import KaggleNamesIntegration
from .religious import ReligiousNamesDatabase

__all__ = [
    "WikidataNameExtractor",
    "SSABabyNamesLoader",
    "CensusDataLoader",
    "KaggleNamesIntegration",
    "ReligiousNamesDatabase",
]
