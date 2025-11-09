# Görsel Tasarım Rehberi - EthniData v1.3.0

---

## 🎨 Renk Paleti

### Ana Renkler
```
Primary Blue:    #2563EB (Başlıklar, logo)
Secondary Green: #10B981 (Başarı, onaylar)
Accent Orange:   #F59E0B (Vurgular, yenilikler)
Dark Gray:       #1F2937 (Metin)
Light Gray:      #F3F4F6 (Arka plan)
White:           #FFFFFF (Kartlar, kutular)
```

### Din Renkleri (Grafiklerde kullanım için)
```
Christianity: #3B82F6 (Mavi)
Islam:        #10B981 (Yeşil)
Hinduism:     #F59E0B (Turuncu)
Buddhism:     #EAB308 (Sarı)
Judaism:      #8B5CF6 (Mor)
```

### Bölge Renkleri
```
Americas:  #3B82F6 (Mavi)
Europe:    #10B981 (Yeşil)
Asia:      #F59E0B (Turuncu)
Africa:    #EF4444 (Kırmızı)
Oceania:   #8B5CF6 (Mor)
```

---

## 📊 Grafik Önerileri

### Grafik 1: Bölge Dağılımı (Pie Chart)

**Veri:**
```python
regions = {
    'Americas': 117005,  # 53%
    'Europe': 96312,     # 44%
    'Asia': 2715,        # 1.2%
    'Africa': 1637,      # 0.7%
    'Oceania': 476       # 0.2%
}
```

**Tasarım Özellikleri:**
- **Tip:** Donut Chart (ortası boş)
- **Başlık:** "Global Coverage: 5 Continents"
- **Alt başlık:** "220,656 Total Records"
- **Renkler:** Yukarıdaki bölge renkleri
- **Font:** Inter veya Roboto, Bold
- **Boyut:** 1200x800px (sosyal medya için)

**Canva/Figma Template:**
```
🌍 [Donut Chart - Merkez]
   "220K+"
   "Records"

[Dilimlere label'lar:]
Americas 53%
Europe 44%
Asia 1.2%
Africa 0.7%
Oceania 0.2%

[Legend - Sağ tarafta]
🔵 Americas: 117,005
🟢 Europe: 96,312
🟠 Asia: 2,715
🔴 Africa: 1,637
🟣 Oceania: 476
```

---

### Grafik 2: Din Dağılımı (Bar Chart)

**Veri:**
```python
religions = {
    'Christianity': 209502,  # 95.7%
    'Judaism': 3489,         # 1.6%
    'Islam': 2811,           # 1.3%
    'Buddhism': 490,         # 0.2%
    'Hinduism': 171          # 0.08%
}
```

**Tasarım Özellikleri:**
- **Tip:** Horizontal Bar Chart
- **Başlık:** "Religion Distribution"
- **Alt başlık:** "98% Coverage with Religion Data"
- **Renkler:** Yukarıdaki din renkleri
- **Animasyon:** Barlar soldan sağa dolsun
- **Boyut:** 1200x800px

**Tasarım Layout:**
```
Religion Distribution
98% Coverage • 216,463 Records with Religion Data

Christianity  ████████████████████  95.7%  (209,502)
Judaism       ██░░░░░░░░░░░░░░░░░░   1.6%  (  3,489)
Islam         █░░░░░░░░░░░░░░░░░░░   1.3%  (  2,811)
Buddhism      ░░░░░░░░░░░░░░░░░░░░   0.2%  (    490)
Hinduism      ░░░░░░░░░░░░░░░░░░░░   0.08% (    171)
```

---

### Grafik 3: Özellikler Karşılaştırması (v1.2 vs v1.3)

**Veri:**
```python
comparison = {
    'Countries': {'v1.2': 172, 'v1.3': 165},
    'Continents': {'v1.2': 4, 'v1.3': 5},
    'Languages': {'v1.2': 3, 'v1.3': 46},
    'Features': {'v1.2': 5, 'v1.3': 6},
    'Records': {'v1.2': 310000, 'v1.3': 220656}
}
```

**Tasarım Özellikleri:**
- **Tip:** Grouped Bar Chart
- **Başlık:** "v1.3.0 Improvements"
- **Renkler:** v1.2 (açık gri), v1.3 (primary blue)
- **Boyut:** 1200x800px

---

