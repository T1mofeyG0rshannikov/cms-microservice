from django.contrib.auth.mixins import AccessMixin
from django.views.generic import TemplateView

from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface


class BaseUserView(TemplateView):
    jwt_processor: JwtProcessorInterface = get_jwt_processor()


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
