from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Component, ExampleComponent, Navbar, Page


class NavComponentInline(admin.StackedInline):
    model = Navbar
    extra = 0
    fields = ["template", "title"]


class ExampleComponentInline(admin.StackedInline):
    model = ExampleComponent
    extra = 0
    fields = ["template", "title", "body", "image1", "image2"]


@register(Component)
class ComponentAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [NavComponentInline, ExampleComponentInline]
    list_display = ["page"]


class PageComponentInline(SortableStackedInline, admin.StackedInline):
    model = Component
    extra = 0
    show_change_link = True


@register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title"]

    inlines = [PageComponentInline]
