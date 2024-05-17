from django import forms
from django.core import validators

from utils.errors import UserErrors
from utils.validators import is_valid_phone


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}))
    phone = forms.CharField(max_length=18, widget=forms.TextInput(attrs={"placeholder": "+7 (777) 777-7777"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not is_valid_phone(phone):
            self.add_error("phone", UserErrors.incorrect_phone.value)

        return phone


class LoginForm(forms.Form):
    phone_or_email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email или телефон"}))
    password = forms.CharField(max_length=18, widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))

    def clean_phone_or_email(self):
        phone_or_email = self.cleaned_data["phone_or_email"]

        valid_as_email = validators.EmailValidator(phone_or_email)
        valid_as_phone = is_valid_phone(phone_or_email)

        if not valid_as_email and not valid_as_phone:
            self.add_error("phone_or_email", UserErrors.incorrect_login.value)

        return phone_or_email
