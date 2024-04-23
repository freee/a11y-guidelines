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
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('.'))
import datetime
import re
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective

# -- Project information -----------------------------------------------------
from version import *

project = 'freeeアクセシビリティー・ガイドライン'
author = 'フリー株式会社'
guidelines_version_suffix = '-RELEASE'
guidelines_version_date = ''

date_obj = datetime.datetime.strptime(publishedDate, '%Y-%m-%d')
if 'current' in tags:
  guidelines_version_suffix = '-CURRENT'
  date_obj = datetime.date.today()
  guidelines_version_date = f'.{date_obj.strftime("%Y%m%d")}'

date_str = date_obj.strftime('%Y年%-m月%-d日')
publishedDate = date_str
version = guidelines_version + guidelines_version_suffix + f'+{checksheet_version}'
release = guidelines_version + guidelines_version_suffix + guidelines_version_date + f'+{checksheet_version}'
guidelines_version_string = guidelines_version + guidelines_version_suffix + guidelines_version_date

html_title = f'{project} {release}'
copyright = '2020-{pubYear}, フリー株式会社'.format(
  pubYear = re.search(r'^(\d{4})年', publishedDate).group(1)
)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinxcontrib.trimblank',
        'sphinx_rtd_theme'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'ja'

# For i18n
#gettext_compact = False
#locale_dirs = ['locale/']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
  "inc/*",
  "checks/inc/*",
  "info/inc/*",
  "intro/ChangeLog/*"
]

# substitution definitions:
rst_prolog = u"""
.. |published_date| replace:: {pubdate}
.. |copyright| replace:: {copyright}
.. |guidelines_version_string| replace:: {guidelines_version_string}
.. |checksheet_version| replace:: {checksheet_version}

.. include:: /inc/misc/defs.txt
""".format(
  pubdate = publishedDate,
  copyright = copyright,
  guidelines_version_string = guidelines_version_string,
  checksheet_version = checksheet_version
)


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {
   "collapse_navigation": "false",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_show_sourcelink = False
html_show_sphinx = False
html_permalinks = False

linkcheck_ignore = [r'http://localhost:\d+/']

class TranslatedDirective(SphinxDirective):
  has_content = False
  required_arguments = 1

  def run(self):
    self.env.metadata[self.env.docname]['translated'] = self.arguments[0] == 'true'
    return []

def setup(app):
  app.add_css_file('a11y-gl.css')
  app.add_directive("translated", TranslatedDirective)
