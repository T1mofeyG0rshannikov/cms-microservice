from django import forms

from catalog.models.product_type import ProductType
from catalog.models.products import Product


class ProductAdminForm(forms.ModelForm):
    product_types_choices = [("", "---------")] + [
        (product_type["id"], product_type["name"]) for product_type in ProductType.objects.values("id", "name").all()
    ]
    type1 = forms.ChoiceField(label="Тип", choices=product_types_choices, required=False)
    type2 = forms.ChoiceField(label="", choices=product_types_choices, required=False)
    type3 = forms.ChoiceField(label="", choices=product_types_choices, required=False)
    type4 = forms.ChoiceField(label="", choices=product_types_choices, required=False)

    class Meta:
        model = Product
        fields = "__all__"
