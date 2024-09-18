from django import forms
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.validator.validator import get_user_validator

from application.texts.errors import UserErrors
from domain.user.validator_interface import UserValidatorInterface
from infrastructure.email_service.email_service import get_email_service
from infrastructure.logging.admin import AdminLoginLogger
from infrastructure.persistence.repositories.admin_log_repository import (
    get_admin_log_repository,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository


class CustomAuthenticationAdminForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("Пожалуйста введите корректные %(username)s и пароль. Оба поля чувствительны к регистру."),
        "inactive": _("This account is inactive."),
    }

    validator: UserValidatorInterface = get_user_validator()

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.username_field = "логин"
        self.fields["username"].label = "Email или телефон"
        self.fields["password"].label = "Пароль"

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field},
        )

    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email или телефон"}))
    password = forms.CharField(
        max_length=18, widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "autocomplete": "off"})
    )

    logger = AdminLoginLogger(get_admin_log_repository(), get_email_service(), get_system_repository())

    def clean_username(self):
        repository = get_user_repository()

        phone_or_email = self.cleaned_data["username"]
        phone_or_email = self.validator.validate_phone_or_email(phone_or_email)

        if phone_or_email is None:
            self.logger.error(self.request, self.cleaned_data, UserErrors.incorrect_login.value)
            self.add_error("username", UserErrors.incorrect_login.value)
            return phone_or_email

        user1 = repository.get_user_by_email(phone_or_email)
        user2 = repository.get_user_by_phone(phone_or_email)

        print(user1)
        print(user2)
        if not user1 and not user2:
            self.logger.error(self.request, self.cleaned_data, UserErrors.incorrect_login.value)

            self.add_error("username", UserErrors.incorrect_login.value)
            return phone_or_email

        return phone_or_email

    def clean(self):
        repository = get_user_repository()

        username = self.cleaned_data.get("username")

        user1 = repository.get_user_by_email(username)
        user2 = repository.get_user_by_phone(username)

        print(user1)
        print(user2)
        if not user1 and not user2:
            self.logger.error(self.request, self.cleaned_data, UserErrors.incorrect_login.value)
            self.add_error("username", UserErrors.incorrect_login.value)
            return self.cleaned_data

        if user1:
            user = user1
        if user2:
            user = user2

        password = self.cleaned_data.get("password")
        if user.check_password(password):
            print(user)
            if not user.superuser:
                self.logger.error(self.request, self.cleaned_data, "Недостаточно прав")
                return self.cleaned_data
            request = self.request
            request.user = user
            user = authenticate(request)
            self.logger.success(self.request, self.cleaned_data)
            return

        self.logger.error(self.request, self.cleaned_data, "Неверный пароль")

        return super().clean()
