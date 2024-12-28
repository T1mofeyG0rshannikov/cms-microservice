from dataclasses import dataclass
from typing import Any, Protocol

from django.http import HttpRequest


@dataclass
class ProfileTemplateLoaderResponse:
    title: str
    content: str


class ProfileTemplateLoaderInterface(Protocol):
    app_name: str

    def load_template(self, app_name: str, template_name: str, context: dict[str, Any] | None = None) -> str | None:
        raise NotImplementedError

    def get_title(self, page_title: str) -> str:
        raise NotImplementedError

    def load_messanger_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError

    def load_profile_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError

    def load_refs_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError

    def load_site_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError

    def load_manuals_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError

    def load_products_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError

    def load_ideas_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        raise NotImplementedError
