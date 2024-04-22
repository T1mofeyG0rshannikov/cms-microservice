from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import MarginBlock, IconSize


@register(MarginBlock)
class MarginBlockAdmin(admin.ModelAdmin):
    pass

@register(IconSize)
class IconSizeAdmin(admin.ModelAdmin):
    pass