import sys
from pathlib import Path

sys.path.insert(0, str(Path('../..').resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Mininet'
copyright = '2025, Ethan Iannicelli'
author = 'Ethan Iannicelli'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.imgconverter'
]

latex_elements = {
    'extraclassoptions': 'openany,oneside'  # Avoid blank pages in PDFs
}

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
