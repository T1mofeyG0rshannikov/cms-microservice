from django import forms

from utils.errors import UserErrors
from utils.format_phone import get_raw_phone
from utils.validators import is_valid_email, is_valid_phone
import unicodedata

from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}))
    phone = forms.CharField(max_length=18, widget=forms.TextInput(attrs={"placeholder": "+7 (777) 777-7777"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        phone = get_raw_phone(phone)

        if not is_valid_phone(phone):
            self.add_error("phone", UserErrors.incorrect_phone.value)

        return phone


class LoginForm(forms.Form):
    phone_or_email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email или телефон"}))
    password = forms.CharField(
        max_length=18, widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "autocomplete": "off"})
    )

    def clean_phone_or_email(self):
        phone_or_email = self.cleaned_data["phone_or_email"]

        valid_as_email = is_valid_email(phone_or_email)
        valid_as_phone = is_valid_phone(get_raw_phone(phone_or_email))

        if not valid_as_email and not valid_as_phone:
            self.add_error("phone_or_email", UserErrors.incorrect_login.value)

        if valid_as_email:
            return phone_or_email
        else:
            return get_raw_phone(phone_or_email)


class SetPasswordForm(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    repeat_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Повтор пароля"})
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))

from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.admin.forms import AuthenticationForm

class CustomAuthenticationAdminForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(forms.Form, self).__init__(*args, **kwargs)


    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
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
            params={"username": self.username_field.verbose_name},
        )
        
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email или телефон"}))
    password = forms.CharField(
        max_length=18, widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "autocomplete": "off"})
    )

    def clean_phone_or_email(self):
        phone_or_email = self.cleaned_data["phone_or_email"]

        valid_as_email = is_valid_email(phone_or_email)
        valid_as_phone = is_valid_phone(get_raw_phone(phone_or_email))

        if not valid_as_email and not valid_as_phone:
            self.add_error("phone_or_email", UserErrors.incorrect_login.value)

        if valid_as_email:
            return phone_or_email
        else:
            return get_raw_phone(phone_or_email)