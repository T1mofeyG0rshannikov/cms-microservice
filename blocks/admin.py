from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register

from .models.common import Block, Page, Template
from .models.blocks import ExampleBlock, Navbar, Cover


@register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]


class BaseBlockAdmin(admin.ModelAdmin):
    list_display = ["name", "template"]
    exclude = ["block_relation"]


@register(Navbar)
class NavbarAdmin(BaseBlockAdmin):
    pass


@register(ExampleBlock)
class ExampleComponenAdmin(BaseBlockAdmin):
    pass
    '''def image1_show(self, obj):
        if obj.image1:
            return mark_safe(f"<img src='{obj.image1.url}' width='120' />")
        return "None"

    def image2_show(self, obj):
        if obj.image2:
            return mark_safe(f"<img src='{obj.image2.url}' width='120' />")
        return "None"

    image1_show.__name__ = "Первое изображение"
    image2_show.__name__ = "Второе изображение"'''

@register(Cover)
class CoverAdmin(BaseBlockAdmin):
    pass

class PageBlockInline(SortableStackedInline, admin.StackedInline):
    model = Block
    extra = 0


@register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title"]

    inlines = [PageBlockInline]
