#!/usr/bin/env python3
"""
Sentetik Veri Üretimi
Mevcut veriden pattern'ler çıkararak yeni isimler üret

Metodlar:
1. Name variations (José → Jose, Joseph, Josef)
2. Gender inference (erkek/kadın isimleri ayır)
3. Regional patterns (Avrupa sonekleri: -son, -sen, -sson)
4. Transliteration (Кирилл → Kirill, محمد → Muhammad)
"""

import pandas as pd
from pathlib import Path
from collections import Counter, defaultdict
import re

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Regional name patterns
REGIONAL_PATTERNS = {
    'scandinavian': {
        'suffixes': ['son', 'sen', 'sson', 'dottir'],
        'prefixes': ['anders', 'lars', 'erik', 'sven', 'olaf'],
    },
    'slavic': {
        'suffixes': ['ov', 'ova', 'ev', 'eva', 'ski', 'sky', 'ic', 'vich'],
        'prefixes': ['ivan', 'dmitri', 'vladimir', 'boris'],
    },
    'arabic': {
        'prefixes': ['abd', 'al', 'abu', 'bin'],
        'suffixes': ['ullah', 'din', 'rahman'],
    },
    'hispanic': {
        'suffixes': ['ez', 'es', 'az', 'iz'],
        'prefixes': ['de', 'del', 'la'],
    },
    'asian': {
        'patterns': ['wang', 'li', 'chen', 'zhang', 'kim', 'park'],
    }
}

# Common name variations
NAME_VARIATIONS = {
    'john': ['jon', 'johann', 'johannes', 'giovanni', 'juan', 'jean', 'ian', 'sean'],
    'mary': ['maria', 'marie', 'marija', 'maryam', 'maria'],
    'michael': ['mikhail', 'miguel', 'michele', 'mikael'],
    'alexander': ['aleksandr', 'alejandro', 'alexandru', 'alex'],
    'joseph': ['jose', 'giuseppe', 'josef', 'yosef'],
    'william': ['wilhelm', 'guillermo', 'willem'],
    'peter': ['pietro', 'pedro', 'petr', 'piotr'],
    'paul': ['pablo', 'paolo', 'pavel'],
}

def generate_name_variations(base_names):
    """Mevcut isimlerden varyasyonlar üret"""
    print("🔄 İsim varyasyonları üretiliyor...")

    variations = []

    for base_name in base_names:
        base_lower = base_name.lower()

        # Bilinen varyasyonlar
        if base_lower in NAME_VARIATIONS:
            for variant in NAME_VARIATIONS[base_lower]:
                variations.append({
                    'original': base_name,
                    'variation': variant,
                    'type': 'known_variation'
                })

        # Basit transformasyonlar
        # -a ile biten → -o (Maria → Mario)
        if base_name.endswith('a'):
            variations.append({
                'original': base_name,
                'variation': base_name[:-1] + 'o',
                'type': 'gender_swap'
            })

        # -o ile biten → -a (Mario → Maria)
        elif base_name.endswith('o'):
            variations.append({
                'original': base_name,
                'variation': base_name[:-1] + 'a',
                'type': 'gender_swap'
            })

    print(f"  ✓ {len(variations):,} varyasyon üretildi")
    return pd.DataFrame(variations)

def generate_patronymic_names(first_names, patterns):
    """Patronimik isimler üret (İskandinavya, Rusya)"""
    print("\n👨‍👦 Patronimik isimler üretiliyor...")

    patronymics = []

    for name in first_names[:1000]:  # İlk 1000 isim
        name_lower = name.lower()

        # Scandinavian -son, -sen
        for suffix in ['son', 'sen', 'sson']:
            patronymics.append({
                'base_name': name,
                'patronymic': name + suffix,
                'region': 'Scandinavia',
                'pattern': f'-{suffix}'
            })

        # Slavic -ovich, -evich
        for suffix in ['ovich', 'evich', 'ovna', 'evna']:
            patronymics.append({
                'base_name': name,
                'patronymic': name + suffix,
                'region': 'Slavic',
                'pattern': f'-{suffix}'
            })

    print(f"  ✓ {len(patronymics):,} patronimik isim üretildi")
    return pd.DataFrame(patronymics)

