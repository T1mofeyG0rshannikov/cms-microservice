from django import forms

from domain.user.validator import UserValidatorInterface
from infrastructure.user.validator import get_user_validator


class ChangeSiteForm(forms.Form):
    subdomain = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)
    font_id = forms.IntegerField()
    font_size = forms.IntegerField()
    logo = forms.FileField(required=False)
    logo_size = forms.IntegerField(required=False)
    owner = forms.CharField(max_length=200)
    contact_info = forms.CharField(max_length=200)
    domain_id = forms.IntegerField()
    delete_logo = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subdomain"].error_messages = {"required": "Укажите адрес своего сайта"}
        self.fields["name"].error_messages = {"required": "Укажите название своего сайта"}
        self.fields["font_id"].error_messages = {"required": "Это поле обязательное"}
        self.fields["font_size"].error_messages = {"required": "Это поле обязательное"}
        self.fields["owner"].error_messages = {"required": "Укажите свое имя или название организации"}
        self.fields["contact_info"].error_messages = {"required": "Укажите свой емейл, телефон или другой способ связи"}


class ChangeUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    second_name = forms.CharField(max_length=200)

    email = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=18)
    social_network = forms.CharField(required=False)
    adress = forms.CharField(required=False)

    profile_picture = forms.FileField(required=False)

    validator: UserValidatorInterface = get_user_validator()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].error_messages = {"required": "Укажите свое имя"}
        self.fields["second_name"].error_messages = {"required": "Укажите свою фамилию"}
        self.fields["email"].error_messages = {"required": "Это поле обязательное"}
        self.fields["phone"].error_messages = {"required": "Это поле обязательное"}

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not self.validator.is_valid_phone(phone):
            self.add_error("phone", "Укажите корректный телефон")

        return self.validator.get_raw_phone(phone)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not self.validator.is_valid_email(email):
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


class ChangeSocialsForm(forms.Form):
    socials = forms.CharField(max_length=5000)


class AddUserProductForm(forms.Form):
    product_id = forms.IntegerField(required=False)
    link = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    connected_with_link = forms.CharField(required=False)
    connected = forms.DateField(required=False)
    got = forms.DateField(required=False)
    profit = forms.DateField(required=False)

    screen = forms.ImageField(required=False)
