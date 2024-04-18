from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from .models import Component, ComponentsName, ExampleComponent, Navbar, Page, Template


@register(ComponentsName)
class ComponentsNameAdmin(admin.ModelAdmin):
    list_display = ["name"]


@register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]


@register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    list_display = ["template", "title"]


@register(ExampleComponent)
class ExampleComponenAdmin(admin.ModelAdmin):
    list_display = ["template", "title", "body", "image1_show", "image2_show"]

    def image1_show(self, obj):
        if obj.image1:
            return mark_safe(f"<img src='{obj.image1.url}' width='120' />")
        return "None"

    def image2_show(self, obj):
        if obj.image2:
            return mark_safe(f"<img src='{obj.image2.url}' width='120' />")
        return "None"

    image1_show.__name__ = "Первое изображение"
    image2_show.__name__ = "Второе изображение"


@register(Component)
class ComponentAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["page", "name"]


class PageComponentInline(SortableStackedInline, admin.StackedInline):
    model = Component
    extra = 0
    # show_change_link = True


@register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title"]

    inlines = [PageComponentInline]
