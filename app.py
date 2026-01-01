from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from utils.yolo_detector import detect_and_extract_document
from utils.dewarper import dewarp_document
from utils.upscaler import upscale_image
import shutil

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp/uploads'
app.config['PROCESSED_FOLDER'] = 'temp/processed'
app.config['MODEL_PATH'] = 'models/trainedYOLO.pt'

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_session_files(session_id):
    """Clean up all files associated with a session"""
    try:
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], session_id)
        
        if os.path.exists(upload_path):
            shutil.rmtree(upload_path)
        if os.path.exists(processed_path):
            shutil.rmtree(processed_path)
    except Exception as e:
        print(f"Error cleaning up session files: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create session directories
        session_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        session_processed_dir = os.path.join(app.config['PROCESSED_FOLDER'], session_id)
        os.makedirs(session_upload_dir, exist_ok=True)
        os.makedirs(session_processed_dir, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(session_upload_dir, filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': filename
        }), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/process', methods=['POST'])
def process_document():
    data = request.get_json()
    session_id = data.get('session_id')
    filename = data.get('filename')
    
    if not session_id or not filename:
        return jsonify({'error': 'Missing session_id or filename'}), 400
    
    try:
        # Paths
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id, filename)
        processed_dir = os.path.join(app.config['PROCESSED_FOLDER'], session_id)
        
        # Step 1: YOLO Detection and Mask Extraction
        step1_output = os.path.join(processed_dir, 'step1_extracted.png')
        success = detect_and_extract_document(
            input_path, 
            app.config['MODEL_PATH'], 
            step1_output
        )
        
        if not success:
            return jsonify({'error': 'Document detection failed. No document found in image.'}), 400
        
        # Step 2: Dewarping and Background Removal
        step2_output = os.path.join(processed_dir, 'step2_dewarped.png')
        success = dewarp_document(step1_output, step2_output)
        
        if not success:
            return jsonify({'error': 'Dewarping failed. Could not straighten document borders.'}), 400
        
        # Step 3: Upscaling with Real-ESRGAN
        final_output = os.path.join(processed_dir, 'final_upscaled.png')
        success = upscale_image(step2_output, final_output)
        
        if not success:
            return jsonify({'error': 'Upscaling failed.'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Document processed successfully',
            'result_path': f'/download/{session_id}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/download/<session_id>')
def download_file(session_id):
    try:
        final_output = os.path.join(app.config['PROCESSED_FOLDER'], session_id, 'final_upscaled.png')
        
        if not os.path.exists(final_output):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            final_output,
            as_attachment=True,
            download_name='processed_document.png',
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/cleanup/<session_id>', methods=['POST'])
def cleanup_session(session_id):
    """Endpoint to clean up session files after download"""
    try:
        cleanup_session_files(session_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': f'Cleanup error: {str(e)}'}), 500

@app.route('/preview/<session_id>')
def preview_result(session_id):
    """Endpoint to preview the processed image before download"""
    try:
        final_output = os.path.join(app.config['PROCESSED_FOLDER'], session_id, 'final_upscaled.png')
        
        if not os.path.exists(final_output):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(final_output, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': f'Preview error: {str(e)}'}), 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
