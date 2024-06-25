import sys

import requests
import sphinx_autodoc_typehints
from directives import AutoModuleSummary
from sphinx.ext import autosummary

project = "lshmm"
version = release = "latest"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

exclude_patterns = []

master_doc = "index"

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "display_version": False,
}

html_static_path = ["_static"]

html_css_files = ["theme_overrides.css"]

html_show_sphinx = False

html_show_copyright = False

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "member-order": "bysource",
}

# Configuration for sphinx_autodoc_typehints
# Document parameter types even if the parameter is otherwise undocumented.
always_document_param_types = True

# For undocumented functions, autosummary ends up using the :param or :rtype:
# line added by sphinx_autodoc_typehints as the function's summary. This results
# in the second column of the summary table containing a <dl> element, which
# breaks the formatting.
#
# To work around this, override autosummary's extract_summary function and
# replace replace these lines with an empty string for the summary.
original_extract_summary = autosummary.extract_summary


def extract_summary(doc, document):
    summary = original_extract_summary(doc, document)
    if any(summary.startswith(tag) for tag in (":param ", ":rtype: ")):
        return ""
    return summary


autosummary.extract_summary = extract_summary

# Configuration for sphinx.ext.intersphinx
intersphinx_mapping = {}


def setup(app):
    app.add_directive("gnomad_automodulesummary", AutoModuleSummary)
