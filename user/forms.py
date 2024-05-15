from django import forms

from user.models import User
from utils.errors import UserErrors


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}))
    phone = forms.CharField(max_length=12, widget=forms.TextInput(attrs={"placeholder": "+7 (777) 777-7777"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        # user_exists = User.objects.filter(username=username).exists()

        # if user_exists:
        #    self.add_error("username", UserErrors.username_alredy_exists.value)
