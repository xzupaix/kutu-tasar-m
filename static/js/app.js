// Box Designer Application JavaScript

let currentSpecs = null;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('boxForm');
    const previewBtn = document.getElementById('previewBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    
    form.addEventListener('submit', handleCalculate);
    previewBtn.addEventListener('click', handlePreview);
    downloadBtn.addEventListener('click', handleDownload);
});

async function handleCalculate(e) {
    e.preventDefault();
    
    const formData = {
        length: parseFloat(document.getElementById('length').value),
        width: parseFloat(document.getElementById('width').value),
        height: parseFloat(document.getElementById('height').value),
        thickness: parseFloat(document.getElementById('thickness').value),
        box_type: document.getElementById('box_type').value
    };
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSpecs = data.specs;
            displayResults(data.specs);
            document.getElementById('previewBtn').disabled = false;
            document.getElementById('downloadBtn').disabled = false;
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Bağlantı hatası: ' + error.message);
    }
}

async function handlePreview() {
    if (!currentSpecs) {
        showError('Lütfen önce hesaplama yapın');
        return;
    }
    
    const formData = {
        length: parseFloat(document.getElementById('length').value),
        width: parseFloat(document.getElementById('width').value),
        height: parseFloat(document.getElementById('height').value),
        thickness: parseFloat(document.getElementById('thickness').value),
        box_type: document.getElementById('box_type').value
    };
    
    try {
        const response = await fetch('/api/preview-svg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            const previewDiv = document.getElementById('svgPreview');
            previewDiv.innerHTML = data.svg;
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Önizleme oluşturma hatası: ' + error.message);
    }
}

async function handleDownload() {
    const formData = {
        length: parseFloat(document.getElementById('length').value),
        width: parseFloat(document.getElementById('width').value),
        height: parseFloat(document.getElementById('height').value),
        thickness: parseFloat(document.getElementById('thickness').value),
        box_type: document.getElementById('box_type').value
    };
    
    try {
        const response = await fetch('/api/generate-svg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${formData.box_type}_box_${formData.length}x${formData.width}x${formData.height}.svg`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showSuccess('SVG dosyası indirildi!');
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('İndirme hatası: ' + error.message);
    }
}

function displayResults(specs) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '<div style="line-height: 2;">';
    
    // Display template information
    const template = specs.template;
    html += '<h4>📦 Şablon Bilgileri / Template Information</h4>';
    html += `<p><strong>Kutu Tipi / Box Type:</strong> ${template.type}</p>`;
    
    if (template.type !== 'lid_box') {
        html += `<p><strong>Toplam Genişlik / Total Width:</strong> ${template.total_width.toFixed(2)} mm</p>`;
        html += `<p><strong>Toplam Yükseklik / Total Height:</strong> ${template.total_height.toFixed(2)} mm</p>`;
    }
    
    // Display dimensions
    const dims = template.dimensions || template.box.dimensions;
    html += '<h4 style="margin-top: 15px;">📏 Ölçüler / Dimensions</h4>';
    html += `<p><strong>Uzunluk / Length:</strong> ${dims.length} mm</p>`;
    html += `<p><strong>Genişlik / Width:</strong> ${dims.width} mm</p>`;
    html += `<p><strong>Yükseklik / Height:</strong> ${dims.height} mm</p>`;
    
    // Display material and volume information
    html += '<h4 style="margin-top: 15px;">📊 Malzeme ve Hacim / Material & Volume</h4>';
    html += `<p><strong>Malzeme Alanı / Material Area:</strong> ${specs.material_area_m2.toFixed(4)} m² (${specs.material_area_mm2.toFixed(0)} mm²)</p>`;
    html += `<p><strong>Kutu Hacmi / Box Volume:</strong> ${specs.box_volume_liters.toFixed(2)} L (${specs.box_volume_mm3.toFixed(0)} mm³)</p>`;
    
    html += '</div>';
    
    resultsContent.innerHTML = html;
    resultsDiv.style.display = 'block';
}

function showError(message) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsContent.innerHTML = `<div class="error-message">❌ ${message}</div>`;
    resultsDiv.style.display = 'block';
}

function showSuccess(message) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = '✅ ' + message;
    resultsContent.insertBefore(successDiv, resultsContent.firstChild);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}
