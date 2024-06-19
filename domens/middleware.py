from django.http import HttpResponseNotFound

from domens.admin import Domain


class BlockAdminPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        partner_domain = Domain.objects.filter(is_partners=True).first().domain

        if request.path.startswith("/admin/") and partner_domain in request.get_host():
            return HttpResponseNotFound("404 Page not found")

        return self.get_response(request)
