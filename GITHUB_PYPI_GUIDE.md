# 🚀 GitHub ve PyPI Yükleme Rehberi

## Kullanıcı: teyfikoz
## Kütüphane: ethnidata

---

## 📦 Adım 1: GitHub Repository Oluştur

### 1.1 GitHub'a Git
https://github.com/new

### 1.2 Repository Bilgileri
- **Repository name**: `ethnidata`
- **Description**: "Predict nationality, ethnicity, and demographics from names"
- **Public** seç (önerilen) veya Private
- ❌ **Initialize with README** - İŞARETLEME (bizde zaten var)
- ❌ **Add .gitignore** - İŞARETLEME (bizde var)
- ❌ **Choose a license** - İŞARETLEME (bizde var)

### 1.3 "Create repository" butonuna tıkla

---

## 📤 Adım 2: GitHub'a Yükle

```bash
# Terminal'de proje klasörüne git
cd /Users/teyfikoz/Downloads/NBD/nbd_database

# Git başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: EthniData v1.0.0"

# GitHub'ı remote olarak ekle
git remote add origin https://github.com/teyfikoz/ethnidata.git

# Ana branch'i main yap (opsiyonel)
git branch -M main

# GitHub'a push et
git push -u origin main
```

### GitHub Kullanıcı Adı/Şifre İstenirse:
- **Username**: teyfikoz
- **Password**: GitHub Personal Access Token (aşağıda nasıl alınır)

