"""
Religious Names Database

Datasets for names associated with major world religions:
- Christianity: Biblical names, Saint names
- Islam: Quranic names, Sahaba names, 99 Names of Allah
- Judaism: Hebrew names, Torah names
- Hinduism: Names from Vedas, Puranas, Deities
- Buddhism: Buddhist scriptures, Pali/Sanskrit names
- Sikhism: Gurbani names, Sikh Gurus

Note: Religion is only a weak signal for ethnicity/nationality.
Use with caution and combine with other features.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class Religion(Enum):
    """Major world religions."""
    CHRISTIANITY = "christianity"
    ISLAM = "islam"
    JUDAISM = "judaism"
    HINDUISM = "hinduism"
    BUDDHISM = "buddhism"
    SIKHISM = "sikhism"
    UNKNOWN = "unknown"


@dataclass
class ReligiousNameRecord:
    """Religious name record."""
    name: str
    religion: Religion
    name_type: str  # "first" typically
    origin: str  # Source text (e.g., "Quran", "Bible", "Torah")
    gender: Optional[str] = None
    meaning: Optional[str] = None


class ReligiousNamesDatabase:
    """
    Database of religiously significant names.

    Data sources:
    - Public domain religious texts
    - Saint calendars (Catholic, Orthodox)
    - Islamic name lists (Sahaba, Companions)
    - Hebrew name databases
    - Hindu deity/epic names (Mahabharata, Ramayana)
    - Buddhist Jataka tales
    - Sikh Gurbani names
    """

    def __init__(self):
        """Initialize religious names database."""
        self._load_databases()

    def _load_databases(self):
        """Load built-in religious name databases."""
        # These would ideally be loaded from curated CSV files
        # For now, we provide representative examples

        self.christian_names = {
            # Biblical names
            "Abraham": ("M", "Bible - Genesis"),
            "Sarah": ("F", "Bible - Genesis"),
            "Moses": ("M", "Bible - Exodus"),
            "Mary": ("F", "Bible - New Testament"),
            "Joseph": ("M", "Bible - Old & New Testament"),
            "Jesus": ("M", "Bible - New Testament"),
            # Saint names
            "Francis": ("M", "Saint Francis of Assisi"),
            "Theresa": ("F", "Saint Teresa of Ávila"),
            "Christopher": ("M", "Saint Christopher"),
            "Catherine": ("F", "Saint Catherine"),
        }

        self.islamic_names = {
            # Quranic names
            "Muhammad": ("M", "Prophet Muhammad (PBUH)"),
            "Ali": ("M", "Imam Ali"),
            "Fatima": ("F", "Fatima al-Zahra"),
            "Hassan": ("M", "Imam Hassan"),
            "Hussain": ("M", "Imam Hussain"),
            "Aisha": ("F", "Aisha bint Abi Bakr"),
            "Khadija": ("F", "Khadija bint Khuwaylid"),
            "Omar": ("M", "Omar ibn al-Khattab"),
            "Ibrahim": ("M", "Prophet Abraham (Quranic)"),
            "Maryam": ("F", "Mary (Quranic)"),
        }

        self.jewish_names = {
            # Hebrew/Torah names
            "David": ("M", "King David - Torah"),
            "Solomon": ("M", "King Solomon - Torah"),
            "Rebecca": ("F", "Rebecca - Torah"),
            "Rachel": ("F", "Rachel - Torah"),
            "Jacob": ("M", "Jacob - Torah"),
            "Isaac": ("M", "Isaac - Torah"),
            "Miriam": ("F", "Miriam - Torah"),
            "Aaron": ("M", "Aaron - Torah"),
        }

        self.hindu_names = {
            # Deity names
            "Krishna": ("M", "Lord Krishna - Mahabharata"),
            "Rama": ("M", "Lord Rama - Ramayana"),
            "Sita": ("F", "Sita - Ramayana"),
            "Lakshmi": ("F", "Goddess Lakshmi"),
            "Ganesh": ("M", "Lord Ganesha"),
            "Durga": ("F", "Goddess Durga"),
            "Arjuna": ("M", "Arjuna - Mahabharata"),
            "Radha": ("F", "Radha - Krishna's consort"),
        }

        self.buddhist_names = {
            # Buddhist scriptures
            "Buddha": ("M", "Gautama Buddha"),
            "Ananda": ("M", "Ananda - Buddha's disciple"),
            "Bodhi": ("U", "Enlightenment"),
            "Tara": ("F", "Goddess Tara"),
            "Manjushri": ("M", "Bodhisattva of Wisdom"),
        }

        self.sikh_names = {
            # Sikh Gurus and Gurbani
            "Nanak": ("M", "Guru Nanak Dev Ji"),
            "Gobind": ("M", "Guru Gobind Singh Ji"),
            "Angad": ("M", "Guru Angad Dev Ji"),
            "Amar": ("M", "Guru Amar Das Ji"),
            "Harpreet": ("U", "Gurbani name - God's Love"),
            "Simran": ("F", "Gurbani name - Meditation"),
        }

    def get_names_by_religion(self, religion: Religion) -> List[ReligiousNameRecord]:
        """
        Get all names for a specific religion.

        Args:
            religion: Religion enum value

        Returns:
            List of ReligiousNameRecord objects
        """
        records = []

        if religion == Religion.CHRISTIANITY:
            source_dict = self.christian_names
        elif religion == Religion.ISLAM:
            source_dict = self.islamic_names
        elif religion == Religion.JUDAISM:
            source_dict = self.jewish_names
        elif religion == Religion.HINDUISM:
            source_dict = self.hindu_names
        elif religion == Religion.BUDDHISM:
            source_dict = self.buddhist_names
        elif religion == Religion.SIKHISM:
            source_dict = self.sikh_names
        else:
            return []

        for name, (gender, origin) in source_dict.items():
            records.append(ReligiousNameRecord(
                name=name,
                religion=religion,
                name_type="first",
                origin=origin,
                gender=gender
            ))

        return records

    def infer_religion(self, name: str) -> Optional[Religion]:
        """
        Infer possible religion from name (weak signal!).

        Args:
            name: Name to analyze

        Returns:
            Religion enum or None
        """
        name_lower = name.lower()

        # Check each religion's database
        if name in self.islamic_names:
            return Religion.ISLAM
        if name in self.christian_names:
            return Religion.CHRISTIANITY
        if name in self.jewish_names:
            return Religion.JUDAISM
        if name in self.hindu_names:
            return Religion.HINDUISM
        if name in self.buddhist_names:
            return Religion.BUDDHISM
        if name in self.sikh_names:
            return Religion.SIKHISM

        return None

    def get_all_names(self) -> Dict[Religion, List[ReligiousNameRecord]]:
        """
        Get all religious names organized by religion.

        Returns:
            Dictionary mapping Religion to list of records
        """
        all_names = {}

        for religion in [
            Religion.CHRISTIANITY,
            Religion.ISLAM,
            Religion.JUDAISM,
            Religion.HINDUISM,
            Religion.BUDDHISM,
            Religion.SIKHISM
        ]:
            all_names[religion] = self.get_names_by_religion(religion)

        return all_names

    def to_ethnidata_format(
        self,
        religion: Optional[Religion] = None
    ) -> List[Dict]:
        """
        Convert religious names to EthniData-compatible format.

        Note: We use "XX" as country code since religion != nationality.
        This data should be used as a feature, not primary prediction.

        Args:
            religion: Specific religion to export, or None for all

        Returns:
            List of dictionaries with EthniData schema
        """
        ethni_records = []

        if religion:
            records = self.get_names_by_religion(religion)
        else:
            all_names = self.get_all_names()
            records = [r for records_list in all_names.values() for r in records_list]

        for record in records:
            ethni_records.append({
                "name": record.name,
                "name_type": record.name_type,
                "country": "XX",  # Religion-based, not country-specific
                "gender": record.gender or "U",
                "frequency": 1,
                "source": f"religious_{record.religion.value}",
                "metadata": {
                    "religion": record.religion.value,
                    "origin": record.origin
                }
            })

        return ethni_records


# Example usage
if __name__ == "__main__":
    db = ReligiousNamesDatabase()

    # Get Islamic names
    islamic_names = db.get_names_by_religion(Religion.ISLAM)
    print(f"🕌 Islamic Names ({len(islamic_names)}):")
    for record in islamic_names[:5]:
        print(f"   {record.name} ({record.gender}): {record.origin}")

    # Get Christian names
    christian_names = db.get_names_by_religion(Religion.CHRISTIANITY)
    print(f"\n✝️  Christian Names ({len(christian_names)}):")
    for record in christian_names[:5]:
        print(f"   {record.name} ({record.gender}): {record.origin}")

    # Infer religion
    test_names = ["Muhammad", "Mary", "David", "Krishna", "Buddha"]
    print(f"\n🔍 Religion Inference:")
    for name in test_names:
        religion = db.infer_religion(name)
        print(f"   {name}: {religion.value if religion else 'Unknown'}")

    # Convert to EthniData format
    ethni_records = db.to_ethnidata_format(Religion.ISLAM)
    print(f"\n✅ Converted {len(ethni_records)} Islamic names to EthniData format")
