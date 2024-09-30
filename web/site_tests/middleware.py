import traceback

from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from infrastructure.email_services.work_email_service.context_processor.context_processor import (
    get_work_email_context_processor,
)
from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator import (
    get_work_email_template_generator,
)
from infrastructure.logging.errors import ErrorLogger
from infrastructure.persistence.models.site_tests import EnableErrorLogging
from infrastructure.persistence.repositories.errors_repository import (
    get_errors_repository,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)
from infrastructure.requests.service import get_request_service


class ExceptionLoggingMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def process_response(self, request: HttpRequest, response):
        request_service = get_request_service(request)

        logger = ErrorLogger(
            get_errors_repository(),
            get_work_email_service(
                get_work_email_template_generator(get_work_email_context_processor()), get_system_repository()
            ),
        )

        status_code = response.status_code
        if 500 <= status_code < 600:
            user = request.user if request.user.is_authenticated else None

            enable_logging = EnableErrorLogging.objects.first()
            enable_logging = enable_logging.enable_error_logging if enable_logging else False

            if enable_logging:
                logger(
                    message=request.error_message,
                    client_ip=request_service.get_client_ip(),
                    path=request.build_absolute_uri(),
                    user=user,
                )

        return response

    def process_exception(self, request, exception):
        error_message = traceback.format_exc()
        request.error_message = error_message
