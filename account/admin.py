from django.contrib import admin

from account.models import UserFont, UserSocialNetwork


class UserFontAdmin(admin.ModelAdmin):
    pass


class UserSocialNetworkAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserFont, UserFontAdmin)
admin.site.register(UserSocialNetwork, UserSocialNetworkAdmin)
