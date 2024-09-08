from django import forms
from django.contrib.admin.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.validator.validator import get_user_validator
from user.validator.validator_interface import UserValidatorInterface
from utils.errors import UserErrors


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}))
    phone = forms.CharField(max_length=18, widget=forms.TextInput(attrs={"placeholder": "+7 (777) 777-7777"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))

    validator: UserValidatorInterface = get_user_validator()

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        phone = self.validator.get_raw_phone(phone)

        if not self.validator.is_valid_phone(phone):
            self.add_error("phone", UserErrors.incorrect_phone.value)

        return phone


class LoginForm(forms.Form):
    phone_or_email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email или телефон"}))
    password = forms.CharField(
        max_length=18, widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "autocomplete": "off"})
    )

    validator: UserValidatorInterface = get_user_validator()

    def clean_phone_or_email(self):
        phone_or_email = self.cleaned_data["phone_or_email"]
        phone_or_email = self.validator.validate_phome_or_email(phone_or_email)

        if phone_or_email is None:
            self.add_error("phone_or_email", UserErrors.incorrect_login.value)

        return phone_or_email


class SetPasswordForm(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    repeat_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Повтор пароля"})
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Ваш email или телефон"}),
        error_messages={"invalid": "Введите корректный email"},
    )


class CustomAuthenticationAdminForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("Пожалуйста введите корректные %(username)s и пароль. Оба поля чувствительны к регистру."),
        "inactive": _("This account is inactive."),
    }

    validator: UserValidatorInterface = get_user_validator()

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def clean_phone_or_email(self):
        phone_or_email = self.cleaned_data["phone_or_email"]
        phone_or_email = self.validator.validate_phome_or_email(phone_or_email)

        if phone_or_email is None:
            self.add_error("phone_or_email", UserErrors.incorrect_login.value)

        return phone_or_email


class AddIdeaForm(forms.Form):
    title = forms.CharField(max_length=60)
    description = forms.CharField(max_length=1000)
    category = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].error_messages = {"required": "Выберите категорию замечания или предложения"}
        self.fields["title"].error_messages = {
            "required": "Сформулируйте тему предложения",
            "max_length": f"Не более {self.fields['title'].max_length} символов с пробелами",
        }
        self.fields["description"].error_messages = {
            "required": "Опишите суть проблемы или идеи",
            "max_length": f"Не более {self.fields['description'].max_length} символов с пробелами",
        }
