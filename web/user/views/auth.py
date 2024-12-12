from typing import Any

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from application.texts.errors import UserErrorsMessages
from application.usecases.auth.login import Login, get_login_interactor
from application.usecases.auth.register import Register, get_register_interactor
from domain.user.exceptions import (
    UserDoesNotExist,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.repository import UserRepositoryInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.requests.request_interface import RequestInterface
from web.common.views import FormView
from web.user.forms import LoginForm, RegistrationForm, ResetPasswordForm
from web.user.views.base_user_view import BaseUserView


class RegisterUser(BaseUserView, FormView):
    template_name = "user/register.html"
    form_class = RegistrationForm

    register_interactor: Register = get_register_interactor()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["register_form"] = RegistrationForm()

        return context

    def form_valid(self, request: RequestInterface, form: RegistrationForm) -> JsonResponse:
        ancor = request.POST.get("ancor")
        is_popup = request.POST.get("is_popup", "false") != "false"
        user_activity_text = None

        try:
            token_to_set_password = self.register_interactor(
                email=form.cleaned_data.get("email"),
                phone=form.cleaned_data.get("phone"),
                host=request.META.get("HTTP_ORIGIN"),
            ).token_to_set_password
        except UserWithPhoneAlreadyExists as e:
            form.add_error("phone", str(e))

            user_activity_text = (
                f'''Ошибка регистрации в форме "{ancor}"'''
                if not is_popup
                else f"""Ошибка регистрации в попапе "{form.cleaned_data.get("username")}", "{form.cleaned_data.get("email")}", "{form.cleaned_data.get("phone")}"""
            )

        except UserWithEmailAlreadyExists as e:
            form.add_error("email", str(e))

            user_activity_text = (
                f'''Ошибка регистрации в форме "{ancor}"'''
                if not is_popup
                else f"""Ошибка регистрации в попапе "{form.cleaned_data.get("username")}", "{form.cleaned_data.get("email")}", "{form.cleaned_data.get("phone")}"""
            )

        if user_activity_text:
            self.create_user_session_log(request, user_activity_text)

            return JsonResponse({"errors": form.errors}, status=400)

        if token_to_set_password:
            user_activity_text = (
                f'''Регистрация в форме "{ancor}"'''
                if not is_popup
                else f'''Регистрация в попапе "{form.cleaned_data.get("username")}", "{form.cleaned_data.get("email")}", "{form.cleaned_data.get("phone")}"'''
            )

            self.create_user_session_log(request, user_activity_text)

            return JsonResponse({"token_to_set_password": token_to_set_password})

        return JsonResponse({"errors": UserErrorsMessages.something_went_wrong}, status=400)


class LoginView(BaseUserView, FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    login_interactor: Login = get_login_interactor()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["register_form"] = RegistrationForm()
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def form_valid(self, request: RequestInterface, form: LoginForm) -> JsonResponse:
        try:
            access_token, user = self.login_interactor(**form.cleaned_data)
            self.login(user)

            self.create_user_session_log(request, text=f'''Вход в ЛК "{form.cleaned_data.get("phone_or_email")}"''')

            return JsonResponse({"acess_token": access_token})
        except UserDoesNotExist as e:
            form.add_error("phone_or_email", str(e))

            self.create_user_session_log(
                request, text=f'''Ошибка входа в ЛК "{form.cleaned_data.get("phone_or_email")}"'''
            )

            return JsonResponse({"errors": form.errors}, status=400)

        return JsonResponse({"errors": form.errors}, status=400)


class SetToken(BaseUserView):
    template_name = "user/set-token.html"
    user_repository: UserRepositoryInterface = get_user_repository()

    def get(self, request: HttpRequest, token: str) -> HttpResponse:
        payload = self.jwt_processor.validate_token(token)
        if payload:
            user = self.user_repository.get(id=payload["id"])
            self.login(user)

            return render(request, "user/set-token.html", {"token": token})

        return HttpResponse(status=401)


class Logout(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect("/")
