from __future__ import annotations

import logging

from flask import Blueprint

import ckan.plugins as p
import ckan.plugins.toolkit as tk

import ckanext.pygments.cache as pygments_cache
import ckanext.pygments.config as pygment_config
import ckanext.pygments.utils as pygments_utils

log = logging.getLogger(__name__)
bp = Blueprint("pygments", __name__, url_prefix="/pygments")


@bp.route("/highlight/<resource_id>", methods=["GET"])
def highlight(resource_id: str) -> str:
    cache_manager = pygments_cache.RedisCache()
    cache_enabled = pygment_config.is_cache_enabled()
    resource_view_id = tk.request.args.get("resource_view_id", type=str)
    preview = ""
    exceed_max_size = False

    if cache_enabled:
        preview = cache_manager.get_data(resource_id, resource_view_id)
        exceed_max_size = len(preview) > pygment_config.get_resource_cache_max_size()

        if exceed_max_size:
            cache_manager.invalidate(resource_id)

    if not preview:
        try:
            preview = pygments_utils.pygment_preview(
                resource_id,
                tk.request.args.get("theme", pygment_config.get_default_theme(), type=str),
                tk.request.args.get("chunk_size", pygment_config.get_resource_cache_max_size(), type=int),
                tk.request.args.get("file_url", type=str),
                tk.asbool(tk.request.args.get("show_line_numbers", "False")),
            )
        except Exception:
            log.exception(
                "Pygments: failed to render preview, resource_id: %s",
                resource_id,
            )
            preview = "Pygments: Error rendering preview. Please, contact the administrator."
        else:
            if cache_enabled and not exceed_max_size:
                cache_manager.set_data(resource_id, preview, resource_view_id)

    return tk.render(
        "pygments/pygment_preview_body.html",
        {"preview": preview},
    )


@bp.route("/clear_cache", methods=["POST"])
def clear_cache():
    pygments_cache.RedisCache.drop_cache()

    tk.h.flash_success(tk._("Cache has been cleared"))

    if p.plugin_loaded("admin_panel"):
        return tk.h.redirect_to("pygments_admin.config")

    return "Cache has been cleared"


@bp.route("/clear_cache/<resource_id>", methods=["POST"])
def clear_resource_cache(resource_id: str):
    pygments_cache.RedisCache().invalidate(resource_id, tk.request.args.get("resource_view_id", type=str))

    if p.plugin_loaded("admin_panel"):
        return tk.h.redirect_to("pygments_admin.config")

    return "Resource cache has been cleared"


if p.plugin_loaded("admin_panel"):
    from ckanext.ap_main.utils import ap_before_request
    from ckanext.ap_main.views.generics import ApConfigurationPageView

    pygments_admin = Blueprint("pygments_admin", __name__)
    pygments_admin.before_request(ap_before_request)

    pygments_admin.add_url_rule(
        "/admin-panel/pygments/config",
        view_func=ApConfigurationPageView.as_view(
            "config",
            "pygments_config",
            render_template="pygments/config.html",
            page_title=tk._("Pygments config"),
        ),
    )
