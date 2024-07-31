from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from common.views import SubdomainMixin
from domens.get_domain import get_domain_string, get_partners_domain_string
from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface


class BaseUserView(SubdomainMixin):
    jwt_processor: JwtProcessorInterface = get_jwt_processor()


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/user/login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user_from_header and not request.user.is_authenticated:
            return self.handle_no_permission()

        path = request.build_absolute_uri()

        partner_domain_string = get_partners_domain_string()
        domain_string = get_domain_string()

        if partner_domain_string in path:
            path = path.replace(request.get_host(), domain_string)

            print(path)
            return HttpResponseRedirect(path)

        return super().dispatch(request, *args, **kwargs)
