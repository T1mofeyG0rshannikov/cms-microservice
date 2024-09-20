from django.contrib import admin

from web.account.admin import MessangerAdmin, UserFontAdmin
from web.common.admin import SocialNetworkAdmin
from web.domens.admin import DomainAdmin
from web.settings.models import (
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
from web.styles.admin import FontAdmin, GlobalStylesAdmin


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
