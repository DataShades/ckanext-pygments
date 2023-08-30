from __future__ import annotations

import logging
from typing import Any

import requests
from requests.exceptions import RequestException
from pygments import highlight
from pygments.lexers import SqlLexer, HtmlLexer, PythonLexer, TextLexer, RustLexer
from pygments.formatters import HtmlFormatter

import ckan.lib.uploader as uploader

from ckanext.pygments.utils import get_list_of_themes

log = logging.getLogger(__name__)
DEFAULT_LEXER = TextLexer
LEXERS = {"sql": SqlLexer, "html": HtmlLexer, "py": PythonLexer, "rs": RustLexer}


def pygment_preview(resource: dict[str, Any], theme: str) -> tuple[str, str]:
    """Render a resource preview with pygments. Return a rendered data and css
    styles for it"""
    lexer = LEXERS.get(resource.get("format", "").lower(), DEFAULT_LEXER)

    data = ""

    if resource.get("url_type") == "upload":
        upload = uploader.get_resource_uploader(resource)
        filepath = upload.get_path(resource["id"])

        with open(filepath) as f:
            data = f.read()
    else:
        if resource.get("url"):
            try:
                resp = requests.get(resource["url"])
            except RequestException as e:
                log.error("Error fetching data for resource: %s", resource["url"])
            else:
                data = resp.text

    css_styles = HtmlFormatter(style=theme).get_style_defs(".highlight")

    return (
        highlight(
            data,
            lexer(),
            HtmlFormatter(
                linenos="table",
                lineanchors="hl-line-number",
                anchorlinenos=True,
                linespans="hl-line",
            ),
        ),
        css_styles,
    )


def get_preview_theme_options() -> list[dict[str, str]]:
    return [{"value": opt, "text": opt} for opt in get_list_of_themes()]
