# EthniData - Veri Kaynakları ve Beklenen Boyut

## 📊 Toplanacak Veri Miktarı (Tahmini)

### 1. Wikipedia/Wikidata
- **Kayıt Sayısı**: ~50,000 kişi
- **Kapsam**: 190+ ülke
- **İçerik**: İsim, ülke, etnisite (bazılarında), doğum tarihi
- **Boyut**: ~5-10 MB (JSON)

### 2. names-dataset 
- **Kayıt Sayısı**: ~100,000+ isim
- **Kapsam**: 106 ülke
- **İçerik**: First names ve last names
- **Boyut**: ~2-5 MB

### 3. Olympics Dataset
- **Kayıt Sayısı**: 271,116 sporcu
- **Kapsam**: 120 yıl (1896-2016), 200+ ülke
- **İçerik**: İsim, ülke, NOC kodu, cinsiyet
- **Boyut**: ~30 MB (CSV)

### 4. Telefon Rehberleri
- **Kayıt Sayısı**: ~50,000-100,000 isim
- **Kapsam**: 20+ ülke (US, GB, DE, TR, vb.)
- **İçerik**: First names, surnames
- **Boyut**: ~5-10 MB

## 🗄️ SQLite Veritabanı (Birleştirilmiş)

### Beklenen Boyut
- **Toplam kayıt**: ~300,000-500,000 benzersiz isim-ülke çifti
- **First names**: ~150,000-250,000 kayıt
- **Last names**: ~150,000-250,000 kayıt
- **Veritabanı boyutu**: **50-150 MB** (tahmin)

### Tablolar
```sql
first_names  - isim, ülke, etnisite, kaynak, frekans
last_names   - isim, ülke, etnisite, kaynak, frekans
countries    - ülke kodu, ülke adı, bölge
```

### Kapsam
- **Ülke sayısı**: 190-200 ülke
- **Etnisite bilgisi**: ~10-20% kayıtlarda mevcut
- **Veri kaynağı çeşitliliği**: 4 farklı kaynak

## ⚡ Veri Toplama Süresi

| Script | Süre | Boyut |
|--------|------|-------|
| 1_fetch_names_dataset.py | ~2 dk | ~5 MB |
| 2_fetch_wikipedia.py | ~10-15 dk | ~10 MB |
| 3_fetch_olympics.py | ~1 dk | ~30 MB |
| 4_fetch_phone_directories.py | ~2-5 dk | ~10 MB |
| 5_merge_all_data.py | ~2-3 dk | ~20 MB |
| 6_create_database.py | ~5-10 dk | 50-150 MB |
| **TOPLAM** | **~20-35 dakika** | **~100-200 MB** |

## 🎯 Kalite ve Kapsam

### Güçlü Yanlar
✅ Olympics verisi çok güvenilir (IOC kayıtları)
✅ Wikipedia/Wikidata etnisite bilgisi içeriyor
✅ 200 ülkeyi kapsıyor
✅ Hem first hem last name desteği

### Kısıtlar
⚠️ Bazı ülkeler az temsil edilebilir
⚠️ Etnisite bilgisi sınırlı (~10-20%)
⚠️ Eski/nadir isimler eksik olabilir
⚠️ Diaspora/göç hesaba katılmıyor

## 📈 Örnek İstatistikler (Beklenen)

```
En çok isim olan ülkeler (tahmini):
1. USA: ~50,000 isim
2. GBR: ~30,000 isim
3. CHN: ~25,000 isim
4. JPN: ~20,000 isim
5. RUS: ~15,000 isim
...
50. TUR: ~5,000-10,000 isim
```

## 💾 Veritabanı Oluşturma

```bash
cd /Users/teyfikoz/Downloads/NBD/ethnidata/scripts

# Tüm scriptleri çalıştır
python 1_fetch_names_dataset.py
python 2_fetch_wikipedia.py
python 3_fetch_olympics.py
python 4_fetch_phone_directories.py
python 5_merge_all_data.py
python 6_create_database.py

# Sonuç: ethnidata/ethnidata.db (~50-150 MB)
```

## 🔍 Veritabanı Boyutunu Kontrol

```bash
cd /Users/teyfikoz/Downloads/NBD/ethnidata

# Veritabanı boyutu
ls -lh ethnidata/ethnidata.db

# İçeriği kontrol
sqlite3 ethnidata/ethnidata.db "SELECT COUNT(*) FROM first_names"
sqlite3 ethnidata/ethnidata.db "SELECT COUNT(*) FROM last_names"
sqlite3 ethnidata/ethnidata.db "SELECT COUNT(DISTINCT country_code) FROM first_names"
```

## 🚀 PyPI Yükleme Stratejisi

### Eğer DB < 50 MB
✅ Pakete dahil et (önerilen)
```bash
python -m build  # DB dahil edilir
twine upload dist/*
```

### Eğer DB > 50 MB
📦 GitHub Release'de host et
```bash
# 1. GitHub'da release oluştur
# 2. ethnidata.db dosyasını upload et
# 3. Kütüphane ilk çalıştırmada otomatik indirir
```

## 📊 Karşılaştırma

| Kütüphane | Veri Boyutu | Ülke | Etnisite |
|-----------|-------------|------|----------|
| **ethnidata** | 50-150 MB | 190+ | ✅ (kısmi) |
| ethnicolr | ~10 MB | USA | ✅ (USA only) |
| name-dataset | ~5 MB | 106 | ❌ |
| NamePrism | API | Global | ✅ (ücretli) |

EthniData = **En kapsamlı ücretsiz çözüm!** 🎉
