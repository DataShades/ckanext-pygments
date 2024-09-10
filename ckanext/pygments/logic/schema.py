from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

import ckanext.pygments.config as pygment_config
from ckanext.pygments.utils import get_list_of_themes

Schema = Dict[str, Any]


@validator_args
def get_preview_schema(
    ignore_empty,
    unicode_safe,
    url_validator,
    default,
    one_of,
    int_validator,
    pygment_max_size,
) -> Schema:
    return {
        "file_url": [ignore_empty, unicode_safe, url_validator],
        "theme": [
            default(pygment_config.get_default_theme()),
            unicode_safe,
            one_of(get_list_of_themes()),
        ],
        "size": [
            default(pygment_config.bytes_to_render()),
            int_validator,
            pygment_max_size,
        ],
    }
