from __future__ import annotations

import ckan.plugins.toolkit as tk
from flask import Blueprint

import ckanext.pygments.config as pygment_config
import ckanext.pygments.utils as pygments_utils

__all__ = ["bp"]

bp = Blueprint("pygments", __name__, url_prefix="/pygments")


@bp.route("/highlight/<resource_id>", methods=["GET"])
def highlight(resource_id: str) -> str:
    preview = pygments_utils.pygment_preview(
        resource_id,
        tk.request.args.get("theme", pygment_config.DEFAULT_THEME, type=str),
        tk.request.args.get("chunk_size", pygment_config.DEFAULT_MAX_SIZE, type=int),
    )

    return tk.render(
        "pygments/pygment_preview_body.html",
        {"preview": preview},
    )
