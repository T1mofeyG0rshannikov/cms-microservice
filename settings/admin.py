from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Icon, Logo, SiteSettings


class LogoInline(admin.StackedInline):
    model = Logo


class IconInline(admin.StackedInline):
    model = Icon


@register(SiteSettings)
class SettingsAdmin(admin.ModelAdmin):
    inlines = [LogoInline, IconInline]
