from flask import Flask, render_template, request, send_file, jsonify
import os
from converter import convert_pdf_to_audio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/pdfs/'
app.config['AUDIO_FOLDER'] = 'uploads/audio/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
app.secret_key = 'your-secret-key-here'

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400
    
    try:
        filename = file.filename
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)
        
        audio_filename = f"{os.path.splitext(filename)[0]}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        
        convert_pdf_to_audio(pdf_path, audio_path)
        
        return jsonify({
            'success': True,
            'audio_url': f'/download/{audio_filename}',
            'filename': audio_filename
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['AUDIO_FOLDER'], filename),
                     as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
    app.run(debug=True)