# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install system dependencies
# Includes tesseract-ocr, poppler-utils for PDF handling, and LaTeX (for pdflatex)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libpoppler-cpp-dev \
    poppler-utils \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-lang-all \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Set environment variables (optional, if using dotenv or config files)
ENV FLASK_APP=app.py

# Expose port 5000 to allow external access
EXPOSE 5001

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
