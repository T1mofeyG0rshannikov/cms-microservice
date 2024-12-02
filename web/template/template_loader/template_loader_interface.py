from typing import Any, Protocol

from django.http.request import HttpRequest


class TemplateLoaderInterface(Protocol):
    @staticmethod
    def load_template(
        app_name: str, template_name: str, request: HttpRequest = None, context: dict[Any, Any] = None
    ) -> str | None:
        raise NotImplementedError

    def load_change_user_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_change_site_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError

    def load_change_socials_form(self, request: HttpRequest) -> str | None:
        raise NotImplementedError
