from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.html import format_html, mark_safe

from catalog.models.blocks import Block, CatalogPageTemplate
from catalog.models.product_type import ProductCategory, ProductType
from catalog.models.products import (
    ExclusiveCard,
    Organization,
    OrganizationType,
    Product,
)
from common.admin import BaseInline


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
    list_display = [
        "image_tag",
        "name_tag",
        "category",
        "organization",
        "created_at_tag",
    ]

    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}
    ordering = ["organization"]

    def name_tag(self, obj):
        return mark_safe(f'<a href="/admin/catalog/product/{obj.pk}/change/" >{obj.name}</a>')

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
    pass


class ProductInline(BaseInline):
    model = Product

    readonly_fields = [
        "image_tag",
        "name_tag",
        "category",
        "organization",
        "created_at_tag",
    ]

    fields = (
        "image_tag",
        "name_tag",
        "category",
        "organization",
        "created_at_tag",
    )

    ordering = ["name"]

    def name_tag(self, obj):
        return mark_safe(f'<a href="/admin/catalog/product/{obj.pk}/change/" >{obj.name}</a>')

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

    def name_tag(self, obj):
        return mark_safe(f'<a href="/admin/catalog/organization/{obj.pk}/change/" >{obj.name}</a>')

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
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(CatalogPageTemplate, CatalogPageTemplateAdmin)
admin.site.register(ExclusiveCard, ExclusiveCardAdmin)
