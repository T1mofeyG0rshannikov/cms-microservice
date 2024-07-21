from django import forms

from utils.validators import is_valid_email, is_valid_phone


class ChangeSiteForm(forms.Form):
    site = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)
    font = forms.IntegerField()
    font_size = forms.IntegerField()
    logo = forms.FileField(required=False)
    logo_size = forms.IntegerField(required=False)
    owner = forms.CharField(max_length=200)
    contact_info = forms.CharField(max_length=200)
    socials = forms.CharField(max_length=5000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["site"].error_messages = {"required": "Это поле обязательное"}
        self.fields["name"].error_messages = {"required": "Это поле обязательное"}
        self.fields["font"].error_messages = {"required": "Это поле обязательное"}
        self.fields["font_size"].error_messages = {"required": "Это поле обязательное"}
        self.fields["owner"].error_messages = {"required": "Это поле обязательное"}
        self.fields["contact_info"].error_messages = {"required": "Это поле обязательное"}


class ChangeUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    second_name = forms.CharField(max_length=200)

    email = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=18)
    social_network = forms.CharField(required=False)
    adress = forms.CharField(required=False)

    profile_picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].error_messages = {"required": "Укажите свое имя"}
        self.fields["second_name"].error_messages = {"required": "Укажите свою фамилию"}
        self.fields["email"].error_messages = {"required": "Это поле обязательное"}
        self.fields["phone"].error_messages = {"required": "Это поле обязательное"}

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not is_valid_phone(phone):
            self.add_error("phone", "Укажите корректный телефон")

        return phone

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not is_valid_email(email):
            self.add_error("email", "Введите корректный email")

        return email


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    repeat_password = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["current_password"].error_messages = {"required": "Это поле обязательное"}
        self.fields["password"].error_messages = {"required": "Это поле обязательное"}
        self.fields["repeat_password"].error_messages = {"required": "Это поле обязательное"}

    def clean_password(self):
        password = self.cleaned_data["password"]

        if len(password) < 6:
            self.add_error("password", "Минимум 6 латинских букв и цифр")

        return password
