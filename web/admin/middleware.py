from django.http import HttpRequest, HttpResponseNotFound
from rest_framework.renderers import JSONRenderer

from domain.domains.domain_repository import DomainRepositoryInterface
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from web.admin.views import JoomlaAdminPage


class AdminMiddleware:
    domain_repository: DomainRepositoryInterface = get_domain_repository()

    def __init__(self, get_response):
        self.get_response = get_response
        self.settings = get_admin_settings()

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        if request.path.startswith("/" + self.settings.admin_url):
            if (
                self.settings.admin_domain in request.get_host()
                or "127.0.0.1" in request.get_host()
                or "localhost" in request.get_host()
            ):
                return response
            else:
                return HttpResponseNotFound()

        if request.path.startswith("/admin/"):
            domain = self.domain_repository.get_domain_string()

            if domain in request.get_host() or "127.0.0.1" in request.get_host():
                response = JoomlaAdminPage.as_view()(request)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                try:
                    response.render()
                except:
                    pass

                return response

            else:
                return HttpResponseNotFound("404 Page not found")

        return response
