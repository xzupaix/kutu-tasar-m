"""
Test script for Box Designer functionality
"""
from box_designer import BoxDesigner
from svg_generator import SVGGenerator
import os


def test_box_designer():
    """Test basic box designer functionality"""
    print("🧪 Testing Box Designer...\n")
    
    # Test 1: Create a standard box
    print("Test 1: Standard Box Creation")
    designer = BoxDesigner(length=200, width=150, height=100, material_thickness=3)
    
    try:
        designer.validate_dimensions()
        print("✅ Dimension validation passed")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False
    
    # Test 2: Calculate standard box template
    print("\nTest 2: Standard Box Template Calculation")
    try:
        template = designer.calculate_standard_box()
        print(f"✅ Template created: {template['type']}")
        print(f"   Total Width: {template['total_width']} mm")
        print(f"   Total Height: {template['total_height']} mm")
    except Exception as e:
        print(f"❌ Template calculation failed: {e}")
        return False
    
    # Test 3: Calculate tray box template
    print("\nTest 3: Tray Box Template Calculation")
    try:
        template = designer.calculate_tray_box()
        print(f"✅ Template created: {template['type']}")
        print(f"   Total Width: {template['total_width']} mm")
        print(f"   Total Height: {template['total_height']} mm")
    except Exception as e:
        print(f"❌ Tray box calculation failed: {e}")
        return False
    
    # Test 4: Calculate lid box template
    print("\nTest 4: Lid Box Template Calculation")
    try:
        template = designer.calculate_lid_box()
        print(f"✅ Template created: {template['type']}")
        print(f"   Box Width: {template['box']['total_width']} mm")
        print(f"   Lid Width: {template['lid']['total_width']} mm")
    except Exception as e:
        print(f"❌ Lid box calculation failed: {e}")
        return False
    
    # Test 5: Get complete design specs
    print("\nTest 5: Complete Design Specifications")
    try:
        specs = designer.get_design_specs('standard')
        print(f"✅ Design specs generated")
        print(f"   Material Area: {specs['material_area_m2']:.4f} m²")
        print(f"   Box Volume: {specs['box_volume_liters']:.2f} L")
    except Exception as e:
        print(f"❌ Design specs failed: {e}")
        return False
    
    # Test 6: SVG Generation
    print("\nTest 6: SVG Generation")
    try:
        generator = SVGGenerator(designer)
        svg_content = generator.generate_standard_box_svg()
        print(f"✅ Standard box SVG generated ({len(svg_content)} bytes)")
        
        svg_content = generator.generate_tray_box_svg()
        print(f"✅ Tray box SVG generated ({len(svg_content)} bytes)")
    except Exception as e:
        print(f"❌ SVG generation failed: {e}")
        return False
    
    # Test 7: Invalid dimensions
    print("\nTest 7: Invalid Dimension Handling")
    try:
        invalid_designer = BoxDesigner(length=-100, width=150, height=100)
        invalid_designer.validate_dimensions()
        print("❌ Should have raised an error for negative dimensions")
        return False
    except ValueError as e:
        print(f"✅ Correctly rejected invalid dimensions: {e}")
    
    # Test 8: Different box sizes
    print("\nTest 8: Multiple Box Sizes")
    test_cases = [
        (100, 100, 50),   # Small cube-like
        (300, 200, 150),  # Medium box
        (500, 400, 200),  # Large box
        (50, 50, 50),     # Tiny cube
    ]
    
    for length, width, height in test_cases:
        try:
            d = BoxDesigner(length, width, height)
            specs = d.get_design_specs('standard')
            print(f"✅ Box {length}x{width}x{height}: {specs['material_area_m2']:.4f} m²")
        except Exception as e:
            print(f"❌ Failed for {length}x{width}x{height}: {e}")
            return False
    
    print("\n" + "="*50)
    print("✅ All tests passed successfully!")
    print("="*50)
    return True


def test_sample_output():
    """Generate sample SVG files"""
    print("\n📄 Generating sample SVG files...\n")
    
    # Create output directory
    output_dir = '/tmp/box_designs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample box 1: Standard shipping box
    print("Generating standard box (200x150x100mm)...")
    designer1 = BoxDesigner(200, 150, 100, 3)
    generator1 = SVGGenerator(designer1)
    svg1 = generator1.generate_standard_box_svg()
    
    output_file1 = os.path.join(output_dir, 'standard_box_200x150x100.svg')
    with open(output_file1, 'w') as f:
        f.write(svg1)
    print(f"✅ Saved to: {output_file1}")
    
    # Sample box 2: Display tray
    print("\nGenerating tray box (300x200x80mm)...")
    designer2 = BoxDesigner(300, 200, 80, 3)
    generator2 = SVGGenerator(designer2)
    svg2 = generator2.generate_tray_box_svg()
    
    output_file2 = os.path.join(output_dir, 'tray_box_300x200x80.svg')
    with open(output_file2, 'w') as f:
        f.write(svg2)
    print(f"✅ Saved to: {output_file2}")
    
    print("\n✅ Sample SVG files generated successfully!")


if __name__ == '__main__':
    print("="*50)
    print("Box Design Automation - Test Suite")
    print("="*50 + "\n")
    
    # Run tests
    success = test_box_designer()
    
    if success:
        test_sample_output()
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        exit(1)
