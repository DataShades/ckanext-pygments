from __future__ import annotations

from typing import Any

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.config.declaration import Declaration, Key
from ckan.types import Context, DataDict

import ckanext.pygments.config as pygment_config
from ckanext.pygments.logic.schema import get_preview_schema


@tk.blanket.helpers
class PygmentsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IResourceView, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "pygments")

    # IResourceView

    def info(self) -> dict[str, Any]:
        return {
            "name": "pygment_view",
            "title": tk._("Pygment"),
            "icon": "fa-file-lines",
            "schema": get_preview_schema(),
            "iframed": False,
            "always_available": True,
            "default_title": tk._("Pygment"),
        }

    def can_view(self, data_dict: DataDict) -> bool:
        return pygment_config.is_format_supported(
            data_dict["resource"].get("format", "").lower()
        )

    def view_template(self, context: Context, data_dict: DataDict) -> str:
        return "pygment_preview.html"

    def form_template(self, context: Context, data_dict: DataDict) -> str:
        return "pygment_form.html"
