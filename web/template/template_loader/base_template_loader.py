from typing import Any

from blocks.template_exist import is_template_exists
from django.template import loader

from .tempate_context_processor.template_context_processor_interface import (
    TemplateContextProcessorInterface,
)


class BaseTemplateLoader:
    def __init__(self, context_processor: TemplateContextProcessorInterface):
        self.context_processor = context_processor

    @staticmethod
    def load_template(app_name: str, template_name: str, request=None, context: dict[Any, Any] = None):
        if is_template_exists(f"{app_name}/{template_name}.html"):
            return loader.render_to_string(f"{app_name}/{template_name}.html", context, request, None)
        return None
