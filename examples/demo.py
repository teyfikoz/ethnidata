#!/usr/bin/env python3
"""
EthniData Database Demo
Örnek kullanımlar
"""

from ethnidata import EthniData

def main():
    print("🌍 EthniData (Name-Based Demographics) Database Demo\n")

    # EthniData instance
    ed = EthniData()

    # Stats
    print("📊 Database Statistics:")
    stats = ed.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value:,}")

    print("\n" + "="*60 + "\n")

    # Test cases
    test_cases = [
        ("Ahmet", "first", "Turkish name"),
        ("Yılmaz", "last", "Turkish surname"),
        ("Muhammad", "first", "Arabic name"),
        ("Chen", "last", "Chinese surname"),
        ("Tanaka", "last", "Japanese surname"),
        ("Smith", "last", "English surname"),
        ("Garcia", "last", "Spanish surname"),
        ("Müller", "last", "German surname"),
        ("Ivanov", "last", "Russian surname"),
        ("Kim", "last", "Korean surname"),
    ]

    print("🔍 Name Nationality Predictions:\n")

    for name, name_type, description in test_cases:
        result = ed.predict_nationality(name, name_type=name_type, top_n=3)

        print(f"📝 {name} ({description})")
        print(f"   → Top prediction: {result['country_name']} ({result['country']}) - {result['confidence']:.2%}")

        if len(result['top_countries']) > 1:
            print(f"   → Other possibilities:")
            for country in result['top_countries'][1:]:
                print(f"      • {country['country_name']}: {country['probability']:.2%}")

        print()

    print("="*60 + "\n")

    # Full name predictions
    print("👤 Full Name Predictions:\n")

    full_names = [
        ("Mehmet", "Yılmaz", "Turkish"),
        ("John", "Smith", "English"),
        ("Wei", "Chen", "Chinese"),
        ("Maria", "Garcia", "Spanish"),
        ("Yuki", "Tanaka", "Japanese"),
    ]

    for first, last, description in full_names:
        result = ed.predict_full_name(first, last, top_n=3)

        print(f"👤 {first} {last} ({description})")
        print(f"   → Predicted: {result['country_name']} ({result['country']}) - {result['confidence']:.2%}")

        if len(result['top_countries']) > 1:
            print(f"   → Alternatives:")
            for country in result['top_countries'][1:]:
                print(f"      • {country['country_name']}: {country['probability']:.2%}")

        print()

    print("="*60 + "\n")

    # Ethnicity predictions
    print("🧬 Ethnicity Predictions:\n")

    ethnicity_tests = [
        ("Muhammad", "first"),
        ("Wei", "first"),
        ("Yuki", "first"),
    ]

    for name, name_type in ethnicity_tests:
        result = ed.predict_ethnicity(name, name_type=name_type)

        print(f"🧬 {name}")
        print(f"   → Ethnicity: {result.get('ethnicity', 'Unknown')}")
        print(f"   → Country: {result.get('country_name', 'Unknown')} ({result.get('country', '?')})")
        print()

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Please run the following steps first:")
        print("   1. pip install -r requirements.txt")
        print("   2. cd scripts && python 1_fetch_names_dataset.py")
        print("   3. python 2_fetch_wikipedia.py")
        print("   4. python 3_fetch_olympics.py")
        print("   5. python 4_fetch_phone_directories.py")
        print("   6. python 5_merge_all_data.py")
        print("   7. python 6_create_database.py")
