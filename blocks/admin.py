from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from styles.admin import (
    ContentCustomStylesInline,
    CoverCustomStylesInline,
    FeaturesCustomStylesInline,
    NavbarCustomStylesInline,
    RegisterCustomStylesInline,
)

from .models.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Navbar,
    RegisterBlock,
    SocialMediaBlock,
)
from .models.blocks_components import Feature, NavMenuItem, SocialMediaButton
from .models.common import Block, Page, Template


@register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]


class BaseBlockAdmin(admin.ModelAdmin):
    change_form_template = "blocks/change_form.html"
    list_display = ["name", "template"]
    exclude = ["block_relation"]


class NavMenuItemAdmin(admin.StackedInline):
    model = NavMenuItem
    extra = 0


@register(Navbar)
class NavbarAdmin(BaseBlockAdmin):
    inlines = [NavMenuItemAdmin, NavbarCustomStylesInline]


@register(ContentBlock)
class ContentComponenAdmin(BaseBlockAdmin):
    inlines = [ContentCustomStylesInline]


@register(Cover)
class CoverAdmin(BaseBlockAdmin):
    inlines = [CoverCustomStylesInline]


class FeatureInline(admin.StackedInline):
    model = Feature
    extra = 0


@register(FeaturesBlock)
class FeaturesBlockAdmin(BaseBlockAdmin):
    inlines = [FeatureInline, FeaturesCustomStylesInline]


@register(RegisterBlock)
class RegisterBlockAdmin(BaseBlockAdmin):
    inlines = [RegisterCustomStylesInline]


class SocialMediaButtonInline(admin.StackedInline):
    model = SocialMediaButton
    extra = 0


@register(SocialMediaBlock)
class SocialMediaBlockAdmin(BaseBlockAdmin):
    inlines = [SocialMediaButtonInline]


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
    list_display = ["url", "title", "your_custom_button"]
    change_list_template = "blocks/change_list_page.html"

    inlines = [PageBlockInline]

    def your_custom_button(self, obj):
        return mark_safe(f'<button class="copy-button" onclick="clonePage({obj.id})">Копировать</button>')

    your_custom_button.allow_tags = True

    your_custom_button.short_description = ""
