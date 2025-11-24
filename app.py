"""
Flask Web Application for Box Designer
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import io
from box_designer import BoxDesigner
from svg_generator import SVGGenerator

app = Flask(__name__)

# Create output directory if it doesn't exist
OUTPUT_DIR = 'output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate_box():
    """Calculate box design specifications"""
    try:
        data = request.json
        
        length = float(data.get('length', 0))
        width = float(data.get('width', 0))
        height = float(data.get('height', 0))
        thickness = float(data.get('thickness', 3))
        box_type = data.get('box_type', 'standard')
        
        designer = BoxDesigner(length, width, height, thickness)
        specs = designer.get_design_specs(box_type)
        
        return jsonify({
            'success': True,
            'specs': specs
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Hata oluştu: {str(e)}'
        }), 500


@app.route('/api/generate-svg', methods=['POST'])
def generate_svg():
    """Generate SVG drawing for box design"""
    try:
        data = request.json
        
        length = float(data.get('length', 0))
        width = float(data.get('width', 0))
        height = float(data.get('height', 0))
        thickness = float(data.get('thickness', 3))
        box_type = data.get('box_type', 'standard')
        
        designer = BoxDesigner(length, width, height, thickness)
        generator = SVGGenerator(designer)
        
        # Generate SVG based on box type
        if box_type == 'standard':
            svg_content = generator.generate_standard_box_svg()
        elif box_type == 'tray':
            svg_content = generator.generate_tray_box_svg()
        else:
            return jsonify({
                'success': False,
                'error': 'Desteklenmeyen kutu tipi / Unsupported box type'
            }), 400
        
        # Return SVG as a file
        svg_buffer = io.BytesIO(svg_content.encode('utf-8'))
        svg_buffer.seek(0)
        
        filename = f'{box_type}_box_{length}x{width}x{height}.svg'
        
        return send_file(
            svg_buffer,
            mimetype='image/svg+xml',
            as_attachment=True,
            download_name=filename
        )
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'SVG oluşturma hatası: {str(e)}'
        }), 500


@app.route('/api/preview-svg', methods=['POST'])
def preview_svg():
    """Generate SVG preview for display in browser"""
    try:
        data = request.json
        
        length = float(data.get('length', 0))
        width = float(data.get('width', 0))
        height = float(data.get('height', 0))
        thickness = float(data.get('thickness', 3))
        box_type = data.get('box_type', 'standard')
        
        designer = BoxDesigner(length, width, height, thickness)
        generator = SVGGenerator(designer)
        
        # Generate SVG based on box type
        if box_type == 'standard':
            svg_content = generator.generate_standard_box_svg()
        elif box_type == 'tray':
            svg_content = generator.generate_tray_box_svg()
        else:
            return jsonify({
                'success': False,
                'error': 'Desteklenmeyen kutu tipi / Unsupported box type'
            }), 400
        
        return jsonify({
            'success': True,
            'svg': svg_content
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'SVG oluşturma hatası: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
