# 📝 Notex

**Notex** is an AI-powered tool that converts handwritten notes, PDFs, and images into structured **LaTeX** documents. It leverages **LLMs**, **computer vision (OCR)**, and **LaTeX formatting corrections** to provide a seamless workflow for generating high-quality, error-free LaTeX documents.

![Notex Banner](https://your-image-url.com/banner.png) <!-- Add a relevant image -->

[![Documentation](https://img.shields.io/badge/docs-readthedocs-green)](https://notex-ai.readthedocs.io/en/latest/)
[![License](https://img.shields.io/github/license/pr1m8/notex-ai)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/notex-ai)](https://pypi.org/project/notex-ai/)
[![Build](https://github.com/pr1m8/notex-ai/actions/workflows/docs.yml/badge.svg)](https://github.com/pr1m8/notex-ai/actions)

---

## 📌 Features

✅ **Convert Handwritten Notes to LaTeX** – Extracts mathematical expressions, text, and formatting.  
✅ **Handles PDFs & Images** – Converts **PDF pages** and **scanned images** into LaTeX code.  
✅ **Error Handling & Auto-Fixing** – Fixes LaTeX compilation issues automatically.  
✅ **Document Structure Detection** – Recognizes **sections, theorems, proofs, equations, exercises** and more.  
✅ **OpenAI & Azure Integration** – Uses LLMs for intelligent text extraction.  
✅ **Fast LaTeX Compilation** – Generates PDFs with error correction.  

---

## 📖 Documentation

**Full Documentation:** 📚 [ReadTheDocs](https://notex.readthedocs.io/en/latest/)  

> The docs include **installation guides, API reference, and examples**.

---

## 🚀 Installation

### **1️⃣ Install via Pip**
```sh
pip install notex
```

### **2️⃣ Install via Poetry**
```sh
poetry add notex
```

### **3️⃣ Install from Source**
```sh
git clone https://github.com/pr1m8/notex.git
cd notex
poetry install
```

---

## ⚡ Usage

### **Convert a PDF or Image to LaTeX**
```python
from notex import Conversation

conv = Conversation(session_id="example", output_dir="output")

# Process a PDF
pdf_path = "input.pdf"
output_pdf = conv.process_pdf(pdf_path)

# Process an Image
image_path = "input.png"
latex_code = conv.process_images([image_path])
```

### **Compile LaTeX to PDF**
```python
final_pdf = conv.compile_latex_text(latex_code)
```

---

## 🛠 Configuration

Notex requires **API keys** for OpenAI/Azure integration.  

### **Setup Environment Variables**
Create a `.env` file:
```ini
AZURE_OPENAI_API_KEY="your-azure-key"
AZURE_URI="your-azure-endpoint"
```

Or use a `config.ini` file:
```ini
[AZURE_OPENAI]
API_KEY="your-key"
URI="your-endpoint"
```

---

## 🖥️ Running the Flask API
Notex includes an **API server** to handle uploads.

```sh
FLASK_APP=notex.app poetry run flask run --host=0.0.0.0 --port=5001
```

Use the API to upload files:
```sh
curl -X POST -F "file=@input.pdf" http://localhost:5001/upload
```

---

## 🏗️ Development & Contribution

Want to contribute? Follow these steps:

### **1️⃣ Fork & Clone**
```sh
git clone https://github.com/pr1m8/notex.git
cd notex
```

### **2️⃣ Install Dependencies**
```sh
poetry install
```

### **3️⃣ Run Tests**
```sh
pytest
```

---

## 🔗 Related Projects
- **[Overleaf](https://www.overleaf.com/)** - Online LaTeX editor  
- **[Pandas](https://pandas.pydata.org/)** - Data processing  
- **[OpenAI](https://platform.openai.com/)** - LLMs  

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🔥 Stay Connected
Follow **@pr1m8** on GitHub for updates and new features!

📢 **Have ideas or feedback?** Open an [issue](https://github.com/pr1m8/notex/issues) or start a [discussion](https://github.com/pr1m8/notex/discussions).

