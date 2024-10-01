from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from infrastructure.email_services.work_email_service.context_processor.context_processor import (
    get_work_email_context_processor,
)
from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator import (
    get_work_email_template_generator,
)
from infrastructure.logging.admin import AdminLoginLogger
from infrastructure.persistence.repositories.admin_log_repository import (
    get_admin_log_repository,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)
from infrastructure.requests.service import get_request_service


@method_decorator(csrf_exempt, name="dispatch")
class JoomlaAdminPage(TemplateView):
    template_name = "admin/joomla.html"

    def dispatch(self, request, *args, **kwargs):
        self.logger = AdminLoginLogger(
            get_admin_log_repository(),
            get_work_email_service(
                get_work_email_template_generator(get_work_email_context_processor()), get_system_repository()
            ),
            get_request_service(request),
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        password = request.POST.get("passwd")

        self.logger.fake_admin_panel(
            {"username": request.POST.get("username"), "user": request.user, "password": password}
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
