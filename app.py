from flask import Flask, request, send_file, jsonify
import os
import uuid
from src.Conversation import *
from pdf2image import convert_from_path

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_project_folder(project_id):
    return os.path.join(UPLOAD_FOLDER, project_id)

def get_latest_files(project_id):
    project_folder = get_project_folder(project_id)
    tex_file = os.path.join(project_folder, 'output.tex')
    pdf_file = os.path.join(project_folder, 'output.pdf')
    
    if os.path.exists(tex_file) and os.path.exists(pdf_file):
        return tex_file, pdf_file
    else:
        return None, None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    file_type = file.content_type
    project_id = request.form.get('project_id', str(uuid.uuid4()))  # Use existing project ID or generate new one

    project_folder = get_project_folder(project_id)
    os.makedirs(project_folder, exist_ok=True)

    conv = Conversation(session_id=project_id, output_dir=project_folder)

    if 'pdf' in file_type:
        pdf_path = os.path.join(project_folder, "input.pdf")
        file.save(pdf_path)
        pdf_output_path = conv.process_pdf(pdf_path)
    elif 'image' in file_type:
        image_path = os.path.join(project_folder, "input.png")
        file.save(image_path)
        latex_code = conv.process_images([image_path])
        cleaned_latex_code = conv.clean_latex_code(latex_code)
        final_latex = latex_preamble_str + cleaned_latex_code + latex_end_str
        pdf_output_path = conv.compile_latex_text(final_latex)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({"project_id": project_id, "pdf_path": pdf_output_path})

@app.route('/api/download_pdf', methods=['GET'])
def download_pdf():
    project_id = request.args.get('project_id')
    if not project_id:
        return jsonify({'error': 'No project_id provided'}), 400

    _, pdf_file = get_latest_files(project_id)
    if pdf_file:
        return send_file(pdf_file, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if os.name == 'nt':  # For Windows
    poppler_path = r"C:\path\to\poppler-xx\bin"
    os.environ["PATH"] += os.pathsep + poppler_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

