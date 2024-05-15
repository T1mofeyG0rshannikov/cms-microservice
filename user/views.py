from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from settings.get_settings import get_settings
from user.forms import RegistrationForm


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(View):
    def get(self, request):
        form = RegistrationForm()

        settings = get_settings()

        return render(request, "user/register.html", {"form": form, "settings": settings})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"], password=form.cleaned_data["password"]
            )

            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            login(request, user)

            return redirect("/user/profile")

        return render(request, "user/register.html", {"form": form})
