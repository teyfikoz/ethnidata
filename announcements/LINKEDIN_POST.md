# LinkedIn Duyurusu - EthniData v1.3.0

---

## 🚀 Yeni Açık Kaynak Proje: EthniData v1.3.0

**İsimlerden Demografik Tahmin Yapan Kapsamlı Python Kütüphanesi**

Bugün, **EthniData v1.3.0**'ı Python topluluğu ile paylaşmaktan büyük mutluluk duyuyorum!

### 🎯 EthniData Nedir?

EthniData, bir isimden 6 farklı demografik özelliği tahmin edebilen, tamamen açık kaynaklı bir Python kütüphanesidir:

✅ **Milliyet** (165 ülke)
✅ **Din** - YENİ! (5 büyük dünya dini)
✅ **Cinsiyet**
✅ **Bölge** (5 kıta)
✅ **Dil** (46 dil)
✅ **Etnik köken**

### 📊 Kapsamlı Global Veri:

🌍 **220,656** kayıt
🗺️ **165 ülke** (tüm kıtalar)
🌎 **5 kıta**: Americas, Europe, Asia, Africa, Oceania
🗣️ **46 dil**
🕌 **5 din**: Christianity, Islam, Hinduism, Buddhism, Judaism
📈 **%98+ veri kapsama oranı**

### 💡 Kullanım Senaryoları:

- 📧 **Email Marketing**: Kullanıcı segmentasyonu ve kişiselleştirme
- 🔍 **Veri Analizi**: Demografik içgörüler ve raporlama
- 🧪 **Araştırma**: Sosyal bilimler ve demografik çalışmalar
- 🎯 **CRM Sistemleri**: Müşteri profilleme
- 🌐 **Uluslararası İşletmeler**: Çok kültürlü ekip yönetimi
- 📊 **İstatistiksel Analizler**: Nüfus dağılımı tahminleri

### 🔥 v1.3.0'daki Yenilikler:

🕌 **DİN TAHMİNİ** - Tamamen yeni özellik!
- 5 büyük dünya dini desteği
- %98+ veri kapsama oranı
- Ülke ve isim pattern tabanlı akıllı çıkarım

🌍 **KAPSAMLI GLOBAL DESTEK**
- Afrika kıtası eklendi (1,637 kayıt)
- Okyanusya kıtası genişletildi (476 kayıt)
- 165 ülke ISO 3166-1 alpha-3 standardına uygun
- 46 dil desteği (önceki 3'ten)

### 🚀 Nasıl Kullanılır?

**Kurulum** (PyPI üzerinden):
```bash
pip install ethnidata
```

**Temel Kullanım**:
```python
from ethnidata import EthniData

ed = EthniData()

# Milliyet tahmini
result = ed.predict_nationality("Ahmet")
# {'country': 'TUR', 'confidence': 0.89, ...}

# Din tahmini (YENİ!)
result = ed.predict_religion("Muhammad")
# {'religion': 'Islam', 'confidence': 0.95, ...}

# Cinsiyet tahmini
result = ed.predict_gender("Emma")
# {'gender': 'F', 'confidence': 0.98, ...}

# TÜMÜNÜ BİRDEN!
result = ed.predict_all("Maria")
# Nationality, Religion, Gender, Region, Language, Ethnicity
```

### 📈 İstatistikler:

**Bölge Dağılımı:**
- Americas: 53% (117,005 kayıt)
- Europe: 44% (96,312 kayıt)
- Asia: 1.2% (2,715 kayıt)
- Africa: 0.7% (1,637 kayıt)
- Oceania: 0.2% (476 kayıt)

**Din Dağılımı:**
- Christianity: 95.7% (209,502 kayıt)
- Judaism: 1.6% (3,489 kayıt)
- Islam: 1.3% (2,811 kayıt)
- Buddhism: 0.2% (490 kayıt)
- Hinduism: 0.08% (171 kayıt)

### 🔗 Linkler:

📦 **PyPI**: https://pypi.org/project/ethnidata/
💻 **GitHub**: https://github.com/teyfikoz/ethnidata
📖 **Dökümantasyon**: https://github.com/teyfikoz/ethnidata#readme
🐛 **Issues**: https://github.com/teyfikoz/ethnidata/issues

### 🌟 Açık Kaynak & Ücretsiz

EthniData tamamen **açık kaynaklı** (MIT Lisansı) ve **ücretsizdir**. Herkes kullanabilir, geliştirebilir ve katkıda bulunabilir!

### 🙏 Katkıda Bulunun

- ⭐ GitHub'da star verin
- 🐛 Bug bildirin
- 💡 Önerilerde bulunun
- 🔧 Pull request gönderin
- 📢 Paylaşın!

---

**#Python #OpenSource #DataScience #MachineLearning #NLP #Demographics #AI #DataAnalysis #GitHub #PyPI**

---

*Bu proje, veri bilimi ve demografik analiz alanında çalışan herkese faydalı olmak amacıyla geliştirilmiştir. Geri bildirimlerinizi ve katkılarınızı bekliyorum!*

**Tefik Yavuz Oz**
Python Developer | Data Science Enthusiast
