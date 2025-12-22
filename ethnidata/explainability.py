"""
EthniData Explainability Layer (v2.0)

Provides detailed explanations for predictions, confidence breakdowns,
and transparency into the decision-making process.

License: MIT
"""

from typing import Dict, List, Any, Optional
import math


class ExplainabilityEngine:
    """
    Generates human-readable explanations for EthniData predictions.
    """

    @staticmethod
    def calculate_ambiguity_score(probabilities: List[float]) -> float:
        """
        Calculate ambiguity score using Shannon entropy.

        Args:
            probabilities: List of probabilities (must sum to ~1.0)

        Returns:
            Ambiguity score in [0, 1]
            - 0 = very certain (one clear winner)
            - 1 = highly ambiguous (uniform distribution)
        """
        if not probabilities or len(probabilities) == 1:
            return 0.0

        # Normalize probabilities
        total = sum(probabilities)
        if total <= 0:
            return 1.0

        probs = [p / total for p in probabilities]

        # Calculate Shannon entropy
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)

        # Normalize by max entropy (log2(n))
        max_entropy = math.log2(len(probs))
        if max_entropy == 0:
            return 0.0

        ambiguity = entropy / max_entropy
        return min(1.0, max(0.0, ambiguity))

    @staticmethod
    def get_confidence_level(confidence: float, ambiguity: float) -> str:
        """
        Convert numeric confidence to human-readable level.

        Args:
            confidence: Confidence score (0-1)
            ambiguity: Ambiguity score (0-1)

        Returns:
            "High", "Medium", or "Low"
        """
        # Adjust confidence by ambiguity penalty
        adjusted = confidence * (1.0 - ambiguity * 0.5)

        if adjusted >= 0.7:
            return "High"
        elif adjusted >= 0.4:
            return "Medium"
        else:
            return "Low"

    @staticmethod
    def decompose_confidence(
        frequency_strength: float,
        cross_source_agreement: float = 0.0,
        name_uniqueness: float = 0.0,
        morphology_signal: float = 0.0,
        entropy_penalty: float = 0.0
    ) -> Dict[str, float]:
        """
        Break down confidence score into interpretable components.

        Args:
            frequency_strength: Base frequency-based confidence (0-1)
            cross_source_agreement: Agreement across multiple sources (0-1)
            name_uniqueness: How unique/rare the name is (0-1)
            morphology_signal: Strength of morphological patterns (0-1)
            entropy_penalty: Reduction due to high ambiguity (0-1)

        Returns:
            Dictionary with normalized breakdown components
        """
        components = {
            "frequency_strength": frequency_strength,
            "cross_source_agreement": cross_source_agreement,
            "name_uniqueness": name_uniqueness,
            "morphology_signal": morphology_signal,
            "entropy_penalty": -entropy_penalty  # Negative contribution
        }

        # Normalize so positive components sum to ~1.0
        total_positive = sum(v for v in components.values() if v > 0)
        if total_positive > 0:
            for key in components:
                if components[key] > 0:
                    components[key] = components[key] / total_positive

        return components

    @staticmethod
    def generate_explanation(
        name: str,
        prediction: Dict[str, Any],
        confidence_breakdown: Dict[str, float],
        ambiguity_score: float,
        morphology_patterns: Optional[List[str]] = None,
        sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for a prediction.

        Args:
            name: The input name
            prediction: The prediction result
            confidence_breakdown: Decomposed confidence components
            ambiguity_score: Ambiguity score (0-1)
            morphology_patterns: Detected morphological patterns
            sources: Data sources used

        Returns:
            Complete explanation structure
        """
        top_country = prediction.get('country_name', 'Unknown')
        confidence = prediction.get('confidence', 0.0)

        # Generate textual explanations
        why = []

        # Frequency-based reasoning
        freq_strength = confidence_breakdown.get('frequency_strength', 0.0)
        if freq_strength > 0.5:
            why.append(f"High frequency in {top_country} name databases")
        elif freq_strength > 0.3:
            why.append(f"Moderate presence in {top_country} records")
        else:
            why.append(f"Limited data available for this name")

        # Cross-source agreement
        cross_source = confidence_breakdown.get('cross_source_agreement', 0.0)
        if cross_source > 0.2:
            n_sources = len(sources) if sources else 2
            why.append(f"Cross-source agreement across {n_sources} datasets")

        # Morphology patterns
        if morphology_patterns and len(morphology_patterns) > 0:
            patterns_str = ", ".join(morphology_patterns)
            why.append(f"Strong morphological patterns detected: {patterns_str}")

        # Name uniqueness
        uniqueness = confidence_breakdown.get('name_uniqueness', 0.0)
        if uniqueness > 0.5:
            why.append("Name is relatively unique/rare globally")
        elif uniqueness < 0.2:
            why.append("Name is very common across multiple regions")

        # Ambiguity warning
        if ambiguity_score > 0.6:
            why.append(f"⚠️ High ambiguity: name is common in {len(prediction.get('top_countries', []))} countries")

        confidence_level = ExplainabilityEngine.get_confidence_level(confidence, ambiguity_score)

        return {
            "prediction": {
                "name": name,
                "country": prediction.get('country'),
                "country_name": top_country,
                "confidence": round(confidence, 4),
                "top_countries": prediction.get('top_countries', [])
            },
            "explanation": {
                "why": why,
                "confidence_breakdown": {
                    k: round(v, 4) for k, v in confidence_breakdown.items()
                },
                "ambiguity_score": round(ambiguity_score, 4),
                "confidence_level": confidence_level
            }
        }

    @staticmethod
    def explain_batch(predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate explanations for a batch of predictions.

        Args:
            predictions: List of prediction results

        Returns:
            List of explanation structures
        """
        explanations = []

        for pred in predictions:
            # Extract probabilities for ambiguity calculation
            top_countries = pred.get('top_countries', [])
            probs = [c.get('probability', 0.0) for c in top_countries]

            ambiguity = ExplainabilityEngine.calculate_ambiguity_score(probs)

            # Simple confidence breakdown (can be enhanced with actual data)
            freq_strength = pred.get('confidence', 0.0)
            breakdown = ExplainabilityEngine.decompose_confidence(
                frequency_strength=freq_strength,
                cross_source_agreement=0.2 if len(top_countries) > 1 else 0.0,
                entropy_penalty=ambiguity * 0.3
            )

            explanation = ExplainabilityEngine.generate_explanation(
                name=pred.get('name', ''),
                prediction=pred,
                confidence_breakdown=breakdown,
                ambiguity_score=ambiguity
            )

            explanations.append(explanation)

        return explanations