### Grafik 4: İstatistik Kartları (Info Cards)

**6 Adet Kart Tasarımı:**

**Kart 1: Toplam Kayıtlar**
```
┌─────────────────────┐
│  📊                 │
│  220,656           │
│  Total Records     │
└─────────────────────┘
```

**Kart 2: Ülkeler**
```
┌─────────────────────┐
│  🌍                 │
│  165               │
│  Countries         │
└─────────────────────┘
```

**Kart 3: Diller**
```
┌─────────────────────┐
│  🗣️                 │
│  46                │
│  Languages         │
└─────────────────────┘
```

**Kart 4: Kıtalar**
```
┌─────────────────────┐
│  🌎                 │
│  5                 │
│  Continents        │
└─────────────────────┘
```

**Kart 5: Dinler**
```
┌─────────────────────┐
│  🕌                 │
│  5                 │
│  Religions         │
└─────────────────────┘
```

**Kart 6: Kapsama**
```
┌─────────────────────┐
│  ✅                 │
│  98%               │
│  Data Coverage     │
└─────────────────────┘
```

**Tasarım Detayları:**
- Beyaz arka plan
- Hafif gölge (shadow)
- Border radius: 12px
- Padding: 32px
- Icon boyutu: 48px
- Sayı font: 48px, Bold
- Label font: 16px, Regular
- Gradient border (opsiyonel)

---

## 🖼️ Banner Tasarımları

### Banner 1: GitHub Repository Cover

**Boyut:** 1280x640px

**İçerik:**
```
┌────────────────────────────────────────────────────┐
│                                                    │
│        🌍 EthniData v1.3.0                        │
│                                                    │
│    Predict Demographics from Names                │
│                                                    │
│  [6 iconlu feature list]                          │
│  🌍 Nationality  🕌 Religion  👤 Gender           │
│  🗺️ Region      🗣️ Language   🧬 Ethnicity         │
│                                                    │
│  165 Countries • 5 Continents • 46 Languages      │
│                                                    │
│  pip install ethnidata                            │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Arka Plan:** Gradient (Primary Blue → Secondary Green)
**Metin:** Beyaz
**Font:** Inter Black, 64px (başlık), 32px (alt başlık)

---

### Banner 2: LinkedIn Cover

**Boyut:** 1584x396px

**İçerik:**
```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  EthniData v1.3.0  |  220K+ Names  |  165 Countries         │
│  Open Source Demographics Prediction from Names             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Arka Plan:** Koyu gri gradient
**Accent:** Primary Blue çizgiler
**Logo:** Sol köşede

---

### Banner 3: Twitter Header

**Boyut:** 1500x500px

**İçerik:**
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  EthniData                                    v1.3.0   │
│  Demographics Prediction from Names                    │
│                                                        │
│  🌍 165 Countries  🗣️ 46 Languages  🕌 5 Religions     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📱 Sosyal Medya Görselleri

### Instagram/LinkedIn Post - Square (1080x1080px)

**Layout 1: Özellik Tanıtımı**
```
┌─────────────────────────────┐
│                             │
│    🌍 EthniData v1.3.0      │
│                             │
│    6 Features:              │
│                             │
│    ✅ Nationality           │
│    ✅ Religion (NEW!)       │
│    ✅ Gender                │
│    ✅ Region                │
│    ✅ Language              │
│    ✅ Ethnicity             │
│                             │
│    pip install ethnidata    │
│                             │
└─────────────────────────────┘
```

**Layout 2: İstatistik Showcase**
```
┌─────────────────────────────┐
│                             │
│    Global Coverage          │
│                             │
│    🌍 165                   │
│       Countries             │
│                             │
│    🗣️ 46                    │
│       Languages             │
│                             │
│    📊 220K+                 │
│       Records               │
│                             │
└─────────────────────────────┘
```

---

## 🎬 GIF/Video Önerileri

### Video 1: Kurulum & İlk Kullanım (15 saniye)

**Storyboard:**
```
[0-3s]  Terminal açılır
        $ pip install ethnidata

[4-7s]  Python REPL açılır
        >>> from ethnidata import EthniData
        >>> ed = EthniData()

[8-12s] İlk tahmin
        >>> ed.predict_nationality("Ahmet")

[13-15s] Sonuç gösterilir (JSON formatted)
         {'country': 'TUR', 'confidence': 0.89, ...}
```

