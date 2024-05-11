from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Icon, Logo, SiteSettings


class LogoInline(admin.StackedInline):
    model = Logo
    max_num = 1
    extra = 0


class IconInline(admin.StackedInline):
    model = Icon
    max_num = 1
    extra = 0


@register(SiteSettings)
class SettingsAdmin(admin.ModelAdmin):
    inlines = [LogoInline, IconInline]
