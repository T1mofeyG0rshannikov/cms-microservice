from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from settings.get_settings import get_settings
from user.auth.jwt_processor import JwtProcessor
from user.auth.jwt_settings import get_jwt_settings
from user.forms import RegistrationForm
from user.models import User
from utils.errors import UserErrors


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(View):
    def __init__(self):
        jwt_settings = get_jwt_settings()
        self.jwt_processor = JwtProcessor(jwt_settings)

    def get(self, request):
        form = RegistrationForm()

        settings = get_settings()

        return render(request, "user/register.html", {"form": form, "settings": settings})

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
