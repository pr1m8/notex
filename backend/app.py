import os
from flask import Flask, request, jsonify, send_file
from Conversation import Conversation
from dotenv import load_dotenv
import subprocess
from tempfile import NamedTemporaryFile

load_dotenv()

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_type = file.content_type

    conv = Conversation(session_id="example_session")

    if 'pdf' in file_type:
        pdf_path = "temp_upload.pdf"
        file.save(pdf_path)
        latex_code = conv.process_pdf(pdf_path)
    elif 'image' in file_type:
        image_path = "temp_upload.png"
        file.save(image_path)
        latex_code = conv.process_images([image_path], is_first_page=True, is_last_page=True)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # Clean up the LaTeX code
    latex_code = latex_code.replace('```latex', '').replace('```', '')

    # Print LaTeX output to console for debugging
    print(f"Generated LaTeX: {latex_code}")

    # Compile the LaTeX code to PDF using Docker
    pdf_data = compile_latex_docker(latex_code)
    if pdf_data is None:
        return jsonify({"error": "Failed to compile LaTeX"}), 500

    # Save the compiled PDF to a file
    with NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        pdf_file.write(pdf_data)
        pdf_file_path = pdf_file.name

    return send_file(pdf_file_path, as_attachment=True, attachment_filename='output.pdf')

@app.route('/compile', methods=['POST'])
def compile_latex():
    data = request.json
    latex_code = data.get('latex')

    if not latex_code:
        return {"error": "No LaTeX code provided"}, 400

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        tex_file_path = os.path.join(tmpdirname, "document.tex")
        pdf_file_path = os.path.join(tmpdirname, "document.pdf")

        # Write LaTeX code to a .tex file
        with open(tex_file_path, "w") as tex_file:
            tex_file.write(latex_code)

        # Compile the .tex file to a .pdf file
        result = subprocess.run(['pdflatex', '-output-directory', tmpdirname, tex_file_path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return {"error": "Failed to compile LaTeX", "details": result.stderr.decode('utf-8')}, 500

        # Return the PDF file
        return send_file(pdf_file_path, as_attachment=True, attachment_filename="document.pdf")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,)
