from __future__ import annotations

from typing import Any

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.types import Context, DataDict

import ckanext.pygments.cache as pygment_cache
import ckanext.pygments.config as pygment_config
from ckanext.pygments.logic.schema import get_preview_schema


@tk.blanket.helpers
@tk.blanket.validators
@tk.blanket.config_declarations
@tk.blanket.blueprints
@tk.blanket.actions
class PygmentsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.IResourceController, inherit=True)
    p.implements(p.ISignal)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "pygments")

    # IResourceView

    def info(self) -> dict[str, Any]:
        return {
            "name": "pygments_view",
            "title": tk._("Pygments"),
            "icon": "palette",
            "schema": get_preview_schema(),
            "iframed": False,
            "always_available": True,
            "default_title": pygment_config.get_default_view_name(),
        }

    def can_view(self, data_dict: DataDict) -> bool:
        return pygment_config.is_format_supported(
            data_dict["resource"].get("format", "").lower()
        )

    def view_template(self, context: Context, data_dict: DataDict) -> str:
        return "pygments/pygment_preview.html"

    def form_template(self, context: Context, data_dict: DataDict) -> str:
        return "pygments/pygment_form.html"

    def setup_template_variables(self, context: Context, data_dict: DataDict) -> None:
        data_dict["resource_view"].setdefault(
            "title", pygment_config.get_default_view_name()
        )
        data_dict["resource_view"].setdefault(
            "description", pygment_config.get_default_description()
        )

    # IResourceController

    def before_resource_delete(
        self,
        context: types.Context,
        resource: dict[str, Any],
        resources: list[dict[str, Any]],
    ) -> None:
        pygment_cache.RedisCache().invalidate(resource["id"])

    def after_resource_update(self, context: Context, resource: dict[str, Any]) -> None:
        pygment_cache.RedisCache().invalidate(resource["id"])

    # ISignal

    def get_signal_subscriptions(self) -> types.SignalMapping:
        return {
            tk.signals.ckanext.signal("ap_main:collect_config_sections"): [
                self.collect_config_sections_subs,
            ],
            tk.signals.ckanext.signal("ap_main:collect_config_schemas"): [
                self.collect_config_schemas_subs,
            ],
        }

    @staticmethod
    def collect_config_sections_subs(sender: None):
        return {
            "name": "Pygments",
            "configs": [
                {
                    "name": "Configuration",
                    "blueprint": "pygments_admin.config",
                    "info": "Pygments settings",
                },
            ],
        }

    @staticmethod
    def collect_config_schemas_subs(sender: None):
        return ["ckanext.pygments:config_schema.yaml"]
