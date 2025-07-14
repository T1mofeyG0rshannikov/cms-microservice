from typing import Any

from django.http import HttpRequest
from django.template import loader

from web.blocks.template_exist import is_template_exists
from web.messanger.get_context import get_chat_body_context
from web.template.template_loader.tempate_context_processor.template_context_processor import (
    get_context_processor,
)

from .tempate_context_processor.template_context_processor_interface import (
    TemplateContextProcessorInterface,
)
from .template_loader_interface import TemplateLoaderInterface


class TemplateLoader(TemplateLoaderInterface):
    def __init__(self, context_processor: TemplateContextProcessorInterface) -> None:
        self.context_processor = context_processor

    @staticmethod
    def load_template(app_name: str, template_name: str, context: dict[str, Any] | None = None) -> str | None:
        if is_template_exists(f"{app_name}/{template_name}.html"):
            return loader.render_to_string(f"{app_name}/{template_name}.html", context, None)
        return None

    def load_change_user_form(self, request: HttpRequest):
        context = self.context_processor.get_change_user_form_context(request)

        return self.load_template(app_name="common", template_name="change-user-form", context=context)

    def load_change_socials_form(self, request: HttpRequest):
        context = self.context_processor.get_change_socials_form_context(request)

        return self.load_template(app_name="account", template_name="forms/socials-form", context=context)

    def load_referral_popup(self, request: HttpRequest):
        context = self.context_processor.get_referral_popup_context(request)

        return self.load_template(app_name="account", template_name="popups/referral-popup", context=context)

    def load_choice_product_form(self, request: HttpRequest):
        context = self.context_processor.get_choice_product_form(request)

        return self.load_template(app_name="account", template_name="forms/choice-product-form", context=context)

    def load_create_user_product_form(self, request: HttpRequest):
        context = self.context_processor.get_create_user_product_form(request)

        return self.load_template(
            app_name="account",
            template_name="forms/update-or-create-user-product-form",
            context=context,
        )

    def load_product_description_popup(self, request: HttpRequest):
        context = self.context_processor.get_product_description_popup(request)

        return self.load_template(app_name="account", template_name="popups/popup-description", context=context)

    def load_delete_product_popup(self, request: HttpRequest):
        return self.load_template(
            app_name="account",
            template_name="popups/delete-popup",
            context={"product_id": request.GET.get("product")},
        )

    def load_create_idea_form(self, request: HttpRequest):
        context = self.context_processor.get_create_idea_form(request)

        return self.load_template(app_name="account", template_name="forms/create-idea-form", context=context)

    def load_chat_body(self, request: HttpRequest):
        context = get_chat_body_context(request)

        return self.load_template(app_name="account", template_name="contents/chat-body", context=context)


def get_template_loader(
    context_processor: TemplateContextProcessorInterface = get_context_processor(),
) -> TemplateLoaderInterface:
    return TemplateLoader(context_processor)
