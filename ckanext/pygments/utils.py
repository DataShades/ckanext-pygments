from __future__ import annotations

import pygments.lexers as pygment_lexers
from pygments.styles import STYLE_MAP


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

    return DEFAULT_LEXER
