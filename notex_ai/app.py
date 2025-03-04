from flask import Flask, request, send_file, jsonify
import os
import uuid
from notex_ai.src.Conversation import Conversation
from pdf2image import convert_from_path
from notex_ai.src.constants import latex_preamble_str, latex_end_str
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_project_folder(project_id: str) -> str:
    """Get the directory path for a specific project.

    Args:
        project_id (str): Unique identifier for the project.

    Returns:
        str: Path to the project folder.
    """
    return os.path.join(UPLOAD_FOLDER, project_id)


def get_latest_files(project_id: str) -> tuple:
    """Retrieve the latest LaTeX and PDF files for a project.

    Args:
        project_id (str): Unique identifier for the project.

    Returns:
        tuple: Paths to the `.tex` and `.pdf` files if they exist, else (None, None).
    """
    project_folder = get_project_folder(project_id)
    tex_file = os.path.join(project_folder, "output.tex")
    pdf_file = os.path.join(project_folder, "output.pdf")

    return (tex_file, pdf_file) if os.path.exists(tex_file) and os.path.exists(pdf_file) else (None, None)


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles file uploads (PDFs or images) and converts them to LaTeX/PDF.

    Returns:
        Response: JSON containing the project ID and the generated PDF path.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_type = file.content_type
    project_id = request.form.get("project_id", str(uuid.uuid4()))

    project_folder = get_project_folder(project_id)
    os.makedirs(project_folder, exist_ok=True)

    conv = Conversation(session_id=project_id, output_dir=project_folder)

    if "pdf" in file_type:
        pdf_path = os.path.join(project_folder, "input.pdf")
        file.save(pdf_path)
        pdf_output_path = conv.process_pdf(pdf_path)
    elif "image" in file_type:
        image_path = os.path.join(project_folder, "input.png")
        file.save(image_path)
        latex_code = conv.process_images([image_path])
        cleaned_latex_code = conv.clean_latex_code(latex_code)
        final_latex = latex_preamble_str + cleaned_latex_code + latex_end_str
        pdf_output_path = conv.compile_latex_text(final_latex)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({"project_id": project_id, "pdf_path": pdf_output_path})


@app.route("/api/download_pdf", methods=["GET"])
def download_pdf():
    """Downloads the compiled PDF for a given project.

    Returns:
        Response: The requested PDF file if available, else an error JSON.
    """
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "No project_id provided"}), 400

    _, pdf_file = get_latest_files(project_id)
    return send_file(pdf_file, as_attachment=True) if pdf_file else jsonify({"error": "File not found"}), 404


# Windows-specific: Ensure `poppler` is in the system path
if os.name == "nt":
    poppler_path = r"C:\path\to\poppler-xx\bin"  # Change this to the actual Poppler path
    os.environ["PATH"] += os.pathsep + poppler_path

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
