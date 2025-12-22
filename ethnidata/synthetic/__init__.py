"""
EthniData Synthetic Data Engine (v2.0)

Privacy-safe synthetic name population generator.

License: MIT
"""

from .engine import (
    SyntheticDataEngine,
    SyntheticConfig,
    SyntheticRecord,
    FrequencyProvider,
    WeightedSampler
)

__all__ = [
    'SyntheticDataEngine',
    'SyntheticConfig',
    'SyntheticRecord',
    'FrequencyProvider',
    'WeightedSampler'
]
