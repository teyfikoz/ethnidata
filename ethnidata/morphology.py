"""
EthniData Morphology & Linguistics Engine (v2.0)

Rule-based pattern detection for name morphology.
Detects cultural/linguistic patterns in names (suffixes, prefixes, etc.)

License: MIT
"""

from typing import Dict, List, Optional, Tuple
import re


class MorphologyEngine:
    """
    Detects morphological patterns in names (rule-based, no ML required).
    """

    # Suffix/Prefix patterns by cultural/linguistic group
    PATTERNS = {
        # Slavic patterns
        "slavic": {
            "suffixes": ["-ov", "-ova", "-ev", "-eva", "-ski", "-ska", "-sky", "-ic", "-vić", "-vich"],
            "prefixes": [],
            "regions": ["Eastern Europe", "Balkans", "Russia"],
            "countries": ["RUS", "UKR", "POL", "CZE", "SRB", "BIH"]
        },

        # Turkic patterns
        "turkic": {
            "suffixes": ["-oğlu", "-oglu", "-soy", "-gil", "-başı", "-can", "-han", "-bey"],
            "prefixes": [],
            "regions": ["Anatolia", "Balkans", "Central Asia"],
            "countries": ["TUR", "AZE", "KAZ", "UZB", "TKM"]
        },

        # Nordic patterns
        "nordic": {
            "suffixes": ["-son", "-sen", "-sson", "-dóttir", "-dottir", "-berg", "-ström", "-lund"],
            "prefixes": [],
            "regions": ["Scandinavia", "Iceland"],
            "countries": ["SWE", "NOR", "DNK", "ISL", "FIN"]
        },

        # Arabic patterns
        "arabic": {
            "suffixes": [],
            "prefixes": ["al-", "el-", "bin", "binti", "ibn", "abu", "abd", "abdul"],
            "regions": ["Middle East", "North Africa"],
            "countries": ["SAU", "EGY", "IRQ", "SYR", "JOR", "MAR", "DZA"]
        },

        # Gaelic/Celtic patterns
        "gaelic": {
            "suffixes": [],
            "prefixes": ["mc", "mac", "o'", "ó"],
            "regions": ["Ireland", "Scotland"],
            "countries": ["IRL", "GBR"]
        },

        # Iberian patterns
        "iberian": {
            "suffixes": ["-ez", "-es", "-az", "-is", "-os"],
            "prefixes": ["de", "del", "da", "dos"],
            "regions": ["Iberia", "Latin America"],
            "countries": ["ESP", "PRT", "MEX", "ARG", "BRA"]
        },

        # Germanic patterns
        "germanic": {
            "suffixes": ["-mann", "-schmidt", "-schneider", "-meyer", "-müller", "-bauer"],
            "prefixes": ["von", "van", "der", "de"],
            "regions": ["Central Europe", "Netherlands"],
            "countries": ["DEU", "AUT", "CHE", "NLD", "BEL"]
        },

        # East Asian patterns
        "east_asian": {
            "suffixes": [],
            "prefixes": [],  # East Asian names typically don't have affixes
            "regions": ["East Asia"],
            "countries": ["CHN", "JPN", "KOR", "TWN"],
            "note": "East Asian names follow different morphological rules"
        },

        # South Asian patterns
        "south_asian": {
            "suffixes": ["-kumar", "-singh", "-sharma", "-patel", "-reddy", "-rao"],
            "prefixes": ["sri", "shri"],
            "regions": ["South Asia"],
            "countries": ["IND", "PAK", "BGD", "LKA", "NPL"]
        }
    }

    @staticmethod
    def normalize_for_pattern(name: str) -> str:
        """Normalize name for pattern matching (lowercase, remove spaces)."""
        return name.lower().strip().replace(" ", "").replace("-", "")

    @classmethod
    def detect_patterns(cls, name: str) -> List[Dict[str, any]]:
        """
        Detect morphological patterns in a name.

        Args:
            name: Name to analyze (first or last)

        Returns:
            List of detected patterns with confidence scores
        """
        normalized = cls.normalize_for_pattern(name)
        detected = []

        for pattern_type, pattern_data in cls.PATTERNS.items():
            # Check suffixes
            for suffix in pattern_data.get("suffixes", []):
                suffix_norm = suffix.lower().replace("-", "")
                if normalized.endswith(suffix_norm):
                    detected.append({
                        "pattern_type": pattern_type,
                        "pattern": suffix,
                        "match_type": "suffix",
                        "regions": pattern_data.get("regions", []),
                        "likely_countries": pattern_data.get("countries", []),
                        "confidence": 0.8  # High confidence for suffix match
                    })
                    break  # One suffix per type

            # Check prefixes
            for prefix in pattern_data.get("prefixes", []):
                prefix_norm = prefix.lower().replace("-", "").replace("'", "")
                if normalized.startswith(prefix_norm):
                    detected.append({
                        "pattern_type": pattern_type,
                        "pattern": prefix,
                        "match_type": "prefix",
                        "regions": pattern_data.get("regions", []),
                        "likely_countries": pattern_data.get("countries", []),
                        "confidence": 0.75  # Slightly lower for prefix (more ambiguous)
                    })
                    break  # One prefix per type

        return detected

    @classmethod
    def get_morphological_signal(cls, name: str, name_type: str = "last") -> Optional[Dict[str, any]]:
        """
        Get aggregated morphological signal for a name.

        Args:
            name: Name to analyze
            name_type: "first" or "last" (last names have stronger patterns)

        Returns:
            Morphological signal dict or None if no patterns detected
        """
        patterns = cls.detect_patterns(name)

        if not patterns:
            return None

        # Take the highest confidence pattern
        best_pattern = max(patterns, key=lambda p: p['confidence'])

        # Adjust confidence based on name type
        confidence_multiplier = 1.0 if name_type == "last" else 0.7

        return {
            "detected_patterns": [p['pattern'] for p in patterns],
            "pattern_types": list(set(p['pattern_type'] for p in patterns)),
            "likely_regions": list(set(r for p in patterns for r in p['regions'])),
            "likely_countries": list(set(c for p in patterns for c in p['likely_countries'])),
            "pattern_confidence": round(best_pattern['confidence'] * confidence_multiplier, 4),
            "primary_pattern": best_pattern['pattern'],
            "primary_type": best_pattern['pattern_type']
        }

    @classmethod
    def explain_pattern(cls, pattern_signal: Dict[str, any]) -> str:
        """
        Generate human-readable explanation for detected pattern.

        Args:
            pattern_signal: Output from get_morphological_signal()

        Returns:
            Textual explanation
        """
        if not pattern_signal:
            return "No distinctive morphological patterns detected"

        pattern_type = pattern_signal.get('primary_type', 'unknown')
        pattern = pattern_signal.get('primary_pattern', '')
        regions = pattern_signal.get('likely_regions', [])
        confidence = pattern_signal.get('pattern_confidence', 0.0)

        region_str = ", ".join(regions[:2]) if regions else "unknown"

        explanations = {
            "slavic": f"Slavic name pattern ('{pattern}') common in {region_str}",
            "turkic": f"Turkic name pattern ('{pattern}') typical of {region_str}",
            "nordic": f"Nordic name pattern ('{pattern}') from {region_str}",
            "arabic": f"Arabic name pattern ('{pattern}') associated with {region_str}",
            "gaelic": f"Gaelic name pattern ('{pattern}') from {region_str}",
            "iberian": f"Iberian name pattern ('{pattern}') typical of {region_str}",
            "germanic": f"Germanic name pattern ('{pattern}') from {region_str}",
            "south_asian": f"South Asian name pattern ('{pattern}') from {region_str}",
        }

        explanation = explanations.get(pattern_type, f"Name pattern '{pattern}' detected")

        if confidence > 0.7:
            return f"{explanation} (high confidence)"
        elif confidence > 0.5:
            return f"{explanation} (moderate confidence)"
        else:
            return f"{explanation} (low confidence)"


