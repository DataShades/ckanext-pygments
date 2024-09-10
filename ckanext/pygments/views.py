from __future__ import annotations

import ckan.plugins.toolkit as tk
from flask import Blueprint

import ckanext.pygments.config as pygment_config
import ckanext.pygments.utils as pygments_utils
import ckanext.pygments.cache as pygments_cache

__all__ = ["bp"]

bp = Blueprint("pygments", __name__, url_prefix="/pygments")


@bp.route("/highlight/<resource_id>", methods=["GET"])
def highlight(resource_id: str) -> str:
    cache_manager = pygments_cache.RedisCache()
    cache_enabled = pygment_config.is_cache_enabled()
    preview = ""

    if cache_enabled:
        preview = cache_manager.get_data(resource_id)
        exceed_max_size = len(preview) > pygment_config.get_resource_cache_max_size()

        if exceed_max_size:
            cache_manager.invalidate(resource_id)

    if not preview:
        preview = pygments_utils.pygment_preview(
            resource_id,
            tk.request.args.get("theme", pygment_config.DEFAULT_THEME, type=str),
            tk.request.args.get(
                "chunk_size", pygment_config.DEFAULT_MAX_SIZE, type=int
            ),
        )

        if cache_enabled and not exceed_max_size:
            cache_manager.set_data(resource_id, preview)

    return tk.render(
        "pygments/pygment_preview_body.html",
        {"preview": preview},
    )
