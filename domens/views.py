from django.http import HttpResponse
from django.views.generic import View


class StopSite(View):
    def get(self, request):
        if self.request.user_from_header:
            self.request.user_from_header.site.deactivate()

            return HttpResponse(status=200)

        return HttpResponse(status=401)


class ActivateSite(View):
    def get(self, request):
        if self.request.user_from_header:
            self.request.user_from_header.site.activate()

            return HttpResponse(status=200)

        return HttpResponse(status=401)
