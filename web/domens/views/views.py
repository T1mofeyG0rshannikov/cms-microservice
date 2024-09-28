from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from web.settings.views import SettingsMixin
from web.user.forms import LoginForm, ResetPasswordForm


class StopSite(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            request.user.site.deactivate()

            return HttpResponse(status=200)

        return HttpResponse(status=401)


class ActivateSite(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            self.request.user.site.activate()

            return HttpResponse(status=200)

        return HttpResponse(status=401)


class PartnerIndexPage(SettingsMixin):
    template_name = "domens/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["reset_password_form"] = ResetPasswordForm()

        return context
