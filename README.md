# Kutu Tasarım Otomasyonu / Box Design Automation

Ambalaj kutu sektöründe otomatik teknik çizim ve kutu tasarımı programı.  
Automatic technical drawing and box design program for the packaging box industry.

## 🎯 Özellikler / Features

- **Otomatik Teknik Çizim** - Verilen ölçülerle otomatik teknik çizim üretimi
- **Çoklu Kutu Tipleri** - Standart kutu, tepsi kutu ve kapaklı kutu desteği
- **SVG Çıktısı** - Profesyonel kesim makineleri ile uyumlu SVG formatında çıktı
- **Web Arayüzü** - Kullanıcı dostu modern web arayüzü
- **Malzeme Hesaplama** - Otomatik malzeme alanı ve hacim hesaplaması
- **Önizleme** - Tarayıcıda anlık çizim önizleme

## 📋 Gereksinimler / Requirements

- Python 3.8+
- pip (Python paket yöneticisi)

## 🚀 Kurulum / Installation

1. Depoyu klonlayın / Clone the repository:
```bash
git clone https://github.com/xzupaix/kutu-tasar-m.git
cd kutu-tasar-m
```

2. Bağımlılıkları yükleyin / Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Kullanım / Usage

### Web Uygulaması / Web Application

1. Uygulamayı başlatın / Start the application:
```bash
python app.py
```

2. Tarayıcınızda açın / Open in your browser:
```
http://localhost:5000
```

3. Kutu ölçülerini girin ve teknik çizimi oluşturun / Enter box dimensions and generate technical drawing

### Python API Kullanımı / Python API Usage

```python
from box_designer import BoxDesigner
from svg_generator import SVGGenerator

# Kutu oluştur / Create a box
designer = BoxDesigner(length=200, width=150, height=100, material_thickness=3)

# Tasarım özelliklerini al / Get design specifications
specs = designer.get_design_specs(box_type='standard')
print(specs)

# SVG çizimi oluştur / Generate SVG drawing
generator = SVGGenerator(designer)
svg_content = generator.generate_standard_box_svg('my_box.svg')
```

## 📦 Desteklenen Kutu Tipleri / Supported Box Types

### 1. Standart Katlanır Kutu / Standard Folding Box
Klasik katlanır ambalaj kutusu (FEFCO 0201 tipi)

### 2. Tepsi/Display Kutu / Tray/Display Box
Açık üst görüntüleme kutusu

### 3. Kapaklı Kutu / Lid Box (Planlanan / Planned)
Ayrı kapaklı kutu sistemi

## 🎨 Teknik Çizim Özellikleri / Technical Drawing Features

- **Ölçü Göstergeleri** - Tüm kritik ölçüler çizimde gösterilir
- **Kıvırma Çizgileri** - Kırmızı kesikli çizgilerle gösterilir
- **Kesim Hatları** - Siyah düz çizgilerle gösterilir
- **Alan Etiketleri** - Her panel etiketlenir (Türkçe/İngilizce)

## 📊 Hesaplanan Değerler / Calculated Values

- Toplam malzeme alanı (m² ve mm²)
- Kutu hacmi (L ve mm³)
- Şablon boyutları
- Malzeme kalınlığı ayarlamaları

## 🔧 Geliştirme / Development

Proje yapısı / Project structure:
```
kutu-tasar-m/
├── app.py                  # Flask web uygulaması
├── box_designer.py         # Kutu tasarım hesaplamaları
├── svg_generator.py        # SVG çizim üretimi
├── requirements.txt        # Python bağımlılıkları
├── templates/              # HTML şablonları
│   └── index.html
├── static/                 # Statik dosyalar
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── README.md
```

## 🤝 Katkıda Bulunma / Contributing

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans / License

Bu proje açık kaynak kodludur.

## 👥 İletişim / Contact

Proje Bağlantısı / Project Link: [https://github.com/xzupaix/kutu-tasar-m](https://github.com/xzupaix/kutu-tasar-m)

## 🙏 Teşekkürler / Acknowledgments

- Flask framework
- svgwrite kütüphanesi
- Ambalaj endüstrisi standartları (FEFCO)
