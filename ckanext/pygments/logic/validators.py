from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk
from ckan.types import Context

import ckanext.pygments.config as pygment_config


def pygment_max_size(value: Any, context: Context) -> Any:
    """Ensures that we are not reading from file more, than maxsize config."""

    max_length = pygment_config.bytes_to_render()

    if value > max_length:
        raise tk.Invalid(f"The max file size to render is {max_length}")

    return value
