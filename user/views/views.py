from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from common.views import SubdomainMixin
from domens.get_domain import get_domain_string, get_partners_domain_string
from domens.models import Domain, Site
from emails.email_service.email_service import get_email_service
from settings.get_settings import get_settings
from user.forms import LoginForm, RegistrationForm, ResetPasswordForm, SetPasswordForm
from user.models import User
from user.serializers import UserSerializer
from user.views.base_user_view import BaseUserView
from utils.errors import Errors, UserErrors
from utils.success_messages import Messages
from utils.validators import is_valid_email, is_valid_phone


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(BaseUserView, SubdomainMixin):
    template_name = "user/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"] = RegistrationForm()

        return context

    @property
    def subdomain(self):
        subdomain = self.get_subdomain(self.request)
        if Site.objects.filter(subdomain=subdomain).exists():
            return Site.objects.get(subdomain=subdomain)

    @property
    def domain(self):
        domain = self.get_domain(self.request)
        if Domain.objects.filter(domain=domain).exists():
            return Domain.objects.get(domain=domain)

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
                        **form.cleaned_data, register_on_site=self.subdomain, register_on_domain=self.domain
                    )
            except Exception as e:
                print(e)
                form.add_error("email", UserErrors.something_went_wrong.value)
                return JsonResponse({"errors": form.errors}, status=400)

            print(user)
            request.user = user
            user = authenticate(request)
            login(request, user)

            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return JsonResponse({"token_to_set_password": token_to_set_password})

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ResetPassword(BaseUserView):
    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_reset_password_link.value}")

        user = User.objects.get_user_by_id(payload["id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_reset_password_link.value}")

        form = SetPasswordForm()

        settings = get_settings(request.domain, request.subdomain)

        if request.domain == "localhost":
            domain = "localhost:8000"
        else:
            domain = get_domain_string()

        partner_domain = get_partners_domain_string()

        return render(
            request,
            "user/set-password.html",
            {"form": form, "token": token, "settings": settings, "domain": domain, "partner_domain": partner_domain},
        )

    def post(self, request, token):
        form = SetPasswordForm(request.POST)

        if form.is_valid():
            payload = self.jwt_processor.validate_token(token)

            if not payload:
                return JsonResponse({"message": Errors.expired_set_password_token.value}, status=404)

            password = form.cleaned_data.get("password")

            user = User.objects.get_user_by_id(payload["id"])
            user.confirm_email()
            user.set_password(password)
            user.save()

            request.user = user
            user = authenticate(request)
            login(request, user)

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class SetPassword(BaseUserView):
    def get(self, request):
        if request.user is None:
            return HttpResponseRedirect("/user/login")
        
        if len(request.user.password) > 0:
            return HttpResponseRedirect("/my/")

        form = SetPasswordForm()

        settings = get_settings(request.domain, request.subdomain)

        if request.domain == "localhost":
            domain = "localhost:8000"
        else:
            domain = get_domain_string()

        partner_domain = get_partners_domain_string()

        return render(
            request,
            "user/set-password.html",
            {"form": form, "settings": settings, "domain": domain, "partner_domain": partner_domain},
        )

    def post(self, request):
        form = SetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")

            user = request.user
            user.set_password(password)
            user.save()

            request.user = user
            user = authenticate(request)
            login(request, user)

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )

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
            request.user = user
            user = authenticate(request)
            login(request, user)

            return JsonResponse({"acess_token": access_token})

        return JsonResponse({"errors": form.errors}, status=400)


class GetUserInfo(View):
    def get(self, request):
        user_from_request = request.user
        user_from_header = request.user_from_header

        user = None
        if user_from_header:
            user = user_from_header
        if user_from_request.is_authenticated:
            user = user_from_request

        if user:
            user = UserSerializer(user).data
            return JsonResponse(user)
        else:
            return HttpResponse(status=401)


class ConfirmEmail(BaseUserView):
    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link.value}")

        user = User.objects.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link.value}")

        user.confirm_email()
        request.user = user
        user = authenticate(request)
        login(request, user)

        if user.password is None or not user.password:
            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return HttpResponseRedirect(f"/user/password/{token_to_set_password}")

        return HttpResponseRedirect(
            f"/my/?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )


@method_decorator(csrf_exempt, name="dispatch")
class SendMailToResetPassword(View):
    template_name = "user/reset-password.html"
    email_service = get_email_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            user = User.objects.get_user_by_email(email)
            print(user)
            if user is None:
                form.add_error("email", UserErrors.user_by_email_not_found.value)
                return JsonResponse({"errors": form.errors}, status=400)

            self.email_service.send_mail_to_reset_password(user)

            return JsonResponse({"message": Messages.sent_message_to_reset_password.value})

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class SetToken(BaseUserView):
    template_name = "user/set-token.html"

    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)
        if payload:
            user = User.objects.get_user_by_id(payload["id"])
            request.user = user
            user = authenticate(request)
            login(request, user)

            return render(request, "user/set-token.html", {"token": token})

        return HttpResponse(status=401)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")
