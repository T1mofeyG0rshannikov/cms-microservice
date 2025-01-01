from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from rest_framework import generics

from domain.domains.domain_repository import DomainRepositoryInterface
from domain.user.entities import UserInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from web.common.forms import FeedbackForm
from web.settings.views.settings_mixin import SettingsMixin
from web.user.forms import LoginForm, RegistrationForm, ResetPasswordForm


class BaseUserView(SettingsMixin):
    jwt_processor: JwtProcessorInterface = get_jwt_processor()
    login_url = "/user/login"
    account_url = "/my/"
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def login(self, user: UserInterface) -> None:
        self.request.user = user
        user = authenticate(self.request)
        login(self.request, user)


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/user/login"
    set_password_url = "/user/password"
    domain_repository: DomainRepositoryInterface = get_domain_repository()

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        path = request.build_absolute_uri()

        domain_string = self.domain_repository.get_domain_string()

        if request.partner_domain in path:
            path = path.replace(request.get_host(), domain_string)

            return HttpResponseRedirect(path)

        if request.user.password is None or not request.user.password:
            return HttpResponseRedirect(self.set_password_url)

        return super().dispatch(request, *args, **kwargs)


class UserFormsView:
    @classmethod
    def get_context_data(self) -> dict[str, Any]:
        return {
            "login_form": LoginForm(),
            "register_form": RegistrationForm(),
            "reset_password_form": ResetPasswordForm(),
            "feedback_form": FeedbackForm(),
        }


class APIUserRequired(View):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        return super().dispatch(request, *args, **kwargs)


class APIUserRequiredGenerics(generics.GenericAPIView):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        return super().dispatch(request, *args, **kwargs)
