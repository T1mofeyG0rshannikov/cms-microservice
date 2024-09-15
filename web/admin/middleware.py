import os

from admin.views import JoomlaAdminPage
from django.http import HttpResponseNotFound
from dotenv import load_dotenv
from rest_framework.renderers import JSONRenderer

from application.services.domains.service import get_domain_service
from domain.domains.interfaces.domain_service_interface import DomainServiceInterface

load_dotenv()


class AdminMiddleware:
    admin_site_domain = os.getenv("ADMIN_DOMAIN")
    domain_service: DomainServiceInterface = get_domain_service()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        domain = self.domain_service.get_domain_string()

        if request.path.startswith("/admin/"):
            """if domain in request.get_host():
                return JoomlaAdminPage.as_view()(request)

            elif self.admin_site_domain in request.get_host():
                return response

            else:
                return HttpResponseNotFound("404 Page not found")"""

            response = JoomlaAdminPage.as_view()(request)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            try:
                response.render()
            except:
                pass

            return response

        return response
