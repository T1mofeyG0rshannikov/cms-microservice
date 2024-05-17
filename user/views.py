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
from user.forms import LoginForm, RegistrationForm
from user.models import User
from utils.errors import UserErrors
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
            phone = get_raw_phone(phone)

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
        return render(request, "user/set-password.html", {"token": token})

    def post(self, request, token):
        data = json.loads(request.body)

        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return JsonResponse({"message": "срок действия токена для ввода пароля истёк"}, status=404)

        password = data.get("password")

        User.objects.filter(id=payload["id"]).update(password=password)

        return HttpResponse(status=200)


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
            print(access_token)

            return render(request, "user/login.html", {"form": form, "acess_token": access_token})

        return render(request, "user/login.html", {"form": form})
