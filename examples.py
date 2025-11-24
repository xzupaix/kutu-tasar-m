"""
Example usage of Box Designer API
Bu dosya, kutu tasarım kütüphanesinin Python API kullanımını gösterir.
This file demonstrates the Python API usage of the box design library.
"""
from box_designer import BoxDesigner
from svg_generator import SVGGenerator
import os


def example_1_basic_usage():
    """Temel kullanım örneği / Basic usage example"""
    print("\n" + "="*60)
    print("Örnek 1: Temel Kullanım / Example 1: Basic Usage")
    print("="*60)
    
    # Standart bir kutu oluştur / Create a standard box
    designer = BoxDesigner(
        length=200,  # Uzunluk / Length
        width=150,   # Genişlik / Width
        height=100,  # Yükseklik / Height
        material_thickness=3  # Malzeme kalınlığı / Material thickness
    )
    
    # Standart kutu için tasarım özelliklerini al
    # Get design specifications for standard box
    specs = designer.get_design_specs(box_type='standard')
    
    print(f"\nKutu Tipi / Box Type: {specs['template']['type']}")
    print(f"Malzeme Alanı / Material Area: {specs['material_area_m2']:.4f} m²")
    print(f"Kutu Hacmi / Box Volume: {specs['box_volume_liters']:.2f} L")
    
    return designer


def example_2_tray_box():
    """Tepsi kutu örneği / Tray box example"""
    print("\n" + "="*60)
    print("Örnek 2: Tepsi Kutu / Example 2: Tray Box")
    print("="*60)
    
    # Tepsi tipi kutu (açık üst görüntüleme kutusu)
    # Tray type box (open-top display box)
    designer = BoxDesigner(length=300, width=200, height=80, material_thickness=3)
    
    specs = designer.get_design_specs(box_type='tray')
    
    print(f"\nŞablon Boyutları / Template Dimensions:")
    print(f"  Toplam Genişlik / Total Width: {specs['template']['total_width']} mm")
    print(f"  Toplam Yükseklik / Total Height: {specs['template']['total_height']} mm")
    print(f"\nGerekli Malzeme / Required Material: {specs['material_area_m2']:.4f} m²")
    
    return designer


def example_3_multiple_sizes():
    """Farklı boyutlarda kutular / Multiple box sizes"""
    print("\n" + "="*60)
    print("Örnek 3: Farklı Boyutlar / Example 3: Multiple Sizes")
    print("="*60)
    
    # Farklı boyutlarda kutu tasarımları
    # Different size box designs
    boxes = [
        ("Küçük Kutu / Small Box", 100, 80, 60),
        ("Orta Kutu / Medium Box", 200, 150, 100),
        ("Büyük Kutu / Large Box", 400, 300, 200),
        ("Uzun Kutu / Long Box", 500, 100, 100),
    ]
    
    print("\nKutu Karşılaştırması / Box Comparison:\n")
    print(f"{'İsim/Name':<25} {'Ölçüler/Dims (mm)':<20} {'Alan/Area (m²)':<15} {'Hacim/Vol (L)':<15}")
    print("-" * 75)
    
    for name, length, width, height in boxes:
        designer = BoxDesigner(length, width, height)
        specs = designer.get_design_specs('standard')
        
        dims = f"{length}×{width}×{height}"
        area = f"{specs['material_area_m2']:.4f}"
        volume = f"{specs['box_volume_liters']:.2f}"
        
        print(f"{name:<25} {dims:<20} {area:<15} {volume:<15}")


