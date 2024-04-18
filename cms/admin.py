from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register
from .get_component import get_component
from .models import Component, ExampleComponent, Navbar, Page


class BaseComponentInline(admin.StackedInline):
    extra = 0
    max_num = 1
    
    def has_add_permission(self, request, obj):
        return get_component(obj) is None

class NavComponentInline(BaseComponentInline):
    model = Navbar
    fields = ["template", "title"]


class ExampleComponentInline(BaseComponentInline):
    model = ExampleComponent
    fields = ["template", "title", "body", "image1", "image2"]  


@register(Component)
class ComponentAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [NavComponentInline, ExampleComponentInline]
    list_display = ["page", "name"]


class PageComponentInline(SortableStackedInline, admin.StackedInline):
    model = Component
    extra = 0
    show_change_link = True


@register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title"]

    inlines = [PageComponentInline]
