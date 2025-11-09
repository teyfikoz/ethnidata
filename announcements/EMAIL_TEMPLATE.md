# Email Duyuru Taslağı - EthniData v1.3.0

---

**Konu:** 🚀 Yeni Açık Kaynak Proje: EthniData v1.3.0 - İsimlerden Demografik Tahmin

---

Merhaba,

**EthniData v1.3.0**'ı sizlerle paylaşmaktan büyük mutluluk duyuyorum!

## 🎯 EthniData Nedir?

EthniData, bir isimden **6 farklı demografik özelliği** tahmin edebilen, tamamen **açık kaynaklı** bir Python kütüphanesidir.

### ✨ Özellikler:

| Özellik | Detay |
|---------|-------|
| 🌍 **Milliyet** | 165 ülke desteği |
| 🕌 **Din** | 5 büyük dünya dini (YENİ!) |
| 👤 **Cinsiyet** | Erkek/Kadın tahmini |
| 🗺️ **Bölge** | 5 kıta desteği |
| 🗣️ **Dil** | 46 dil desteği |
| 🧬 **Etnik Köken** | Kapsamlı analiz |

### 📊 Veriler:

- ✅ **220,656** toplam kayıt
- ✅ **165 ülke** (tüm dünya)
- ✅ **5 kıta**: Americas, Europe, Asia, Africa, Oceania
- ✅ **46 dil** desteği
- ✅ **%98+ veri kapsama oranı**

---

## 🚀 Hızlı Başlangıç

### Kurulum:
```bash
pip install ethnidata
```

### Kullanım:
```python
from ethnidata import EthniData

ed = EthniData()

# Milliyet
result = ed.predict_nationality("Ahmet")
print(result)
# {'country': 'TUR', 'country_name': 'Turkey', 'confidence': 0.89}

# Din (YENİ!)
result = ed.predict_religion("Muhammad")
print(result)
# {'religion': 'Islam', 'confidence': 0.95}

# Cinsiyet
result = ed.predict_gender("Emma")
print(result)
# {'gender': 'F', 'confidence': 0.98}

# Tüm özellikleri birden al
result = ed.predict_all("Maria")
print(result)
# Nationality, Religion, Gender, Region, Language, Ethnicity
```

---

## 💼 Kullanım Senaryoları

### 1. **Email Marketing & CRM**
```python
# Kullanıcı segmentasyonu
users = ["John Smith", "Ahmed Hassan", "Yuki Tanaka"]
for name in users:
    first, last = name.split()
    result = ed.predict_full_name(first, last)
    print(f"{name}: {result['country_name']} - {result['region']}")
```

### 2. **Veri Analizi**
```python
# CSV'den toplu analiz
import pandas as pd

df = pd.read_csv("customers.csv")
df['country'] = df['first_name'].apply(
    lambda x: ed.predict_nationality(x)['country']
)
df['religion'] = df['first_name'].apply(
    lambda x: ed.predict_religion(x)['religion']
)
```

### 3. **Araştırma & Raporlama**
```python
# İstatistiksel analiz
stats = ed.get_stats()
print(f"Toplam ülke: {stats['countries']}")
print(f"Toplam dil: {stats['languages']}")
```

---

## 🔥 v1.3.0 Yenilikleri

### 🕌 Din Tahmini - Tamamen Yeni!
- Christianity, Islam, Hinduism, Buddhism, Judaism
- %98+ veri kapsama oranı
- Ülke ve isim pattern tabanlı akıllı çıkarım