**Stil:**
- Arka plan: VS Code dark theme
- Font: Fira Code
- Highlight: Syntax highlighting
- Terminal: iTerm2 benzeri

---

### Video 2: Tüm Özellikleri Göster (30 saniye)

**Sahneler:**
```
[0-5s]   predict_nationality()
[6-10s]  predict_religion() - YENİ badge
[11-15s] predict_gender()
[16-20s] predict_region()
[21-25s] predict_language()
[26-30s] predict_all() - Hepsini birden!
```

**Animasyon:**
- Smooth transitions
- JSON sonuçları formatlanmış
- Key highlight'lar
- "NEW!" badge için özel vurgu

---

### GIF 1: Data Coverage Animation

**Frame 1:** Dünya haritası (gri)
**Frame 2:** Americas kısmı mavi olur (53%)
**Frame 3:** Europe kısmı yeşil olur (44%)
**Frame 4:** Asia kısmı turuncu olur (1.2%)
**Frame 5:** Africa kısmı kırmızı olur (0.7%)
**Frame 6:** Oceania kısmı mor olur (0.2%)
**Frame 7:** "165 Countries • 5 Continents" metni

**Boyut:** 800x600px
**Format:** GIF, 3 saniye loop

---

## 🎯 Logo Tasarımı

### Logo Konsept 1: Globe + Name
```
    🌍
EthniData
```

**Renk:** Primary Blue (#2563EB)
**Font:** Inter Black
**Icon:** Globe emoji veya özel icon

---

### Logo Konsept 2: Monogram
```
┌─────┐
│ ED  │  EthniData
└─────┘
```

**Renk:** Gradient (Blue → Green)
**Font:** Inter Bold
**Stil:** Modern, minimal

---

### Logo Konsept 3: Data + Globe Kombine
```
  📊🌍
EthniData
```

**Konsept:** Veri analizi + Global kapsama
**Kullanım:** Sosyal medya profil fotoğrafı

---

## 🛠️ Tasarım Araçları Önerileri

### Grafik Tasarım
1. **Canva Pro** - En kolay, template'ler hazır
2. **Figma** - Profesyonel, collaboration
3. **Adobe Illustrator** - Detaylı vektör grafik

### Veri Görselleştirme
1. **Python (Matplotlib/Seaborn)**
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns

   # Region dağılımı
   regions = {'Americas': 117005, 'Europe': 96312, ...}
   plt.pie(regions.values(), labels=regions.keys())
   plt.savefig('region_distribution.png', dpi=300)
   ```

2. **Plotly** - İnteraktif grafikler
   ```python
   import plotly.express as px
   fig = px.pie(values=list(regions.values()),
                names=list(regions.keys()))
   fig.write_image('region_pie.png')
   ```

3. **Chart.js** - Web için
4. **D3.js** - Özel animasyonlar

### Video/GIF
1. **Screen Studio** (Mac) - Terminal recordings
2. **OBS Studio** - Ücretsiz screen recording
3. **LICEcap** - GIF creation
4. **Gifox** - Mac için GIF tool

### Screenshot & Mockup
1. **Carbon** (carbon.now.sh) - Kod screenshot
2. **Ray.so** - Kod screenshot (alternatif)
3. **Mockuphone** - Telefon mockup
4. **Shots.so** - Mac window mockup

---

## 📐 Boyut Rehberi

### Sosyal Medya Boyutları

**LinkedIn:**
- Post image: 1200x627px
- Profile cover: 1584x396px
- Company logo: 300x300px

**Twitter/X:**
- Post image: 1200x675px (16:9)
- Header: 1500x500px
- Profile: 400x400px

**GitHub:**
- Repository social: 1280x640px
- Profile README: 800px genişlik (responsive)

**Instagram:**
- Square post: 1080x1080px
- Story: 1080x1920px

**Email:**
- Header banner: 600px genişlik
- Inline images: 400-500px genişlik

---

## 🎨 Python Kod Örnekleri (Grafik Üretimi)

### Grafik 1: Bölge Dağılımı
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Data
regions = {
    'Americas': 117005,
    'Europe': 96312,
    'Asia': 2715,
    'Africa': 1637,
    'Oceania': 476
}

# Colors
colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

# Create pie chart
fig, ax = plt.subplots(figsize=(12, 8))
wedges, texts, autotexts = ax.pie(
    regions.values(),
    labels=regions.keys(),
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 14, 'weight': 'bold'}
)

# Title
plt.title('EthniData: Global Coverage - 5 Continents',
          fontsize=20, weight='bold', pad=20)

# Add center text (donut effect)
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

plt.text(0, 0, '220,656\nRecords',
         ha='center', va='center',
         fontsize=24, weight='bold')

plt.tight_layout()
plt.savefig('region_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Grafik 2: Din Dağılımı
```python
import matplotlib.pyplot as plt
import numpy as np

# Data
religions = {
    'Christianity': 209502,
    'Judaism': 3489,
    'Islam': 2811,
    'Buddhism': 490,
    'Hinduism': 171
}

# Colors
colors = ['#3B82F6', '#8B5CF6', '#10B981', '#EAB308', '#F59E0B']

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 8))

