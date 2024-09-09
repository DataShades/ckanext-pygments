from __future__ import annotations

import ckanext.pygments.config as pygment_config
import ckanext.pygments.utils as pygment_utils


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
