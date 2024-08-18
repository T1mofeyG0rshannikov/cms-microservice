from typing import Any, Protocol

from django.http.request import HttpRequest


class TemplateContextProcessorInterface(Protocol):
    @staticmethod
    def get_context(request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError()

    def get_change_user_form_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError()

    def get_change_site_form_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError()

    def get_change_socials_form_context(self, request: HttpRequest) -> dict[Any, Any]:
        raise NotImplementedError()
