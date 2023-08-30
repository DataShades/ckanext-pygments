from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk

import ckan.plugins as p
from ckan.types import Context, DataDict
from ckan.config.declaration import Declaration, Key


@tk.blanket.helpers
class PygmentsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.IConfigDeclaration)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "pygments")

        self.formats = tk.aslist(config_.get("ckan.pygments.supported_formats"))

    # IResourceView

    def info(self) -> dict[str, Any]:
        return {
            "name": "pygment_view",
            "title": tk._("Pygment"),
            "icon": "fa-file-lines",
            "schema": {
                "file_url": [
                    tk.get_validator("ignore_empty"),
                    tk.get_validator("unicode_safe"),
                    tk.get_validator("url_validator"),
                ]
            },
            "iframed": False,
            "always_available": True,
            "default_title": tk._("Pygment"),
        }

    def can_view(self, data_dict: DataDict) -> bool:
        return data_dict["resource"].get("format", "").lower() in self.formats

    def view_template(self, context: Context, data_dict: DataDict) -> str:
        return "pygment_preview.html"

    def form_template(self, context: Context, data_dict: DataDict) -> str:
        return "pygment_form.html"

    # # IConfigDeclaration

    def declare_config_options(self, declaration: Declaration, key: Key):
        declaration.annotate("pygments preview settings")
        declaration.declare(key.ckanextr.pygments.supported_formats, "sql py rs html xhtml")
