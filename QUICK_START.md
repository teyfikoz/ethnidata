# 🚀 EthniData - Hızlı Başlangıç

## 📍 Şu An Neredesiniz

Proje klasörü: `/Users/teyfikoz/Downloads/NBD/ethnidata`

## ✅ Yapılması Gerekenler (Sırayla)

### 1️⃣ GitHub'a Yükle (5 dakika)

```bash
cd /Users/teyfikoz/Downloads/NBD/ethnidata

# Git başlat
git init
git add .
git commit -m "Initial commit: EthniData v1.0.0"

# GitHub'a bağlan
git remote add origin https://github.com/teyfikoz/ethnidata.git
git branch -M main
git push -u origin main
```

**Not:** GitHub repo önce oluşturulmalı:
1. https://github.com/new
2. Repository name: `ethnidata`
3. Public seç
4. **Initialize with README** - İŞARETLEME (bizde var)
5. Create repository

### 2️⃣ PyPI'ye Yükle (10 dakika)

```bash
# Araçları kur
pip install --upgrade build twine

# Build et
python -m build

# PyPI'ye yükle
twine upload dist/*
```

**Sorulacak bilgiler:**
- Username: `__token__`
- Password: PyPI token'ınız (pypi-... ile başlıyor)

**PyPI Token nasıl alınır:**
1. https://pypi.org (giriş yap: teyfikoz)
2. Account settings → API tokens
3. "Add API token"
4. Token name: "EthniData"
5. Scope: "Entire account"
6. Create token → KOPYALA

### 3️⃣ Test Et (2 dakika)

```bash
# Yeni klasör
cd ~
mkdir test_ethnidata
cd test_ethnidata

# Virtual env
python -m venv venv
source venv/bin/activate

# PyPI'den yükle
pip install ethnidata

# Test
python
>>> from ethnidata import EthniData
>>> ed = EthniData()
```

**NOT:** İlk test'te "Database not found" hatası alacaksınız. Bu normal!

### 4️⃣ Veritabanını Oluştur (20-30 dakika)

```bash
cd /Users/teyfikoz/Downloads/NBD/ethnidata

# Bağımlılıklar
pip install -r requirements.txt

# Veri toplama (sırayla çalıştır)
cd scripts
python 1_fetch_names_dataset.py      # ~2 dakika
python 2_fetch_wikipedia.py          # ~10 dakika
python 3_fetch_olympics.py           # ~1 dakika
python 4_fetch_phone_directories.py  # ~2 dakika
python 5_merge_all_data.py           # ~2 dakika
python 6_create_database.py          # ~5 dakika
```

Veritabanı oluşturuldu: `ethnidata/ethnidata.db`

### 5️⃣ Veritabanı Boyutunu Kontrol Et

```bash
cd ..
ls -lh ethnidata/ethnidata.db
```

**Eğer <50MB ise:**
```bash
# Yeni version yap
# setup.py ve pyproject.toml: version = "1.0.1"
sed -i '' 's/version = "1.0.0"/version = "1.0.1"/' setup.py
sed -i '' 's/version = "1.0.0"/version = "1.0.1"/' pyproject.toml

# Yeni build
rm -rf dist/
python -m build

# PyPI'ye yükle
twine upload dist/*
```

**Eğer >50MB ise:**
GitHub Release oluştur:
1. https://github.com/teyfikoz/ethnidata/releases
2. "Create a new release"
3. Tag: v1.0.0
4. Title: "EthniData v1.0.0"
5. `ethnidata.db` dosyasını upload et
6. Publish release

Sonra `ethnidata/__init__.py` dosyasını güncelle (otomatik indirme için):
```python
# Dosyanın başına ekle
from pathlib import Path
import requests

DB_PATH = Path(__file__).parent / "ethnidata.db"
DB_URL = "https://github.com/teyfikoz/ethnidata/releases/download/v1.0.0/ethnidata.db"

def ensure_database():
    if not DB_PATH.exists():
        print("📥 Downloading database (first time, ~50MB)...")
        r = requests.get(DB_URL, stream=True)
        r.raise_for_status()
        with open(DB_PATH, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        print("✅ Database ready!")

ensure_database()

# Geri kalan kod...
```

## 📊 Kullanım Örnekleri

```python
from ethnidata import EthniData

ed = EthniData()

# Tek isim
print(ed.predict_nationality("Ahmet"))

# Tam isim
print(ed.predict_full_name("Tefik", "Oz"))

# Etnisite
print(ed.predict_ethnicity("Muhammad"))

# İstatistikler
print(ed.get_stats())
```

## 🔗 Linkler

- **PyPI**: https://pypi.org/project/ethnidata/
- **GitHub**: https://github.com/teyfikoz/ethnidata
- **Downloads**: https://pypistats.org/packages/ethnidata

## ❓ Sorun mu Var?

Detaylı talimatlar için:
- `GITHUB_PYPI_GUIDE.md` - Adım adım rehber
- `PUBLISH.md` - PyPI yayınlama kılavuzu
- `README.md` - Genel dokümantasyon

## ✅ Checklist

- [ ] GitHub repo oluşturuldu
- [ ] Kod GitHub'a yüklendi
- [ ] PyPI token alındı
- [ ] `python -m build` çalıştı
- [ ] PyPI'ye yüklendi
- [ ] Veritabanı oluşturuldu
- [ ] Veritabanı boyutu kontrol edildi
- [ ] Veritabanı PyPI'ye eklendi VEYA GitHub Release'de
- [ ] Final test yapıldı: `pip install ethnidata`

Başarılar! 🎉
