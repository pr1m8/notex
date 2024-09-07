from typing import List, Dict
from pdf2image import convert_from_path
import base64
import os
import subprocess
import re
import cv2
import numpy as np
from PIL import Image
from src.Client import client
from tqdm import tqdm
import logging
import uuid
import time
import requests

from src.constants import latex_preamble_str, latex_issues_prompt, preamble_instructions, latex_end_str, GPT_COST

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Conversation:
    def __init__(self, session_id: str, output_dir: str) -> None:
        self.session_id = session_id
        self.output_dir = output_dir
        self.images_dir = os.path.join(self.output_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        self.start_time = time.time()
        self.total_cost = 0.0
        self.messages: List[Dict] = []
        
    def preprocess_image(self, image_path: str) -> str:
        processed_dir = os.path.join(self.output_dir, "processed_images")
        os.makedirs(processed_dir, exist_ok=True)

        logger.info(f"Preprocessing image: {image_path}")
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((2, 2), np.uint8)
        denoised = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        kernel = np.array([[0, -1, 0], [-1,  5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        resized = cv2.resize(sharpened, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        preprocessed_image_path = os.path.join(processed_dir, os.path.basename(image_path).replace(".png", "_processed.png"))
        cv2.imwrite(preprocessed_image_path, resized)

    return preprocessed_image_path


    def prepare_image_context(self, image_paths: List[str], title="Title of the Document", author="Author Name") -> List[Dict]:
        images = [{"type": "image_url", "image_url": {"url": self.encode_image_to_base64(path)}} for path in image_paths]
        preamble_instructions = (
            "You are a LaTeX converter. Do not output anything other than the LaTeX code. Ensure the script is valid and has no errors. "
            "Make sure the LaTeX you write is perfect and has no errors. Ensure things are in math-mode when they need to be. "
            "Ensure all commands are finished and have an end. Recognize sections, theorems, proofs, questions, exercises, problems, solutions, "
            "and diagrams and format them properly. Maintain the continuity of the document. Use appropriate LaTeX commands for theorems, definitions, "
            "proofs, exercises, examples, and solutions. Use environments such as \\begin{theorem}...\\end{theorem}, \\begin{definition}...\\end{definition}, "
            "\\begin{proof}...\\end{proof}, \\begin{exercise}...\\end{exercise}, \\begin{problem}...\\end{problem}, \\begin{example}...\\end{example}, and "
            "\\begin{proof}...\\end{proof}. Use \\section{...}, \\subsection{...}, and \\subsubsection{...} to organize the document into clearly defined sections. "
            "Ensure proper spacing between different elements and avoid redundant commands. For diagrams and photographs, describe the content briefly in LaTeX comments. "
            "If photographs or images of text are unclear, make reasonable guesses but note these as comments. Do not include \\documentclass, \\usepackage, \\begin{document}, or \\end{document} commands in your response. "
            "Unescaped Special Characters: Some special characters like underscores (_) and ampersands (&) need to be escaped in LaTeX. "
            "Math Mode Delimiters: Ensure that math mode delimiters ($ or \\[...\\]) are used appropriately. "
            "Incomplete Environments: Make sure all environments are properly opened and closed. "
            "Overlapping Definitions: Ensure definitions are not overlapping and properly formatted. "
            "Remove Extra Symbols and Comments: Ensure there are no residual symbols or comments that could cause LaTeX errors. "
            "Try to link examples and proofs together. "
            "Abstain from undefined control sequences. "
            "When giving a definition, theorem, proposition or anything of that nature, enclose in \\textbf{...} the name of it, followed by descriptions. "
            "Any solutions or proofs should be started with \\begin{proof} and obviously closed by \\end{proof}. "
            "Use \\frac when discussing a fraction. "
            "Do not use solutions unless it's clearly a problem set, use proof instead. "
            "Use sections, subsections, newpage, subsubsection intelligently and discern how information should be organized. "
            "Ensure all environments are properly closed: Make sure each \\begin{...} has a corresponding \\end{...}. "
            "To prevent overflow, make sure to break long equations into multiple lines if necessary. "
            "Ensure that there is no overflow horizontally. Do not use \\textbf{proof} or any variant other than \\begin{proof}. "
            "Use partial sign to denote boundary. "
            "If handwriting is messy, try to use the context to infer as best as you can what the symbol should be. Highlight uncertain entries in red and bold. "
            "Whenever discussing other examples or theorems, or exercises, use \\emph. "
            "Title of the document and author should be predefined or set by the user. Use \\title{%s}, \\author{%s}, and \\date{\\today}. " % (title, author) +
            "Use \\tableofcontents and set a new page for it. "
            "Always ensure figures are loaded correctly, and fill them in if they aren't there. "
            "Definitions, Theorems, Propositions, Problems, etc., should all be stated on the same line they are declared, never escaping a row before that. "
            "Use \\begin{mydefbox} for definitions, \\begin{mythmbox} for theorems, \\begin{myexamplebox} for examples, and \\begin{mypropbox} for propositions."
            "Use align and equation sparingly outside of the boxes above, and in proofs."
            "Try to use a combination of $,center,equation,and align*"
            "Use Sections & Subsections for table of contents."
            "You cannot use placeholders for images - try to crop them or recreate them in latex."
            "Do not use \\O"
        )

        context = [
            {"role": "system", "content": preamble_instructions},
            {"role": "user", "content": [
                {"type": "text", "text": "Convert these images into LaTeX."}
            ] + images}
        ]
        return context


        

    def clean_latex_code(self, latex_code: str) -> str:
        patterns = [
            (r'\\documentclass{.*?}', ''),
            (r'\\usepackage{.*?}', ''),
            (r'\\begin{document}', ''),
            (r'\\end{document}', ''),
            (r'\$\$', r'$'),
            (r'\\\[', r'$'),
            (r'\\\]', r'$'),
            (r'```latex', ''),
            (r'```', ''),
            (r'\n\s*\n', '\n\n'),
            (r'\begin{figure}[H]', r'\begin{figure}')
        ]
        for pattern, replacement in patterns:
            latex_code = re.sub(pattern, replacement, latex_code, flags=re.DOTALL)
        return latex_code.strip()

    def encode_image_to_base64(self, image_path: str) -> str:
        logger.info(f"Encoding image to base64: {image_path}")
        with open(image_path, "rb") as image_file:
            base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{base64_encoded_image}"

    def get_openai_response(self, context, stream=False):
        logger.info("Requesting response from OpenAI.")
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=context,
            stream=stream
        )

        # Calculate cost based on token usage
        if 'usage' in response:
            input_tokens = response['usage']['prompt_tokens']
            output_tokens = response['usage']['completion_tokens']
        else:
            # In case usage field is missing, default to zero (for testing purposes)
            input_tokens = 0
            output_tokens = 0

        # Calculate the cost using the GPT_COST dictionary
        input_cost = (input_tokens / 1_000_000) * GPT_COST['input_token_cost']
        output_cost = (output_tokens / 1_000_000) * GPT_COST['output_token_cost']
        cost = input_cost + output_cost

        self.total_cost += cost
        logger.info(f"Cost of this run: ${cost:.2f}")
        
        # Check for the finish_reason flag and handle it
        if response.choices[0].finish_reason == 'length':
            logger.info("Response truncated, sending 'please continue' prompt.")
            context.append({"role": "user", "content": "Please continue."})
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=context,
                stream=stream
            )
        return response

    def process_images(self, image_paths: List[str]) -> str:
        context = self.prepare_image_context(image_paths)
        response = self.get_openai_response(context)
        latex_code = response.choices[0].message.content.strip()
        return latex_code

    def save_latex_to_file(self, latex_code: str, file_path: str):
        logger.info(f"Saving LaTeX code to {file_path}.")
        with open(file_path, 'w') as f:
            f.write(latex_code)

    def convert_latex_to_pdf(self, tex_file: str):
        logger.info(f"Compiling LaTeX file {tex_file} to PDF in directory {self.output_dir}.")
        try:
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', self.output_dir, tex_file],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            logger.info(f"LaTeX compilation stdout: {result.stdout.decode('utf-8', errors='ignore')}")
            logger.error(f"LaTeX compilation stderr: {result.stderr.decode('utf-8', errors='ignore')}")
            if result.returncode != 0:
                logger.warning(f"LaTeX compilation completed with errors. Return code: {result.returncode}")
            if not os.path.exists(os.path.join(self.output_dir, "output.pdf")):
                raise FileNotFoundError("Compiled PDF not found in output directory.")
        except subprocess.TimeoutExpired:
            logger.error("LaTeX compilation timed out.")
            raise RuntimeError("LaTeX compilation timed out.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during LaTeX compilation: {e}")
            raise

    def process_pdf(self, pdf_path: str) -> str:
        pages = convert_from_path(pdf_path, output_folder=self.output_dir)
        image_paths = []
        for i, page in enumerate(tqdm(pages, desc="Converting PDF pages to images")):
            image_path = os.path.join(self.images_dir, f"temp_page_{i}.png")
            page.save(image_path, "PNG")
            preprocessed_image_path = self.preprocess_image(image_path)
            image_paths.append(preprocessed_image_path)

        latex_parts = []
        for image_path in tqdm(image_paths, desc="Processing images to LaTeX"):
            latex_output = self.process_images([image_path])
            latex_parts.append(latex_output)

        combined_latex = self.clean_latex_code("\n".join(latex_parts))
        final_latex = latex_preamble_str + combined_latex + latex_end_str

        tex_file = os.path.join(self.output_dir, "output.tex")
        self.save_latex_to_file(final_latex, tex_file)

        try:
            self.convert_latex_to_pdf(tex_file)
            final_pdf_path = os.path.join(self.output_dir, "output.pdf")
            if not os.path.exists(final_pdf_path):
                raise FileNotFoundError("Compiled PDF not found in output directory.")
        except RuntimeError as e:
            logger.error(f"LaTeX compilation failed, attempting to fix: {e}")
            fixed_tex_file = self.fix_latex_errors(tex_file)
            try:
                self.convert_latex_to_pdf(fixed_tex_file)
                final_pdf_path = os.path.join(self.output_dir, "output_fixed.pdf")
                if not os.path.exists(final_pdf_path):
                    raise FileNotFoundError("Compiled PDF not found in output directory after fixing.")
            except RuntimeError as e:
                logger.error(f"Failed after fixing LaTeX errors: {e}")
                raise e

        return final_pdf_path

    def fix_latex_errors(self, tex_file: str) -> str:
        logger.info(f"Fixing LaTeX errors in {tex_file}.")
        with open(tex_file, 'r') as file:
            latex_code = file.read()

        error_context = [
            {"role": "system", "content": (
                "You are a LaTeX error fixer. Fix any LaTeX errors, ensuring the code is valid and the document is well-structured. "
                "Only output LaTeX. Do not output anything else. "
                + preamble_instructions + latex_issues_prompt + latex_preamble_str
            )},
            {"role": "user", "content": latex_code}
        ]

        response = self.get_openai_response(error_context)
        fixed_latex = response.choices[0].message.content.strip()
        while response.choices[0].finish_reason == 'length':
            logger.info("Response truncated, sending 'please continue' prompt.")
            error_context.append({"role": "user", "content": "Please continue."})
            response = self.get_openai_response(error_context)
            fixed_latex += response.choices[0].message.content.strip()
        fixed_latex = self.clean_latex_code(fixed_latex)

        final_fixed_latex = latex_preamble_str + fixed_latex + latex_end_str

        fixed_tex_file = tex_file.replace(".tex", "_fixed.tex")
        with open(fixed_tex_file, 'w') as file:
            file.write(final_fixed_latex)

        logger.info(f"Fixed LaTeX code saved to {fixed_tex_file}.")
        return fixed_tex_file
