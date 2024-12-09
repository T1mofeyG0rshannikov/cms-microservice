from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from application.email_services.user_email_service.email_service_interface import (
    EmailServiceInterface,
)
from application.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)
from application.texts.errors import ErrorsMessages
from application.usecases.user.get_admin import (
    GetAdminUser,
    get_get_admin_user_interactor,
)
from domain.email.exceptions import CantSendMailError
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist
from infrastructure.email_services.admin_code_generator import (
    LoginCodeGenerator,
    get_login_code_generator,
)
from infrastructure.email_services.email_service.email_service import get_email_service
from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)


class SendConfirmEmail(View):
    email_service: EmailServiceInterface = get_email_service()

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        if user.is_authenticated:
            try:
                self.email_service.send_mail_to_confirm_email(user)
            except CantSendMailError:
                return JsonResponse({"error": ErrorsMessages.something_went_wrong}, status=503)

            return HttpResponse(status=200)

        return HttpResponse(status=401)


class SendAdminAuthCode(View):
    email_service: WorkEmailServiceInterface = get_work_email_service()
    code_generator: LoginCodeGenerator = get_login_code_generator()
    get_admin_user_interactor: GetAdminUser = get_get_admin_user_interactor()

    def get(self, request: HttpRequest) -> HttpResponse:
        email = request.GET.get("username")
        password = request.GET.get("password")

        try:
            user = self.get_admin_user_interactor(email, password)
            code = self.code_generator.generate_admin_login_code(user.email)
            self.email_service.send_code_to_login_in_admin(user.email, code)

            return HttpResponse(status=200)
        except CantSendMailError:
            return JsonResponse({"error": ErrorsMessages.something_went_wrong}, status=503)
        except (UserDoesNotExist, IncorrectPassword) as e:
            return JsonResponse({"error": str(e)}, status=400)

        return HttpResponse(status=401)
