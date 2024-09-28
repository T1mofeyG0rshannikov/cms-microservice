import random

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from application.usecases.user.get_admin import GetAdminUser
from domain.email.exceptions import CantSendMailError
from domain.email.repository import SystemRepositoryInterface
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist
from infrastructure.email_services.email_service.email_service import get_email_service
from infrastructure.email_services.email_service.email_service_interface import (
    EmailServiceInterface,
)
from infrastructure.email_services.work_email_service.context_processor.context_processor import (
    get_work_email_context_processor,
)
from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)
from infrastructure.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator import (
    get_work_email_template_generator,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository


class SendConfirmEmail(View):
    email_service: EmailServiceInterface = get_email_service()

    def get(self, request: HttpRequest):
        user = request.user

        if user:
            try:
                self.email_service.send_mail_to_confirm_email(user)
            except CantSendMailError:
                return JsonResponse({"error": "Что-то пошло не так, повторите попытку чуть позже"}, status=503)

            return HttpResponse(status=200)

        return HttpResponse(status=401)


class LoginCodeGenerator:
    def __init__(self, repository: SystemRepositoryInterface):
        self.repository = repository

    def generate_admin_login_code(self, email: str) -> int:
        code = random.randrange(100000, 1000000)

        admin_code = self.repository.update_or_create_admin_code(email=email, code=code)
        print(admin_code)
        return admin_code


class SendAdminAuthCode(View):
    email_service: WorkEmailServiceInterface = get_work_email_service(
        get_work_email_template_generator(get_work_email_context_processor()), get_system_repository()
    )
    code_generator = LoginCodeGenerator(get_system_repository())
    get_admin_user_interactor = GetAdminUser(get_user_repository())

    def get(self, request):
        email = request.GET.get("username")
        password = request.GET.get("password")

        try:
            user = self.get_admin_user_interactor(email, password)
            code = self.code_generator.generate_admin_login_code(user.email)
            self.email_service.send_code_to_login_in_admin(user.email, code)

            return HttpResponse(status=200)
        except CantSendMailError:
            return JsonResponse({"error": "Что-то пошло не так, повторите попытку чуть позже"}, status=503)
        except (UserDoesNotExist, IncorrectPassword) as e:
            return JsonResponse({"error": str(e)}, status=400)

        return HttpResponse(status=401)
