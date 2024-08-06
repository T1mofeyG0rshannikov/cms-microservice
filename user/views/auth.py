from django.contrib.auth import logout
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from domens.domain_service.domain_service import get_domain_service
from domens.domain_service.domain_service_interface import DomainServiceInterface
from user.forms import LoginForm, RegistrationForm, ResetPasswordForm
from user.models import User
from user.views.base_user_view import BaseUserView
from utils.errors import UserErrors
from utils.validators import is_valid_email, is_valid_phone


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(BaseUserView):
    template_name = "user/register.html"
    domain_service: DomainServiceInterface = get_domain_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"] = RegistrationForm()

        return context

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")

            user_with_phone = User.objects.get_user_by_phone(phone)
            user_with_email = User.objects.get_user_by_email(email)

            if user_with_email is not None and user_with_email.email_is_confirmed:
                form.add_error("email", UserErrors.username_with_email_alredy_exists.value)

                return JsonResponse({"errors": form.errors}, status=400)

            elif user_with_phone is not None and user_with_phone.phone_is_confirmed:
                form.add_error("phone", UserErrors.username_with_phone_alredy_exists.value)

                return JsonResponse({"errors": form.errors}, status=400)

            try:
                with transaction.atomic():
                    User.objects.filter(email=email).update(email=None)
                    User.objects.filter(phone=phone).update(phone=None)

                    user = User.objects.create_user(
                        **form.cleaned_data,
                        register_on_site=self.domain_service.get_site_model(request),
                        register_on_domain=self.domain_service.get_domain_model_from_request(request),
                    )
            except Exception as e:
                print(e)
                form.add_error("email", UserErrors.something_went_wrong.value)
                return JsonResponse({"errors": form.errors}, status=400)

            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return JsonResponse({"token_to_set_password": token_to_set_password})

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class Login(BaseUserView):
    template_name = "user/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["register_form"] = RegistrationForm()
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_or_email = form.cleaned_data.get("phone_or_email")
            password = form.cleaned_data.get("password")

            if is_valid_phone(phone_or_email):
                user = User.objects.get_user_by_phone(phone_or_email)
                if user is None:
                    form.add_error("phone_or_email", UserErrors.user_by_phone_not_found.value)

                    return JsonResponse({"errors": form.errors}, status=400)

            elif is_valid_email(phone_or_email):
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

        return JsonResponse({"errors": form.errors}, status=400)


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
