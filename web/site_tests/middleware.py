import traceback

from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from infrastructure.logging.errors import ErrorLogger, get_error_logger
from infrastructure.persistence.models.site_tests import EnableErrorLogging
from infrastructure.requests.service import get_request_service


class ExceptionLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request: HttpRequest, response, logger: ErrorLogger = get_error_logger()):
        request_service = get_request_service(request)

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
