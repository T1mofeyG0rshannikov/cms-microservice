from django import forms


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
