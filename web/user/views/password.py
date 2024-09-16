from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from application.texts.errors import UserErrors
from application.texts.success_messages import Messages
from application.usecases.user.reset_password import (
    ResetPassword,
    ValidResetPasswordToken,
)
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.persistence.repositories.user_repository import get_user_repository
from web.common.views import FormView
from web.emails.email_service.email_service import get_email_service
from web.user.exceptions import InvalidJwtToken
from web.user.forms import ResetPasswordForm, SetPasswordForm
from web.user.models.user import User
from web.user.views.base_user_view import BaseUserView


@method_decorator(csrf_exempt, name="dispatch")
class ResetPasswordView(BaseUserView, FormView):
    template_name = "user/set-password.html"
    form_class = SetPasswordForm
    valid_reset_password_token_interactor = ValidResetPasswordToken(get_jwt_processor(), get_user_repository())
    reset_password_interactor = ResetPassword(get_jwt_processor(), get_user_repository())

    def get(self, request, token):
        try:
            user = self.valid_reset_password_token_interactor(token)
            self.login(user)
        except InvalidJwtToken as e:
            return HttpResponseRedirect(f"/?error={str(e)}")

        return super().get(request, token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SetPasswordForm()
        context["token"] = self.kwargs.get("token")

        return context

    def form_valid(self, request, form, token):
        try:
            user, access_token = self.reset_password_interactor(token, form.cleaned_data.get("password"))
            self.login(user)

            access_token = self.jwt_processor.create_access_token(user.username, user.id)

            return JsonResponse(
                {
                    "access_token": access_token,
                },
            )
        except InvalidJwtToken as e:
            return JsonResponse({"message": str(e)}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class SetPassword(BaseUserView, FormView):
    template_name = "user/set-password.html"
    form_class = SetPasswordForm

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

    def form_valid(self, request, form):
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


@method_decorator(csrf_exempt, name="dispatch")
class SendMailToResetPassword(FormView):
    template_name = "user/reset-password.html"
    email_service = get_email_service()
    form_class = ResetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reset_password_form"] = ResetPasswordForm()

        return context

    def form_valid(self, request, form):
        email = form.cleaned_data.get("email")

        user = User.objects.get_user_by_email(email)

        if user is None:
            form.add_error("email", UserErrors.user_by_email_not_found.value)
            return JsonResponse({"errors": form.errors}, status=400)

        self.email_service.send_mail_to_reset_password(user)

        return JsonResponse({"message": Messages.sent_message_to_reset_password.value})
