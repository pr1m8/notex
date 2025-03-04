# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'notex'
copyright = '2025, William R. Astley <william.astley@algebraicwealth.com>'
author = 'William R. Astley <william.astley@algebraicwealth.com>'
release = '0.1.0'
import os
import sys
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath("../.."))

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",        # Extracts docstrings
    "sphinx.ext.autosummary",     # Generates summaries for modules
    "sphinx.ext.napoleon",        # Supports Google/NumPy-style docstrings
    "sphinx.ext.viewcode",        # Links to source code
    "sphinx_autodoc_typehints",   # Adds type hints to docs
]

# Ensure autosummary generates stub files automatically
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
}

# Theme
html_theme = "sphinx_rtd_theme"
