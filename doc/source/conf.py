# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import sys
#
#

import inspect
import pathlib
import os

import numba as nb

# in CodeFactor there is no version, since it is generated upon installation
import eko.version # pylint: disable=no-name-in-module

# -- Project information -----------------------------------------------------

project = 'EKO'
copyright = '2019-2020, the N3PDF team' # pylint: disable=redefined-builtin
author = 'N3PDF team'

# The short X.Y version
version = eko.version.short_version
if not eko.version.is_released:
    version = "develop"

# The full version, including alpha/beta/rc tags
release = eko.version.full_version

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.napoleon',
    'sphinxcontrib.bibtex',
    "sphinx.ext.graphviz",
    "sphinx.ext.extlinks",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Markdown configuration

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
}

autosectionlabel_prefix_document = True
#autosectionlabel_maxdepth = 10
# Allow to embed rst syntax in  markdown files.
enable_eval_rst = True

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["shared/*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# A string to be included at the beginning of all files
shared = pathlib.Path(__file__).absolute().parent / "shared"
rst_prolog = "\n".join([open(x).read() for x in os.scandir(shared)])

extlinks = {'yadism': ('https://n3pdf.github.io/yadism/%s', 'yadism')}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'EKO Documentation'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'EKODocumentation.tex', 'EKO Documentation',
     'N3PDF team', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'ekodocumentation', 'EKO Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'EKODocumentation', 'EKO Documentation',
     author, 'EKODocumentation', 'EKO Documentation.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
# Thanks https://github.com/bskinn/sphobjinv
intersphinx_mapping = {
    "python": ('https://docs.python.org/3/', None),
    "scipy": ('https://docs.scipy.org/doc/scipy/reference', None),
    "numpy": ("https://numpy.org/doc/stable", None)
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

mathjax_config = {
    "TeX": {"Macros":{
        # texts
        "tLL": [r"\text{LL}",0],
        # PDFs
        "dSV": [r"{{\begin{pmatrix}\tilde \Sigma\\\tilde g\end{pmatrix}}^{(#1)}\!(#2)}",2],
        "dVf": [r"{\tilde{V}^{(#1)}(#2)}",2],
        "dVj": [r"{\tilde{V}_{\!#1}^{(#2)}(#3)}",3],
        "dTj": [r"{\tilde{T}_{\!#1}^{(#2)}(#3)}",3],
        # EKOs
        "ES": [r"{\tilde{\mathbf{E}}_S({#1}\leftarrow {#2})}",2],
        "ESk": [r"{\tilde{\mathbf{E}}_S^{(#1)}({#2}\leftarrow {#3})}",3],
        "Ensv": [r"{\tilde{E}_{ns}^v({#1}\leftarrow {#2})}",2],
        "Ensp": [r"{\tilde{E}_{ns}^+({#1}\leftarrow {#2})}",2],
        "Ensm": [r"{\tilde{E}_{ns}^-({#1}\leftarrow {#2})}",2],
        # projectors
        "em": [r"{\mathbf{e}}_-",0],
        "ep": [r"{\mathbf{e}}_+",0],
    }}
}

# I don't know where and when, but at some point sphinx stopped to detect the documentation
# hidden below numba. This issue is discussed here https://github.com/sphinx-doc/sphinx/issues/3783
# pointing to this conf.py:
# https://github.com/duetosymmetry/qnm/blob/d286cad616a4abe5ff3b4e05adbfb4b0e305583e/docs/conf.py#L71-L93
# However, it doesn't do the trick truly, but the idea is take from there ...
# see also https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#docstring-preprocessing
def process_numba_docstring(app, what, name, obj, options, lines): # pylint: disable=unused-argument
    """Recover the docstring under numba, as the numba.njit decorator doesn't repeat the __doc__"""
    if not isinstance(obj,nb.core.registry.CPUDispatcher):
        return
    else:
        original = obj.py_func
        orig_sig = inspect.signature(original)
        lines = orig_sig.__doc__

def setup(app):
    """Configure Sphinx"""
    app.setup_extension("sphinx.ext.autodoc")
    app.connect('autodoc-process-docstring', process_numba_docstring)
