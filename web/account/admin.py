from django.contrib import admin

from infrastructure.persistence.models.account import UserSocialNetwork
from infrastructure.persistence.models.materials import DocumentFormatPattern
from web.common.admin import BaseInline


class UserFontAdmin(admin.ModelAdmin):
    pass


class UserSocialNetworkAdmin(admin.ModelAdmin):
    pass


class MessangerAdmin(admin.ModelAdmin):
    pass


class DocumentFormatterPatternAdmin(BaseInline):
    model = DocumentFormatPattern


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [DocumentFormatterPatternAdmin]


admin.site.register(UserSocialNetwork, UserSocialNetworkAdmin)
