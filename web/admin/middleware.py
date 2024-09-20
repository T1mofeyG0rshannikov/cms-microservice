import os

from django.http import HttpResponseNotFound
from dotenv import load_dotenv
from rest_framework.renderers import JSONRenderer

from application.services.domains.service import get_domain_service
from domain.domains.service import DomainServiceInterface
from web.admin.views import JoomlaAdminPage

load_dotenv()


class AdminMiddleware:
    admin_site_domain = os.getenv("ADMIN_DOMAIN")
    admin_site_url = "/" + os.getenv("ADMIN_URL") + "/"
    domain_service: DomainServiceInterface = get_domain_service()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith(self.admin_site_url):
            if (
                self.admin_site_domain in request.get_host()
                or "127.0.0.1" in request.get_host()
                or "localhost" in request.get_host()
            ):
                return response
            else:
                return HttpResponseNotFound()

        if request.path.startswith("/admin/"):
            domain = self.domain_service.get_domain_string()

            if domain in request.get_host():
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