def example_4_generate_svgs():
    """SVG dosyaları oluşturma / Generate SVG files"""
    print("\n" + "="*60)
    print("Örnek 4: SVG Oluşturma / Example 4: Generate SVGs")
    print("="*60)
    
    # Çıktı dizini oluştur / Create output directory
    import tempfile
    output_dir = os.path.join(tempfile.gettempdir(), 'example_boxes')
    os.makedirs(output_dir, exist_ok=True)
    
    # Standart kutu SVG'si
    print("\nStandart kutu SVG oluşturuluyor...")
    designer1 = BoxDesigner(200, 150, 100)
    generator1 = SVGGenerator(designer1)
    svg1 = generator1.generate_standard_box_svg()
    
    file1 = os.path.join(output_dir, 'example_standard.svg')
    with open(file1, 'w') as f:
        f.write(svg1)
    print(f"✅ Kaydedildi / Saved: {file1}")
    
    # Tepsi kutu SVG'si
    print("\nTepsi kutu SVG oluşturuluyor...")
    designer2 = BoxDesigner(300, 200, 80)
    generator2 = SVGGenerator(designer2)
    svg2 = generator2.generate_tray_box_svg()
    
    file2 = os.path.join(output_dir, 'example_tray.svg')
    with open(file2, 'w') as f:
        f.write(svg2)
    print(f"✅ Kaydedildi / Saved: {file2}")
    
    print(f"\nTüm SVG dosyaları şurada: {output_dir}")
    print(f"All SVG files at: {output_dir}")


def example_5_custom_thickness():
    """Farklı malzeme kalınlıkları / Different material thicknesses"""
    print("\n" + "="*60)
    print("Örnek 5: Malzeme Kalınlıkları / Example 5: Material Thickness")
    print("="*60)
    
    # Aynı kutu, farklı kalınlıklar
    # Same box, different thicknesses
    base_dims = (250, 180, 120)
    thicknesses = [2, 3, 4, 5]
    
    print(f"\nKutu Boyutu / Box Size: {base_dims[0]}×{base_dims[1]}×{base_dims[2]} mm\n")
    print(f"{'Kalınlık/Thick':<15} {'Alan/Area (m²)':<20} {'Fark/Diff'}")
    print("-" * 55)
    
    prev_area = None
    for thickness in thicknesses:
        designer = BoxDesigner(*base_dims, material_thickness=thickness)
        specs = designer.get_design_specs('standard')
        area = specs['material_area_m2']
        
        diff = ""
        if prev_area:
            diff = f"+{(area - prev_area):.4f}"
        
        print(f"{thickness} mm{'':<10} {area:.4f}{'':<15} {diff}")
        prev_area = area


def example_6_lid_box():
    """Kapaklı kutu örneği / Lid box example"""
    print("\n" + "="*60)
    print("Örnek 6: Kapaklı Kutu / Example 6: Lid Box")
    print("="*60)
    
    designer = BoxDesigner(200, 150, 100, material_thickness=3)
    specs = designer.get_design_specs(box_type='lid')
    
    print("\nKutu Gövdesi / Box Body:")
    print(f"  Genişlik / Width: {specs['template']['box']['total_width']} mm")
    print(f"  Yükseklik / Height: {specs['template']['box']['total_height']} mm")
    
    print("\nKapak / Lid:")
    print(f"  Genişlik / Width: {specs['template']['lid']['total_width']} mm")
    print(f"  Yükseklik / Height: {specs['template']['lid']['total_height']} mm")
    
    print(f"\nToplam Malzeme / Total Material: {specs['material_area_m2']:.4f} m²")


def run_all_examples():
    """Tüm örnekleri çalıştır / Run all examples"""
    print("\n" + "#"*60)
    print("KUTU TASARIM OTOMASYONU - PYTHON API ÖRNEKLERİ")
    print("BOX DESIGN AUTOMATION - PYTHON API EXAMPLES")
    print("#"*60)
    
    example_1_basic_usage()
    example_2_tray_box()
    example_3_multiple_sizes()
    example_4_generate_svgs()
    example_5_custom_thickness()
    example_6_lid_box()
    
    print("\n" + "#"*60)
    print("✅ Tüm örnekler tamamlandı / All examples completed")
    print("#"*60 + "\n")


if __name__ == '__main__':
    run_all_examples()
