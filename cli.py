#!/usr/bin/env python3
"""
Command Line Interface for Box Designer
Simple CLI tool to generate box designs from command line
"""
import argparse
import sys
from box_designer import BoxDesigner
from svg_generator import SVGGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Kutu Tasarım Otomasyonu - Box Design Automation CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler / Examples:
  %(prog)s -l 200 -w 150 -h 100 -t standard -o my_box.svg
  %(prog)s --length 300 --width 200 --height 80 --type tray --output tray.svg
  %(prog)s -l 250 -w 180 -h 120 --thickness 4 -t standard
        """
    )
    
    parser.add_argument('-l', '--length', type=float, required=True,
                        help='Kutu uzunluğu (mm) / Box length (mm)')
    parser.add_argument('-w', '--width', type=float, required=True,
                        help='Kutu genişliği (mm) / Box width (mm)')
    parser.add_argument('-ht', '--height', type=float, required=True,
                        help='Kutu yüksekliği (mm) / Box height (mm)')
    parser.add_argument('-t', '--type', choices=['standard', 'tray', 'lid'],
                        default='standard',
                        help='Kutu tipi / Box type (default: standard)')
    parser.add_argument('--thickness', type=float, default=3,
                        help='Malzeme kalınlığı (mm) / Material thickness (mm) (default: 3)')
    parser.add_argument('-o', '--output', type=str,
                        help='Çıktı dosya adı / Output filename (optional)')
    parser.add_argument('--no-save', action='store_true',
                        help='SVG dosyası kaydetme / Do not save SVG file')
    
    args = parser.parse_args()
    
    try:
        # Create box designer
        print(f"\n{'='*60}")
        print("Kutu Tasarım Otomasyonu / Box Design Automation")
        print(f"{'='*60}\n")
        
        designer = BoxDesigner(
            length=args.length,
            width=args.width,
            height=args.height,
            material_thickness=args.thickness
        )
        
        # Validate dimensions
        designer.validate_dimensions()
        print("✅ Ölçüler geçerli / Dimensions valid")
        
        # Get design specifications
        specs = designer.get_design_specs(args.type)
        
        # Print specifications
        print(f"\n📦 Kutu Bilgileri / Box Information:")
        print(f"   Tip / Type: {specs['template']['type']}")
        print(f"   Ölçüler / Dimensions: {args.length}×{args.width}×{args.height} mm")
        print(f"   Kalınlık / Thickness: {args.thickness} mm")
        
        print(f"\n📊 Hesaplamalar / Calculations:")
        print(f"   Malzeme Alanı / Material Area: {specs['material_area_m2']:.4f} m²")
        print(f"   Kutu Hacmi / Box Volume: {specs['box_volume_liters']:.3f} L")
        
        if not args.no_save:
            # Generate SVG
            generator = SVGGenerator(designer)
            
            if args.type == 'standard':
                svg_content = generator.generate_standard_box_svg()
            elif args.type == 'tray':
                svg_content = generator.generate_tray_box_svg()
            else:
                print(f"\n⚠️  Uyarı: '{args.type}' tipi için henüz SVG üretimi desteklenmiyor")
                print(f"    Warning: SVG generation not yet supported for '{args.type}' type")
                sys.exit(0)
            
            # Determine output filename
            if args.output:
                output_file = args.output
            else:
                output_file = f"{args.type}_box_{args.length}x{args.width}x{args.height}.svg"
            
            # Save SVG file
            with open(output_file, 'w') as f:
                f.write(svg_content)
            
            print(f"\n✅ SVG dosyası kaydedildi / SVG file saved:")
            print(f"   {output_file}")
        
        print(f"\n{'='*60}")
        print("✅ İşlem tamamlandı / Operation completed successfully")
        print(f"{'='*60}\n")
        
    except ValueError as e:
        print(f"\n❌ Hata / Error: {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata / Unexpected error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
