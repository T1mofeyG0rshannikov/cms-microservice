from django.http import HttpResponse
from django.views.generic import TemplateView, View

from user.forms import LoginForm


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


class PartnerIndexPage(TemplateView):
    template_name = "domens/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()

        return context
