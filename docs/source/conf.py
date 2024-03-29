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

# 5/13/22 srn - I've also added to PATH environment variable.
import os
import sys
sys.path.insert(0, os.path.abspath('../../src/simpleth'))
sys.path.insert(0, os.path.abspath('../../tools'))


# -- Project information -----------------------------------------------------

project = 'simpleth'
copyright = '2021-2022, Stephen Newell'
author = 'Stephen Newell'

# The full version, including alpha/beta/rc tags
release = '0.1.65'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- SN added -------------------------------------------------

# from: https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
    }

# from: https://sublime-and-sphinx-guide.readthedocs.io/en/latest/code_blocks.html#show-example-code
# Makes code-block work.

pygments_style = 'sphinx'

# 6/7/22
# from: https://github.com/readthedocs/readthedocs.org/issues/1776
# Getting: WARNING: html_static_path entry '_static' does not exist
# in RtD Build raw view.

html_static_path = []