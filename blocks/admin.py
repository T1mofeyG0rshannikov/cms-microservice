from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from blocks.models.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Navbar,
    QuestionsBlock,
    RegisterBlock,
    SocialMediaBlock,
    StagesBlock,
)
from blocks.models.blocks_components import (
    CatalogProduct,
    CatalogProductType,
    Feature,
    NavMenuItem,
    Question,
    SocialMediaButton,
    Stage,
)
from blocks.models.catalog_block import CatalogBlock, MainPageCatalogBlock
from blocks.models.common import Block, Page, Template
from common.admin import BaseInline
from styles.admin import (
    CatalogCustomStylesInline,
    ContentCustomStylesInline,
    CoverCustomStylesInline,
    FeaturesCustomStylesInline,
    MainPageCatalogCustomStylesInline,
    NavbarCustomStylesInline,
    QuestionsCustomStylesInline,
    RegisterCustomStylesInline,
    SocialCustomStylesInline,
    StagesCustomStylesInline,
)


class QuestionInline(BaseInline):
    model = Question


class NavMenuItemAdmin(BaseInline):
    model = NavMenuItem


class FeatureInline(BaseInline):
    model = Feature


class SocialMediaButtonInline(BaseInline):
    model = SocialMediaButton


class StageInline(BaseInline):
    model = Stage


class PageBlockInline(SortableStackedInline, BaseInline):
    model = Block


class CatalogProductInline(SortableStackedInline, BaseInline):
    model = CatalogProduct


class MainPageCatalogProductInline(SortableStackedInline, BaseInline):
    model = CatalogProductType


@register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]


class BaseBlockAdmin(admin.ModelAdmin):
    change_form_template = "blocks/change_form.html"
    list_display = ["name", "template"]
    exclude = ["block_relation"]


@register(Navbar)
class NavbarAdmin(BaseBlockAdmin):
    inlines = [NavMenuItemAdmin, NavbarCustomStylesInline]


@register(ContentBlock)
class ContentComponenAdmin(BaseBlockAdmin):
    inlines = [ContentCustomStylesInline]


@register(Cover)
class CoverAdmin(BaseBlockAdmin):
    inlines = [CoverCustomStylesInline]


@register(FeaturesBlock)
class FeaturesBlockAdmin(BaseBlockAdmin):
    inlines = [FeatureInline, FeaturesCustomStylesInline]


@register(RegisterBlock)
class RegisterBlockAdmin(BaseBlockAdmin):
    inlines = [RegisterCustomStylesInline]


@register(SocialMediaBlock)
class SocialMediaBlockAdmin(BaseBlockAdmin):
    inlines = [SocialMediaButtonInline, SocialCustomStylesInline]


@register(QuestionsBlock)
class QuestionsBlockAdmin(BaseBlockAdmin):
    inlines = [QuestionInline, QuestionsCustomStylesInline]


@register(StagesBlock)
class StagesBlockAdmin(BaseBlockAdmin):
    inlines = [StageInline, StagesCustomStylesInline]


@register(CatalogBlock)
class CatalogBlogAdmin(SortableAdminBase, BaseBlockAdmin):
    inlines = [CatalogProductInline, CatalogCustomStylesInline]
    exclude = BaseBlockAdmin.exclude  # + ["product_type"]

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


@register(MainPageCatalogBlock)
class MainPageCatalogBlogAdmin(SortableAdminBase, BaseBlockAdmin):
    inlines = [MainPageCatalogProductInline, MainPageCatalogCustomStylesInline]
    exclude = BaseBlockAdmin.exclude

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


@register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title", "clone_button"]
    change_list_template = "blocks/change_list_page.html"

    inlines = [PageBlockInline]

    def clone_button(self, obj):
        return mark_safe(f'<button class="copy-button" onclick="clonePage({obj.id})">Копировать</button>')

    clone_button.short_description = ""
