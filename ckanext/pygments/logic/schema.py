from __future__ import annotations

from ckan.logic.schema import validator_args
from ckan import types

import ckanext.pygments.config as pygment_config
from ckanext.pygments.utils import get_list_of_themes


@validator_args
def get_preview_schema(
    ignore_empty,
    unicode_safe,
    url_validator,
    default,
    one_of,
    int_validator,
    is_positive_integer,
    boolean_validator,
) -> types.Schema:
    return {
        "file_url": [ignore_empty, unicode_safe, url_validator],
        "theme": [
            default(pygment_config.get_default_theme()),
            unicode_safe,
            one_of(get_list_of_themes()),
        ],
        "max_size": [
            default(pygment_config.get_default_max_size()),
            int_validator,
            is_positive_integer,
        ],
        "show_line_numbers": [
            default(pygment_config.get_default_show_line_numbers()),
            boolean_validator,
        ],
    }