### 🌍 Tam Global Destek
- **Afrika** kıtası eklendi (1,637 kayıt)
- **Okyanusya** genişletildi (476 kayıt)
- **165 ülke** ISO standardına uygun
- **46 dil** desteği (önceki 3'ten)

### 📈 Performans İyileştirmeleri
- Veritabanı optimize edildi: 21 MB → 19.38 MB
- 310K kayıt temizlendi → 220K kaliteli kayıt
- Daha hızlı sorgular

---

## 📊 Detaylı İstatistikler

### Bölgesel Dağılım:
```
Americas  ████████████████████████░░  53.0%  (117,005 kayıt)
Europe    ████████████████████░░░░░░  43.6%  ( 96,312 kayıt)
Asia      █░░░░░░░░░░░░░░░░░░░░░░░░   1.2%  (  2,715 kayıt)
Africa    ░░░░░░░░░░░░░░░░░░░░░░░░░   0.7%  (  1,637 kayıt)
Oceania   ░░░░░░░░░░░░░░░░░░░░░░░░░   0.2%  (    476 kayıt)
```

### Din Dağılımı:
```
Christianity  ████████████████████████  95.7%  (209,502 kayıt)
Judaism       █░░░░░░░░░░░░░░░░░░░░░░   1.6%  (  3,489 kayıt)
Islam         █░░░░░░░░░░░░░░░░░░░░░░   1.3%  (  2,811 kayıt)
Buddhism      ░░░░░░░░░░░░░░░░░░░░░░░   0.2%  (    490 kayıt)
Hinduism      ░░░░░░░░░░░░░░░░░░░░░░░   0.08% (    171 kayıt)
```

---

## 🌟 Neden EthniData?

✅ **Tamamen Ücretsiz** - MIT Lisansı
✅ **Açık Kaynak** - GitHub'da mevcut
✅ **Kolay Kurulum** - `pip install ethnidata`
✅ **Kapsamlı Dokümantasyon**
✅ **Aktif Geliştirme** - Sürekli güncellemeler
✅ **Global Destek** - 165 ülke, 5 kıta, 46 dil

---

## 🔗 Bağlantılar

📦 **PyPI**: https://pypi.org/project/ethnidata/
💻 **GitHub**: https://github.com/teyfikoz/ethnidata
📖 **Dökümantasyon**: https://github.com/teyfikoz/ethnidata#readme
🐛 **Issues**: https://github.com/teyfikoz/ethnidata/issues

---

## 🙏 Destek Olun

EthniData'yı beğendiyseniz:

- ⭐ **GitHub'da star verin**: https://github.com/teyfikoz/ethnidata
- 📢 **Paylaşın**: Arkadaşlarınızla ve ekibinizle paylaşın
- 🐛 **Katkıda bulunun**: Bug bildirin, önerilerde bulunun
- 💬 **Geri bildirim verin**: Ne düşündüğünüzü bize bildirin

---

## 📧 İletişim

**Sorularınız mı var?**
- GitHub Issues: https://github.com/teyfikoz/ethnidata/issues
- Email: teyfikoz@example.com

---

**Teşekkürler ve mutlu kodlamalar!** 🚀

**Tefik Yavuz Oz**
Python Developer | Data Science Enthusiast

---

*Bu e-posta, EthniData açık kaynak projesini duyurmak amacıyla gönderilmiştir. Eğer bu tür güncellemeleri almak istemiyorsanız, lütfen bize bildirin.*

---

### 📎 EK: Örnek Kullanım Senaryoları

**Senaryo 1: E-ticaret Sitesi Kullanıcı Profilleme**
```python
# Yeni kullanıcı kaydı
user_name = "Emma Johnson"
first, last = user_name.split()

profile = ed.predict_full_name(first, last)
# Kullanıcıya uygun dil seçeneği göster
# Uygun para birimi öner
# Bölgesel ürün önerileri yap
```

**Senaryo 2: Araştırma Verileri Analizi**
```python
# Anket katılımcılarının demografik analizi
participants = ["John Smith", "Li Wei", "Maria Garcia"]
demographics = []

for name in participants:
    result = ed.predict_all(name.split()[0])
    demographics.append({
        'name': name,
        'country': result['nationality']['country_name'],
        'region': result['region']['region'],
        'religion': result['religion']['religion']
    })
```

**Senaryo 3: CRM Sistemi Enrichment**
```python
# Eksik müşteri verilerini tamamla
customer = {
    'name': 'Ahmed',
    'last_name': 'Hassan',
    'country': None,  # Eksik
    'language': None  # Eksik
}

prediction = ed.predict_full_name(
    customer['name'],
    customer['last_name']
)

customer['country'] = prediction['country_name']
customer['language'] = prediction['language']
```
