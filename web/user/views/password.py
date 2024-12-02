from django.http import HttpRequest, HttpResponseRedirect, JsonResponse

from application.common.base_url_parser import UrlParserInterface
from infrastructure.url_parser import get_url_parser
from application.texts.errors import UserErrors
from application.texts.success_messages import Messages
from application.usecases.user.reset_password import (
    ResetPassword,
    ValidResetPasswordToken,
)
from domain.user.exceptions import InvalidJwtToken
from domain.user.repository import UserRepositoryInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.email_services.email_service.email_service import get_email_service
from infrastructure.email_services.email_service.email_service_interface import (
    EmailServiceInterface,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from web.common.views import FormView
from web.user.forms import ResetPasswordForm, SetPasswordForm
from web.user.views.base_user_view import BaseUserView


class ResetPasswordView(BaseUserView, FormView):
    template_name = "user/set-password.html"
    form_class = SetPasswordForm
    valid_reset_password_token_interactor = ValidResetPasswordToken(get_jwt_processor(), get_user_repository())
    reset_password_interactor = ResetPassword(get_jwt_processor(), get_user_repository())

    def get(self, request, token):
        try:
            user = self.valid_reset_password_token_interactor(token)
            self.login(user)
        except InvalidJwtToken as e:
            return HttpResponseRedirect(f"/?error={str(e)}")

        return super().get(request, token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SetPasswordForm()
        context["token"] = self.kwargs.get("token")

        return context

    def form_valid(self, request, form, token):
        try:
            user, access_token = self.reset_password_interactor(token, form.cleaned_data.get("password"))
            self.login(user)

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )
        except InvalidJwtToken as e:
            return JsonResponse({"message": str(e)}, status=404)


class SetPassword(BaseUserView, FormView):
    template_name = "user/set-password.html"
    form_class = SetPasswordForm
    user_session_repository = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def get(self, request):
        if request.user is None:
            return HttpResponseRedirect(self.login_url)

        if len(request.user.password) > 0:
            return HttpResponseRedirect(self.account_url)

        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SetPasswordForm()

        return context

    def form_valid(self, request: HttpRequest, form):
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))
        password = form.cleaned_data.get("password")

        user = request.user
        user.set_password(password)
        user.save()

        self.login(user)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f"""Установил пароль""",
            session_id=request.user_session_id,
        )

        return JsonResponse(
            {
                "access_token": access_token,
            },
        )


class SendMailToResetPassword(FormView):
    template_name = "user/reset-password.html"
    email_service: EmailServiceInterface = get_email_service()
    form_class = ResetPasswordForm
    user_repository: UserRepositoryInterface = get_user_repository()
    user_session_repository = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def form_valid(self, request: HttpRequest, form):
        email = form.cleaned_data.get("email")
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        user = self.user_repository.get_user_by_email(email)

        if user is None:
            self.user_session_repository.create_user_action(
                adress=adress,
                text=f'''Ошибка восстановления пароля "{email}"''',
                session_id=request.user_session_id,
            )

            form.add_error("email", UserErrors.user_by_email_not_found)
            return JsonResponse({"errors": form.errors}, status=400)

        self.email_service.send_mail_to_reset_password(user)

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f'''Восстановление пароля "{email}"''',
            session_id=request.user_session_id,
        )

        return JsonResponse({"message": Messages.sent_message_to_reset_password})
