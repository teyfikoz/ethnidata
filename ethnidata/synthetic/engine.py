"""
EthniData Synthetic Data Engine (v2.0)
License: MIT

Goal:
- Generate privacy-safe, statistically plausible synthetic name populations
- No real-person generation: sampling from aggregated frequency tables
- Deterministic with seed
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import random
import csv
import json
from collections import Counter


@dataclass(frozen=True)
class SyntheticConfig:
    seed: int = 42
    size: int = 10000
    country: str = "TUR"
    context_country: Optional[str] = None
    diaspora_ratio: float = 0.15
    diaspora_strength: float = 1.0
    rare_name_boost: float = 1.0
    noise_level: float = 0.02
    first_weight: float = 0.4
    last_weight: float = 0.6
    include_probabilities: bool = True
    include_ethnicity_profile: bool = False
    export_format: str = "csv"
    output_path: str = "synthetic_population.csv"


@dataclass
class SyntheticRecord:
    first_name: str
    last_name: str
    origin_country: str
    context_country: Optional[str]
    nationality_top1: Optional[str] = None
    nationality_topk: Optional[List[Dict[str, Any]]] = None
    ethnicity_topk: Optional[List[Dict[str, Any]]] = None


class WeightedSampler:
    """Fast weighted sampler using cumulative distribution."""
    def __init__(self, items: List[str], weights: List[float], rng: random.Random):
        if len(items) != len(weights) or not items:
            raise ValueError("items/weights mismatch or empty")
        total = sum(weights)
        if total <= 0:
            raise ValueError("non-positive total weight")

        self.items = items
        self.cdf = []
        cum = 0.0
        for w in weights:
            cum += w / total
            self.cdf.append(cum)
        self.rng = rng

    def sample(self) -> str:
        r = self.rng.random()
        lo, hi = 0, len(self.cdf) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if r <= self.cdf[mid]:
                hi = mid
            else:
                lo = mid + 1
        return self.items[lo]


class FrequencyProvider:
    """
    Adapter interface for EthniData integration.
    Implement this against your existing DB + predictor.
    """
    def get_first_name_freq(self, country: str) -> Dict[str, int]:
        raise NotImplementedError

    def get_last_name_freq(self, country: str) -> Dict[str, int]:
        raise NotImplementedError

    def get_migration_weights(self, context_country: str) -> Dict[str, float]:
        return {}

    def predict_full_name(self, first: str, last: str, context_country: Optional[str] = None) -> Dict[str, Any]:
        return {"country": None, "top_countries": []}

    def predict_ethnicity(self, name: str, name_type: str = "first", context_country: Optional[str] = None) -> Dict[str, Any]:
        return {"top_ethnicities": []}


class SyntheticDataEngine:
    """
    Privacy-safe synthetic data generator.
    """

    def __init__(self, freq_provider: FrequencyProvider):
        self.freq_provider = freq_provider

    def generate(self, cfg: SyntheticConfig) -> List[SyntheticRecord]:
        self._validate_cfg(cfg)
        rng = random.Random(cfg.seed)

        mixture = self._build_country_mixture(cfg, rng)
        records: List[SyntheticRecord] = []

        for _ in range(cfg.size):
            origin_country = mixture.sample()
            first = self._sample_name(
                self.freq_provider.get_first_name_freq(origin_country),
                rng, cfg.rare_name_boost, cfg.noise_level
            )
            last = self._sample_name(
                self.freq_provider.get_last_name_freq(origin_country),
                rng, cfg.rare_name_boost, cfg.noise_level
            )

            rec = SyntheticRecord(
                first_name=first,
                last_name=last,
                origin_country=origin_country,
                context_country=cfg.context_country
            )

            if cfg.include_probabilities:
                nat = self.freq_provider.predict_full_name(first, last, context_country=cfg.context_country)
                rec.nationality_top1 = nat.get("country")
                rec.nationality_topk = nat.get("top_countries")

                if cfg.include_ethnicity_profile:
                    eth = self.freq_provider.predict_ethnicity(first, name_type="first", context_country=cfg.context_country)
                    rec.ethnicity_topk = eth.get("top_ethnicities") or eth.get("ethnic_profile") or None

            records.append(rec)

        return records

    def export(self, records: List[SyntheticRecord], cfg: SyntheticConfig) -> None:
        if cfg.export_format == "csv":
            self._export_csv(records, cfg.output_path)
        elif cfg.export_format == "jsonl":
            self._export_jsonl(records, cfg.output_path)
        else:
            raise ValueError(f"Unsupported export_format: {cfg.export_format}")

    def sanity_report(self, records: List[SyntheticRecord]) -> Dict[str, Any]:
        """Distribution checks for debugging."""
        origins = Counter(r.origin_country for r in records)
        firsts = Counter(r.first_name for r in records)
        lasts = Counter(r.last_name for r in records)

        return {
            "n": len(records),
            "unique_first_names": len(firsts),
            "unique_last_names": len(lasts),
            "top_origin_countries": origins.most_common(10),
            "top_first_names": firsts.most_common(10),
            "top_last_names": lasts.most_common(10),
        }

    def _build_country_mixture(self, cfg: SyntheticConfig, rng: random.Random) -> WeightedSampler:
        base_country = cfg.country

        if not cfg.context_country or cfg.diaspora_ratio <= 0:
            return WeightedSampler([base_country], [1.0], rng)

        mig = self.freq_provider.get_migration_weights(cfg.context_country)
        mig = dict(mig)
        mig.setdefault(base_country, 1.0)

        origins = list(mig.keys())
        weights = []
        total_other = sum(w for c, w in mig.items() if c != base_country)

        for c in origins:
            if c == base_country:
                weights.append(max(1e-9, 1.0 - cfg.diaspora_ratio))
            else:
                if total_other <= 0:
                    weights.append(1e-9)
                else:
                    w = (mig[c] / total_other) * cfg.diaspora_ratio * cfg.diaspora_strength
                    weights.append(max(1e-9, w))

        return WeightedSampler(origins, weights, rng)

    def _sample_name(self, freq_map: Dict[str, int], rng: random.Random, rare_name_boost: float, noise_level: float) -> str:
        if not freq_map:
            return "unknown"

        items = list(freq_map.keys())
        weights: List[float] = []

        for name in items:
            f = max(1, int(freq_map[name]))
            exponent = 1.0 / max(1e-9, rare_name_boost)
            w = float(f) ** exponent

            if noise_level > 0:
                w *= (1.0 + rng.uniform(-noise_level, noise_level))

            weights.append(max(1e-12, w))

        sampler = WeightedSampler(items, weights, rng)
        return sampler.sample()

    def _export_csv(self, records: List[SyntheticRecord], path: str) -> None:
        fieldnames = ["first_name", "last_name", "origin_country", "context_country", "nationality_top1", "nationality_topk", "ethnicity_topk"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in records:
                w.writerow({
                    "first_name": r.first_name,
                    "last_name": r.last_name,
                    "origin_country": r.origin_country,
                    "context_country": r.context_country or "",
                    "nationality_top1": r.nationality_top1 or "",
                    "nationality_topk": json.dumps(r.nationality_topk, ensure_ascii=False) if r.nationality_topk else "",
                    "ethnicity_topk": json.dumps(r.ethnicity_topk, ensure_ascii=False) if r.ethnicity_topk else "",
                })

    def _export_jsonl(self, records: List[SyntheticRecord], path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for r in records:
                obj = {
                    "first_name": r.first_name,
                    "last_name": r.last_name,
                    "origin_country": r.origin_country,
                    "context_country": r.context_country,
                    "nationality_top1": r.nationality_top1,
                    "nationality_topk": r.nationality_topk,
                    "ethnicity_topk": r.ethnicity_topk,
                }
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def _validate_cfg(self, cfg: SyntheticConfig) -> None:
        if cfg.size <= 0:
            raise ValueError("size must be > 0")
        if not (0.0 <= cfg.diaspora_ratio <= 1.0):
            raise ValueError("diaspora_ratio must be in [0,1]")
        if cfg.noise_level < 0:
            raise ValueError("noise_level must be >= 0")
        if cfg.rare_name_boost <= 0:
            raise ValueError("rare_name_boost must be > 0")
