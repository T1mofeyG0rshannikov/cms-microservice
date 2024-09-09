from django.contrib import admin
from django.db import models
from django.utils.html import mark_safe

from catalog.admin import CustomAdminFileWidget
from catalog.models.product_type import OfferTypeRelation, ProductType
from common.admin import BaseInline
from offers.forms import OfferAdminForm
from offers.models import Link, Offer


def get_product_types():
    return [("", "---------"), *ProductType.objects.all().values_list("id", "name")]


def get_initial_product_type(product_id, index):
    product_types = list(
        OfferTypeRelation.objects.select_related("type").filter(offer_id=product_id).values_list("type_id", flat=True)
    )

    try:
        return product_types[index]
    except IndexError:
        return 0


def get_initial_product_type_profit(product_id, index):
    product_types = list(
        OfferTypeRelation.objects.select_related("type").filter(offer_id=product_id).values_list("profit", flat=True)
    )

    try:
        return product_types[index]
    except IndexError:
        return 0


class LinkInline(BaseInline):
    model = Link
    template = "catalog/link_inline.html"


class OfferAdmin(admin.ModelAdmin):
    form = OfferAdminForm

    list_display = [
        "name_tag",
        "status_tag",
        "created_at_tag",
        "end_promotion_tag",
        "links",
        "is_promote",
        "for_partners",
    ]
    inlines = [LinkInline]
    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}

    def is_promote(self, obj):
        if obj.promote:
            return True

        return False

    def for_partners(self, obj):
        return obj.partner_program

    for_partners.short_description = "Партнерам"

    is_promote.boolean = True
    is_promote.short_description = "Промо"

    def links(self, obj):
        return obj.links.count()

    links.short_description = "Ссылки"

    def status_tag(self, obj):
        if obj.status == "Опубликовано":
            return True

        if obj.status == "Архив":
            return False

        return None

    status_tag.boolean = True
    status_tag.short_description = ""

    def name_tag(self, obj):
        return mark_safe(f'<a href="/admin/offers/offer/{obj.pk}/change/" >{obj.name}</a>')

    def created_at_tag(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def end_promotion_tag(self, obj):
        return obj.get_end_promotion.strftime("%Y-%m-%d")

    created_at_tag.short_description = "дата создания"
    created_at_tag.allow_tags = True

    end_promotion_tag.short_description = "Акция"
    end_promotion_tag.allow_tags = True

    name_tag.short_description = "имя"
    name_tag.allow_tags = True

    class Media:
        css = {"all": ("catalog/css/product_admin.css",)}

    TYPES_COUNT = 4

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["annotation"].widget.attrs["style"] = "width: 45em;"

        for i in range(self.TYPES_COUNT):
            form.base_fields[f"type{i + 1}"].choices = get_product_types()
            form.base_fields[f"type{i + 1}"].initial = get_initial_product_type(obj, i)

            form.base_fields[f"profit{i + 1}"].initial = get_initial_product_type_profit(obj, i)

        return form

    def get_fieldsets(self, request, obj):
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        "status",
                        "name",
                        "product",
                        ("type1", "profit1"),
                        ("type2", "profit2"),
                        ("type3", "profit3"),
                        ("type4", "profit4"),
                        "annotation",
                        "profit",
                        "description",
                        "terms_of_the_promotion",
                        ("partner_program", "verification_of_registration"),
                        ("promotion", "start_promotion", "end_promotion"),
                        "banner",
                        "promote",
                    ),
                    "description": obj.status if obj else None,
                },
            ),
        )
        return fieldsets

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        OfferTypeRelation.objects.filter(offer=obj).delete()

        for i in range(self.TYPES_COUNT):
            type = form.cleaned_data[f"type{i + 1}"]
            profit = form.cleaned_data[f"profit{i + 1}"]

            if type:
                offer_type, _ = OfferTypeRelation.objects.update_or_create(
                    offer=obj, type=ProductType.objects.get(id=type), profit=profit
                )

        super().save_model(request, obj, form, change)


admin.site.register(Offer, OfferAdmin)
