# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyhms'
copyright = '2024, Barron H. Henderson'
author = 'Barron H. Henderson'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    'matplotlib.sphinxext.plot_directive',
    'sphinx_copybutton',
    'sphinx_design',
    'myst_nb',
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.napoleon',
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for Gallery --

sphinx_gallery_conf = {
     'examples_dirs': '../examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path to where to save gallery generated output
}