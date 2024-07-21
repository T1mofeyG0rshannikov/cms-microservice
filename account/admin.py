from django.contrib import admin

from account.models import Messanger, UserFont, UserSocialNetwork


class UserFontAdmin(admin.ModelAdmin):
    pass


class UserSocialNetworkAdmin(admin.ModelAdmin):
    pass


class MessangerAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserFont, UserFontAdmin)
admin.site.register(UserSocialNetwork, UserSocialNetworkAdmin)
admin.site.register(Messanger, MessangerAdmin)
