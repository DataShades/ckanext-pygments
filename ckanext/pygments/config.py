import ckan.plugins.toolkit as tk


CONF_SUPPORTED_FORMATS = "ckanext.pygments.supported_formats"

CONF_MAX_SIZE = "ckanext.pygments.max_size"
CONF_ENABLE_HTMX = "ckanext.pygments.include_htmx_asset"
CONF_DEFAULT_THEME = "ckanext.pygments.default_theme"
CONF_GUESS_LEXER = "ckanext.pygments.guess_lexer"

CONF_ENABLE_CACHE = "ckanext.pygments.cache.enable"
CONF_RES_CACHE_MAX_SIZE = "ckanext.pygments.cache.preview_max_size"
CONF_CACHE_TTL = "ckanext.pygments.cache.ttl"

CONF_DEFAULT_VIEW_NAME = "ckanext.pygments.default.view_name"
CONF_DEFAULT_DESCRIPTION = "ckanext.pygments.default.description"


def is_format_supported(fmt: str) -> bool:
    return fmt in tk.config[CONF_SUPPORTED_FORMATS].split(",")


def bytes_to_render() -> int:
    """Check how many bytes from file we are going to render as preview"""
    return tk.config[CONF_MAX_SIZE]


def include_htmx_asset() -> bool:
    """Include HTMX library asset. Disable it, if no other library do it."""
    return tk.asbool(tk.config[CONF_ENABLE_HTMX])


def get_default_theme() -> str:
    """Get the default theme for pygments"""
    return tk.config[CONF_DEFAULT_THEME]


def guess_lexer() -> bool:
    """Check if we should guess the lexer"""
    return tk.config[CONF_GUESS_LEXER]


def is_cache_enabled() -> bool:
    """Check if the cache is enabled"""
    return tk.config[CONF_ENABLE_CACHE]


def get_resource_cache_max_size() -> int:
    """Get the max size of the cache for the resource"""
    return tk.config[CONF_RES_CACHE_MAX_SIZE]


def get_cache_ttl() -> int:
    """Get the cache TTL"""
    return tk.config[CONF_CACHE_TTL]


def get_default_view_name() -> str:
    """Get the default view name"""
    return tk.config[CONF_DEFAULT_VIEW_NAME]


def get_default_description() -> str:
    """Get the default description"""
    return tk.config[CONF_DEFAULT_DESCRIPTION]
