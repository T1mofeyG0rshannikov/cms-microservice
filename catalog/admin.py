from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.html import format_html, mark_safe

from catalog.models.blocks import Block, CatalogPageTemplate
from catalog.models.product_type import (
    ProductCategory,
    ProductType,
    ProductTypeRelation,
)
from catalog.models.products import (
    ExclusiveCard,
    Link,
    Organization,
    OrganizationType,
    Product,
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


def get_product_types():
    product_types = [("", "---------")]
    product_types.extend(list(ProductType.objects.all().values_list("id", "name")))

    return product_types


def get_initial_product_type(product_id, index):
    product_types = list(
        ProductTypeRelation.objects.select_related("type")
        .filter(product_id=product_id)
        .values_list("type_id", flat=True)
    )

    try:
        return product_types[index]
    except IndexError:
        return 0


class ProductAdminForm(forms.ModelForm):
    product_types_choices = [("", "---------")] + [
        (product_type.id, product_type.name) for product_type in ProductType.objects.all()
    ]
    type1 = forms.ChoiceField(label="Тип", choices=product_types_choices, required=False)
    type2 = forms.ChoiceField(label="", choices=product_types_choices, required=False)
    type3 = forms.ChoiceField(label="", choices=product_types_choices, required=False)
    type4 = forms.ChoiceField(label="", choices=product_types_choices, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if instance:
            # Здесь вы можете использовать ваш объект для изменения полей формы
            self.fields["type1"].choices = get_product_types()
            self.fields["type1"].initial = get_initial_product_type(instance, 0)

            self.fields["type2"].choices = get_product_types()
            self.fields["type2"].initial = get_initial_product_type(instance, 1)

            self.fields["type3"].choices = get_product_types()
            self.fields["type3"].initial = get_initial_product_type(instance, 2)

            self.fields["type4"].choices = get_product_types()
            self.fields["type4"].initial = get_initial_product_type(instance, 3)


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = [
        "image_tag",
        "name_tag",
        "status_tag",
        "category",
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
        return obj.get_end_promotion.strftime("%Y-%m-%d")

    image_tag.short_description = ""
    image_tag.allow_tags = True

    created_at_tag.short_description = "дата создания"
    created_at_tag.allow_tags = True

    end_promotion_tag.short_description = "Акция"
    end_promotion_tag.allow_tags = True

    name_tag.short_description = "имя"
    name_tag.allow_tags = True

    class Media:
        css = {"all": ("catalog/css/product_admin.css",)}

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
                        "category",
                        ("type1", "type2", "type3", "type4"),
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

    def save_model(self, request, obj, form, change):
        type1 = form.cleaned_data["type1"]
        type2 = form.cleaned_data["type2"]
        type3 = form.cleaned_data["type3"]
        type4 = form.cleaned_data["type4"]

        ProductTypeRelation.objects.filter(product=obj).delete()

        if type1:
            product_type1, _ = ProductTypeRelation.objects.update_or_create(
                product=obj, type=ProductType.objects.get(id=type1)
            )

        if type2:
            product_type2, _ = ProductTypeRelation.objects.update_or_create(
                product=obj, type=ProductType.objects.get(id=type2)
            )

        if type3:
            product_type3, _ = ProductTypeRelation.objects.update_or_create(
                product=obj, type=ProductType.objects.get(id=type3)
            )

        if type4:
            product_type4, _ = ProductTypeRelation.objects.update_or_create(
                product=obj, type=ProductType.objects.get(id=type4)
            )

        # Вызовем метод сохранения объекта
        super().save_model(request, obj, form, change)


class OrganizationTypeAdmin(admin.ModelAdmin):
    pass


class ProductInline(BaseInline):
    model = Product

    readonly_fields = [
        "image_tag",
        "name_tag",
        "status_tag",
        "category",
        "organization",
        "created_at_tag",
        "end_promotion_tag",
        "links",
        "is_promote",
        "for_partners",
    ]

    fields = (
        "image_tag",
        "name_tag",
        "status_tag",
        "category",
        "organization",
        "created_at_tag",
        "end_promotion_tag",
        "links",
        "is_promote",
        "for_partners",
    )

    ordering = ["name"]

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
    status_tag.short_description = "статус"

    def name_tag(self, obj):
        return mark_safe(f'<a href="/admin/catalog/product/{obj.pk}/change/" >{obj.name}</a>')

    def image_tag(self, obj):
        return mark_safe('<img src="%s" height="35" />' % (obj.cover.url))

    def created_at_tag(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def end_promotion_tag(self, obj):
        return obj.get_end_promotion.strftime("%Y-%m-%d")

    image_tag.short_description = "картинка"
    image_tag.allow_tags = True

    created_at_tag.short_description = "дата создания"
    created_at_tag.allow_tags = True

    end_promotion_tag.short_description = "Акция"
    end_promotion_tag.allow_tags = True

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


class ProductTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ExclusiveCardAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(CatalogPageTemplate, CatalogPageTemplateAdmin)
admin.site.register(ExclusiveCard, ExclusiveCardAdmin)
