from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from domens.domain_service.domain_service import DomainService
from domens.views.mixins import SubdomainMixin
from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.forms import LoginForm, RegistrationForm, ResetPasswordForm


class BaseUserView(SubdomainMixin):
    jwt_processor: JwtProcessorInterface = get_jwt_processor()
    login_url = "/user/login"
    account_url = "/my/"


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/user/login"
    set_password_url = "/user/password"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user_from_header and not request.user.is_authenticated:
            return self.handle_no_permission()

        path = request.build_absolute_uri()

        partner_domain_string = DomainService.get_partners_domain_string()
        domain_string = DomainService.get_domain_string()

        if partner_domain_string in path:
            path = path.replace(request.get_host(), domain_string)

            return HttpResponseRedirect(path)

        if request.user.password is None or not request.user.password:
            return HttpResponseRedirect(self.set_password_url)

        return super().dispatch(request, *args, **kwargs)


class UserFormsView:
    @classmethod
    def get_context_data(self):
        context = {}
        context["login_form"] = LoginForm()
        context["register_form"] = RegistrationForm()
        context["reset_password_form"] = ResetPasswordForm()
        return context
