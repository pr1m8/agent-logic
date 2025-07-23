# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Project information -----------------------------------------------------

project = "agentic-logic"
author = "William R. Astley (Pr1m8)"
copyright = "2025, William R. Astley (Pr1m8)"
release = "0.1.0"

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath("../../agent_logic"))

# -- General configuration ---------------------------------------------------

master_doc = "index"  # <- ✅ Ensures Sphinx builds from index.rst

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.youtube",
    "sphinxext.opengraph",
    "sphinx_rtd_theme",
    "sphinx_needs",
    "sphinx_sitemap",
]

autosummary_generate = True  # <- ✅ Generates the generated/*.rst files
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "show-inheritance": True,
}
todo_include_todos = True

templates_path = ["_templates"]
exclude_patterns = []

# -- Myst-parser configuration -----------------------------------------------

myst_enable_extensions = [
    "deflist",
    "fieldlist",
    "html_image",
]

# -- HTML output -------------------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
html_baseurl = "https://agent-logic.readthedocs.io/en/latest/"
