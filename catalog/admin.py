from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register

from catalog.models import (
    Block,
    CatalogPageTemplate,
    Link,
    Organization,
    OrganizationType,
    Product,
    ProductType,
)
from common.admin import BaseInline


class LinkInline(BaseInline):
    model = Link


class BlockInline(SortableStackedInline, BaseInline):
    model = Block


@register(CatalogPageTemplate)
class CatalogPageTemplateAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [BlockInline]


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [LinkInline]


@register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    pass


@register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj):
        fieldsets = ((None, {"fields": ("name", "type", "logo", "site", "admin_hint"), "description": obj.admin_hint}),)
        return fieldsets


@register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
