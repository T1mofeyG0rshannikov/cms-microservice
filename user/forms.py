from django import forms

from user.models import User
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
