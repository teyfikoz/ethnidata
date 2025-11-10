# Email Duyurusu - EthniData v3.0.1

---

**Subject:** 🚀 EthniData v3.0.1 Released - Complete Religious Coverage with 6 Major World Religions!

**Subject (Turkish):** 🚀 EthniData v3.0.1 Yayınlandı - 6 Büyük Dünya Dini ile Tam Kapsama!

---

## Email Body

Merhaba {{name}},

EthniData v3.0.1'in yayınlandığını duyurmaktan büyük mutluluk duyuyorum! 🎉

### 🕌 6 Büyük Dünya Dini - Artık TAM KAPSAMA!

v3.0.1 ile **tüm büyük dünya dinlerini** kapsayan ilk sürümümüzü sunuyoruz:

✅ **Christianity** (3.9M kayıt - +3,065%)
✅ **Buddhism** (1.3M kayıt - +18,848%)
✅ **Islam** (504K kayıt - +623%)
✅ **Judaism** (121K kayıt - +2,371%) ← 24x artış! ✡️
✅ **Hinduism** (90K kayıt - +2,210%)
✅ **Sikhism** (24K kayıt) ← YENİ din! 🪯

### 📊 İnanılmaz Büyüme: 5.9M+ Kayıt!

v2.0.0'dan bu yana **14x büyüme**:
- 📊 **5,927,548** toplam kayıt (+1,326%)
- 🌍 **238** ülke
- 🗣️ **72** dil
- 🕌 **6** büyük dünya dini
- 💾 **1.1 GB** veritabanı

### 🌍 Mükemmel Global Denge

```
Asia     ████████████████████  33%  (2.0M kayıt)
Americas ████████████████████  32%  (1.9M kayıt)
Africa   ██████████████████    30%  (1.8M kayıt)
Europe   ███                    3%  (156K kayıt)
```

### 💡 Yeni Özellikler

**1. Judaism Coverage - 24x Artış! ✡️**

v2.0.0: 4.9K kayıt
v3.0.1: 121K kayıt (+2,371%)

```python
from ethnidata import EthniData
ed = EthniData(use_v3=True)

result = ed.predict_religion("Cohen")
# {'religion': 'Judaism', 'confidence': 0.95}
```

**2. Sikhism - Yeni Din Desteği! 🪯**

İlk kez Sikh isimleri için 24K kayıt eklendi!

```python
result = ed.predict_religion("Singh")
# {'religion': 'Sikhism', 'confidence': 0.92}
```

**3. Massive Buddhism Expansion ☸️**

v2.0.0: 6.9K kayıt
v3.0.1: 1.3M kayıt (+18,848%)

Asya isimleri için mükemmel kapsama!

### 🗂️ İki Seçenek: v2.0.0 ve v3.0.1

**v2.0.0 (Paket ile gelir):**
- 415K kayıt
- 75 MB
- Hızlı indirme
- Çoğu kullanım için yeterli

**v3.0.1 (Opsiyonel):**
- 5.9M kayıt (14x daha fazla!)
- 1.1 GB
- Maksimum doğruluk
- Araştırma için ideal

### 💻 Kurulum

**v2.0.0 ile başlayın (varsayılan):**
```bash
pip install --upgrade ethnidata
```

```python
from ethnidata import EthniData
ed = EthniData()  # v2.0.0 (415K kayıt)
```

**v3.0.1'e geçin (isteğe bağlı):**
```python
from ethnidata.downloader import download_v3_database

# v3.0.1 veritabanını indir (1.1 GB)
db_path = download_v3_database()

# v3.0.1 ile kullan
ed = EthniData(use_v3=True)  # 5.9M kayıt!
```

### 🔥 Kullanım Örnekleri

**Tüm 6 din ile çalışma:**
```python
customers = [
    "Muhammad Ali",    # Islam
    "David Cohen",     # Judaism
    "Priya Sharma",    # Hinduism
    "Wei Chen",        # Buddhism
    "Gurpreet Singh",  # Sikhism
    "John Smith"       # Christianity
]

for name in customers:
    result = ed.predict_all(name)
    print(f"{name}: {result['religion']['religion']}")
```

**Pandas ile toplu işlem:**
```python
import pandas as pd

df = pd.read_csv("customers.csv")
df['religion'] = df['name'].apply(
    lambda x: ed.predict_religion(x)['religion']
)

# Artık 6 din ile doğru segmentasyon!
print(df['religion'].value_counts())
```

### 📈 v2.0.0 vs v3.0.1 Karşılaştırma

| Özellik | v2.0.0 | v3.0.1 | Gelişme |
|---------|--------|--------|---------|
| Toplam Kayıt | 415K | 5.9M | +1,326% |
| **Dinler** | 5 | **6** | +20% |
| Christianity | 122K | 3.9M | +3,065% |
| Buddhism | 6.9K | 1.3M | +18,848% |
| Islam | 69.7K | 504K | +623% |
| **Judaism** | 4.9K | **121K** | **+2,371%** |
| Hinduism | 3.9K | 90K | +2,210% |
| **Sikhism** | 0 | **24K** | **YENİ!** |
| Asia Kapsama | 14.1% | 33% | +141% |
| Africa Kapsama | 13.4% | 30% | +131% |

### ⚡ Breaking Changes?

**HAYIR!** v3.0.1 tamamen geriye uyumlu. Mevcut kodunuz hiçbir değişiklik gerektirmeden çalışacak!

### 🔗 Linkler

- 📦 **PyPI**: https://pypi.org/project/ethnidata/
- 💻 **GitHub**: https://github.com/teyfikoz/ethnidata
- 📖 **Changelog**: https://github.com/teyfikoz/ethnidata/blob/main/CHANGELOG.md
- 📚 **v3.0.1 Docs**: https://github.com/teyfikoz/ethnidata/blob/main/README_V3_INFO.md

### 🙏 Katkıda Bulunun

EthniData açık kaynaklı ve ücretsizdir (MIT Lisansı):

- ⭐ GitHub'da star verin: https://github.com/teyfikoz/ethnidata
- 🐛 Bug bildirin
- 💡 Önerilerde bulunun
- 📢 Paylaşın!

### 🌟 Neden EthniData v3.0.1?

✅ **Tam Din Kapsamı**: 6 büyük dünya dini
✅ **Massive Dataset**: 5.9M+ kayıt
✅ **Mükemmel Global Denge**: 238 ülke, 5 kıta
✅ **Kolay Kullanım**: `pip install ethnidata`
✅ **Tamamen Ücretsiz**: MIT lisansı
✅ **Aktif Geliştirme**: Sürekli güncelleniyor!

---

Sorularınız varsa cevaplamaktan mutluluk duyarım!

Saygılarımla,

**Tefik Yavuz Oz**
Python Developer | Data Science Enthusiast
📧 teyfikoz@example.com
💻 https://github.com/teyfikoz

---

**PS:** v3.0.1 (5.9M kayıt) çok büyük, ama v2.0.0 (415K kayıt) çoğu kullanım için yeterli! İhtiyacınıza göre seçim yapabilirsiniz.

**PPS:** Bu email'i yararlı buldunuz mu? GitHub'da ⭐ vererek destek olabilirsiniz!

---

*Bu email'den çıkmak isterseniz: [unsubscribe link]*
*Email tercihlerinizi değiştirin: [preferences link]*
