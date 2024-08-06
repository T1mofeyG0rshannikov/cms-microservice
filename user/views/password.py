from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from emails.email_service.email_service import get_email_service
from user.forms import ResetPasswordForm, SetPasswordForm
from user.models import User
from user.views.base_user_view import BaseUserView
from utils.errors import Errors, UserErrors
from utils.success_messages import Messages


@method_decorator(csrf_exempt, name="dispatch")
class ResetPassword(BaseUserView):
    template_name = "user/set-password.html"

    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_reset_password_link.value}")

        user = User.objects.get_user_by_id(payload["id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_reset_password_link.value}")

        self.login(user)

        return super().get(request, token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SetPasswordForm()
        context["token"] = self.kwargs.get("token")

        return context

    def post(self, request, token):
        form = SetPasswordForm(request.POST)

        if form.is_valid():
            payload = self.jwt_processor.validate_token(token)

            if not payload:
                return JsonResponse({"message": Errors.expired_set_password_token.value}, status=404)

            password = form.cleaned_data.get("password")

            user = User.objects.get_user_by_id(payload["id"])
            user.set_password(password)
            user.save()

            self.login(user)

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class SetPassword(BaseUserView):
    template_name = "user/set-password.html"

    def get(self, request):
        if request.user is None:
            return HttpResponseRedirect(self.login_url)

        if len(request.user.password) > 0:
            return HttpResponseRedirect(self.account_url)

        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SetPasswordForm()

        return context

    def post(self, request):
        form = SetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")

            user = request.user
            user.set_password(password)
            user.save()

            self.login(user)

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )

        return JsonResponse({"errors": form.errors}, status=400)


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

            if user is None:
                form.add_error("email", UserErrors.user_by_email_not_found.value)
                return JsonResponse({"errors": form.errors}, status=400)

            self.email_service.send_mail_to_reset_password(user)

            return JsonResponse({"message": Messages.sent_message_to_reset_password.value})

        return JsonResponse({"errors": form.errors}, status=400)
