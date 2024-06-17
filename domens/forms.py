from django import forms

from domens.models import Site


class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = ["domain", "is_active"]
