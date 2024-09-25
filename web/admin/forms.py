from django import forms
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from application.usecases.user.get_admin import GetAdminUser
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist, UserNotAdmin
from domain.user.validator import UserValidatorInterface
from infrastructure.email_services.work_email_service.context_processor.context_processor import (
    get_work_email_context_processor,
)
from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator import (
    get_work_email_template_generator,
)
from infrastructure.logging.admin import AdminLoginLogger
from infrastructure.persistence.repositories.admin_log_repository import (
    get_admin_log_repository,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.user.validator import get_user_validator


def check_code(email: str, code: int) -> bool:
    repository = get_system_repository()

    return repository.code_exists(email, code)


def delete_login_code(email: str) -> None:
    repository = get_system_repository()

    repository.delete_user_code(email)


class CustomAuthenticationAdminForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("Пожалуйста введите корректные %(username)s и пароль. Оба поля чувствительны к регистру."),
        "inactive": _("This account is inactive."),
    }

    validator: UserValidatorInterface = get_user_validator()

    logging: bool = False
    code_submit: bool = False

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.username_field = "логин"
        self.fields["username"].label = "Email или телефон"
        self.fields["password"].label = "Пароль"
        self.fields["code"].label = "Код"

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

    code = forms.IntegerField(max_value=999999, widget=forms.TextInput(attrs={"placeholder": "Код"}))

    logger = AdminLoginLogger(
        get_admin_log_repository(),
        get_work_email_service(
            get_work_email_template_generator(get_work_email_context_processor()), get_system_repository()
        ),
    )
    get_admin_user_interactor = GetAdminUser(get_user_repository())

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        code = int(self.cleaned_data.get("code"))

        try:
            user = self.get_admin_user_interactor(username, password)

        except (UserDoesNotExist, UserNotAdmin, IncorrectPassword) as e:
            print(e, "error")
            self.add_error("username", str(e))
            if self.logging:
                self.logger.error(self.request, self.cleaned_data, str(e))
            return self.cleaned_data

        print(user, 4)

        if self.code_submit and not check_code(user.email, code):
            if self.logging:
                self.logger.error(self.request, self.cleaned_data, "неправильный код")

            self.add_error("code", "неправильный код")
            return self.cleaned_data

        request = self.request
        request.user = user
        user = authenticate(request)
        delete_login_code(username)
        if self.logging:
            self.logger.success(self.request, {"username": username})

        return
