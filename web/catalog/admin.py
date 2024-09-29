import os

from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.html import format_html, mark_safe

from web.admin.admin import redirect_to_change_page_tag
from web.catalog.forms import OfferAdminForm
from web.catalog.models.blocks import Block, CatalogPageTemplate
from web.catalog.models.product_type import ProductCategory, ProductType
from web.catalog.models.products import (
    ExclusiveCard,
    Link,
    Offer,
    OfferTypeRelation,
    Organization,
    OrganizationType,
    Product,
)
from web.common.admin import BaseInline


class BlockInline(SortableStackedInline, BaseInline):
    model = Block


class CatalogPageTemplateAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [BlockInline]


class CustomAdminFileWidget(AdminFileWidget):
    height = 100

    def render(self, name, value, attrs=None, renderer=None):
        result = []
        try:
            if hasattr(value, "url"):
                if self.height:
                    result.append(
                        f"""<a href="{value.url}" target="_blank">
                            <img
                                src="{value.url}" alt="{value}"
                                height="{self.height}"
                                style="object-fit: cover; margin-right: 30px;"
                            />
                            </a>"""
                    )
                elif self.width:
                    result.append(
                        f"""<a href="{value.url}" target="_blank">
                            <img
                                src="{value.url}" alt="{value}"
                                width="{self.width}"
                                style="object-fit: cover; margin-right: 30px;"
                            />
                            </a>"""
                    )
        except ValueError:
            pass

        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))


class CustomOrganizationLogo(CustomAdminFileWidget):
    height = None
    width = 300


class ProductAdmin(admin.ModelAdmin):
    list_display = ["image_tag", "name_tag", "status_tag", "category", "organization", "created_at_tag", "offers"]

    def offers(self, obj):
        return obj.offers.count()

    offers.short_description = "Офферы"

    def status_tag(self, obj):
        if obj.status == "Опубликовано":
            return True

        if obj.status == "Архив":
            return False

        return None

    status_tag.boolean = True
    status_tag.short_description = ""

    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}
    ordering = ["organization"]

    def name_tag(self, obj):
        return redirect_to_change_page_tag(obj, obj.name)

    def image_tag(self, obj):
        return mark_safe('<img src="%s" height="35" />' % (obj.cover.url))

    def created_at_tag(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    image_tag.short_description = ""
    image_tag.allow_tags = True

    created_at_tag.short_description = "дата создания"
    created_at_tag.allow_tags = True

    name_tag.short_description = "имя"
    name_tag.allow_tags = True

    class Media:
        css = {"all": ("catalog/css/product_admin.css",)}

    def get_fieldsets(self, request, obj):
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        "status",
                        "organization",
                        "cover",
                        "name",
                        "category",
                        "partner_annotation",
                        "partner_bonus",
                        "partner_description",
                        "private",
                    ),
                },
            ),
        )
        return fieldsets


class OrganizationTypeAdmin(admin.ModelAdmin):
    ordering = ["name"]


class ProductInline(BaseInline):
    model = Product

    fields = (
        "image_tag",
        "name_tag",
        "category",
        "organization",
        "created_at_tag",
    )

    readonly_fields = fields

    ordering = ["name"]

    def name_tag(self, obj):
        return redirect_to_change_page_tag(obj, obj.name)

    def image_tag(self, obj):
        return mark_safe('<img src="%s" height="35" />' % (obj.cover.url))

    def created_at_tag(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    image_tag.short_description = "картинка"
    image_tag.allow_tags = True

    created_at_tag.short_description = "дата создания"
    created_at_tag.allow_tags = True

    name_tag.short_description = "имя"
    name_tag.allow_tags = True

    def has_add_permission(self, *args, **kwargs):
        return False


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["image_tag", "name_tag", "type", "site", "products"]
    inlines = [ProductInline]
    formfield_overrides = {models.ImageField: {"widget": CustomOrganizationLogo}}

    def products(self, obj):
        return obj.products.count()

    products.short_description = "Продукты"

    admin_site_url = os.getenv("ADMIN_URL")

    def name_tag(self, obj):
        return redirect_to_change_page_tag(obj, obj.name)

    name_tag.short_description = "Название"

    ordering = ["name"]

    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="75" />' % (obj.logo.url))

    image_tag.short_description = ""

    def get_fieldsets(self, request, obj):
        fieldsets = (
            (
                None,
                {
                    "fields": ("name", "type", "logo", "site", "admin_hint", "partner_program"),
                    "description": obj.admin_hint if obj else None,
                },
            ),
        )
        return fieldsets

    class Media:
        css = {"all": ("catalog/css/organization_admin.css",)}


class ExclusiveCardAdmin(admin.ModelAdmin):
    pass


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "status_tag", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]

    def status_tag(self, obj):
        if obj.status == "Опубликовано":
            return True

        if obj.status == "Архив":
            return False

        return None

    status_tag.boolean = True
    status_tag.short_description = ""


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
    product_types = list(OfferTypeRelation.objects.filter(offer_id=product_id).values_list("profit", flat=True))

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
        "image_tag",
        "name_tag",
        "status_tag",
        "organization",
        "created_at_tag",
        "end_promotion_tag",
        "links",
        "is_promote",
        "for_partners",
    ]
    inlines = [LinkInline]
    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}

    def organization(self, obj):
        return obj.product.organization

    organization.short_description = "Организация"

    def image_tag(self, obj):
        return mark_safe('<img src="%s" height="35" />' % (obj.product.cover.url))

    image_tag.short_description = "картинка"
    image_tag.allow_tags = True

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
        return redirect_to_change_page_tag(obj, obj.name)

    def created_at_tag(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def end_promotion_tag(self, product):
        if product.promotion:
            start_promotion = product.start_promotion.strftime("%d.%m.%Y")
            end_promotion = product.get_end_promotion
            end_promotion = end_promotion.strftime("%d.%m.%Y")

            return f"{start_promotion}-{end_promotion}"

        return "Бессрочная акция"

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


class ProductCategoryAdmin(admin.ModelAdmin):
    ordering = ["name"]


admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(CatalogPageTemplate, CatalogPageTemplateAdmin)
admin.site.register(ExclusiveCard, ExclusiveCardAdmin)
