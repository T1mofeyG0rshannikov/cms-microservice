from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from common.views import SubdomainMixin
from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface


class BaseUserView(TemplateView, SubdomainMixin):
    jwt_processor: JwtProcessorInterface = get_jwt_processor()


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/user/login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user_from_header and not request.user.is_authenticated:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
