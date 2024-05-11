from django.contrib import admin
from .models import Logo, Icon
from django.contrib.admin.decorators import register


@register(Logo)
class LogoAdmin(admin.ModelAdmin):
    pass

@register(Icon)
class IconAdmin(admin.ModelAdmin):
    pass