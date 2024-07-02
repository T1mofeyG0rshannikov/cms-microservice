from django.contrib import admin
from django.contrib.admin.decorators import register

from common.models import SocialNetwork


class BaseInline(admin.StackedInline):
    extra = 0


@register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    pass
