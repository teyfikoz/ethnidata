"""
EthniData Predictor v4.0.0 - State-of-the-Art Features
Yeni özellikler:
- Gender prediction (Cinsiyet tahmini)
- Region prediction (Bölge: Europe, Asia, Americas, Africa, Oceania)
- Language prediction (Yaygın dil tahmini)
- Explainability layer (Açıklanabilirlik)
- Ambiguity scoring (Belirsizlik skoru - Shannon entropy)
- Morphology pattern detection (Morfoljik kalıp tespiti)
- Confidence breakdown (Güven skoru ayrıştırması)
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Literal
from unidecode import unidecode
import pycountry

# v4.0.0 new modules
from .explainability import ExplainabilityEngine
from .morphology import MorphologyEngine, NameFeatureExtractor

class EthniData:
    """Ethnicity, Nationality, Gender, Region and Language predictor"""

    def __init__(self, db_path: Optional[str] = None, use_v3: bool = False):
        """
        Initialize EthniData predictor

        Args:
            db_path: Path to SQLite database. If None, uses default location.
            use_v3: If True, attempts to use v3.0.0 database (5.8M records).
                   If False, uses v2.0.0 database (415K records, included in package).
        """
        if db_path is None:
            package_dir = Path(__file__).parent

            if use_v3:
                # Try to use v3 database
                v3_path = package_dir / "ethnidata_v3.db"
                if v3_path.exists():
                    db_path = v3_path
                else:
                    print(f"\n💡 EthniData v3.0.0 (5.8M records) is not installed.")
                    print(f"   To download: from ethnidata.downloader import download_v3_database")
                    print(f"   download_v3_database()")
                    print(f"\n   Using v2.0.0 (415K records) for now...")
                    db_path = package_dir / "ethnidata.db"
            else:
                db_path = package_dir / "ethnidata.db"

        self.db_path = Path(db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.db_path}\n"
                f"Please reinstall: pip install --upgrade --force-reinstall ethnidata"
            )

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize name (lowercase, remove accents)"""
        return unidecode(name.strip().lower())

    def predict_nationality(
        self,
        name: str,
        name_type: Literal["first", "last"] = "first",
        top_n: int = 5,
        explain: bool = False
    ) -> Dict:
        """
        Predict nationality from name - ENHANCED v4.0.0

        Args:
            name: First or last name
            name_type: "first" or "last"
            top_n: Number of top predictions
            explain: If True, includes explainability layer (v4.0.0 NEW!)

        Returns:
            {
                'name': str,
                'country': str (ISO 3166-1 alpha-3),
                'country_name': str,
                'confidence': float (0-1),
                'region': str,
                'language': str,
                'top_countries': [...],

                # NEW v4.0.0 fields (if explain=True):
                'ambiguity_score': float,  # Shannon entropy (0-1)
                'confidence_level': str,  # 'High', 'Medium', 'Low'
                'morphology_signal': {...},  # Detected patterns
                'explanation': {...}  # Full human-readable explanation
            }
        """

        normalized = self.normalize_name(name)

        query = """
            SELECT country_code, region, language, COUNT(*) as frequency
            FROM names
            WHERE name = ? AND name_type = ?
            GROUP BY country_code, region, language
            ORDER BY frequency DESC
            LIMIT ?
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (normalized, name_type, top_n))
        results = cursor.fetchall()

        if not results:
            base_result = {
                'name': normalized,
                'country': None,
                'country_name': None,
                'confidence': 0.0,
                'region': None,
                'language': None,
                'top_countries': []
            }

            # v4.0.0: Add explain fields even when no results
            if explain:
                # Still try to detect morphological patterns
                morphology_signal = MorphologyEngine.get_morphological_signal(name, name_type)

                base_result['ambiguity_score'] = 1.0  # Maximum ambiguity (no data)
                base_result['confidence_level'] = "Low"
                base_result['morphology_signal'] = morphology_signal
                base_result['explanation'] = {
                    'why': ["Name not found in database"],
                    'confidence_breakdown': {
                        'frequency_strength': 0.0,
                        'cross_source_agreement': 0.0,
                        'name_uniqueness': 0.0,
                        'morphology_signal': morphology_signal['pattern_confidence'] if morphology_signal else 0.0,
                        'entropy_penalty': 0.0
                    },
                    'ambiguity_score': 1.0,
                    'confidence_level': "Low"
                }

            return base_result

        # Calculate probabilities
        total_freq = sum(row['frequency'] for row in results)

        top_countries = []
        for row in results:
            prob = row['frequency'] / total_freq

            try:
                country = pycountry.countries.get(alpha_3=row['country_code'])
                country_name = country.name if country else row['country_code']
            except:
                country_name = row['country_code']

            top_countries.append({
                'country': row['country_code'],
                'country_name': country_name,
                'region': row['region'],
                'language': row['language'],
                'probability': round(prob, 4),
                'frequency': row['frequency']
            })

        top = top_countries[0]

        # IMPROVED: Calculate real confidence score
        # Factors: frequency strength, data quality, entropy
        freq_strength = top['probability']
        data_quality = min(1.0, total_freq / 100.0)  # Higher total = better quality

        # Calculate entropy (ambiguity)
        import math
        probs = [c['probability'] for c in top_countries]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probs)
        max_entropy = math.log2(len(probs)) if len(probs) > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

        # Confidence = weighted average
        confidence = (
            freq_strength * 0.6 +      # Probability weight
            data_quality * 0.2 +       # Data quality weight
            (1 - normalized_entropy) * 0.2  # Low entropy = high confidence
        )

        # MORPHOLOGY-BASED CORRECTION for poor database coverage
        # Detect Turkish patterns when data quality is low
        morphology_boost_applied = False
        if data_quality < 0.3:  # Low data quality threshold
            # Detect Turkish name patterns
            turkish_chars = set('ığşçöü')
            turkish_suffixes = ['oğlu', 'oglu', 'er', 'can', 'ay', 'han', 'gül', 'demir', 'kaya', 'yılmaz', 'öz', 'kurt']

            has_turkish_chars = any(c in name.lower() for c in turkish_chars)
            has_turkish_suffix = any(name.lower().endswith(suffix) for suffix in turkish_suffixes)

            if has_turkish_chars or has_turkish_suffix:
                # Boost TUR country if it exists in top results
                tur_found = False
                for i, country_data in enumerate(top_countries):
                    if country_data['country'] == 'TUR':
                        # Move TUR to top and boost its probability
                        top_countries.insert(0, top_countries.pop(i))
                        top = top_countries[0]
                        confidence = max(confidence, 0.7)  # Boost confidence
                        morphology_boost_applied = True
                        tur_found = True
                        break

                # If TUR not in results but strong Turkish signals, inject it
                if not tur_found and (has_turkish_chars and has_turkish_suffix):
                    try:
                        country = pycountry.countries.get(alpha_3='TUR')
                        top_countries.insert(0, {
                            'country': 'TUR',
                            'country_name': country.name if country else 'Turkey',
                            'region': 'Asia',
                            'language': 'Turkish',
                            'probability': 0.8,
                            'frequency': 0
                        })
                        top = top_countries[0]
                        confidence = 0.65  # Moderate confidence for morphology-based
                        morphology_boost_applied = True
                    except:
                        pass

        # Apply minimum confidence threshold
        MIN_CONFIDENCE = 0.15
        if confidence < MIN_CONFIDENCE and not morphology_boost_applied:
            # Return "uncertain" result
            result = {
                'name': normalized,
                'country': None,
                'country_name': None,
                'confidence': round(confidence, 4),
                'region': top['region'],
                'language': top['language'],
                'top_countries': top_countries,
                'note': f'Low confidence ({round(confidence, 4)}) - threshold is {MIN_CONFIDENCE}'
            }

            if explain:
                result['ambiguity_score'] = 0.9
                result['confidence_level'] = "Low"
                result['morphology_signal'] = None
                result['explanation'] = {
                    'why': ["Confidence below minimum threshold", "Insufficient data quality"],
                    'confidence_breakdown': {'overall': round(confidence, 4)},
                    'ambiguity_score': 0.9,
                    'confidence_level': "Low"
                }

            return result

        # Base result
        result = {
            'name': normalized,
            'country': top['country'],
            'country_name': top['country_name'],
            'confidence': round(confidence, 4),
            'region': top['region'],
            'language': top['language'],
            'top_countries': top_countries
        }

        if morphology_boost_applied:
            result['note'] = 'Morphology-based Turkish pattern detected'

        # v4.0.0: Add explainability features if requested
        if explain:
            # Calculate ambiguity score (Shannon entropy)
            probs = [c['probability'] for c in top_countries]
            ambiguity = ExplainabilityEngine.calculate_ambiguity_score(probs)

            # Detect morphological patterns
            morphology_signal = MorphologyEngine.get_morphological_signal(name, name_type)

            # Calculate confidence breakdown
            freq_strength = top['probability']
            morph_signal_strength = morphology_signal['pattern_confidence'] if morphology_signal else 0.0

            breakdown = ExplainabilityEngine.decompose_confidence(
                frequency_strength=freq_strength,
                cross_source_agreement=0.15 if len(top_countries) > 1 else 0.0,
                morphology_signal=morph_signal_strength,
                entropy_penalty=ambiguity * 0.3
            )

            # Generate full explanation
            morphology_patterns = [morphology_signal['primary_pattern']] if morphology_signal else None

            explanation = ExplainabilityEngine.generate_explanation(
                name=name,
                prediction=result,
                confidence_breakdown=breakdown,
                ambiguity_score=ambiguity,
                morphology_patterns=morphology_patterns,
                sources=["EthniData Database"]
            )

            # Add v4.0.0 fields to result
            result['ambiguity_score'] = round(ambiguity, 4)
            result['confidence_level'] = explanation['explanation']['confidence_level']
            result['morphology_signal'] = morphology_signal
            result['explanation'] = explanation['explanation']

        return result

    def predict_gender(
        self,
        name: str
    ) -> Dict:
        """
        Predict gender from first name

        Args:
            name: First name

        Returns:
            {
                'name': str,
                'gender': str ('M' or 'F' or None),
                'confidence': float,
                'distribution': {'M': prob, 'F': prob, None: prob}
            }
        """

        normalized = self.normalize_name(name)

        query = """
            SELECT gender, COUNT(*) as count
            FROM names
            WHERE name = ? AND name_type = 'first'
            GROUP BY gender
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (normalized,))
        results = cursor.fetchall()

        if not results:
            return {
                'name': normalized,
                'gender': None,
                'confidence': 0.0,
                'distribution': {}
            }

        # Count by gender
        gender_counts = {}
        total = 0

        for row in results:
            gender = row['gender']
            count = row['count']
            gender_counts[gender] = count
            total += count

        # Calculate probabilities
        distribution = {g: round(c / total, 4) for g, c in gender_counts.items()}

        # Top gender
        top_gender = max(gender_counts.items(), key=lambda x: x[1])[0]
        confidence = gender_counts[top_gender] / total

        return {
            'name': normalized,
            'gender': top_gender,
            'confidence': round(confidence, 4),
            'distribution': distribution
        }

    def predict_region(
        self,
        name: str,
        name_type: Literal["first", "last"] = "first"
    ) -> Dict:
        """
        Predict geographic region from name

        Args:
            name: First or last name
            name_type: "first" or "last"

        Returns:
            {
                'name': str,
                'region': str (Europe, Asia, Americas, Africa, Oceania, Other),
                'confidence': float,
                'distribution': {region: probability, ...}
            }
        """

        normalized = self.normalize_name(name)

        query = """
            SELECT region, COUNT(*) as total_freq
            FROM names
            WHERE name = ? AND name_type = ?
            GROUP BY region
            ORDER BY total_freq DESC
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (normalized, name_type))
        results = cursor.fetchall()

        if not results:
            return {
                'name': normalized,
                'region': None,
                'confidence': 0.0,
                'distribution': {}
            }

        total = sum(row['total_freq'] for row in results)

        distribution = {}
        for row in results:
            region = row['region']
            prob = row['total_freq'] / total
            distribution[region] = round(prob, 4)

        top_region = results[0]['region']
        confidence = results[0]['total_freq'] / total

        return {
            'name': normalized,
            'region': top_region,
            'confidence': round(confidence, 4),
            'distribution': distribution
        }

    def predict_language(
        self,
        name: str,
        name_type: Literal["first", "last"] = "first",
        top_n: int = 5
    ) -> Dict:
        """
        Predict most likely language from name

        Args:
            name: First or last name
            name_type: "first" or "last"
            top_n: Number of top predictions

        Returns:
            {
                'name': str,
                'language': str,
                'confidence': float,
                'top_languages': [{language, probability}, ...]
            }
        """

        normalized = self.normalize_name(name)

        query = """
            SELECT language, COUNT(*) as total_freq
            FROM names
            WHERE name = ? AND name_type = ? AND language IS NOT NULL
            GROUP BY language
            ORDER BY total_freq DESC
            LIMIT ?
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (normalized, name_type, top_n))
        results = cursor.fetchall()

        if not results:
            return {
                'name': normalized,
                'language': None,
                'confidence': 0.0,
                'top_languages': []
            }

        total = sum(row['total_freq'] for row in results)

        top_languages = []
        for row in results:
            lang = row['language']
            prob = row['total_freq'] / total
            top_languages.append({
                'language': lang,
                'probability': round(prob, 4)
            })

        return {
            'name': normalized,
            'language': top_languages[0]['language'],
            'confidence': top_languages[0]['probability'],
            'top_languages': top_languages
        }

    def predict_religion(
        self,
        name: str,
        name_type: Literal["first", "last"] = "first",
        top_n: int = 5
    ) -> Dict:
        """
        Predict religion from name - NEW in v1.3.0!

        Args:
            name: First or last name
            name_type: "first" or "last"
            top_n: Number of top predictions

        Returns:
            {
                'name': str,
                'religion': str (Christianity, Islam, Hinduism, Buddhism, Judaism),
                'confidence': float,
                'top_religions': [{religion, probability}, ...]
            }
        """

        normalized = self.normalize_name(name)

        query = """
            SELECT religion, COUNT(*) as total_freq
            FROM names
            WHERE name = ? AND name_type = ? AND religion IS NOT NULL
            GROUP BY religion
            ORDER BY total_freq DESC
            LIMIT ?
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (normalized, name_type, top_n))
        results = cursor.fetchall()

        if not results:
            return {
                'name': normalized,
                'religion': None,
                'confidence': 0.0,
                'top_religions': []
            }

        total = sum(row['total_freq'] for row in results)

        top_religions = []
        for row in results:
            religion = row['religion']
            prob = row['total_freq'] / total
            top_religions.append({
                'religion': religion,
                'probability': round(prob, 4)
            })

        return {
            'name': normalized,
            'religion': top_religions[0]['religion'],
            'confidence': top_religions[0]['probability'],
            'top_religions': top_religions
        }

    def predict_ethnicity(
        self,
        name: str,
        name_type: Literal["first", "last"] = "first"
    ) -> Dict:
        """Predict ethnicity from name (uses nationality as proxy)"""

        # Use nationality as ethnicity proxy since we don't have separate ethnicity data
        nationality = self.predict_nationality(name, name_type, top_n=1)

        return {
            'name': nationality['name'],
            'ethnicity': nationality['country_name'],  # Use country as ethnicity
            'country': nationality['country'],
            'country_name': nationality['country_name'],
            'region': nationality.get('region'),
            'language': nationality.get('language'),
            'confidence': nationality['confidence']
        }

    def predict_full_name(
        self,
        first_name: str,
        last_name: str,
        top_n: int = 5,
        explain: bool = False
    ) -> Dict:
        """
        Predict from full name (first + last) - ENHANCED v4.0.0

        Returns nationality, region, language

        Args:
            first_name: First name
            last_name: Last name
            top_n: Number of top predictions
            explain: If True, includes explainability layer (v4.0.0 NEW!)
        """

        first_pred = self.predict_nationality(first_name, "first", top_n=top_n, explain=False)
        last_pred = self.predict_nationality(last_name, "last", top_n=top_n, explain=False)

        # Combine scores
        combined_scores = {}

        for item in first_pred['top_countries']:
            combined_scores[item['country']] = {
                'score': item['probability'] * 0.4,
                'region': item['region'],
                'language': item['language']
            }

        for item in last_pred['top_countries']:
            if item['country'] in combined_scores:
                combined_scores[item['country']]['score'] += item['probability'] * 0.6
            else:
                combined_scores[item['country']] = {
                    'score': item['probability'] * 0.6,
                    'region': item['region'],
                    'language': item['language']
                }

        # Sort
        sorted_countries = sorted(
            combined_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )[:top_n]

        # Format
        top_countries = []
        for country_code, data in sorted_countries:
            try:
                country = pycountry.countries.get(alpha_3=country_code)
                country_name = country.name if country else country_code
            except:
                country_name = country_code

            top_countries.append({
                'country': country_code,
                'country_name': country_name,
                'region': data['region'],
                'language': data['language'],
                'probability': round(data['score'], 4)
            })

        top = top_countries[0] if top_countries else {}

        # Base result
        result = {
            'first_name': self.normalize_name(first_name),
            'last_name': self.normalize_name(last_name),
            'country': top.get('country'),
            'country_name': top.get('country_name'),
            'region': top.get('region'),
            'language': top.get('language'),
            'confidence': top.get('probability', 0.0),
            'top_countries': top_countries
        }

        # v4.0.0: Add explainability features if requested
        if explain:
            # Calculate ambiguity score
            probs = [c['probability'] for c in top_countries]
            ambiguity = ExplainabilityEngine.calculate_ambiguity_score(probs)

            # Detect morphological patterns in both names
            first_morph = MorphologyEngine.get_morphological_signal(first_name, "first")
            last_morph = MorphologyEngine.get_morphological_signal(last_name, "last")

            # Use last name morphology (stronger signal)
            morphology_signal = last_morph if last_morph else first_morph

            # Calculate confidence breakdown
            freq_strength = top.get('probability', 0.0)
            morph_signal_strength = morphology_signal['pattern_confidence'] if morphology_signal else 0.0

            breakdown = ExplainabilityEngine.decompose_confidence(
                frequency_strength=freq_strength,
                cross_source_agreement=0.20 if len(top_countries) > 1 else 0.0,
                morphology_signal=morph_signal_strength,
                entropy_penalty=ambiguity * 0.3
            )

            # Generate full explanation
            morphology_patterns = []
            if first_morph:
                morphology_patterns.append(f"{first_morph['primary_pattern']} (first)")
            if last_morph:
                morphology_patterns.append(f"{last_morph['primary_pattern']} (last)")

            explanation = ExplainabilityEngine.generate_explanation(
                name=f"{first_name} {last_name}",
                prediction=result,
                confidence_breakdown=breakdown,
                ambiguity_score=ambiguity,
                morphology_patterns=morphology_patterns if morphology_patterns else None,
                sources=["EthniData Database"]
            )

            # Add v4.0.0 fields
            result['ambiguity_score'] = round(ambiguity, 4)
            result['confidence_level'] = explanation['explanation']['confidence_level']
            result['morphology_signal'] = {
                'first_name': first_morph,
                'last_name': last_morph
            }
            result['explanation'] = explanation['explanation']

        return result

    def predict_all(
        self,
        name: str,
        name_type: Literal["first", "last"] = "first"
    ) -> Dict:
        """
        Predict ALL attributes at once - UPDATED v1.3.0
        Now includes: nationality, gender, region, language, religion, ethnicity

        Args:
            name: First or last name
            name_type: "first" or "last"

        Returns:
            {
                'name': str,
                'nationality': {...},
                'gender': {...},  # Only for first names
                'region': {...},
                'language': {...},
                'religion': {...},  # NEW in v1.3.0!
                'ethnicity': {...}
            }
        """

        normalized = self.normalize_name(name)

        result = {
            'name': normalized,
            'nationality': self.predict_nationality(name, name_type),
            'region': self.predict_region(name, name_type),
            'language': self.predict_language(name, name_type),
            'religion': self.predict_religion(name, name_type),  # NEW!
            'ethnicity': self.predict_ethnicity(name, name_type)
        }

        # Gender only for first names
        if name_type == "first":
            result['gender'] = self.predict_gender(name)

        return result

    def get_stats(self) -> Dict:
        """Get database statistics"""

        cursor = self.conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) as count FROM names WHERE name_type = 'first'")
        stats['total_first_names'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM names WHERE name_type = 'last'")
        stats['total_last_names'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(DISTINCT country_code) as count FROM names")
        stats['countries'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(DISTINCT region) as count FROM names WHERE region IS NOT NULL")
        stats['regions'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(DISTINCT language) as count FROM names WHERE language IS NOT NULL")
        stats['languages'] = cursor.fetchone()['count']

        return stats
