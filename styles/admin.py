from django.contrib import admin
from django.contrib.admin.decorators import register

from styles.models.colors.colors import ColorStyles
from styles.models.other import IconSize, MarginBlock
from styles.models.styles.styles import (
    CatalogCustomStyles,
    ContentCustomStyles,
    CoverCustomStyles,
    FeaturesCustomStyles,
    GlobalStyles,
    MainPageCatalogCustomStyles,
    NavbarCustomStyles,
    PromoCatalogCustomStyles,
    QuestionsCustomStyles,
    RegisterCustomStyles,
    SocialCustomStyles,
    StagesCustomStyles,
)
from styles.models.texts.font import Font
from styles.models.texts.texts import (
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


class CatalogCustomStylesInline(StyleInline):
    model = CatalogCustomStyles


class MainPageCatalogCustomStylesInline(StyleInline):
    model = MainPageCatalogCustomStyles


class PromoCatalogCustomStylesInline(StyleInline):
    model = PromoCatalogCustomStyles


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


@register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ["name", "link"]


@register(GlobalStyles)
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
