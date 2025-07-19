from django.contrib import admin

from infrastructure.persistence.models.settings import (
    Font,
    FormLogo,
    GlobalStyles,
    Icon,
    LandingDomain,
    Logo,
    SiteSettings,
    SocialNetwork,
    Trackers,
)
from web.styles.admin import FontAdmin, GlobalStylesAdmin


class LogoInline(admin.StackedInline):
    model = Logo


class FormLogoInline(admin.StackedInline):
    model = FormLogo


class IconInline(admin.StackedInline):
    model = Icon


class SettingsAdmin(admin.ModelAdmin):
    inlines = [LogoInline, FormLogoInline, IconInline]


admin.site.register(LandingDomain)
admin.site.register(SiteSettings, SettingsAdmin)
admin.site.register(GlobalStyles, GlobalStylesAdmin)
admin.site.register(Font, FontAdmin)
admin.site.register(SocialNetwork)
admin.site.register(Trackers)
