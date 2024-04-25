from django.contrib import admin
from django.contrib.admin.decorators import register
from .models.colors import ColorStyles
from .models.texts import HeaderText, MainText, SubheaderText, ExplanationText
from .models.other_styles import MarginBlock, IconSize
from .models.common import GlobalStyles


class StyleInline(admin.StackedInline):
    extra = 0
    max_num = 1
    
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

@register(GlobalStyles)
class GlobalStylesAdmin(admin.ModelAdmin):
    inlines = [ColorStylesInline, HeaderTextInline, MainTextInline, SubheaderTextInline, ExplanationTextInline, MarginBlockInline, IconSizeInline]