from __future__ import annotations

import logging
from typing import Any

import pygments.lexers as pygment_lexers
import requests
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.styles import STYLE_MAP
from pygments.token import Text
from requests.exceptions import RequestException

import ckan.plugins.toolkit as tk
from ckan import model
from ckan.lib import uploader

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
            f".{self.cssclass} pre {{ {self._pre_style} }}",  # type: ignore
            f".{self.cssclass} td.linenos .normal {{ {self._linenos_style} }}",  # type: ignore
            f".{self.cssclass} span.linenos {{ {self._linenos_style} }}",  # type: ignore
            f".{self.cssclass} td.linenos .special {{ {self._linenos_special_style} }}",  # type: ignore
            f".{self.cssclass} span.linenos.special {{ {self._linenos_special_style} }}",  # type: ignore
        ]

    def get_background_style_defs(self, arg=None):
        """Alter: pass self.cssclass to prefix()."""
        prefix = self.get_css_prefix(arg)
        bg_color = self.style.background_color
        hl_color = self.style.highlight_color

        lines = []

        if arg and not self.nobackground and bg_color is not None:
            text_style = ""
            if Text in self.ttype2class:  # type: ignore
                text_style = " " + self.class2style[self.ttype2class[Text]][0]  # type: ignore
            lines.insert(
                0,
                f"{prefix(self.cssclass)}{{ background: {bg_color};{text_style} }}",
            )
        if hl_color is not None:
            lines.insert(0, f"{prefix('hll')} {{ background-color: {hl_color} }}")

        return lines


def get_formats_for_declaration() -> str:
    return " ".join(fmt for formats in LEXERS for fmt in formats)


def get_list_of_themes() -> list[str]:
    """Return a list of supported preview themes."""
    return list(STYLE_MAP)


def get_lexer_for_format(fmt: str):
    """Return a lexer for a specified format."""
    for formats, lexer in LEXERS.items():
        if fmt in formats:
            return lexer

    if pygment_config.guess_lexer():
        lexer = pygment_lexers.find_lexer_class_for_filename(f"file.{fmt}")
        if lexer:
            return lexer

    return DEFAULT_LEXER


def pygment_preview(
    resource_id: str,
    theme: str,
    chunk_size: int,
    file_url: str | None,
    show_line_numbers: bool = False,
) -> str:
    """Render a preview of a resource using Pygments."""
    resource = model.Resource.get(resource_id)

    if not resource:
        return ""

    maxsize = chunk_size or pygment_config.bytes_to_render()

    if file_url or resource.url_type != "upload":
        data = get_remote_resource_data(resource, maxsize, file_url)
    else:
        data = get_local_resource_data(resource, maxsize)

    lexer = get_lexer_for_resource(resource, file_url, data)

    log.debug("Pygments: using lexer %s for resource %s", lexer, resource_id)

    try:
        formatter = CustomHtmlFormatter(
            full=False,
            style=theme,
            linenos="table" if show_line_numbers else False,
            lineanchors="hl-line-number",
            anchorlinenos=False,
            linespans="hl-line",
            cssclass="pgh ",
        )
        styles = formatter.get_style_defs(".pgh")
        preview = highlight(data, lexer=lexer, formatter=formatter)
    except TypeError:
        return ""

    return f"<style>{styles}</style>{preview}"


def get_local_resource_data(resource: model.Resource, maxsize: int) -> str:
    """Return a local resource data."""
    upload = uploader.get_resource_uploader(resource.as_dict(True))
    filepath = upload.get_path(resource.id)

    try:
        with open(filepath) as f:
            data = f.read(maxsize)
    except FileNotFoundError:
        log.exception("Pygments: Error reading data from file: %s", filepath)
        return "Pygments: Error reading data from file. Please, contact the administrator."

    return data


def get_remote_resource_data(resource: model.Resource, maxsize: int, file_url: str | None) -> str:
    """Return remote resource data.

    If maxsize is -1, fetch full content.
    Otherwise fetch only first maxsize bytes without downloading the whole file.
    """
    url = file_url or resource.url
    if not url:
        return tk._("Resource URL is not provided")

    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
    except RequestException:
        log.exception("Pygments: Error fetching data for resource: %s", url)
        return f"Pygments: Error fetching data for resource by URL {url}. Please contact the administrator."

    if maxsize == -1:
        try:
            text = resp.text
        except UnicodeDecodeError:
            text = resp.content.decode("utf-8", errors="replace")
        return text

    data_bytes = b""

    for chunk in resp.iter_content(chunk_size=8192):
        if not chunk:
            break

        data_bytes += chunk

        if len(data_bytes) >= maxsize:
            data_bytes = data_bytes[:maxsize]
            break

    try:
        return data_bytes.decode(resp.encoding or "utf-8", errors="replace")
    except LookupError:
        return data_bytes.decode("utf-8", errors="replace")


def get_lexer_for_resource(resource: model.Resource, file_url: str | None = None, data: str = "") -> Any:
    """Return a lexer for a specified resource."""
    if not file_url:
        return get_lexer_for_format(resource.format.lower())()

    if data:
        if guessed_lexer := pygment_lexers.guess_lexer(data):
            return guessed_lexer
    elif guessed_lexer := pygment_lexers.find_lexer_class_for_filename(file_url):
        return guessed_lexer()

    return DEFAULT_LEXER()
