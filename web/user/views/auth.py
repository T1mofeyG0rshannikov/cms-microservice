from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from infrastructure.url_parser import get_url_parser
from application.texts.errors import UserErrors
from application.usecases.auth.login import Login
from application.usecases.auth.register import Register
from domain.user.exceptions import (
    UserDoesNotExist,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.repository import UserRepositoryInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.user.validator import get_user_validator
from web.common.views import FormView
from web.user.forms import LoginForm, RegistrationForm, ResetPasswordForm
from web.user.views.base_user_view import BaseUserView


class RegisterUser(BaseUserView, FormView):
    template_name = "user/register.html"
    form_class = RegistrationForm

    register_interactor = Register(
        get_user_repository(), get_domain_repository(), get_url_parser(), get_jwt_processor()
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"] = RegistrationForm()

        return context

    def form_valid(self, request: HttpRequest, form) -> JsonResponse:
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))
        ancor = request.POST.get("ancor")
        is_popup = request.POST.get("is_popup", "false") != "false"

        try:
            token_to_set_password = self.register_interactor(
                fields=form.cleaned_data, host=request.META.get("HTTP_ORIGIN")
            ).token_to_set_password
        except UserWithPhoneAlreadyExists:
            form.add_error("phone", UserErrors.user_with_phone_alredy_exists)

            user_activity_text = (
                f'''Ошибка регистрации в форме "{ancor}"'''
                if not is_popup
                else f"""Ошибка регистрации в попапе "{form.cleaned_data.get("username")}", "{form.cleaned_data.get("email")}", "{form.cleaned_data.get("phone")}"""
            )

            self.user_session_repository.create_user_action(
                adress=adress,
                text=user_activity_text,
                session_id=request.user_session_id,
            )

            return JsonResponse({"errors": form.errors}, status=400)

        except UserWithEmailAlreadyExists:
            form.add_error("email", UserErrors.user_with_email_alredy_exists)

            user_activity_text = (
                f'''Ошибка регистрации в форме "{ancor}"'''
                if not is_popup
                else f"""Ошибка регистрации в попапе "{form.cleaned_data.get("username")}", "{form.cleaned_data.get("email")}", "{form.cleaned_data.get("phone")}"""
            )

            self.user_session_repository.create_user_action(
                adress=adress,
                text=user_activity_text,
                session_id=self.request.user_session_id,
            )

            return JsonResponse({"errors": form.errors}, status=400)

        if token_to_set_password:
            # set register in session

            user_activity_text = (
                f'''Регистрация в форме "{ancor}"'''
                if not is_popup
                else f'''Регистрация в попапе "{form.cleaned_data.get("username")}", "{form.cleaned_data.get("email")}", "{form.cleaned_data.get("phone")}"'''
            )

            self.user_session_repository.create_user_action(
                adress=adress,
                text=user_activity_text,
                session_id=request.user_session_id,
            )

            return JsonResponse({"token_to_set_password": token_to_set_password})

        return JsonResponse({"errors": UserErrors.something_went_wrong}, status=400)


class LoginView(BaseUserView, FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    login_interactor = Login(get_user_repository(), get_user_validator(), get_jwt_processor())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["register_form"] = RegistrationForm()
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def form_valid(self, request: HttpRequest, form) -> JsonResponse:
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        try:
            access_token, user = self.login_interactor(form.cleaned_data)
            self.login(user)

            self.user_session_repository.create_user_action(
                adress=adress,
                text=f'''Вход в ЛК "{form.cleaned_data.get("phone_or_email")}"''',
                session_id=request.user_session_id,
            )

            return JsonResponse({"acess_token": access_token})
        except UserDoesNotExist as e:
            form.add_error("phone_or_email", str(e))

            self.user_session_repository.create_user_action(
                adress=adress,
                text=f'''Ошибка входа в ЛК "{form.cleaned_data.get("phone_or_email")}"''',
                session_id=request.user_session_id,
            )

            return JsonResponse({"errors": form.errors}, status=400)

        return JsonResponse({"errors": form.errors}, status=400)


class SetToken(BaseUserView):
    template_name = "user/set-token.html"
    repository: UserRepositoryInterface = get_user_repository()

    def get(self, request: HttpRequest, token):
        payload = self.jwt_processor.validate_token(token)
        if payload:
            user = self.repository.get_user_by_id(payload["id"])
            self.login(user)

            return render(request, "user/set-token.html", {"token": token})

        return HttpResponse(status=401)


class Logout(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect("/")
