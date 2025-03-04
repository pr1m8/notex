"""
Handles LaTeX conversion from handwritten notes.
"""

import os
import re
import cv2
import base64
import logging
import subprocess
import numpy as np
from tqdm import tqdm
from PIL import Image
from pdf2image import convert_from_path
from typing import List, Dict
from notex_ai.config import client
from notex_ai.src.constants import latex_preamble_str, latex_end_str, GPT_COST
import uuid
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Conversation:
    """
    Handles a session for processing handwritten notes into LaTeX.
    """

    def __init__(self, session_id: str, output_dir: str) -> None:
        """
        Initializes a Conversation instance.

        Args:
            session_id (str): Unique identifier for the session.
            output_dir (str): Directory where output files are stored.
        """
        self.session_id = session_id
        self.output_dir = output_dir
        self.images_dir = os.path.join(self.output_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        self.total_cost = 0.0

    def preprocess_image(self, image_path: str) -> str:
        """
        Preprocesses an image to enhance readability.

        Args:
            image_path (str): Path to the input image.

        Returns:
            str: Path to the preprocessed image.
        """
        processed_dir = os.path.join(self.output_dir, "processed_images")
        os.makedirs(processed_dir, exist_ok=True)

        logger.info(f"Preprocessing image: {image_path}")
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        processed_image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        preprocessed_image_path = os.path.join(processed_dir, f"{uuid.uuid4()}_processed.png")
        cv2.imwrite(preprocessed_image_path, processed_image)

        return preprocessed_image_path

    def process_images(self, image_paths: List[str]) -> str:
        """
        Converts images into LaTeX code using OpenAI.

        Args:
            image_paths (List[str]): List of image paths.

        Returns:
            str: Generated LaTeX code.
        """
        context = [
            {"role": "system", "content": "Convert these images into LaTeX. No explanations."},
            {"role": "user", "content": [{"type": "image_url", "image_url": {"url": self.encode_image_to_base64(path)}} for path in image_paths]},
        ]
        response = client.chat.completions.create(model="gpt-4o", messages=context)
        return response.choices[0].message.content.strip()

    def clean_latex_code(self, latex_code: str) -> str:
        """
        Cleans up the LaTeX code by removing unnecessary elements.

        Args:
            latex_code (str): Raw LaTeX code.

        Returns:
            str: Cleaned LaTeX code.
        """
        patterns = [
            (r"\\documentclass{.*?}", ""),
            (r"\\usepackage{.*?}", ""),
            (r"\\begin{document}", ""),
            (r"\\end{document}", ""),
            (r"\$\$", r"$"),
        ]
        for pattern, replacement in patterns:
            latex_code = re.sub(pattern, replacement, latex_code, flags=re.DOTALL)
        return latex_code.strip()

    def convert_latex_to_pdf(self, tex_file: str):
        """
        Converts LaTeX code into a PDF.

        Args:
            tex_file (str): Path to the LaTeX file.
        """
        logger.info(f"Compiling LaTeX file: {tex_file}")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", self.output_dir, tex_file])

    def process_pdf(self, pdf_path: str) -> str:
        """
        Processes a PDF file by converting it into images and extracting LaTeX.

        Args:
            pdf_path (str): Path to the input PDF.

        Returns:
            str: Path to the generated PDF.
        """
        pages = convert_from_path(pdf_path, output_folder=self.output_dir)
        image_paths = [self.preprocess_image(os.path.join(self.images_dir, f"page_{i}.png")) for i, page in enumerate(pages)]
        
        latex_code = "\n".join(self.process_images([img]) for img in image_paths)
        final_latex = f"{latex_preamble_str}\n{latex_code}\n{latex_end_str}"

        tex_file = os.path.join(self.output_dir, "output.tex")
        with open(tex_file, "w") as f:
            f.write(final_latex)

        self.convert_latex_to_pdf(tex_file)
        return os.path.join(self.output_dir, "output.pdf")

