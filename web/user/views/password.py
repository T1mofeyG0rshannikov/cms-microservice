from typing import Any

from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from application.email_services.user_email_service.email_service_interface import (
    EmailServiceInterface,
)
from application.texts.errors import UserErrorsMessages
from application.texts.success_messages import Messages
from application.texts.user_session import UserActions
from application.usecases.user.reset_password import (
    ResetPassword,
    ValidResetPasswordToken,
    get_reset_password_interactor,
    get_valid_reset_pass_token_interactor,
)
from domain.user.exceptions import InvalidJwtToken
from domain.user.repository import UserRepositoryInterface
from infrastructure.email_services.email_service.email_service import get_email_service
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.requests.request_interface import RequestInterface
from web.common.views import FormView
from web.styles.views import StylesMixin
from web.user.forms import ResetPasswordForm, SetPasswordForm
from web.user.views.base_user_view import BaseUserView


class ResetPasswordView(BaseUserView, FormView, StylesMixin):
    form_class = SetPasswordForm
    valid_reset_password_token_interactor: ValidResetPasswordToken = get_valid_reset_pass_token_interactor()
    reset_password_interactor: ResetPassword = get_reset_password_interactor()

    def get(self, request: HttpRequest, *args, token: str, **kwargs):
        try:
            user = self.valid_reset_password_token_interactor(token)
            self.login(user)
        except InvalidJwtToken as e:
            return HttpResponseRedirect(f"/?error={str(e)}")

        context = super().get_context_data() | self.get_styles_context()
        context |= {"form": SetPasswordForm(), "token": token}

        return render(request, "user/set-password.html", context)

    def form_valid(self, request: HttpRequest, form: SetPasswordForm, token: str) -> JsonResponse:
        try:
            user, access_token = self.reset_password_interactor(token, form.cleaned_data.get("password"))
            self.login(user)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )
        except InvalidJwtToken as e:
            return JsonResponse({"message": str(e)}, status=404)


class SetPassword(BaseUserView, FormView, StylesMixin):
    template_name = "user/set-password.html"
    form_class = SetPasswordForm

    def get(self, request: HttpRequest):
        if request.user is None:
            return HttpResponseRedirect(self.login_url)

        if len(request.user.password) > 0:
            return HttpResponseRedirect(self.account_url)

        return super().get(request)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs) | self.get_styles_context()
        context["form"] = SetPasswordForm()

        return context

    def form_valid(self, request: RequestInterface, form: SetPasswordForm) -> JsonResponse:
        password = form.cleaned_data.get("password")

        user = request.user
        user.set_password(password)
        self.login(user)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        self.create_user_session_log(
            request=request,
            text=UserActions.set_password,
        )

        return JsonResponse(
            {
                "access_token": access_token,
            },
        )


class SendMailToResetPassword(FormView, StylesMixin):
    template_name = "user/reset-password.html"
    email_service: EmailServiceInterface = get_email_service()
    form_class = ResetPasswordForm
    user_repository: UserRepositoryInterface = get_user_repository()
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs) | self.get_styles_context()
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def form_valid(self, request: RequestInterface, form: ResetPasswordForm) -> JsonResponse:
        email = form.cleaned_data.get("email")

        user = self.user_repository.get(email=email)

        if user is None:
            self.create_user_session_log(
                request=request,
                text=f'''Ошибка восстановления пароля "{email}"''',
            )

            form.add_error("email", UserErrorsMessages.user_by_email_not_found)
            return JsonResponse({"errors": form.errors}, status=400)

        self.email_service.send_mail_to_reset_password(user)

        self.create_user_session_log(
            request=request,
            text=f'''Восстановление пароля "{email}"''',
        )

        return JsonResponse({"message": Messages.sent_message_to_reset_password})