class NameFeatureExtractor:
    """
    Extract linguistic features from names for analysis.
    """

    @staticmethod
    def get_name_features(name: str) -> Dict[str, any]:
        """
        Extract various linguistic features from a name.

        Args:
            name: Name to analyze

        Returns:
            Dictionary of features
        """
        normalized = name.lower().strip()

        features = {
            "length": len(normalized),
            "has_hyphen": "-" in name,
            "has_apostrophe": "'" in name,
            "has_space": " " in name,
            "starts_with_vowel": normalized[0] in "aeiouáéíóúàèìòù" if normalized else False,
            "ends_with_vowel": normalized[-1] in "aeiouáéíóúàèìòù" if normalized else False,
            "consonant_clusters": bool(re.search(r'[bcdfghjklmnpqrstvwxyz]{3,}', normalized)),
            "double_letters": bool(re.search(r'(.)\1', normalized)),
            "numeric_chars": bool(re.search(r'\d', normalized)),
            "special_chars": bool(re.search(r'[^a-záéíóúàèìòùäöüßñçåæø\s\-\']', normalized)),
        }

        # Vowel/consonant ratio
        vowels = sum(1 for c in normalized if c in "aeiouáéíóúàèìòù")
        features["vowel_ratio"] = vowels / len(normalized) if normalized else 0.0

        return features

    @staticmethod
    def is_likely_romanized(name: str) -> bool:
        """
        Detect if name is likely a romanized/transliterated non-Latin name.

        Args:
            name: Name to check

        Returns:
            True if likely romanized
        """
        features = NameFeatureExtractor.get_name_features(name)

        # Heuristic indicators of romanization:
        # - Uncommon consonant clusters
        # - High consonant ratio
        # - Specific patterns (x, q without u, etc.)

        indicators = 0

        if features['consonant_clusters']:
            indicators += 1

        if features['vowel_ratio'] < 0.25:
            indicators += 1

        if any(char in name.lower() for char in ['x', 'zh', 'ch', 'sh']):
            indicators += 1

        return indicators >= 2
