from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)
from infrastructure.logging.admin import AdminLoginLogger
from infrastructure.persistence.repositories.admin_log_repository import (
    get_admin_log_repository,
)


@method_decorator(csrf_exempt, name="dispatch")
class JoomlaAdminPage(TemplateView):
    template_name = "admin/joomla.html"
    logger = AdminLoginLogger(get_admin_log_repository(), get_work_email_service())

    def post(self, request):
        print(request.POST)
        password = request.POST.get("passwd")

        self.logger.fake_admin_panel(
            request, {"username": request.POST.get("username"), "user": request.user, "password": password}
        )

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
