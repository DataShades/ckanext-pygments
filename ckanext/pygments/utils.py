from __future__ import annotations

from pygments.styles import STYLE_MAP


def get_list_of_themes() -> list[str]:
    return [theme for theme in STYLE_MAP]
