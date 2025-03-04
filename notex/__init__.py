"""
Notex: A Python package for converting handwritten notes into LaTeX.

Provides:
- PDF/Image to LaTeX conversion
- Error correction for LaTeX
- API for processing handwritten notes

Modules:
    - `app`: Flask API
    - `config`: Handles environment variables
    - `src.Conversation`: Core LaTeX processing
    - `src.constants`: LaTeX constants

"""

__version__ = "0.1.0"
import os
# Avoid unnecessary imports during Sphinx builds
if os.getenv("SPHINX_BUILD") != "1":
    from . import app  # Only import when NOT building docs

__all__ = ["config", "src"]
