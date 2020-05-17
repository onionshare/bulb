# -*- coding: utf-8 -*-
#
# Stem documentation build configuration file, created by
# sphinx-quickstart on Thu May 31 09:56:13 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys
import warnings

from sphinx.domains.python import PythonDomain

TYPEHINTS_REQUIRED = """\
Building Stem's website requires...

  https://github.com/agronholm/sphinx-autodoc-typehints

Please run...

  % pip install sphinx-autodoc-typehints
"""

try:
  import sphinx_autodoc_typehints
except ImportError:
  print(TYPEHINTS_REQUIRED, file = sys.stderr)
  sys.exit(1)

# These warnings are due to: https://github.com/agronholm/sphinx-autodoc-typehints/issues/133

warnings.filterwarnings('ignore', message = 'sphinx.util.inspect.Signature\(\) is deprecated')

# Drop redundant return types because we state this in our :returns: clasuses.
# This is an argument for sphinx-autodoc-typehints.

typehints_document_rtype = False

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.1' # required for the sphinx-apidoc command

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx_autodoc_typehints', 'roles']

autodoc_default_options = {
  'members': True,
  'member-order': 'bysource',
  'show-inheritance': True,
  'undoc-members': True,

  # Without this Sphinx emits several warnings of the form...
  #
  #   WARNING: missing attribute mentioned in :members: or __all__: module stem, attribute directory
  #
  # This is because Sphinx expects modules from importlib.import_module() to
  # have attributes for its submodules. These attributes might or might not be
  # present depending on what other modules have been imported.
  #
  # Said another way...
  #
  #  % print(importlib.import_module('stem').__dict__.keys())
  #  dict_keys(['__name__', '__doc__', '__package__', ...])  <= doesn't have submodules
  #
  # But if instead we call...
  #
  #  % importlib.import_module('stem.connection')
  #  % print(importlib.import_module('stem').__dict__.keys())
  #  dict_keys(['__name__', '__doc__', '__package__', ..., 'descriptor', 'control', 'connection'])  <= includes submodules refernced by stem.connection
  #
  # By telling it to ignore our '__all__' attributes Sphinx will import in a
  # fashon that doesn't emit these warnings.

  'ignore-module-all': True,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

from stem import __version__, __author__, __contact__

# Ignore the '-dev' version suffix.

if __version__.endswith('-dev'):
  __version__ = __version__[:-4]

# General information about the project.
project = 'Stem'
copyright = '2012, %s' % __author__

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__[:__version__.rfind(".")]
# The full version, including alpha/beta/rc tags.
release = __version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'default'
html_theme = 'haiku'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'Stem Docs'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.

html_logo = '_static/logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.

html_favicon = '_static/favicon.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
smartquotes = False

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'Stemdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Stem.tex', 'Stem Documentation',
   'Damian Johnson', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'stem', 'Stem Documentation',
     ['%s (%s)' % (__author__, __contact__)], 1)
]

trac_url = 'https://trac.torproject.org/{slug}'
spec_url = 'https://gitweb.torproject.org/torspec.git/commit/?id={slug}'


def skip_members(app, what, name, obj, skip, options):
  if name in ('ATTRIBUTES', 'PARSER_FOR_LINE'):
    return True  # skip the descriptor's parser constants


class PythonDomainNoXref(PythonDomain):
  """
  Sphinx attempts to create cross-reference links for variable names...

    https://github.com/sphinx-doc/sphinx/issues/2549
    https://github.com/sphinx-doc/sphinx/issues/3866

  This causes alot of warnings such as...

    stem/descriptor/networkstatus.py:docstring of
    stem.descriptor.networkstatus.DocumentDigest:: WARNING: more than one
    target found for cross-reference 'digest':
    stem.descriptor.extrainfo_descriptor.ExtraInfoDescriptor.digest, ...
  """

  def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
    if 'refspecific' in node:
      del node['refspecific']

    return super(PythonDomainNoXref, self).resolve_xref(
      env, fromdocname, builder, typ, target, node, contnode)


def setup(app):
  app.connect('autodoc-skip-member', skip_members)
  app.add_domain(PythonDomainNoXref, override = True)
