from __future__ import annotations

import logging
from typing import Any

import ckan.lib.uploader as uploader
import ckan.plugins.toolkit as tk
import pygments.lexers as pygment_lexers
import requests
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.styles import STYLE_MAP
from pygments.token import Text
from requests.exceptions import RequestException

from ckanext.pygments import config as pygment_config

log = logging.getLogger(__name__)

DEFAULT_LEXER = pygment_lexers.TextLexer
LEXERS = {
    ("sql",): pygment_lexers.SqlLexer,
    ("html", "xhtml", "htm", "xslt"): pygment_lexers.HtmlLexer,
    ("py", "pyw", "pyi", "jy", "sage", "sc"): pygment_lexers.PythonLexer,
    ("rs", "rs.in"): pygment_lexers.RustLexer,
    ("rst", "rest"): pygment_lexers.RstLexer,
    ("md", "markdown"): pygment_lexers.MarkdownLexer,
    ("xml", "xsl", "rss", "xslt", "xsd", "wsdl", "wsf", "rdf"): pygment_lexers.XmlLexer,
    ("json",): pygment_lexers.JsonLexer,
    ("jsonld",): pygment_lexers.JsonLdLexer,
    ("yaml", "yml"): pygment_lexers.YamlLexer,
    ("dtd",): pygment_lexers.DtdLexer,
    ("php", "inc"): pygment_lexers.PhpLexer,
    ("ttl",): pygment_lexers.TurtleLexer,
    ("js",): pygment_lexers.JavascriptLexer,
}


class CustomHtmlFormatter(HtmlFormatter):
    """CSS post-processing for Pygments HTML formatter due to poor isolation"""

    def get_linenos_style_defs(self):
        """Alter: prepend styles with self.cssclass"""
        return [
            ".%s pre { %s }" % (self.cssclass, self._pre_style),
            ".%s td.linenos .normal { %s }" % (self.cssclass, self._linenos_style),
            ".%s span.linenos { %s }" % (self.cssclass, self._linenos_style),
            ".%s td.linenos .special { %s }"
            % (self.cssclass, self._linenos_special_style),
            ".%s span.linenos.special { %s }"
            % (self.cssclass, self._linenos_special_style),
        ]

    def get_background_style_defs(self, arg=None):
        """Alter: pass self.cssclass to prefix()"""
        prefix = self.get_css_prefix(arg)
        bg_color = self.style.background_color
        hl_color = self.style.highlight_color

        lines = []

        if arg and not self.nobackground and bg_color is not None:
            text_style = ""
            if Text in self.ttype2class:
                text_style = " " + self.class2style[self.ttype2class[Text]][0]
            lines.insert(
                0,
                "%s{ background: %s;%s }"
                % (prefix(self.cssclass), bg_color, text_style),
            )
        if hl_color is not None:
            lines.insert(0, "%s { background-color: %s }" % (prefix("hll"), hl_color))

        return lines


def get_formats_for_declaration() -> str:
    return " ".join(fmt for formats in LEXERS for fmt in formats)


def get_list_of_themes() -> list[str]:
    """Return a list of supported preview themes"""
    return [theme for theme in STYLE_MAP]


def get_lexer_for_format(fmt: str):
    """Return a lexer for a specified format"""
    for formats, lexer in LEXERS.items():
        if fmt in formats:
            return lexer

    if pygment_config.guess_lexer():
        if lexer := pygment_lexers.find_lexer_class_for_filename(f"file.{fmt}"):
            return lexer

    return DEFAULT_LEXER


def pygment_preview(resource_id: str, theme: str, chunk_size: int) -> str:
    """Render a preview of a resource using Pygments"""

    resource = tk.get_action("resource_show")({}, {"id": resource_id})

    maxsize = chunk_size or pygment_config.bytes_to_render()

    data = (
        get_local_resource_data(resource, maxsize)
        if resource.get("url_type") == "upload"
        else get_remote_resource_data(resource, maxsize)
    )

    try:
        preview = highlight(
            data,
            lexer=get_lexer_for_format(resource.get("format", "").lower())(),
            formatter=CustomHtmlFormatter(
                full=True,
                style=theme,
                linenos="table",
                lineanchors="hl-line-number",
                anchorlinenos=True,
                linespans="hl-line",
                cssclass="pygments_highlight",
            ),
        )
    except TypeError:
        preview = ""

    return preview


def get_local_resource_data(resource: dict[str, Any], maxsize: int) -> str:
    """Return a local resource data"""

    upload = uploader.get_resource_uploader(resource)
    filepath = upload.get_path(resource["id"])

    try:
        with open(filepath) as f:
            data = f.read(maxsize)
    except FileNotFoundError:
        log.error("Pygments: Error reading data from file: %s", filepath)
        return (
            "Pygments: Error reading data from file. Please, contact the administrator."
        )

    return data


def get_remote_resource_data(resource: dict[str, Any], maxsize: int) -> str:
    """Return a remote resource data"""

    if not resource.get("url"):
        return tk._("Resource URL is not provided")

    try:
        resp = requests.get(resource["url"])
    except RequestException:
        log.error("Pygments: Error fetching data for resource: %s", resource["url"])
        return f"Pygments: Error fetching data for resource by URL {resource['url']}. Please, contact the administrator."
    else:
        data = resp.text[:maxsize]

    return data
