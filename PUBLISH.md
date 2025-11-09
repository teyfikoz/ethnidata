# PyPI'ye Yayınlama Kılavuzu

## 📋 Ön Hazırlık

### 1. PyPI Hesabı Oluştur
- Production: https://pypi.org/account/register/
- Test: https://test.pypi.org/account/register/

### 2. API Token Al
1. PyPI'ye giriş yap
2. Account Settings → API tokens
3. "Add API token" → Scope: "Entire account"
4. Token'ı kopyala (sadece bir kez gösterilir!)

### 3. `.pypirc` Dosyası Oluştur (Opsiyonel ama Önerilen)

```bash
nano ~/.pypirc
```

İçeriği:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

Güvenlik:
```bash
chmod 600 ~/.pypirc
```

## 🛠️ Build Süreci

### 1. Gerekli Araçları Kur
```bash
pip install --upgrade build twine
```

### 2. Veritabanını Oluştur (ÖNEMLİ!)
```bash
cd scripts
python 1_fetch_names_dataset.py
python 2_fetch_wikipedia.py
python 3_fetch_olympics.py
python 4_fetch_phone_directories.py
python 5_merge_all_data.py
python 6_create_database.py
cd ..
```

**NOT:** Veritabanı boyutu çok büyükse (>100MB), PyPI'ye yüklemek yerine:
- Alternatif 1: GitHub Releases'da host et
- Alternatif 2: İlk çalıştırmada otomatik indir
- Alternatif 3: CDN kullan

### 3. Eski Build'leri Temizle
```bash
rm -rf dist/ build/ *.egg-info
```

### 4. Paketi Build Et
```bash
python -m build
```

Bu komut şunları oluşturur:
- `dist/nbd-database-1.0.0.tar.gz` (source distribution)
- `dist/nbd_database-1.0.0-py3-none-any.whl` (wheel)

### 5. Build'i Kontrol Et
```bash
twine check dist/*
```

## 🧪 Test (TestPyPI)

### 1. TestPyPI'ye Yükle
```bash
twine upload --repository testpypi dist/*
```

veya token ile manuel:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Username: __token__
# Password: your-testpypi-token
```

### 2. Test Et
```bash
# Yeni virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# TestPyPI'den yükle
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nbd-database

# Test et
python -c "from nbd import NBD; print('Success!')"
```

## 🚀 Production Yayını (PyPI)

### 1. Versiyon Kontrol
`setup.py` ve `pyproject.toml` dosyalarında version numarasını kontrol et:
```python
version = "1.0.0"
```

### 2. PyPI'ye Yükle
```bash
twine upload dist/*
```

veya manuel:
```bash
twine upload dist/*
# Username: __token__
# Password: your-pypi-token
```

### 3. Doğrula
```bash
# Yeni environment
python -m venv prod_test
source prod_test/bin/activate

# PyPI'den yükle
pip install nbd-database

# Test et
python
>>> from nbd import NBD
>>> nbd = NBD()
>>> nbd.predict_nationality("Ahmet")
```

### 4. PyPI Sayfasını Kontrol Et
https://pypi.org/project/nbd-database/

## 📦 Veritabanı Sorunu Çözümü

Veritabanı çok büyükse:

### Çözüm 1: İlk Çalıştırmada İndir

`nbd/__init__.py` güncelle:
```python
from pathlib import Path
import requests

DB_URL = "https://github.com/YOURUSERNAME/nbd-database/releases/download/v1.0.0/nbd_database.db"
DB_PATH = Path(__file__).parent / "nbd_database.db"

def ensure_database():
    if not DB_PATH.exists():
        print("Downloading database (first time only)...")
        response = requests.get(DB_URL)
        DB_PATH.write_bytes(response.content)
        print("Database downloaded!")

ensure_database()
from .predictor import NBD
```

### Çözüm 2: Küçük Veritabanı Oluştur

`scripts/6_create_database.py` modifiye et:
- Sadece en yaygın 10K isim
- Sadece top 50 ülke
- Compressed SQLite (VACUUM)

### Çözüm 3: Ayrı Data Paketi

```bash
# Ana paket: nbd-database (sadece kod)
# Data paketi: nbd-database-data (sadece DB)
pip install nbd-database
pip install nbd-database-data  # opsiyonel
```

## 🔄 Güncelleme Yayını

```bash
# 1. Versiyon numarasını artır
# setup.py ve pyproject.toml: version = "1.0.1"

# 2. CHANGELOG.md güncelle

# 3. Build et
rm -rf dist/ build/ *.egg-info
python -m build

# 4. Yükle
twine upload dist/*
```

## ❌ Sorun Giderme

### "File already exists"
PyPI'de aynı versiyon tekrar yüklenemez. Çözüm:
```bash
# Versiyon numarasını artır
version = "1.0.1"
```

### "Invalid distribution"
```bash
# Build'i kontrol et
twine check dist/*

# setup.py validasyon
python setup.py check
```

### "Long description failed"
README.md formatı hatalı:
```bash
pip install readme-renderer
python -m readme_renderer README.md
```

### "Authentication failed"
Token yanlış:
```bash
# Yeni token al ve .pypirc'yi güncelle
```

## 📊 PyPI İstatistikleri

Yayından sonra:
- Download stats: https://pypistats.org/packages/nbd-database
- Badge ekle README'ye:

```markdown
[![PyPI version](https://badge.fury.io/py/nbd-database.svg)](https://badge.fury.io/py/nbd-database)
[![Downloads](https://pepy.tech/badge/nbd-database)](https://pepy.tech/project/nbd-database)
```

## ✅ Checklist

Yayından önce:
- [ ] README.md eksiksiz
- [ ] LICENSE dosyası var
- [ ] Veritabanı oluşturuldu (veya alternatif çözüm)
- [ ] Testler geçiyor (`pytest tests/`)
- [ ] Versiyon numarası doğru
- [ ] `python -m build` çalışıyor
- [ ] `twine check dist/*` başarılı
- [ ] TestPyPI'de test edildi
- [ ] PyPI token hazır

Yayından sonra:
- [ ] `pip install nbd-database` test edildi
- [ ] PyPI sayfası kontrol edildi
- [ ] README'de badges güncellendi
- [ ] GitHub'da release oluşturuldu (opsiyonel)
