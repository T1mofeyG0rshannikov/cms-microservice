from django import forms
from django.db.utils import OperationalError

from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import Offer


def get_offer_types():
    try:
        return [("", "---------")] + [
            (product_type["id"], product_type["name"])
            for product_type in ProductType.objects.values("id", "name").all()
        ]
    except OperationalError:
        return [("", "---------")]


class OfferAdminForm(forms.ModelForm):
    offers_types_choices = get_offer_types()

    type1 = forms.ChoiceField(label="Тип", choices=offers_types_choices, required=False)
    type2 = forms.ChoiceField(label="", choices=offers_types_choices, required=False)
    type3 = forms.ChoiceField(label="", choices=offers_types_choices, required=False)
    type4 = forms.ChoiceField(label="", choices=offers_types_choices, required=False)

    profit1 = forms.CharField(label="", required=False)
    profit2 = forms.CharField(label="", required=False)
    profit3 = forms.CharField(label="", required=False)
    profit4 = forms.CharField(label="", required=False)

    class Meta:
        model = Offer
        fields = "__all__"
