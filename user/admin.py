from django.contrib import admin
from django.contrib.admin.decorators import register

from user.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    pass
