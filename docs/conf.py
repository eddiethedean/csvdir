"""Sphinx configuration for csvdir."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from csvdir import __version__  # noqa: E402

project = "csvdir"
copyright = "2025–2026, csvdir contributors"
author = "csvdir contributors"
release = version = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

root_doc = "index"

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "csvdir"
html_theme_options = {
    "source_repository": "https://github.com/eddiethedean/csvdir",
    "source_branch": "main",
    "source_directory": "docs/",
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/eddiethedean/csvdir",
            "html": "",
            "class": "fa-brands fa-github",
        },
    ],
}

html_meta = {
    "description": (
        "csvdir — read every CSV in a directory with one iterator. "
        "Install, guides, configuration, and API reference."
    ),
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "smartquotes",
    "substitution",
]

myst_heading_anchors = 3

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "show-inheritance": True,
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autosummary_generate = True
napoleon_google_docstring = True
napoleon_numpy_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

pygments_style = "sphinx"

# Flat sidebar: Getting started and Changelog appear at the top level (StreamTree-style).
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ],
}
