# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'ultraspy'
copyright = 'MIT License'
author = 'Pierre Ecarlat'

# The full version, including alpha/beta/rc tags
release = 'alpha 0.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx_tabs.tabs',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Added manually; to document both the contents of the header of the classes
# and their init methods
autoclass_content = 'both'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Logo title
html_logo = "images/image4us.png"
html_theme_options = {
    'logo_only': False,
    'display_version': False,
}


# -- Options for LaTex output -------------------------------------------------

# Avoid blank page used for duplex printing.
latex_elements = {
  'extraclassoptions': 'openany,oneside',
  'preamble': r'''
      \usepackage{mathdots}
  '''
}


# -- Additional ---------------------------------------------------------------

# This value contains a list of modules to be mocked up. This is useful when
# some external dependencies are not met at build time and break the building
# process.
autodoc_mock_imports = ["cupy", "cupyx"]


# Adds some custom css classes
def setup(app):
    app.add_css_file('custom.css')
