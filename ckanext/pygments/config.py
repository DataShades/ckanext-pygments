import ckan.plugins.toolkit as tk

import ckanext.pygments.utils as pygment_utils

CONF_SUPPORTED_FORMATS = "ckanext.pygments.supported_formats"

CONF_MAX_SIZE = "ckanext.pygments.max_size"
DEFAULT_MAX_SIZE = 1048576  # 1MB

CONF_ENABLE_HTMX = "ckanext.pygments.include_htmx_asset"

CONF_DEFAULT_THEME = "ckanext.pygments.default_theme"
DEFAULT_THEME = "default"

CONF_ENABLE_CACHE = "ckanext.pygments.cache.enable"
CONF_RES_CACHE_MAX_SIZE = "ckanext.pygments.cache.preview_max_size"
CONF_CACHE_TTL = "ckanext.pygments.cache.ttl"


def is_format_supported(fmt: str) -> bool:
    """Check if the format is supported by the pygments library"""
    if fmt not in tk.config[CONF_SUPPORTED_FORMATS]:
        return False

    for formats in pygment_utils.LEXERS:
        if fmt in formats:
            return True

    return False


def bytes_to_render() -> int:
    """Check how many bytes from file we are going to render as preview"""

    return tk.asint(tk.config.get(CONF_MAX_SIZE, DEFAULT_MAX_SIZE))


def include_htmx_asset() -> bool:
    """Include HTMX library asset. Disable it, if no other library do it."""
    return tk.asbool(tk.config[CONF_ENABLE_HTMX])


def get_default_theme() -> str:
    """Get the default theme for pygments"""
    return tk.config.get(CONF_DEFAULT_THEME, DEFAULT_THEME)


def is_cache_enabled() -> bool:
    """Check if the cache is enabled"""
    return tk.config[CONF_ENABLE_CACHE]


def get_resource_cache_max_size() -> int:
    """Get the max size of the cache for the resource"""
    return tk.config[CONF_RES_CACHE_MAX_SIZE]


def get_cache_ttl() -> int:
    """Get the cache TTL"""
    return tk.config[CONF_CACHE_TTL]
