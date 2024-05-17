import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from common.views import BaseTemplateView
from user.auth.jwt_processor import JwtProcessor, get_jwt_processor
from user.forms import LoginForm, RegistrationForm, SetPasswordForm
from user.models import User
from user.serializers import UserSerializer
from utils.errors import Errors, UserErrors
from utils.format_phone import get_raw_phone
from utils.validators import is_valid_phone


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(BaseTemplateView):
    template_name = "user/register.html"

    def __init__(self):
        super().__init__()
        self.jwt_processor: JwtProcessor = get_jwt_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RegistrationForm()

        return context

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")

            user_with_phone = User.objects.filter(phone=phone).first()
            user_with_email = User.objects.filter(email=email).filter(email_is_confirmed=True).first()

            if user_with_email is not None:
                form.add_error("email", UserErrors.username_with_email_alredy_exists.value)

                return render(request, "user/register.html", {"form": form})

            if user_with_phone is not None:
                if user_with_phone.email_is_confirmed:
                    form.add_error("phone", UserErrors.username_with_phone_alredy_exists)

                    return render(request, "user/register.html", {"form": form})

            user = User.objects.create(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                phone=form.cleaned_data.get("phone"),
            )

            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return redirect(f"/user/password/{token_to_set_password}")

        return render(request, "user/register.html", {"form": form})


@method_decorator(csrf_exempt, name="dispatch")
class SetPassword(View):
    def __init__(self):
        self.jwt_processor = get_jwt_processor()

    def get(self, request, token):
        form = SetPasswordForm()
        return render(request, "user/set-password.html", {"form": form, "token": token})

    def post(self, request, token):
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            payload = self.jwt_processor.validate_token(token)
            print(payload)

            if not payload:
                return JsonResponse({"message": Errors.expired_set_password_token.value}, status=404)

            password = form.cleaned_data.get("password")

            User.objects.filter(id=payload["id"]).update(password=password)

            user = User.objects.get(id=payload["id"])

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return render(request, "user/set-password.html", {"access_token": access_token})

        return render(request, "user/set-password.html", {"form": form, "token": token})


@method_decorator(csrf_exempt, name="dispatch")
class Login(BaseTemplateView):
    template_name = "user/login.html"

    def __init__(self):
        super().__init__()
        self.jwt_processor: JwtProcessor = get_jwt_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()

        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_or_email = form.cleaned_data.get("phone_or_email")
            password = form.cleaned_data.get("password")

            if is_valid_phone(phone_or_email):
                try:
                    user = User.objects.get(phone=phone_or_email)
                except User.DoesNotExist:
                    form.add_error("phone_or_email", UserErrors.user_by_phone_not_found.value)
                    return render(request, "user/login.html", {"form": form})

            else:
                try:
                    user = User.objects.get(email=phone_or_email)
                except User.DoesNotExist:
                    form.add_error("phone_or_email", UserErrors.user_by_email_not_found.value)
                    return render(request, "user/login.html", {"form": form})

            if user.password != password:
                form.add_error("password", UserErrors.incorrect_password.value)
                return render(request, "user/login.html", {"form": form})

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return render(request, "user/login.html", {"acess_token": access_token})

        return render(request, "user/login.html", {"form": form})


class Profile(BaseTemplateView):
    template_name = "user/profile.html"


class GetUserInfo(View):
    def __init__(self):
        self.jwt_processor: JwtProcessor = get_jwt_processor()

    def get(self, request):
        token = request.headers.get("Authorization")
        payload = self.jwt_processor.validate_token(token)

        user = None

        if payload:
            user = User.objects.get(id=payload["id"])
            user = UserSerializer(user).data

        return JsonResponse(user)
