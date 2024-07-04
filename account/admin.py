from django.contrib import admin
from django.contrib.admin.decorators import register

from account.models import UserFont, UserSocialNetwork


@register(UserFont)
class UserFontAdmin(admin.ModelAdmin):
    pass


@register(UserSocialNetwork)
class UserSocialNetworkAdmin(admin.ModelAdmin):
    pass