def infer_missing_genders(names_df):
    """Cinsiyet bilgisi eksik isimlere tahmin ekle"""
    print("\n⚧️ Cinsiyet tahmini yapılıyor...")

    # Yaygın erkek/kadın sonekleri
    male_endings = ['o', 'os', 'us', 'is', 'an', 'en', 'ar', 'or', 'n']
    female_endings = ['a', 'ia', 'ina', 'ella', 'ette', 'ie', 'y', 'e']

    def infer_gender(name):
        if pd.isna(name):
            return None

        name_lower = str(name).lower()

        for ending in female_endings:
            if name_lower.endswith(ending):
                return 'F'

        for ending in male_endings:
            if name_lower.endswith(ending):
                return 'M'

        return None

    # Gender eksik olanlara tahmin ekle
    if 'gender' in names_df.columns:
        mask = names_df['gender'].isna()
        names_df.loc[mask, 'gender_inferred'] = names_df.loc[mask, 'name'].apply(infer_gender)
    else:
        names_df['gender_inferred'] = names_df['name'].apply(infer_gender)

    inferred_count = names_df['gender_inferred'].notna().sum()
    print(f"  ✓ {inferred_count:,} isim için cinsiyet tahmin edildi")

    return names_df

def generate_transliterations():
    """Yaygın transliterasyonlar üret"""
    print("\n🔤 Transliterasyon örnekleri...")

    # Cyrillic → Latin
    cyrillic_latin = {
        'Александр': 'Alexander',
        'Дмитрий': 'Dmitry',
        'Владимир': 'Vladimir',
        'Екатерина': 'Ekaterina',
        'Мария': 'Maria',
        'Иван': 'Ivan',
    }

    # Arabic → Latin
    arabic_latin = {
        'محمد': 'Muhammad',
        'علي': 'Ali',
        'فاطمة': 'Fatima',
        'أحمد': 'Ahmed',
    }

    transliterations = []

    for orig, latin in {**cyrillic_latin, **arabic_latin}.items():
        transliterations.append({
            'original': orig,
            'transliteration': latin,
            'script': 'Cyrillic' if ord(orig[0]) > 1000 else 'Arabic'
        })

    print(f"  ✓ {len(transliterations)} transliterasyon")
    return pd.DataFrame(transliterations)

def analyze_existing_patterns():
    """Mevcut verideki pattern'leri analiz et"""
    print("\n📊 Mevcut veri pattern analizi...")

    all_names = []

    # Olympics'ten isimler
    olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
    if olympics_file.exists():
        df = pd.read_csv(olympics_file)
        all_names.extend(df['first_name'].dropna().tolist())
        all_names.extend(df['last_name'].dropna().tolist())

    # Sonekleri analiz et
    suffix_counter = Counter()
    for name in all_names:
        if isinstance(name, str) and len(name) > 3:
            suffix_counter[name[-2:].lower()] += 1
            suffix_counter[name[-3:].lower()] += 1

    print(f"  → Analiz edilen isim: {len(all_names):,}")
    print(f"  → En yaygın sonekler:")
    for suffix, count in suffix_counter.most_common(15):
        print(f"     -{suffix}: {count:,}")

    return suffix_counter

def main():
    print("=" * 70)
    print("SENTETİK VERİ ÜRETİMİ")
    print("=" * 70)

    # 1. Pattern analizi
    patterns = analyze_existing_patterns()

    # 2. Mevcut isimlerden sample al
    olympics_file = RAW_DIR / "olympics" / "olympics_names.csv"
    sample_names = []

    if olympics_file.exists():
        df = pd.read_csv(olympics_file)
        sample_names = df['first_name'].dropna().unique()[:5000]

    # 3. Varyasyonlar üret
    variations_df = generate_name_variations(sample_names)
    variations_df.to_csv(OUTPUT_DIR / 'name_variations.csv', index=False)

    # 4. Patronimik isimler
    patronymic_df = generate_patronymic_names(sample_names, patterns)
    patronymic_df.to_csv(OUTPUT_DIR / 'patronymic_names.csv', index=False)

    # 5. Transliterasyonlar
    trans_df = generate_transliterations()
    trans_df.to_csv(OUTPUT_DIR / 'transliterations.csv', index=False)

    # 6. Gender inference
    if olympics_file.exists():
        df = pd.read_csv(olympics_file)
        df_with_gender = infer_missing_genders(df)
        df_with_gender.to_csv(OUTPUT_DIR / 'olympics_with_inferred_gender.csv', index=False)

    # Toplam
    total_synthetic = len(variations_df) + len(patronymic_df) + len(trans_df)

    print("\n" + "=" * 70)
    print(f"✅ TOPLAM SENTETİK VERİ: {total_synthetic:,} kayıt")
    print("=" * 70)
    print(f"\n📁 Kaydedilen dosyalar:")
    print(f"  - name_variations.csv: {len(variations_df):,}")
    print(f"  - patronymic_names.csv: {len(patronymic_df):,}")
    print(f"  - transliterations.csv: {len(trans_df):,}")

    return total_synthetic

if __name__ == "__main__":
    main()
