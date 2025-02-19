# Notex

## 📌 Overview
Notex is a lightweight and extensible application that converts handwritten notes into LaTeX code, generating well-formatted PDF documents. It originally implemented a basic reflection technique, reading LaTeX compile errors and rewriting the code as if it were a traditional branching structure. This approach was ahead of its time, structuring output before structured output models and output parsers became widely used.

The application consists of a **client and a core processing engine**:
- The **client** interacts with OpenAI's agent to process handwritten input and generate structured LaTeX.
- The **conversation file** handles all of the LaTeX processing, error handling, and iteration to refine the generated output.

Notex is designed to work without the OpenAI API if necessary, allowing for manual LaTeX handling. The core application runs using **Flask** as a backend service, facilitating communication between the client and the processing pipeline.

## 🚀 Features
- Secure authentication
- Integration with Azure OpenAI, Firebase, MongoDB, and financial APIs
- AI-driven insights with TimeGPT
- Configurable and extensible architecture
- Handwritten note-to-LaTeX conversion
- Automated LaTeX error correction and iterative compilation
- Flask-based backend for structured interaction

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
 git clone https://github.com/yourusername/notex.git
 cd notex
```

### **2️⃣ Install Dependencies**
```sh
 pip install -r requirements.txt
```

### **3️⃣ Install LaTeX**
You need to install LaTeX for your operating system:
- **Ubuntu/Linux**:
  ```sh
  sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
  ```
- **MacOS** (via MacTeX):
  ```sh
  brew install mactex
  ```
- **Windows**:
  Download and install [MiKTeX](https://miktex.org/download).

### **4️⃣ Configure Environment Variables**
Copy the example config and update it with your credentials.
```sh
 cp config.example.ini config.ini
```
Then, edit `config.ini` with your API keys and database credentials.

## 📚 Usage
To start the application, run:
```sh
python app.py
```
This will launch the Flask server, which the client will interact with.

For more details, check the [Usage Guide](docs/usage.md).

## 📄 Configuration
Configuration is managed through `config.ini`. Refer to [Configuration Guide](docs/config.md) for details.

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

## 💡 Acknowledgements
- OpenAI
- Firebase
- MongoDB
- Azure
- Financial Modeling Prep

