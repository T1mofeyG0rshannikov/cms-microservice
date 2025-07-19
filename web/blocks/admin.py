from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.utils.safestring import mark_safe

from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.blocks.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Footer,
    Navbar,
    QuestionsBlock,
    RegisterBlock,
    SocialMediaBlock,
    StagesBlock,
)
from infrastructure.persistence.models.blocks.blocks_components import (
    AdditionalCatalogProductType,
    CatalogProduct,
    CatalogProductType,
    Feature,
    FooterMenuItem,
    NavMenuItem,
    Question,
    SocialMediaButton,
    Stage,
)
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.blocks.common import Block, Page, Template
from infrastructure.persistence.models.blocks.landings import Landing, LandingBlock
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.admin.admin import BaseInline
from web.blocks.forms import PageBlockInlineForm
from web.styles.admin import (
    AdditionalCatalogCustomStylesInline,
    CatalogCustomStylesInline,
    ContentCustomStylesInline,
    CoverCustomStylesInline,
    FeaturesCustomStylesInline,
    FooterCustomStylesInline,
    MainPageCatalogCustomStylesInline,
    NavbarCustomStylesInline,
    PromoCatalogCustomStylesInline,
    QuestionsCustomStylesInline,
    RegisterCustomStylesInline,
    SocialCustomStylesInline,
    StagesCustomStylesInline,
)


class QuestionInline(BaseInline):
    model = Question


class NavMenuItemAdmin(BaseInline):
    model = NavMenuItem


class FooterMenuItemAdmin(BaseInline):
    model = FooterMenuItem


class FeatureInline(BaseInline):
    model = Feature


class SocialMediaButtonInline(BaseInline):
    model = SocialMediaButton


class StageInline(BaseInline):
    model = Stage


class PageBlockInline(SortableStackedInline, BaseInline):
    model = Block
    form = PageBlockInlineForm


class LandingBlockInline(SortableStackedInline, BaseInline):
    model = LandingBlock


class CatalogProductInline(SortableStackedInline, BaseInline):
    model = CatalogProduct
    repository: ProductRepositoryInterface = get_product_repository()

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields["offer"].queryset = self.repository.get_published_offers(obj.product_type_id)
        return formset


class MainPageCatalogProductInline(SortableStackedInline, BaseInline):
    model = CatalogProductType


class AdditionalCatalogProductInline(SortableStackedInline, BaseInline):
    model = AdditionalCatalogProductType


class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]


class BaseBlockAdmin(admin.ModelAdmin):
    change_form_template = "blocks/change_form.html"
    list_display = ["name", "template", "clone_button"]
    exclude = ["block_relation"]

    change_list_template = "blocks/change_list_page.html"

    def clone_button(self, obj):
        return mark_safe(
            f"""<button class="copy-button" onclick="cloneBlock({obj.id}, '{obj.__class__.__name__}')">Копировать</button>"""
        )

    clone_button.short_description = ""


class NavbarAdmin(BaseBlockAdmin):
    inlines = [NavMenuItemAdmin, NavbarCustomStylesInline]


class FooterAdmin(BaseBlockAdmin):
    inlines = [FooterMenuItemAdmin, FooterCustomStylesInline]


class ContentAdmin(BaseBlockAdmin):
    inlines = [ContentCustomStylesInline]


class CoverAdmin(BaseBlockAdmin):
    inlines = [CoverCustomStylesInline]


class FeaturesBlockAdmin(BaseBlockAdmin):
    inlines = [FeatureInline, FeaturesCustomStylesInline]


class RegisterBlockAdmin(BaseBlockAdmin):
    inlines = [RegisterCustomStylesInline]


class SocialMediaBlockAdmin(BaseBlockAdmin):
    inlines = [SocialMediaButtonInline, SocialCustomStylesInline]


class QuestionsBlockAdmin(BaseBlockAdmin):
    inlines = [QuestionInline, QuestionsCustomStylesInline]


class StagesBlockAdmin(BaseBlockAdmin):
    inlines = [StageInline, StagesCustomStylesInline]


class CatalogAdmin(SortableAdminBase, BaseBlockAdmin):
    inlines = [CatalogProductInline, CatalogCustomStylesInline]
    exclude = BaseBlockAdmin.exclude
    ordering = ["name"]


class MainPageCatalogBlogAdmin(SortableAdminBase, BaseBlockAdmin):
    inlines = [MainPageCatalogProductInline, MainPageCatalogCustomStylesInline]
    exclude = BaseBlockAdmin.exclude


class AdditionalCatalogBlogAdmin(SortableAdminBase, BaseBlockAdmin):
    inlines = [AdditionalCatalogProductInline, AdditionalCatalogCustomStylesInline]
    exclude = BaseBlockAdmin.exclude


class PromoCatalogAdmin(BaseBlockAdmin):
    inlines = [PromoCatalogCustomStylesInline]


class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "title", "clone_button"]
    change_list_template = "blocks/change_list_page.html"

    inlines = [PageBlockInline]

    def clone_button(self, obj):
        return mark_safe(f'<button class="copy-button" onclick="clonePage({obj.id})">Копировать</button>')

    clone_button.short_description = ""


class LandingAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["url", "logo", "name"]

    inlines = [LandingBlockInline]


admin.site.register(Page, PageAdmin)
admin.site.register(Landing, LandingAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(Navbar, NavbarAdmin)
admin.site.register(Cover, CoverAdmin)
admin.site.register(RegisterBlock, RegisterBlockAdmin)
admin.site.register(PromoCatalog, PromoCatalogAdmin)
admin.site.register(MainPageCatalogBlock, MainPageCatalogBlogAdmin)
admin.site.register(AdditionalCatalogBlock, AdditionalCatalogBlogAdmin)
admin.site.register(CatalogBlock, CatalogAdmin)
admin.site.register(ContentBlock, ContentAdmin)
admin.site.register(FeaturesBlock, FeaturesBlockAdmin)
admin.site.register(StagesBlock, StagesBlockAdmin)
admin.site.register(SocialMediaBlock, SocialMediaBlockAdmin)
admin.site.register(QuestionsBlock, QuestionsBlockAdmin)
admin.site.register(Template, TemplateAdmin)
