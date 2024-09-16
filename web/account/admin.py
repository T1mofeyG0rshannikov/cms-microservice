from django.contrib import admin

from web.account.models import UserSocialNetwork


class UserFontAdmin(admin.ModelAdmin):
    pass


class UserSocialNetworkAdmin(admin.ModelAdmin):
    pass


class MessangerAdmin(admin.ModelAdmin):
    pass


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(UserSocialNetwork, UserSocialNetworkAdmin)
