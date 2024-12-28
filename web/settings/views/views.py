from django.http import HttpResponse

from domain.user.sites.exceptions import SiteDoesNotExists
from infrastructure.requests.request_interface import RequestInterface
from web.settings.views.settings_mixin import SettingsMixin
from web.user.forms import LoginForm, ResetPasswordForm
from web.user.views.base_user_view import APIUserRequiredGenerics


class PartnerIndexPage(SettingsMixin):
    template_name = "common/domens/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["reset_password_form"] = ResetPasswordForm()

        return context


class StopSite(APIUserRequiredGenerics):
    def get(self, request: RequestInterface) -> HttpResponse:
        if not request.user.site:
            raise SiteDoesNotExists()

        request.user.site.deactivate()
        return HttpResponse(status=200)


class ActivateSite(APIUserRequiredGenerics):
    def get(self, request: RequestInterface) -> HttpResponse:
        if not request.user.site:
            raise SiteDoesNotExists()

        request.user.site.activate()
        return HttpResponse(status=200)
