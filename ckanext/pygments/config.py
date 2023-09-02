import ckan.plugins.toolkit as tk

import ckanext.pygments.utils as pygment_utils

CONF_SUPPORTED_FORMATS = "ckanext.pygments.supported_formats"

CONF_MAX_SIZE = "ckanext.pygments.max_size"
DEFAULT_MAX_SIZE = 1048576


def is_format_supported(fmt: str) -> bool:
    """Check if we are supporting a specified resource format"""
    if fmt not in tk.config[CONF_SUPPORTED_FORMATS]:
        return False

    for formats in pygment_utils.LEXERS:
        if fmt in formats:
            return True

    return False


def bytes_to_render() -> int:
    """Check how many bytes from file we are going to render as preview"""

    return tk.asint(tk.config.get(CONF_MAX_SIZE, DEFAULT_MAX_SIZE))
