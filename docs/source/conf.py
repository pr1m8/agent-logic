# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

project = "agent-logic"
copyright = "2025, William R. Astley (Pr1m8)"
author = "William R. Astley (Pr1m8)"
release = "0.1.0"


sys.path.insert(0, os.path.abspath("../../agent_logic"))
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # for Google and NumPy docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    # "sphinx_tabs.tabs",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.youtube",
    "sphinxext.opengraph",
    "sphinx_rtd_theme",  # optional backup
    "sphinx_needs",  # advanced requirements diagrams
    "sphinx_sitemap",  # sitemap.xml for SEO
]

html_baseurl = "https://agent-logic.readthedocs.io/en/latest/"

templates_path = ["_templates"]
exclude_patterns = []


autosummary_generate = True
autodoc_typehints = "description"  # clean type hints in docstrings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "show-inheritance": True,
}
todo_include_todos = True

# Myst-parser settings if using Markdown
myst_enable_extensions = [
    "deflist",
    "fieldlist",
    "html_image",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
