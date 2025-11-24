"""
Box Designer - Core module for generating box designs with measurements
"""
import math


class BoxDesigner:
    """
    Generates technical drawings and calculations for various box types
    """
    
    def __init__(self, length, width, height, material_thickness=3):
        """
        Initialize box designer with dimensions (in mm)
        
        Args:
            length: Box length (mm)
            width: Box width (mm)
            height: Box height (mm)
            material_thickness: Material thickness (mm), default 3mm
        """
        self.length = float(length)
        self.width = float(width)
        self.height = float(height)
        self.thickness = float(material_thickness)
        
    def validate_dimensions(self):
        """Validate that dimensions are positive"""
        if self.length <= 0 or self.width <= 0 or self.height <= 0:
            raise ValueError("Tüm ölçüler pozitif olmalıdır / All dimensions must be positive")
        if self.thickness <= 0:
            raise ValueError("Malzeme kalınlığı pozitif olmalıdır / Material thickness must be positive")
        return True
    
    def calculate_standard_box(self):
        """
        Calculate die-cut template for standard folding box (FEFCO 0201)
        Returns coordinates and dimensions for flat template
        """
        self.validate_dimensions()
        
        # Standard box unfolds to: width + height + width + height (for sides)
        # and length for top/bottom flaps
        
        template = {
            'type': 'standard_box',
            'total_width': 2 * (self.width + self.height),
            'total_height': self.length + 2 * self.height,
            'dimensions': {
                'length': self.length,
                'width': self.width,
                'height': self.height,
                'thickness': self.thickness
            },
            'flaps': {
                'top': self.height,
                'bottom': self.height
            }
        }
        
        return template
    
    def calculate_tray_box(self):
        """
        Calculate die-cut template for tray/display box
        """
        self.validate_dimensions()
        
        template = {
            'type': 'tray_box',
            'total_width': self.width + 2 * self.height,
            'total_height': self.length + 2 * self.height,
            'dimensions': {
                'length': self.length,
                'width': self.width,
                'height': self.height,
                'thickness': self.thickness
            },
            'corners': 'cut'  # Corner cuts for folding
        }
        
        return template
    
    def calculate_lid_box(self):
        """
        Calculate die-cut template for box with separate lid
        """
        self.validate_dimensions()
        
        # Lid should be slightly larger
        lid_clearance = self.thickness * 2
        
        template = {
            'type': 'lid_box',
            'box': {
                'total_width': 2 * (self.width + self.height),
                'total_height': self.length + self.height,
                'dimensions': {
                    'length': self.length,
                    'width': self.width,
                    'height': self.height
                }
            },
            'lid': {
                'total_width': 2 * (self.width + lid_clearance + self.height / 2),
                'total_height': self.length + lid_clearance + self.height / 2,
                'dimensions': {
                    'length': self.length + lid_clearance,
                    'width': self.width + lid_clearance,
                    'height': self.height / 2
                }
            },
            'thickness': self.thickness
        }
        
        return template
    
    def calculate_material_area(self, template):
        """Calculate total material area needed (in mm²)"""
        if template['type'] == 'lid_box':
            box_area = template['box']['total_width'] * template['box']['total_height']
            lid_area = template['lid']['total_width'] * template['lid']['total_height']
            return box_area + lid_area
        else:
            return template['total_width'] * template['total_height']
    
    def get_design_specs(self, box_type='standard'):
        """
        Get complete design specifications for a box type
        
        Args:
            box_type: Type of box ('standard', 'tray', 'lid')
            
        Returns:
            Dictionary with complete design specifications
        """
        if box_type == 'standard':
            template = self.calculate_standard_box()
        elif box_type == 'tray':
            template = self.calculate_tray_box()
        elif box_type == 'lid':
            template = self.calculate_lid_box()
        else:
            raise ValueError(f"Bilinmeyen kutu tipi: {box_type} / Unknown box type: {box_type}")
        
        material_area = self.calculate_material_area(template)
        
        specs = {
            'template': template,
            'material_area_mm2': material_area,
            'material_area_m2': material_area / 1000000,
            'box_volume_mm3': self.length * self.width * self.height,
            'box_volume_liters': (self.length * self.width * self.height) / 1000000
        }
        
        return specs
