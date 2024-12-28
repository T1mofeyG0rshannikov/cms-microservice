from typing import Any

from django.template import loader

from web.blocks.template_exist import is_template_exists


class BaseTemplateLoader:
    def load_template(self, app_name: str, template_name: str, context: dict[str, Any] | None = None):
        if is_template_exists(f"{app_name}/{template_name}.html"):
            return loader.render_to_string(f"{app_name}/{template_name}.html", context, None)
        return None