y_pos = np.arange(len(religions))
values = list(religions.values())

bars = ax.barh(y_pos, values, color=colors)

# Labels
ax.set_yticks(y_pos)
ax.set_yticklabels(religions.keys(), fontsize=14, weight='bold')
ax.set_xlabel('Number of Records', fontsize=14, weight='bold')
ax.set_title('EthniData: Religion Distribution\n98% Coverage • 216,463 Records',
             fontsize=18, weight='bold', pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, values)):
    percentage = (value / sum(values)) * 100
    ax.text(value, i, f'  {value:,} ({percentage:.1f}%)',
            va='center', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig('religion_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Grafik 3: İstatistik Kartları
```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('EthniData v1.3.0 Statistics',
             fontsize=24, weight='bold', y=0.98)

stats = [
    ('📊', '220,656', 'Total Records'),
    ('🌍', '165', 'Countries'),
    ('🗣️', '46', 'Languages'),
    ('🌎', '5', 'Continents'),
    ('🕌', '5', 'Religions'),
    ('✅', '98%', 'Coverage')
]

colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#22C55E']

for ax, (icon, value, label), color in zip(axes.flat, stats, colors):
    ax.axis('off')

    # Card background
    rect = patches.FancyBboxPatch(
        (0.1, 0.1), 0.8, 0.8,
        boxstyle="round,pad=0.05",
        edgecolor=color, facecolor='white',
        linewidth=3, transform=ax.transAxes
    )
    ax.add_patch(rect)

    # Content
    ax.text(0.5, 0.7, icon, ha='center', va='center',
            fontsize=48, transform=ax.transAxes)
    ax.text(0.5, 0.45, value, ha='center', va='center',
            fontsize=32, weight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.25, label, ha='center', va='center',
            fontsize=14, color='gray', transform=ax.transAxes)

plt.tight_layout()
plt.savefig('statistics_cards.png', dpi=300, bbox_inches='tight',
            facecolor='#F3F4F6')
plt.show()
```

---

## ✅ Hazırlanacak Görseller Checklist

### Zorunlu Görseller
- [ ] Logo (3 varyant)
- [ ] GitHub repository cover (1280x640px)
- [ ] Bölge dağılımı pie chart
- [ ] Din dağılımı bar chart
- [ ] 6 istatistik kartı

### LinkedIn İçin
- [ ] Ana duyuru görseli (1200x627px)
- [ ] Profile cover (1584x396px)
- [ ] Carousel (5-10 slide)

### Twitter İçin
- [ ] Header image (1500x500px)
- [ ] Thread görselleri (1200x675px, 4-5 adet)
- [ ] GIF: Kurulum demo

### Email İçin
- [ ] Header banner (600px)
- [ ] Feature showcase (3 görsel)
- [ ] Footer banner

### Opsiyonel
- [ ] Video tutorial (30s)
- [ ] Interactive demo GIF
- [ ] Comparison chart (v1.2 vs v1.3)
- [ ] World map with coverage highlight

---

## 🎯 Sonraki Adımlar

1. **Canva/Figma'da template oluştur**
2. **Python scriptleri çalıştır** (grafikleri üret)
3. **Carbon.now.sh'ta kod screenshot'ları al**
4. **Logo tasarımını finalize et**
5. **Video/GIF kayıtlarını yap**
6. **Tüm görselleri optimize et** (boyut küçültme)
7. **GitHub'a `assets/` klasörüne yükle**

---

**Tüm görseller Creative Commons lisansı altında açık kaynak olarak paylaşılabilir!**
