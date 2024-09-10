from __future__ import annotations

import math

import ckanext.pygments.config as pygment_config
import ckanext.pygments.utils as pygment_utils
import ckanext.pygments.cache as pygments_cache


def pygments_get_preview_theme_options() -> list[dict[str, str]]:
    return [{"value": opt, "text": opt} for opt in pygment_utils.get_list_of_themes()]


def pygments_get_default_max_size() -> int:
    return pygment_config.bytes_to_render()


def pygments_include_htmx_asset() -> bool:
    """Include HTMX asset if enabled."""
    return pygment_config.include_htmx_asset()


def pygments_get_default_theme() -> str:
    """Get the default theme for pygments"""
    return pygment_config.get_default_theme()


def pygments_is_cache_enabled() -> bool:
    return pygment_config.is_cache_enabled()


def pygments_get_cache_size() -> int:
    """Get the size of the Redis cache"""
    return pygments_cache.RedisCache().calculate_cache_size()


def pygments_get_resource_cache_size(resource_id: str) -> int:
    return pygments_cache.RedisCache().calculate_resource_cache_size(resource_id)


def pygments_printable_file_size(size_bytes: int) -> str:
    """Convert file size in bytes to human-readable format"""
    if size_bytes == 0:
        return "0 bytes"

    size_name = ("bytes", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(float(size_bytes) / p, 1)

    return f"{s} {size_name[i]}"
