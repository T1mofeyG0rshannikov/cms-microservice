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
    fields = ["action"]
    readonly_fields = fields

    def action(self, obj):
        return f"""{obj.time.strftime('%d.%m %H:%M:%S')}:{r"     "}{obj.adress} - {obj.text}"""

    action.short_description = ""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False


class UserActivityAdmin(admin.ModelAdmin):
    inlines = [UserActionInline]

    fields = ["ip", "start_time", "end_time", "banks_count", "pages_count", "popups_count", "auth"]

    readonly_fields = fields

    list_display = fields

    class Media:
        css = {"all": ("site_statistics/css/user_action_admin.css",)}


admin.site.register(TryLoginToAdminPanel)
admin.site.register(TryLoginToFakeAdminPanel)
admin.site.register(UserActivity, UserActivityAdmin)
