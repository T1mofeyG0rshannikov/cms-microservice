from django.contrib import admin
from django.contrib.admin.decorators import register
from .models.texts import HeaderText, MainText, SubheaderText, ExplanationText


@register(HeaderText)
class HeaderTextAdmin(admin.ModelAdmin):
    pass
    
@register(MainText)
class MainTextAdmin(admin.ModelAdmin):
    pass

@register(SubheaderText)
class SubheaderAdmin(admin.ModelAdmin):
    pass

@register(ExplanationText)
class ExplanationTextAdmin(admin.ModelAdmin):
    pass