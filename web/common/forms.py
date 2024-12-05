from django import forms

from application.texts.errors import UserErrors
from domain.user.validator import UserValidatorInterface
from infrastructure.user.validator import get_user_validator


class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}))
    phone = forms.CharField(max_length=18, widget=forms.TextInput(attrs={"placeholder": "+7 (777) 777-7777"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={"placeholder": "Сообщение"}))

    validator: UserValidatorInterface = get_user_validator()

    def clean_phone(self) -> str:
        phone = self.cleaned_data["phone"]
        phone = self.validator.get_raw_phone(phone)

        if not self.validator.is_valid_phone(phone):
            self.add_error("phone", UserErrors.incorrect_phone)

        return phone
