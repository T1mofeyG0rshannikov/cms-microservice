from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from common.views import FormView
from domens.domain_repository.repository import get_domain_repository
from infrastructure.persistence.repositories.user_repository import get_user_repository
from user.auth.jwt_processor import get_jwt_processor
from user.exceptions import UserWithEmailAlreadyExists, UserWithPhoneAlreadyExists
from user.forms import LoginForm, RegistrationForm, ResetPasswordForm
from user.models.user import User
from user.url_parser import get_url_parser
from user.usecases.auth.register import Register
from user.validator.validator import get_user_validator
from user.validator.validator_interface import UserValidatorInterface
from user.views.base_user_view import BaseUserView
from utils.errors import UserErrors


@method_decorator(csrf_exempt, name="dispatch")
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

    def form_valid(self, request, form):
        try:
            token_to_set_password = self.register_interactor(
                fields=form.cleaned_data, host=request.META.get("HTTP_ORIGIN")
            )
        except UserWithPhoneAlreadyExists:
            form.add_error("phone", UserErrors.username_with_phone_alredy_exists.value)
            return JsonResponse({"errors": form.errors}, status=400)

        except UserWithEmailAlreadyExists:
            form.add_error("email", UserErrors.username_with_email_alredy_exists.value)
            return JsonResponse({"errors": form.errors}, status=400)

        if token_to_set_password:
            return JsonResponse({"token_to_set_password": token_to_set_password})

        return JsonResponse({"errors": UserErrors.something_went_wrong.value}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class Login(BaseUserView, FormView):
    template_name = "user/login.html"
    validator: UserValidatorInterface = get_user_validator()
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["register_form"] = RegistrationForm()
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def form_valid(self, request, form):
        phone_or_email = form.cleaned_data.get("phone_or_email")
        password = form.cleaned_data.get("password")

        if self.validator.is_valid_phone(phone_or_email):
            user = User.objects.get_user_by_phone(phone_or_email)
            if user is None:
                form.add_error("phone_or_email", UserErrors.user_by_phone_not_found.value)

                return JsonResponse({"errors": form.errors}, status=400)

        elif self.validator.is_valid_email(phone_or_email):
            user = User.objects.get_user_by_email(phone_or_email)
            if user is None:
                form.add_error("phone_or_email", UserErrors.user_by_email_not_found.value)

                return JsonResponse({"errors": form.errors}, status=400)

        else:
            form.add_error("phone_or_email", UserErrors.incorrect_login.value)

            return JsonResponse({"errors": form.errors}, status=400)

        if not user.verify_password(password):
            form.add_error("password", UserErrors.incorrect_password.value)

            return JsonResponse({"errors": form.errors}, status=400)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)
        self.login(user)

        return JsonResponse({"acess_token": access_token})


@method_decorator(csrf_exempt, name="dispatch")
class SetToken(BaseUserView):
    template_name = "user/set-token.html"

    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)
        if payload:
            user = User.objects.get_user_by_id(payload["id"])
            self.login(user)

            return render(request, "user/set-token.html", {"token": token})

        return HttpResponse(status=401)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")
