from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.html import format_html, mark_safe

from catalog.models.blocks import Block, CatalogPageTemplate
from catalog.models.products import (
    ExclusiveCard,
    Link,
    Organization,
    OrganizationType,
    Product,
    ProductType,
)
from common.admin import BaseInline


class LinkInline(BaseInline):
    model = Link
    template = "catalog/link_inline.html"


class BlockInline(SortableStackedInline, BaseInline):
    model = Block


class CatalogPageTemplateAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [BlockInline]


class CustomAdminFileWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        try:
            if hasattr(value, "url"):
                result.append(
                    f"""<a href="{value.url}" target="_blank">
                        <img
                            src="{value.url}" alt="{value}"
                            height="100"
                            style="object-fit: cover; margin-right: 30px;"
                        />
                        </a>"""
                )
        except ValueError:
            pass

        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "image_tag",
        "name_tag",
        "status_tag",
        "type",
        "organization",
        "created_at_tag",
        "end_promotion_tag",
        "links",
        "is_promote",
        "for_partners",
    ]
    inlines = [LinkInline]
    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}
    ordering = ["organization"]

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
        return mark_safe(f'<a href="/admin/catalog/product/{obj.pk}/change/" >{obj.name}</a>')

    def image_tag(self, obj):
        return mark_safe('<img src="%s" height="35" />' % (obj.cover.url))

    def created_at_tag(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def end_promotion_tag(self, obj):
        if obj.end_promotion is None:
            return None

        return obj.end_promotion.strftime("%Y-%m-%d")

    image_tag.short_description = ""
    image_tag.allow_tags = True

    created_at_tag.short_description = "дата создания"
    created_at_tag.allow_tags = True

    end_promotion_tag.short_description = "Акция"
    end_promotion_tag.allow_tags = True

    name_tag.short_description = "имя"
    name_tag.allow_tags = True

    class Media:
        css = {"all": ("catalog/css/custom_admin.css",)}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["annotation"].widget.attrs["style"] = "width: 45em;"

        return form

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
                        "type",
                        "annotation",
                        "profit",
                        "description",
                        "terms_of_the_promotion",
                        ("partner_program", "verification_of_registration"),
                        "partner_annotation",
                        "partner_bonus",
                        "partner_description",
                        ("promotion", "start_promotion", "end_promotion"),
                        "banner",
                        "promote",
                        "private",
                    ),
                    "description": obj.status if obj else None,
                },
            ),
        )
        return fieldsets


class OrganizationTypeAdmin(admin.ModelAdmin):
    pass


class OrganizationAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj):
        fieldsets = (
            (
                None,
                {
                    "fields": ("name", "type", "logo", "site", "admin_hint"),
                    "description": obj.admin_hint if obj else None,
                },
            ),
        )
        return fieldsets


class ProductTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ExclusiveCardAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(CatalogPageTemplate, CatalogPageTemplateAdmin)
admin.site.register(ExclusiveCard, ExclusiveCardAdmin)