### GitHub Token Oluşturma (şifre yerine):
1. https://github.com/settings/tokens
2. "Generate new token" → "Generate new token (classic)"
3. **Note**: "EthniData Upload"
4. **Expiration**: 90 days (veya istediğin)
5. **Select scopes**:
   - ✅ repo (tüm repo checkbox'ları)
6. "Generate token" butonuna tıkla
7. Token'ı KOPYALA (bir daha gösterilmez!)
8. Git push yaparken şifre yerine bu token'ı kullan

---

## 🐍 Adım 3: PyPI'ye Yükle

### 3.1 PyPI Hesabı Kontrol
- https://pypi.org/account/login/
- Kullanıcı adın: **teyfikoz**
- Şifren zaten biliyorsun

### 3.2 PyPI API Token Al

1. PyPI'ye giriş yap: https://pypi.org
2. Account settings → API tokens
3. "Add API token" butonuna tıkla
4. **Token name**: "EthniData Upload"
5. **Scope**: "Entire account (all projects)" seç
6. "Create token" butonuna tıkla
7. Token'ı KOPYALA (pypi-... ile başlıyor)

### 3.3 Gerekli Araçları Kur

```bash
pip install --upgrade build twine
```

### 3.4 Paketi Build Et

```bash
# Proje klasöründe
cd /Users/teyfikoz/Downloads/NBD/nbd_database

# Eski build'leri temizle
rm -rf dist/ build/ *.egg-info

# Yeni build
python -m build
```

Bu komut şunları oluşturur:
- `dist/ethnidata-1.0.0.tar.gz`
- `dist/ethnidata-1.0.0-py3-none-any.whl`

### 3.5 Build'i Kontrol Et

```bash
twine check dist/*
```

✅ Çıktı: "Checking distribution dist/ethnidata-... : PASSED"

### 3.6 TestPyPI'de Dene (Opsiyonel ama Önerilir)

TestPyPI hesabı oluştur: https://test.pypi.org/account/register/

```bash
twine upload --repository testpypi dist/*
```

Sorulan bilgiler:
- **Username**: `__token__` (tam olarak böyle yaz)
- **Password**: (TestPyPI token'ını yapıştır)

Test et:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ethnidata
```

### 3.7 GERÇEK PyPI'ye Yükle

```bash
twine upload dist/*
```

Sorulan bilgiler:
- **Username**: `__token__` (tam olarak böyle yaz)
- **Password**: (PyPI token'ını yapıştır - pypi-... ile başlıyor)

✅ **BAŞARILI!** Çıktı: "View at: https://pypi.org/project/ethnidata/"

---

## ✅ Adım 4: Doğrulama

### 4.1 PyPI'de Kontrol Et
https://pypi.org/project/ethnidata/

### 4.2 Yükleme Testi

```bash
# Yeni bir klasörde
cd ~
mkdir test_ethnidata
cd test_ethnidata

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Mac/Linux
# veya Windows: venv\Scripts\activate

# PyPI'den yükle
pip install ethnidata

# Test et
python
>>> from ethnidata import EthniData
>>> ed = EthniData()
# Hata alacaksın çünkü veritabanı yok (sonraki adımda çözeceğiz)
```

---

## ⚠️ Adım 5: Veritabanı Sorunu Çözümü

Veritabanı dosyası çok büyük olabilir (PyPI limiti ~100MB). İki seçenek:

### Seçenek A: GitHub'da Host Et

1. Veritabanını oluştur:
```bash
cd /Users/teyfikoz/Downloads/NBD/nbd_database
cd scripts
python 1_fetch_names_dataset.py
python 2_fetch_wikipedia.py
python 3_fetch_olympics.py
python 4_fetch_phone_directories.py
python 5_merge_all_data.py
python 6_create_database.py
```

2. DB boyutunu kontrol et:
```bash
ls -lh ethnidata/ethnidata.db
```

3. Eğer <50MB ise, pakete dahil et:
```bash
# Veritabanını kopyala
cp ethnidata/ethnidata.db .

# Yeni build
rm -rf dist/
python -m build
twine upload dist/*
```

4. Eğer >50MB ise, GitHub Release olarak yükle:
```bash
# GitHub'da: https://github.com/teyfikoz/ethnidata/releases
# "Create a new release" → Tag: v1.0.0
# Upload ethnidata.db dosyasını
```

### Seçenek B: İlk Kullanımda Otomatik İndir

`ethnidata/__init__.py` dosyasına ekle (en başa):
```python
from pathlib import Path
import requests
import os

DB_PATH = Path(__file__).parent / "ethnidata.db"
DB_URL = "https://github.com/teyfikoz/ethnidata/releases/download/v1.0.0/ethnidata.db"

def ensure_database():
    if not DB_PATH.exists():
        print("📥 Downloading database (first time only, ~50MB)...")
        response = requests.get(DB_URL, stream=True)
        response.raise_for_status()

        with open(DB_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("✅ Database downloaded!")

ensure_database()
```

---

## 🎉 Kullanım (Son Kullanıcı İçin)

```bash
pip install ethnidata
```

```python
from ethnidata import EthniData

ed = EthniData()

# Milliyet tahmini
result = ed.predict_nationality("Ahmet")
print(result)

# Tam isim
result = ed.predict_full_name("Teyfik", "Oz")
print(result['country'])
```

---

## 🔄 Güncelleme Yayını

Gelecekte yeni versiyon yayınlamak için:

```bash
# 1. Kodu güncelle
# 2. Versiyon numarasını artır (setup.py ve pyproject.toml)
version = "1.0.1"

# 3. Git commit
git add .
git commit -m "v1.0.1: Bug fixes"
git push

# 4. Build ve PyPI'ye yükle
rm -rf dist/
python -m build
twine upload dist/*
```

---

## ❓ Sorun Giderme

### "Repository not found" (Git)
Token'ı doğru kopyaladın mı? Repo adı doğru mu?

### "Invalid username/password" (PyPI)
Username: `__token__` (tam olarak böyle)
Password: `pypi-...` token'ı (tümünü kopyala)

### "File already exists" (PyPI)
Aynı versiyon iki kez yüklenemez. `setup.py`'de version numarasını artır.

### "Database not found" (Kullanım)
- Adım 5'i uygula (veritabanı host et)
- Veya pakete dahil et (eğer <50MB)

---

## 📊 İstatistikler

Yayından sonra:
- PyPI: https://pypi.org/project/ethnidata/
- GitHub: https://github.com/teyfikoz/ethnidata
- Downloads: https://pypistats.org/packages/ethnidata

---

## ✅ Checklist

Yayınlamadan önce:
- [ ] GitHub repo oluşturuldu
- [ ] Kod GitHub'a yüklendi
- [ ] PyPI token alındı
- [ ] `python -m build` çalıştı
- [ ] `twine check dist/*` başarılı
- [ ] TestPyPI'de denendi (opsiyonel)
- [ ] PyPI'ye yüklendi
- [ ] `pip install ethnidata` test edildi
- [ ] Veritabanı sorunu çözüldü
