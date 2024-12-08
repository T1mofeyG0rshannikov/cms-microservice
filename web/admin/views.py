from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from infrastructure.logging.admin import get_admin_logger
from infrastructure.requests.service import get_request_service


@method_decorator(csrf_exempt, name="dispatch")
class JoomlaAdminPage(TemplateView):
    template_name = "admin/joomla.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.logger = get_admin_logger(get_request_service(request))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest):
        password = request.POST.get("passwd")

        user = request.user if request.user.is_authenticated else None

        self.logger.fake_admin_panel(username=request.POST.get("username"), user=user, password=password)

        error_message = (
            "Empty password not allowed"
            if not password
            else "Username and password do not match or you do not have an account yet."
        )

        return render(
            request,
            "admin/joomla.html",
            {"error": error_message},
        )
