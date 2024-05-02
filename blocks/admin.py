from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register

from styles.admin import (
    ContentCustomStylesInline,
    CoverCustomStylesInline,
    NavbarCustomStylesInline,
)

# from .get_block import get_block
from .models.blocks import Cover, ExampleBlock, Navbar

# from .models.common import Block, BlockRelationship, Page, Template
from .models.common import Block, Page, Template

# from django.contrib.admin.views.main import ChangeList
# from django.utils.html import format_html


@register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]


class BaseBlockAdmin(admin.ModelAdmin):
    change_form_template = "blocks/change_form.html"
    list_display = ["name", "template"]
    exclude = ["block_relation"]


@register(Navbar)
class NavbarAdmin(BaseBlockAdmin):
    inlines = [NavbarCustomStylesInline]


@register(ExampleBlock)
class ExampleComponenAdmin(BaseBlockAdmin):
    inlines = [ContentCustomStylesInline]
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
    inlines = [CoverCustomStylesInline]


"""
class FooChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return "/foos/foo/"
"""
"""
@register(BlockRelationship)
class BlockRelationAdmin(admin.ModelAdmin):
    list_display = ["name", "content"]

    def content(self, block):
        return format_html(f"<a href='admin/styles'>Контент</a>")

    def name(self, block):
        return str(get_block(block))

    #def get_changelist(self, request, **kwargs):
    #    return FooChangeList

    # inlines = [NavbarAdminInline]
"""


class PageBlockInline(SortableStackedInline, admin.StackedInline):
    model = Block
    extra = 0


@register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title"]

    inlines = [PageBlockInline]
