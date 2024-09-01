from typing import Protocol

from django.http import HttpRequest


class ProfileTemplateContextProcessorInterface(Protocol):
    def get_profile_template_context(self, request: HttpRequest):
        raise NotImplementedError()

    def get_site_template_context(self, request: HttpRequest):
        raise NotImplementedError()

    def get_refs_template_context(self, request: HttpRequest):
        raise NotImplementedError()

    def get_manuals_template_context(self, request: HttpRequest):
        raise NotImplementedError()

    def get_products_template_context(self, request: HttpRequest):
        raise NotImplementedError()
