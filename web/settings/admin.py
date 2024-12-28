from django.contrib import admin

from infrastructure.persistence.models.settings import (
    Domain,
    Font,
    FormLogo,
    GlobalStyles,
    Icon,
    LandingDomain,
    Logo,
    Messanger,
    SiteSettings,
    SocialNetwork,
    Trackers,
    UserFont,
)
from web.account.admin import MessangerAdmin, UserFontAdmin
from web.common.admin import SocialNetworkAdmin
from web.styles.admin import FontAdmin, GlobalStylesAdmin


class LogoInline(admin.StackedInline):
    model = Logo


class FormLogoInline(admin.StackedInline):
    model = FormLogo


class IconInline(admin.StackedInline):
    model = Icon


class SettingsAdmin(admin.ModelAdmin):
    inlines = [LogoInline, FormLogoInline, IconInline]


class DomainAdmin(admin.ModelAdmin):
    pass


admin.site.register(Domain, DomainAdmin)
admin.site.register(LandingDomain, DomainAdmin)
admin.site.register(SiteSettings, SettingsAdmin)
admin.site.register(GlobalStyles, GlobalStylesAdmin)
admin.site.register(Font, FontAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(Messanger, MessangerAdmin)
admin.site.register(UserFont, UserFontAdmin)
admin.site.register(Trackers)
