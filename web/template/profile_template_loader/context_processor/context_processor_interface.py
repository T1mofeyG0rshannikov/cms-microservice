from typing import Protocol

from django.http import HttpRequest


class ProfileTemplateContextProcessorInterface(Protocol):
    def get_profile_context(self, request: HttpRequest):
        raise NotImplementedError

    def get_site_context(self, request: HttpRequest):
        raise NotImplementedError

    def get_refs_context(self, request: HttpRequest):
        raise NotImplementedError

    def get_manuals_context(self, request: HttpRequest):
        raise NotImplementedError

    def get_products_context(self, request: HttpRequest):
        raise NotImplementedError

    def get_ideas_context(self, request: HttpRequest):
        raise NotImplementedError

    def get_messanger_context(self, request: HttpRequest):
        raise NotImplementedError
