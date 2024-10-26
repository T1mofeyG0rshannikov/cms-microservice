from django.contrib import admin

from infrastructure.persistence.models.styles.colors.colors import ColorStyles
from infrastructure.persistence.models.styles.other import IconSize, MarginBlock
from infrastructure.persistence.models.styles.styles.styles import (
    AdditionalCatalogCustomStyles,
    CatalogCustomStyles,
    ContentCustomStyles,
    CoverCustomStyles,
    FeaturesCustomStyles,
    FooterCustomStyles,
    MainPageCatalogCustomStyles,
    NavbarCustomStyles,
    PromoCatalogCustomStyles,
    QuestionsCustomStyles,
    RegisterCustomStyles,
    SocialCustomStyles,
    StagesCustomStyles,
)
from infrastructure.persistence.models.styles.texts.texts import (
    ExplanationText,
    HeaderText,
    MainText,
    SubheaderText,
)


class StyleInline(admin.StackedInline):
    pass


class NavbarCustomStylesInline(StyleInline):
    model = NavbarCustomStyles


class ContentCustomStylesInline(StyleInline):
    model = ContentCustomStyles


class CoverCustomStylesInline(StyleInline):
    model = CoverCustomStyles


class FeaturesCustomStylesInline(StyleInline):
    model = FeaturesCustomStyles


class RegisterCustomStylesInline(StyleInline):
    model = RegisterCustomStyles


class SocialCustomStylesInline(StyleInline):
    model = SocialCustomStyles


class QuestionsCustomStylesInline(StyleInline):
    model = QuestionsCustomStyles


class StagesCustomStylesInline(StyleInline):
    model = StagesCustomStyles


class FooterCustomStylesInline(StyleInline):
    model = FooterCustomStyles


class CatalogCustomStylesInline(StyleInline):
    model = CatalogCustomStyles


class MainPageCatalogCustomStylesInline(StyleInline):
    model = MainPageCatalogCustomStyles


class PromoCatalogCustomStylesInline(StyleInline):
    model = PromoCatalogCustomStyles


class AdditionalCatalogCustomStylesInline(StyleInline):
    model = AdditionalCatalogCustomStyles


class ColorStylesInline(StyleInline):
    model = ColorStyles


class HeaderTextInline(StyleInline):
    model = HeaderText


class MainTextInline(StyleInline):
    model = MainText


class SubheaderTextInline(StyleInline):
    model = SubheaderText


class ExplanationTextInline(StyleInline):
    model = ExplanationText


class MarginBlockInline(StyleInline):
    model = MarginBlock


class IconSizeInline(StyleInline):
    model = IconSize


class FontAdmin(admin.ModelAdmin):
    list_display = ["name", "link"]


class GlobalStylesAdmin(admin.ModelAdmin):
    inlines = [
        ColorStylesInline,
        HeaderTextInline,
        MainTextInline,
        SubheaderTextInline,
        ExplanationTextInline,
        MarginBlockInline,
        IconSizeInline,
    ]
