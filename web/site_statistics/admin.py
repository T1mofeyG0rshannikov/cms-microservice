from django.contrib import admin

from web.common.admin import BaseInline
from web.site_statistics.models import (
    TryLoginToAdminPanel,
    TryLoginToFakeAdminPanel,
    UserAction,
    UserActivity,
)


class UserActionInline(BaseInline):
    model = UserAction
    fields = ["adress", "text"]
    readonly_fields = ["adress", "text"]


class UserActivityAdmin(admin.ModelAdmin):
    inlines = [UserActionInline]


admin.site.register(TryLoginToAdminPanel)
admin.site.register(TryLoginToFakeAdminPanel)
admin.site.register(UserActivity, UserActivityAdmin)
