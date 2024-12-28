from typing import Any, Protocol

from django.http.request import HttpRequest


class TemplateContextProcessorInterface(Protocol):
    def get_change_user_form_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_change_site_form_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_change_socials_form_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_referral_popup_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_create_idea_form(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_choice_product_form(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_create_user_product_form(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError

    def get_product_description_popup(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError
