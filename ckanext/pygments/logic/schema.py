from __future__ import annotations

from typing import Any, Dict

from ckanext.pygments.utils import get_list_of_themes

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def get_preview_schema(
    ignore_empty, unicode_safe, url_validator, default, one_of
) -> Schema:
    return {
        "file_url": [ignore_empty, unicode_safe, url_validator],
        "theme": [
            default("default"),
            unicode_safe,
            one_of(get_list_of_themes()),
        ],
    }
