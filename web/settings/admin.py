from account.admin import MessangerAdmin, UserFontAdmin
from common.admin import SocialNetworkAdmin
from django.contrib import admin
from domens.admin import DomainAdmin
from styles.admin import FontAdmin, GlobalStylesAdmin

from .models import (
    Domain,
    Font,
    FormLogo,
    GlobalStyles,
    Icon,
    Logo,
    Messanger,
    SiteSettings,
    SocialNetwork,
    UserFont,
)


class LogoInline(admin.StackedInline):
    model = Logo


class FormLogoInline(admin.StackedInline):
    model = FormLogo


class IconInline(admin.StackedInline):
    model = Icon


class SettingsAdmin(admin.ModelAdmin):
    inlines = [LogoInline, FormLogoInline, IconInline]


admin.site.register(Domain, DomainAdmin)
admin.site.register(SiteSettings, SettingsAdmin)
admin.site.register(GlobalStyles, GlobalStylesAdmin)
admin.site.register(Font, FontAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(Messanger, MessangerAdmin)
admin.site.register(UserFont, UserFontAdmin)
