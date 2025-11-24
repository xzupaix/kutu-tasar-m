# Kullanım Kılavuzu / User Guide

## Hızlı Başlangıç / Quick Start

### 1. Kurulum / Installation

```bash
# Bağımlılıkları yükleyin / Install dependencies
pip install -r requirements.txt
```

### 2. Web Arayüzü / Web Interface

Web uygulamasını başlatın / Start the web application:

```bash
python app.py
```

Tarayıcınızda açın / Open in your browser:
```
http://localhost:5000
```

#### Kullanım Adımları / Usage Steps:

1. **Kutu Tipini Seçin** - Standart, Tepsi veya Kapaklı
2. **Ölçüleri Girin** - Uzunluk, genişlik, yükseklik (mm cinsinden)
3. **Hesapla** - Malzeme alanı ve hacim hesaplanır
4. **Önizleme** - Teknik çizimi görüntüleyin
5. **İndir** - SVG dosyasını indirin

### 3. Komut Satırı / Command Line

Komut satırından doğrudan SVG oluşturun / Generate SVG directly from command line:

```bash
# Temel kullanım / Basic usage
python cli.py -l 200 -w 150 -ht 100 -t standard

# Özel çıktı dosyası / Custom output file
python cli.py -l 300 -w 200 -ht 80 -t tray -o my_box.svg

# Farklı malzeme kalınlığı / Different material thickness
python cli.py -l 250 -w 180 -ht 120 --thickness 4 -t standard

# Dosya kaydetmeden önizleme / Preview without saving
python cli.py -l 200 -w 150 -ht 100 --no-save
```

#### Parametreler / Parameters:

- `-l, --length`: Kutu uzunluğu (mm)
- `-w, --width`: Kutu genişliği (mm)
- `-ht, --height`: Kutu yüksekliği (mm)
- `-t, --type`: Kutu tipi (standard/tray/lid)
- `--thickness`: Malzeme kalınlığı (mm, varsayılan: 3)
- `-o, --output`: Çıktı dosya adı
- `--no-save`: Dosya kaydetme

### 4. Python API

Python kodunuzda kullanın / Use in your Python code:

```python
from box_designer import BoxDesigner
from svg_generator import SVGGenerator

# Kutu oluştur / Create box
designer = BoxDesigner(
    length=200,
    width=150,
    height=100,
    material_thickness=3
)

# Tasarım özelliklerini al / Get design specs
specs = designer.get_design_specs('standard')
print(f"Malzeme Alanı: {specs['material_area_m2']:.4f} m²")
print(f"Kutu Hacmi: {specs['box_volume_liters']:.2f} L")

# SVG oluştur / Generate SVG
generator = SVGGenerator(designer)
svg_content = generator.generate_standard_box_svg()

# Dosyaya kaydet / Save to file
with open('my_box.svg', 'w') as f:
    f.write(svg_content)
```

## Kutu Tipleri / Box Types

### 1. Standart Katlanır Kutu / Standard Folding Box
- FEFCO 0201 standardı
- Klasik ambalaj kutusu
- Kıvrılabilir kanatlar ile

### 2. Tepsi/Display Kutu / Tray/Display Box
- Açık üst tasarım
- Görüntüleme için ideal
- Köşe kesikleri ile kıvırma

### 3. Kapaklı Kutu / Lid Box
- Ayrı kapak ve gövde
- Premium paketleme için
- Yeniden kullanılabilir

## Teknik Çizim Özellikleri / Technical Drawing Features

### Çizgi Tipleri / Line Types:

- **Siyah Düz Çizgiler** = Kesim çizgileri / Cut lines
- **Kırmızı Kesikli Çizgiler** = Kıvırma çizgileri / Fold lines
- **Turuncu Çizgiler** = Köşe kesikleri / Corner cuts

### Bilgiler / Information:

- Kutu boyutları (L × W × H)
- Panel etiketleri (Türkçe/İngilizce)
- Ölçü göstergeleri

## Örnekler / Examples

Daha fazla örnek için `examples.py` dosyasını çalıştırın:

```bash
python examples.py
```

Bu dosya şunları gösterir:
- Temel kullanım
- Farklı kutu tipleri
- Çoklu boyutlar
- SVG oluşturma
- Malzeme kalınlığı karşılaştırması

## Üretim Kullanımı / Production Use

### Güvenlik / Security

Üretim ortamında Flask uygulamasını çalıştırırken:

```bash
# Debug modunu kapatın / Disable debug mode
export FLASK_DEBUG=False
python app.py
```

Veya Gunicorn gibi production server kullanın:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Toplu İşleme / Batch Processing

Birden fazla kutu için script oluşturun:

```python
from box_designer import BoxDesigner
from svg_generator import SVGGenerator

boxes = [
    ("Küçük", 100, 80, 60),
    ("Orta", 200, 150, 100),
    ("Büyük", 400, 300, 200),
]

for name, l, w, h in boxes:
    designer = BoxDesigner(l, w, h)
    generator = SVGGenerator(designer)
    svg = generator.generate_standard_box_svg()
    
    with open(f'box_{name}.svg', 'w') as f:
        f.write(svg)
    print(f"✓ {name} kutu oluşturuldu")
```

## Sık Sorulan Sorular / FAQ

**S: SVG dosyalarını nasıl kullanırım?**
C: SVG dosyaları lazer kesim makineleri, plotter cihazları ve profesyonel kesim sistemleri ile uyumludur.

**S: Hangi ölçü birimi kullanılıyor?**
C: Tüm ölçüler milimetre (mm) cinsindendir.

**S: Farklı malzeme kalınlıkları için ayarlama yapabiliyor muyum?**
C: Evet, `--thickness` parametresi ile malzeme kalınlığını ayarlayabilirsiniz.

**S: Kendi kutu tipimi ekleyebilir miyim?**
C: Evet, `box_designer.py` dosyasına yeni hesaplama metodları ekleyebilir ve `svg_generator.py` dosyasında SVG üretimi yapabilirsiniz.

## Destek / Support

Sorunlar veya öneriler için GitHub Issues kullanın:
https://github.com/xzupaix/kutu-tasar-m/issues
