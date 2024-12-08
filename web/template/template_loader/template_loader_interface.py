from typing import Any, Protocol

from django.http.request import HttpRequest


class TemplateLoaderInterface(Protocol):
    @staticmethod
    def load_template(
        app_name: str, template_name: str, request: HttpRequest = None, context: dict[str, Any] = None
    ) -> str | None:
        raise NotImplementedError

    def load_change_user_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_change_site_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_change_socials_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_choice_product_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_create_idea_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_delete_product_popup(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_referral_popup(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_create_user_product_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError
