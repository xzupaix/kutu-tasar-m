"""
SVG Generator - Creates technical drawing SVG files for box designs
"""
import svgwrite
from box_designer import BoxDesigner


class SVGGenerator:
    """
    Generates SVG technical drawings for box die-cut templates
    """
    
    def __init__(self, designer: BoxDesigner):
        self.designer = designer
        self.scale = 1  # pixels per mm
        self.margin = 50  # margin in pixels
        
    def generate_standard_box_svg(self, filename='standard_box.svg'):
        """Generate SVG for standard folding box"""
        template = self.designer.calculate_standard_box()
        
        total_width = template['total_width'] * self.scale + 2 * self.margin
        total_height = template['total_height'] * self.scale + 2 * self.margin
        
        dwg = svgwrite.Drawing(filename, size=(f'{total_width}px', f'{total_height}px'))
        
        # Add title and dimensions
        self._add_title(dwg, f"Standard Kutu - {template['dimensions']['length']}x{template['dimensions']['width']}x{template['dimensions']['height']}mm")
        
        # Base coordinates
        x0 = self.margin
        y0 = self.margin
        
        L = template['dimensions']['length']
        W = template['dimensions']['width']
        H = template['dimensions']['height']
        
        # Draw the unfolded box template
        # Bottom flap
        self._draw_rectangle(dwg, x0 + W, y0, W, H, 'Taban Kanat / Bottom Flap')
        
        # Bottom
        self._draw_rectangle(dwg, x0 + W, y0 + H, W, L, 'Taban / Bottom')
        
        # Sides
        self._draw_rectangle(dwg, x0, y0 + H, W, L, 'Yan / Side 1')
        self._draw_rectangle(dwg, x0 + W * 2, y0 + H, W, L, 'Yan / Side 2')
        
        # End panels
        self._draw_rectangle(dwg, x0 + W, y0 + H, W, L, 'Ön / Front', fill='none')
        
        # Top
        self._draw_rectangle(dwg, x0 + W, y0 + H + L, W, L, 'Üst / Top')
        
        # Top flap
        self._draw_rectangle(dwg, x0 + W, y0 + H + L + L, W, H, 'Üst Kanat / Top Flap')
        
        # Add fold lines (dashed)
        self._add_fold_lines(dwg, x0, y0, W, H, L)
        
        # Add dimensions
        self._add_dimension_lines(dwg, template, x0, y0)
        
        return dwg.tostring()
    
    def generate_tray_box_svg(self, filename='tray_box.svg'):
        """Generate SVG for tray/display box"""
        template = self.designer.calculate_tray_box()
        
        total_width = template['total_width'] * self.scale + 2 * self.margin
        total_height = template['total_height'] * self.scale + 2 * self.margin
        
        dwg = svgwrite.Drawing(filename, size=(f'{total_width}px', f'{total_height}px'))
        
        self._add_title(dwg, f"Tepsi Kutu - {template['dimensions']['length']}x{template['dimensions']['width']}x{template['dimensions']['height']}mm")
        
        x0 = self.margin
        y0 = self.margin
        
        L = template['dimensions']['length']
        W = template['dimensions']['width']
        H = template['dimensions']['height']
        
        # Draw base
        self._draw_rectangle(dwg, x0 + H, y0 + H, W, L, 'Taban / Base')
        
        # Draw sides with corner cuts
        # Left side
        self._draw_rectangle(dwg, x0, y0 + H, H, L, 'Sol Yan / Left')
        
        # Right side
        self._draw_rectangle(dwg, x0 + H + W, y0 + H, H, L, 'Sağ Yan / Right')
        
        # Front
        self._draw_rectangle(dwg, x0 + H, y0, W, H, 'Ön / Front')
        
        # Back
        self._draw_rectangle(dwg, x0 + H, y0 + H + L, W, H, 'Arka / Back')
        
        # Add corner cut indicators
        self._add_corner_cuts(dwg, x0, y0, W, H, L)
        
        # Add fold lines
        self._add_fold_lines_tray(dwg, x0, y0, W, H, L)
        
        return dwg.tostring()
    
    def _draw_rectangle(self, dwg, x, y, width, height, label='', fill='none'):
        """Draw a rectangle with label"""
        rect = dwg.rect(
            insert=(x * self.scale, y * self.scale),
            size=(width * self.scale, height * self.scale),
            fill=fill,
            stroke='black',
            stroke_width=2
        )
        dwg.add(rect)
        
        if label:
            text = dwg.text(
                label,
                insert=((x + width/2) * self.scale, (y + height/2) * self.scale),
                text_anchor='middle',
                font_size='12px',
                fill='blue'
            )
            dwg.add(text)
    
    def _add_title(self, dwg, title):
        """Add title to the drawing"""
        text = dwg.text(
            title,
            insert=(self.margin, self.margin - 20),
            font_size='16px',
            font_weight='bold',
            fill='black'
        )
        dwg.add(text)
    
    def _add_fold_lines(self, dwg, x0, y0, W, H, L):
        """Add dashed lines to indicate folds"""
        # Horizontal fold lines
        lines = [
            (x0, y0 + H, x0 + W * 3, y0 + H),
            (x0, y0 + H + L, x0 + W * 3, y0 + H + L),
        ]
        
        for x1, y1, x2, y2 in lines:
            line = dwg.line(
                start=(x1 * self.scale, y1 * self.scale),
                end=(x2 * self.scale, y2 * self.scale),
                stroke='red',
                stroke_width=1,
                stroke_dasharray='5,5'
            )
            dwg.add(line)
    
    def _add_fold_lines_tray(self, dwg, x0, y0, W, H, L):
        """Add fold lines for tray box"""
        lines = [
            (x0 + H, y0, x0 + H, y0 + H + L + H),
            (x0 + H + W, y0, x0 + H + W, y0 + H + L + H),
            (x0, y0 + H, x0 + H + W + H, y0 + H),
            (x0, y0 + H + L, x0 + H + W + H, y0 + H + L),
        ]
        
        for x1, y1, x2, y2 in lines:
            line = dwg.line(
                start=(x1 * self.scale, y1 * self.scale),
                end=(x2 * self.scale, y2 * self.scale),
                stroke='red',
                stroke_width=1,
                stroke_dasharray='5,5'
            )
            dwg.add(line)
    
    def _add_corner_cuts(self, dwg, x0, y0, W, H, L):
        """Add corner cut indicators"""
        # Small diagonal lines at corners
        corner_size = 10
        corners = [
            (x0, y0 + H),
            (x0, y0 + H + L),
            (x0 + H + W + H, y0 + H),
            (x0 + H + W + H, y0 + H + L),
        ]
        
        for cx, cy in corners:
            line = dwg.line(
                start=(cx * self.scale, cy * self.scale),
                end=((cx + corner_size) * self.scale, (cy + corner_size) * self.scale),
                stroke='orange',
                stroke_width=2
            )
            dwg.add(line)
    
    def _add_dimension_lines(self, dwg, template, x0, y0):
        """Add dimension annotations"""
        dims = template['dimensions']
        
        # Add dimension text
        dim_text = f"L: {dims['length']}mm × W: {dims['width']}mm × H: {dims['height']}mm"
        text = dwg.text(
            dim_text,
            insert=(self.margin, self.margin - 5),
            font_size='12px',
            fill='green'
        )
        dwg.add(text)
